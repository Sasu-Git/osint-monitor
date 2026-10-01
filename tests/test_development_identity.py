"""Development identity rules (Phase 2, evaluations/identity/development-identity-contract.md): deterministic
order-independent persistence, one Development per item, continuation only through a compatible link, single-
source evidence below the Development layer, report headlines as summaries. Real embeddings, no clustering."""

from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, Event, EventItem, RawItem, Source
from osint_monitor.processors.clustering import persist_clusters

T0 = datetime(2026, 9, 30, 8)
QUAKE = [("Outlet A", "Magnitude 6.8 earthquake strikes eastern Turkey, killing dozens"),
         ("Outlet B", "Strong earthquake kills dozens in eastern Turkey"),
         ("Outlet C", "Death toll rises after powerful earthquake in eastern Turkey")]
UNRELATED = ("Outlet D", "Central bank raises interest rates to curb inflation")


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'i.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    yield factory
    engine.dispose()


def add(s, source, title, hours=0):
    from osint_monitor.processors.embeddings import embed_texts, embedding_to_blob
    src = s.query(Source).filter_by(name=source).first()
    if src is None:
        src = Source(name=source, type="rss", url=f"https://{source.replace(' ', '').lower()}.invalid/",
                     credibility_score=0.7)
        s.add(src)
        s.flush()
    n = s.query(RawItem).count()
    item = RawItem(source_id=src.id, external_id=str(n), title=title, content="", url=f"https://x.invalid/{n}",
                   content_hash=f"h{n}", published_at=T0 + timedelta(hours=hours), fetched_at=T0,
                   embedding=embedding_to_blob(embed_texts([title])[0]))
    s.add(item)
    s.flush()
    return item.id


def developments(s):
    out = {}
    for ei in s.query(EventItem).order_by(EventItem.id):
        out.setdefault(ei.event_id, []).append(ei.item_id)
    return {e: sorted(v) for e, v in out.items()}


def test_cluster_order_does_not_change_identity(tmp_path):
    results = []
    for order in (0, 1):
        engine = create_engine(f"sqlite:///{tmp_path / f'o{order}.db'}")
        Base.metadata.create_all(engine)
        s = sessionmaker(bind=engine)()
        a, b = add(s, *QUAKE[0]), add(s, *QUAKE[1])
        x = add(s, "Outlet E", "Floods in Bangladesh force thousands from their homes", 1)
        y = add(s, "Outlet F", "Thousands flee their homes as floods hit Bangladesh", 1)
        s.commit()
        clusters = [{"item_ids": [a, b], "summary": "q"}, {"item_ids": [x, y], "summary": "f"}]
        persist_clusters(s, clusters if order == 0 else clusters[::-1])
        results.append({e: [s.get(RawItem, i).title for i in ids] for e, ids in developments(s).items()})
        s.close()
        engine.dispose()
    assert len(results[0]) == 2 and results[0] == results[1]   # same IDs, same members, whatever the order


def test_an_item_never_joins_a_second_development_and_continuation_needs_a_link(db):
    s = db()
    a, b = add(s, *QUAKE[0]), add(s, *QUAKE[1])
    s.commit()
    persist_clusters(s, [{"item_ids": [a, b], "summary": "q"}])
    c, u = add(s, *QUAKE[2], hours=3), add(s, *UNRELATED, hours=3)
    s.commit()
    decisions = []
    persist_clusters(s, [{"item_ids": [b, c, u], "summary": "q"}], decisions)
    devs = developments(s)
    assert list(devs.values()) == [sorted([a, b, c])]          # the update continues it; nothing else joins
    assert u in {i for d in decisions for i in d.held}
    assert s.query(EventItem).filter_by(item_id=b).count() == 1


def test_single_source_evidence_stays_below_the_development_layer(db):
    s = db()
    a = add(s, "Outlet A", "Magnitude 6.8 earthquake strikes eastern Turkey, killing dozens")
    a2 = add(s, "Outlet A", "Magnitude 6.8 earthquake strikes eastern Turkey, killing dozens", hours=1)
    s.commit()
    decisions = []
    assert persist_clusters(s, [{"item_ids": [a, a2], "summary": "q"}], decisions) == 0
    assert developments(s) == {}
    assert all(r.startswith("single-source") for d in decisions for r in d.held.values())
    b = add(s, *QUAKE[1], hours=2)                              # independent evidence arrives
    s.commit()
    assert persist_clusters(s, [{"item_ids": [a, a2, b], "summary": "q"}]) == 1
    assert list(developments(s).values()) == [sorted([a, a2, b])]


def test_the_summary_is_a_report_headline_not_a_live_blog(db):
    s = db()
    live = add(s, "Outlet B", "Live: earthquake strikes eastern Turkey, dozens killed")
    report = add(s, "Outlet A", "Magnitude 6.8 earthquake strikes eastern Turkey, killing dozens")
    other = add(s, "Outlet C", "Strong earthquake kills dozens in eastern Turkey")   # a second independent origin
    s.get(RawItem, live).source.credibility_score = 0.9              # the live blog's outlet ranks higher
    s.commit()
    persist_clusters(s, [{"item_ids": [live, report, other], "summary": "x"}])
    event = s.query(Event).one()
    assert event.summary == "Magnitude 6.8 earthquake strikes eastern Turkey, killing dozens"


def test_a_roundup_does_not_corroborate(db):
    s = db()
    report = add(s, "Outlet A", "Magnitude 6.8 earthquake strikes eastern Turkey, killing dozens")
    roundup = add(s, "Outlet B", "Live: earthquake strikes eastern Turkey, dozens killed")
    s.commit()
    decisions = []
    assert persist_clusters(s, [{"item_ids": [report, roundup], "summary": "x"}], decisions) == 0
    assert all(r.startswith("single-source: 1 independent") for d in decisions for r in d.held.values())


# --- owner rule P7: explicit evidence resolves a doubtful headline mismatch ---------------------------------

def _seg(title, hours=0, places=(), anchors=(), cited=None):
    from osint_monitor.processors.development_segmentation import SegmentItem
    return SegmentItem(id=title, source=title, title=title, published_at=T0 + timedelta(hours=hours), vector=None,
                       headline_vector=None, locations=set(places), anchors=set(anchors), cited=cited)


@pytest.fixture
def p7():
    from osint_monitor.core.config import load_event_grouping_config
    cfg = load_event_grouping_config().development_segmentation
    assert cfg.occurrence_match is not None
    return cfg


def test_p7_needs_time_no_place_conflict_and_a_specific_anchor_or_cited_source(p7):
    from osint_monitor.processors.development_segmentation import occurrence_evidence as ev
    a = _seg("Pentagon awards Raytheon $20.7 billion AMRAAM contract", places=["united states"], anchors=["raytheon"])
    b = _seg("Raytheon nets potential $20.7 billion AMRAAM deal", hours=20, anchors=["raytheon"])
    assert "shared anchors ['raytheon']" in ev(a, b, p7)                 # a missing place is not a conflict
    assert ev(a, _seg("Raytheon nets AMRAAM deal", hours=30, anchors=["raytheon"]), p7) is None    # too far apart
    assert ev(a, _seg("Raytheon deal", places=["kyiv"], anchors=["raytheon"]), p7) is None         # place conflict
    assert ev(a, _seg("Why the Raytheon deal matters", anchors=["raytheon"]), p7) is None          # analysis headline
    assert ev(a, _seg("Missile maker wins contract", anchors=["lockheed martin"]), p7) is None     # no shared anchor
    c, d = _seg("Strike hits port", cited="Reuters"), _seg("Port attacked overnight", hours=2, cited="Reuters")
    assert "same cited source Reuters" in ev(c, d, p7)
    assert ev(c, _seg("Port attacked overnight", cited="AP"), p7) is None


def test_p7_anchors_exclude_states_leaders_outlets_generic_labels_and_short_names(db, p7):
    from osint_monitor.core.database import Entity, ItemEntity
    from osint_monitor.processors.development_segmentation import _occurrence_anchors
    s = db()
    item = add(s, "Outlet A", "Raytheon wins AMRAAM deal")
    for name, etype in (("Raytheon", "ORG"), ("Donald Trump", "PERSON"), ("Reuters", "ORG"), ("Navy", "ORG"),
                        ("United States", "GPE"), ("US Department of Defense", "ORG"), ("AI", "ORG")):
        e = Entity(canonical_name=name, entity_type=etype, aliases=[])
        s.add(e)
        s.flush()
        s.add(ItemEntity(item_id=item, entity_id=e.id, role="SUBJECT"))
    s.commit()
    anchors, _ = _occurrence_anchors(s, {item: s.get(RawItem, item)}, p7)
    assert anchors[item] == {"raytheon"}
