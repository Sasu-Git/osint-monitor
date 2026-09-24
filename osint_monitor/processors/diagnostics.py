"""Read-only inspection of events for debugging clustering, principals, regions and ranking.

    python main.py inspect                 # top events by rank, with warnings
    python main.py inspect --sort size     # largest clusters first
    python main.py inspect --event 42      # one event in full
"""

from __future__ import annotations

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.config import load_sources_config
from osint_monitor.core.database import Event, EventEntity, EventItem, RawItem, Situation
from osint_monitor.processors.clustering import LARGE_CLUSTER_WARNING, REGION_MIN_SCORE, region_scores
from osint_monitor.processors.embeddings import blob_to_embedding

LOW_COHESION = 0.55          # mean cosine to centroid below this: probably several stories


def describe_event(session: Session, event: Event, regions: dict | None = None) -> dict:
    regions = regions if regions is not None else load_sources_config().regions
    items = (session.query(RawItem).options(joinedload(RawItem.source))
             .join(EventItem, EventItem.item_id == RawItem.id).filter(EventItem.event_id == event.id).all())
    links = (session.query(EventEntity).options(joinedload(EventEntity.entity))
             .filter(EventEntity.event_id == event.id).all())
    vectors = [blob_to_embedding(i.embedding) for i in items if i.embedding is not None]
    cohesion = None
    if len(vectors) >= 2:
        centroid = np.mean(vectors, axis=0)
        cohesion = float(np.mean([np.dot(v, centroid) / (np.linalg.norm(v) * np.linalg.norm(centroid))
                                  for v in vectors]))
    times = [t for t in (i.published_at or i.fetched_at for i in items) if t]
    scores = region_scores(items, regions)
    situation = session.get(Situation, event.situation_id) if event.situation_id else None

    warnings = []
    if len(items) > LARGE_CLUSTER_WARNING:
        warnings.append(f"large cluster ({len(items)} items)")
    if cohesion is not None and cohesion < LOW_COHESION:
        warnings.append(f"low cohesion ({cohesion:.2f})")
    strong = [r for r, s in scores.items() if s >= 2 * REGION_MIN_SCORE]
    if len(strong) > 1:
        warnings.append(f"mixed regions ({', '.join(sorted(strong))})")
    if not any(ee.is_principal for ee in links):
        warnings.append("no principal actors")

    return {
        "id": event.id,
        "summary": event.summary,
        "items": len(items),
        "sources": sorted({i.source.name for i in items if i.source}),
        "principal_actors": sorted({ee.entity.canonical_name for ee in links if ee.is_principal and ee.entity}),
        "entities": sorted({ee.entity.canonical_name for ee in links if ee.entity}),
        "region": event.region,
        "region_scores": dict(scores.most_common()),
        "cohesion": round(cohesion, 3) if cohesion is not None else None,
        "event_type": event.event_type,
        "event_domain": event.event_domain,
        "concreteness": event.concreteness,
        "confidence_class": event.confidence_class,
        "rank_reasons": event.rank_reasons or [],
        "situation": situation.slug if situation else None,
        "earliest": min(times).isoformat() if times else None,
        "latest": max(times).isoformat() if times else None,
        "titles": [i.title for i in items],
        "warnings": warnings,
    }


def select_events(session: Session, sort: str = "rank", limit: int = 10) -> list[Event]:
    q = session.query(Event)
    if sort == "size":
        sizes = dict(session.query(EventItem.event_id, func.count(EventItem.id)).group_by(EventItem.event_id))
        events = q.all()
        events.sort(key=lambda e: (-sizes.get(e.id, 0), e.id))
        return events[:limit]
    if sort == "recent":
        return q.order_by(Event.last_updated_at.desc(), Event.id.desc()).limit(limit).all()
    return q.order_by(Event.rank_score.is_(None), Event.rank_score.desc(), Event.id).limit(limit).all()


def format_event(d: dict, full: bool = False) -> str:
    lines = [f"#{d['id']}  {d['summary'][:100]}",
             f"    items={d['items']} sources={len(d['sources'])} cohesion={d['cohesion']} "
             f"region={d['region']} situation={d['situation']}",
             f"    type={d['event_type']} domain={d['event_domain']} concreteness={d['concreteness']} "
             f"confidence={d['confidence_class']}",
             f"    principals={d['principal_actors'] or '-'}",
             f"    rank reasons={', '.join(d['rank_reasons'][:5]) or '-'}"]
    if d["warnings"]:
        lines.append(f"    WARNING: {'; '.join(d['warnings'])}")
    if full:
        lines.append(f"    region scores={d['region_scores']}")
        lines.append(f"    time span={d['earliest']} .. {d['latest']}")
        lines.append(f"    entities={d['entities']}")
        lines.extend(f"    - {t[:110]}" for t in d["titles"])
    return "\n".join(lines)
