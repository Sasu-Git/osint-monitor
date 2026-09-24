# Domain Model — Development / Situation / Actor Roles

**Date:** 2026-09-24
**Scope:** Prompt 2 of the fork development chain. Design only; no code changed.
**Depends on:** [architecture-review.md](architecture-review.md)
**Baseline commit:** `168abd7`

---

## Amendments

**2026-09-24 — DevelopmentClassifier (Prompt 3), implemented in `osint_monitor/processors/classification/`:**

- `EventType`, `EventDomain`, `Concreteness` gain `UNKNOWN = "unknown"` (evidence insufficient). `OTHER` remains for clear developments outside the taxonomy. `SignificanceClass` has no unknown member; classifiers use `None` instead, so ranking values stay clean.
- New enum `UncertaintyFlag`: `single_source`, `contradictory_reports`, `unconfirmed_completion`, `interaction_mode_unclear`, `actors_unclear`, `insufficient_context`, `output_repaired`, `classifier_fallback`.
- `DevelopmentClassification` (in `core/models.py`) replaces the §4 draft. Fields: `event_type`, `event_domain`, `interaction_mode`, `concreteness`, `significance_class` (optional), `actors`, `countries`, `organizations`, `location`, `material_change`, `why_it_matters`, `is_routine_commentary`, `classification_notes`, `uncertainty_flags`, `classifier`. Actors are names; mapping them to `EventEntity.is_principal` happens when results are applied to the DB (domain-migration step).
- Classifier input is `ClusterContext` (items, entities, location, has_contradictions), built read-only by `classification/context.py`.
- Not yet done: the §2 schema migration and applying classifications to `events`.

**2026-09-24 — DevelopmentRanker (Prompt 4), implemented in `osint_monitor/processors/ranking/`:**

- `ConfidenceClass`, `DevelopmentStatus`, `RoleClass` from §1 now exist in `core/models.py`. `RoleClass` gains `spokesperson` (routine official comment, weight 0).
- New enum `RankReason`: machine-readable reasons (`senior_actor`, `physical_interaction`, `formal_decision`, `new_policy`, `independently_confirmed`, `duplicate_commentary_penalty`, …). Only reasons that actually moved a development are reported, strongest first.
- Contracts: `RankingInput` (classification + confidence, independent source count, actor roles, status / previous status, `topic_key`, `prior_similar_count`, `occurred_at`, region) → `RankedDevelopment` (position, reasons, internal `score` used only for sorting).
- `PolicyRanker` is deterministic: additive weights from `config/ranking.yaml` (validated by `RankingConfig`; every `EventType` must have a weight). Batch-level rules: repeats of the same type in a topic decay, rhetoric is demoted when its topic has a concrete development, first concrete development of its type in a topic gets a novelty bonus. Ties break on recency, then `development_id`.
- `PolicyRanker.explain(reasons)` returns a short label string from `reason_labels`; no numbers reach the UI.
- Not yet done: deriving `significance_class` / `significance_reasons` from the ranking and writing them to `events` (depends on the §2 migration).

**2026-09-24 — Source provenance and confidence (Prompt 5), implemented in `osint_monitor/processors/provenance/`:**

- `SourceRole` (`primary_official`, `wire`, `independent_reporting`, `specialist_reporting`, `analysis`, `osint`, `social`, `unknown`) replaces the §2.5 `source_role` draft values. Roles and origin groups live in `config/provenance.yaml` (per source name > sources.yaml category > collector type), not in new `sources` columns, so no migration is needed yet.
- `EvidenceType` (`primary`, `firsthand`, `independent`, `derivative`, `commentary`) replaces the §1 `EvidenceRole` draft; `ItemStance` (`supports`, `denies`, `retracts`); `ProvenanceFlag` for exposed uncertainty (`derivative_collapsed`, `syndicated_copy`, `provenance_unknown`, `conflicting_official_statements`, `retracted`, …).
- Corroboration counts **independent origins**: items attributing their report to a configured origin ("(Reuters)", "according to AP", "told Reuters", title suffix "- Reuters") or whose body text is a near-identical copy of an earlier item collapse into that origin; analysis never counts as confirmation. No citation-graph reconstruction.
- `assess_confidence` → `ConfidenceAssessment` (`confidence_class`, origin summaries, per-item provenance, flags). It carries no significance; high significance + low confidence stays representable.
- Retractions: story-level retraction phrasing by an origin makes its latest stance `retracts`; if no origin still supports, the assessment is `unverified` + `fully_retracted`. Denials come from items whose extracted claims are all denials.
- `compute_corroboration_score` now reports origins as `independent_sources`, plus additive keys `outlets`, `confidence_class`, `provenance_flags`. The cached `Event.source_count` / `corroboration_level` therefore stop counting syndicated copies.
- Not yet done: persisting `confidence_class` and per-item `evidence_role` (§2.1 / §2.4 migration); feeding `independent_origins` into `RankingInput` when the ranker is wired into the pipeline.

---

## 0. Decisions at a glance

| Question | Decision |
|---|---|
| New `developments` table or extend `events`? | **Extend `events`.** Keep table and class name `Event`; add alias `Development = Event`. No rename migration, no duplication. |
| Enum storage | Plain `String` columns validated by Python `(str, Enum)` classes. No SQL `ENUM` — SQLite has none, and taxonomy edits must not need a schema migration. |
| Where editorial defaults live | `config/development_types.yaml` (type → default domain / concreteness / interaction mode). Python enum = the list of valid values; YAML = policy. A test keeps them in sync. |
| Situation now or later? | **Now**, minimal table (5 columns). The whole UI hierarchy hangs off it; adding it later forces a second backfill of every development. Matching rules stay in YAML, not the DB. |
| Development ↔ Situation cardinality | **Many-to-one** (`events.situation_id`, nullable). One primary situation per development. Many-to-many deferred until a real case demands it. |
| Actor roles | Small `actor_roles` table (roles change over time → validity dates → multiple rows). Seeded only from `entities.yaml`. No automatic person database. |
| `phone_call` type | **Dropped.** Represented as `bilateral_meeting` + `interaction_mode=telephone`. Avoids two axes encoding the same fact. |
| `confirmed` in development_status | **Dropped from status.** Confirmation is `confidence_class`. Keeping both allows contradictory states (status *confirmed*, confidence *disputed*). Status is lifecycle only. |
| Legacy `severity` float | Kept, no longer displayed. Written from `significance_class` via a fixed lookup, only so existing sort-by-severity code keeps working until it is migrated. |

---

## 1. Enumerations

Location: `osint_monitor/core/models.py` (existing home of `EntityType`, `AlertType`, …). Style follows the existing `class X(str, Enum)` pattern — the project still declares Python ≥3.10, so no `StrEnum`.

```python
class EventType(str, Enum):
    """What kind of real-world development this is. Compact on purpose:
    add a value only when an existing one is clearly wrong for a recurring case."""
    # Diplomacy
    BILATERAL_MEETING = "bilateral_meeting"        # any direct senior exchange; mode in interaction_mode
    MULTILATERAL_MEETING = "multilateral_meeting"
    SUMMIT = "summit"                              # scheduled leaders-level gathering
    NEGOTIATION = "negotiation"                    # talks in progress, no outcome yet
    DIPLOMATIC_VISIT = "diplomatic_visit"          # travel to another country (may contain meetings)
    AGREEMENT = "agreement"                        # deal, MoU, joint declaration with commitments
    TREATY = "treaty"                              # formal legal instrument: signature, ratification, withdrawal
    # Coercion / security
    SANCTIONS = "sanctions"
    MILITARY_ACTION = "military_action"            # strikes, attacks, operations
    DEPLOYMENT = "deployment"                      # force movement / posture change
    MILITARY_EXERCISE = "military_exercise"
    CEASEFIRE = "ceasefire"
    ARMS_TRANSFER = "arms_transfer"
    # Political / institutional
    ELECTION = "election"
    APPOINTMENT = "appointment"
    RESIGNATION = "resignation"                    # includes dismissal / removal
    POLICY_CHANGE = "policy_change"
    ECONOMIC_ACTION = "economic_action"            # tariffs, export controls, aid packages, asset freezes
    # Rhetoric
    SIGNIFICANT_STATEMENT = "significant_statement"
    THREAT = "threat"                              # coercive: "we will do X if Y"
    WARNING = "warning"                            # advisory: "X is likely / dangerous"
    COMMENTARY = "commentary"                      # opinion or analysis, no new action
    # Fallbacks
    OTHER = "other"
    UNKNOWN = "unknown"                            # added in Prompt 3


class EventDomain(str, Enum):
    DIPLOMACY = "diplomacy"
    MILITARY = "military"            # state armed forces
    SECURITY = "security"            # non-military: terrorism, cyber, policing, intelligence
    POLITICAL = "political"          # domestic politics, elections, leadership
    ECONOMIC = "economic"
    HUMANITARIAN = "humanitarian"
    INSTITUTIONAL = "institutional"  # international organisations, courts, treaty bodies


class InteractionMode(str, Enum):
    PHYSICAL = "physical"
    TELEPHONE = "telephone"
    VIDEO = "video"
    WRITTEN = "written"      # letters, notes verbales, published statements addressed to a party
    NONE = "none"            # development has no interaction (strike, sanctions, appointment)
    UNKNOWN = "unknown"


class Concreteness(str, Enum):
    """How far from words toward deeds. Distinguishes announced vs executed within one type
    (e.g. sanctions *threatened* = declaration, sanctions *imposed* = decision)."""
    ACTION = "action"            # something physically/operationally happened (strike, meeting held)
    DECISION = "decision"        # authoritative decision taken (designation, appointment, policy adopted)
    AGREEMENT = "agreement"      # mutual commitment reached
    NEGOTIATION = "negotiation"  # talks ongoing, no outcome
    DECLARATION = "declaration"  # formal official statement, threat, warning
    COMMENTARY = "commentary"    # opinion / analysis


class SignificanceClass(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    NOTABLE = "notable"
    BACKGROUND = "background"


class ConfidenceClass(str, Enum):
    CONFIRMED = "confirmed"      # ≥3 independent sources incl. ≥2 reliable, or a primary official source + 1 independent
    PROBABLE = "probable"        # ≥2 independent sources
    POSSIBLE = "possible"        # 1 reliable source
    DISPUTED = "disputed"        # sources contradict each other
    UNVERIFIED = "unverified"    # 1 low-reliability source or nothing usable


class DevelopmentStatus(str, Enum):
    """Lifecycle only — confirmation lives in ConfidenceClass."""
    EMERGING = "emerging"        # new, few items, still forming
    DEVELOPING = "developing"    # receiving new reporting
    CONCLUDED = "concluded"      # no new reporting for the configured quiet period
    SUPERSEDED = "superseded"    # merged into / replaced by another development (terminal)


class RoleClass(str, Enum):
    HEAD_OF_STATE = "head_of_state"
    HEAD_OF_GOVERNMENT = "head_of_government"
    FOREIGN_MINISTER = "foreign_minister"
    DEFENSE_MINISTER = "defense_minister"
    FINANCE_MINISTER = "finance_minister"
    SENIOR_DIPLOMAT = "senior_diplomat"              # envoys, ambassadors to major posts, deputy FMs
    SENIOR_MILITARY = "senior_military"              # chiefs of staff, combatant commanders
    INTERNATIONAL_ORG_LEADER = "international_org_leader"
    OTHER = "other"


class EvidenceRole(str, Enum):
    """How a source item relates to its development (EventItem.evidence_role)."""
    PRIMARY = "primary"          # official source of the action itself (MFA readout, OFAC notice)
    INDEPENDENT = "independent"  # original reporting by an independent outlet
    DERIVATIVE = "derivative"    # syndicated / rewritten from another item
    COMMENTARY = "commentary"    # opinion or analysis about the development


class SituationStatus(str, Enum):
    ACTIVE = "active"
    DORMANT = "dormant"          # no developments in the configured period
    CLOSED = "closed"            # manually closed or removed from situations.yaml
```

Existing `EntityRole` (SUBJECT/OBJECT/LOCATION) is unchanged.

---

## 2. Database / schema changes

All additions are nullable or have defaults; no column is removed or renamed.

### 2.1 `events` (extended — the Development)

| Column | Type | Null | Default | Notes |
|---|---|---|---|---|
| `summary` | Text | no | — | **existing**; treated as the headline |
| `event_type` | String(100) | yes | — | **existing**, always NULL today; now holds `EventType` |
| `event_domain` | String(30) | yes | — | `EventDomain`; indexed |
| `interaction_mode` | String(20) | yes | — | `InteractionMode` |
| `concreteness` | String(20) | yes | — | `Concreteness` |
| `significance_class` | String(20) | yes | — | `SignificanceClass`; indexed |
| `significance_reasons` | JSON | yes | — | list of plain-language strings from the ranker |
| `confidence_class` | String(20) | yes | — | `ConfidenceClass` |
| `development_status` | String(20) | no | `'emerging'` | `DevelopmentStatus`; indexed |
| `superseded_by_id` | Integer FK → events.id | yes | — | required iff status = superseded |
| `occurred_at` | DateTime | yes | — | when it happened in the world (≠ when first reported) |
| `first_reported_at` | DateTime | no | — | **existing**; exposed as `first_seen` (synonym). Backfill fixes it to earliest item time |
| `last_updated_at` | DateTime | no | — | **existing**; exposed as `last_updated` (synonym) |
| `change_summary` | Text | yes | — | FACT: what changed, 1–2 sentences |
| `why_it_matters` | Text | yes | — | ASSESSMENT |
| `watch_for` | JSON | yes | — | WATCH: list of observable next events |
| `classification_source` | String(100) | yes | — | `rules` / `llm:<model>` / `manual` |
| `classification_reason` | Text | yes | — | one sentence explaining the classification |
| `narrative_source` | String(100) | yes | — | model that wrote change_summary / why_it_matters / watch_for |
| `narrative_updated_at` | DateTime | yes | — | regenerate when `last_updated_at` > this |
| `manual_override` | Boolean | no | `false` | pipeline must not overwrite classification fields when true |
| `situation_id` | Integer FK → situations.id | yes | — | indexed |

Legacy columns kept and still written: `severity`, `region`, `source_count`, `admiralty_rating`, `corroboration_level`, `has_contradictions`, `location_name`, `lat`, `lon`.

### 2.2 `situations` (new)

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | Integer PK | no | — |
| `slug` | String(100), unique | no | — |
| `name` | String(255) | no | — |
| `description` | Text | yes | — |
| `status` | String(20) | no | `'active'` |
| `created_at` | DateTime | no | now |

First/last activity and development counts are derived by query, not stored. Matching rules (entities, keywords) live in `config/situations.yaml`, keyed by `slug`.

### 2.3 `actor_roles` (new)

| Column | Type | Null | Notes |
|---|---|---|---|
| `id` | Integer PK | no | |
| `entity_id` | FK → entities.id | no | indexed; entity_type should be PERSON |
| `role_class` | String(40) | no | `RoleClass` |
| `title` | String(255) | no | e.g. "Minister of Foreign Affairs" |
| `country_code` | String(3) | yes | ISO 3166-1 alpha-3; NULL for international-org roles |
| `organization` | String(255) | yes | e.g. "United Nations", "NATO" |
| `valid_from` | Date | yes | |
| `valid_to` | Date | yes | NULL = current |

"Current role" = the row(s) with `valid_to IS NULL`; not stored separately. `Entity.wikidata_id` already exists and is reused.

### 2.4 Small changes to existing junction tables

| Table | Change |
|---|---|
| `event_items` | add `evidence_role` String(20) NULL; add **unique** `(event_id, item_id)` |
| `event_entities` | add `is_principal` Boolean NOT NULL DEFAULT false; add **unique** `(event_id, entity_id, role)` |

`is_principal` separates the actors *doing* the development (who met whom) from entities merely mentioned. Without it, any article mentioning a head of state would look senior.

### 2.5 `sources` (needed to compute `confidence_class` correctly)

| Column | Type | Null | Notes |
|---|---|---|---|
| `reliability` | String(1) | yes | Admiralty A–F, set explicitly in sources.yaml |
| `origin_group` | String(100) | yes | syndication group; items sharing it count as one source |
| `source_role` | String(20) | yes | official / wire / media / analysis / social / data |

### 2.6 `schema_meta` (new, migration bookkeeping)

| Column | Type |
|---|---|
| `key` | String(50) PK |
| `value` | String(100) |

Row `('schema_version', '<n>')`. A table rather than `PRAGMA user_version` so the same code works on PostgreSQL.

---

## 3. SQLAlchemy definitions

Additions to `osint_monitor/core/database.py`. Existing columns omitted except where referenced.

```python
from sqlalchemy import Date
from sqlalchemy.orm import synonym


class Situation(Base):
    __tablename__ = "situations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    developments: Mapped[list["Event"]] = relationship(back_populates="situation")


class Event(Base):
    __tablename__ = "events"
    # ... existing columns unchanged ...

    # Classification
    event_domain: Mapped[str | None] = mapped_column(String(30), index=True)
    interaction_mode: Mapped[str | None] = mapped_column(String(20))
    concreteness: Mapped[str | None] = mapped_column(String(20))
    classification_source: Mapped[str | None] = mapped_column(String(100))
    classification_reason: Mapped[str | None] = mapped_column(Text)
    manual_override: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Significance / confidence
    significance_class: Mapped[str | None] = mapped_column(String(20), index=True)
    significance_reasons: Mapped[list | None] = mapped_column(JSON)
    confidence_class: Mapped[str | None] = mapped_column(String(20))

    # Lifecycle
    development_status: Mapped[str] = mapped_column(
        String(20), default="emerging", nullable=False, index=True)
    superseded_by_id: Mapped[int | None] = mapped_column(ForeignKey("events.id"))
    occurred_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Narrative (FACT / ASSESSMENT / WATCH)
    change_summary: Mapped[str | None] = mapped_column(Text)
    why_it_matters: Mapped[str | None] = mapped_column(Text)
    watch_for: Mapped[list | None] = mapped_column(JSON)
    narrative_source: Mapped[str | None] = mapped_column(String(100))
    narrative_updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Situation
    situation_id: Mapped[int | None] = mapped_column(ForeignKey("situations.id"), index=True)
    situation: Mapped["Situation | None"] = relationship(back_populates="developments")

    # Product vocabulary without renaming columns
    first_seen = synonym("first_reported_at")
    last_updated = synonym("last_updated_at")


Development = Event  # product-facing name


class EventItem(Base):
    __tablename__ = "event_items"
    __table_args__ = (UniqueConstraint("event_id", "item_id", name="uq_event_item"),)
    # ... existing columns ...
    evidence_role: Mapped[str | None] = mapped_column(String(20))


class EventEntity(Base):
    __tablename__ = "event_entities"
    __table_args__ = (
        UniqueConstraint("event_id", "entity_id", "role", name="uq_event_entity_role"),
    )
    # ... existing columns ...
    is_principal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class ActorRole(Base):
    __tablename__ = "actor_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity_id: Mapped[int] = mapped_column(ForeignKey("entities.id"), nullable=False, index=True)
    role_class: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(3))
    organization: Mapped[str | None] = mapped_column(String(255))
    valid_from: Mapped[date | None] = mapped_column(Date)
    valid_to: Mapped[date | None] = mapped_column(Date)

    entity: Mapped["Entity"] = relationship(back_populates="roles")

# Entity gains:  roles: Mapped[list["ActorRole"]] = relationship(back_populates="entity")


class Source(Base):
    # ... existing columns ...
    reliability: Mapped[str | None] = mapped_column(String(1))
    origin_group: Mapped[str | None] = mapped_column(String(100))
    source_role: Mapped[str | None] = mapped_column(String(20))


class SchemaMeta(Base):
    __tablename__ = "schema_meta"
    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    value: Mapped[str] = mapped_column(String(100), nullable=False)
```

---

## 4. Pydantic contracts (stage interfaces)

Additions to `osint_monitor/core/models.py`. These are what the later `DevelopmentClassifier`, `DevelopmentRanker`, and narrative generator return; the DB is written only through the domain helpers in §5.

```python
class DevelopmentClassification(BaseModel):
    event_type: EventType
    event_domain: EventDomain
    concreteness: Concreteness
    interaction_mode: InteractionMode = InteractionMode.UNKNOWN
    principal_entity_ids: list[int] = Field(default_factory=list)
    reason: str                 # one sentence, shown in UI
    source: str                 # "rules" | "llm:<model>"


class SignificanceAssessment(BaseModel):
    significance_class: SignificanceClass
    reasons: list[str]          # e.g. ["In-person meeting of foreign ministers", "3 independent sources"]


class DevelopmentNarrative(BaseModel):
    change_summary: str         # FACT
    why_it_matters: str         # ASSESSMENT
    watch_for: list[str] = Field(default_factory=list)   # WATCH
    source: str                 # "llm:<model>" | "manual"


class ActorRoleSeed(BaseModel):
    role_class: RoleClass
    title: str
    country_code: Optional[str] = None
    organization: Optional[str] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None

# EntitySeedConfig (core/config.py) gains:  roles: list[ActorRoleSeed] = Field(default_factory=list)
```

The existing `EventCluster` model stays as the clustering output.

---

## 5. Domain helpers

New module `osint_monitor/core/development.py` — small pure functions, the only place domain rules live. No classes.

```python
ALLOWED_TRANSITIONS: dict[DevelopmentStatus, set[DevelopmentStatus]] = {
    DevelopmentStatus.EMERGING:   {DevelopmentStatus.DEVELOPING, DevelopmentStatus.CONCLUDED, DevelopmentStatus.SUPERSEDED},
    DevelopmentStatus.DEVELOPING: {DevelopmentStatus.CONCLUDED, DevelopmentStatus.SUPERSEDED},
    DevelopmentStatus.CONCLUDED:  {DevelopmentStatus.DEVELOPING, DevelopmentStatus.SUPERSEDED},  # reopen on new reporting
    DevelopmentStatus.SUPERSEDED: set(),                                                         # terminal
}

# Legacy compatibility only: keeps ORDER BY severity meaningful. Never displayed.
LEGACY_SEVERITY: dict[SignificanceClass, float] = {
    SignificanceClass.CRITICAL: 1.0, SignificanceClass.MAJOR: 0.75,
    SignificanceClass.NOTABLE: 0.5, SignificanceClass.BACKGROUND: 0.25,
}

_LEGACY_CORROBORATION = {
    "CONFIRMED": ConfidenceClass.CONFIRMED, "PROBABLE": ConfidenceClass.PROBABLE,
    "POSSIBLE": ConfidenceClass.POSSIBLE, "DOUBTFUL": ConfidenceClass.UNVERIFIED,
    "UNCONFIRMED": ConfidenceClass.UNVERIFIED, "UNVERIFIED": ConfidenceClass.UNVERIFIED,
}


def confidence_from_corroboration(level: str | None, has_contradictions: bool) -> ConfidenceClass:
    """Map legacy corroboration output to ConfidenceClass. Contradictions win."""
    if has_contradictions:
        return ConfidenceClass.DISPUTED
    return _LEGACY_CORROBORATION.get((level or "").upper(), ConfidenceClass.UNVERIFIED)


def transition(event: Event, new: DevelopmentStatus, superseded_by: Event | None = None) -> None:
    """Change lifecycle status; raises ValueError on an illegal transition."""


def apply_classification(event: Event, c: DevelopmentClassification) -> bool:
    """Write classification fields unless event.manual_override. Returns True if written.
    Also sets EventEntity.is_principal for c.principal_entity_ids."""


def apply_significance(event: Event, s: SignificanceAssessment) -> None:
    """Write significance_class + reasons, and legacy severity via LEGACY_SEVERITY."""


def active_role(roles: list[ActorRole], at: date) -> ActorRole | None:
    """Most senior role valid on `at` (valid_from <= at and (valid_to is None or at <= valid_to)).
    Seniority order comes from config/ranking.yaml, not from the enum."""
```

---

## 6. Configuration files introduced

### `config/development_types.yaml` — defaults per type (editorial policy)

```yaml
bilateral_meeting:     {domain: diplomacy,     concreteness: action,      interaction_mode: physical}
multilateral_meeting:  {domain: diplomacy,     concreteness: action,      interaction_mode: physical}
summit:                {domain: diplomacy,     concreteness: action,      interaction_mode: physical}
negotiation:           {domain: diplomacy,     concreteness: negotiation, interaction_mode: unknown}
diplomatic_visit:      {domain: diplomacy,     concreteness: action,      interaction_mode: physical}
agreement:             {domain: diplomacy,     concreteness: agreement,   interaction_mode: unknown}
treaty:                {domain: institutional, concreteness: agreement,   interaction_mode: written}
sanctions:             {domain: economic,      concreteness: decision,    interaction_mode: none}
military_action:       {domain: military,      concreteness: action,      interaction_mode: none}
deployment:            {domain: military,      concreteness: action,      interaction_mode: none}
military_exercise:     {domain: military,      concreteness: action,      interaction_mode: none}
ceasefire:             {domain: security,      concreteness: agreement,   interaction_mode: unknown}
arms_transfer:         {domain: military,      concreteness: decision,    interaction_mode: none}
election:              {domain: political,     concreteness: action,      interaction_mode: none}
appointment:           {domain: political,     concreteness: decision,    interaction_mode: none}
resignation:           {domain: political,     concreteness: decision,    interaction_mode: none}
policy_change:         {domain: political,     concreteness: decision,    interaction_mode: none}
economic_action:       {domain: economic,      concreteness: decision,    interaction_mode: none}
significant_statement: {domain: diplomacy,     concreteness: declaration, interaction_mode: written}
threat:                {domain: security,      concreteness: declaration, interaction_mode: written}
warning:               {domain: security,      concreteness: declaration, interaction_mode: written}
commentary:            {domain: political,     concreteness: commentary,  interaction_mode: none}
other:                 {domain: political,     concreteness: declaration, interaction_mode: unknown}
```

Defaults only — a classifier may override any of the three per development.

### `config/situations.yaml`

```yaml
situations:
  - slug: us-iran-nuclear
    name: "US–Iran nuclear negotiations"
    description: "Talks, pressure and incidents around Iran's nuclear programme."
    match:
      entities_all_of: [["United States", "Iran"]]
      keywords_any: ["nuclear", "enrichment", "IAEA", "JCPOA", "talks"]
  - slug: russia-ukraine
    name: "Russia–Ukraine war"
    match:
      entities_any: ["Russia", "Ukraine"]
  - slug: eu-china-trade
    name: "EU–China trade dispute"
    match:
      entities_all_of: [["European Union", "China"]]
      keywords_any: ["tariff", "anti-dumping", "export control", "EV", "trade"]
  - slug: sudan-civil-war
    name: "Sudan civil war"
    match:
      entities_any: ["Sudan", "Rapid Support Forces", "SAF"]
```

Sync rule: slugs in YAML are upserted; a slug removed from YAML is set to `closed`, never deleted.

### `config/entities.yaml` — optional `roles:` per person

```yaml
  - canonical_name: "Abbas Araghchi"
    entity_type: "PERSON"
    aliases: ["Araghchi"]
    wikidata_id: "Q…"           # look up before seeding
    roles:
      - role_class: foreign_minister
        title: "Minister of Foreign Affairs"
        country_code: IRN
        valid_from: 2024-08-21
```

Sync rule: for each seeded entity, `actor_roles` rows are replaced by the YAML list (YAML is the source of truth). Entities without `roles:` are untouched.

---

## 7. Example records

*Illustrative data — names/dates to be verified before use as seeds.*

**Situation**

```json
{"id": 1, "slug": "us-iran-nuclear", "name": "US–Iran nuclear negotiations",
 "description": "Talks, pressure and incidents around Iran's nuclear programme.",
 "status": "active", "created_at": "2026-09-24T08:00:00"}
```

**Development — in-person ministerial meeting**

```json
{"id": 4812, "summary": "Iranian FM and US envoy hold talks in Muscat",
 "event_type": "bilateral_meeting", "event_domain": "diplomacy",
 "interaction_mode": "physical", "concreteness": "action",
 "significance_class": "major",
 "significance_reasons": ["In-person meeting between a foreign minister and a senior envoy",
                          "Reported by 4 independent outlets", "Primary source: Omani MFA readout"],
 "confidence_class": "confirmed", "development_status": "developing",
 "occurred_at": "2026-09-23T10:00:00", "first_reported_at": "2026-09-23T11:42:00",
 "last_updated_at": "2026-09-24T06:15:00",
 "change_summary": "Iran's foreign minister and the US special envoy met in Muscat with Omani mediation, the first in-person round since June.",
 "why_it_matters": "Moves the channel from indirect message-passing to direct talks, lowering the chance of a near-term strike while negotiations run.",
 "watch_for": ["Date set for a follow-up round", "IAEA access announcement", "New US Treasury designations on Iranian oil"],
 "classification_source": "rules", "classification_reason": "Verb 'met' with two PERSON principals holding senior roles; location Muscat.",
 "narrative_source": "llm:gpt-5-mini", "manual_override": false, "situation_id": 1,
 "severity": 0.75, "corroboration_level": "CONFIRMED", "source_count": 4, "admiralty_rating": "A1"}
```

**Development — rhetoric on the same situation (ranks lower)**

```json
{"id": 4815, "summary": "Iranian parliament speaker says talks 'will fail without guarantees'",
 "event_type": "significant_statement", "event_domain": "diplomacy",
 "interaction_mode": "written", "concreteness": "declaration",
 "significance_class": "background",
 "significance_reasons": ["Statement only, no action", "Same topic as a major development in the last 24h"],
 "confidence_class": "probable", "development_status": "emerging", "situation_id": 1}
```

**Development — superseded after merge**

```json
{"id": 4790, "summary": "Reports of US–Iran contacts in Oman",
 "development_status": "superseded", "superseded_by_id": 4812, "situation_id": 1}
```

**Event entities for #4812**

```json
[{"event_id": 4812, "entity_id": 311, "role": "SUBJECT",  "is_principal": true},
 {"event_id": 4812, "entity_id": 902, "role": "SUBJECT",  "is_principal": true},
 {"event_id": 4812, "entity_id": 57,  "role": "LOCATION", "is_principal": false},
 {"event_id": 4812, "entity_id": 12,  "role": "SUBJECT",  "is_principal": false}]
```

**Actor role**

```json
{"id": 7, "entity_id": 311, "role_class": "foreign_minister",
 "title": "Minister of Foreign Affairs", "country_code": "IRN",
 "organization": null, "valid_from": "2024-08-21", "valid_to": null}
```

**Evidence**

```json
[{"event_id": 4812, "item_id": 99120, "evidence_role": "primary"},
 {"event_id": 4812, "item_id": 99131, "evidence_role": "independent"},
 {"event_id": 4812, "item_id": 99140, "evidence_role": "derivative"},
 {"event_id": 4812, "item_id": 99177, "evidence_role": "commentary"}]
```

---

## 8. Migration strategy

1. **Versioned migrations** in new `osint_monitor/core/migrations.py`: an ordered list `MIGRATIONS = [(1, m001_legacy), (2, m002_developments)]`. `init_db()` runs `create_all` and then any migration with version > `schema_meta.schema_version`, each in its own transaction, updating the version after success. Failures raise — no more swallowed exceptions.
2. **m001_legacy** absorbs the current ad-hoc block in `init_db` (`processed_at`, `trigger_key`, `superseded_by_id` on alerts). Each `ADD COLUMN` is guarded by an inspector check, so it is idempotent. The `UPDATE raw_items SET processed_at = fetched_at WHERE processed_at IS NULL` currently runs on **every startup**; inside m001 it runs once.
3. **m002_developments**
   - `create_all` has already created `situations`, `actor_roles`, `schema_meta` (new tables are created automatically).
   - `ALTER TABLE … ADD COLUMN` for every new column in §2.1, §2.4, §2.5 (guarded). NOT NULL columns use `DEFAULT` (`development_status DEFAULT 'emerging'`, `manual_override DEFAULT 0`, `is_principal DEFAULT 0`).
   - Deduplicate before unique indexes:
     `DELETE FROM event_items WHERE id NOT IN (SELECT MIN(id) FROM event_items GROUP BY event_id, item_id)`; same for `event_entities` on `(event_id, entity_id, role)`.
   - `CREATE UNIQUE INDEX` for both constraints (works on existing SQLite tables, unlike `ADD CONSTRAINT`).
   - Backfill:
     - `confidence_class` via `confidence_from_corroboration(corroboration_level, has_contradictions)`.
     - `occurred_at` and `first_reported_at` ← earliest `COALESCE(published_at, fetched_at)` of the event's items (today `first_reported_at` is the clustering run time).
     - `development_status` ← `concluded` if `last_updated_at` older than the quiet period (default 7 days, configurable), else `developing` if `source_count >= 2`, else `emerging`.
     - `event_type`, `significance_class`, narrative fields, `situation_id` stay NULL. They are filled by the classifier / ranker / grouper on the next pipeline run, or by a `rebuild-developments --days N` command (Prompt 3+).
4. **Fresh databases**: `create_all` builds the head schema; the version is set straight to the latest without running migrations.
5. **Safety**: before running any migration on an existing SQLite file, copy it to `data/backups/osint-pre-v{n}-{timestamp}.db`.
6. **PostgreSQL**: the same SQL works (`ADD COLUMN`, `CREATE UNIQUE INDEX`); `schema_meta` avoids SQLite-only pragmas.

---

## 9. Backward compatibility

- Table and class names unchanged; `Development` is an alias, `first_seen` / `last_updated` are synonyms.
- Every new column is nullable or defaulted, so existing code that builds `Event(...)` keeps working.
- Legacy fields keep being written during the transition:
  - `severity` from `LEGACY_SEVERITY[significance_class]` (unclassified events keep their old value);
  - `corroboration_level`, `admiralty_rating`, `source_count`, `has_contradictions` still produced by corroboration alongside `confidence_class`;
  - `region` still assigned.
- API responses change additively only: `/api/events` gains the new keys; no key is removed or renamed.
- The existing dashboard, CSV export, STIX, temporal, graph, and alert modules continue to read legacy fields unchanged.
- **Removal later** (separate step, after UI migration): stop writing `severity` and `corroboration_level`; drop them from API responses; drop the columns only once nothing reads them.

---

## 10. Fields intentionally NOT added

| Not added | Reason |
|---|---|
| Any probability / numeric confidence / score field | Contradicts evidence-over-scores; classes + reasons instead |
| Separate `developments` table | Would duplicate `events` and its junctions |
| `phone_call` event type | Encoded by `interaction_mode = telephone` |
| `confirmed` development status | Encoded by `confidence_class` |
| `occurred_at_precision` (day/hour) | Add only if date-only reports cause visible errors |
| Event subtype / tags | Taxonomy must stay hand-maintainable |
| Escalation direction (escalatory / de-escalatory) | Belongs in `why_it_matters` text until a concrete UI need exists |
| Situation hierarchy (parent situations) | No current need; flat list is enough |
| Development ↔ Situation many-to-many | Single primary situation first |
| Stored situation stats (first/last activity, counts) | Derived by query; SQLite handles it |
| `Situation.is_configured` / auto-situation fields | No automatic grouper yet |
| `Entity.country` | GPE entities are countries; person affiliation comes from `actor_roles.country_code` |
| `Entity.current_role` | Derived from `actor_roles` where `valid_to IS NULL` |
| Biography, party, birth date, photo, person relationships | Not a political-person database |
| Automatic Wikidata sync | Manual YAML seeding only; revisit if the actor list grows past a few hundred |
| Development version history / audit table | The report archive and `narrative_updated_at` suffice for a personal tool |
| Per-field provenance | `classification_source` + `narrative_source` are enough |
| Casualty counts, geometry, multilingual text fields | Unrelated to this step |
| User notes / bookmarks | UI feature, later prompt |

---

## 11. Tests required for the domain layer

Behavioural tests only; no tests of enum string values or Pydantic defaults.

**Taxonomy / config consistency** (`tests/test_taxonomy.py`)
- Every `EventType` has an entry in `development_types.yaml`, with no extra keys; every default domain / concreteness / interaction mode is a valid enum value.
- `situations.yaml` and `entities.yaml` roles validate against the Pydantic seed models (unknown `role_class` fails loudly).

**Domain helpers** (`tests/test_development.py`)
- `confidence_from_corroboration`: table test for every legacy level; contradictions always yield `disputed`; unknown / None yields `unverified`.
- `transition`: allowed transitions succeed; `superseded → *` raises; `superseded` without `superseded_by` raises; superseding an event with itself raises; `concluded → developing` (reopen) succeeds.
- `apply_classification`: writes all fields and sets `is_principal` on the listed entities; returns False and writes nothing when `manual_override` is true.
- `apply_significance`: sets class, reasons, and the matching legacy severity.
- `active_role`: picks the role valid on the date; respects open-ended `valid_to`; returns None outside any validity window; with overlapping roles returns the most senior per ranking config.

**Persistence** (`tests/test_domain_persistence.py`, in-memory SQLite from `conftest.session`)
- Duplicate `(event_id, item_id)` in `event_items` raises `IntegrityError`; same for `event_entities`.
- `Development` alias and `first_seen` / `last_updated` synonyms read and filter correctly.
- Situation sync: upserts by slug; removing a slug from YAML sets `closed`, keeps its developments.
- Actor-role sync: replaces the YAML-seeded roles of an entity; leaves other entities untouched.

**Migrations** (`tests/test_migrations.py`)
- Fresh DB → head version, all tables/columns present.
- Legacy DB fixture (schema as of `168abd7`, created from a raw SQL snapshot, with duplicate `event_items` rows and events carrying `corroboration_level` values) → migrates to head; row counts preserved except removed duplicates; `confidence_class`, `occurred_at`, `first_reported_at`, `development_status` backfilled as specified.
- Running `init_db()` twice is a no-op on the second run.
- A failing migration raises and leaves `schema_version` unchanged.

**Backward compatibility** (`tests/test_api_compat.py`)
- `GET /api/events` still returns every legacy key with the same types, plus the new keys.
