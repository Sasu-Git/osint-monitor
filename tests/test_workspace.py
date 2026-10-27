"""Situational-awareness workspace: personal priorities, the map's GeoJSON and placement, and the boundary
that priorities are presentation only (they never change a Development, a Situation or the evidence).

Reuses the temporary-database fixtures of the situation evidence tests; personal priorities go to the
per-test user-state database set up in conftest.py."""

import re
from collections import Counter

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect

from osint_monitor.api.app import app
from osint_monitor.api.geo import CountryIndex, placement
from osint_monitor.api.workspace_views import priority_for
from osint_monitor.core.database import Entity, Event, EventItem, ItemEntity, Situation
from osint_monitor.core.user_state import Level, PriorityStore, Scope, default_path
from tests.test_situation_views import add_development, db, seeded  # noqa: F401  (pytest fixtures)


def client():
    return TestClient(app)


def dev_ids(html: str) -> list[int]:
    return [int(x) for x in re.findall(r'class="title"><a href="/developments/(\d+)"', html)]


def add(make, title, principals=(), places=(), lat=None, lon=None, location_name=None, rank=1.0, **fields):
    """A corroborated development (two outlets) with principal actors and place mentions on its items."""
    s = make()
    e = add_development(s, None, title, ["Reuters", "BBC World"], 1, principals=principals, lat=lat, lon=lon,
                        location_name=location_name, rank_score=rank, **fields)
    item_ids = [ei.item_id for ei in s.query(EventItem).filter_by(event_id=e.id)]
    for name in places:
        ent = s.query(Entity).filter_by(canonical_name=name).first() or Entity(canonical_name=name, entity_type="GPE")
        s.add(ent)
        s.flush()
        for i in item_ids:
            s.add(ItemEntity(item_id=i, entity_id=ent.id, role="LOCATION"))
    s.commit()
    eid = e.id
    s.close()
    return eid


def canonical_state(make) -> dict:
    """Everything a priority must never change: Developments, memberships, Situations, evidence links."""
    s = make()
    try:
        return {
            "events": sorted((e.id, e.summary, e.situation_id, e.event_domain, e.confidence_class, e.source_count,
                              e.rank_score, e.lat, e.lon) for e in s.query(Event)),
            "members": sorted((m.event_id, m.item_id) for m in s.query(EventItem)),
            "situations": sorted((x.id, x.slug, x.title, x.status, tuple(x.primary_actors or []))
                                 for x in s.query(Situation)),
        }
    finally:
        s.close()


# --- persistence and stable ids ---------------------------------------------------------------------

def test_priorities_persist_per_scope_and_normal_is_no_row(tmp_path):
    path = tmp_path / "state.db"
    st = PriorityStore(path)
    st.set(Scope.COUNTRY, "CHN", Level.HIGH)
    st.set(Scope.COUNTRY, "RUS", Level.MUTED)
    st.set(Scope.DOMAIN, "economic", Level.LOW)
    again = PriorityStore(path)                                   # a new store on the same file sees them
    assert again.levels(Scope.COUNTRY) == {"CHN": Level.HIGH, "RUS": Level.MUTED}
    assert again.get(Scope.DOMAIN, "economic") is Level.LOW and again.get(Scope.DOMAIN, "military") is Level.NORMAL
    again.set(Scope.COUNTRY, "RUS", Level.NORMAL)                 # NORMAL deletes the row
    assert again.levels(Scope.COUNTRY) == {"CHN": Level.HIGH}
    again.reset(Scope.COUNTRY)
    assert again.levels(Scope.COUNTRY) == {} and again.levels(Scope.DOMAIN) == {"economic": Level.LOW}
    again.reset()
    assert again.levels(Scope.DOMAIN) == {}


def test_priority_api_takes_stable_ids_only(db):
    c = client()
    assert c.put("/api/priorities/country/China", json={"level": "HIGH"}).status_code == 404     # a name, not an id
    assert c.put("/api/priorities/domain/Military", json={"level": "HIGH"}).status_code == 404
    assert c.put("/api/priorities/actor/CHN", json={"level": "HIGH"}).status_code == 404         # unknown scope
    assert c.put("/api/priorities/country/CHN", json={"level": "loud"}).status_code == 422
    assert c.put("/api/priorities/country/CHN", json={"level": "HIGH"}).json()["level"] == "HIGH"
    assert c.put("/api/priorities/domain/military", json={"level": "muted"}).json()["level"] == "MUTED"
    assert c.get("/api/priorities").json() == {"country": {"CHN": "HIGH"}, "domain": {"military": "MUTED"}}
    assert c.delete("/api/priorities/country/CHN").json()["level"] == "NORMAL"
    assert c.delete("/api/priorities").json() == {"country": {}, "domain": {}}
    # HTMX form route: same validation; the panel's buttons post stable ids
    assert c.post("/ui/priorities/country/China", data={"level": "HIGH"}).status_code == 404
    r = c.post("/ui/priorities/country/FRA", data={"level": "HIGH"})
    assert r.status_code == 200 and r.headers["HX-Trigger"] == "priorities-changed"
    assert 'hx-post="/ui/priorities/country/FRA"' in r.text and "France" in r.text
    assert 'hx-post="/ui/priorities/domain/military"' in c.get("/priorities").text
    assert "Germany" in c.get("/ui/countries?q=germ").text


def test_user_state_is_not_in_the_intelligence_database(db):
    make, path = db
    client().put("/api/priorities/country/CHN", json={"level": "HIGH"})
    assert default_path().exists() and default_path().resolve() != path.resolve()
    s = make()
    try:
        assert "preferences" not in inspect(s.get_bind()).get_table_names()
    finally:
        s.close()


# --- ordering, emphasis, mute ---------------------------------------------------------------------------

def test_high_normal_low_reorder_within_the_pipeline_ranking(seeded):
    make, _ = seeded
    first = add(make, "France holds budget vote", principals=["France"], rank=9.0)
    middle = add(make, "Russia moves troops", principals=["Russia"], rank=5.0)
    last = add(make, "China opens port", principals=["China"], rank=1.0)
    c = client()
    order = dev_ids(c.get("/").text)
    assert order.index(first) < order.index(middle) < order.index(last)          # NORMAL: pipeline ranking
    c.put("/api/priorities/country/CHN", json={"level": "HIGH"})
    c.put("/api/priorities/country/FRA", json={"level": "LOW"})
    r = c.get("/")
    order = dev_ids(r.text)
    assert order.index(last) < order.index(middle) < order.index(first)          # HIGH first, LOW after NORMAL
    assert "Surfaced first because: HIGH country: China (actor)" in r.text
    assert "De-emphasised because: LOW country: France (actor)" in r.text
    assert re.search(r'class="dev lvl-HIGH" data-id="%d"' % last, r.text)
    assert "score" not in r.text.lower().replace("nothing here is a score", "")  # no relevance score is shown


def test_mute_hides_by_default_and_show_muted_reveals(seeded):
    make, _ = seeded
    trade = add(make, "Tariff deal signed", principals=["France"], event_domain="economic")
    only_russia = add(make, "Russia drills in the Baltic", principals=["Russia"])
    shared = add(make, "Russia and China meet", principals=["Russia", "China"])
    c = client()
    c.put("/api/priorities/domain/economic", json={"level": "MUTED"})
    c.put("/api/priorities/country/RUS", json={"level": "MUTED"})
    shown = dev_ids(c.get("/").text)
    assert trade not in shown and only_russia not in shown
    assert shared in shown                          # one of its countries is not muted
    r = c.get("/?show_muted=1")
    assert {trade, only_russia, shared} <= set(dev_ids(r.text))
    assert "Muted because: MUTED topic: Economic" in r.text
    geo = c.get("/api/workspace/developments.geojson").json()
    assert all(f["properties"]["level"] != "MUTED" for f in geo["features"])


def test_priority_rules_are_deterministic():
    idx = CountryIndex.load()
    p = lambda dom, countries, cl=None, dl=None: priority_for(dom, countries, cl or {}, dl or {}, idx)  # noqa: E731
    assert p("military", {}).level is Level.NORMAL and p("military", {}).note is None
    assert p("economic", {"CHN": {"actor"}}, {"CHN": Level.HIGH}, {"economic": Level.MUTED}).level is Level.MUTED
    assert p(None, {"RUS": {"actor"}, "CHN": {"actor"}}, {"RUS": Level.MUTED}).level is Level.NORMAL
    assert p(None, {"RUS": {"actor"}}, {"RUS": Level.MUTED}).level is Level.MUTED
    assert p("military", {"FRA": {"location"}}, {"FRA": Level.LOW}, {"military": Level.HIGH}).level is Level.HIGH
    assert p(None, {"FRA": {"location"}, "DEU": {"actor"}}, {"FRA": Level.LOW}).level is Level.NORMAL
    low = p(None, {"FRA": {"location"}, "DEU": {"actor"}}, {"FRA": Level.LOW, "DEU": Level.LOW})
    assert low.level is Level.LOW and low.note.startswith("De-emphasised because: LOW country:")


# --- geography -------------------------------------------------------------------------------------

def test_geneva_meeting_is_located_in_switzerland_and_concerns_the_actors(seeded):
    make, _ = seeded
    geneva = add(make, "US and China envoys meet in Geneva", principals=["United States", "China"],
                 places=["Geneva", "Switzerland"], lat=46.2044, lon=6.1432,
                 location_name="Genève, Switzerland")
    c = client()
    for country in ("CHE", "USA", "CHN"):          # location and actor relevance both select it
        assert geneva in dev_ids(c.get(f"/?country={country}").text)
    assert geneva not in dev_ids(c.get("/?country=FRA").text)
    feature = next(f for f in c.get("/api/workspace/developments.geojson").json()["features"] if f["id"] == geneva)
    assert feature["properties"]["country"] == "CHE"
    assert feature["geometry"]["coordinates"] == [6.1432, 46.2044]
    c.put("/api/priorities/country/CHN", json={"level": "HIGH"})
    r = c.get("/")
    assert "HIGH country: China (actor)" in r.text and "Involves China, United States" in r.text


def test_geojson_never_fabricates_or_trusts_contradicted_coordinates(seeded):
    make, _ = seeded
    paris = add(make, "Strike in Paris", places=["Paris", "France"], lat=48.8566, lon=2.3522,
                location_name="Paris, Île-de-France, France", event_domain="security")
    gaza = add(make, "Shelling in Gaza", places=["Gaza"], lat=-24.0, lon=33.6,          # a "Gaza" in Mozambique
               location_name="Gaza, Moçambique", event_domain="military")
    nowhere = add(make, "Statement without a place", event_domain="political")
    c = client()
    geo = c.get("/api/workspace/developments.geojson").json()
    ids = {f["id"] for f in geo["features"]}
    assert paris in ids and gaza not in ids and nowhere not in ids
    assert geo["unmapped"] >= 2
    feed = c.get("/")
    assert {paris, gaza, nowhere} <= set(dev_ids(feed.text))     # unmapped developments stay in the feed
    assert "No confirmed location" in feed.text
    assert {f["id"] for f in c.get("/api/workspace/developments.geojson?domain=security").json()["features"]} == {paris}
    assert c.get("/api/workspace/developments.geojson?country=FRA").json()["features"][0]["id"] == paris
    assert c.get("/api/workspace/developments.geojson?country=MOZ").json()["features"] == []


def test_placement_check():
    idx = CountryIndex.load()
    ok = placement(idx, 48.8566, 2.3522, "Paris, France", Counter({"Paris": 3, "France": 1}))
    assert ok.mapped and ok.country == "FRA" and not ok.country_level
    wrong = placement(idx, -24.0, 33.6, "Gaza, Moçambique", Counter({"Gaza": 4}))
    assert not wrong.mapped and wrong.country == "PSE" and "Mozambique" in wrong.reason
    assert not placement(idx, None, None, None, Counter({"Gaza": 1})).mapped
    assert not placement(idx, 0.0, 0.0, "Null Island", Counter()).mapped
    unconfirmed = placement(idx, 40.52, -78.39, "Altoona, Pennsylvania", Counter({"Altoona": 2}))
    assert not unconfirmed.mapped                                 # nothing the gazetteer knows confirms it
    assert placement(idx, 53.48, -2.24, "Manchester, England", Counter({"Manchester": 2})).country == "GBR"
    whole = placement(idx, 46.6, 1.89, "France", Counter({"France": 2}))
    assert whole.mapped and whole.country_level


# --- presentation only ----------------------------------------------------------------------------------

def test_priorities_never_change_developments_situations_or_evidence(seeded):
    make, _ = seeded
    add(make, "Russia and China meet", principals=["Russia", "China"], places=["Moscow"], lat=55.75, lon=37.62,
        location_name="Москва, Russia")
    before = canonical_state(make)
    c = client()
    for scope, key, level in [("country", "CHN", "HIGH"), ("country", "RUS", "MUTED"), ("country", "USA", "LOW"),
                              ("domain", "economic", "MUTED"), ("domain", "diplomacy", "HIGH")]:
        assert c.put(f"/api/priorities/{scope}/{key}", json={"level": level}).status_code == 200
    for url in ("/", "/?show_muted=1", "/map", "/?country=CHN", "/api/workspace/developments.geojson",
                "/situations", "/situations/china-united-states", "/priorities"):
        assert c.get(url).status_code == 200
    for eid in [e[0] for e in before["events"]]:
        assert c.get(f"/developments/{eid}").status_code == 200
        assert c.get(f"/developments/{eid}/preview").status_code == 200
    c.delete("/api/priorities")
    assert canonical_state(make) == before


# --- pages ----------------------------------------------------------------------------------------------

def test_workspace_today_map_and_partial(seeded):
    c = client()
    for url in ("/", "/map", "/?range=3d", "/?range=7d&lifecycle=new"):
        r = c.get(url)
        assert r.status_code == 200 and 'id="map"' in r.text and 'id="ws-filters"' in r.text
    partial = c.get("/?range=7d", headers={"HX-Request": "true"})
    assert partial.status_code == 200 and "<html" not in partial.text
    assert 'id="feed"' in partial.text and 'id="context" class="context" hx-swap-oob="true"' in partial.text
    assert "Situations that changed" in partial.text


def test_development_detail_and_preview(seeded):
    make, _ = seeded
    paris = add(make, "Strike in Paris", principals=["France"], places=["Paris"], lat=48.8566, lon=2.3522,
                location_name="Paris, France")
    c = client()
    detail = c.get(f"/developments/{paris}")
    assert detail.status_code == 200 and "Where" in detail.text and "Supporting evidence" in detail.text
    assert "Paris, France" in detail.text and 'href="/map?country=FRA&amp;range=7d"' in detail.text
    preview = c.get(f"/developments/{paris}/preview")
    assert preview.status_code == 200 and "<html" not in preview.text and "Open development and evidence" in preview.text
    assert c.get("/developments/999999/preview").status_code == 404


def test_situation_page_and_its_map(seeded):
    c = client()
    page = c.get("/situations/china-united-states")
    assert page.status_code == 200 and "Geographic context" in page.text and "Latest development" in page.text
    assert "scope=situation&amp;situation=china-united-states" in page.text
    geo = c.get("/api/workspace/developments.geojson?scope=situation&situation=china-united-states&show_muted=1")
    assert geo.status_code == 200 and geo.json()["type"] == "FeatureCollection"
    empty = c.get("/situations/sudan-civil-war")
    assert empty.status_code == 200 and "No developments linked yet" in empty.text
