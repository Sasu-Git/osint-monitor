"""Phase 1 (evaluations/system/full-basis-audit.md): run ledger, membership time, publication time kept apart
from creation time, and migration 5 on an existing database."""

import re
from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from osint_monitor.core import runs
from osint_monitor.core.database import Base, Event, EventItem, PipelineRun, RawItem, Source
from osint_monitor.core.migrations import current_version, head_version, run_migrations


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'r.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    yield factory
    engine.dispose()


def _source(s):
    src = Source(name="Wire", type="rss", url="https://w.invalid/")
    s.add(src)
    s.flush()
    return src


def _item(s, src, n, published):
    item = RawItem(source_id=src.id, external_id=str(n), title=f"item {n}", content="c", url=f"https://w/{n}",
                   content_hash=f"h{n}", published_at=published, fetched_at=datetime(2026, 9, 30, 12),
                   ingested_run_id=runs.current_run_id())
    s.add(item)
    s.flush()
    return item


# --- the ledger ---------------------------------------------------------------------------------

def test_run_ids_are_opaque_unique_and_not_time_derived(db):
    s = db()
    ids = set()
    for _ in range(3):
        run, token = runs.start_run(s, "tier", tier="warm", started_at=datetime(2026, 9, 30, 8))
        runs.finish_run(s, run, token, {"stages": {"clustering": "ok"}, "new_items": 0})
        ids.add(run.id)
    assert len(ids) == 3                                             # same start time, different ids
    assert all(re.fullmatch(r"[0-9a-f]{32}", i) for i in ids)
    assert runs.current_run_id() is None                            # ended runs are no longer current


def test_a_run_records_its_outcome_and_versions(db):
    s = db()
    run, token = runs.start_run(s, "tier", tier="hot")
    assert runs.current_run_id() == run.id
    runs.finish_run(s, run, token, {"new_items": 4, "stages": {"clustering": "ok", "geocoding": "failed: X"}},
                    items_collected=9)
    row = db().get(PipelineRun, run.id)
    assert (row.status, row.items_collected, row.items_new) == ("partial", 9, 4)
    assert row.finished_at is not None and row.config_hash and row.models.get("embedding")
    run, token = runs.start_run(s, "oneshot")
    runs.finish_run(s, run, token, error=RuntimeError("boom"))
    assert db().get(PipelineRun, run.id).status == "failed"


# --- stamps --------------------------------------------------------------------------------------

def test_memberships_record_their_run_and_publication_time_stays_apart_from_creation(db):
    from osint_monitor.processors.clustering import persist_clusters
    s = db()
    src = _source(s)
    run1, t1 = runs.start_run(s, "tier", tier="warm")
    a = _item(s, src, 1, datetime(2026, 9, 28, 6))
    b = _item(s, src, 2, datetime(2026, 9, 29, 7))
    d = _item(s, src, 4, datetime(2026, 9, 29, 9))                   # ingested in run 1, not clustered yet
    s.commit()
    persist_clusters(s, [{"item_ids": [a.id, b.id], "summary": "story", "severity": 0.1}])
    runs.finish_run(s, run1, t1)

    run2, t2 = runs.start_run(s, "tier", tier="warm")
    c = _item(s, src, 3, datetime(2026, 9, 27, 5))                   # published earlier than a and b
    s.commit()
    persist_clusters(s, [{"item_ids": [a.id, c.id, d.id], "summary": "story", "severity": 0.1}])
    runs.finish_run(s, run2, t2)
    a_id, b_id, c_id, d_id, r1, r2 = a.id, b.id, c.id, d.id, run1.id, run2.id

    s = db()
    event = s.query(Event).one()
    members = {m.item_id: m for m in s.query(EventItem).filter_by(event_id=event.id)}
    items = {i.id: i for i in s.query(RawItem)}
    assert members[a_id].added_run_id == r1 and members[b_id].added_run_id == r1
    assert members[c_id].added_run_id == r2 and items[c_id].ingested_run_id == r2
    # the three facts stay distinguishable: new item (c), existing item newly attached (d), unchanged (a)
    assert items[d_id].ingested_run_id == r1 and members[d_id].added_run_id == r2
    assert items[a_id].ingested_run_id == r1 and members[a_id].added_run_id == r1
    assert all(m.added_at is not None for m in members.values())
    assert event.earliest_published_at == datetime(2026, 9, 27, 5)
    assert event.first_reported_at != event.earliest_published_at    # creation time is not publication time


def test_a_membership_can_exist_only_once(db):
    from sqlalchemy.exc import IntegrityError
    s = db()
    src = _source(s)
    a = _item(s, src, 1, None)
    event = Event(summary="e")
    s.add(event)
    s.flush()
    s.add(EventItem(event_id=event.id, item_id=a.id))
    s.flush()
    s.add(EventItem(event_id=event.id, item_id=a.id))
    with pytest.raises(IntegrityError):
        s.flush()


# --- migration 5 ---------------------------------------------------------------------------------

V5_ONLY = ("ingested_run_id", "added_at", "added_run_id", "earliest_published_at", "uq_event_item")


def _v4_ddl(engine, table):
    """The model's CREATE TABLE for ``table`` without the columns and constraints migration 5 adds."""
    from sqlalchemy.schema import CreateTable
    lines = str(CreateTable(Base.metadata.tables[table]).compile(engine)).splitlines()
    kept = [l for l in lines if not any(k in l for k in V5_ONLY)]
    return re.sub(r",\s*\n(\s*)\)", r"\n\1)", "\n".join(kept).rstrip())


def _insert(conn, table, **values):
    """INSERT with every other NOT NULL column filled with a neutral value of its type."""
    for col in inspect(conn).get_columns(table):
        if col["name"] in values or col["nullable"] or col.get("autoincrement") is True:
            continue
        kind = str(col["type"]).upper()
        values[col["name"]] = ("2026-09-21 00:00:00" if "DATE" in kind else
                               0 if any(k in kind for k in ("INT", "FLOAT", "BOOL", "NUMERIC")) else "x")
    cols = ", ".join(values)
    conn.execute(text(f"INSERT INTO {table} ({cols}) VALUES ({', '.join(':' + c for c in values)})"), values)


def test_migration_5_adds_the_stamps_backfills_publication_time_and_invents_no_membership_time(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'v4.db'}")
    with engine.begin() as conn:                     # v4 shapes of the three tables migration 5 changes
        for table in ("raw_items", "events", "event_items"):
            conn.execute(text(_v4_ddl(engine, table)))
    Base.metadata.create_all(engine)                 # every other table, as at v4
    with engine.begin() as conn:
        conn.execute(text("INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', '4')"))
        _insert(conn, "sources", id=1, name="Wire", type="rss", url="u")
        for n, pub in ((1, "2026-09-20 10:00:00"), (2, "2026-09-18 09:00:00")):
            _insert(conn, "raw_items", id=n, source_id=1, title="t", content_hash=f"h{n}", published_at=pub)
        _insert(conn, "events", id=1, summary="e", first_reported_at="2026-09-21 01:00:00")
        for i, item in ((1, 1), (2, 2), (3, 1)):
            _insert(conn, "event_items", id=i, event_id=1, item_id=item)
    assert "ingested_run_id" not in {c["name"] for c in inspect(engine).get_columns("raw_items")}

    assert run_migrations(engine, backup_dir=tmp_path / "backups") == head_version() == 5
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, added_at, added_run_id FROM event_items ORDER BY id")).fetchall()
        assert [r[0] for r in rows] == [1, 2]                        # identical duplicate removed, oldest kept
        assert all(r[1] is None and r[2] is None for r in rows)       # unknown time is not invented
        assert str(conn.execute(text("SELECT earliest_published_at FROM events")).scalar()).startswith("2026-09-18")
        idx = {i["name"] for i in inspect(conn).get_indexes("event_items")}
        assert {"uq_event_item", "ix_event_items_item", "ix_event_items_added_run_id"} <= idx
        assert "ingested_run_id" in {c["name"] for c in inspect(conn).get_columns("raw_items")}
    assert current_version(engine) == 5
    assert (tmp_path / "backups").exists()                           # pre-migration backup taken
    engine.dispose()
