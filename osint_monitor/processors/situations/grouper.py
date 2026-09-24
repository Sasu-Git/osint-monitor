"""Deterministic situation grouping (no database).

For each development, every open situation that shares enough of its actors is a
candidate. Candidates are compared on the evidence available for that pair --
actor overlap, same region, semantic similarity to the situation's recent
developments, the situation's topic keywords -- averaged over the signals that
exist, so a missing embedding or region neither helps nor hurts.

  clear best candidate >= join_threshold          -> join it
  best in the ambiguous band, or two close calls  -> ask the arbiter (LLM, optional);
                                                     it may only pick an existing candidate
  nothing                                          -> stay unassigned

Unassigned developments whose canonical actor set (>= min_actors_to_create actors)
recurs at least create_min_developments times become a new situation keyed by that
actor set -- unless a situation with the same actor set already exists.
"""

from __future__ import annotations

import logging
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Protocol, Sequence, runtime_checkable

from osint_monitor.core.config import SituationsConfig, load_situations_config
from osint_monitor.core.models import (
    DevelopmentSignature, SituationAssignment, SituationMatchReason, SituationProfile, SituationStatus,
)
from osint_monitor.processors.situations.canonical import ActorCanonicalizer

logger = logging.getLogger(__name__)
R = SituationMatchReason


@runtime_checkable
class SituationArbiter(Protocol):
    """Settles ambiguous cases. Must return one of the candidate slugs, or None."""

    def choose(self, development: DevelopmentSignature, candidates: Sequence[SituationProfile]) -> str | None:
        ...


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


class SituationGrouper:
    def __init__(self, config: SituationsConfig | None = None, arbiter: SituationArbiter | None = None):
        self.config = config or load_situations_config()
        self.arbiter = arbiter
        self.actors = ActorCanonicalizer(self.config.actor_aliases, self.config.actor_represents)
        for seed in self.config.situations:
            for name in seed.primary_actors:
                self.actors.remember(name)

    # -- one development vs one situation ----------------------------------------------

    def match(self, dev: DevelopmentSignature, situation: SituationProfile) -> tuple[float, list[R]] | None:
        """Evidence that ``dev`` belongs to ``situation``; None if it is not a candidate."""
        p = self.config.policy
        dev_actors = self.actors.keys(dev.actors)
        sit_actors = self.actors.keys(situation.primary_actors)
        shared = dev_actors & sit_actors
        if not shared or situation.status == SituationStatus.CLOSED:
            return None
        coverage = len(shared) / len(sit_actors)
        min_coverage = p.min_actor_coverage if dev.actors_are_principal else p.fallback_min_actor_coverage
        if coverage < min_coverage:
            return None

        signals = [(p.actor_weight, coverage, R.ACTOR_OVERLAP)]
        if dev.region and situation.region:
            signals.append((p.region_weight, float(dev.region == situation.region), R.SAME_REGION))
        if dev.embedding and situation.centroid:
            signals.append((p.semantic_weight, max(0.0, _cosine(dev.embedding, situation.centroid)),
                            R.SEMANTIC_SIMILARITY))
        if situation.keywords:
            title = dev.title.lower()
            hit = any(re.search(rf"\b{re.escape(k.lower())}\b", title) for k in situation.keywords)
            signals.append((p.keyword_weight, float(hit), R.TOPIC_KEYWORDS))

        score = sum(w * s for w, s, _ in signals) / sum(w for w, _, _ in signals)
        return score, [r for _, s, r in signals if s >= 0.5]

    def assign(self, dev: DevelopmentSignature, situations: Sequence[SituationProfile]) -> SituationAssignment:
        p = self.config.policy
        scored = []
        for s in situations:
            m = self.match(dev, s)
            if m is not None:
                scored.append((m[0], s, m[1]))
        scored.sort(key=lambda t: (-t[0], t[1].slug))
        candidates = [s.slug for _, s, _ in scored]
        if not scored or scored[0][0] < p.ambiguous_threshold:
            return SituationAssignment(event_id=dev.event_id, reasons=[R.NO_MATCH], candidates=candidates)

        best_score, best, best_reasons = scored[0]
        runner_up = scored[1][0] if len(scored) > 1 else None
        join_threshold = p.join_threshold if dev.actors_are_principal else p.fallback_join_threshold
        clear = best_score >= join_threshold and (runner_up is None or best_score - runner_up > p.ambiguity_margin)
        if clear:
            return SituationAssignment(event_id=dev.event_id, slug=best.slug, reasons=best_reasons,
                                       candidates=candidates)

        contenders = [(sc, s, rs) for sc, s, rs in scored if sc >= p.ambiguous_threshold]
        choice = self._arbitrate(dev, [s for _, s, _ in contenders])
        for _, s, reasons in contenders:
            if s.slug == choice:
                return SituationAssignment(event_id=dev.event_id, slug=s.slug,
                                           reasons=[*reasons, R.ARBITER_CHOICE], candidates=candidates)
        return SituationAssignment(event_id=dev.event_id, reasons=[R.AMBIGUOUS], candidates=candidates)

    def _arbitrate(self, dev: DevelopmentSignature, candidates: list[SituationProfile]) -> str | None:
        if self.arbiter is None:
            return None
        try:
            choice = self.arbiter.choose(dev, candidates)
        except Exception as e:
            logger.warning("Situation arbiter failed for event %s: %s", dev.event_id, e)
            return None
        if choice is not None and choice not in {c.slug for c in candidates}:
            logger.warning("Situation arbiter returned unknown slug %r; ignored", choice)
            return None
        return choice

    # -- a batch ---------------------------------------------------------------------------

    def group(self, developments: Sequence[DevelopmentSignature], situations: Sequence[SituationProfile]
              ) -> tuple[list[SituationAssignment], list[SituationProfile]]:
        """Assign a batch of unassigned developments. Returns (assignments in input order,
        situations created for this batch)."""
        p = self.config.policy
        order = sorted(range(len(developments)),
                       key=lambda i: (developments[i].occurred_at or datetime.min, i))
        assignments: list[SituationAssignment | None] = [None] * len(developments)
        for i in order:
            assignments[i] = self.assign(developments[i], situations)

        existing_sets = {self.actors.keys(s.primary_actors) for s in situations}
        existing_slugs = {s.slug for s in situations}
        recurring: dict[frozenset[str], list[int]] = defaultdict(list)
        for i in order:
            # only principal actor sets define new storylines; incidental mentions never do
            if assignments[i].slug is None and developments[i].actors_are_principal:
                key = self.actors.keys(developments[i].actors)
                if len(key) >= p.min_actors_to_create:
                    recurring[key].append(i)

        created: list[SituationProfile] = []
        for key, members in recurring.items():
            slug = self.actors.slug(key)
            if len(members) < p.create_min_developments or key in existing_sets or slug in existing_slugs:
                continue
            regions = Counter(developments[i].region for i in members if developments[i].region)
            profile = SituationProfile(
                slug=slug, title=self.actors.title(key),
                region=regions.most_common(1)[0][0] if regions else None,
                primary_actors=sorted(self.actors.display(k) for k in key),
            )
            created.append(profile)
            existing_slugs.add(slug)
            for i in members:
                assignments[i] = SituationAssignment(event_id=developments[i].event_id, slug=slug, created=True,
                                                     reasons=[R.RECURRING_ACTORS, R.ACTOR_OVERLAP],
                                                     candidates=assignments[i].candidates)
        return list(assignments), created
