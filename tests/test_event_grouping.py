"""Narrative news is clustered on its text; sensor and record feeds are grouped by what they
record. Templated sensor text must never build a narrative event."""

import os
from datetime import datetime, timedelta

import pytest

from osint_monitor.core.config import EventGroupingConfig, load_event_grouping_config
from osint_monitor.core.database import Event, RawItem, Situation, Source
from osint_monitor.processors.clustering import cluster_recent_items, persist_clusters
from osint_monitor.processors.event_grouping import NARRATIVE, STRUCTURED, group_structured, source_class
from tests import live_fixtures as live

SUMMIT_WIRES = [
    ("Reuters", "rss", None, None, "Trump and Xi agree to extend trade truce at White House summit",
     "US President Donald Trump and Chinese President Xi Jinping agreed on Thursday to extend a tariff truce "
     "for another year after talks at the White House.", None),
    ("Associated Press", "rss", None, None, "Xi and Trump extend tariff truce after White House talks",
     "Chinese leader Xi Jinping and President Donald Trump agreed to extend their trade truce by a year "
     "following a summit in Washington.", None),
]


@pytest.fixture(scope="module")
def embed():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")          # use the local cache, never the network
    from osint_monitor.processors.embeddings import embed_item, embedding_to_blob
    try:
        embed_item("probe", "")
    except Exception as e:
        pytest.skip(f"needs the cached embedding model (run `python main.py smoke` once): {e}")
    return lambda title, content: embedding_to_blob(embed_item(title, content))


def ingest(session, records, embed=None):
    """records: (source, type, external_id, url, title, content, published). Published times are
    moved so the newest record is 10 minutes old, keeping the gaps between records."""
    stamps = [datetime.fromisoformat(r[6]) for r in records if r[6]]
    shift = datetime.utcnow() - timedelta(minutes=10) - max(stamps) if stamps else timedelta(0)
    ids = {}
    for n, (source, stype, ext, url, title, content, published) in enumerate(records):
        src = session.query(Source).filter_by(name=source).first()
        if src is None:
            src = Source(name=source, type=stype, url=url or source, credibility_score=0.8)
            session.add(src)
            session.flush()
        pub = datetime.fromisoformat(published) + shift if published else datetime.utcnow() - timedelta(minutes=n)
        item = RawItem(source_id=src.id, external_id=ext, url=url, title=title, content=content,
                       content_hash=f"{source}-{n}-{title}", published_at=pub, fetched_at=datetime.utcnow(),
                       embedding=embed(title, content) if embed else None)
        session.add(item)
        session.flush()
        ids[item.id] = title
    session.commit()
    return ids


def groups(session, ids):
    return [sorted(ids[i] for i in c["item_ids"]) for c in cluster_recent_items(session)]


# --- source classes ------------------------------------------------------------------------

@pytest.mark.parametrize("name, stype, kind", [
    ("USGS Seismic", "structured_api", STRUCTURED),
    ("Seismic Explosion Detector", "infrastructure", STRUCTURED),
    ("ADSB Military Tracks", "adsb", STRUCTURED),
    ("BGP Infrastructure Monitor", "infrastructure", STRUCTURED),
    ("UN Consolidated", "sanctions", STRUCTURED),
    ("GDELT", "structured_api", NARRATIVE),          # news articles despite the API type
    ("BBC World", "rss", NARRATIVE),
    ("Some New Outlet", "rss", NARRATIVE),            # new sources default to narrative
])
def test_source_classes(name, stype, kind):
    assert source_class(name, stype, load_event_grouping_config()) == kind


def test_unknown_strategy_is_a_configuration_error(session):
    ids = ingest(session, live.SEISMIC_RECORDS[:1])
    item = session.get(RawItem, next(iter(ids)))
    with pytest.raises(ValueError, match="Unknown structured grouping strategy"):
        group_structured([item], EventGroupingConfig(strategies={"USGS Seismic": "vibes"}))


# --- structured ------------------------------------------------------------------------------

def test_separate_earthquakes_stay_separate_despite_templated_wording(session, embed):
    # with real embeddings: these used to form one 18-item event
    ids = ingest(session, live.SEISMIC_RECORDS, embed)
    assert groups(session, ids) == []


def test_same_earthquake_from_two_structured_sources_merges(session):
    usgs = ("USGS Seismic", "structured_api", "usgs_us7000abcd", "https://earthquake.usgs.gov/earthquakes/eventpage/us7000abcd",
            "Earthquake M4.6 - 30 km E of Tabas, Iran",
            "Magnitude: 4.6 | Depth: 8.0 km | Location: 33.61,57.25 | Place: 30 km E of Tabas, Iran", "2026-09-24 10:00:00")
    detector = ("Seismic Explosion Detector", "infrastructure", "seis_exp_us7000abcd",
                "https://earthquake.usgs.gov/earthquakes/eventpage/us7000abcd",
                "Shallow seismic: M4.6 depth=8km at 30 km E of Tabas, Iran — explosion likelihood: MODERATE",
                "Magnitude: 4.6\nDepth: 8 km\nLocation: 33.61, 57.25\nPlace: 30 km E of Tabas, Iran\n", "2026-09-24 10:00:00")
    ids = ingest(session, [usgs, detector, *live.SEISMIC_RECORDS])
    [cluster] = cluster_recent_items(session)
    assert cluster["kind"] == STRUCTURED and cluster["source_count"] == 2
    assert sorted(ids[i] for i in cluster["item_ids"]) == sorted([usgs[4], detector[4]])


def test_same_earthquake_under_different_catalogue_ids_merges_on_time_place_and_magnitude(session):
    a = ("USGS Seismic", "structured_api", "usgs_us7000aaaa", "https://earthquake.usgs.gov/earthquakes/eventpage/us7000aaaa",
         "Earthquake M5.1 - Taiwan", "Magnitude: 5.1 | Location: 23.90,121.60", "2026-09-24 10:00:00")
    b = ("Seismic Explosion Detector", "infrastructure", "seis_exp_tw2026bbbb", "https://earthquake.usgs.gov/earthquakes/eventpage/tw2026bbbb",
         "Shallow seismic: M4.9 depth=5km near Hualien", "Magnitude: 4.9\nLocation: 23.95, 121.55\n", "2026-09-24 10:00:40")
    far = ("Seismic Explosion Detector", "infrastructure", "seis_exp_jp2026cccc", "https://earthquake.usgs.gov/earthquakes/eventpage/jp2026cccc",
           "Shallow seismic: M5.0 depth=5km off Okinawa", "Magnitude: 5.0\nLocation: 26.20, 127.70\n", "2026-09-24 10:00:30")
    ids = ingest(session, [a, b, far])
    assert groups(session, ids) == [sorted([a[4], b[4]])]


def test_adsb_snapshots_do_not_become_a_narrative_mega_event(session, embed):
    # the same concentrations reported again on the next 2.5-minute tick
    next_tick = [(src, t, ext + "_next", url, title, body, pub[:-5] + "52:14")
                 for src, t, ext, url, title, body, pub in live.ADSB_RECORDS[2:]]
    ids = ingest(session, live.ADSB_RECORDS + next_tick, embed)
    assert groups(session, ids) == []


# --- narrative, and the two together ----------------------------------------------------------

def test_two_wire_articles_about_one_summit_still_merge_beside_sensor_feeds(session, embed):
    ids = ingest(session, SUMMIT_WIRES + live.SEISMIC_RECORDS + live.ADSB_RECORDS, embed)
    clusters = cluster_recent_items(session)
    assert [(c["kind"], sorted(ids[i] for i in c["item_ids"])) for c in clusters] == [
        (NARRATIVE, sorted(t[4] for t in SUMMIT_WIRES))]


def test_structured_and_narrative_events_can_share_a_situation_without_merging(session, embed):
    quake = [("USGS Seismic", "structured_api", "usgs_us7000iran", "https://earthquake.usgs.gov/earthquakes/eventpage/us7000iran",
              "Earthquake M4.4 - 20 km S of Natanz, Iran", "Magnitude: 4.4 | Location: 33.33,51.90", "2026-09-24 10:00:00"),
             ("Seismic Explosion Detector", "infrastructure", "seis_exp_us7000iran",
              "https://earthquake.usgs.gov/earthquakes/eventpage/us7000iran",
              "Shallow seismic: M4.4 depth=2km at 20 km S of Natanz, Iran — explosion likelihood: HIGH",
              "Magnitude: 4.4\nLocation: 33.33, 51.90\n", "2026-09-24 10:00:00")]
    talks = [("Reuters", "rss", None, None, "US and Iran resume nuclear talks in Muscat",
              "The United States and Iran resumed indirect nuclear talks in Muscat on Tuesday.", None),
             ("Associated Press", "rss", None, None, "Iran and US negotiators meet in Muscat for nuclear talks",
              "Iranian and American negotiators met in Oman for a new round of nuclear talks.", None)]
    ingest(session, quake + talks, embed)
    assert persist_clusters(session, cluster_recent_items(session)) == 2

    situation = Situation(slug="us-iran", title="US–Iran")
    session.add(situation)
    session.flush()
    for e in session.query(Event):
        e.situation_id = situation.id
    session.commit()
    quake_event, talks_event = sorted(situation.developments, key=lambda e: "Earthquake" not in e.summary)
    assert "Earthquake" in quake_event.summary and "talks" in talks_event.summary
    assert not {ei.item_id for ei in quake_event.event_items} & {ei.item_id for ei in talks_event.event_items}
