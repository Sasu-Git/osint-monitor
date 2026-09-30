"""Phase 0 foundation fixes (evaluations/system/full-basis-audit.md, stop condition S4 and risks 7, 9): writes
that were silently lost, and collector failures that turned into signals."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, Entity, EntityRelationship, RawItem, Source


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'f.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    yield factory
    engine.dispose()


# --- lost JSON writes ---------------------------------------------------------------------------

def test_an_alias_added_to_a_stored_entity_is_persisted(db):
    from osint_monitor.processors.entity_resolver import EntityResolver
    s = db()
    s.add(Entity(canonical_name="Pete Hegseth", entity_type="PERSON", aliases=["Hegseth"]))
    s.commit()
    s.close()

    s = db()
    resolver = EntityResolver(s)
    resolver._build_alias_map()
    resolver._register_alias(s.query(Entity).one(), "Pete Hegseth's")
    s.commit()
    s.close()

    assert db().query(Entity).one().aliases == ["Hegseth", "Pete Hegseth's"]


def _item(s):
    src = s.query(Source).filter_by(name="Test Wire").first()
    if src is None:
        src = Source(name="Test Wire", type="rss", url="https://x.invalid/")
        s.add(src)
        s.flush()
    n = s.query(RawItem).count()
    item = RawItem(source_id=src.id, title="t", content="c", url=f"https://x.invalid/{n}", external_id=str(n),
                   content_hash=f"h{n}")
    s.add(item)
    s.flush()
    return item.id


def test_relation_evidence_is_persisted_and_reruns_do_not_inflate_confidence(db):
    from osint_monitor.processors.relations import persist_relations
    rel = [{"subject": "Iran", "object": "Hezbollah", "predicate": "supports", "confidence": 0.5}]
    s = db()
    first, second = _item(s), _item(s)
    s.commit()
    persist_relations(s, first, rel)
    s.commit()
    persist_relations(s, second, rel)          # new evidence: recorded, confidence +0.05
    s.commit()
    for _ in range(3):
        persist_relations(s, second, rel)      # the same evidence again: no change
        s.commit()
    s.close()

    r = db().query(EntityRelationship).one()
    assert r.evidence_item_ids == [first, second]
    assert r.confidence == pytest.approx(0.55)
