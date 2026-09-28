"""Development segmentation on real embeddings: reports of one occurrence stay one Development,
analysis / template look-alikes / other places split off, and the switch defaults to off.
Known limitations (same-place repeated actions, reactions) are pinned as strict xfails."""

import os
from datetime import datetime, timedelta

import pytest

from osint_monitor.core.config import DevelopmentSegmentationConfig, load_event_grouping_config
from osint_monitor.core.database import RawItem, Source
from osint_monitor.processors import clustering
from osint_monitor.processors.development_segmentation import (
    ANALYSIS, REPORT, ROLLING, SegmentItem, headline_kind, segment,
)
from tests import live_fixtures as live

ON = DevelopmentSegmentationConfig(enabled=True)
T0 = datetime(2026, 8, 7, 9, 0)


@pytest.fixture(scope="module")
def embed():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")          # use the local cache, never the network
    from osint_monitor.processors.embeddings import embed_item, embed_text
    try:
        embed_item("probe", "")
    except Exception as e:
        pytest.skip(f"needs the cached embedding model (run `python main.py smoke` once): {e}")
    return embed_item, embed_text


def items(embed, specs):
    """specs: (id, source, hours after T0, title, content, locations)."""
    embed_item, embed_text = embed
    return [SegmentItem(id=i, source=src, title=title, published_at=T0 + timedelta(hours=h),
                        vector=embed_item(title, content), headline_vector=embed_text(title), locations=set(locs))
            for i, src, h, title, content, locs in specs]


def together(seg, *ids):
    return any(set(ids) <= set(g) for g in seg.groups)


def apart(seg, a, b):
    return not together(seg, a, b)


def cut(seg, a, b, guard):
    """The clusterer linked a and b and this guard dropped the link (the split is not vacuous)."""
    return (a, b, guard) in seg.cuts or (b, a, guard) in seg.cuts


# --- must stay together ------------------------------------------------------------------------

def test_two_outlets_reporting_the_same_summit_stay_one_development(embed):
    (t1, c1), (t2, c2) = live.TRUMP_XI_SUMMIT[1], live.TRUMP_XI_SUMMIT[2]
    seg = segment(items(embed, [("a", "BBC World", 0, t1, c1, ["washington", "china"]),
                                ("b", "Al Jazeera", 3, t2, c2, ["washington"])]), ON)
    assert together(seg, "a", "b")


def test_two_reports_of_the_same_strike_stay_one_development(embed):
    seg = segment(items(embed, [
        ("a", "Reuters World", 0, "Russian missile strike hits Kharkiv apartment block, killing four",
         "A Russian missile struck an apartment block in Kharkiv overnight, killing four people, officials said.",
         ["kharkiv", "ukraine"]),
        ("b", "BBC World", 2, "Four killed as Russian missile hits residential building in Kharkiv",
         "Four people died when a Russian missile hit a residential building in the Ukrainian city of Kharkiv.",
         ["kharkiv"]),
    ]), ON)
    assert together(seg, "a", "b")


def test_differently_worded_reports_of_one_agreement_stay_one_development(embed):
    seg = segment(items(embed, [
        ("a", "Al Jazeera", 0, "Saudi Arabia, Turkiye and Pakistan sign joint defence pact",
         "The three countries signed a mutual defence agreement in Mecca on Friday.", ["mecca", "saudi arabia"]),
        ("b", "BBC World", 2, "Saudi Arabia, Turkey and Pakistan sign defence pact",
         "Leaders of Saudi Arabia, Turkey and Pakistan have signed a defence pact at a meeting in Mecca.",
         ["saudi arabia", "mecca", "turkey"]),
    ]), ON)
    assert together(seg, "a", "b")


def test_death_toll_updates_of_one_disaster_stay_one_development(embed):
    seg = segment(items(embed, [
        ("a", "BBC World", 0, "At least 41 dead after ferry capsizes off Guyana",
         "A passenger ferry capsized off the coast of Guyana, killing at least 41 people.", ["guyana"]),
        ("b", "Al Jazeera", 26, "Guyana ferry capsize death toll rises to 53 as survivors describe terror",
         "The death toll from the ferry disaster off Guyana has risen to 53.", ["guyana"]),
    ]), ON)
    assert together(seg, "a", "b")


# --- must split --------------------------------------------------------------------------------

PACT_REPORTS = [
    ("sign-aj", "Al Jazeera", 0, "Saudi Arabia, Turkiye and Pakistan sign joint defence pact",
     "The three countries signed a mutual defence agreement in Mecca, pledging to treat an attack on one as an "
     "attack on all.", ["mecca", "saudi arabia"]),
    ("sign-bbc", "BBC World", 2, "Saudi Arabia, Turkey and Pakistan sign defence pact",
     "Saudi Arabia, Turkey and Pakistan have signed a defence pact in Mecca, pledging to treat an attack on one "
     "as an attack on all.", ["saudi arabia", "mecca"]),
]


def test_agreement_signing_and_a_later_explainer_are_different_developments(embed):
    explainer = ("explainer", "Al Jazeera", 20, "Turkiye, Saudi Arabia, Pakistan sign joint defence agreement: What's in it?",
                 "The pact signed in Mecca commits the three countries to treat an attack on one as an attack on all. "
                 "Here is what the agreement says.", ["mecca", "saudi arabia"])
    seg = segment(items(embed, PACT_REPORTS + [explainer]), ON)
    assert together(seg, "sign-aj", "sign-bbc")
    assert all("explainer" not in g for g in seg.groups)
    assert seg.commentary.get("explainer") is not None          # kept as commentary on the signing
    assert any(c[2] == "analysis_headline" and "explainer" in c[:2] for c in seg.cuts)


def test_summit_preview_and_the_summit_are_different_developments(embed):
    seg = segment(items(embed, [
        ("preview", "Al Jazeera", 0, "Xi, Modi and Putin set to meet for SCO summit: What's on the agenda?",
         "Leaders gather in Bishkek for the Shanghai Cooperation Organisation summit.", ["bishkek"]),
        ("summit-a", "South China Morning Post", 30, "Xi, Modi and Putin meet at SCO summit in Bishkek",
         "Leaders of China, India and Russia met at the Shanghai Cooperation Organisation summit in Bishkek.",
         ["bishkek"]),
        ("summit-b", "BBC World", 31, "Putin, Xi and Modi hold talks at SCO summit in Kyrgyzstan",
         "The leaders of Russia, China and India met at the Shanghai Cooperation Organisation summit in Bishkek.",
         ["bishkek", "kyrgyzstan"]),
    ]), ON)
    assert apart(seg, "preview", "summit-a") and apart(seg, "preview", "summit-b")
    assert cut(seg, "preview", "summit-a", "analysis_headline")
    assert together(seg, "summit-a", "summit-b")


def test_template_similar_disasters_in_different_places_are_different_developments(embed):
    seg = segment(items(embed, [
        ("guyana-1", "BBC World", 0, "At least 41 dead after ferry capsizes off Guyana",
         "A passenger ferry capsized off Guyana, killing at least 41 people.", ["guyana"]),
        ("guyana-2", "Al Jazeera", 3, "Guyana reports ferry disaster death toll rises to 41",
         "Authorities in Guyana say 41 people died when a ferry capsized.", ["guyana"]),
        ("mauritania", "Al Jazeera", 20, "More than 140 dead, missing on refugee boat stranded off Mauritania",
         "More than 140 people are dead or missing after a boat carrying refugees was stranded off Mauritania.",
         ["mauritania"]),
    ]), ON)
    assert together(seg, "guyana-1", "guyana-2")
    assert apart(seg, "guyana-1", "mauritania") and apart(seg, "guyana-2", "mauritania")
    assert "mauritania" in seg.detached                          # a report, not commentary
    assert cut(seg, "guyana-1", "mauritania", "disjoint_locations")


def test_strikes_on_different_cities_on_consecutive_days_are_different_developments(embed):
    seg = segment(items(embed, [
        ("mon", "BBC World", 0, "Russian drone attack on Kyiv kills three on Monday",
         "Russia launched a drone attack on Kyiv overnight, killing three people.", ["kyiv"]),
        ("tue", "Al Jazeera", 24, "Russian drone attack on Odesa kills three on Tuesday",
         "Russia launched a drone attack on Odesa overnight, killing three people.", ["odesa"]),
    ]), ON)
    assert apart(seg, "mon", "tue")
    assert cut(seg, "mon", "tue", "disjoint_locations")


def test_one_storyline_keeps_the_occurrence_and_sheds_analysis_and_live_coverage(embed):
    seg = segment(items(embed, PACT_REPORTS + [
        ("analysis", "Al Jazeera", 26, "Saudi-Pakistan-Turkiye pact: A new shield or strategic signal?",
         "The defence pact signed in Mecca raises questions about the region's security architecture.",
         ["mecca", "saudi arabia"]),
        ("strategy", "Al Jazeera", 30, "Will Pakistan-Saudi-Turkiye defence pact change US strategy?",
         "Analysts weigh what the Mecca defence pact means for Washington.", ["mecca", "washington"]),
    ]), ON)
    [development] = [g for g in seg.groups if "sign-aj" in g]
    assert set(development) == {"sign-aj", "sign-bbc"}


@pytest.mark.xfail(strict=True, reason="known limitation: repeated actions in the same place on nearby days "
                                       "need an explicit event date, which RSS text rarely carries")
def test_known_limitation_repeated_strikes_on_the_same_city(embed):
    seg = segment(items(embed, [
        ("mon", "BBC World", 0, "Russian drone attack on Kyiv kills three",
         "Russia launched a drone attack on Kyiv overnight, killing three people.", ["kyiv"]),
        ("tue", "Al Jazeera", 24, "Russian drones hit Kyiv again, killing two",
         "Russia launched another drone attack on Kyiv overnight, killing two people.", ["kyiv"]),
    ]), ON)
    assert apart(seg, "mon", "tue")


@pytest.mark.xfail(strict=True, reason="known limitation: a policy response reported in the same place and in the "
                                       "same words as the incident is not separated by the guards")
def test_known_limitation_shooting_and_later_policy_response(embed):
    seg = segment(items(embed, [
        ("shooting", "BBC World", 0, "Seven killed after teen shooter opens fire at school in Thailand",
         "A teenage gunman killed seven people at a school in northern Thailand.", ["thailand"]),
        ("policy", "Al Jazeera", 17, "Thai PM vows stricter gun laws after seven killed in school shooting",
         "Thailand's prime minister promised tougher gun laws after a teenage gunman killed seven people at a school.",
         ["thailand"]),
    ]), ON)
    assert apart(seg, "shooting", "policy")


# --- contract -----------------------------------------------------------------------------------

def test_segmentation_only_splits_never_joins(embed):
    specs = [("a", "BBC World", 0, "Russian drone attack on Kyiv kills three", "Drones hit Kyiv.", ["kyiv"]),
             ("b", "Al Jazeera", 1, "Dock workers strike shuts down Rotterdam port", "Dockers walked out.", ["rotterdam"])]
    seg = segment(items(embed, specs), ON)
    assert seg.groups == []                                      # unlinked items are never grouped


def test_headline_kind():
    assert headline_kind("Why has Israel escalated attacks in southern Lebanon?") == ANALYSIS
    assert headline_kind("What we know so far about the deadly Thailand shooting") == ANALYSIS
    assert headline_kind("Erdogan visits Saudi Arabia: What to expect") == ANALYSIS
    assert headline_kind("Iran war live: US launches new attacks") == ROLLING
    assert headline_kind("War on Iran: Phase II: Day 28") == ROLLING
    assert headline_kind("Zelensky sacks Ukraine's top army commander after days of protests") == REPORT


def test_segmentation_is_off_by_default():
    assert load_event_grouping_config().development_segmentation.enabled is False
    assert DevelopmentSegmentationConfig().enabled is False


def test_enabled_pipeline_keeps_analysis_as_commentary_not_evidence(session, embed, monkeypatch):
    embed_item, _ = embed
    from osint_monitor.processors.embeddings import embedding_to_blob
    config = load_event_grouping_config()
    config.development_segmentation.enabled = True
    monkeypatch.setattr(clustering, "load_event_grouping_config", lambda: config)
    now = datetime.utcnow()
    ids = {}
    for n, (key, source, hours, title, content, _) in enumerate(PACT_REPORTS + [
            ("explainer", "Al Jazeera", 20, "Turkiye, Saudi Arabia, Pakistan sign joint defence agreement: What's in it?",
             "The pact signed in Mecca commits the three countries to treat an attack on one as an attack on all. "
             "Here is what the agreement says.", [])]):
        src = session.query(Source).filter_by(name=source).first()
        if src is None:
            src = Source(name=source, type="rss", url=source, credibility_score=0.8)
            session.add(src)
            session.flush()
        item = RawItem(source_id=src.id, title=title, content=content, content_hash=f"h{n}",
                       published_at=now - timedelta(hours=24 - hours), fetched_at=now,
                       embedding=embedding_to_blob(embed_item(title, content)))
        session.add(item)
        session.flush()
        ids[key] = item.id
    session.commit()
    [cluster] = clustering.cluster_recent_items(session)
    assert set(cluster["item_ids"]) == {ids["sign-aj"], ids["sign-bbc"]}
    assert cluster["commentary_item_ids"] == [ids["explainer"]]
