"""Database side of situation grouping: seeds, profiles, applying assignments, status."""

from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.config import SituationsConfig
from osint_monitor.core.database import Event, EventEntity, EventItem, RawItem, Situation
from osint_monitor.core.models import (
    DevelopmentBrief, DevelopmentSignature, SituationAssignment, SituationOverview, SituationProfile,
    SituationStatus,
)
from osint_monitor.processors.embeddings import blob_to_embedding
from osint_monitor.processors.situations.grouper import SituationGrouper

ACTOR_ENTITY_TYPES = {"GPE", "ORG", "NORP"}


# -- seeds ------------------------------------------------------------------------------------

def sync_seeds(session: Session, config: SituationsConfig, now: datetime | None = None) -> None:
    """Upsert situations.yaml seeds by slug. Only an explicit YAML status change (closing, or
    reopening a closed one) overrides the automatic active/dormant status."""
    now = now or datetime.utcnow()
    existing = {s.slug: s for s in session.query(Situation).filter(
        Situation.slug.in_([seed.slug for seed in config.situations]))}
    for seed in config.situations:
        row = existing.get(seed.slug)
        if row is None:
            session.add(Situation(slug=seed.slug, title=seed.title, short_description=seed.short_description,
                                  status=seed.status.value, region=seed.region,
                                  primary_actors=list(seed.primary_actors), created_at=now, updated_at=now))
            continue
        row.title, row.short_description = seed.title, seed.short_description
        row.region, row.primary_actors = seed.region, list(seed.primary_actors)
        if seed.status == SituationStatus.CLOSED or row.status == SituationStatus.CLOSED.value:
            row.status = seed.status.value
    session.flush()


# -- profiles and signatures -----------------------------------------------------------------

def _event_embedding(session: Session, event_ids: list[int]) -> list[float] | None:
    blobs = [b for (b,) in session.query(RawItem.embedding)
             .join(EventItem, EventItem.item_id == RawItem.id)
             .filter(EventItem.event_id.in_(event_ids), RawItem.embedding.isnot(None))]
    if not blobs:
        return None
    return np.mean([blob_to_embedding(b) for b in blobs], axis=0).tolist()


def load_profiles(session: Session, config: SituationsConfig) -> list[SituationProfile]:
    keywords = {seed.slug: seed.keywords for seed in config.situations}
    n = config.policy.centroid_developments
    profiles = []
    for s in session.query(Situation).order_by(Situation.id):
        recent = [eid for (eid,) in session.query(Event.id).filter(Event.situation_id == s.id)
                  .order_by(Event.last_updated_at.desc()).limit(n)]
        profiles.append(SituationProfile(
            situation_id=s.id, slug=s.slug, title=s.title, short_description=s.short_description or "",
            status=SituationStatus(s.status), region=s.region, primary_actors=list(s.primary_actors or []),
            keywords=keywords.get(s.slug, []),
            centroid=_event_embedding(session, recent) if recent else None,
        ))
    return profiles


def signature_for_event(session: Session, event: Event) -> DevelopmentSignature:
    actors = [ee.entity.canonical_name for ee in
              session.query(EventEntity).options(joinedload(EventEntity.entity))
              .filter(EventEntity.event_id == event.id)
              if ee.entity and ee.entity.entity_type in ACTOR_ENTITY_TYPES]
    return DevelopmentSignature(
        event_id=event.id, title=event.summary, actors=list(dict.fromkeys(actors)), region=event.region,
        occurred_at=event.first_reported_at, embedding=_event_embedding(session, [event.id]),
    )


# -- the pipeline stage -------------------------------------------------------------------------

def assign_situations(session: Session, grouper: SituationGrouper | None = None,
                      now: datetime | None = None) -> list[SituationAssignment]:
    """Group recent unassigned developments into situations and persist the result.
    Developments already in a situation are never moved."""
    grouper = grouper or SituationGrouper()
    cfg = grouper.config
    now = now or datetime.utcnow()
    sync_seeds(session, cfg, now)

    window_start = now - timedelta(days=cfg.policy.create_window_days)
    events = (session.query(Event)
              .filter(Event.situation_id.is_(None), Event.last_updated_at >= window_start)
              .order_by(Event.first_reported_at, Event.id).all())
    assignments: list[SituationAssignment] = []
    if events:
        signatures = [signature_for_event(session, e) for e in events]
        assignments, created = grouper.group(signatures, load_profiles(session, cfg))
        for p in created:
            session.add(Situation(slug=p.slug, title=p.title, short_description=p.short_description or None,
                                  status=SituationStatus.ACTIVE.value, region=p.region,
                                  primary_actors=p.primary_actors, created_at=now, updated_at=now))
        session.flush()

        by_slug = {s.slug: s for s in session.query(Situation)}
        by_id = {e.id: e for e in events}
        for a in assignments:
            if a.slug is None:
                continue
            situation, event = by_slug[a.slug], by_id[a.event_id]
            event.situation_id = situation.id
            _touch(situation, event)

    refresh_statuses(session, cfg, now)
    session.commit()
    return assignments


def _touch(situation: Situation, event: Event) -> None:
    """A new development arrived: move the situation's clock forward, wake it if dormant."""
    seen = event.last_updated_at or event.first_reported_at
    if seen and (situation.updated_at is None or seen > situation.updated_at):
        situation.updated_at = seen
    if situation.status == SituationStatus.DORMANT.value:
        situation.status = SituationStatus.ACTIVE.value
    if not situation.region and event.region:
        situation.region = event.region


def refresh_statuses(session: Session, config: SituationsConfig, now: datetime | None = None) -> None:
    now = now or datetime.utcnow()
    cutoff = now - timedelta(days=config.policy.dormant_after_days)
    (session.query(Situation)
     .filter(Situation.status == SituationStatus.ACTIVE.value, Situation.updated_at < cutoff)
     .update({Situation.status: SituationStatus.DORMANT.value}, synchronize_session=False))


# -- read side ----------------------------------------------------------------------------------

def situation_overview(session: Session, situation_id: int, config: SituationsConfig,
                       recent_days: int = 7, limit: int = 10, now: datetime | None = None) -> SituationOverview:
    s = session.get(Situation, situation_id)
    if s is None:
        raise ValueError(f"Situation {situation_id} not found")
    now = now or datetime.utcnow()
    members = session.query(Event).filter(Event.situation_id == s.id)
    recent = (members.filter(Event.last_updated_at >= now - timedelta(days=recent_days))
              .order_by(Event.last_updated_at.desc(), Event.id.desc()).limit(limit).all())
    keywords = {seed.slug: seed.keywords for seed in config.situations}
    return SituationOverview(
        situation=SituationProfile(situation_id=s.id, slug=s.slug, title=s.title,
                                   short_description=s.short_description or "", status=SituationStatus(s.status),
                                   region=s.region, primary_actors=list(s.primary_actors or []),
                                   keywords=keywords.get(s.slug, [])),
        created_at=s.created_at, updated_at=s.updated_at, development_count=members.count(),
        recent_developments=[DevelopmentBrief(event_id=e.id, title=e.summary, occurred_at=e.first_reported_at,
                                              corroboration_level=e.corroboration_level) for e in recent],
    )
