"""Build a ClusterContext from the database (read-only)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.database import Event, EventEntity, EventItem, RawItem
from osint_monitor.core.models import ClusterContext, ContextEntity, ContextItem

EXCERPT_CHARS = 1000


def build_cluster_context(session: Session, event_id: int, max_items: int = 12) -> ClusterContext:
    """Collect an event's items and entities into a classifier input.

    Item order: one item per source first (most credible source first), then the
    remaining items by publication time, so a small ``max_items`` keeps source diversity.
    """
    event = session.get(Event, event_id)
    if event is None:
        raise ValueError(f"Event {event_id} not found")

    items = (
        session.query(RawItem)
        .join(EventItem, EventItem.item_id == RawItem.id)
        .options(joinedload(RawItem.source))
        .filter(EventItem.event_id == event_id)
        .all()
    )
    items.sort(key=lambda i: (-(i.source.credibility_score if i.source else 0.0),
                              i.published_at or i.fetched_at or datetime.max))
    first_per_source, rest, seen = [], [], set()
    for item in items:
        (rest if item.source_id in seen else first_per_source).append(item)
        seen.add(item.source_id)
    ordered = (first_per_source + rest)[:max_items]

    entities = (
        session.query(EventEntity)
        .options(joinedload(EventEntity.entity))
        .filter(EventEntity.event_id == event_id)
        .all()
    )
    seen_names: set[str] = set()
    context_entities = []
    for ee in entities:
        if ee.entity and ee.entity.canonical_name not in seen_names:
            seen_names.add(ee.entity.canonical_name)
            context_entities.append(ContextEntity(name=ee.entity.canonical_name,
                                                  entity_type=ee.entity.entity_type))

    return ClusterContext(
        event_id=event_id,
        items=[
            ContextItem(
                title=i.title,
                excerpt=(i.content or "")[:EXCERPT_CHARS],
                source_name=i.source.name if i.source else "",
                published_at=i.published_at,
                url=i.url or "",
            )
            for i in ordered
        ],
        entities=context_entities,
        location_name=event.location_name,
        has_contradictions=bool(event.has_contradictions),
    )
