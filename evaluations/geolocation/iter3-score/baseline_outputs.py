"""Iteration 3 scoring, run step 1: the map baselines' country per sample case, from audit.py outputs. Read-only.

    python baseline_outputs.py --system B0 --audit audit-all-20261105.json --out outputs/B0.json
    python baseline_outputs.py --system B1 --audit audit-aliases-20261105.json --out outputs/B1.json

The map gives the stored point's country (point_country) when it shows the point (shown), else NONE.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE.parent / "iter3-sample" / "manifest.json"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--system", required=True)
    ap.add_argument("--audit", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    audit = {r["development_id"]: r for r in json.loads(a.audit.read_text(encoding="utf-8"))}
    ids = [c["development_id"] for c in json.loads(MANIFEST.read_text(encoding="utf-8"))["cases"]]
    rows = {}
    for eid in ids:
        r = audit[eid]
        rows[str(eid)] = {"country": (r.get("point_country") or "NONE") if r["shown"] else "NONE",
                          "shown": r["shown"], "point_country": r.get("point_country"),
                          "frontend_reason": r.get("frontend_reason")}
    out = {"system": a.system, "audit_sha256": hashlib.sha256(a.audit.read_bytes()).hexdigest(), "cases": rows}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(a.system, sum(1 for r in rows.values() if r["country"] != "NONE"), "of", len(rows), "shown")


if __name__ == "__main__":
    main()
