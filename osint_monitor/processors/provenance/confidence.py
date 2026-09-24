"""Confidence from independent origins.

Confidence says how well-established a development is, never how important it is:
a critical development can be unverified, a trivial one confirmed.

Rules (thresholds in config/provenance.yaml):
  disputed    a non-commentary origin supports it and another denies it
  confirmed   >= confirmed_origins independent origins, >= confirmed_reliable of them reliable;
              or a primary official source plus one other reliable, non-official origin
  probable    >= probable_origins independent origins, at least one reliable
  possible    one reliable origin, or several low-reliability ones
  unverified  one low-reliability origin, commentary only, fully retracted, or nothing
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Sequence

from osint_monitor.core.models import (
    ConfidenceAssessment, ConfidenceClass, EvidenceItem, EvidenceType, ItemProvenance,
    ItemStance, OriginSummary, ProvenanceFlag, SourceRole,
)
from osint_monitor.processors.provenance.resolve import ProvenanceResolver


def assess_confidence(items: Sequence[EvidenceItem],
                      resolver: ProvenanceResolver | None = None) -> ConfidenceAssessment:
    resolver = resolver or ProvenanceResolver()
    cfg = resolver.config
    provenance = resolver.resolve(items)

    grouped: dict[str, list[tuple[EvidenceItem, ItemProvenance]]] = defaultdict(list)
    for item, prov in zip(items, provenance):
        grouped[prov.origin].append((item, prov))

    origins = [_summarize(origin, members, resolver, cfg.reliable_roles) for origin, members in grouped.items()]
    origins.sort(key=lambda o: (not o.reliable, o.origin))

    def substantive(o: OriginSummary) -> bool:
        return any(t != EvidenceType.COMMENTARY for t in o.evidence_types)

    supporting = [o for o in origins if o.stance == ItemStance.SUPPORTS and substantive(o)]
    denying = [o for o in origins if o.stance == ItemStance.DENIES and substantive(o)]
    retracted = [o for o in origins if o.stance == ItemStance.RETRACTS]
    reliable = [o for o in supporting if o.reliable]
    primary = [o for o in supporting if EvidenceType.PRIMARY in o.evidence_types]

    flags: list[ProvenanceFlag] = []
    if primary:
        flags.append(ProvenanceFlag.PRIMARY_SOURCE)
    if len(supporting) == 1:
        flags.append(ProvenanceFlag.SINGLE_ORIGIN)
    if any(o.item_count > 1 and len(o.sources) > 1 for o in origins):
        flags.append(ProvenanceFlag.DERIVATIVE_COLLAPSED)
    if any(p.note.startswith("near-identical copy") for p in provenance):
        flags.append(ProvenanceFlag.SYNDICATED_COPY)
    if items and not supporting and not denying and not retracted:
        flags.append(ProvenanceFlag.COMMENTARY_ONLY)
    if any(p.source_role == SourceRole.UNKNOWN for p in provenance):
        flags.append(ProvenanceFlag.PROVENANCE_UNKNOWN)
    if supporting and not reliable:
        flags.append(ProvenanceFlag.LOW_RELIABILITY_ONLY)
    if denying:
        flags.append(ProvenanceFlag.DENIED)
        official = {EvidenceType.PRIMARY}
        if primary and any(official & set(o.evidence_types) for o in denying):
            flags.append(ProvenanceFlag.CONFLICTING_OFFICIAL_STATEMENTS)
    if retracted:
        flags.append(ProvenanceFlag.FULLY_RETRACTED if not supporting else ProvenanceFlag.RETRACTED)

    t = cfg.thresholds
    independent_reliable = [o for o in reliable if o.role != SourceRole.PRIMARY_OFFICIAL]
    if supporting and denying:
        level = ConfidenceClass.DISPUTED
    elif not supporting:
        level = ConfidenceClass.UNVERIFIED
    elif (len(supporting) >= t.confirmed_origins and len(reliable) >= t.confirmed_reliable) \
            or (primary and independent_reliable):
        level = ConfidenceClass.CONFIRMED
    elif len(supporting) >= t.probable_origins and reliable:
        level = ConfidenceClass.PROBABLE
    elif reliable or len(supporting) >= 2:
        level = ConfidenceClass.POSSIBLE
    else:
        level = ConfidenceClass.UNVERIFIED

    return ConfidenceAssessment(
        confidence_class=level,
        independent_origins=len(supporting),
        reliable_origins=len(reliable),
        origins=origins,
        items=provenance,
        flags=flags,
    )


def _summarize(origin: str, members: list[tuple[EvidenceItem, ItemProvenance]],
               resolver: ProvenanceResolver, reliable_roles: list[SourceRole]) -> OriginSummary:
    # the origin's role: configured origin role, else the role of its own (non-derivative) items
    own = [p for _, p in members if p.derived_from is None]
    role = resolver.origin_role(origin) or (own[0] if own else members[0][1]).source_role
    # latest stance wins, so a later retraction or denial overrides earlier support
    latest = max(members, key=lambda m: (m[0].published_at or datetime.min,
                                         m[1].stance != ItemStance.SUPPORTS))
    return OriginSummary(
        origin=origin,
        role=role,
        evidence_types=list(dict.fromkeys(p.evidence_type for _, p in members)),
        sources=list(dict.fromkeys(p.source_name for _, p in members)),
        item_count=len(members),
        stance=latest[1].stance,
        reliable=role in reliable_roles,
    )
