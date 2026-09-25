"""Pipeline stages that turn clustered events into classified, ranked developments.

  classify_events   ClusterContext -> DevelopmentClassification -> Event columns
  rank_events       Event columns -> RankingInput -> rank_score / rank_reasons

Both are idempotent: an event is re-classified only after it changed, and
ranking is recomputed for the whole recent window (ranks are relative).
Classification values come only from the classifier; nothing is filled in by
guessing. Events the classifier could not handle stay unclassified and remain
usable (they rank with the neutral 'unknown' weights).
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.database import Entity, Event, EventEntity, Situation
from osint_monitor.core.models import (
    Concreteness, ConfidenceClass, DevelopmentClassification, EventDomain, EventType, InteractionMode,
    RankingInput, RoleClass, SignificanceClass, UncertaintyFlag,
)
from osint_monitor.processors.classification import (
    DevelopmentClassifier, HybridClassifier, LLMClassifier, RuleBasedClassifier, get_classifier,
)
from osint_monitor.processors.classification.context import build_cluster_context
from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.entity_resolver import normalise
from osint_monitor.processors.ranking import DevelopmentRanker, PolicyRanker

logger = logging.getLogger(__name__)

RANK_WINDOW_DAYS = 7


# -- classification ----------------------------------------------------------------------

def usable_classifier(classifier: DevelopmentClassifier | None = None) -> DevelopmentClassifier:
    """The configured classifier, or the rule-based one when the LLM backend cannot be used
    (missing key / unknown provider). Checked once per run instead of failing per event."""
    classifier = classifier or get_classifier()
    if isinstance(classifier, (LLMClassifier, HybridClassifier)):
        try:
            classifier.llm
        except Exception as e:
            logger.warning(f"LLM classifier unavailable ({e}); classifying with rules instead")
            return RuleBasedClassifier()
    return classifier


def apply_classification(event: Event, c: DevelopmentClassification, now: datetime) -> None:
    event.event_type = c.event_type.value
    event.event_domain = c.event_domain.value
    event.interaction_mode = c.interaction_mode.value
    event.concreteness = c.concreteness.value
    event.significance_class = c.significance_class.value if c.significance_class else None
    event.change_summary = c.material_change or None
    event.why_it_matters = c.why_it_matters or None
    event.is_routine_commentary = c.is_routine_commentary
    event.uncertainty_flags = [f.value for f in c.uncertainty_flags]
    event.classification_source = c.classifier
    event.classification_notes = c.classification_notes or None
    event.classified_at = now


def stored_classification(event: Event) -> DevelopmentClassification:
    """Rebuild the classification from Event columns; unclassified events get 'unknown'."""
    def enum(cls, value, default):
        try:
            return cls(value) if value else default
        except ValueError:
            return default

    return DevelopmentClassification(
        event_type=enum(EventType, event.event_type, EventType.UNKNOWN),
        event_domain=enum(EventDomain, event.event_domain, EventDomain.UNKNOWN),
        interaction_mode=enum(InteractionMode, event.interaction_mode, InteractionMode.UNKNOWN),
        concreteness=enum(Concreteness, event.concreteness, Concreteness.UNKNOWN),
        significance_class=enum(SignificanceClass, event.significance_class, None),
        is_routine_commentary=bool(event.is_routine_commentary),
        uncertainty_flags=[f for f in (enum(UncertaintyFlag, v, None) for v in event.uncertainty_flags or []) if f],
        classifier=event.classification_source or "",
    )


def classify_events(session: Session, classifier: DevelopmentClassifier | None = None,
                    now: datetime | None = None) -> dict[str, Any]:
    """Classify events that are new or changed since their last classification."""
    now = now or datetime.utcnow()
    classifier = usable_classifier(classifier)
    pending = (session.query(Event)
               .filter((Event.classified_at.is_(None)) | (Event.last_updated_at > Event.classified_at))
               .order_by(Event.id).all())
    stats = {"classifier": getattr(classifier, "name", type(classifier).__name__), "candidates": len(pending),
             "classified": 0, "failed": 0, "fallback": 0, "unknown_type": 0}
    for event in pending:
        try:
            result = classifier.classify(build_cluster_context(session, event.id))
        except Exception as e:
            stats["failed"] += 1
            logger.warning(f"Classification failed for event {event.id}: {e}")
            continue
        apply_classification(event, result, now)
        stats["classified"] += 1
        stats["fallback"] += UncertaintyFlag.CLASSIFIER_FALLBACK in result.uncertainty_flags
        stats["unknown_type"] += result.event_type == EventType.UNKNOWN
    session.commit()
    if stats["failed"] and not stats["classified"]:
        raise RuntimeError(f"classification failed for all {stats['failed']} candidate events")
    return stats


# -- ranking ----------------------------------------------------------------------------------

def _role_lookup(known_roles: dict[str, RoleClass]) -> dict[str, RoleClass]:
    return {normalise(name): role for name, role in known_roles.items()}


def ranking_input(event: Event, principals: list[Entity], roles: dict[str, RoleClass],
                  topic_key: str | None) -> RankingInput:
    confidence = ConfidenceClass.UNVERIFIED
    if event.confidence_class:
        try:
            confidence = ConfidenceClass(event.confidence_class)
        except ValueError:
            pass
    return RankingInput(
        development_id=event.id,
        classification=stored_classification(event),
        confidence=confidence,
        independent_sources=event.source_count or 0,
        actor_roles=[roles[k] for k in (normalise(e.canonical_name) for e in principals
                                         if e.entity_type == "PERSON") if k in roles],
        topic_key=topic_key,
        occurred_at=event.first_reported_at,
        region=event.region,
    )


def rank_events(session: Session, ranker: DevelopmentRanker | None = None, now: datetime | None = None,
                window_days: int = RANK_WINDOW_DAYS) -> dict[str, Any]:
    """Rank every event updated in the window as one batch and store score + reasons."""
    now = now or datetime.utcnow()
    ranker = ranker or PolicyRanker()
    roles = _role_lookup(getattr(getattr(ranker, "config", None), "known_roles", {}) or {})
    events = (session.query(Event)
              .filter(Event.last_updated_at >= now - timedelta(days=window_days))
              .order_by(Event.id).all())
    if not events:
        return {"ranked": 0, "unclassified_ranked": 0}

    principal_rows = (session.query(EventEntity).options(joinedload(EventEntity.entity))
                      .filter(EventEntity.event_id.in_([e.id for e in events]), EventEntity.is_principal.is_(True)))
    principals: dict[int, dict[int, Entity]] = {}
    for ee in principal_rows:
        principals.setdefault(ee.event_id, {})[ee.entity_id] = ee.entity
    slugs = dict(session.query(Situation.id, Situation.slug))
    actors = ActorNormalizer.load()        # "Trump" and "US" principals are one topic

    def topic(event: Event) -> str | None:
        if event.situation_id:
            return slugs.get(event.situation_id)
        names = sorted(actors.keys(e.canonical_name for e in principals.get(event.id, {}).values()))
        return "actors:" + "|".join(names) if names else None

    inputs = [ranking_input(e, list(principals.get(e.id, {}).values()), roles, topic(e)) for e in events]
    by_id = {e.id: e for e in events}
    for r in ranker.rank(inputs, now=now):
        event = by_id[r.development_id]
        event.rank_score = r.score
        event.rank_reasons = [reason.value for reason in r.reasons]
        event.ranked_at = now
    session.commit()
    return {"ranked": len(events), "unclassified_ranked": sum(1 for e in events if e.classified_at is None)}
