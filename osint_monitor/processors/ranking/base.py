"""DevelopmentRanker interface.

A ranker orders classified developments by editorial importance and says why.
Ranking is policy, so the default implementation is deterministic and driven by
config/ranking.yaml; it never calls an LLM and never touches the database.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, Sequence, runtime_checkable

from osint_monitor.core.models import RankedDevelopment, RankingInput


@runtime_checkable
class DevelopmentRanker(Protocol):
    """Anything with this method can rank developments."""

    name: str

    def rank(self, developments: Sequence[RankingInput],
             now: datetime | None = None) -> list[RankedDevelopment]:
        """Return every development, most important first. Deterministic for equal inputs."""
        ...
