"""Development identity (audit Phase 2, evaluations/identity/development-identity-contract.md).

How a batch of clusters becomes, continues, or stays below Developments. The clusterer and segmentation decide
which items *could* be one occurrence; this module decides, deterministically, what is persisted:

1. **Order.** Clusters are processed in a fixed order (earliest member publication time, then lowest item id), so
   the result never depends on the order HDBSCAN emitted them in.
2. **Existing memberships are kept.** An item already in a Development stays there. It is never added to a second
   one: one item, at most one Development.
3. **Continuation.** A cluster that shares items with existing Developments may extend them. Each new item joins
   the existing Development it *continues*: a member it is directly linked to under the clusterer's link rule,
   with no segmentation guard against the pair (``development_segmentation.compatible_link``). Being in the same
   cluster is not enough. Among several Developments it continues, the one with the most linked members wins
   (then the highest similarity, then the lowest id).
4. **New Developments.** New items that continue nothing may form a new Development. They must be connected by
   compatible links themselves (at least ``MIN_SIZE`` items), and must come from at least two independent origins
   (``independent_origins``). Otherwise they stay below the Development layer, as unclustered items, until
   independent evidence arrives (single-source policy). Structured record groups (sensor and record identity) are
   exempt: a record's identity is its grouping key, not a corroboration claim.
5. **Summary.** A Development's summary is the headline of its best *report* (not a live blog, roundup or
   analysis headline), preferring higher source credibility.

No Development is ever deleted, split or merged here, so its ID and existing membership are stable. Every
decision is returned with its reason for stats and diagnostics.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

MIN_SIZE = 2
MIN_INDEPENDENT_ORIGINS = 2


@dataclass
class Decision:
    cluster: dict
    event_id: int | None = None           # Development created or extended (None: nothing persisted)
    created: bool = False
    added: list[int] = field(default_factory=list)
    held: dict[int, str] = field(default_factory=dict)     # item id -> why it stayed below the Development layer
    reasons: list[str] = field(default_factory=list)
    # item id -> the evidence this decision used (supporting members, similarities, override, ...); filled only when
    # membership provenance is on (core/membership_log.py) and never read by any decision
    evidence: dict[int, dict] = field(default_factory=dict)
    origins: int | None = None                                 # independent origins counted for a new Development


def cluster_order_key(session: Session, cluster: dict):
    from osint_monitor.core.database import RawItem
    ids = cluster["item_ids"]
    times = [t for (t,) in session.query(RawItem.published_at).filter(RawItem.id.in_(ids)) if t is not None]
    return (min(times) if times else datetime.max, min(ids))


def is_report_headline(title: str) -> bool:
    from osint_monitor.processors.actor_roles import is_roundup
    from osint_monitor.processors.development_segmentation import REPORT, headline_kind
    return headline_kind(title or "") == REPORT and not is_roundup(title or "")


def summary_item(items):
    """The item whose headline names the Development: a report headline first, then source credibility, then the
    earliest item (lowest id) for a stable choice."""
    return max(items, key=lambda i: (is_report_headline(i.title), i.source.credibility_score if i.source else 0.0,
                                     -i.id))


def independent_origins(session: Session, item_ids) -> int:
    """Distinct provenance origins among the items that are evidence (not commentary): wire copy and attributed
    reports collapse into their origin, and analysis, live blogs and roundups do not count."""
    from osint_monitor.core.database import RawItem
    from osint_monitor.core.models import EvidenceItem, EvidenceType
    from osint_monitor.processors.provenance import ProvenanceResolver
    from osint_monitor.processors.provenance.context import TEXT_CHARS, _feed_categories
    from sqlalchemy.orm import joinedload

    rows = (session.query(RawItem).options(joinedload(RawItem.source))
            .filter(RawItem.id.in_(list(item_ids))).order_by(RawItem.id).all())
    categories = _feed_categories()
    evidence = [EvidenceItem(item_id=r.id, source_name=r.source.name if r.source else "",
                             source_category=(r.source.category if r.source else None)
                             or categories.get(r.source.name if r.source else ""),
                             collector_type=r.source.type if r.source else None, title=r.title,
                             text=(r.content or "")[:TEXT_CHARS], url=r.url or "",
                             published_at=r.published_at or r.fetched_at) for r in rows]
    resolved = ProvenanceResolver().resolve(evidence)
    return len({p.origin for p in resolved if p.evidence_type != EvidenceType.COMMENTARY})


def _components(ids: list[int], linked) -> list[list[int]]:
    seen, parts = set(), []
    for start in ids:
        if start in seen:
            continue
        stack, part = [start], []
        seen.add(start)
        while stack:
            i = stack.pop()
            part.append(i)
            for j in ids:
                if j not in seen and linked(i, j):
                    seen.add(j)
                    stack.append(j)
        parts.append(sorted(part))
    return parts


def reconcile(session: Session, cluster: dict, config, evidence: bool = False) -> list[Decision]:
    """Decide what one cluster does to the persisted Developments (no writes). Returns one Decision per
    Development it extends or creates, plus one (event_id None) for the items it leaves below the layer.
    With ``evidence``, each Decision also carries the evidence it used (provenance only; decisions are identical)."""
    from osint_monitor.core.database import EventItem
    from osint_monitor.processors.development_segmentation import _cosine, compatible_link, segment_items
    from osint_monitor.processors.event_grouping import STRUCTURED

    ids = sorted(set(cluster["item_ids"]))
    member_of = {ei.item_id: ei.event_id for ei in session.query(EventItem).filter(EventItem.item_id.in_(ids))}
    new_ids = [i for i in ids if i not in member_of]
    if not new_ids:
        return []
    touched = sorted(set(member_of.values()))

    if cluster.get("kind") == STRUCTURED:                       # record identity decides, not similarity
        d = Decision(cluster=cluster, event_id=touched[0] if touched else None, created=not touched, added=new_ids)
        d.reasons.append("structured record group" + (f" extends D{touched[0]}" if touched else ""))
        return [d]

    # all existing members of the touched Developments, not only those in this cluster
    members = {e: sorted(i for (i,) in session.query(EventItem.item_id).filter(EventItem.event_id == e))
               for e in touched}
    seg = segment_items(session, set(new_ids) | {m for ms in members.values() for m in ms}, config)
    cache: dict[tuple[int, int], bool] = {}

    def linked(a: int, b: int) -> bool:
        key = (a, b) if a < b else (b, a)
        if key not in cache:
            cache[key] = a in seg and b in seg and compatible_link(seg[a], seg[b], config)
        return cache[key]

    decisions: list[Decision] = []
    extend: dict[int, list[int]] = {}
    rest: list[int] = []
    candidates: dict[int, dict[int, list[int]]] = {}         # item -> Development -> linked members (provenance)
    for n in new_ids:
        best = None
        for e in touched:
            links = [m for m in members[e] if linked(n, m)]
            candidates.setdefault(n, {})[e] = links
            if links:
                score = (len(links), max(_cosine(seg[n].vector, seg[m].vector) for m in links), -e)
                if best is None or score > best[0]:
                    best = (score, e)
        if best:
            extend.setdefault(best[1], []).append(n)
        else:
            rest.append(n)
    for e in sorted(extend):
        d = Decision(cluster=cluster, event_id=e, added=sorted(extend[e]))
        d.reasons.append(f"continues D{e}: {len(d.added)} new item(s) linked to its members")
        decisions.append(d)

    held = Decision(cluster=cluster)
    for part in _components(sorted(rest), linked):
        if len(part) < MIN_SIZE:
            for n in part:
                held.held[n] = ("linked to no member of an overlapping Development" if touched
                                else "not linked compatibly to another new item")
            continue
        origins = independent_origins(session, part)
        if origins < MIN_INDEPENDENT_ORIGINS:
            for n in part:
                held.held[n] = f"single-source: {origins} independent origin(s)"
            continue
        d = Decision(cluster=cluster, created=True, added=part, origins=origins)
        d.reasons.append(f"new Development: {len(part)} items, {origins} independent origins")
        decisions.append(d)
    if held.held:
        held.reasons.append("below the Development layer")
        decisions.append(held)
    if evidence:
        try:
            _attach_evidence(decisions, seg, candidates, linked, config)
        except Exception as e:                                   # provenance never affects identity
            logger.debug(f"membership evidence skipped: {e}")
    return decisions


def _attach_evidence(decisions: list[Decision], seg: dict, candidates: dict, linked, config) -> None:
    """Describe, per item, the links each decision already relied on. Pure: reads the same cached links and
    segmentation items; computes no new link and changes no decision."""
    from osint_monitor.processors.development_segmentation import (
        _cosine, _headline_mismatch_outweighed, occurrence_evidence, places_compatible)

    def describe(n: int, partners: list[int]) -> dict:
        ranked = sorted(partners, key=lambda m: -_cosine(seg[n].vector, seg[m].vector)) if n in seg else []
        out = {"supporting_member_ids": ranked[:5], "n_links": len(partners), "best_cosine": None,
               "best_headline_cosine": None, "override": None, "places_compatible": None,
               "segmentation": "no guard on the supporting link" if ranked else None,
               "actors_compatible": None}                     # actors are not part of the current link rule
        if not ranked:
            return out
        a, b = seg[n], seg[ranked[0]]
        out["best_cosine"] = round(_cosine(a.vector, b.vector), 4)
        if a.headline_vector is not None and b.headline_vector is not None:
            h = _cosine(a.headline_vector, b.headline_vector)
            out["best_headline_cosine"] = round(h, 4)
            if (config.min_headline_similarity is not None and a.source != b.source
                    and h < config.min_headline_similarity):
                out["override"] = ("headline_6h" if _headline_mismatch_outweighed(a, b, config)
                                   else "p7" if occurrence_evidence(a, b, config) else None)
        if a.locations and b.locations:
            out["places_compatible"] = places_compatible(a.locations, b.locations, config)
        return out

    for d in decisions:
        if d.event_id is not None and not d.created:             # continuation of an existing Development
            for n in d.added:
                cands = candidates.get(n, {})
                d.evidence[n] = {**describe(n, cands.get(d.event_id, [])),
                                 "competing_event_ids": sorted(e for e, ls in cands.items() if ls and e != d.event_id)}
        elif d.created:                                          # a new Development: links among its own items
            for n in d.added:
                d.evidence[n] = {**describe(n, [m for m in d.added if m != n and linked(n, m)]),
                                 "independent_origins": d.origins, "competing_event_ids": []}
        for n in d.held:
            cands = candidates.get(n, {})
            d.evidence[n] = {**describe(n, []), "competing_event_ids": sorted(e for e, ls in cands.items() if ls)}
