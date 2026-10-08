"""Score the current code on the identity gold (revision 2), development windows only, and compare with the Phase 2
baseline. The holdout is never replayed or scored here (holdout scoring is a separate, one-time step).

Usage: python evaluations/identity/scripts/score_identity.py --label NAME [--runs 1]
Writes runs/phase2-dev-NAME.json and prints the metric table against runs/phase2-baseline.json.
"""
import json
import os
import sys
from collections import Counter
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

import replay_current  # noqa: E402
from phase2_baseline import comparable, diff_traces, score  # noqa: E402


def totals(windows):
    T = Counter()
    for w in windows:
        T.update(w["tally"])
    mixed = sum(len(w["mixed"]) for w in windows)
    labelled = sum(len(w["labelled_developments"]) for w in windows)
    dup = sum(len(w["duplicate_memberships"]) for w in windows)
    inside = sum(w["items_in_developments"] for w in windows)
    single = sum(len(w["single_source"]) for w in windows)
    infl = sum(1 for w in windows for r in w["roundups"] if r["source_count_inflated"])
    summ = sum(1 for w in windows for r in w["roundups"] if r["summary_is_roundup_with_reports_present"])
    return {
        "continuity_precision": (T["together_and_same"], T["together"]),
        "continuity_recall": (T["together_and_same"], T["gold_same"]),
        "split_failures": (T["together"] - T["together_and_same"], T["pairs"] - T["gold_same"]),
        "merge_failures": (T["gold_same"] - T["together_and_same"], T["gold_same"]),
        "id_stability": (T["cross_tick_same_retained"], T["cross_tick_same"]),
        "mixed_developments": (mixed, labelled),
        "duplicate_membership": (dup, inside),
        "single_source_developments": (single, None),
        "roundup_source_inflation": (infl, None),
        "roundup_summaries": (summ, None),
        "error_classes": dict(Counter(e["error_class"] for w in windows for e in w["ledger"])),
    }


def fmt(v):
    n, d = v
    return f"{n}" if d is None else (f"{n}/{d} ({100 * n / d:.0f}%)" if d else f"{n}/0")


def main() -> int:
    label = sys.argv[sys.argv.index("--label") + 1]
    nruns = int(sys.argv[sys.argv.index("--runs") + 1]) if "--runs" in sys.argv else 1
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    gm = yaml.safe_load((ROOT / "gold" / "manifest.yaml").read_text(encoding="utf-8"))
    assert gm["revision"] >= 2          # revision 3 only adds cases (scored by score_rev3_xlang.py); these are rev 2's
    gold = {k: v for k, v in yaml.safe_load((ROOT / "gold" / "identity-gold.yaml").read_text(encoding="utf-8")).items()
            if v["split"] == "development"}
    results, determinism = [], []
    for w in manifest["windows"]:
        if w["split"] != "development":
            continue
        runs = [replay_current.replay(w) for _ in range(nruns)]
        if nruns > 1:
            diffs = diff_traces(comparable(runs[0]), comparable(runs[1]))
            determinism.append({"window": w["id"], "identical": not diffs, "diffs": diffs[:10]})
        results.append(score(runs[0], gold))
        traces = ROOT / "runs" / f"phase2-dev-{label}-traces"
        traces.mkdir(parents=True, exist_ok=True)
        (traces / f"{w['id']}.json").write_text(json.dumps(comparable(runs[0]), indent=1, ensure_ascii=False) + "\n",
                                                encoding="utf-8", newline="\n")
        print(w["id"], "scored", flush=True)
    out = ROOT / "runs" / f"phase2-dev-{label}.json"
    out.write_text(json.dumps({"label": label, "gold_revision": 2, "windows": results, "determinism": determinism},
                              indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    base = totals(json.loads((ROOT / "runs" / "phase2-baseline.json").read_text(encoding="utf-8"))["windows"])
    now = totals(results)
    print(f"{'metric':30s} {'baseline':>16s} {label:>16s}")
    for k in base:
        if k == "error_classes":
            continue
        print(f"{k:30s} {fmt(base[k]):>16s} {fmt(now[k]):>16s}")
    print("error classes baseline:", base["error_classes"])
    print(f"error classes {label}:", now["error_classes"])
    if determinism:
        print("determinism:", {d["window"]: d["identical"] for d in determinism})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
