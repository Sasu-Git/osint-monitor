"""Membership-decision provenance (core/membership_log.py): records for accepted and held decisions, the dedup
path, ordinary attachment, explicit nulls, rotation, failure isolation, and no effect on identity or the database."""

import json
from datetime import datetime

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from osint_monitor.core import membership_log
from osint_monitor.core.database import Base, Event, EventItem, RawItem
from osint_monitor.processors.clustering import persist_clusters
from tests.test_development_identity import QUAKE, UNRELATED, add, db, developments  # noqa: F401  (fixture)


def records(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.exists() else []


@pytest.fixture
def log_on(tmp_path, monkeypatch):
    path = tmp_path / "decisions.jsonl"
    monkeypatch.setenv("OSINT_MEMBERSHIP_LOG", "true")
    monkeypatch.setenv("OSINT_MEMBERSHIP_LOG_PATH", str(path))
    return path


def scenario(s):
    """A quake Development formed by two reports, then an update that continues it and an unrelated item held."""
    a, b = add(s, *QUAKE[0]), add(s, *QUAKE[1])
    s.commit()
    persist_clusters(s, [{"item_ids": [a, b], "summary": "q"}])
    c, u = add(s, *QUAKE[2], hours=3), add(s, *UNRELATED, hours=3)
    s.commit()
    persist_clusters(s, [{"item_ids": [b, c, u], "summary": "q"}])
    return a, b, c, u


def test_off_by_default_writes_nothing(db, tmp_path):
    assert membership_log.writer() is None                     # conftest: default off
    scenario(db())
    assert not (tmp_path / "membership_decisions.jsonl").exists()


def test_formation_attachment_and_held_records(db, log_on):
    s = db()
    a, b, c, u = scenario(s)
    rs = records(log_on)
    by = {(r["item_id"], r["path"]): r for r in rs}
    event_id = s.query(EventItem).filter_by(item_id=a).one().event_id
    for i in (a, b):                                            # formation: accepted, linked to the other founder
        r = by[(i, "formation")]
        assert r["decision"] == "accepted" and r["event_id"] == event_id
        assert r["supporting_member_ids"] == [b if i == a else a] and r["best_cosine"] > 0.53
        assert r["independent_origins"] == 2 and r["reason"].startswith("new Development")
    r = by[(c, "late_attachment")]                              # ordinary attachment to an existing Development
    assert r["decision"] == "accepted" and r["event_id"] == event_id
    assert set(r["supporting_member_ids"]) <= {a, b} and r["n_links"] >= 1 and r["competing_event_ids"] == []
    assert r["segmentation"] == "no guard on the supporting link" and r["cluster_fingerprint"]
    r = by[(u, "held")]                                         # rejected: linked to no member
    assert r["decision"] == "rejected" and r["event_id"] is None
    assert r["reason"] == "linked to no member of an overlapping Development" and r["supporting_member_ids"] == []


def test_missing_optional_fields_are_explicit_nulls(tmp_path):
    path = tmp_path / "x.jsonl"
    membership_log.Writer(path, 10_000, 2).record(item_id=7, decision="accepted", path="formation")
    [r] = records(path)
    assert set(r) == set(membership_log.FIELDS)
    assert r["item_id"] == 7 and r["at"] and r["core_check"] is None and r["actors_compatible"] is None


def test_rotation_is_bounded(tmp_path):
    path = tmp_path / "rot.jsonl"
    w = membership_log.Writer(path, 1_000, 2)
    for i in range(200):
        w.record(item_id=i, decision="accepted", path="formation", reason="x" * 40)
    files = sorted(p.name for p in tmp_path.iterdir())
    assert files == ["rot.jsonl", "rot.jsonl.1", "rot.jsonl.2"]          # oldest backups dropped
    assert all((tmp_path / f).stat().st_size <= 1_000 for f in files)
    assert records(path)[-1]["item_id"] == 199


def test_write_failure_never_fails_the_pipeline(db, tmp_path, monkeypatch):
    blocked = tmp_path / "is_a_directory"
    blocked.mkdir()
    membership_log.Writer(blocked, 10_000, 2).record(item_id=1)        # cannot open a directory: swallowed
    monkeypatch.setenv("OSINT_MEMBERSHIP_LOG", "true")
    monkeypatch.setenv("OSINT_MEMBERSHIP_LOG_PATH", str(blocked))
    s = db()
    scenario(s)
    assert len(developments(s)) == 1                                    # identity unaffected


def test_logging_changes_no_membership_and_no_schema(tmp_path, monkeypatch):
    results = []
    for on in (False, True):
        monkeypatch.setenv("OSINT_MEMBERSHIP_LOG", "true" if on else "false")
        monkeypatch.setenv("OSINT_MEMBERSHIP_LOG_PATH", str(tmp_path / f"log{on}.jsonl"))
        engine = create_engine(f"sqlite:///{tmp_path / f'm{on}.db'}")
        Base.metadata.create_all(engine)
        s = sessionmaker(bind=engine)()
        scenario(s)
        results.append((developments(s), sorted(inspect(engine).get_table_names()),
                        [(e.id, e.summary) for e in s.query(Event).order_by(Event.id)]))
        s.close()
        engine.dispose()
    assert results[0] == results[1]
    assert records(tmp_path / "logTrue.jsonl") and not (tmp_path / "logFalse.jsonl").exists()


def test_dedup_path_record(db, log_on, monkeypatch):
    from osint_monitor.core.models import RawItemModel
    from osint_monitor.processors import pipeline
    s = db()
    a, b = add(s, *QUAKE[0]), add(s, *QUAKE[1])
    s.commit()
    persist_clusters(s, [{"item_ids": [a, b], "summary": "q"}])
    existing = s.get(RawItem, a)

    class NearDuplicate:
        def deduplicate(self, item):
            return {"is_duplicate": False, "duplicate_type": "near_different_source", "existing_item": existing,
                    "similarity": 0.97, "content_hash": "dup-1", "embedding": None}

    monkeypatch.setattr(pipeline, "extract_entities", lambda text, lang="en": [])
    item = RawItemModel(source_name="Outlet Z", source_type="rss", url="https://z.invalid/1", external_id="z1",
                        title=QUAKE[0][1], content="", published_at=datetime(2026, 9, 30, 9), fetched_at=datetime(2026, 9, 30, 9))
    pipeline._process_single_item(s, item, NearDuplicate(), resolver=None, stats={"duplicates": 0, "new_items": 0,
                                                                                      "entities_extracted": 0})
    s.commit()
    new_id = s.query(RawItem).filter_by(external_id="z1").one().id
    [r] = [r for r in records(log_on) if r["path"] == "dedup"]
    assert r["item_id"] == new_id and r["supporting_member_ids"] == [a] and r["similarity"] == 0.97
    assert r["event_id"] == s.query(EventItem).filter_by(item_id=a).one().event_id and r["source"] == "Outlet Z"
