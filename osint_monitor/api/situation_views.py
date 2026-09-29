"""Read-only, web-facing Situation contract, built only from facts the pipeline already stores.

    Situation
    ├── title / status / region / principal actors / last changed
    ├── developments (timeline)
    │   ├── what happened, when
    │   ├── classification (type, domain, mode, concreteness)
    │   ├── significance (class, ranking reasons)
    │   └── confidence (class, independent origins)
    └── evidence per development
        └── sources, provenance (role, evidence type, origin), corroboration

No analytical interpretation: no "why it matters", assessment, watch items or
forecasts. Those layers can be added later as separate fields without changing this.
Nothing here writes to the database.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from osint_monitor.core.database import Event, EventEntity, EventItem, RawItem, Situation
from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.provenance import assess_event
from osint_monitor.processors.situations.canonical import ActorCanonicalizer


class SourceEvidence(BaseModel):
    item_id: int
    source: str
    title: str
    url: str = ""
    published_at: Optional[datetime] = None
    source_role: Optional[str] = None          # provenance: official, wire, outlet, analysis ...
    evidence_type: Optional[str] = None        # provenance: primary, report, derivative, commentary ...
    origin: Optional[str] = None               # who actually reported it; shared origins count once
    derived_from: Optional[str] = None
    provenance_note: str = ""
    excerpt: str = ""                          # opening of the stored item text, for reading


class OriginGroup(BaseModel):
    """Reports that trace back to one origin: it counts once, however many outlets carried it."""
    origin: str
    role: Optional[str] = None
    items: list[SourceEvidence] = Field(default_factory=list)


class EvidenceGroup(BaseModel):
    """Evidence of one kind (backend provenance only): official, independent, derivative,
    commentary, or not determined."""
    kind: str
    origins: list[OriginGroup] = Field(default_factory=list)

    @property
    def item_count(self) -> int:
        return sum(len(o.items) for o in self.origins)


class EvidenceCounts(BaseModel):
    items: int = 0                              # stored source items linked to the development
    outlets: int = 0
    independent_origins: Optional[int] = None   # from provenance; commentary never counts
    official_origins: int = 0
    derivative_items: int = 0
    commentary_items: int = 0
    undetermined_items: int = 0


class SummaryInfo(BaseModel):
    text: Optional[str] = None                  # persisted factual summary, never generated here
    method: Optional[str] = None                # "extractive-leads-v1", "llm", "insufficient-evidence"
    model: Optional[str] = None
    generated_at: Optional[datetime] = None
    item_ids: list[int] = Field(default_factory=list)


class Classification(BaseModel):
    event_type: Optional[str] = None
    event_domain: Optional[str] = None
    interaction_mode: Optional[str] = None
    concreteness: Optional[str] = None
    classified_by: Optional[str] = None
    uncertainty_flags: list[str] = Field(default_factory=list)


class Confidence(BaseModel):
    confidence_class: Optional[str] = None     # confirmed / probable / possible / unverified / disputed
    independent_origins: Optional[int] = None
    reliable_origins: Optional[int] = None
    source_count: int = 0
    flags: list[str] = Field(default_factory=list)


class DevelopmentView(BaseModel):
    id: int
    what_happened: str                         # headline of the most credible report
    change_summary: Optional[str] = None       # FACT: what changed, when the classifier stated it
    first_reported_at: Optional[datetime] = None
    last_updated_at: Optional[datetime] = None
    region: Optional[str] = None
    principal_actors: list[str] = Field(default_factory=list)
    classification: Classification
    significance_class: Optional[str] = None
    rank_reasons: list[str] = Field(default_factory=list)
    confidence: Confidence
    summary: SummaryInfo = Field(default_factory=SummaryInfo)
    evidence: list[SourceEvidence] = Field(default_factory=list)
    evidence_groups: list[EvidenceGroup] = Field(default_factory=list)   # the same items, grouped
    counts: EvidenceCounts = Field(default_factory=EvidenceCounts)


class SituationSummary(BaseModel):
    slug: str
    title: str
    status: str
    region: Optional[str] = None
    primary_actors: list[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    last_changed: Optional[datetime] = None    # newest development update, else the situation's own
    development_count: int = 0
    latest_development: Optional[str] = None


class SituationDetail(SituationSummary):
    description: str = ""
    developments: list[DevelopmentView] = Field(default_factory=list)   # timeline, newest first


# --- builders ---------------------------------------------------------------------------------

EXCERPT_CHARS = 280


def _excerpt(content: str | None) -> str:
    import html
    import re
    text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", content or "")).split())
    if len(text) <= EXCERPT_CHARS:
        return text
    cut = text[:EXCERPT_CHARS].rsplit(" ", 1)[0]
    return cut + " …"

def _canonicalizer() -> ActorCanonicalizer:
    return ActorCanonicalizer(normalizer=ActorNormalizer.load())


def list_situations(session: Session) -> list[SituationSummary]:
    """All situations, the ones that changed most recently first; seeds without developments last."""
    stats = {sid: (n, last) for sid, n, last in session.query(
        Event.situation_id, func.count(Event.id), func.max(Event.last_updated_at))
        .filter(Event.situation_id.isnot(None)).group_by(Event.situation_id)}
    out = []
    for s in session.query(Situation):
        n, last = stats.get(s.id, (0, None))
        latest = (session.query(Event.summary).filter(Event.situation_id == s.id)
                  .order_by(Event.last_updated_at.desc(), Event.id.desc()).limit(1).scalar()) if n else None
        out.append(SituationSummary(
            slug=s.slug, title=s.title, status=s.status, region=s.region,
            primary_actors=list(s.primary_actors or []), created_at=s.created_at,
            last_changed=last or s.updated_at, development_count=n, latest_development=latest))
    out.sort(key=lambda s: (s.development_count == 0, -(s.last_changed.timestamp() if s.last_changed else 0), s.slug))
    return out


GROUP_ORDER = ["official", "independent", "derivative", "commentary", "undetermined"]


def evidence_kind(e: SourceEvidence) -> str:
    """Which evidence group an item belongs to, from its stored provenance only."""
    if e.evidence_type is None:
        return "undetermined"                   # provenance did not assess this item
    if e.evidence_type == "commentary" or e.source_role == "analysis":
        return "commentary"
    if e.evidence_type == "derivative":
        return "derivative"
    if e.evidence_type == "primary" or e.source_role == "primary_official":
        return "official"
    return "independent"


def group_evidence(evidence: list[SourceEvidence]) -> list[EvidenceGroup]:
    groups: dict[str, dict[str, OriginGroup]] = {k: {} for k in GROUP_ORDER}
    for e in evidence:
        kind = evidence_kind(e)
        key = (e.derived_from if kind == "derivative" and e.derived_from else e.origin) or e.source
        group = groups[kind].setdefault(key, OriginGroup(origin=key, role=e.source_role))
        group.items.append(e)
    return [EvidenceGroup(kind=k, origins=list(groups[k].values())) for k in GROUP_ORDER if groups[k]]


def development_view(session: Session, event: Event, canon: ActorCanonicalizer,
                     with_evidence: bool = True) -> DevelopmentView:
    links = (session.query(EventEntity).options(joinedload(EventEntity.entity))
             .filter(EventEntity.event_id == event.id, EventEntity.is_principal.is_(True)))
    actors = sorted({canon.display(k) for k in canon.keys(ee.entity.canonical_name for ee in links if ee.entity)})
    confidence = Confidence(confidence_class=event.confidence_class, source_count=event.source_count or 0)
    evidence: list[SourceEvidence] = []
    if with_evidence:
        items = (session.query(RawItem).options(joinedload(RawItem.source))
                 .join(EventItem, EventItem.item_id == RawItem.id).filter(EventItem.event_id == event.id)
                 .order_by(RawItem.published_at.is_(None), RawItem.published_at).all())
        assessment = assess_event(session, event.id)
        prov = {p.item_id: p for p in assessment.items}
        confidence = Confidence(
            confidence_class=event.confidence_class or assessment.confidence_class.value,
            independent_origins=assessment.independent_origins, reliable_origins=assessment.reliable_origins,
            source_count=len({i.source_id for i in items}), flags=[f.value for f in assessment.flags])
        for i in items:
            p = prov.get(i.id)
            evidence.append(SourceEvidence(
                item_id=i.id, source=i.source.name if i.source else "?", title=i.title or "", url=i.url or "",
                published_at=i.published_at or i.fetched_at,
                source_role=p.source_role.value if p else None, evidence_type=p.evidence_type.value if p else None,
                origin=p.origin if p else None, derived_from=p.derived_from if p else None,
                provenance_note=p.note if p else "", excerpt=_excerpt(i.content)))
    groups = group_evidence(evidence) if with_evidence else []
    by_kind = {g.kind: g for g in groups}
    counts = EvidenceCounts(
        items=len(evidence), outlets=confidence.source_count,
        independent_origins=confidence.independent_origins,
        official_origins=len(by_kind["official"].origins) if "official" in by_kind else 0,
        derivative_items=by_kind["derivative"].item_count if "derivative" in by_kind else 0,
        commentary_items=by_kind["commentary"].item_count if "commentary" in by_kind else 0,
        undetermined_items=by_kind["undetermined"].item_count if "undetermined" in by_kind else 0)
    return DevelopmentView(
        id=event.id, what_happened=event.summary, change_summary=event.change_summary,
        summary=SummaryInfo(text=event.development_summary, method=event.summary_method, model=event.summary_model,
                            generated_at=event.summary_generated_at, item_ids=list(event.summary_item_ids or [])),
        evidence_groups=groups, counts=counts,
        first_reported_at=event.first_reported_at, last_updated_at=event.last_updated_at, region=event.region,
        principal_actors=actors,
        classification=Classification(
            event_type=event.event_type, event_domain=event.event_domain,
            interaction_mode=event.interaction_mode, concreteness=event.concreteness,
            classified_by=event.classification_source, uncertainty_flags=list(event.uncertainty_flags or [])),
        significance_class=event.significance_class, rank_reasons=list(event.rank_reasons or []),
        confidence=confidence, evidence=evidence)


def situation_detail(session: Session, slug: str) -> SituationDetail | None:
    s = session.query(Situation).filter_by(slug=slug).first()
    if s is None:
        return None
    canon = _canonicalizer()
    events = (session.query(Event).filter(Event.situation_id == s.id)
              .order_by(Event.first_reported_at.desc(), Event.id.desc()).all())
    developments = [development_view(session, e, canon) for e in events]
    last = max((d.last_updated_at for d in developments if d.last_updated_at), default=None)
    return SituationDetail(
        slug=s.slug, title=s.title, status=s.status, region=s.region,
        primary_actors=list(s.primary_actors or []), created_at=s.created_at,
        last_changed=last or s.updated_at, development_count=len(developments),
        latest_development=developments[0].what_happened if developments else None,
        description=s.short_description or "", developments=developments)
