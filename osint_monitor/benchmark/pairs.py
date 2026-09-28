"""Candidate pairs for a replayed window, from several independent retrieval paths.

Paths only *propose* pairs; nothing here links anything. Each pair carries every signal
a linking rule could use, the production clusterer's decision and the gold label.

Paths:
    semantic      either item is among the other's top-k embedding neighbours
    actors        share >= 1 canonical actor (any mention)
    principals    share >= 1 canonical principal actor
    organisations share >= 1 organisation
    locations     share >= 1 location
    time          published within CLOSE_HOURS
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from itertools import combinations

import numpy as np

from osint_monitor.benchmark.format import Gold, PairLabel
from osint_monitor.benchmark.replay import ReplayResult

TOP_K = 5
CLOSE_HOURS = 6.0
PATHS = ("semantic", "actors", "principals", "organisations", "locations", "time")


@dataclass
class Pair:
    a: str
    b: str
    similarity: float
    hours_apart: float
    same_source: bool
    shared_actors: list[str]
    actor_counts: tuple[int, int]
    actor_coverage: float               # shared / smaller actor set (0 when either has none)
    shared_principals: list[str]
    shared_organisations: list[str]
    shared_locations: list[str]
    type_compatible: bool | None        # both typed and equal; None when either is unknown
    domain_compatible: bool | None
    clusterer: str                      # same_cluster | different_clusters | one_noise | both_noise
    gold: PairLabel
    paths: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        d = asdict(self)
        d["gold"] = self.gold.value
        d["similarity"] = round(self.similarity, 4)
        d["hours_apart"] = round(self.hours_apart, 2)
        d["actor_coverage"] = round(self.actor_coverage, 3)
        return d


def _typed(a: str | None, b: str | None) -> bool | None:
    if not a or not b or a in ("unknown", "other") or b in ("unknown", "other"):
        return None
    return a == b


def all_pairs(result: ReplayResult, gold: Gold, top_k: int = TOP_K) -> list[Pair]:
    """Every pair of surviving items with features; ``paths`` says which retrievals find it."""
    feats = result.features
    ids = sorted(i for i in feats if feats[i].vector is not None)
    if not ids:
        return []
    V = np.array([feats[i].vector for i in ids], dtype=float)
    V /= np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-12, None)
    sims = V @ V.T
    neighbours = {ids[n]: {ids[j] for j in [j for j in np.argsort(-sims[n]) if j != n][:top_k]}
                  for n in range(len(ids))}
    cluster_of = result.cluster_of()
    index = {i: n for n, i in enumerate(ids)}
    pairs = []
    for a, b in combinations(ids, 2):
        fa, fb = feats[a], feats[b]
        ca, cb = cluster_of.get(a), cluster_of.get(b)
        decision = ("same_cluster" if ca is not None and ca == cb else
                    "different_clusters" if ca is not None and cb is not None else
                    "both_noise" if ca is None and cb is None else "one_noise")
        shared = sorted(fa.actors & fb.actors)
        smaller = min(len(fa.actors), len(fb.actors))
        p = Pair(
            a=a, b=b, similarity=float(sims[index[a], index[b]]),
            hours_apart=abs((fa.published_at - fb.published_at).total_seconds()) / 3600,
            same_source=fa.source == fb.source, shared_actors=shared,
            actor_counts=(len(fa.actors), len(fb.actors)),
            actor_coverage=len(shared) / smaller if smaller else 0.0,
            shared_principals=sorted(fa.principals & fb.principals),
            shared_organisations=sorted(fa.organisations & fb.organisations),
            shared_locations=sorted(fa.locations & fb.locations),
            type_compatible=_typed(fa.event_type, fb.event_type),
            domain_compatible=_typed(fa.event_domain, fb.event_domain),
            clusterer=decision, gold=gold.label(a, b))
        if b in neighbours[a] or a in neighbours[b]:
            p.paths.append("semantic")
        for path, values in (("actors", p.shared_actors), ("principals", p.shared_principals),
                             ("organisations", p.shared_organisations), ("locations", p.shared_locations)):
            if values:
                p.paths.append(path)
        if p.hours_apart <= CLOSE_HOURS:
            p.paths.append("time")
        pairs.append(p)
    return pairs


def candidate_pairs(pairs: list[Pair]) -> list[Pair]:
    """Pairs found by at least one path other than time alone, or gold SAME/RELATED ones."""
    return [p for p in pairs if (set(p.paths) - {"time"}) or p.gold in (PairLabel.SAME, PairLabel.RELATED)]


def path_recall(pairs: list[Pair]) -> dict[str, dict]:
    """For each path: how many gold SAME pairs it finds, and how many pairs it proposes."""
    same = [p for p in pairs if p.gold == PairLabel.SAME and not p.same_source]
    out = {}
    for path in PATHS:
        proposed = [p for p in pairs if path in p.paths and not p.same_source]
        found = [p for p in same if path in p.paths]
        out[path] = {"proposed": len(proposed), "same_found": len(found), "same_total": len(same)}
    return out
