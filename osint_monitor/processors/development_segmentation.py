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
  With ``location_match: containment`` places are compared through config/geography.yaml, so
  "Northern Cyprus" and "Cyprus" are compatible, while Kyiv and Odesa stay different places.

``headline_override`` (optional) keeps a link the headline guard would cut when both are report
headlines, published close together, naming compatible places (and, optionally, share actors):
outlets sometimes headline one occurrence very differently ("storm floods US Northeast" /
"nor'easter pummels New York and New Jersey").

A cluster becomes the connected components of its remaining links. Analysis items cut off
this way are not evidence of a Development; they are returned as commentary on the group they
discussed. Other cut-off singletons return to the unclustered pool.

Enabled in config/event_grouping.yaml (``development_segmentation.enabled``). The code default is
off, so without that file narrative clusters are used unsplit.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime

import numpy as np

from osint_monitor.core.config import DevelopmentSegmentationConfig
from osint_monitor.processors.geography import Gazetteer

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
    actors: set[str] = field(default_factory=set)       # canonical actor keys (headline override only)
    anchors: set[str] = field(default_factory=set)      # specific named entities (occurrence match only)
    cited: str | None = None                            # the origin the item attributes its report to, if any


@dataclass
class Segmentation:
    groups: list[list]                                   # item ids per Development
    commentary: dict = field(default_factory=dict)       # analysis item id -> index into groups
    detached: list = field(default_factory=list)         # other items cut off, back to the unclustered pool
    cuts: list[tuple] = field(default_factory=list)      # (item a, item b, guard) for every dropped link


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b)) / denom if denom else 0.0


_GAZETTEERS: dict[bool, Gazetteer] = {}


def gazetteer(use_regions: bool = False) -> Gazetteer:
    if use_regions not in _GAZETTEERS:
        _GAZETTEERS[use_regions] = Gazetteer.load(use_regions=use_regions)
    return _GAZETTEERS[use_regions]


def places_compatible(a: set[str], b: set[str], config: DevelopmentSegmentationConfig) -> bool:
    if config.location_match == "containment":
        return gazetteer(config.use_regions).compatible(a, b)
    return bool(a & b)


def _headline_mismatch_outweighed(a: SegmentItem, b: SegmentItem, config: DevelopmentSegmentationConfig) -> bool:
    o = config.headline_override
    if o is None:
        return False
    if headline_kind(a.title) != REPORT or headline_kind(b.title) != REPORT:
        return False                                    # live blogs and roundups mix developments
    if a.published_at is None or b.published_at is None             or abs((a.published_at - b.published_at).total_seconds()) > o.max_hours * 3600:
        return False
    if o.require_shared_place and not (a.locations and b.locations and places_compatible(a.locations, b.locations, config)):
        return False
    return len(a.actors & b.actors) >= o.min_shared_actors


def occurrence_evidence(a: SegmentItem, b: SegmentItem, config: DevelopmentSegmentationConfig) -> list[str] | None:
    """Owner rule P7: the explicit evidence that two report headlines describe one occurrence despite a headline
    mismatch, as a list of the conditions met, or None when the rule does not hold (``OccurrenceMatchConfig``)."""
    o = config.occurrence_match
    if o is None:
        return None
    if headline_kind(a.title) != REPORT or headline_kind(b.title) != REPORT:
        return None
    if a.published_at is None or b.published_at is None \
            or abs((a.published_at - b.published_at).total_seconds()) > o.max_hours * 3600:
        return None
    if a.locations and b.locations and not places_compatible(a.locations, b.locations, config):
        return None                                     # a place conflict is never outweighed
    evidence = [f"within {o.max_hours:g} h", "no place conflict"]
    shared = sorted(a.anchors & b.anchors)
    if len(shared) >= o.min_shared_anchors and shared:
        evidence.append(f"shared anchors {shared}")
    elif o.use_cited_source and a.cited and a.cited == b.cited:
        evidence.append(f"same cited source {a.cited}")
    else:
        return None
    return evidence


def incompatibility(a: SegmentItem, b: SegmentItem, config: DevelopmentSegmentationConfig) -> str | None:
    """The guard that rules out a and b being one Development, or None."""
    if config.analysis_headlines and {headline_kind(a.title), headline_kind(b.title)} == {ANALYSIS, REPORT}:
        return "analysis_headline"
    if (config.min_headline_similarity is not None and a.source != b.source
            and a.headline_vector is not None and b.headline_vector is not None
            and _cosine(a.headline_vector, b.headline_vector) < config.min_headline_similarity
            and not _headline_mismatch_outweighed(a, b, config)
            and not occurrence_evidence(a, b, config)):
        return "headline_similarity"
    if config.disjoint_locations and a.locations and b.locations and not places_compatible(a.locations, b.locations, config):
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


def segment_items(session, ids, config: DevelopmentSegmentationConfig) -> dict[int, SegmentItem]:
    """SegmentItems for RawItem ids (places, actors, embeddings, headline embeddings), as segmentation sees them.
    Items without an embedding are left out."""
    from osint_monitor.core.database import Entity, ItemEntity, RawItem
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.embeddings import blob_to_embedding, embed_texts
    from osint_monitor.processors.entity_resolver import normalise

    ids = sorted(set(ids))
    if not ids:
        return {}
    rows = {r.id: r for r in session.query(RawItem).filter(RawItem.id.in_(ids)) if r.embedding is not None}
    locations: dict[int, set[str]] = {}
    actors: dict[int, set[str]] = {}
    normalizer = ActorNormalizer.load() if config.headline_override and config.headline_override.min_shared_actors else None
    for item_id, name, etype in (session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                                 .join(Entity, Entity.id == ItemEntity.entity_id)
                                 .filter(ItemEntity.item_id.in_(list(rows)))):
        if etype in LOCATION_TYPES and (key := normalise(name)):
            locations.setdefault(item_id, set()).add(key)
        if normalizer and etype in ACTOR_TYPES and (key := normalizer.key(name)):
            actors.setdefault(item_id, set()).add(key)
    order = sorted(rows)
    headline_vectors = dict(zip(order, embed_texts([rows[i].title or "" for i in order]))) \
        if config.min_headline_similarity is not None and order else {}
    anchors, cited = (_occurrence_anchors(session, rows, config) if config.occurrence_match else ({}, {}))
    return {i: SegmentItem(id=i, source=rows[i].source_id, title=rows[i].title or "",
                           published_at=rows[i].published_at or rows[i].fetched_at,
                           vector=blob_to_embedding(rows[i].embedding), headline_vector=headline_vectors.get(i),
                           locations=locations.get(i, set()), actors=actors.get(i, set()),
                           anchors=anchors.get(i, set()), cited=cited.get(i)) for i in order}


ANCHOR_TYPES = ("PERSON", "ORG", "FAC", "PRODUCT", "EVENT", "WEAPON_SYSTEM", "FACILITY")
MIN_ANCHOR_CHARS = 4      # "AI", "UN", "EU": abbreviations this short name a topic or a body, not one occurrence


def _occurrence_anchors(session, rows: dict, config: DevelopmentSegmentationConfig) -> tuple[dict, dict]:
    """Per item: specific named entities (not a state, not someone or something standing for a state, not a media
    outlet, not a generic institution label), and the origin it attributes its report to."""
    from osint_monitor.core.database import Entity, ItemEntity
    from osint_monitor.core.models import EvidenceItem
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.entity_resolver import normalise
    from osint_monitor.processors.institutions import registry
    from osint_monitor.processors.provenance import ProvenanceResolver

    normalizer, geo, reg = ActorNormalizer.load(), gazetteer(False), registry()
    anchors: dict[int, set[str]] = {}
    for item_id, name, etype in (session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                                 .join(Entity, Entity.id == ItemEntity.entity_id)
                                 .filter(ItemEntity.item_id.in_(list(rows)))):
        if etype not in ANCHOR_TYPES or not name:
            continue
        key = normalizer.key(name)
        if (key and geo.is_country(key)) or geo.is_country(name) or normalizer.is_media(name) \
                or reg.is_generic(name):
            continue
        if (norm := normalise(name)) and len(norm.replace(" ", "")) >= MIN_ANCHOR_CHARS:
            anchors.setdefault(item_id, set()).add(norm)
    cited: dict[int, str] = {}
    if config.occurrence_match.use_cited_source:
        resolver = ProvenanceResolver()
        for i, r in rows.items():
            src = r.source.name if getattr(r, "source", None) else ""
            ev = EvidenceItem(item_id=i, source_name=src, title=r.title, text=(r.content or "")[:2000], url=r.url or "",
                              published_at=r.published_at or r.fetched_at)
            origin = resolver.attributed_origin(ev, resolver.source_origin(ev))
            if origin:
                cited[i] = origin
    return anchors, cited


def compatible_link(a: SegmentItem, b: SegmentItem, config: DevelopmentSegmentationConfig) -> bool:
    """True when a and b are linked by the clusterer's own link rule and no guard rules them out as one
    Development: the per-pair test segmentation applies inside a cluster."""
    from osint_monitor.processors.clustering import _ClusterMember, _linked
    ma = _ClusterMember(a.id, a.source, a.title, a.published_at, a.vector)
    mb = _ClusterMember(b.id, b.source, b.title, b.published_at, b.vector)
    return _linked(ma, mb) and incompatibility(a, b, config) is None


def segment_groups(session, groups: list[list[int]], config: DevelopmentSegmentationConfig,
                   min_size: int = 2) -> tuple[list[list[int]], dict[int, list[int]]]:
    """Segment narrative clusters of RawItem ids. Returns (groups, commentary), where
    commentary maps an index into the returned groups to the analysis item ids about it."""
    ids = sorted({i for g in groups for i in g})
    if not ids:
        return groups, {}
    by_id = segment_items(session, ids, config)

    out: list[list[int]] = []
    commentary: dict[int, list[int]] = {}
    for g in groups:
        items = [by_id[i] for i in g]
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
ACTOR_TYPES = ("PERSON", "ORG", "GPE", "NORP")
