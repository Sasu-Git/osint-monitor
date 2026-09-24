"""Development ranking: list[RankingInput] -> list[RankedDevelopment].

PolicyRanker is deterministic and reads its weights from config/ranking.yaml.
Scores are internal sort keys; show RankedDevelopment.reasons (or
PolicyRanker.explain) in the UI, never the number.
"""

from __future__ import annotations

from pathlib import Path

from osint_monitor.core.config import load_ranking_config
from osint_monitor.processors.ranking.base import DevelopmentRanker
from osint_monitor.processors.ranking.policy import PolicyRanker

__all__ = ["DevelopmentRanker", "PolicyRanker", "get_ranker"]


def get_ranker(config_path: Path | None = None) -> DevelopmentRanker:
    return PolicyRanker(load_ranking_config(config_path))
