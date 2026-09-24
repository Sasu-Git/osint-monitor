"""Deterministic, config-driven DevelopmentRanker.

Each development gets an internal sort key: its event type weight plus
additive adjustments from config/ranking.yaml. Every adjustment that moves a
development is recorded as a RankReason, so the UI can say *why* something is
on top without showing arithmetic.

Some adjustments depend on the rest of the batch:
  - redundancy: the n-th development of the same event type in a topic is
    penalised n times (plus ``prior_similar_count`` from earlier batches);
  - overshadowing: statements and commentary are demoted when their topic also
    has a concrete development (action, decision, agreement) in the batch;
  - novelty: the first concrete development of its type in a topic gets a bonus.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Sequence

from osint_monitor.core.config import RankingConfig, load_ranking_config
from osint_monitor.core.models import (
    Concreteness, ConfidenceClass, DevelopmentStatus, EventType, InteractionMode,
    RankedDevelopment, RankingInput, RankReason, SignificanceClass, UncertaintyFlag,
)

CONCRETE = {Concreteness.ACTION, Concreteness.DECISION, Concreteness.AGREEMENT}
RHETORIC = {Concreteness.DECLARATION, Concreteness.COMMENTARY}
REMOTE = {InteractionMode.TELEPHONE, InteractionMode.VIDEO}
HIGH_SIGNIFICANCE = {SignificanceClass.CRITICAL, SignificanceClass.MAJOR}

_CONCRETENESS_REASON = {
    Concreteness.ACTION: RankReason.CONCRETE_ACTION,
    Concreteness.DECISION: RankReason.FORMAL_DECISION,
    Concreteness.AGREEMENT: RankReason.AGREEMENT_REACHED,
    Concreteness.DECLARATION: RankReason.RHETORIC_ONLY,
    Concreteness.COMMENTARY: RankReason.RHETORIC_ONLY,
}
_FLAG_REASON = {
    UncertaintyFlag.SINGLE_SOURCE: RankReason.SINGLE_SOURCE,
    UncertaintyFlag.UNCONFIRMED_COMPLETION: RankReason.UNCONFIRMED_REPORT,
    UncertaintyFlag.CONTRADICTORY_REPORTS: RankReason.DISPUTED,
}
_STATUS_REASON = {
    DevelopmentStatus.SUPERSEDED: RankReason.SUPERSEDED,
    DevelopmentStatus.CONCLUDED: RankReason.CONCLUDED,
}


def _utc_naive(dt: datetime) -> datetime:
    """The codebase stores naive UTC; accept aware datetimes too."""
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt


class _Adjustments:
    """Collects score changes; reasoned ones are reported, the rest only move the key."""

    def __init__(self, base: float):
        self.base = base
        self.by_reason: dict[RankReason, float] = defaultdict(float)

    def add(self, value: float, reason: RankReason | None = None) -> None:
        if not value:
            return
        if reason is None:
            self.base += value
        else:
            self.by_reason[reason] += value

    @property
    def total(self) -> float:
        return self.base + sum(self.by_reason.values())

    def reasons(self) -> list[RankReason]:
        effective = [(r, v) for r, v in self.by_reason.items() if abs(v) > 1e-9]
        return [r for r, _ in sorted(effective, key=lambda rv: -abs(rv[1]))]


class PolicyRanker:
    """Ranks developments with the weights in config/ranking.yaml."""

    name = "policy"

    def __init__(self, config: RankingConfig | None = None):
        self.config = config or load_ranking_config()

    # -- public ------------------------------------------------------------------

    def rank(self, developments: Sequence[RankingInput],
             now: datetime | None = None) -> list[RankedDevelopment]:
        now = _utc_naive(now) if now else datetime.utcnow()
        repeats = self._repeat_counts(developments)
        concrete_by_topic = self._concrete_by_topic(developments)

        scored = []
        for idx, dev in enumerate(developments):
            adj = self._score(dev, idx, repeats[idx], concrete_by_topic, now)
            scored.append((idx, dev, round(adj.total, 6), adj.reasons()))

        def sort_key(entry):
            idx, dev, score, _ = entry
            when = _utc_naive(dev.occurred_at) if dev.occurred_at else None
            # ties: newer first, undated last, then id, then input order
            return (-score, when is None, -(when - datetime.min).total_seconds() if when else 0,
                    dev.development_id is None, dev.development_id or 0, idx)

        scored.sort(key=sort_key)
        return [
            RankedDevelopment(position=pos, development_id=dev.development_id, input_index=idx,
                              score=score, reasons=reasons)
            for pos, (idx, dev, score, reasons) in enumerate(scored, start=1)
        ]

    def explain(self, reasons: Sequence[RankReason], limit: int = 2) -> str:
        """Short UI explanation from the strongest reasons. Never contains numbers."""
        labels = self.config.reason_labels
        return "; ".join(labels.get(r, r.value.replace("_", " ").capitalize()) for r in reasons[:limit])

    # -- batch context -------------------------------------------------------------

    @staticmethod
    def _repeat_counts(developments: Sequence[RankingInput]) -> list[int]:
        """Per development: earlier developments of the same type in the same topic."""
        order = sorted(
            range(len(developments)),
            key=lambda i: (developments[i].occurred_at is None,
                           _utc_naive(developments[i].occurred_at) if developments[i].occurred_at else datetime.min,
                           i),
        )
        seen: dict[tuple[str, EventType], int] = defaultdict(int)
        counts = [0] * len(developments)
        for i in order:
            dev = developments[i]
            counts[i] = dev.prior_similar_count
            if dev.topic_key:
                key = (dev.topic_key, dev.classification.event_type)
                counts[i] += seen[key]
                seen[key] += 1
        return counts

    @staticmethod
    def _concrete_by_topic(developments: Sequence[RankingInput]) -> dict[str, set[int]]:
        topics: dict[str, set[int]] = defaultdict(set)
        for i, dev in enumerate(developments):
            c = dev.classification
            if (dev.topic_key and c.concreteness in CONCRETE and not c.is_routine_commentary
                    and dev.status != DevelopmentStatus.SUPERSEDED):
                topics[dev.topic_key].add(i)
        return topics

    # -- scoring -----------------------------------------------------------------

    def _score(self, dev: RankingInput, idx: int, repeats: int,
               concrete_by_topic: dict[str, set[int]], now: datetime) -> _Adjustments:
        cfg = self.config
        c = dev.classification
        adj = _Adjustments(cfg.event_type_weights[c.event_type])
        rhetorical = c.concreteness in RHETORIC or c.is_routine_commentary

        # how the parties interacted
        mode_w = cfg.interaction_mode_weights.get(c.interaction_mode, 0.0)
        if c.interaction_mode == InteractionMode.PHYSICAL:
            adj.add(mode_w, RankReason.PHYSICAL_INTERACTION)
        elif c.interaction_mode in REMOTE:
            adj.add(mode_w, RankReason.REMOTE_INTERACTION)
        else:
            adj.add(mode_w)

        # deeds over words
        reason = _CONCRETENESS_REASON.get(c.concreteness)
        if c.event_type == EventType.POLICY_CHANGE and c.concreteness in (Concreteness.DECISION, Concreteness.ACTION):
            reason = RankReason.NEW_POLICY
        adj.add(cfg.concreteness_weights.get(c.concreteness, 0.0), reason)

        if c.significance_class is not None:
            adj.add(cfg.significance_weights.get(c.significance_class, 0.0),
                    RankReason.HIGH_SIGNIFICANCE if c.significance_class in HIGH_SIGNIFICANCE else None)

        # most senior actor
        seniority = max((cfg.role_weights.get(r, 0.0) for r in dev.actor_roles), default=0.0)
        adj.add(seniority, RankReason.SENIOR_ACTOR if seniority >= cfg.senior_role_threshold else None)

        # corroboration
        confidence_reason = {ConfidenceClass.CONFIRMED: RankReason.INDEPENDENTLY_CONFIRMED,
                             ConfidenceClass.DISPUTED: RankReason.DISPUTED}.get(dev.confidence)
        adj.add(cfg.confidence_weights.get(dev.confidence, 0.0), confidence_reason)
        corr = cfg.corroboration
        if dev.independent_sources > 1:
            bonus = min(corr.max_bonus, corr.per_extra_source * (dev.independent_sources - 1))
            adj.add(bonus, RankReason.WIDELY_REPORTED if dev.independent_sources >= corr.widely_reported_sources else None)

        for flag in c.uncertainty_flags:
            adj.add(-cfg.uncertainty_penalties.get(flag, 0.0), _FLAG_REASON.get(flag, RankReason.WEAK_EVIDENCE))

        if c.is_routine_commentary:
            adj.add(-cfg.routine_commentary_penalty, RankReason.ROUTINE_COMMENTARY)

        # redundancy / novelty
        red = cfg.redundancy
        if repeats:
            rate = red.per_repeat.get(c.concreteness, red.default_per_repeat)
            if c.is_routine_commentary:
                rate = max(rate, red.per_repeat.get(Concreteness.COMMENTARY, red.default_per_repeat))
            adj.add(-min(red.max_penalty, rate * repeats),
                    RankReason.DUPLICATE_COMMENTARY_PENALTY if rhetorical else RankReason.REPEATED_COVERAGE_PENALTY)
        elif dev.topic_key and not rhetorical:
            adj.add(cfg.novelty_bonus, RankReason.NEW_DEVELOPMENT)

        if rhetorical and dev.topic_key and concrete_by_topic.get(dev.topic_key, set()) - {idx}:
            adj.add(-cfg.overshadow_penalty, RankReason.OVERSHADOWED_BY_CONCRETE)

        # lifecycle
        adj.add(cfg.status_weights.get(dev.status, 0.0), _STATUS_REASON.get(dev.status))
        if dev.previous_status and dev.previous_status != dev.status:
            key = f"{dev.previous_status.value}->{dev.status.value}"
            adj.add(cfg.status_transition_weights.get(key, 0.0), RankReason.STATUS_CHANGE)

        self._geography(dev, adj)

        # recency
        if dev.occurred_at:
            rec = cfg.recency
            age_hours = (now - _utc_naive(dev.occurred_at)).total_seconds() / 3600
            if age_hours > rec.grace_hours:
                adj.add(-min(rec.max_penalty, rec.penalty_per_day * (age_hours - rec.grace_hours) / 24),
                        RankReason.STALE)
        return adj

    def _geography(self, dev: RankingInput, adj: _Adjustments) -> None:
        geo = self.config.geography
        c = dev.classification
        countries = {x.lower() for x in c.countries}
        priority = {k.lower(): v for k, v in geo.priority_countries.items()}
        regions = {k.lower(): v for k, v in geo.priority_regions.items()}
        best = max([priority[x] for x in countries if x in priority]
                   + ([regions[dev.region.lower()]] if dev.region and dev.region.lower() in regions else []),
                   default=0.0)
        adj.add(best, RankReason.PRIORITY_GEOGRAPHY)

        extra = len(countries) - geo.countries_included
        if extra > 0:
            adj.add(min(geo.max_multinational_bonus, geo.per_extra_country * extra), RankReason.MULTINATIONAL)

        global_orgs = {o.lower() for o in geo.global_organizations}
        if any(o.lower() in global_orgs for o in c.organizations):
            adj.add(geo.global_organization_bonus, RankReason.GLOBAL_INSTITUTION)
