"""Mark every relation gold revision 2 case as RUNTIME_ELIGIBLE, NOT_SURFACED or BLOCKED_BY_IDENTITY.

    python evaluations/relations/scripts/mark_runtime_eligibility.py

Owner decision (2026-10-09): relation endpoints stay Development IDs only. The 187-case gold is semantic relation
gold at the occurrence (item-set) level and stays frozen; eligibility depends on which Developments the system
formed, so it is a derived file tied to the code and the replays that produced it (runs-rev2/), not part of the
gold:

- RUNTIME_ELIGIBLE: both sides map to Developments and at least one distinct Development pair exists;
- NOT_SURFACED: a side is in no Development (upstream Development formation; not a relation-layer error);
- BLOCKED_BY_IDENTITY: both sides map only to the same single Development (an upstream identity over-merge).

Writes runtime-eligibility-rev2.yaml with, for blocked cases, the merging Development and its size (input to the
Phase 2 over-merge follow-up).
"""
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATUS = {"COVERED": "RUNTIME_ELIGIBLE", "NOT_SURFACED": "NOT_SURFACED", "BLOCKED_BY_IDENTITY": "BLOCKED_BY_IDENTITY"}


def main() -> int:
    summary = json.loads((ROOT / "runs-rev2" / "candidates-summary.json").read_text(encoding="utf-8"))
    gold = yaml.safe_load((ROOT / "gold" / "relation-gold-rev2.yaml").read_text(encoding="utf-8"))
    sides = yaml.safe_load((ROOT / "gold" / "relation-sides-rev2.yaml").read_text(encoding="utf-8"))
    traces = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "runs-rev2").glob("2026-*.json")}
    code = subprocess.run(["git", "log", "-1", "--format=%h", "--", "osint_monitor", "config"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    cases = {}
    for r in summary["rows"]:
        e = gold[r["case"]]
        entry = {"status": STATUS[r["coverage"]], "label": e["label"], "scored": e["scored"],
                 "canonical": e["canonical"]}
        if r["coverage"] == "BLOCKED_BY_IDENTITY":
            t = traces[sides[e["a"]]["window"]]
            [dev] = {d for m in sides[e["a"]]["members"] for d in (t["items"][m]["developments"] or [])}
            entry["development"] = {"window": t["window"], "id": dev, "size": len(t["developments"][str(dev)]["members"]),
                                    "summary": t["developments"][str(dev)]["summary"][:120]}
        if r["coverage"] == "NOT_SURFACED":
            entry["unsurfaced_sides"] = [s for s in ("a", "b") if not any(
                traces[sides[e[s]]["window"]]["items"][m]["developments"] for m in sides[e[s]]["members"])]
        cases[r["case"]] = entry
    scored = [c for c in cases.values() if c["scored"]]
    out = {"gold": "relation-gold-rev2.yaml",
           "code": code, "replays": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in sorted((ROOT / "runs-rev2").glob("2026-*.json"))},
           "counts": {"all": dict(Counter(c["status"] for c in cases.values())),
                      "scored": dict(Counter(c["status"] for c in scored)),
                      "canonical_positives": dict(Counter(c["status"] for c in scored if c["canonical"]))},
           "cases": dict(sorted(cases.items(), key=lambda kv: (kv[0][0], int(kv[0][1:]))))}
    (ROOT / "runtime-eligibility-rev2.yaml").write_text(
        "# Derived from relation gold revision 2 and runs-rev2/ (see scripts/mark_runtime_eligibility.py).\n"
        "# Not gold: eligibility changes when Development formation changes.\n"
        + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8", newline="\n")
    print(out["counts"])
    blocked = {k: v for k, v in cases.items() if v["status"] == "BLOCKED_BY_IDENTITY"}
    for k, v in blocked.items():
        d = v["development"]
        print(f"  {k} {v['label']:26s} {d['window']} D{d['id']} ({d['size']} items) {d['summary'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
