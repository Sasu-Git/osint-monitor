"""Situation grouping: developments -> continuing storylines.

SituationGrouper is deterministic (actor overlap, region, semantic similarity,
topic keywords). Ambiguous cases can be settled by an arbiter -- the LLM arbiter
may only choose among existing candidates. New situations are keyed by canonical
actor sets, so near-duplicate names cannot appear.

Select the arbiter with OSINT_SITUATION_ARBITER ("none" default, or "llm").
"""

from __future__ import annotations

from osint_monitor.core.config import get_settings, load_situations_config
from osint_monitor.processors.situations.arbiter import LLMSituationArbiter
from osint_monitor.processors.situations.canonical import ActorCanonicalizer
from osint_monitor.processors.situations.grouper import SituationArbiter, SituationGrouper
from osint_monitor.processors.situations.store import (
    assign_situations, load_profiles, refresh_statuses, situation_overview, sync_seeds,
)

__all__ = [
    "ActorCanonicalizer", "LLMSituationArbiter", "SituationArbiter", "SituationGrouper",
    "assign_situations", "get_grouper", "load_profiles", "refresh_statuses", "situation_overview", "sync_seeds",
]


def get_grouper(arbiter: str | None = None) -> SituationGrouper:
    settings = get_settings()
    arbiter = arbiter or settings.situation_arbiter
    if arbiter == "none":
        return SituationGrouper(load_situations_config())
    if arbiter == "llm":
        return SituationGrouper(load_situations_config(), LLMSituationArbiter(
            provider=settings.classifier_llm_provider, model=settings.classifier_llm_model))
    raise ValueError(f"Unknown situation arbiter: {arbiter!r}. Options: 'none', 'llm'")
