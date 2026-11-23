"""repair_situations.invalid_reason validates actor sets through the Situation canonicaliser (2026-11-23)."""
import importlib.util
from pathlib import Path

import pytest

from osint_monitor.processors.actors import ActorNormalizer

_spec = importlib.util.spec_from_file_location("repair_situations",
                                               Path(__file__).resolve().parents[1] / "scripts" / "repair_situations.py")
repair = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(repair)


@pytest.fixture(scope="module")
def norm():
    return ActorNormalizer.load()


@pytest.mark.parametrize("actors", [["Elon Musk", "Musk"], ["Christa Pike", "Pike"], ["Javier Milei", "Milei"],
                                    ["Machado", "Maria Corina Machado"]])
def test_name_variant_pairs_are_invalid(norm, actors):
    assert repair.invalid_reason(actors, norm, 2) is not None


@pytest.mark.parametrize("actors", [["China", "United States"], ["Israel", "Palestine"], ["Rachel", "Simon"],
                                    ["Jair Bolsonaro", "Flávio Bolsonaro"]])
def test_valid_or_unchanged_sets_pass(norm, actors):
    assert repair.invalid_reason(actors, norm, 2) is None


def test_previous_findings_still_found(norm):
    assert "collapse" in repair.invalid_reason(["Donald J. Trump", "United States"], norm, 2)
    assert "no longer actors" in repair.invalid_reason(["Democrat", "United States"], norm, 2)


def _db(tmp_path):
    from datetime import datetime
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.database import Base, Event, Situation
    p = tmp_path / "t.db"
    engine = create_engine(f"sqlite:///{p.as_posix()}")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    now = datetime(2026, 10, 13, 12)
    s.add(Situation(id=18, slug="rachel-simon", title="t", status="dormant", primary_actors=["Rachel", "Simon"],
                    created_at=now, updated_at=now))
    s.add(Situation(id=19, slug="israel-palestine", title="t", status="active", primary_actors=["Israel", "Palestine"],
                    created_at=now, updated_at=now))
    for eid, sid in ((402, 18), (429, 18), (5, 19)):
        s.add(Event(id=eid, summary=f"e{eid}", situation_id=sid, first_reported_at=now, last_updated_at=now))
    s.commit()
    s.close()
    engine.dispose()
    return p


def test_allow_list_retires_exactly_the_listed_ids(tmp_path):
    db = _db(tmp_path)
    out = tmp_path / "r.json"
    assert repair.main(["--db", str(db), "--only", "18:rachel-simon", "--apply", "--backup-dir", str(tmp_path / "b"),
                        "--out", str(out)]) == 0
    import json, sqlite3
    r = json.loads(out.read_text(encoding="utf-8"))
    assert [x["id"] for x in r["invalid"]] == [18] and r["invalid"][0]["developments"] == [402, 429]
    assert r["after"][0]["status"] == "closed" and r["after"][0]["members"] == 0
    c = sqlite3.connect(db)
    assert c.execute("select situation_id from events where id=5").fetchone()[0] == 19       # untouched


def test_allow_list_refuses_mismatched_slug_and_regroup(tmp_path):
    db = _db(tmp_path)
    assert repair.main(["--db", str(db), "--only", "18:wrong-slug"]) == 3
    assert repair.main(["--db", str(db), "--only", "18:rachel-simon", "--regroup"]) == 2
