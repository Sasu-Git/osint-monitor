"""Evaluate the clusterer on frozen benchmark windows of one split.

    development: production metrics, the rule-variant sweep and the actor-first probe,
                 per window and combined. Use it to understand failures and pick a rule.
    holdout:     production metrics and the *frozen* rule only. Each run is appended to
                 holdout_runs.jsonl with the rule and file hashes, so repeated peeking is
                 visible in Git. Run it once, after freezing the rule.

Results are benchmark results on a handful of windows, not estimates for all news.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from osint_monitor.benchmark.format import (
    BENCHMARK_DIR, BenchmarkError, Gold, Split, load_items, load_labels, load_manifest, verify_frozen,
)
from osint_monitor.benchmark.metrics import combine, evaluate
from osint_monitor.benchmark.pairs import all_pairs, path_recall
from osint_monitor.benchmark.replay import replay_window
from osint_monitor.benchmark.rules import BOUNDARY_HOURS, FROZEN_RULE_FILE, actor_first_probe, apply_rule, load_frozen_rule, rule_effect, variants

HOLDOUT_LOG = "holdout_runs.jsonl"
HOLDOUT_WARNING = ("HOLD-OUT RUN. The hold-out is meant to be evaluated once, after the candidate rule is frozen "
                   "from development windows only. Do not change the rule because of what you see here.")


def evaluate_split(split: Split, root: Path = BENCHMARK_DIR, window_ids: list[str] | None = None,
                   replay=replay_window) -> dict:
    manifest = load_manifest(root)
    windows = [w for w in manifest.windows if w.split == split and (not window_ids or w.id in window_ids)]
    if not windows:
        raise BenchmarkError(f"no {split.value} windows in {root / 'manifest.yaml'}")
    frozen = load_frozen_rule(root) if split == Split.HOLDOUT else None
    rules = [frozen] if frozen else variants()

    per_window, combined_current, combined_rules = [], [], {r.name: [] for r in rules}
    effects = {r.name: [] for r in rules}
    probes, recalls = [], []
    for w in windows:
        verify_frozen(w, root)
        items = load_items(root / w.items_file)
        gold = Gold(load_labels(root / w.labels_file, items), items)
        result = replay(items)
        present = set(result.features)
        pairs = all_pairs(result, gold)
        current = evaluate(result.clusters, gold, present)
        combined_current.append(current)
        window_report = {"window": w.id, "items": len(items), "deduplicated": len(result.deduplicated),
                         "current": current, "rules": {}}
        for rule in rules:
            variant = evaluate(apply_rule(result.clusters, pairs, rule), gold, present)
            effect = rule_effect(pairs, rule)
            window_report["rules"][rule.name] = {"metrics": variant, "effect": effect}
            combined_rules[rule.name].append(variant)
            effects[rule.name].append(effect)
        if split == Split.DEVELOPMENT:
            probes.append(actor_first_probe(pairs))
            recalls.append(path_recall(pairs))
            window_report["pairs"] = [p.as_dict() for p in pairs
                                      if p.gold.value != "unrelated" or set(p.paths) - {"time"}]
        per_window.append(window_report)

    report = {
        "split": split.value,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds"),
        "windows": [w.id for w in windows],
        "current": combine(combined_current),
        "rules": {name: {"metrics": combine(ms), "effect": _sum_effects(effects[name])}
                  for name, ms in combined_rules.items()},
        "per_window": per_window,
    }
    if split == Split.DEVELOPMENT:
        report["actor_first"] = combine(probes)
        report["path_recall"] = combine(recalls)
    else:
        _log_holdout(root, frozen, windows)
    return report


def _sum_effects(effects: list[dict]) -> dict:
    keys = ("added_same", "added_related", "added_unrelated", "added_uncertain",
            "remaining_same_misses", "remaining_misses_below_band")
    out = {k: sum(e[k] for e in effects) for k in keys}
    out["max_hours"] = effects[0]["max_hours"] if effects else None
    out["boundary_cases"] = [c for e in effects for c in e["boundary_cases"]]
    out["false_joins"] = [c for e in effects for c in e["false_joins"]]
    return out


def _log_holdout(root: Path, rule, windows) -> None:
    rule_hash = hashlib.sha256((root / FROZEN_RULE_FILE).read_bytes()).hexdigest()
    record = {"ran_at": datetime.utcnow().isoformat(timespec="seconds"), "rule": rule.name, "rule_sha256": rule_hash,
              "windows": {w.id: {"items": w.items_sha256, "labels": w.labels_sha256} for w in windows}}
    with open(root / HOLDOUT_LOG, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def previous_holdout_runs(root: Path = BENCHMARK_DIR) -> list[dict]:
    path = root / HOLDOUT_LOG
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def format_report(report: dict) -> str:
    def dev_line(m):
        d = m["developments"]
        ms, two, three = d["multi_source"], d["two_sources"], d["three_plus_sources"]
        return (f"multi-source developments {ms['developments']}: recovered {ms['recovered']}, "
                f"partial {ms['partial']}, missed {ms['missed']}  "
                f"(2 sources: {two['recovered']}/{two['developments']} recovered; "
                f"3+: {three['recovered']}/{three['developments']})")

    def rest_line(m):
        p, n, pr = m["pairs"], m["noise"], m["precision"]
        return (f"cross-source SAME pairs linked {p['cross_source_same_linked']}/{p['cross_source_same_pairs']}; "
                f"wrong links: related {p['related_linked']}, unrelated {p['unrelated_linked']}; "
                f"mixed clusters {pr['mixed_clusters']}/{pr['clusters']}; "
                f"members left as noise {n['members_left_as_noise']}/{n['members']}; "
                f"singletons clustered {n['singletons_clustered']}/{n['singletons']}")

    lines = [f"BENCHMARK RESULTS ({report['split']}) on windows {report['windows']} — "
             "a small labelled benchmark, not an estimate for all news.", "",
             "Current clusterer:", "  " + dev_line(report["current"]), "  " + rest_line(report["current"]), ""]
    for name, r in report["rules"].items():
        e = r["effect"]
        lines += [f"Rule [{name}]",
                  f"  adds: same {e['added_same']}, related {e['added_related']}, unrelated {e['added_unrelated']}"
                  f"; remaining cross-source SAME misses {e['remaining_same_misses']} "
                  f"({e['remaining_misses_below_band']} below the band)",
                  "  " + dev_line(r["metrics"]),
                  f"  pairs within {BOUNDARY_HOURS:.0f}h of the {e['max_hours']:g}h limit: {len(e['boundary_cases'])}; "
                  f"false joins listed in --out"]
    if "actor_first" in report:
        lines += ["", "Actor-first retrieval for low-similarity SAME misses (not implemented):",
                  f"  {json.dumps(report['actor_first'], sort_keys=True)}",
                  "Retrieval paths (cross-source pairs; found / gold SAME, and share of proposals that are SAME):"]
        for path, r in sorted(report["path_recall"].items()):
            share = f"{r['same_found'] / r['proposed']:.2f}" if r["proposed"] else "-"
            lines.append(f"  {path:13} {r['same_found']}/{r['same_total']}  proposes {r['proposed']}  ({share})")
    lines += ["", "Pairs not SAME and not labelled RELATED are assumed UNRELATED (not every pair is reviewed)."]
    return "\n".join(lines)
