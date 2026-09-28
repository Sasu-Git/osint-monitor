"""Development segmentation: split a narrative cluster into concrete Developments.

Narrative clustering answers "are these reports about the same story?". Similarity cannot
answer "do they describe the same occurrence?": a strike, the next night's strike, the
reaction to it and an explainer about it all read alike. This step re-checks each link
inside a cluster and drops the ones where the two items are incompatible as one
Development (evaluations/clustering/development-identity-diagnosis.md):

- ``analysis_headlines``: an analysis/explainer headline ("Why ...?", "What we know ...")
  never describes the same Development as a report headline;
- ``min_headline_similarity``: two outlets' headlines that do not describe the same thing
  (headline-only cosine below the threshold) are not one Development, however similar the
  bodies (this separates "N dead after ..." template disasters);
- ``disjoint_locations``: items that name places but share none are not one Development.

A cluster becomes the connected components of its remaining links. Analysis items cut off
this way are not evidence of a Development; they are returned as commentary on the group they
discussed. Other cut-off singletons return to the unclustered pool.

Off by default (``development_segmentation.enabled`` in config/event_grouping.yaml).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime

import numpy as np

from osint_monitor.core.config import DevelopmentSegmentationConfig

logger = logging.getLogger(__name__)

# Headline form. Rolling coverage (live blogs, day-N roundups) mixes developments, so it
# is neither a report nor analysis of one.
ROLLING_HEADLINE = re.compile(r"\blive\b|\bas it happened\b|\bday \d+\b|\broundup\b|\bweekly\b|\bbriefing\b", re.I)
ANALYSIS_HEADLINE = re.compile(
    r"^(what|why|how|will|can|could|is|are|does|do|who|should|where)\b|\?|\bwhat we know\b|\bexplain|"
    r"\banalysis\b|\bopinion\b|\btakeaways?\b|\blessons\b|\bwhat it means\b|\bwhat'?s next\b|\bwhat next\b|"
    r"\bwhat to expect\b|\bin (charts|pictures|maps)\b|\bcould\b.*\bbe\b|\bmay soon\b|\bsignals?\b", re.I)

REPORT, ANALYSIS, ROLLING = "report", "analysis", "rolling"


def headline_kind(title: str) -> str:
    if ROLLING_HEADLINE.search(title or ""):
        return ROLLING
    if ANALYSIS_HEADLINE.search(title or ""):
        return ANALYSIS
    return REPORT


@dataclass
class SegmentItem:
    id: int | str
    source: str | int
    title: str
    published_at: datetime | None
    vector: np.ndarray                    # the clustering embedding (title + lead)
    headline_vector: np.ndarray | None    # headline-only embedding
    locations: set[str] = field(default_factory=set)


@dataclass
class Segmentation:
    groups: list[list]                                   # item ids per Development
    commentary: dict = field(default_factory=dict)       # analysis item id -> index into groups
    detached: list = field(default_factory=list)         # other items cut off, back to the unclustered pool
    cuts: list[tuple] = field(default_factory=list)      # (item a, item b, guard) for every dropped link


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b)) / denom if denom else 0.0


def incompatibility(a: SegmentItem, b: SegmentItem, config: DevelopmentSegmentationConfig) -> str | None:
    """The guard that rules out a and b being one Development, or None."""
    if config.analysis_headlines and {headline_kind(a.title), headline_kind(b.title)} == {ANALYSIS, REPORT}:
        return "analysis_headline"
    if (config.min_headline_similarity is not None and a.source != b.source
            and a.headline_vector is not None and b.headline_vector is not None
            and _cosine(a.headline_vector, b.headline_vector) < config.min_headline_similarity):
        return "headline_similarity"
    if config.disjoint_locations and a.locations and b.locations and not (a.locations & b.locations):
        return "disjoint_locations"
    return None


def segment(items: list[SegmentItem], config: DevelopmentSegmentationConfig, min_size: int = 2) -> Segmentation:
    """Split one narrative cluster into Developments. Links are the clusterer's own
    (``clustering._linked``); only incompatible ones are dropped, so nothing new is joined."""
    from osint_monitor.processors.clustering import _ClusterMember, _linked

    members = [_ClusterMember(i.id, i.source, i.title, i.published_at, i.vector) for i in items]
    n = len(items)
    edges: dict[int, set[int]] = {i: set() for i in range(n)}
    cut_partners: dict[int, list[int]] = {i: [] for i in range(n)}
    cuts = []
    for i in range(n):
        for j in range(i + 1, n):
            if not _linked(members[i], members[j]):
                continue
            guard = incompatibility(items[i], items[j], config)
            if guard:
                cuts.append((items[i].id, items[j].id, guard))
                cut_partners[i].append(j)
                cut_partners[j].append(i)
            else:
                edges[i].add(j)
                edges[j].add(i)

    component = [-1] * n
    parts: list[list[int]] = []
    for start in range(n):
        if component[start] >= 0:
            continue
        stack, part = [start], []
        component[start] = len(parts)
        while stack:
            i = stack.pop()
            part.append(i)
            for j in edges[i]:
                if component[j] < 0:
                    component[j] = len(parts)
                    stack.append(j)
        parts.append(sorted(part))

    kept = [p for p in parts if len(p) >= min_size]
    group_of = {i: g for g, p in enumerate(kept) for i in p}
    result = Segmentation(groups=[[items[i].id for i in p] for p in kept], cuts=cuts)
    for p in parts:
        if len(p) >= min_size:
            continue
        for i in p:
            partners = [j for j in cut_partners[i] if j in group_of]
            if headline_kind(items[i].title) == ANALYSIS and partners:
                best = max(partners, key=lambda j: _cosine(items[i].vector, items[j].vector))
                result.commentary[items[i].id] = group_of[best]
            else:
                result.detached.append(items[i].id)
    return result


def segment_groups(session, groups: list[list[int]], config: DevelopmentSegmentationConfig,
                   min_size: int = 2) -> tuple[list[list[int]], dict[int, list[int]]]:
    """Segment narrative clusters of RawItem ids. Returns (groups, commentary), where
    commentary maps an index into the returned groups to the analysis item ids about it."""
    from osint_monitor.core.database import Entity, ItemEntity, RawItem
    from osint_monitor.processors.embeddings import blob_to_embedding, embed_texts
    from osint_monitor.processors.entity_resolver import normalise

    ids = sorted({i for g in groups for i in g})
    if not ids:
        return groups, {}
    rows = {r.id: r for r in session.query(RawItem).filter(RawItem.id.in_(ids))}
    locations: dict[int, set[str]] = {}
    for item_id, name in (session.query(ItemEntity.item_id, Entity.canonical_name)
                          .join(Entity, Entity.id == ItemEntity.entity_id)
                          .filter(ItemEntity.item_id.in_(ids), Entity.entity_type.in_(LOCATION_TYPES))):
        if key := normalise(name):
            locations.setdefault(item_id, set()).add(key)
    headline_vectors = dict(zip(ids, embed_texts([rows[i].title or "" for i in ids]))) \
        if config.min_headline_similarity is not None else {}

    out: list[list[int]] = []
    commentary: dict[int, list[int]] = {}
    for g in groups:
        items = [SegmentItem(id=i, source=rows[i].source_id, title=rows[i].title or "",
                             published_at=rows[i].published_at or rows[i].fetched_at,
                             vector=blob_to_embedding(rows[i].embedding), headline_vector=headline_vectors.get(i),
                             locations=locations.get(i, set())) for i in g]
        seg = segment(items, config, min_size)
        if len(seg.groups) != 1 or seg.commentary or seg.detached:
            logger.info(f"Development segmentation: cluster of {len(g)} -> {len(seg.groups)} developments, "
                        f"{len(seg.commentary)} commentary, {len(seg.detached)} detached "
                        f"({sorted({c[2] for c in seg.cuts})})")
        for item_id, local in seg.commentary.items():
            commentary.setdefault(len(out) + local, []).append(item_id)
        out.extend(seg.groups)
    return out, commentary


LOCATION_TYPES = ("GPE", "LOC", "FAC")
