"""Regression check on the Phase 2 identity holdout (already scored once and closed; owner request 2026-10-09).

    python evaluations/identity/defects/holdout_regression.py --label NAME   # run with the code tree to check

Replays the Phase 2 holdout window with the code on sys.path and scores the 30 holdout cases (identity gold,
split holdout) with the same scorer as the one-time run. Writes runs/phase2-holdout-regression-NAME.json. It never
touches runs/phase2-holdout.json or the freeze record, and it does not read the sealed multilingual identity holdout
or the relation holdout.
"""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
IDN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(IDN / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import yaml  # noqa: E402


def main() -> int:
    import replay_current
    from phase2_baseline import score
    from score_identity import fmt, totals
    label = sys.argv[sys.argv.index("--label") + 1]
    manifest = yaml.safe_load((IDN / "manifest.yaml").read_text(encoding="utf-8"))
    gold = {k: v for k, v in yaml.safe_load((IDN / "gold" / "identity-gold.yaml").read_text(encoding="utf-8")).items()
            if v["split"] == "holdout"}
    results = []
    for w in manifest["windows"]:
        if w["split"] == "holdout":
            results.append(score(replay_current.replay(w), gold))
    out = IDN / "runs" / f"phase2-holdout-regression-{label}.json"
    out.write_text(json.dumps({"label": label, "windows": results}, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8", newline="\n")
    t = totals(results)
    for k, v in t.items():
        if k != "error_classes":
            print(f"{k:30s} {fmt(v)}")
    print("ledger:", sorted((e["case"], e["failure"]) for r in results for e in r["ledger"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
