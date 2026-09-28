"""Benchmark metrics for a clustering (production or a rule variant) against gold labels.

Clusters are plain lists of benchmark ids, so the same functions score the current
clusterer and any offline variant. Items the pipeline dropped as duplicates are not
present and are reported, not scored.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations

from osint_monitor.benchmark.format import Gold, PairLabel


def development_metrics(clusters: list[list[str]], gold: Gold, present: set[str]) -> dict:
    cluster_of = {i: n for n, c in enumerate(clusters) for i in c}
    rows = []
    for dev, members in gold.multi_item_developments().items():
        here = [m for m in members if m in present]
        sources = {gold.source[m] for m in here}
        if len(here) < 2:
            rows.append({"development": dev, "status": "not_evaluable", "present": len(here), "sources": len(sources)})
            continue
        together = Counter(cluster_of[m] for m in here if m in cluster_of)
        best = together.most_common(1)[0][1] if together else 0
        status = "recovered" if best == len(here) else "partial" if best >= 2 else "missed"
        rows.append({"development": dev, "status": status, "present": len(here), "sources": len(sources),
                     "largest_share": best, "noise_members": sum(1 for m in here if m not in cluster_of)})
    evaluable = [r for r in rows if r["status"] != "not_evaluable"]

    def tally(subset):
        c = Counter(r["status"] for r in subset)
        return {"developments": len(subset), "recovered": c["recovered"], "partial": c["partial"],
                "missed": c["missed"]}

    multi = [r for r in evaluable if r["sources"] >= 2]
    return {
        "all": tally(evaluable),
        "multi_source": tally(multi),
        "two_sources": tally([r for r in multi if r["sources"] == 2]),
        "three_plus_sources": tally([r for r in multi if r["sources"] >= 3]),
        "single_source_multi_item": tally([r for r in evaluable if r["sources"] == 1]),
        "not_evaluable": sum(1 for r in rows if r["status"] == "not_evaluable"),
        "rows": rows,
    }


def precision_metrics(clusters: list[list[str]], gold: Gold) -> dict:
    """Over-merges: clusters mixing gold units (a development, or a singleton item)."""
    def unit(i):
        return gold.dev_of.get(i, i)
    mixed = []
    for c in clusters:
        units = Counter(unit(i) for i in c)
        if len(units) > 1:
            kinds = Counter(gold.label(a, b).value for a, b in combinations(c, 2) if unit(a) != unit(b))
            mixed.append({"size": len(c), "units": len(units), "cross_unit_pairs": dict(kinds)})
    return {"clusters": len(clusters), "mixed_clusters": len(mixed), "mixed": mixed}


def noise_metrics(clusters: list[list[str]], gold: Gold, present: set[str]) -> dict:
    clustered = {i for c in clusters for i in c}
    in_multi = {m for d in gold.multi_item_developments().values() for m in d}
    singletons = present - in_multi
    members = present & in_multi
    return {"singletons": len(singletons),
            "singletons_left_unclustered": len(singletons - clustered),
            "singletons_clustered": len(singletons & clustered),
            "members": len(members),
            "members_left_as_noise": len(members - clustered)}


def pair_metrics(clusters: list[list[str]], gold: Gold, present: set[str]) -> dict:
    """Linked = in the same cluster. SAME counted for all and for cross-source pairs;
    RELATED / UNRELATED counted only when linked (they should never be)."""
    cluster_of = {i: n for n, c in enumerate(clusters) for i in c}
    same = [(a, b) for a, b in gold.same_pairs() if a in present and b in present]
    linked_same = [(a, b) for a, b in same if a in cluster_of and cluster_of.get(a) == cluster_of.get(b)]
    cross = [(a, b) for a, b in same if gold.source[a] != gold.source[b]]
    linked_cross = [p for p in linked_same if gold.source[p[0]] != gold.source[p[1]]]
    wrong = Counter()
    for c in clusters:
        for a, b in combinations(c, 2):
            label = gold.label(a, b)
            if label in (PairLabel.RELATED, PairLabel.UNRELATED):
                wrong[label.value] += 1
    return {"same_pairs": len(same), "same_linked": len(linked_same),
            "cross_source_same_pairs": len(cross), "cross_source_same_linked": len(linked_cross),
            "related_linked": wrong[PairLabel.RELATED.value], "unrelated_linked": wrong[PairLabel.UNRELATED.value]}


def evaluate(clusters: list[list[str]], gold: Gold, present: set[str]) -> dict:
    return {"developments": development_metrics(clusters, gold, present),
            "precision": precision_metrics(clusters, gold),
            "noise": noise_metrics(clusters, gold, present),
            "pairs": pair_metrics(clusters, gold, present)}


def combine(results: list[dict]) -> dict:
    """Sum the counts of several windows' ``evaluate`` results (rows and mixed lists dropped)."""
    def add(total, value):
        if isinstance(value, dict):
            base = total if isinstance(total, dict) else {}
            return {**base, **{k: add(base.get(k), v) for k, v in value.items() if k not in ("rows", "mixed")}}
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return (total or 0) + value
        return total if total is not None else value
    combined = None
    for r in results:
        combined = add(combined, r)
    return combined or {}
