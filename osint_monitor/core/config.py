"""Configuration loading and validation."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

from osint_monitor.core.models import (
    Concreteness, ConfidenceClass, DevelopmentStatus, EventDomain, EventType, InteractionMode,
    RankReason, RoleClass, SignificanceClass, SituationStatus, SourceRole, UncertaintyFlag,
)


BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
PROMPTS_DIR = CONFIG_DIR / "prompts"
DATA_DIR = BASE_DIR / "data"


class SourceConfig(BaseModel):
    name: str
    url: str
    type: str = "rss"
    category: str = "general"
    credibility_score: float = 0.5
    priority: int = 2
    poll_interval: int = 900
    enabled: bool = True


class TwitterAccountConfig(BaseModel):
    username: str
    focus: str = "general"
    credibility_score: float = 0.4


class RegionConfig(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    priority: int = 2


class AlertKeywordsConfig(BaseModel):
    critical: list[str] = Field(default_factory=list)
    high: list[str] = Field(default_factory=list)


class AlertRuleConfig(BaseModel):
    name: str
    type: str = "keyword"  # keyword, anomaly, trend, threshold, compound
    conditions: dict = Field(default_factory=dict)
    severity: float = 0.5
    cooldown_minutes: int = 240
    channels: list[str] = Field(default_factory=lambda: ["desktop"])


class AlertChannelConfig(BaseModel):
    type: str  # email, slack, discord, webhook, desktop
    enabled: bool = True
    config: dict = Field(default_factory=dict)


class AlertsConfig(BaseModel):
    rules: list[AlertRuleConfig] = Field(default_factory=list)
    channels: list[AlertChannelConfig] = Field(default_factory=list)
    quiet_hours: dict = Field(default_factory=dict)  # {"start": "22:00", "end": "07:00"}
    default_cooldown_minutes: int = 240


class EntitySeedConfig(BaseModel):
    canonical_name: str
    entity_type: str
    aliases: list[str] = Field(default_factory=list)
    wikidata_id: Optional[str] = None


class TierConfig(BaseModel):
    hot_interval_seconds: int = 150    # 2.5 min
    warm_interval_seconds: int = 600   # 10 min
    cold_interval_seconds: int = 3600  # 60 min
    # collector class name -> seconds one collect() may take before it stops and returns what it has
    collector_budgets: dict[str, float] = Field(default_factory=dict)


class SourcesFileConfig(BaseModel):
    rss_feeds: list[SourceConfig] = Field(default_factory=list)
    twitter_accounts: list[TwitterAccountConfig] = Field(default_factory=list)
    nitter_instances: list[str] = Field(default_factory=list)
    alert_keywords: AlertKeywordsConfig = Field(default_factory=AlertKeywordsConfig)
    regions: dict[str, RegionConfig] = Field(default_factory=dict)
    tiers: TierConfig = Field(default_factory=TierConfig)


class DevelopmentTypeDefaults(BaseModel):
    domain: EventDomain
    concreteness: Concreteness
    interaction_mode: InteractionMode


class CorroborationPolicy(BaseModel):
    per_extra_source: float = 0.0          # bonus per independent source beyond the first
    max_bonus: float = 0.0
    widely_reported_sources: int = 3       # from this many independent sources: 'widely reported'


class RedundancyPolicy(BaseModel):
    per_repeat: dict[Concreteness, float] = Field(default_factory=dict)
    default_per_repeat: float = 0.0
    max_penalty: float = 0.0


class GeographyPolicy(BaseModel):
    priority_countries: dict[str, float] = Field(default_factory=dict)   # name -> bonus, case-insensitive
    priority_regions: dict[str, float] = Field(default_factory=dict)
    countries_included: int = 2            # a bilateral development involves two countries at no bonus
    per_extra_country: float = 0.0
    max_multinational_bonus: float = 0.0
    global_organizations: list[str] = Field(default_factory=list)
    global_organization_bonus: float = 0.0


class RecencyPolicy(BaseModel):
    grace_hours: float = 12.0
    penalty_per_day: float = 0.0
    max_penalty: float = 0.0


class RankingConfig(BaseModel):
    """Editorial ranking policy (config/ranking.yaml). Unknown enum keys fail validation."""
    event_type_weights: dict[EventType, float]
    interaction_mode_weights: dict[InteractionMode, float] = Field(default_factory=dict)
    concreteness_weights: dict[Concreteness, float] = Field(default_factory=dict)
    significance_weights: dict[SignificanceClass, float] = Field(default_factory=dict)
    role_weights: dict[RoleClass, float] = Field(default_factory=dict)
    senior_role_threshold: float = 3.0
    known_roles: dict[str, RoleClass] = Field(default_factory=dict)   # person name -> office (until actor_roles exists)
    confidence_weights: dict[ConfidenceClass, float] = Field(default_factory=dict)
    corroboration: CorroborationPolicy = Field(default_factory=CorroborationPolicy)
    uncertainty_penalties: dict[UncertaintyFlag, float] = Field(default_factory=dict)
    routine_commentary_penalty: float = 0.0
    redundancy: RedundancyPolicy = Field(default_factory=RedundancyPolicy)
    overshadow_penalty: float = 0.0
    novelty_bonus: float = 0.0
    status_weights: dict[DevelopmentStatus, float] = Field(default_factory=dict)
    status_transition_weights: dict[str, float] = Field(default_factory=dict)   # "emerging->developing"
    geography: GeographyPolicy = Field(default_factory=GeographyPolicy)
    recency: RecencyPolicy = Field(default_factory=RecencyPolicy)
    reason_labels: dict[RankReason, str] = Field(default_factory=dict)

    @field_validator("event_type_weights")
    @classmethod
    def _all_event_types(cls, weights: dict[EventType, float]) -> dict[EventType, float]:
        missing = set(EventType) - set(weights)
        if missing:
            raise ValueError(f"event_type_weights missing: {sorted(m.value for m in missing)}")
        return weights

    @field_validator("status_transition_weights")
    @classmethod
    def _valid_transitions(cls, weights: dict[str, float]) -> dict[str, float]:
        for key in weights:
            parts = key.split("->")
            if len(parts) != 2:
                raise ValueError(f"status transition must look like 'old->new', got {key!r}")
            for p in parts:
                DevelopmentStatus(p.strip())
        return {"->".join(p.strip() for p in k.split("->")): v for k, v in weights.items()}


class SourceProfile(BaseModel):
    role: Optional[SourceRole] = None
    origin: Optional[str] = None              # origin group; defaults to the source name


class OriginProfile(BaseModel):
    role: SourceRole
    aliases: list[str] = Field(default_factory=list)   # names as they appear in attributions


class ConfidenceThresholds(BaseModel):
    confirmed_origins: int = 3                # independent origins for CONFIRMED ...
    confirmed_reliable: int = 2               # ... of which at least this many reliable
    probable_origins: int = 2


class ProvenanceConfig(BaseModel):
    """Source roles and derivative-reporting detection (config/provenance.yaml)."""
    sources: dict[str, SourceProfile] = Field(default_factory=dict)      # by source name, case-insensitive
    category_roles: dict[str, SourceRole] = Field(default_factory=dict)  # sources.yaml category -> role
    collector_roles: dict[str, SourceRole] = Field(default_factory=dict) # Source.type -> role
    origins: dict[str, OriginProfile] = Field(default_factory=dict)      # attributable origins (wires ...)
    attribution_patterns: list[str] = Field(default_factory=list)        # regex, "{alias}" placeholder
    firsthand_patterns: list[str] = Field(default_factory=list)
    retraction_patterns: list[str] = Field(default_factory=list)
    reliable_roles: list[SourceRole] = Field(default_factory=list)
    commentary_roles: list[SourceRole] = Field(default_factory=list)
    syndication_min_chars: int = 200          # compare this many leading characters of body text
    syndication_similarity: float = 0.95      # 0-1; at or above: treated as the same copy
    thresholds: ConfidenceThresholds = Field(default_factory=ConfidenceThresholds)

    @field_validator("attribution_patterns")
    @classmethod
    def _has_alias_placeholder(cls, patterns: list[str]) -> list[str]:
        for p in patterns:
            if "{alias}" not in p:
                raise ValueError(f"attribution pattern needs an {{alias}} placeholder: {p!r}")
        return patterns


class SituationSeed(BaseModel):
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: str
    short_description: str = ""
    region: Optional[str] = None
    primary_actors: list[str] = Field(min_length=1)
    keywords: list[str] = Field(default_factory=list)
    status: SituationStatus = SituationStatus.ACTIVE


class SituationPolicy(BaseModel):
    # evidence weights; signals that are unavailable for a pair are left out of the average
    actor_weight: float = 0.5
    region_weight: float = 0.1
    semantic_weight: float = 0.3
    keyword_weight: float = 0.2
    min_actor_coverage: float = 0.5      # share of the situation's actors the development must involve
    join_threshold: float = 0.6
    # stricter policy when a development has no principal actors and only mentioned entities are known
    fallback_min_actor_coverage: float = 1.0
    fallback_join_threshold: float = 0.8
    ambiguous_threshold: float = 0.4     # between this and join_threshold: ask the arbiter
    ambiguity_margin: float = 0.1        # two candidates this close are ambiguous too
    min_actors_to_create: int = 2        # single-actor storylines must be seeded
    create_min_developments: int = 2     # an actor set must recur before it becomes a situation
    create_window_days: int = 7
    dormant_after_days: int = 14
    centroid_developments: int = 20      # recent members averaged into the situation centroid


class ActorsConfig(BaseModel):
    """How entity mentions become canonical actors (config/actors.yaml)."""
    non_actors: list[str] = Field(default_factory=list)          # topics the NER mislabels as actors
    demonyms: dict[str, str] = Field(default_factory=dict)       # "Australian" -> country
    aliases: dict[str, str] = Field(default_factory=dict)        # variant -> canonical name
    represents: dict[str, str] = Field(default_factory=dict)     # person / body -> state it acts for


class StructuredSourcesConfig(BaseModel):
    source_types: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class SeismicFusionConfig(BaseModel):
    max_seconds_apart: float = 120
    max_km_apart: float = 100
    max_magnitude_difference: float = 0.5


class EventGroupingConfig(BaseModel):
    """Narrative vs structured item grouping (config/event_grouping.yaml)."""
    structured: StructuredSourcesConfig = Field(default_factory=StructuredSourcesConfig)
    narrative_sources: list[str] = Field(default_factory=list)
    strategies: dict[str, str] = Field(default_factory=dict)      # source name -> structured strategy
    seismic: SeismicFusionConfig = Field(default_factory=SeismicFusionConfig)


class SituationsConfig(BaseModel):
    """Situation seeds and grouping policy (config/situations.yaml)."""
    policy: SituationPolicy = Field(default_factory=SituationPolicy)
    # extend config/actors.yaml (kept for older situations.yaml files)
    actor_aliases: dict[str, str] = Field(default_factory=dict)   # variant -> canonical name
    actor_represents: dict[str, str] = Field(default_factory=dict)   # person / body -> state it acts for
    situations: list[SituationSeed] = Field(default_factory=list)

    @field_validator("situations")
    @classmethod
    def _unique_slugs(cls, seeds: list[SituationSeed]) -> list[SituationSeed]:
        slugs = [s.slug for s in seeds]
        dupes = {s for s in slugs if slugs.count(s) > 1}
        if dupes:
            raise ValueError(f"duplicate situation slugs: {sorted(dupes)}")
        return seeds


class AppSettings(BaseSettings):
    """App-level settings from environment variables."""
    db_url: str = f"sqlite:///{DATA_DIR / 'osint.db'}"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    default_llm_provider: str = "openai"
    # Development classifier: "rules" (deterministic, free), "llm", or "hybrid" (LLM only for ambiguous cases)
    classifier_backend: str = "rules"
    classifier_llm_provider: Optional[str] = None   # falls back to default_llm_provider
    classifier_llm_model: Optional[str] = None      # falls back to the provider's default
    # Situation grouping: ambiguous cases left unassigned ("none") or settled by the LLM ("llm")
    situation_arbiter: str = "none"
    spacy_model: str = "en_core_web_lg"
    embedding_model: str = "all-MiniLM-L6-v2"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = {"env_prefix": "OSINT_", "env_file": str(BASE_DIR / ".env"), "extra": "ignore"}


def load_sources_config(path: Path | None = None) -> SourcesFileConfig:
    """Load and validate sources.yaml."""
    path = path or CONFIG_DIR / "sources.yaml"
    with open(path) as f:
        raw = yaml.safe_load(f)
    return SourcesFileConfig(**raw)


def load_entities_config(path: Path | None = None) -> list[EntitySeedConfig]:
    """Load and validate entities.yaml."""
    path = path or CONFIG_DIR / "entities.yaml"
    if not path.exists():
        return []
    with open(path) as f:
        raw = yaml.safe_load(f)
    return [EntitySeedConfig(**e) for e in raw.get("entities", [])]


def load_alerts_config(path: Path | None = None) -> AlertsConfig:
    """Load and validate alerts.yaml."""
    path = path or CONFIG_DIR / "alerts.yaml"
    if not path.exists():
        return AlertsConfig()
    with open(path) as f:
        raw = yaml.safe_load(f)
    return AlertsConfig(**raw)


def load_development_types(path: Path | None = None) -> dict[EventType, DevelopmentTypeDefaults]:
    """Load and validate development_types.yaml."""
    path = path or CONFIG_DIR / "development_types.yaml"
    with open(path) as f:
        raw = yaml.safe_load(f) or {}
    return {EventType(k): DevelopmentTypeDefaults(**v) for k, v in raw.items()}


def load_ranking_config(path: Path | None = None) -> RankingConfig:
    """Load and validate ranking.yaml."""
    path = path or CONFIG_DIR / "ranking.yaml"
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return RankingConfig(**raw)


def load_provenance_config(path: Path | None = None) -> ProvenanceConfig:
    """Load and validate provenance.yaml."""
    path = path or CONFIG_DIR / "provenance.yaml"
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return ProvenanceConfig(**raw)


def load_situations_config(path: Path | None = None) -> SituationsConfig:
    """Load and validate situations.yaml."""
    path = path or CONFIG_DIR / "situations.yaml"
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return SituationsConfig(**raw)


def load_actors_config(path: Path | None = None) -> ActorsConfig:
    """Load and validate actors.yaml (empty config if the file is missing)."""
    path = path or CONFIG_DIR / "actors.yaml"
    if not path.exists():
        return ActorsConfig()
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return ActorsConfig(**raw)


def load_event_grouping_config(path: Path | None = None) -> EventGroupingConfig:
    """Load and validate event_grouping.yaml (everything narrative if the file is missing)."""
    path = path or CONFIG_DIR / "event_grouping.yaml"
    if not path.exists():
        return EventGroupingConfig()
    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return EventGroupingConfig(**raw)


def load_prompt(name: str) -> str:
    """Load a prompt template from config/prompts/<name>.md."""
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")


def get_settings() -> AppSettings:
    """Get application settings."""
    return AppSettings()
