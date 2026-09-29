"""Reading pages: Today, Development detail, Situations. Semantics, not markup: what a reader can
and cannot see. Reuses the temporary-database fixtures of the situation evidence tests."""

import re

from fastapi.testclient import TestClient

from osint_monitor.api.app import app
from osint_monitor.core.database import RawItem, Situation, Source
from tests.test_situation_views import NOW, add_development, db, seeded  # noqa: F401  (pytest fixtures)


def page(url, **kw):
    return TestClient(app).get(url, **kw)


def dev_ids(html: str) -> list[int]:
    return [int(x) for x in re.findall(r'class="title"><a href="/developments/(\d+)"', html)]


def extra(make, *specs):
    """Add developments to the seeded database; returns their ids."""
    s = make()
    summit = s.query(Situation).filter_by(slug="china-united-states").one()
    ids = []
    for situated, title, sources, hours, fields in specs:
        ids.append(add_development(s, summit if situated else None, title, sources, hours, **fields).id)
    s.commit()
    s.close()
    return ids


def test_today_lists_corroborated_developments_in_ranking_order(seeded):
    make, _ = seeded
    low, high = extra(make,
                      (False, "Ministers meet in Geneva", ["Reuters", "BBC World"], 1,
                       {"event_type": "bilateral_meeting", "rank_score": 1.0, "rank_reasons": ["physical_interaction"]}),
                      (True, "Navy deploys carrier group", ["Reuters", "Al Jazeera"], 1,
                       {"event_type": "deployment", "rank_score": 9.0, "rank_reasons": ["concrete_action", "stale"],
                        "confidence_class": "probable"}))
    r = page("/")
    assert r.status_code == 200
    order = dev_ids(r.text)
    assert order.index(high) < order.index(low)                          # ranked, not chronological
    assert "Part of <b>China – United States</b>" in r.text and "No active situation" in r.text
    assert "2 independent sources" in r.text and "Probable" in r.text
    assert "Reported action" in r.text and "Older development" in r.text  # reason labels, caveat kept
    assert "9.0" not in r.text                                            # the rank score is never shown


def test_single_source_cluster_and_raw_items_are_not_developments(seeded):
    make, _ = seeded
    [lonely] = extra(make, (False, "Only one outlet reports a blast", ["BBC World"], 1, {"event_type": "security_incident"}))
    s = make()
    src = s.query(Source).filter_by(name="Reuters").one()
    s.add(RawItem(source_id=src.id, title="Unclustered wire story", content="", content_hash="raw-1",
                  published_at=NOW, fetched_at=NOW))
    s.commit()
    s.close()
    r = page("/")
    assert lonely not in dev_ids(r.text) and "Unclustered wire story" not in r.text
    assert "1 story cluster in this period has fewer than two independent sources" in " ".join(r.text.split())
    detail = page(f"/developments/{lonely}")
    assert detail.status_code == 200 and "Awaiting corroboration" in detail.text


def test_unclassified_and_unsituated_developments_render_honestly(seeded):
    make, _ = seeded
    [dev] = extra(make, (False, "Protest outside parliament", ["Reuters", "BBC World"], 1, {}))
    r = page(f"/developments/{dev}")
    assert r.status_code == 200
    assert "Unclassified" in r.text and "No active situation" in r.text
    assert "No principal actors identified" in r.text and "Not assessed" in r.text


def test_development_detail_shows_evidence_reasons_and_classification(seeded):
    make, _ = seeded
    s = make()
    [truce] = [e for e in s.query(__import__("osint_monitor.core.database", fromlist=["Event"]).Event)
               if e.summary.startswith("Trump and Xi agree")]
    s.close()
    r = page(f"/developments/{truce.id}")
    assert r.status_code == 200
    for source in ("Reuters", "Associated Press", "BBC World"):
        assert source in r.text
    assert 'href="https://reuters.example/' in r.text                     # evidence links to the original
    assert "Tariff truce extended by one year." in r.text                 # the stored summary, not an invented one
    assert "Why this surfaced" in r.text and "Classification" in r.text and "Agreement" in r.text
    assert 'href="/situations/china-united-states"' in r.text
    assert "Pacific balance" not in page("/situations/china-united-states").text   # no assessment layer


def test_situation_pages_load_and_reach_evidence_in_one_click(seeded):
    listing = page("/situations")
    assert listing.status_code == 200 and "China – United States" in listing.text and "Sudan civil war" in listing.text
    detail = page("/situations/china-united-states")
    assert detail.status_code == 200 and "Timeline" in detail.text
    first = re.search(r'href="(/developments/\d+)"', detail.text).group(1)
    assert page(first).status_code == 200
    empty = page("/situations/sudan-civil-war")
    assert empty.status_code == 200 and "No developments linked yet" in empty.text
    assert page("/situations/no-such-thing").status_code == 404
    assert page("/developments/999999").status_code == 404


def test_filters_narrow_the_list_and_htmx_gets_only_the_list(seeded):
    make, _ = seeded
    extra(make, (False, "Border clash kills two", ["Reuters", "BBC World"], 1,
                 {"event_type": "military_action", "event_domain": "military", "rank_score": 5.0}))
    military = page("/?domain=military")
    assert "Border clash kills two" in military.text and "Trump and Xi agree" not in military.text
    unsituated = page("/?situation=none")
    assert "Border clash kills two" in unsituated.text and "Trump and Xi agree" not in unsituated.text
    partial = page("/?domain=military", headers={"HX-Request": "true"})
    assert partial.status_code == 200 and "<html" not in partial.text and "Border clash kills two" in partial.text


def test_empty_database_shows_an_empty_state(db):
    r = page("/")
    assert r.status_code == 200
    assert "No corroborated developments in this period." in r.text and "Nothing has been collected yet" in r.text


def test_database_errors_render_an_unavailable_page(monkeypatch):
    import osint_monitor.api.pages as pages
    monkeypatch.setattr(pages, "_session", lambda: (_ for _ in ()).throw(RuntimeError("database is locked")))
    for url in ("/", "/developments/1", "/situations", "/situations/x"):
        r = page(url)
        assert r.status_code == 503 and "could not be read" in r.text
