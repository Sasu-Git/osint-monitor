"""Taxonomy config consistency, backend selection, and the DB -> context adapter."""

from datetime import datetime, timedelta

import pytest

from osint_monitor.core.config import load_development_types
from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem, Source
from osint_monitor.core.models import EventType
from osint_monitor.processors.classification import LLMClassifier, RuleBasedClassifier, get_classifier
from osint_monitor.processors.classification.context import build_cluster_context


def test_every_event_type_has_defaults():
    assert set(load_development_types()) == set(EventType)


def test_backend_selection():
    assert isinstance(get_classifier("rules"), RuleBasedClassifier)
    assert isinstance(get_classifier("llm"), LLMClassifier)   # provider is created lazily
    with pytest.raises(ValueError):
        get_classifier("magic")


def test_build_cluster_context(session):
    wire = Source(name="Wire", type="rss", url="u1", credibility_score=0.9)
    blog = Source(name="Blog", type="rss", url="u2", credibility_score=0.3)
    session.add_all([wire, blog])
    session.flush()
    now = datetime.utcnow()
    items = [
        RawItem(source_id=blog.id, title="Blog take", content="x", content_hash="h1", published_at=now - timedelta(hours=3)),
        RawItem(source_id=wire.id, title="Wire first", content="y" * 2000, content_hash="h2", published_at=now - timedelta(hours=2)),
        RawItem(source_id=wire.id, title="Wire update", content="z", content_hash="h3", published_at=now - timedelta(hours=1)),
    ]
    event = Event(summary="Wire first", location_name="Muscat", has_contradictions=True)
    iran = Entity(canonical_name="Iran", entity_type="GPE")
    session.add_all(items + [event, iran])
    session.flush()
    session.add_all([EventItem(event_id=event.id, item_id=i.id) for i in items])
    session.add_all([EventEntity(event_id=event.id, entity_id=iran.id, role="SUBJECT"),
                     EventEntity(event_id=event.id, entity_id=iran.id, role="LOCATION")])
    session.commit()

    ctx = build_cluster_context(session, event.id)
    # one item per source first (most credible first), then the rest
    assert [i.title for i in ctx.items] == ["Wire first", "Blog take", "Wire update"]
    assert len(ctx.items[0].excerpt) == 1000
    assert [e.name for e in ctx.entities] == ["Iran"]
    assert ctx.location_name == "Muscat"
    assert ctx.has_contradictions
    assert len(build_cluster_context(session, event.id, max_items=2).items) == 2

    with pytest.raises(ValueError):
        build_cluster_context(session, 9999)
