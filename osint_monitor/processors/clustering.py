"""HDBSCAN event clustering on embeddings."""

from __future__ import annotations

import logging
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta

import hdbscan
import numpy as np
from rapidfuzz import fuzz
from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.config import load_event_grouping_config, load_sources_config
from osint_monitor.core.database import (
    Event, EventEntity, EventItem, ItemEntity, RawItem, Source,
)
from osint_monitor.core.models import ExtractedEntity, EntityType, EntityRole
from osint_monitor.processors.embeddings import blob_to_embedding
from osint_monitor.processors.event_grouping import NARRATIVE, STRUCTURED, group_structured, partition
from osint_monitor.processors.scoring import compute_composite_severity

logger = logging.getLogger(__name__)

DEFAULT_WINDOW_HOURS = 48
MIN_CLUSTER_SIZE = 2

# Cluster refinement (see refine_cluster). Calibrated on live data: reports of the same
# development from different outlets score 0.55-0.67 cosine; different developments on
# the same topic score <= 0.51; templated single-source feeds (sanctions lists, stock
# moves, ADS-B snapshots, seismic) score 0.45-0.85 among themselves.
LINK_SIMILARITY = 0.53             # cross-source link: midpoint between 0.51 (different) and 0.55 (same)
SAME_SOURCE_TITLE_RATIO = 90       # same outlet: only near-identical headlines (story updates) link
MEMBER_SIMILARITY = 0.45           # minimum cosine to the cluster centroid after linking
MAX_LINK_HOURS = 72
LARGE_CLUSTER_WARNING = 10


def recent_items(session: Session, window_hours: int = DEFAULT_WINDOW_HOURS,
                 now: datetime | None = None) -> list[RawItem]:
    """Items fetched in the window whose publication date (if known) is inside it too."""
    cutoff = (now or datetime.utcnow()) - timedelta(hours=window_hours)
    fetched = (
        session.query(RawItem)
        .options(joinedload(RawItem.source))
        .filter(RawItem.fetched_at >= cutoff)
        .all()
    )
    return [i for i in fetched if i.published_at is None or i.published_at >= cutoff]


def cluster_recent_items(
    session: Session,
    window_hours: int = DEFAULT_WINDOW_HOURS,
    min_cluster_size: int = MIN_CLUSTER_SIZE,
    now: datetime | None = None,
) -> list[dict]:
    """Group recent items into events: narrative items by HDBSCAN + link graph on
    embeddings, structured (sensor / record) items by record identity
    (see ``event_grouping``).

    Returns list of cluster dicts: {item_ids, label, summary, severity, region, kind}.
    """
    recent = recent_items(session, window_hours, now)
    narrative, structured = partition(recent, load_event_grouping_config())
    structured_groups = group_structured(structured, min_size=min_cluster_size)
    narrative_groups = cluster_narrative([i for i in narrative if i.embedding is not None], min_cluster_size)
    logger.info(f"Event grouping: {len(narrative_groups)} narrative clusters from {len(narrative)} items, "
                f"{len(structured_groups)} structured groups from {len(structured)} records")
    groups = {n: ids for n, ids in enumerate(narrative_groups)}
    kinds = {n: NARRATIVE for n in groups}
    for ids in structured_groups:
        kinds[len(groups)] = STRUCTURED
        groups[len(groups)] = ids
    clusters = _build_cluster_summaries(session, groups)
    for c in clusters:
        c["kind"] = kinds[c["label"]]
    return clusters


def cluster_narrative(items: list[RawItem], min_cluster_size: int = MIN_CLUSTER_SIZE) -> list[list[int]]:
    """Semantic clustering of prose items (news, statements, analysis)."""
    if len(items) < min_cluster_size:
        logger.info(f"Only {len(items)} items with embeddings, skipping clustering")
        return []

    # Build embedding matrix
    item_ids = []
    embeddings = []
    for item in items:
        try:
            emb = blob_to_embedding(item.embedding)
            embeddings.append(emb)
            item_ids.append(item.id)
        except Exception:
            continue

    if len(embeddings) < min_cluster_size:
        return []

    X = np.array(embeddings)

    # HDBSCAN on cosine distance
    # Convert cosine similarity to distance: d = 1 - sim
    # Since embeddings are normalized, cosine_sim = dot product
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        metric="euclidean",
        cluster_selection_epsilon=0.2,
    )
    labels = clusterer.fit_predict(X)

    # Group by cluster label
    clusters: dict[int, list[int]] = defaultdict(list)
    for idx, label in enumerate(labels):
        if label >= 0:  # -1 = noise
            clusters[label].append(item_ids[idx])

    # Re-cluster large clusters to decompose mega-events into sub-events
    clusters = _split_large_clusters(clusters, item_ids, X)

    # HDBSCAN proposes; the link graph decides (cuts topical and templated-feed merges)
    by_id = {item.id: item for item in items}
    vectors = {item_id: X[idx] for idx, item_id in enumerate(item_ids)}
    refined: dict[int, list[int]] = {}
    for ids in clusters.values():
        for part in refine_cluster([_ClusterMember.of(by_id[i], vectors[i]) for i in ids], min_cluster_size):
            refined[len(refined)] = part
    # HDBSCAN labels small or sparse batches as noise; the same strict links recover
    # multi-outlet reports of one development among them
    clustered = {i for part in refined.values() for i in part}
    noise = [_ClusterMember.of(by_id[i], vectors[i]) for i in item_ids if i not in clustered]
    noise = _attach_to_clusters(noise, refined, by_id, vectors)
    rescued = refine_cluster(noise, min_cluster_size)
    for part in rescued:
        refined[len(refined)] = part
    for part in refined.values():
        if len(part) > LARGE_CLUSTER_WARNING:
            logger.warning(f"Large event cluster: {len(part)} items (first: {by_id[part[0]].title[:80]!r})")
    logger.info(f"Found {len(refined)} clusters from {len(items)} items "
                f"({len(clusters)} HDBSCAN candidates, {len(rescued)} recovered from noise)")

    return list(refined.values())


class _ClusterMember:
    __slots__ = ("id", "source_id", "title", "time", "vector")

    def __init__(self, id, source_id, title, time, vector):
        self.id, self.source_id, self.title, self.time, self.vector = id, source_id, title, time, vector

    @classmethod
    def of(cls, item: RawItem, vector: np.ndarray) -> "_ClusterMember":
        return cls(item.id, item.source_id, item.title or "", item.published_at or item.fetched_at, vector)


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b)) / denom if denom else 0.0


def _linked(a: _ClusterMember, b: _ClusterMember) -> bool:
    if a.time and b.time and abs((a.time - b.time).total_seconds()) > MAX_LINK_HOURS * 3600:
        return False
    if a.source_id == b.source_id:
        return fuzz.ratio(a.title.lower(), b.title.lower()) >= SAME_SOURCE_TITLE_RATIO
    return _cosine(a.vector, b.vector) >= LINK_SIMILARITY


def _attach_to_clusters(noise: list[_ClusterMember], clusters: dict[int, list[int]],
                        by_id: dict, vectors: dict) -> list[_ClusterMember]:
    """Add each noise item to the cluster it links to and sits closest to; return the rest."""
    members = {label: [_ClusterMember.of(by_id[i], vectors[i]) for i in ids] for label, ids in clusters.items()}
    centroids = {label: np.mean([m.vector for m in ms], axis=0) for label, ms in members.items()}
    left = []
    for item in noise:
        best, best_sim = None, MEMBER_SIMILARITY
        for label, ms in members.items():
            sim = _cosine(item.vector, centroids[label])
            if sim >= best_sim and any(_linked(item, m) for m in ms):
                best, best_sim = label, sim
        if best is None:
            left.append(item)
        else:
            clusters[best].append(item.id)
    return left


def refine_cluster(members: list[_ClusterMember], min_size: int = MIN_CLUSTER_SIZE) -> list[list[int]]:
    """Split a candidate cluster into connected components of linked items, then drop
    members far from their component's centroid. Components below ``min_size`` vanish."""
    remaining = list(range(len(members)))
    parts: list[list[int]] = []
    while remaining:
        stack, component = [remaining.pop(0)], []
        while stack:
            i = stack.pop()
            component.append(i)
            linked = [j for j in remaining if _linked(members[i], members[j])]
            for j in linked:
                remaining.remove(j)
            stack.extend(linked)
        if len(component) >= min_size:
            parts.append(component)

    result = []
    for component in parts:
        centroid = np.mean([members[i].vector for i in component], axis=0)
        kept = [i for i in component if _cosine(members[i].vector, centroid) >= MEMBER_SIMILARITY]
        if len(kept) >= min_size:
            result.append([members[i].id for i in kept])
    return result


def _split_large_clusters(
    clusters: dict[int, list[int]],
    all_item_ids: list[int],
    X: np.ndarray,
    max_cluster_size: int = 15,
) -> dict[int, list[int]]:
    """Re-cluster any cluster with more than *max_cluster_size* items.

    Uses stricter HDBSCAN parameters (epsilon=0.1, min_cluster_size=2) on
    just the subset embeddings to decompose mega-events into distinct
    sub-events (e.g. separating a blockade from a missile debate).
    """
    # Build a lookup from item_id to index in X
    id_to_idx = {item_id: idx for idx, item_id in enumerate(all_item_ids)}

    result: dict[int, list[int]] = {}
    next_label = max(clusters.keys(), default=-1) + 1

    for label, ids in clusters.items():
        if len(ids) <= max_cluster_size:
            result[next_label] = ids
            next_label += 1
            continue

        # Extract the subset of embeddings for this cluster
        subset_indices = [id_to_idx[i] for i in ids if i in id_to_idx]
        if len(subset_indices) < 2:
            result[next_label] = ids
            next_label += 1
            continue

        subset_X = X[subset_indices]
        subset_ids = [ids[j] for j, i in enumerate(ids) if i in id_to_idx]

        sub_clusterer = hdbscan.HDBSCAN(
            min_cluster_size=2,
            metric="euclidean",
            cluster_selection_epsilon=0.1,
        )
        sub_labels = sub_clusterer.fit_predict(subset_X)

        sub_clusters: dict[int, list[int]] = defaultdict(list)
        noise_items: list[int] = []
        for idx, sub_label in enumerate(sub_labels):
            if sub_label >= 0:
                sub_clusters[sub_label].append(subset_ids[idx])
            else:
                noise_items.append(subset_ids[idx])

        if len(sub_clusters) <= 1:
            # Re-clustering didn't help; keep original cluster
            result[next_label] = ids
            next_label += 1
        else:
            logger.info(
                f"Split large cluster (size {len(ids)}) into "
                f"{len(sub_clusters)} sub-clusters"
            )
            for sub_ids in sub_clusters.values():
                result[next_label] = sub_ids
                next_label += 1
            # Noise items stay out: dumping them into the largest sub-cluster built mega-events
            if noise_items:
                logger.debug(f"Dropped {len(noise_items)} noise items when splitting a cluster of {len(ids)}")

    return result


def _build_cluster_summaries(
    session: Session,
    clusters: dict[int, list[int]],
) -> list[dict]:
    """Build event summaries for each cluster."""
    # Load region config once for all clusters
    try:
        sources_config = load_sources_config()
        regions = sources_config.regions  # dict[str, RegionConfig]
    except Exception:
        logger.warning("Could not load sources config for region assignment")
        regions = {}

    results = []
    for label, ids in clusters.items():
        items = (
            session.query(RawItem)
            .options(joinedload(RawItem.source))
            .filter(RawItem.id.in_(ids))
            .all()
        )
        if not items:
            continue

        # Pick summary from highest-credibility source
        best_item = max(items, key=lambda i: i.source.credibility_score)

        # --- Compute severity as max across all items in the cluster ---
        max_severity = 0.0
        for item in items:
            item_text = f"{item.title or ''} {item.content or ''}"
            # Build ExtractedEntity list from ItemEntity records
            item_entities = _get_extracted_entities_for_item(session, item.id)
            source_name = item.source.name if item.source else ""
            score_result = compute_composite_severity(
                text=item_text,
                entities=item_entities,
                source_name=source_name,
            )
            if score_result["severity"] > max_severity:
                max_severity = score_result["severity"]

        # --- Assign region based on keyword matching ---
        region = _assign_region(items, regions)

        results.append({
            "item_ids": ids,
            "label": label,
            "summary": best_item.title,
            "event_type": None,
            "severity": max_severity,
            "region": region,
            "source_count": len(set(i.source_id for i in items)),
        })

    return results


def _get_extracted_entities_for_item(
    session: Session, item_id: int
) -> list[ExtractedEntity]:
    """Load ItemEntity records for an item and convert to ExtractedEntity models."""
    item_entities = (
        session.query(ItemEntity)
        .filter(ItemEntity.item_id == item_id)
        .all()
    )
    result = []
    for ie in item_entities:
        try:
            entity = ie.entity
            result.append(ExtractedEntity(
                text=ie.span_text or entity.canonical_name,
                entity_type=EntityType(entity.entity_type),
                role=EntityRole(ie.role) if ie.role else EntityRole.SUBJECT,
                confidence=ie.confidence,
                canonical_name=entity.canonical_name,
            ))
        except Exception:
            continue
    return result


REGION_TITLE_WEIGHT = 3
REGION_BODY_WEIGHT = 1
REGION_MIN_SCORE = 2        # a single incidental body mention is not enough


def _keyword_pattern(keyword: str) -> re.Pattern:
    """Whole-word match; all-caps acronyms (PLA, PLAN, IRGC) are case-sensitive so that
    'plan' or 'place' never count as China."""
    flags = 0 if keyword.isupper() else re.IGNORECASE
    return re.compile(rf"(?<!\w){re.escape(keyword)}(?!\w)", flags)


def region_scores(items: list[RawItem], regions: dict) -> Counter:
    """Per region: headline hits weigh more than body hits; each item counts once per field."""
    patterns = {name: [_keyword_pattern(k) for k in cfg.keywords] for name, cfg in regions.items()}
    scores: Counter = Counter()
    for item in items:
        for text, weight in ((item.title or "", REGION_TITLE_WEIGHT), (item.content or "", REGION_BODY_WEIGHT)):
            for name, pats in patterns.items():
                if any(p.search(text) for p in pats):
                    scores[name] += weight
    return scores


def _assign_region(
    items: list[RawItem],
    regions: dict,
) -> str | None:
    """Region whose keywords dominate the cluster's headlines (and, less, bodies).

    Returns None when no region reaches REGION_MIN_SCORE or two regions tie:
    mixed-region reporting stays unlabelled rather than taking the first match.
    """
    if not regions:
        return None
    ranked = region_scores(items, regions).most_common(2)
    if not ranked or ranked[0][1] < REGION_MIN_SCORE:
        return None
    if len(ranked) > 1 and ranked[1][1] == ranked[0][1]:
        return None
    return ranked[0][0]


def persist_clusters(session: Session, clusters: list[dict]) -> int:
    """Save clusters as Event records in the database. Returns the number of new events
    (clusters that overlap an existing event extend it instead)."""
    created = 0
    for cluster in clusters:
        # Check if this cluster overlaps with an existing event
        existing_event = _find_overlapping_event(session, cluster["item_ids"])

        if existing_event:
            # Update existing event with new items
            new_item_ids = []
            for item_id in cluster["item_ids"]:
                if not session.query(EventItem).filter_by(
                    event_id=existing_event.id, item_id=item_id
                ).first():
                    session.add(EventItem(
                        event_id=existing_event.id,
                        item_id=item_id,
                        similarity_score=1.0,
                    ))
                    new_item_ids.append(item_id)
            if new_item_ids:
                # Re-clustering the same items is not an update: downstream stages
                # re-classify and treat the event as fresh when this moves.
                existing_event.last_updated_at = datetime.utcnow()
            # Update severity and region if the new cluster has better values
            if cluster.get("severity", 0.0) > existing_event.severity:
                existing_event.severity = cluster["severity"]
            if cluster.get("region") and not existing_event.region:
                existing_event.region = cluster["region"]
            session.flush()

            # Populate event_entities for newly added items
            _populate_event_entities(session, existing_event.id, new_item_ids)
        else:
            # Create new event
            event = Event(
                summary=cluster["summary"],
                event_type=cluster.get("event_type"),
                severity=cluster.get("severity", 0.0),
                region=cluster.get("region"),
                first_reported_at=datetime.utcnow(),
                last_updated_at=datetime.utcnow(),
            )
            session.add(event)
            session.flush()
            created += 1

            for item_id in cluster["item_ids"]:
                session.add(EventItem(
                    event_id=event.id,
                    item_id=item_id,
                    similarity_score=1.0,
                ))
            session.flush()

            # Populate event_entities from all items in the cluster
            _populate_event_entities(session, event.id, cluster["item_ids"])

            # Link claims to event
            _link_claims_to_event(session, event.id, cluster["item_ids"])

    session.commit()
    return created


def _link_claims_to_event(session: Session, event_id: int, item_ids: list[int]):
    """Link existing claims from items to the event."""
    try:
        from osint_monitor.core.database import Claim
        session.query(Claim).filter(
            Claim.item_id.in_(item_ids),
            Claim.event_id.is_(None),
        ).update({"event_id": event_id}, synchronize_session="fetch")
    except Exception:
        pass  # Claim table may not exist in older DBs


def _populate_event_entities(
    session: Session, event_id: int, item_ids: list[int]
):
    """Copy unique entity references from ItemEntity to EventEntity for an event."""
    if not item_ids:
        return

    # Query all ItemEntity records for the given items
    item_entities = (
        session.query(ItemEntity)
        .filter(ItemEntity.item_id.in_(item_ids))
        .all()
    )

    # Find existing event_entity pairs to avoid duplicates
    existing_pairs = set()
    existing_event_entities = (
        session.query(EventEntity)
        .filter(EventEntity.event_id == event_id)
        .all()
    )
    for ee in existing_event_entities:
        existing_pairs.add((ee.entity_id, ee.role))

    # Add unique entity references
    seen = set()
    for ie in item_entities:
        key = (ie.entity_id, ie.role)
        if key not in seen and key not in existing_pairs:
            seen.add(key)
            session.add(EventEntity(
                event_id=event_id,
                entity_id=ie.entity_id,
                role=ie.role,
            ))

    session.flush()


def _find_overlapping_event(session: Session, item_ids: list[int]) -> Event | None:
    """Find an existing event that shares items with this cluster."""
    existing = (
        session.query(EventItem)
        .filter(EventItem.item_id.in_(item_ids))
        .first()
    )
    if existing:
        return existing.event
    return None
