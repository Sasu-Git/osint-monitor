"""Read-only situation evidence layer: the web contract, its JSON API and its pages.

Uses a temporary SQLite file (the app serves requests from another thread, so an
in-memory database would be invisible to it)."""

import hashlib
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.api import situation_views
from osint_monitor.api.app import app
from osint_monitor.core.database import Base, Entity, Event, EventEntity, EventItem, RawItem, Situation, Source

NOW = datetime(2026, 9, 25, 12, 0)


@pytest.fixture()
def db(tmp_path, monkeypatch):
    path = tmp_path / "views.db"
    engine = create_engine(f"sqlite:///{path}")
    Base.metadata.create_all(engine)
    make = sessionmaker(bind=engine)
    import osint_monitor.api.routes.situations as routes
    import osint_monitor.core.database as database
    monkeypatch.setattr(database, "get_session", make)
    monkeypatch.setattr(routes, "get_session", make)
    yield make, path
    engine.dispose()


def add_development(s, situation, title, sources, hours_ago, principals=(), **fields):
    event = Event(summary=title, situation_id=situation.id if situation else None,
                  first_reported_at=NOW - timedelta(hours=hours_ago), last_updated_at=NOW - timedelta(hours=hours_ago),
                  source_count=len(sources), **fields)
    s.add(event)
    s.flush()
    for n, name in enumerate(sources):
        src = s.query(Source).filter_by(name=name).first() or Source(name=name, type="rss", url=name,
                                                                     credibility_score=0.9)
        s.add(src)
        s.flush()
        item = RawItem(source_id=src.id, title=f"{name}: {title}", content=f"{title}. Details.",
                       url=f"https://{name.lower().replace(' ', '')}.example/{event.id}", content_hash=f"{event.id}-{n}",
                       published_at=NOW - timedelta(hours=hours_ago, minutes=n), fetched_at=NOW)
        s.add(item)
        s.flush()
        s.add(EventItem(event_id=event.id, item_id=item.id))
    for name in principals:
        ent = s.query(Entity).filter_by(canonical_name=name).first() or Entity(canonical_name=name, entity_type="PERSON")
        s.add(ent)
        s.flush()
        s.add(EventEntity(event_id=event.id, entity_id=ent.id, role="SUBJECT", is_principal=True))
    return event


@pytest.fixture()
def seeded(db):
    make, path = db
    s = make()
    summit = Situation(slug="china-united-states", title="China – United States", status="active",
                       primary_actors=["China", "United States"], created_at=NOW - timedelta(days=1), updated_at=NOW)
    empty = Situation(slug="sudan-civil-war", title="Sudan civil war", status="active",
                      primary_actors=["Sudan", "Rapid Support Forces"], created_at=NOW - timedelta(days=2),
                      updated_at=NOW - timedelta(days=2))
    s.add_all([summit, empty])
    s.flush()
    add_development(s, summit, "Xi arrives at the White House for state visit", ["Reuters", "BBC World"], 30,
                    principals=["Xi Jinping", "Donald Trump"], event_type="diplomatic_visit", event_domain="diplomacy",
                    interaction_mode="physical", concreteness="action", confidence_class="probable",
                    classification_source="rules", rank_reasons=["senior_actor", "physical_interaction"],
                    why_it_matters="This will reshape the Pacific balance.")
    add_development(s, summit, "Trump and Xi agree to extend trade truce", ["Reuters", "Associated Press", "BBC World"],
                    2, principals=["Trump", "Xi"], event_type="agreement", event_domain="economic",
                    concreteness="agreement", confidence_class="confirmed", uncertainty_flags=["single_source"],
                    change_summary="Tariff truce extended by one year.")
    s.commit()
    s.close()
    return make, path


def test_contract_holds_developments_classification_confidence_and_evidence(seeded):
    make, _ = seeded
    detail = situation_views.situation_detail(make(), "china-united-states")
    assert detail.development_count == 2
    truce, visit = detail.developments                        # timeline, newest first
    assert truce.what_happened == "Trump and Xi agree to extend trade truce"
    assert truce.change_summary == "Tariff truce extended by one year."
    assert truce.principal_actors == ["China", "United States"]   # people shown as the states they act for
    assert truce.classification.event_type == "agreement" and truce.classification.concreteness == "agreement"
    assert truce.confidence.confidence_class == "confirmed" and truce.confidence.source_count == 3
    assert {e.source for e in truce.evidence} == {"Reuters", "Associated Press", "BBC World"}
    assert all(e.url.startswith("https://") and e.source_role for e in truce.evidence)
    assert visit.rank_reasons == ["senior_actor", "physical_interaction"]
    assert detail.last_changed == truce.last_updated_at


def test_contract_carries_no_analytical_interpretation(seeded):
    make, _ = seeded
    dumped = situation_views.situation_detail(make(), "china-united-states").model_dump_json()
    assert "why_it_matters" not in dumped and "Pacific balance" not in dumped


def test_list_orders_by_last_change_and_puts_empty_seeds_last(seeded):
    make, _ = seeded
    listed = situation_views.list_situations(make())
    assert [s.slug for s in listed] == ["china-united-states", "sudan-civil-war"]
    assert listed[0].development_count == 2 and listed[0].latest_development.startswith("Trump and Xi agree")
    assert listed[1].development_count == 0 and listed[1].latest_development is None


def test_api_serves_the_contract(seeded):
    client = TestClient(app)
    listing = client.get("/api/situations").json()
    assert [s["slug"] for s in listing] == ["china-united-states", "sudan-civil-war"]
    detail = client.get("/api/situations/china-united-states").json()
    assert len(detail["developments"]) == 2 and detail["developments"][0]["evidence"]
    assert client.get("/api/situations/no-such-thing").status_code == 404


def test_pages_render_situations_and_their_evidence(seeded):
    client = TestClient(app)
    listing = client.get("/situations")
    assert listing.status_code == 200 and 'href="/situations/china-united-states"' in listing.text
    assert "No developments yet" in listing.text and "Sudan civil war" in listing.text
    page = client.get("/situations/china-united-states")
    assert page.status_code == 200
    for expected in ["Trump and Xi agree to extend trade truce", "Tariff truce extended by one year.",
                     "Associated Press", "confirmed", "Timeline", "diplomatic visit"]:
        assert expected in page.text
    assert "Pacific balance" not in page.text
    assert client.get("/situations/no-such-thing").status_code == 404


def test_the_evidence_layer_never_writes(seeded):
    make, path = seeded
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    client = TestClient(app)
    for url in ["/situations", "/situations/china-united-states", "/api/situations",
                "/api/situations/china-united-states"]:
        assert client.get(url).status_code == 200
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
