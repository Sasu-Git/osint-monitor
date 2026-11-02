"""Workspace accessibility and polish (owner follow-ups, 2026-11): priority-control labels and focus ids, day
grouping by stored timestamps, the shared map legend, the "no confirmed location" presentation and the empty states.
Presentation only: nothing here changes a Development, a Situation or a priority's meaning.

Reuses the temporary-database fixtures of the workspace and situation evidence tests."""

import re
from datetime import datetime

from osint_monitor.api.pages import day_bucket
from osint_monitor.core.user_state import Level, PriorityStore, Scope, default_path
from tests.test_situation_views import db, seeded  # noqa: F401  (pytest fixtures)
from tests.test_workspace import add, client


# --- priority controls -------------------------------------------------------------------------------

def test_priority_buttons_are_labelled_focusable_and_have_stable_ids(seeded):
    html = client().get("/priorities").text
    buttons = re.findall(r"<button[^>]*class=\"lv lv-(\w+)\"[^>]*>", html)
    assert buttons and set(buttons) == {"HIGH", "NORMAL", "LOW", "MUTED"}
    for tag in re.findall(r"<button[^>]*class=\"lv lv-\w+\"[^>]*>", html):
        assert 'type="button"' in tag                            # native button: Tab, Enter and Space work
        assert re.search(r'aria-label="[^"]+: (High|Normal|Low|Muted): ', tag), tag
        assert re.search(r'title="(High|Normal|Low|Muted): ', tag), tag
        assert re.search(r'id="lv-domain-\w+-(HIGH|NORMAL|LOW|MUTED)"', tag), tag
    ids = re.findall(r'id="(lv-[^"]+)"', html)
    assert len(ids) == len(set(ids))                             # unique, so HTMX can restore focus after a swap
    assert "(current)" in html                                   # the selected level says so in its tooltip


def test_country_search_results_use_their_own_ids(seeded):
    PriorityStore(default_path()).set(Scope.COUNTRY, "CHN", Level.HIGH)
    c = client()
    panel = c.get("/priorities").text
    results = c.get("/ui/countries?q=chin").text
    assert 'id="lv-country-CHN-HIGH"' in panel and 'id="lvs-country-CHN-HIGH"' in results
    assert 'id="lv-country-CHN-HIGH"' not in results


# --- day grouping -------------------------------------------------------------------------------------

def test_day_bucket_uses_utc_calendar_days():
    now = datetime(2026, 11, 2, 9, 0)
    assert day_bucket(datetime(2026, 11, 2, 0, 5), now) == "Today"
    assert day_bucket(datetime(2026, 11, 1, 23, 59), now) == "Yesterday"
    assert day_bucket(datetime(2026, 10, 31, 12, 0), now) == "Earlier"
    assert day_bucket(None, now) == "Earlier"


def test_situation_timeline_has_one_separator_per_day_group(seeded):
    html = client().get("/situations/china-united-states").text
    heads = re.findall(r'<li class="tl-day"><h3>(\w+)</h3></li>', html)
    assert heads and len(heads) == len(set(heads))               # each group once, in timeline order
    assert html.index('class="tl-day"') < html.index('class="tl"')


def test_feed_keeps_rank_order_and_labels_the_day(seeded):
    html = client().get("/").text
    assert 'class="day-tag"' in html and 'class="tl-day"' not in html   # no separators inside a ranked list


# --- location and legend ------------------------------------------------------------------------------

def test_no_confirmed_location_is_explained(seeded):
    make, _ = seeded
    add(make, "Statement without a place", event_domain="political")
    html = client().get("/").text
    assert "No confirmed location" in html and "(listed here, not on the map)" in html
    assert 'class="loc-mark"' in html


def test_legend_is_shared_and_readable_by_screen_readers(seeded):
    c = client()
    for page in ("/", "/map", "/situations/china-united-states"):
        html = c.get(page).text
        legend = re.search(r'<details class="map-legend"[^>]*>(.*?)</details>', html, re.S)
        assert legend, page
        assert "aria-hidden" not in legend.group(0).split(">")[0]      # the legend itself is not hidden
        assert "<summary>Map legend</summary>" in legend.group(1)     # a keyboard-operable disclosure
        assert "Point: a specific place" in legend.group(1)
        assert "Hollow ring: the whole country" in legend.group(1)
        assert "high priority" in legend.group(1)
        assert "No confirmed location" in legend.group(1)
        assert 'id="map-empty"' in html


# --- empty states -------------------------------------------------------------------------------------

def test_all_muted_empty_state_offers_show_muted(seeded):
    store = PriorityStore(default_path())
    for d in ("diplomacy", "economic"):
        store.set(Scope.DOMAIN, d, Level.MUTED)
    html = client().get("/?range=7d").text
    assert "Every development in this view is muted." in html
    assert re.search(r'href="[^"]*show_muted=1[^"]*">Show them</a>', html)


def test_filtered_empty_state_names_the_filters_and_clears_them(seeded):
    html = client().get("/?range=7d&type=protest&confidence=disputed").text
    assert "No development matches these filters." in html
    assert "Filtered by type, confidence." in html and 'href="/?range=7d">Clear the filters</a>' in html


def test_no_situations_page(db):
    html = client().get("/situations").text
    assert "No situations yet." in html and 'href="/">Today</a>' in html


def test_phone_width_rules_keep_title_time_actors_and_context():
    css = open("web/static/app.css", encoding="utf-8").read()
    block = css[css.index("/* phone width: title, time"):]
    phone = block[block.index("@media (max-width: 640px)"):]
    hidden = phone[:phone.index("display: none")]
    for kept in (".dev .title", ".dev .meta-right .time", ".actors", ".place", ".situation-link", ".prio-note"):
        assert kept not in hidden
    for dropped in (".dev .summary", ".dev .reasons", ".dev .line-class .chip", ".dev .line-ctx .srcs"):
        assert dropped in hidden
