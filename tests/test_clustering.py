"""Event clustering precision on real embeddings: over-merges seen in live data stay apart,
genuine multi-outlet coverage of one development still clusters."""

import os
from datetime import datetime, timedelta

import pytest

from osint_monitor.core.database import RawItem, Source
from osint_monitor.processors.clustering import cluster_recent_items
from tests import live_fixtures as live


@pytest.fixture(scope="module")
def embed():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")          # use the local cache, never the network
    from osint_monitor.processors.embeddings import embed_item, embedding_to_blob
    try:
        embed_item("probe", "")
    except Exception as e:
        pytest.skip(f"needs the cached embedding model (run `python main.py smoke` once): {e}")
    return lambda title, content: embedding_to_blob(embed_item(title, content))


def ingest(session, embed, articles):
    """articles: (story, source, title, content). Returns {item_id: story}."""
    now = datetime.utcnow()
    stories = {}
    for n, (story, source, title, content) in enumerate(articles):
        src = session.query(Source).filter_by(name=source).first()
        if src is None:
            src = Source(name=source, type="rss", url=source, credibility_score=0.8)
            session.add(src)
            session.flush()
        item = RawItem(source_id=src.id, title=title, content=content, content_hash=f"h{n}",
                       published_at=now - timedelta(minutes=5 * n), fetched_at=now, embedding=embed(title, content))
        session.add(item)
        session.flush()
        stories[item.id] = story
    session.commit()
    return stories


def clustered_stories(session, stories):
    return [sorted({stories[i] for i in c["item_ids"]}) for c in cluster_recent_items(session)]


def test_templated_feeds_do_not_merge_different_events(session, embed):
    articles = [("quake", "USGS Seismic", "Earthquake M5.3 - 15 km SSW of Hilvan, Turkey",
                 "Magnitude: 5.3 | Depth: 10.0 km | Place: 15 km SSW of Hilvan, Turkey")]
    articles += [(f"sanction-{n}", "UN Consolidated", f"UN Sanctions: {name}",
                  f"Listed: 2012-11-30. {name} was a military leader of the M23 group in the Democratic Republic "
                  f"of the Congo. INTERPOL-UN Security Council Special Notice.")
                 for n, name in enumerate(["INNOCENT KAINA", "SULTANI MAKENGA", "BOSCO TAGANDA", "LAURENT NKUNDA"])]
    articles += [(f"quake-{n}", "USGS Seismic", f"Earthquake M4.{n} - 20 km N of {place}",
                  f"Magnitude: 4.{n} | Depth: 12 km | Place: 20 km N of {place}")
                 for n, place in enumerate(["Kokopo, Papua New Guinea", "Hualien, Taiwan", "Illapel, Chile"])]
    stories = ingest(session, embed, articles)
    assert all(len(c) == 1 for c in clustered_stories(session, stories)), "templated items of different events merged"


def test_military_strike_and_labour_strike_stay_apart(session, embed):
    stories = ingest(session, embed, [
        ("missile", "Reuters World", "Russian missile strike hits Kharkiv apartment block, killing four",
         "A Russian missile struck an apartment block in Kharkiv overnight, killing four people, Ukrainian officials said."),
        ("missile", "BBC World", "Four killed as Russian missile hits residential building in Kharkiv",
         "Four people died when a Russian missile hit a residential building in the Ukrainian city of Kharkiv."),
        ("labour", "Al Jazeera", "Dock workers strike shuts down Rotterdam port",
         "Dock workers at the port of Rotterdam walked out over pay, halting container traffic at Europe's largest port."),
        ("labour", "Defense News", "Rotterdam port paralysed as dockers strike over wages",
         "Container traffic at Rotterdam stopped as dock workers went on strike demanding higher wages."),
    ])
    clusters = clustered_stories(session, stories)
    assert ["labour", "missile"] not in clusters
    assert ["missile"] in clusters


def test_independent_reports_of_one_summit_cluster_together(session, embed):
    sources = ["Al Jazeera", "BBC World", "South China Morning Post", "Reuters World"]
    summit = [live.TRUMP_XI_SUMMIT[i] for i in (1, 2, 3, 10)]
    stories = ingest(session, embed, [("summit", s, t, c) for s, (t, c) in zip(sources, summit)])
    clusters = cluster_recent_items(session)
    assert any(len(c["item_ids"]) >= 3 for c in clusters), \
        f"summit coverage from four outlets did not cluster: {[c['item_ids'] for c in clusters]}"
    assert all(set(stories[i] for i in c["item_ids"]) == {"summit"} for c in clusters)


def test_different_developments_about_the_same_country_do_not_merge(session, embed):
    stories = ingest(session, embed, [
        ("talks", "Reuters World", "US and Iran resume nuclear talks in Muscat",
         "The United States and Iran resumed indirect nuclear talks in Muscat, mediated by Oman."),
        ("talks", "BBC World", "Iran and US hold new round of nuclear talks in Oman",
         "Iran and the United States held a new round of nuclear talks in Muscat, Oman."),
        ("football", "Al Jazeera", "Iran hosts West Asian football championship in Tehran",
         "Iran opened the West Asian football championship in Tehran with eight national teams."),
        ("quake", "South China Morning Post", "Earthquake shakes southern Iran, no casualties reported",
         "A magnitude 5.1 earthquake shook Hormozgan province in southern Iran, officials said."),
    ])
    for c in clustered_stories(session, stories):
        assert len(c) == 1, f"merged different Iran stories: {c}"


def test_unrelated_defense_stories_from_live_data_do_not_merge(session, embed):
    sources = ["Breaking Defense", "Breaking Defense", "Breaking Defense", "Defense News", "War on the Rocks"]
    stories = ingest(session, embed, [(f"story-{n}", s, t, c) for n, (s, (t, c)) in enumerate(zip(sources, live.NAVY_CYBER))])
    assert all(len(c) == 1 for c in clustered_stories(session, stories))
