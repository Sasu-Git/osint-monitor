"""Pydantic v2 data contracts for pipeline communication."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EntityType(str, Enum):
    PERSON = "PERSON"
    ORG = "ORG"
    GPE = "GPE"
    NORP = "NORP"
    FAC = "FAC"
    EVENT = "EVENT"
    PRODUCT = "PRODUCT"
    LOC = "LOC"
    WEAPON_SYSTEM = "WEAPON_SYSTEM"
    FACILITY = "FACILITY"


class AlertType(str, Enum):
    # Legacy (kept for backward compat with existing DB rows)
    KEYWORD = "keyword"
    ANOMALY = "anomaly"
    TREND = "trend"
    THRESHOLD = "threshold"
    COMPOUND = "compound"
    # New state-transition alert types
    IW_THRESHOLD = "iw_threshold"
    CORROBORATION_CHANGE = "corroboration_change"
    FUSION_CONVERGENCE = "fusion_convergence"
    ASSESSMENT_CONTRADICTION = "assessment_contradiction"
    NEW_EVENT_CLUSTER = "new_event_cluster"
    SOURCE_SILENCE_BREAK = "source_silence_break"
    ENTITY_EMERGENCE = "entity_emergence"
    COORDINATED_POSTING = "coordinated_posting"
    SIGNAL_GAP_OPENED = "signal_gap_opened"
    SIGNAL_GAP_CLOSED = "signal_gap_closed"
    SOURCE_FAILURE = "source_failure"
    INFRA_ANOMALY = "infra_anomaly"
    FIRST_REPORT = "first_report"


class BriefingType(str, Enum):
    DAILY = "daily"
    FLASH = "flash"
    WEEKLY = "weekly"
    DELTA = "delta"


class EntityRole(str, Enum):
    SUBJECT = "SUBJECT"
    OBJECT = "OBJECT"
    LOCATION = "LOCATION"


# ---------------------------------------------------------------------------
# Development taxonomy (see docs/domain-model.md)
#
# OTHER   = a clear development that fits no category.
# UNKNOWN = the evidence is insufficient to decide.
# ---------------------------------------------------------------------------

class EventType(str, Enum):
    # Diplomacy
    BILATERAL_MEETING = "bilateral_meeting"   # any direct exchange; mode in InteractionMode
    MULTILATERAL_MEETING = "multilateral_meeting"
    SUMMIT = "summit"
    NEGOTIATION = "negotiation"
    DIPLOMATIC_VISIT = "diplomatic_visit"
    AGREEMENT = "agreement"
    TREATY = "treaty"
    # Coercion / security
    SANCTIONS = "sanctions"
    MILITARY_ACTION = "military_action"
    DEPLOYMENT = "deployment"
    MILITARY_EXERCISE = "military_exercise"
    CEASEFIRE = "ceasefire"
    ARMS_TRANSFER = "arms_transfer"
    # Political / institutional
    ELECTION = "election"
    APPOINTMENT = "appointment"
    RESIGNATION = "resignation"
    POLICY_CHANGE = "policy_change"
    ECONOMIC_ACTION = "economic_action"
    # Rhetoric
    SIGNIFICANT_STATEMENT = "significant_statement"
    THREAT = "threat"
    WARNING = "warning"
    COMMENTARY = "commentary"
    # Fallbacks
    OTHER = "other"
    UNKNOWN = "unknown"


class EventDomain(str, Enum):
    DIPLOMACY = "diplomacy"
    MILITARY = "military"            # state armed forces
    SECURITY = "security"            # terrorism, cyber, policing, intelligence
    POLITICAL = "political"
    ECONOMIC = "economic"
    HUMANITARIAN = "humanitarian"
    INSTITUTIONAL = "institutional"  # international organisations, courts, treaty bodies
    UNKNOWN = "unknown"


class InteractionMode(str, Enum):
    PHYSICAL = "physical"
    TELEPHONE = "telephone"
    VIDEO = "video"
    WRITTEN = "written"
    NONE = "none"                    # no interaction (strike, sanctions, appointment)
    UNKNOWN = "unknown"


class Concreteness(str, Enum):
    ACTION = "action"                # something happened (strike, meeting held)
    DECISION = "decision"            # authoritative decision taken
    AGREEMENT = "agreement"          # mutual commitment reached
    NEGOTIATION = "negotiation"      # talks ongoing, no outcome
    DECLARATION = "declaration"      # formal statement, threat, announced plan
    COMMENTARY = "commentary"        # opinion / analysis
    UNKNOWN = "unknown"


class SignificanceClass(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    NOTABLE = "notable"
    BACKGROUND = "background"


class UncertaintyFlag(str, Enum):
    SINGLE_SOURCE = "single_source"
    CONTRADICTORY_REPORTS = "contradictory_reports"
    UNCONFIRMED_COMPLETION = "unconfirmed_completion"      # announced/planned, not reported as done
    INTERACTION_MODE_UNCLEAR = "interaction_mode_unclear"
    ACTORS_UNCLEAR = "actors_unclear"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    OUTPUT_REPAIRED = "output_repaired"                    # model output had invalid values, coerced
    CLASSIFIER_FALLBACK = "classifier_fallback"            # primary classifier failed, fallback used


class ConfidenceClass(str, Enum):
    CONFIRMED = "confirmed"      # >=3 independent sources incl. >=2 reliable, or primary official source + 1 independent
    PROBABLE = "probable"        # >=2 independent sources
    POSSIBLE = "possible"        # 1 reliable source
    DISPUTED = "disputed"        # sources contradict each other
    UNVERIFIED = "unverified"    # 1 low-reliability source or nothing usable


class DevelopmentStatus(str, Enum):
    """Lifecycle only -- confirmation lives in ConfidenceClass."""
    EMERGING = "emerging"
    DEVELOPING = "developing"
    CONCLUDED = "concluded"
    SUPERSEDED = "superseded"    # terminal


class RoleClass(str, Enum):
    """Office an actor holds. Seniority order comes from config/ranking.yaml, not from the enum."""
    HEAD_OF_STATE = "head_of_state"
    HEAD_OF_GOVERNMENT = "head_of_government"
    FOREIGN_MINISTER = "foreign_minister"
    DEFENSE_MINISTER = "defense_minister"
    FINANCE_MINISTER = "finance_minister"
    SENIOR_DIPLOMAT = "senior_diplomat"              # envoys, ambassadors to major posts, deputy FMs
    SENIOR_MILITARY = "senior_military"              # chiefs of staff, combatant commanders
    INTERNATIONAL_ORG_LEADER = "international_org_leader"
    SPOKESPERSON = "spokesperson"
    OTHER = "other"


class SourceRole(str, Enum):
    """What kind of publisher a source is (config/provenance.yaml)."""
    PRIMARY_OFFICIAL = "primary_official"          # government, military, IO, court: the actor itself
    WIRE = "wire"                                  # Reuters, AP, AFP ...
    INDEPENDENT_REPORTING = "independent_reporting"  # general news outlets with own reporting
    SPECIALIST_REPORTING = "specialist_reporting"  # trade / defense press
    ANALYSIS = "analysis"                          # think tanks, op-eds, analysis sites
    OSINT = "osint"                                # open-source investigators
    SOCIAL = "social"                              # individual social accounts, channels
    UNKNOWN = "unknown"


class EvidenceType(str, Enum):
    """How one item relates to the development it is evidence for."""
    PRIMARY = "primary"            # official record of the action itself (readout, OFAC notice)
    FIRSTHAND = "firsthand"        # reporter / investigator observed it directly
    INDEPENDENT = "independent"    # own reporting, origin not traced further
    DERIVATIVE = "derivative"      # repeats another origin's report (attribution or syndicated copy)
    COMMENTARY = "commentary"      # analysis / opinion about the development


class ItemStance(str, Enum):
    SUPPORTS = "supports"
    DENIES = "denies"
    RETRACTS = "retracts"          # correction / retraction of the outlet's own earlier report


class ProvenanceFlag(str, Enum):
    PRIMARY_SOURCE = "primary_source"
    SINGLE_ORIGIN = "single_origin"
    DERIVATIVE_COLLAPSED = "derivative_collapsed"          # several items traced back to one origin
    SYNDICATED_COPY = "syndicated_copy"                    # near-identical text across outlets
    COMMENTARY_ONLY = "commentary_only"
    PROVENANCE_UNKNOWN = "provenance_unknown"              # some items from sources with unknown role
    LOW_RELIABILITY_ONLY = "low_reliability_only"
    DENIED = "denied"
    CONFLICTING_OFFICIAL_STATEMENTS = "conflicting_official_statements"
    RETRACTED = "retracted"                                # an origin withdrew its report
    FULLY_RETRACTED = "fully_retracted"                    # every supporting origin withdrew


class SituationStatus(str, Enum):
    ACTIVE = "active"
    DORMANT = "dormant"          # no new developments for the configured period
    CLOSED = "closed"            # manually closed; never auto-joined or reopened


class SituationMatchReason(str, Enum):
    """Why a development was (or was not) put in a situation."""
    ACTOR_OVERLAP = "actor_overlap"
    SAME_REGION = "same_region"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    TOPIC_KEYWORDS = "topic_keywords"
    ARBITER_CHOICE = "arbiter_choice"          # ambiguous case settled by the LLM arbiter
    RECURRING_ACTORS = "recurring_actors"      # new situation: same actor set recurred
    AMBIGUOUS = "ambiguous"                    # left unassigned: candidates too close to call
    NO_MATCH = "no_match"


class RankReason(str, Enum):
    """Machine-readable reason a development moved up or down. Only reasons that
    actually changed the ranking are reported."""
    HIGH_SIGNIFICANCE = "high_significance"
    SENIOR_ACTOR = "senior_actor"
    PHYSICAL_INTERACTION = "physical_interaction"
    REMOTE_INTERACTION = "remote_interaction"
    CONCRETE_ACTION = "concrete_action"
    FORMAL_DECISION = "formal_decision"
    NEW_POLICY = "new_policy"
    AGREEMENT_REACHED = "agreement_reached"
    INDEPENDENTLY_CONFIRMED = "independently_confirmed"
    WIDELY_REPORTED = "widely_reported"
    NEW_DEVELOPMENT = "new_development"
    STATUS_CHANGE = "status_change"
    PRIORITY_GEOGRAPHY = "priority_geography"
    MULTINATIONAL = "multinational"
    GLOBAL_INSTITUTION = "global_institution"
    # demotions
    ROUTINE_COMMENTARY = "routine_commentary"
    RHETORIC_ONLY = "rhetoric_only"
    SINGLE_SOURCE = "single_source"
    UNCONFIRMED_REPORT = "unconfirmed_report"
    DISPUTED = "disputed"
    WEAK_EVIDENCE = "weak_evidence"
    DUPLICATE_COMMENTARY_PENALTY = "duplicate_commentary_penalty"
    REPEATED_COVERAGE_PENALTY = "repeated_coverage_penalty"
    OVERSHADOWED_BY_CONCRETE = "overshadowed_by_concrete"
    CONCLUDED = "concluded"
    SUPERSEDED = "superseded"
    STALE = "stale"


# ---------------------------------------------------------------------------
# Pipeline data contracts
# ---------------------------------------------------------------------------

class RawItemModel(BaseModel):
    """Item as collected from a source, before processing."""
    title: str
    content: str = ""
    url: str = ""
    published_at: Optional[datetime] = None
    source_name: str = ""
    source_type: str = "rss"
    external_id: Optional[str] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class ExtractedEntity(BaseModel):
    """Entity extracted from an item by NLP."""
    text: str
    entity_type: EntityType
    role: EntityRole = EntityRole.SUBJECT
    confidence: float = 1.0
    canonical_name: Optional[str] = None


class ProcessedItem(BaseModel):
    """Item after NLP + scoring + entity extraction."""
    raw_item: RawItemModel
    content_hash: str = ""
    entities: list[ExtractedEntity] = Field(default_factory=list)
    severity_score: float = 0.0
    keyword_score: float = 0.0
    entity_salience: float = 0.0
    novelty_score: float = 1.0
    region: Optional[str] = None
    is_duplicate: bool = False
    duplicate_of_id: Optional[int] = None
    embedding: Optional[list[float]] = None


class ClaimModel(BaseModel):
    """A factual claim extracted from a source item."""
    subject: str
    verb: str
    object: str = ""
    claim_text: str
    claim_type: str = "assertion"
    source_name: str = ""
    confidence: float = 1.0


class EventCluster(BaseModel):
    """A cluster of items representing a single real-world event."""
    summary: str
    event_type: Optional[str] = None
    severity: float = 0.0
    item_ids: list[int] = Field(default_factory=list)
    entity_names: list[str] = Field(default_factory=list)
    region: Optional[str] = None
    location_name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class ContextItem(BaseModel):
    """One source item inside a cluster, as shown to a classifier."""
    title: str
    excerpt: str = ""
    source_name: str = ""
    published_at: Optional[datetime] = None
    url: str = ""


class ContextEntity(BaseModel):
    name: str
    entity_type: str   # EntityType value; kept as str so unknown NER labels don't fail


class ClusterContext(BaseModel):
    """Normalized, read-only view of an event cluster handed to a classifier."""
    event_id: Optional[int] = None
    items: list[ContextItem] = Field(default_factory=list)
    entities: list[ContextEntity] = Field(default_factory=list)
    location_name: Optional[str] = None
    has_contradictions: bool = False

    @property
    def distinct_sources(self) -> set[str]:
        return {i.source_name for i in self.items if i.source_name}


class DevelopmentClassification(BaseModel):
    """Structured classification of a development. Describes what happened;
    ranking is a separate stage."""
    event_type: EventType = EventType.UNKNOWN
    event_domain: EventDomain = EventDomain.UNKNOWN
    interaction_mode: InteractionMode = InteractionMode.UNKNOWN
    concreteness: Concreteness = Concreteness.UNKNOWN
    significance_class: Optional[SignificanceClass] = None   # None = cannot judge
    actors: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    location: Optional[str] = None
    material_change: str = ""        # FACT: what changed
    why_it_matters: str = ""         # ASSESSMENT, grounded in the supplied context
    is_routine_commentary: bool = False
    classification_notes: str = ""
    uncertainty_flags: list[UncertaintyFlag] = Field(default_factory=list)
    classifier: str = ""             # "rules" | "llm:<provider>/<model>"

    @field_validator("actors", "countries", "organizations", mode="after")
    @classmethod
    def _dedupe_names(cls, values: list[str]) -> list[str]:
        seen: set[str] = set()
        out = []
        for v in values:
            v = v.strip()
            if v and v.lower() not in seen:
                seen.add(v.lower())
                out.append(v)
        return out

    @field_validator("uncertainty_flags", mode="after")
    @classmethod
    def _dedupe_flags(cls, values: list[UncertaintyFlag]) -> list[UncertaintyFlag]:
        return list(dict.fromkeys(values))

    @field_validator("location", mode="after")
    @classmethod
    def _blank_location_is_none(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() or None if value else None


class EvidenceItem(BaseModel):
    """One source item as seen by the provenance stage."""
    item_id: Optional[int] = None
    source_name: str
    source_category: Optional[str] = None     # sources.yaml category, if known
    collector_type: Optional[str] = None      # Source.type: rss, twitter, sanctions ...
    title: str = ""
    text: str = ""
    url: str = ""
    published_at: Optional[datetime] = None
    stance: ItemStance = ItemStance.SUPPORTS


class ItemProvenance(BaseModel):
    item_id: Optional[int] = None
    source_name: str
    source_role: SourceRole
    evidence_type: EvidenceType
    origin: str                               # who actually reported it; items sharing it count once
    stance: ItemStance
    derived_from: Optional[str] = None        # set when evidence_type is derivative
    note: str = ""                            # how provenance was decided, for the evidence view


class OriginSummary(BaseModel):
    origin: str
    role: SourceRole
    evidence_types: list[EvidenceType]
    sources: list[str]                        # outlets whose items trace back to this origin
    item_count: int
    stance: ItemStance                        # latest stance of this origin
    reliable: bool


class ConfidenceAssessment(BaseModel):
    """How well-established a development is. Independent of how significant it is."""
    confidence_class: ConfidenceClass
    independent_origins: int                  # origins that support it with non-commentary evidence
    reliable_origins: int
    origins: list[OriginSummary] = Field(default_factory=list)
    items: list[ItemProvenance] = Field(default_factory=list)
    flags: list[ProvenanceFlag] = Field(default_factory=list)


class DevelopmentSignature(BaseModel):
    """What the situation grouper needs to know about one development."""
    event_id: Optional[int] = None
    title: str
    actors: list[str] = Field(default_factory=list)      # countries / organisations, any spelling
    region: Optional[str] = None
    occurred_at: Optional[datetime] = None
    embedding: Optional[list[float]] = Field(default=None, repr=False)


class SituationProfile(BaseModel):
    """An existing situation as seen by the grouper."""
    situation_id: Optional[int] = None
    slug: str
    title: str
    short_description: str = ""
    status: SituationStatus = SituationStatus.ACTIVE
    region: Optional[str] = None
    primary_actors: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)     # from situations.yaml seeds only
    centroid: Optional[list[float]] = Field(default=None, repr=False)   # mean embedding of recent members


class SituationAssignment(BaseModel):
    """Grouper decision for one development. ``slug`` None = stays unassigned."""
    event_id: Optional[int] = None
    slug: Optional[str] = None
    created: bool = False                                 # this decision created the situation
    reasons: list[SituationMatchReason] = Field(default_factory=list)
    candidates: list[str] = Field(default_factory=list)   # slugs considered, best first


class DevelopmentBrief(BaseModel):
    event_id: int
    title: str
    occurred_at: Optional[datetime] = None
    corroboration_level: Optional[str] = None


class SituationOverview(BaseModel):
    """What the UI needs to answer: what is this story, what changed, what belongs to it."""
    situation: SituationProfile
    created_at: datetime
    updated_at: datetime                                  # time of the latest development
    development_count: int
    recent_developments: list[DevelopmentBrief] = Field(default_factory=list)   # newest first


class RankingInput(BaseModel):
    """Everything the ranker looks at for one development: the classification plus
    corroboration, lifecycle and history facts supplied by the caller."""
    development_id: Optional[int] = None
    classification: DevelopmentClassification
    confidence: ConfidenceClass = ConfidenceClass.UNVERIFIED
    independent_sources: int = 0
    actor_roles: list[RoleClass] = Field(default_factory=list)
    status: DevelopmentStatus = DevelopmentStatus.EMERGING
    previous_status: Optional[DevelopmentStatus] = None   # set when the status changed this run
    topic_key: Optional[str] = None      # situation slug / topic; groups repeats and overshadowing
    prior_similar_count: int = 0         # same topic + event type already seen before this batch
    occurred_at: Optional[datetime] = None
    region: Optional[str] = None


class RankedDevelopment(BaseModel):
    """Ranker output. ``score`` is an internal sort key only -- never show it in the UI."""
    position: int                        # 1 = top
    development_id: Optional[int] = None
    input_index: int                     # index into the list given to rank()
    score: float
    reasons: list[RankReason] = Field(default_factory=list)   # strongest effect first


class AlertModel(BaseModel):
    """Alert generated by the alerting engine."""
    alert_type: AlertType
    severity: float
    title: str
    detail: str = ""
    event_id: Optional[int] = None
    item_id: Optional[int] = None
    delivered_via: Optional[str] = None


class BriefingRequest(BaseModel):
    """Request to generate a briefing."""
    briefing_type: BriefingType = BriefingType.DAILY
    hours_back: int = 24
    model: Optional[str] = None


class BriefingResult(BaseModel):
    """Generated briefing."""
    briefing_type: BriefingType
    content_md: str
    model_used: str
    covering_from: datetime
    covering_to: datetime


class TrendPoint(BaseModel):
    """A single trend measurement."""
    entity_name: str
    metric_name: str
    metric_value: float
    window_start: datetime
    window_end: datetime
    is_anomaly: bool = False
    sigma: float = 0.0
