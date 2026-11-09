"""Multi-source corroboration scoring using the Admiralty/NATO system.

Assigns reliability and credibility ratings to events based on source
diversity, independent confirmation, and cross-item agreement.
"""

from __future__ import annotations

import logging
from collections import Counter
from itertools import combinations

import numpy as np
from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.database import (
    Claim,
    Event,
    EventItem,
    RawItem,
    Source,
)
from osint_monitor.core.models import ConfidenceClass
from osint_monitor.processors.embeddings import (
    blob_to_embedding,
    cosine_similarity,
    embed_text,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Admiralty / NATO rating system
# ---------------------------------------------------------------------------

# Source reliability grades
RELIABILITY_GRADES = {
    "A": "Completely reliable",
    "B": "Usually reliable",
    "C": "Fairly reliable",
    "D": "Not usually reliable",
    "E": "Unreliable",
    "F": "Cannot be judged",
}

# Information credibility grades
CREDIBILITY_GRADES = {
    "1": "Confirmed",
    "2": "Probably true",
    "3": "Possibly true",
    "4": "Doubtful",
    "5": "Improbable",
    "6": "Cannot be judged",
}

# Map source type (Source.type + Source.category) to reliability grade.
# The ``type`` field holds rss/twitter/telegram/sanctions/custom;
# ``category`` refines further (e.g. "official_gov", "wire_service").
SOURCE_TYPE_RELIABILITY: dict[str, str] = {
    "official_gov": "A",
    "wire_service": "B",
    "major_news": "B",
    "analysis": "C",
    "osint_account": "D",
    "individual_twitter": "E",
    "unknown": "F",
}

# Fallback mapping based on collector type when category is absent
_COLLECTOR_TYPE_RELIABILITY: dict[str, str] = {
    "sanctions": "A",
    "rss": "C",
    "twitter": "D",
    "telegram": "D",
    "custom": "E",
}

# Numeric weight per reliability grade (for computing diversity score)
_RELIABILITY_WEIGHT: dict[str, float] = {
    "A": 1.0,
    "B": 0.85,
    "C": 0.65,
    "D": 0.40,
    "E": 0.20,
    "F": 0.10,
}

# Credibility number based on corroboration level
_CORROBORATION_CREDIBILITY: dict[str, str] = {
    "CONFIRMED": "1",
    "PROBABLE": "2",
    "POSSIBLE": "3",
    "DOUBTFUL": "4",
    "UNCONFIRMED": "6",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_source_reliability(source: Source) -> str:
    """Determine the Admiralty reliability grade for a source."""
    # Prefer category-based mapping
    if source.category and source.category in SOURCE_TYPE_RELIABILITY:
        return SOURCE_TYPE_RELIABILITY[source.category]
    # Fall back to collector type
    return _COLLECTOR_TYPE_RELIABILITY.get(source.type, "F")


def _best_reliability(grades: list[str]) -> str:
    """Return the best (lowest letter) reliability grade from a list."""
    order = "ABCDEF"
    best_idx = min((order.index(g) for g in grades), default=5)
    return order[best_idx]


def _compute_diversity_score(source_grades: list[str]) -> float:
    """Compute a 0-1 diversity score based on how varied the source types are.

    Higher diversity = a mix of gov, news, and OSINT sources.
    A single source type yields low diversity; spread across tiers yields high.
    """
    if not source_grades:
        return 0.0

    unique_grades = set(source_grades)
    # Base diversity: fraction of distinct reliability tiers present (out of 5 usable: A-E)
    tier_coverage = len(unique_grades - {"F"}) / 5.0

    # Weight by the quality of sources present
    total_weight = sum(_RELIABILITY_WEIGHT.get(g, 0.1) for g in source_grades)
    avg_weight = total_weight / len(source_grades)

    # Blend tier coverage and average quality
    return min(0.6 * tier_coverage + 0.4 * avg_weight, 1.0)


# ---------------------------------------------------------------------------
# Core scoring
# ---------------------------------------------------------------------------

_EMPTY_SCORE = {
    "independent_sources": 0,
    "outlets": 0,
    "source_diversity": 0.0,
    "admiralty_rating": "F6",
    "corroboration_level": "UNCONFIRMED",
    "confidence": 0.0,
    "confidence_class": ConfidenceClass.UNVERIFIED.value,
    "provenance_flags": [],
}


def compute_corroboration_score(session: Session, event_id: int, resolver=None, categories=None) -> dict:
    """Compute multi-source corroboration score for an event.

    Returns a dict with:
        - ``independent_sources``: independent origins (see processors.provenance)
        - ``outlets``: distinct publishing sources, before collapsing derivative copies
        - ``source_diversity``: 0-1 float indicating type spread
        - ``admiralty_rating``: e.g. ``"B2"``
        - ``corroboration_level``: CONFIRMED / PROBABLE / POSSIBLE / DOUBTFUL / UNCONFIRMED
        - ``confidence``: 0-1 composite confidence
        - ``confidence_class``: ConfidenceClass value from provenance
        - ``provenance_flags``: ProvenanceFlag values, e.g. derivative_collapsed

    ``resolver`` (a ProvenanceResolver) and ``categories`` (the sources.yaml feed categories) may be passed in to reuse
    them across events; by default they are loaded for this call. ``score_events`` scores many events at once.
    """
    # Gather all items + their sources for this event
    event_items = (
        session.query(EventItem)
        .filter(EventItem.event_id == event_id)
        .all()
    )

    if not event_items:
        return dict(_EMPTY_SCORE)

    item_ids = [ei.item_id for ei in event_items]
    items = session.query(RawItem).filter(RawItem.id.in_(item_ids)).all()
    sources_by_id = _sources_of(items, lambda source_id: session.get(Source, source_id))

    def provenance():
        from osint_monitor.processors.provenance import assess_event
        return assess_event(session, event_id, resolver, categories)

    def claims():
        found = session.query(Claim).filter(Claim.event_id == event_id).all()
        if not found:
            # Also check claims linked via items
            found = session.query(Claim).filter(Claim.item_id.in_(item_ids)).all()
        return found

    return _score(event_id, items, sources_by_id, provenance, claims)


def score_events(session: Session, event_ids: list[int], chunk: int = 200) -> dict:
    """``compute_corroboration_score`` for many events: one ProvenanceResolver and one read of the feed categories for
    the whole call, and the members, items (with their sources) and claims loaded per chunk of events instead of per
    event. The scoring itself is the same function on the same rows. Maps event id -> score dict, or -> the exception
    its scoring raised, so the caller can handle a failed event as before."""
    from osint_monitor.processors.provenance import ProvenanceResolver, assess_confidence
    from osint_monitor.processors.provenance.context import _feed_categories, evidence_from_items

    resolver, categories = ProvenanceResolver(), _feed_categories()
    results: dict = {}
    for start in range(0, len(event_ids), chunk):
        ids = event_ids[start:start + chunk]
        members: dict[int, list[int]] = {e: [] for e in ids}
        for event_id, item_id in (session.query(EventItem.event_id, EventItem.item_id)
                                  .filter(EventItem.event_id.in_(ids)).order_by(EventItem.id)):
            members[event_id].append(item_id)
        all_items = sorted({i for v in members.values() for i in v})
        rows = {r.id: r for r in _in_chunks(all_items, lambda part: session.query(RawItem)
                                            .options(joinedload(RawItem.source))
                                            .filter(RawItem.id.in_(part)).all())}
        claims_by_item: dict[int, list] = {}
        for c in _in_chunks(all_items, lambda part: session.query(Claim).filter(Claim.item_id.in_(part))
                            .order_by(Claim.id).all()):
            claims_by_item.setdefault(c.item_id, []).append(c)
        claims_by_event: dict[int, list] = {}
        for c in session.query(Claim).filter(Claim.event_id.in_(ids)).order_by(Claim.id):
            claims_by_event.setdefault(c.event_id, []).append(c)

        for event_id in ids:
            try:
                item_ids = members[event_id]
                if not item_ids:
                    results[event_id] = dict(_EMPTY_SCORE)
                    continue
                items = [rows[i] for i in sorted(set(item_ids)) if i in rows]
                sources_by_id = _sources_of(items, lambda source_id, items=items: next(
                    (i.source for i in items if i.source_id == source_id), None))
                claim_types = {i: {c.claim_type for c in claims_by_item.get(i, [])} for i in item_ids}

                def provenance(items=items, claim_types=claim_types):
                    return assess_confidence(evidence_from_items(items, claim_types, categories), resolver)

                def claims(event_id=event_id, item_ids=item_ids):
                    return claims_by_event.get(event_id) or [c for i in sorted(set(item_ids))
                                                             for c in claims_by_item.get(i, [])]

                results[event_id] = _score(event_id, items, sources_by_id, provenance, claims)
            except Exception as exc:
                results[event_id] = exc
    return results


def _in_chunks(ids: list[int], fetch, size: int = 500) -> list:
    out = []
    for start in range(0, len(ids), size):
        out.extend(fetch(ids[start:start + size]))
    return out


def _sources_of(items, get_source) -> dict:
    """Distinct sources of the items, in item order (the order compute_corroboration_score has always used)."""
    sources_by_id: dict = {}
    for item in items:
        if item.source_id not in sources_by_id:
            source = get_source(item.source_id)
            if source:
                sources_by_id[item.source_id] = source
    return sources_by_id


def _score(event_id: int, items, sources_by_id: dict, provenance, claims) -> dict:
    """The corroboration score from an event's items, their sources, its provenance assessment (a callable, so that
    a failure falls back to counting outlets, as before) and its claims (a callable)."""
    source_ids = {item.source_id for item in items}

    # Independent origins, not outlets: wire copy republished by five outlets counts once,
    # analysis never counts as confirmation.
    assessment = None
    try:
        assessment = provenance()
        independent_count = assessment.independent_origins
    except Exception as exc:
        logger.warning(f"Provenance assessment failed for event {event_id}: {exc}")
        independent_count = len(source_ids)

    # Determine reliability grades for each source
    source_grades = [
        _get_source_reliability(src) for src in sources_by_id.values()
    ]

    best_grade = _best_reliability(source_grades) if source_grades else "F"
    diversity = _compute_diversity_score(source_grades)

    # Determine corroboration level
    high_reliability_grades = {"A", "B", "C"}
    high_rel_count = sum(1 for g in source_grades if g in high_reliability_grades)

    if independent_count >= 3 and high_rel_count >= 2:
        corroboration_level = "CONFIRMED"
    elif independent_count >= 2:
        corroboration_level = "PROBABLE"
    elif independent_count == 1 and best_grade in high_reliability_grades:
        corroboration_level = "POSSIBLE"
    elif independent_count == 1:
        corroboration_level = "DOUBTFUL"
    else:
        corroboration_level = "UNCONFIRMED"

    # Build Admiralty rating: best source reliability + credibility from corroboration
    credibility_number = _CORROBORATION_CREDIBILITY[corroboration_level]
    admiralty_rating = f"{best_grade}{credibility_number}"

    # Composite confidence (0-1)
    source_count_factor = min(independent_count / 5.0, 1.0)
    reliability_factor = _RELIABILITY_WEIGHT.get(best_grade, 0.1)
    confidence = (
        0.35 * source_count_factor
        + 0.30 * reliability_factor
        + 0.20 * diversity
        + 0.15 * (1.0 if corroboration_level in ("CONFIRMED", "PROBABLE") else 0.3)
    )
    confidence = min(confidence, 1.0)

    # Check for contradictions via claims with opposing types about the same subject
    has_contradictions = False
    try:
        # Group by subject, check for assertion vs denial
        from collections import defaultdict as _dd
        subj_types: dict[str, set[str]] = _dd(set)
        for c in claims():
            subj_types[c.subject.lower()].add(c.claim_type)
        for subj, types in subj_types.items():
            if "assertion" in types and "denial" in types:
                has_contradictions = True
                break
            if "confirmation" in types and "denial" in types:
                has_contradictions = True
                break
    except Exception:
        pass

    if assessment and assessment.confidence_class == ConfidenceClass.DISPUTED:
        has_contradictions = True

    return {
        "independent_sources": independent_count,
        "outlets": len(source_ids),
        "source_diversity": round(diversity, 3),
        "admiralty_rating": admiralty_rating,
        "corroboration_level": corroboration_level,
        "confidence": round(confidence, 3),
        "has_contradictions": has_contradictions,
        "confidence_class": assessment.confidence_class.value if assessment else None,
        "provenance_flags": [f.value for f in assessment.flags] if assessment else [],
    }


# ---------------------------------------------------------------------------
# Claim-level corroboration
# ---------------------------------------------------------------------------

def compute_claim_corroboration(session: Session, event_id: int) -> dict:
    """Compute claim-level corroboration for an event.

    Groups claims by (subject, verb_category), checks for supporting and
    contradicting sources, and assigns per-group Admiralty ratings.

    Returns a dict with ``claim_groups``, ``overall_confidence``,
    ``has_contradictions``, and ``contradiction_summary``.
    """
    from collections import defaultdict

    # Query claims linked to event (directly or via items)
    claims = session.query(Claim).filter(Claim.event_id == event_id).all()
    if not claims:
        event_items = (
            session.query(EventItem)
            .filter(EventItem.event_id == event_id)
            .all()
        )
        item_ids = [ei.item_id for ei in event_items]
        if item_ids:
            claims = (
                session.query(Claim)
                .filter(Claim.item_id.in_(item_ids))
                .all()
            )

    event = session.get(Event, event_id)
    event_summary = event.summary if event else ""

    if not claims:
        return {
            "event_summary": event_summary,
            "claim_groups": [],
            "overall_confidence": 0.0,
            "has_contradictions": False,
            "contradiction_summary": "",
        }

    # Group claims by (subject_lower, verb_category)
    # verb_category: take the root verb
    groups: dict[tuple[str, str], list[Claim]] = defaultdict(list)
    for c in claims:
        key = (c.subject.lower().strip(), c.verb.lower().strip())
        groups[key].append(c)

    claim_groups: list[dict] = []
    has_contradictions = False
    contradiction_topics: list[str] = []

    for (subj, verb), group_claims in groups.items():
        topic = f"{subj} {verb}".strip()

        # Separate assertions/confirmations from denials
        assertions: list[dict] = []
        denials: list[dict] = []
        other: list[dict] = []

        seen_sources: set[str] = set()
        unique_assertion_sources: set[str] = set()
        unique_denial_sources: set[str] = set()

        for c in group_claims:
            entry = {
                "claim": c.claim_text[:200],
                "source": c.source_name,
                "rating": "",
            }
            if c.claim_type in ("assertion", "confirmation"):
                assertions.append(entry)
                unique_assertion_sources.add(c.source_name)
            elif c.claim_type == "denial":
                denials.append(entry)
                unique_denial_sources.add(c.source_name)
            else:
                other.append(entry)
            seen_sources.add(c.source_name)

        # Determine consensus
        if assertions and denials:
            consensus = "DISPUTED"
            has_contradictions = True
            contradiction_topics.append(topic)
        elif len(unique_assertion_sources) >= 2:
            consensus = "CONFIRMED"
        elif assertions and not denials:
            consensus = "UNVERIFIED"
        else:
            consensus = "UNVERIFIED"

        # Assign per-group Admiralty rating
        n_sources = len(seen_sources)
        if consensus == "CONFIRMED" and n_sources >= 3:
            group_rating = "B1"
        elif consensus == "CONFIRMED":
            group_rating = "B2"
        elif consensus == "DISPUTED":
            group_rating = "C3"
        elif n_sources >= 2:
            group_rating = "C2"
        else:
            group_rating = "D3"

        # Assign ratings to individual entries
        for entry in assertions + denials + other:
            entry["rating"] = group_rating

        claim_groups.append({
            "topic": topic,
            "assertions": assertions,
            "denials": denials,
            "consensus": consensus,
            "admiralty_rating": group_rating,
        })

    # Overall confidence
    total = len(claim_groups)
    confirmed_count = sum(1 for g in claim_groups if g["consensus"] == "CONFIRMED")
    disputed_count = sum(1 for g in claim_groups if g["consensus"] == "DISPUTED")

    if total > 0:
        overall_confidence = (confirmed_count * 1.0 + (total - confirmed_count - disputed_count) * 0.5) / total
        if has_contradictions:
            overall_confidence *= 0.7  # Penalise for contradictions
    else:
        overall_confidence = 0.0

    # Build contradiction summary
    if contradiction_topics:
        contradiction_summary = (
            f"Sources disagree on: {', '.join(contradiction_topics[:5])}"
        )
    else:
        contradiction_summary = ""

    return {
        "event_summary": event_summary,
        "claim_groups": claim_groups,
        "overall_confidence": round(overall_confidence, 3),
        "has_contradictions": has_contradictions,
        "contradiction_summary": contradiction_summary,
    }


# ---------------------------------------------------------------------------
# Source disagreement detection
# ---------------------------------------------------------------------------

def detect_source_disagreement(session: Session, event_id: int) -> list[dict]:
    """Detect potential disagreements between items within an event.

    Compares item titles (via embeddings) and flags pairs with cosine
    similarity below 0.5 -- these may represent contradictory framing of the
    same underlying event.

    Returns a list of dicts:
        ``{"item_a": str, "item_b": str, "similarity": float}``
    """
    event_items = (
        session.query(EventItem)
        .filter(EventItem.event_id == event_id)
        .all()
    )
    item_ids = [ei.item_id for ei in event_items]
    if len(item_ids) < 2:
        return []

    items = session.query(RawItem).filter(RawItem.id.in_(item_ids)).all()
    if len(items) < 2:
        return []

    # Build title embeddings -- prefer stored embeddings, fall back to on-the-fly
    title_embeddings: list[tuple[RawItem, np.ndarray]] = []
    for item in items:
        if item.embedding is not None:
            try:
                emb = blob_to_embedding(item.embedding)
                title_embeddings.append((item, emb))
                continue
            except Exception:
                pass
        # Fall back: embed the title on the fly
        try:
            emb = embed_text(item.title)
            title_embeddings.append((item, emb))
        except Exception:
            logger.debug(f"Could not embed item {item.id} title for disagreement check")

    if len(title_embeddings) < 2:
        return []

    # Compare all pairs
    disagreements: list[dict] = []
    for (item_a, emb_a), (item_b, emb_b) in combinations(title_embeddings, 2):
        sim = cosine_similarity(emb_a, emb_b)
        if sim < 0.5:
            disagreements.append({
                "item_a": item_a.title,
                "item_b": item_b.title,
                "similarity": round(float(sim), 4),
            })

    # Sort by lowest similarity first (most divergent)
    disagreements.sort(key=lambda d: d["similarity"])

    if disagreements:
        logger.info(
            f"Event {event_id}: found {len(disagreements)} potential "
            f"source disagreement(s)"
        )

    return disagreements


# ---------------------------------------------------------------------------
# Batch scoring
# ---------------------------------------------------------------------------

def score_all_events(session: Session) -> dict[int, dict]:
    """Compute corroboration scores for all events.

    Returns a mapping of ``event_id -> corroboration result dict``.
    """
    events = session.query(Event).all()
    results: dict[int, dict] = {}

    for ev in events:
        try:
            score = compute_corroboration_score(session, ev.id)
            results[ev.id] = score
        except Exception as exc:
            logger.warning(f"Failed to score event {ev.id}: {exc}")

    confirmed = sum(1 for r in results.values() if r["corroboration_level"] == "CONFIRMED")
    probable = sum(1 for r in results.values() if r["corroboration_level"] == "PROBABLE")
    logger.info(
        f"Batch corroboration complete: {len(results)} events scored "
        f"({confirmed} confirmed, {probable} probable)"
    )

    return results
