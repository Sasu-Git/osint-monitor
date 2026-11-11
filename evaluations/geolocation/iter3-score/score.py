"""Iteration 3 scoring, run step 3: score every system's outputs against both label bases (SCORING.md). Read-only.

    python score.py --outputs outputs --out results.json --md RESULTS-TABLES.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SAMPLE = HERE.parent / "iter3-sample"
SYSTEMS = ["B0", "B1", "I1", "I2", "I3-2a", "I3-3a", "I3-4a", "I3-5a", "I3-all"]
GATES = {"W_removed_share": 0.80, "C_preserved_share": 0.90}   # iteration 1's, PROPOSED (not approved)


def label_bases() -> dict[str, dict[int, str]]:
    final = {int(k): v["event_country"] for k, v in
             yaml.safe_load((SAMPLE / "owner-labels.yaml").read_text(encoding="utf-8")).items()}
    first: dict[int, str] = {}
    for line in (SAMPLE / "owner-label-history.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            first.setdefault(int(r["case"]), r["event_country"])
    assert set(first) == set(final), "label bases cover different cases"
    return {"primary_first_answers": first, "secondary_final_labels": final}


def outcome(s: str, g: str) -> str:
    if g == "NONE":
        return "CORRECT_NONE" if s == "NONE" else "SPURIOUS"
    return "CORRECT" if s == g else "MISSED" if s == "NONE" else "WRONG_COUNTRY"


def share(n: int, d: int) -> float | None:
    return round(n / d, 3) if d else None


def score_system(sys_out: dict[int, str], base: dict[int, str], gold: dict[int, str]) -> dict:
    overall = Counter(outcome(sys_out[i], gold[i]) for i in gold)
    w = [i for i in gold if base[i] != "NONE" and base[i] != gold[i]]
    c = [i for i in gold if base[i] != "NONE" and base[i] == gold[i]]
    u = [i for i in gold if base[i] == "NONE"]
    w_removed = [i for i in w if sys_out[i] != base[i]]
    c_preserved = [i for i in c if sys_out[i] == gold[i]]
    r = {
        "overall": dict(sorted(overall.items())),
        "agree_with_gold": sum(1 for i in gold if sys_out[i] == gold[i]),
        "W_total": len(w), "W_removed": len(w_removed), "W_removed_share": share(len(w_removed), len(w)),
        "C_total": len(c), "C_preserved": len(c_preserved), "C_preserved_share": share(len(c_preserved), len(c)),
        "C_lost_to_none": sum(1 for i in c if sys_out[i] == "NONE"),
        "C_changed": sum(1 for i in c if sys_out[i] not in ("NONE", gold[i])),
        "W_still_wrong_cases": sorted(i for i in w if i not in w_removed),
        "C_lost_cases": sorted(i for i in c if i not in c_preserved),
        "unmapped": dict(sorted(Counter(outcome(sys_out[i], gold[i]) for i in u).items())),
        "unmapped_total": len(u),
    }
    r["meets_proposed_gates"] = (r["W_removed_share"] is not None and r["W_removed_share"] >= GATES["W_removed_share"]
                                 and r["C_preserved_share"] is not None
                                 and r["C_preserved_share"] >= GATES["C_preserved_share"])
    return r


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outputs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--md", type=Path, required=True)
    a = ap.parse_args()
    outs, hashes = {}, {}
    for s in SYSTEMS:
        p = a.outputs / f"{s}.json"
        hashes[s] = hashlib.sha256(p.read_bytes()).hexdigest()
        outs[s] = {int(k): v["country"] for k, v in json.loads(p.read_text(encoding="utf-8"))["cases"].items()}
    bases = label_bases()
    base_map = outs["B0"]
    results = {"gates_PROPOSED_not_approved": GATES, "output_sha256": hashes, "bases": {}}
    for name, gold in bases.items():
        assert set(gold) == set(base_map), "outputs and labels cover different cases"
        results["bases"][name] = {s: score_system(outs[s], base_map, gold) for s in SYSTEMS}
    verdicts = {}
    for s in SYSTEMS:
        if s.startswith("B"):
            continue
        p, f = (results["bases"][b][s]["meets_proposed_gates"] for b in bases)
        verdicts[s] = "meets PROPOSED gates on both bases" if p and f else \
            "fails PROPOSED gates on both bases" if not p and not f else "INCONCLUSIVE (bases disagree)"
    results["verdicts_against_PROPOSED_gates"] = verdicts
    a.out.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8", newline="\n")

    lines = ["| System | Basis | Agree with gold | W removed | C preserved | C lost to NONE | Overall outcomes |",
             "|---|---|---|---|---|---|---|"]
    for s in SYSTEMS:
        for b in bases:
            r = results["bases"][b][s]
            lines.append(f"| {s} | {b.split('_')[0]} | {r['agree_with_gold']}/100 | {r['W_removed']}/{r['W_total']} "
                         f"({r['W_removed_share']}) | {r['C_preserved']}/{r['C_total']} ({r['C_preserved_share']}) | "
                         f"{r['C_lost_to_none']} | {r['overall']} |")
    lines += ["", "| System | Verdict against PROPOSED gates |", "|---|---|"]
    lines += [f"| {s} | {v} |" for s, v in verdicts.items()]
    a.md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
