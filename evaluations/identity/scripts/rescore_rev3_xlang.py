"""Rescore the frozen cross-language benchmark observations (runs/rev3-xlang.json) against the current gold labels
(revision 4), without replaying anything.

    python evaluations/identity/scripts/rescore_rev3_xlang.py   # -> runs/rev4-xlang-rescore.json, prints the report

The replay outputs (together / apart per case, stage off and on, and every accepted link with its evidence) are
treated as frozen observations; only the labels change.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")


def prf(rows, key):
    tp = sum(1 for r in rows if r["label"] == "SAME_DEVELOPMENT" and r[key])
    fp = sum(1 for r in rows if r["label"] == "DIFFERENT_DEVELOPMENT" and r[key])
    fn = sum(1 for r in rows if r["label"] == "SAME_DEVELOPMENT" and not r[key])
    p = tp / (tp + fp) if tp + fp else None
    rc = tp / (tp + fn) if tp + fn else None
    return {"tp": tp, "fp": fp, "fn": fn, "precision": p, "recall": rc,
            "f1": 2 * p * rc / (p + rc) if p and rc else None}


def fmt(x):
    return "-" if x is None else f"{x:.2f}"


def main() -> int:
    arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d   # noqa: E731
    obs = json.loads((ROOT / "runs" / arg("--in", "rev3-xlang.json")).read_text(encoding="utf-8"))
    adds = yaml.safe_load((ROOT / "gold" / "identity-gold-rev3-additions.yaml").read_text(encoding="utf-8"))
    rows = [{**r, "label": adds[r["case"]]["label"]} for r in obs["rows"]]
    groups = {"all": rows,
              **{f"band {b}": [r for r in rows if r["band"] == b] for b in sorted({r["band"] for r in rows})},
              **{f"langs {l}": [r for r in rows if r["langs"] == l] for l in sorted({r["langs"] for r in rows})}}
    report = {k: {"off": prf(v, "off"), "on": prf(v, "on"), "n": len(v)} for k, v in groups.items()}
    stage_true = sorted(r["case"] for r in rows if r["on"] and not r["off"] and r["label"] == "SAME_DEVELOPMENT")
    stage_false = sorted(r["case"] for r in rows if r["on"] and not r["off"] and r["label"] == "DIFFERENT_DEVELOPMENT")
    missed = sorted(r["case"] for r in rows if not r["on"] and r["label"] == "SAME_DEVELOPMENT")
    # which accepted link evidence produced each false merge: links whose unit sides contain the case's items
    def links_for(case):
        e = adds[case]
        return [l for l in obs["accepted_links"] if l["window"] == e["window"]
                and ((e["a"] in l["a"] and e["b"] in l["b"]) or (e["a"] in l["b"] and e["b"] in l["a"]))]
    false_detail = {c: [l["evidence"] for l in links_for(c)][:2] for c in stage_false}
    evid = Counter()
    for c in stage_false:
        for l in links_for(c)[:1]:
            for ev in l["evidence"][1:]:
                evid[ev.split(" ")[1] if ev.startswith("shared") else ev.split(" ")[0]] += 1
    out = {"labels": "revision 4", "report": report, "stage_added_true": stage_true, "stage_added_false": stage_false,
           "missed_same_on": missed, "false_merge_evidence": false_detail, "false_merge_anchor_kinds": dict(evid),
           "accepted_link_count": obs["accepted_link_count"], "regression": obs["regression"]}
    (ROOT / "runs" / arg("--out", "rev4-xlang-rescore.json")).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                                                           encoding="utf-8")
    print(f"{'group':28s} {'n':>3s}  off P/R/F1        on P/R/F1   (tp/fp/fn on)")
    for k, v in report.items():
        o, n = v["off"], v["on"]
        print(f"{k:28s} {v['n']:3d}  {fmt(o['precision'])}/{fmt(o['recall'])}/{fmt(o['f1'])}   "
              f"{fmt(n['precision'])}/{fmt(n['recall'])}/{fmt(n['f1'])}   ({n['tp']}/{n['fp']}/{n['fn']})")
    print("accepted links:", obs["accepted_link_count"])
    print("stage added TRUE merges:", stage_true)
    print("stage added FALSE merges:", stage_false)
    print("anchor kinds behind false merges:", dict(evid))
    print("missed SAME (on):", missed)
    print("regression:", {k: (v["off"], v["on"]) for k, v in obs["regression"].items()})
    for c, ev in false_detail.items():
        print(f"  {c}: {ev[0] if ev else 'no direct link (merged through a chain)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
