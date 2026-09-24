"""Build EvidenceItems for an event from the database (read-only)."""

from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.config import load_sources_config
from osint_monitor.core.database import Claim, EventItem, RawItem
from osint_monitor.core.models import EvidenceItem, ItemStance

TEXT_CHARS = 2000


def _feed_categories() -> dict[str, str]:
    """Source.category is not populated by the collectors; fall back to sources.yaml."""
    try:
        return {f.name: f.category for f in load_sources_config().rss_feeds}
    except (OSError, ValueError):
        return {}


def build_evidence(session: Session, event_id: int) -> list[EvidenceItem]:
    items = (
        session.query(RawItem)
        .join(EventItem, EventItem.item_id == RawItem.id)
        .options(joinedload(RawItem.source))
        .filter(EventItem.event_id == event_id)
        .all()
    )
    if not items:
        return []

    # An item whose extracted claims are all denials is the source denying the development.
    claim_types: dict[int, set[str]] = {}
    for item_id, claim_type in (session.query(Claim.item_id, Claim.claim_type)
                                .filter(Claim.item_id.in_([i.id for i in items]))):
        claim_types.setdefault(item_id, set()).add(claim_type)

    categories = _feed_categories()
    evidence = []
    for item in sorted(items, key=lambda i: i.id):
        source = item.source
        name = source.name if source else ""
        types = claim_types.get(item.id, set())
        evidence.append(EvidenceItem(
            item_id=item.id,
            source_name=name,
            source_category=(source.category if source else None) or categories.get(name),
            collector_type=source.type if source else None,
            title=item.title,
            text=(item.content or "")[:TEXT_CHARS],
            url=item.url or "",
            published_at=item.published_at or item.fetched_at,
            stance=ItemStance.DENIES if types == {"denial"} else ItemStance.SUPPORTS,
        ))
    return evidence
