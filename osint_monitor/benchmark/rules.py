"""Offline link rules: what a secondary linking rule *would* change. Production is untouched.

A rule adds edges between cross-source pairs the production clusterer did not put in the
same cluster; clusters are then the connected components of (production clusters + new
edges). The effect is scored against gold labels: added true joins, added false joins
(split into related-but-distinct and unrelated), and remaining misses.

The frozen rule (``frozen_rule.yaml``) is the one candidate chosen on development windows;
it is the only rule the hold-out evaluates.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import yaml

from osint_monitor.benchmark.format import BENCHMARK_DIR, BenchmarkError, PairLabel
from osint_monitor.benchmark.pairs import Pair
from osint_monitor.processors.clustering import LINK_SIMILARITY, MEMBER_SIMILARITY

FROZEN_RULE_FILE = "frozen_rule.yaml"
BOUNDARY_HOURS = 2.0


@dataclass(frozen=True)
class LinkRule:
    name: str
    min_similarity: float = MEMBER_SIMILARITY          # 0.45
    max_similarity: float = LINK_SIMILARITY            # 0.53: above it production already links
    max_hours: float = 6.0
    min_shared: int | None = 2                         # shared canonical actors (count)
    min_coverage: float | None = None                  # alternative: shared / smaller actor set
    actor_field: str = "actors"                        # "actors" (all mentions) or "principals"
    require_same_type: bool = False
    require_shared_location: bool = False

    def passes(self, p: Pair) -> bool:
        if p.same_source or not self.min_similarity <= p.similarity < self.max_similarity:
            return False
        if p.hours_apart > self.max_hours:
            return False
        shared = p.shared_principals if self.actor_field == "principals" else p.shared_actors
        if self.min_shared is not None and len(shared) < self.min_shared:
            return False
        if self.min_coverage is not None and p.actor_coverage < self.min_coverage:
            return False
        if self.require_same_type and p.type_compatible is not True:
            return False
        if self.require_shared_location and not p.shared_locations:
            return False
        return True

    def as_dict(self) -> dict:
        return asdict(self)


PROPOSED = LinkRule("proposed: 0.45-0.53, <=6h, >=2 shared actors")


def variants() -> list[LinkRule]:
    """The proposed rule and sensible neighbours. Deliberately small: a stable relationship
    should show across nearby settings, not only at one tuned point."""
    rules = [PROPOSED]
    for hours in (4, 8, 12):
        rules.append(LinkRule(f"<= {hours}h, >=2 shared actors", max_hours=hours))
    rules += [
        LinkRule("<= 6h, >=1 shared actor", min_shared=1),
        LinkRule("<= 6h, actor coverage >= 0.5", min_shared=None, min_coverage=0.5),
        LinkRule("<= 6h, >=2 shared principals", actor_field="principals"),
        LinkRule("<= 6h, >=2 shared actors, same event type", require_same_type=True),
        LinkRule("<= 6h, >=2 shared actors, shared location", require_shared_location=True),
    ]
    return rules


def apply_rule(clusters: list[list[str]], pairs: list[Pair], rule: LinkRule, min_size: int = 2) -> list[list[str]]:
    parent: dict[str, str] = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for c in clusters:
        for i in c[1:]:
            union(c[0], i)
        find(c[0])
    for p in pairs:
        if p.clusterer != "same_cluster" and rule.passes(p):
            union(p.a, p.b)
    groups: dict[str, list[str]] = {}
    for x in parent:
        groups.setdefault(find(x), []).append(x)
    return sorted((sorted(g) for g in groups.values() if len(g) >= min_size), key=lambda g: g[0])


def rule_effect(pairs: list[Pair], rule: LinkRule) -> dict:
    """Edge-level effect: which new pairs the rule links, by gold label."""
    added = [p for p in pairs if p.clusterer != "same_cluster" and rule.passes(p)]
    missed_same = [p for p in pairs if p.gold == PairLabel.SAME and not p.same_source
                   and p.clusterer != "same_cluster" and not rule.passes(p)]
    by = {label: [p for p in added if p.gold == label] for label in PairLabel}
    near = [p for p in pairs if not p.same_source and p.clusterer != "same_cluster"
            and rule.min_similarity <= p.similarity < rule.max_similarity
            and abs(p.hours_apart - rule.max_hours) <= BOUNDARY_HOURS and p.gold != PairLabel.UNCERTAIN]
    return {
        "rule": rule.name,
        "max_hours": rule.max_hours,
        "added_same": len(by[PairLabel.SAME]),
        "added_related": len(by[PairLabel.RELATED]),
        "added_unrelated": len(by[PairLabel.UNRELATED]),
        "added_uncertain": len(by[PairLabel.UNCERTAIN]),
        "remaining_same_misses": len(missed_same),
        "remaining_misses_below_band": sum(1 for p in missed_same if p.similarity < rule.min_similarity),
        "boundary_cases": [_brief(p) for p in near],
        "false_joins": [_brief(p) for p in by[PairLabel.RELATED] + by[PairLabel.UNRELATED]],
    }


def actor_first_probe(pairs: list[Pair], max_hours: float = 24.0, below: float = MEMBER_SIMILARITY) -> dict:
    """Would actor-first retrieval find low-similarity same-development pairs, and at what cost?"""
    low = [p for p in pairs if not p.same_source and p.similarity < below and p.gold != PairLabel.UNCERTAIN]
    targets = [p for p in low if p.gold == PairLabel.SAME and p.clusterer != "same_cluster"]
    out = {"low_similarity_same_misses": len(targets)}
    for name, test in (
        (">=1 shared principal", lambda p: len(p.shared_principals) >= 1),
        (">=2 shared principals", lambda p: len(p.shared_principals) >= 2),
        (">=2 shared actors", lambda p: len(p.shared_actors) >= 2),
    ):
        retrieved = [p for p in low if p.hours_apart <= max_hours and test(p)]
        out[name] = {"candidates": len(retrieved),
                     "same_found": sum(1 for p in retrieved if p.gold == PairLabel.SAME and p.clusterer != "same_cluster"),
                     "related": sum(1 for p in retrieved if p.gold == PairLabel.RELATED),
                     "unrelated": sum(1 for p in retrieved if p.gold == PairLabel.UNRELATED)}
    return out


def _brief(p: Pair) -> dict:
    return {"a": p.a, "b": p.b, "similarity": round(p.similarity, 3), "hours": round(p.hours_apart, 1),
            "shared_actors": p.shared_actors, "gold": p.gold.value}


# --- the frozen rule ---------------------------------------------------------------------------

def freeze_rule(rule: LinkRule, rationale: str, root: Path = BENCHMARK_DIR) -> Path:
    path = root / FROZEN_RULE_FILE
    if path.exists():
        raise BenchmarkError(f"{path} exists: a rule is already frozen. Delete it deliberately to re-freeze.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump({"rule": rule.as_dict(), "rationale": rationale,
                        "frozen_at": datetime.utcnow().isoformat(timespec="seconds")}, f, sort_keys=False)
    return path


def load_frozen_rule(root: Path = BENCHMARK_DIR) -> LinkRule:
    path = root / FROZEN_RULE_FILE
    if not path.exists():
        raise BenchmarkError(f"no frozen rule at {path}. Choose one on development windows and run "
                             "`python main.py benchmark freeze-rule` before any hold-out run.")
    try:
        return LinkRule(**yaml.safe_load(path.read_text(encoding="utf-8"))["rule"])
    except (TypeError, KeyError, yaml.YAMLError) as e:
        raise BenchmarkError(f"{path}: malformed frozen rule: {e}") from e
