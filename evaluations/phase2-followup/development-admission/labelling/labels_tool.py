"""Validate, freeze and summarise the Development-admission owner labels (no DA rule is applied here).

    python labels_tool.py validate            all cases labelled, one verdict each, reviewer recorded, frozen files intact
    python labels_tool.py freeze              validate, then write LABELS-FREEZE.json (label-file hash, reviewers, inputs)
    python labels_tool.py summary             counts by label set (L1, L2, L2b, L3a, L3b) and stratum

The summary reports label counts only. It never applies a variant's admission test (that is the H3 feasibility
check, which needs a separate approval).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
LABELS = ("SAME_OCCURRENCE", "DIFFERENT_OCCURRENCE", "AMBIGUOUS")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load():
    cases = {c["case"] for c in json.loads((HERE / "review-cases.json").read_text(encoding="utf-8"))}
    key = json.loads((HERE / "key.json").read_text(encoding="utf-8"))
    path = HERE / "owner-labels.yaml"
    labels = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.exists() else {}
    return cases, key, labels


def validate() -> list[str]:
    cases, key, labels = load()
    problems = []
    freeze = json.loads((HERE / "FREEZE-LABELLING.json").read_text(encoding="utf-8"))
    for name, h in freeze["outputs"].items():
        if sha(HERE / name) != h:
            problems.append(f"frozen file changed: {name}")
    if set(key) != cases:
        problems.append("key and cases differ")
    for c in sorted(cases):
        e = labels.get(c)
        if not e or not e.get("label"):
            problems.append(f"{c}: not labelled")
            continue
        if e["label"] not in LABELS:
            problems.append(f"{c}: invalid label {e['label']!r}")
        if not e.get("reviewer"):
            problems.append(f"{c}: no reviewer")
        for h in e.get("history") or []:
            if h.get("reviewer") and h["reviewer"] != e["reviewer"]:
                problems.append(f"{c}: verdict history has another reviewer ({h['reviewer']})")
    for c in labels:
        if c not in cases:
            problems.append(f"{c}: label for an unknown case")
    return problems


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "validate"
    cases, key, labels = load()
    if cmd in ("validate", "freeze"):
        problems = validate()
        print(f"{sum(1 for c in cases if (labels.get(c) or {}).get('label'))} of {len(cases)} labelled; {len(problems)} problem(s)")
        for p in problems[:40]:
            print("  ", p)
        if problems:
            return 1
        if cmd == "freeze":
            out = {"frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "labels_sha256": sha(HERE / "owner-labels.yaml"),
                   "reviewers": dict(Counter(e["reviewer"] for e in labels.values())),
                   "revised_verdicts": sum(1 for e in labels.values() if e.get("history")),
                   "labelling_freeze_sha256": sha(HERE / "FREEZE-LABELLING.json"),
                   "scoring_inputs": {n: sha(HERE / n) for n in ("key.json", "review-cases.json", "owner-labels.yaml")}}
            (HERE / "LABELS-FREEZE.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
            print(json.dumps(out, indent=1))
        return 0
    if cmd == "summary":
        by = Counter()
        for c, e in labels.items():
            k = key[c]
            by[(k["set"], k.get("stratum") or "-", e["label"])] += 1
        for (s, st, l), n in sorted(by.items()):
            print(f"{s:4} {st:8} {l:22} {n}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
