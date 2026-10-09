"""Phase 3 relation contract and persistence (processors/development_relations.py)."""
from datetime import datetime
from pathlib import Path

import pytest
import yaml
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, DevelopmentRelation, Event, EventItem, RawItem, Source
from osint_monitor.core.migrations import run_migrations
from osint_monitor.processors.development_relations import (
    GOLD_ONLY_TYPES, RUNTIME_TYPES, Proposal, RelationError, record, relations_of,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'rel.db'}")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    src = Source(name="Wire", type="rss", url="u")
    s.add(src)
    s.flush()
    for n in range(1, 4):
        s.add(RawItem(id=n, source_id=src.id, title=f"item {n}", content_hash=f"h{n}"))
        s.add(Event(id=10 * n, summary=f"development {n}"))
        s.flush()
        s.add(EventItem(event_id=10 * n, item_id=n))
    s.commit()
    yield s
    s.close()
    engine.dispose()


def explicit(source_item, target_item):
    return [{"item_id": source_item, "side": "source", "cue": "condemns", "text": "condemns the strike"},
            {"item_id": target_item, "side": "target", "cue": None, "text": "the strike"}]


# the contract


def test_runtime_types_are_the_owner_decision():
    manifest = yaml.safe_load((ROOT / "evaluations/relations/gold/manifest.yaml").read_text(encoding="utf-8"))
    runtime = manifest["runtime_taxonomy"]
    assert set(RUNTIME_TYPES) == {t for t, plan in runtime.items() if str(plan).startswith("implement")}
    assert set(GOLD_ONLY_TYPES) == {t for t, plan in runtime.items() if not str(plan).startswith("implement")}
    assert RUNTIME_TYPES["reaction_to"].roles == ("reaction", "trigger")
    assert not RUNTIME_TYPES["same_calamity_lifecycle"].directed and not RUNTIME_TYPES["same_convened_event"].directed


def test_runtime_types_are_defined_in_the_taxonomy():
    taxonomy = (ROOT / "evaluations/relations/taxonomy.md").read_text(encoding="utf-8")
    for name in RUNTIME_TYPES:
        assert f"| `{name}` |" in taxonomy
    assert "**reaction → trigger**" in taxonomy


# persistence


def test_an_explicit_reaction_is_stored_with_its_roles(db):
    row = record(db, Proposal("reaction_to", 20, 10, "accepted", "explicit", "test", explicit(2, 1)))
    assert (row.source_event_id, row.target_event_id) == (20, 10)        # reaction -> trigger, not reordered
    assert relations_of(db, 10)[0].id == row.id and relations_of(db, 20)[0].id == row.id


def test_symmetric_types_are_stored_lower_id_first_with_evidence_sides_swapped(db):
    row = record(db, Proposal("same_calamity_lifecycle", 30, 10, "accepted", "explicit", "test", explicit(3, 1)))
    assert (row.source_event_id, row.target_event_id) == (10, 30)
    assert {e["item_id"]: e["side"] for e in row.evidence} == {3: "target", 1: "source"}


def test_recording_twice_updates_one_row(db):
    record(db, Proposal("same_convened_event", 10, 20, "candidate", "none", "rule-v1"))
    row = record(db, Proposal("same_convened_event", 20, 10, "accepted", "explicit", "rule-v2", explicit(2, 1)))
    assert db.query(DevelopmentRelation).count() == 1
    assert (row.status, row.method) == ("accepted", "rule-v2")


@pytest.mark.parametrize("proposal,message", [
    (Proposal("follow_up_to", 10, 20, "candidate", "none", "t"), "deferred"),
    (Proposal("caused_by", 10, 20, "candidate", "none", "t"), "dropped"),
    (Proposal("related", 10, 20, "candidate", "none", "t"), "not in the taxonomy"),
    (Proposal("reaction_to", 10, 10, "candidate", "none", "t"), "two distinct Developments"),
    (Proposal("reaction_to", 10, 99, "candidate", "none", "t"), "no Development with ID"),
    (Proposal("reaction_to", 10, "Trump rejects the Hormuz plan", "candidate", "none", "t"), "free-text"),
    (Proposal("reaction_to", 20, 10, "accepted", "inferred", "t", explicit(2, 1)), "explicit evidence"),
    (Proposal("reaction_to", 20, 10, "accepted", "explicit", "t"), "must cite"),
    (Proposal("reaction_to", 20, 10, "accepted", "explicit", "t", explicit(3, 1)), "not a member"),
    (Proposal("reaction_to", 20, 10, "pending", "none", "t"), "status"),
])
def test_the_contract_refuses(db, proposal, message):
    with pytest.raises(RelationError, match=message):
        record(db, proposal)
    assert db.query(DevelopmentRelation).count() == 0


def test_candidates_need_no_evidence_and_are_not_returned_as_accepted(db):
    record(db, Proposal("reaction_to", 20, 10, "candidate", "none", "t"))
    assert relations_of(db, 10) == [] and len(relations_of(db, 10, status=None)) == 1


def test_an_existing_database_migrates_to_the_relations_table(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'm.db'}")
    Base.metadata.create_all(engine, tables=[t for name, t in Base.metadata.tables.items()
                                             if name != "development_relations"])
    from sqlalchemy import text
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO schema_meta (key, value) VALUES ('schema_version', '6')"))
    assert run_migrations(engine, backup_dir=tmp_path / "b") == 7
    insp = inspect(engine)
    assert "development_relations" in insp.get_table_names()
    assert "ix_development_relations_target" in {i["name"] for i in insp.get_indexes("development_relations")}
    engine.dispose()
