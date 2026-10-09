"""Identity follow-up rule T24 (evaluations/identity/defects/fix-plan.md): a Development's reports span at most N hours.
Implemented but off in config/event_grouping.yaml (followup-results.md); these tests switch it on at 24 h."""

from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core import config as C
from osint_monitor.core.database import Base, EventItem, RawItem, Source
from osint_monitor.processors.clustering import persist_clusters

T0 = datetime(2026, 9, 30, 8)
QUAKE = [("Outlet A", "Magnitude 6.8 earthquake strikes eastern Turkey, killing dozens"),
         ("Outlet B", "Strong earthquake kills dozens in eastern Turkey"),
         ("Outlet C", "Death toll rises after powerful earthquake in eastern Turkey"),
         ("Outlet D", "Powerful earthquake in eastern Turkey kills dozens, rescuers search rubble")]


@pytest.fixture
def s(tmp_path, monkeypatch):
    base = C.load_event_grouping_config

    def with_span(*a, **k):
        cfg = base(*a, **k)
        cfg.development_segmentation.max_occurrence_span_hours = 24
        return cfg
    monkeypatch.setattr(C, "load_event_grouping_config", with_span)
    engine = create_engine(f"sqlite:///{tmp_path / 'f.db'}")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
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
    return sorted(sorted(v) for v in out.values())


def cluster(ids):
    return {"item_ids": ids, "label": 0, "summary": "", "severity": 0.0, "region": None, "kind": "narrative"}


def test_the_span_is_off_in_the_persisted_config():
    assert C.load_event_grouping_config().development_segmentation.max_occurrence_span_hours is None


def test_a_report_within_24_hours_continues_the_development(s):
    a, b = add(s, *QUAKE[0]), add(s, *QUAKE[1], hours=1)
    persist_clusters(s, [cluster([a, b])])
    c = add(s, *QUAKE[2], hours=20)
    persist_clusters(s, [cluster([a, b, c])])
    assert developments(s) == [[a, b, c]]


def test_a_report_more_than_24_hours_after_the_first_does_not_continue_it(s):
    a, b = add(s, *QUAKE[0]), add(s, *QUAKE[1], hours=1)
    persist_clusters(s, [cluster([a, b])])
    c = add(s, *QUAKE[2], hours=30)
    persist_clusters(s, [cluster([a, b, c])])
    assert developments(s) == [[a, b]]             # c stays below the layer: alone, it is single-source


def test_later_reports_from_two_origins_form_their_own_development(s):
    a, b = add(s, *QUAKE[0]), add(s, *QUAKE[1], hours=1)
    persist_clusters(s, [cluster([a, b])])
    c, d = add(s, *QUAKE[2], hours=30), add(s, *QUAKE[3], hours=31)
    persist_clusters(s, [cluster([a, b, c, d])])
    assert developments(s) == [[a, b], [c, d]]


def test_new_items_spanning_more_than_24_hours_are_split_into_spans(s):
    ids = [add(s, *QUAKE[0]), add(s, *QUAKE[1], hours=2), add(s, *QUAKE[2], hours=30), add(s, *QUAKE[3], hours=31)]
    persist_clusters(s, [cluster(ids)])
    assert developments(s) == [ids[:2], ids[2:]]


def test_an_earlier_weakly_linked_report_does_not_decide_where_the_span_starts(s):
    early = add(s, "Outlet A", "Earthquake strikes eastern Turkey", 0)
    b = add(s, "Outlet B", "Death toll rises to 40 after earthquake in eastern Turkey", 20)
    c = add(s, "Outlet C", "Death toll rises to 45 after earthquake in eastern Turkey", 30)
    persist_clusters(s, [cluster([early, b, c])])
    assert developments(s) == [[b, c]]             # the strongest link groups first; adding `early` would span 30 h
