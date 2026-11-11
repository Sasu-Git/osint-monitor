"""Continuity (FREEZE.md step 5): re-score iteration 1 or 2 on its own frozen inputs under the frozen lookup.

    PYTHONPATH=<iteration code> python rescore_iter12.py --db snap-20261102.db --countries <ab45312 checkout> \
        --out ../contract-eval-iter2/results-lookup-20261111.json

Executes the frozen ../contract-eval/evaluate.py (sha a922554753c9…, checked) with exactly one line changed: the ISO
lookup line gains lookup-overrides.json in front (asserted to occur once). Audit cases and acceptance cases are the
frozen ones (hashes checked). The historical results.json files are never written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEO = HERE.parent
FROZEN = {
    GEO / "contract-eval" / "evaluate.py": "a922554753c951701e75b27c9879a9549a79269f8f4905fc53296ce3f0fb5712",
    GEO / "contract-eval" / "audit-cases.json": "c11e52a5d0f1ec82bfac40f3d2814f9b421aa43e6f71ad68de534e459e48846f",
    GEO / "acceptance-cases.yaml": "92a30dd268239b2c9e5ce8c0878ccdf35e33a5f598d73efd112d74a4ecca3898",
}
SNAPSHOT_SHA = "b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40"
OLD = "iso = lambda c: None if c is None else DISPUTED_ISO.get(c) or index.of_place(c)"
NEW = "iso = lambda c: None if c is None else _LOOKUP_OVERRIDES.get(c) or DISPUTED_ISO.get(c) or index.of_place(c)"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--countries", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    for p, h in FROZEN.items():
        if sha(p) != h:
            sys.exit(f"frozen input changed: {p}")
    if sha(a.db) != SNAPSHOT_SHA:
        sys.exit("snapshot hash differs from the frozen 2026-11-02 snapshot")
    if a.out.name == "results.json":
        sys.exit("refusing to overwrite a historical results.json")
    src = (GEO / "contract-eval" / "evaluate.py").read_text(encoding="utf-8")
    if src.count(OLD) != 1:
        sys.exit("the lookup line is not present exactly once")
    src = src.replace(OLD, NEW)
    overrides = json.loads((HERE / "lookup-overrides.json").read_text(encoding="utf-8"))["overrides"]
    sys.argv = ["evaluate.py", "--db", str(a.db), "--audit", str(GEO / "contract-eval" / "audit-cases.json"),
                "--acceptance", str(GEO / "acceptance-cases.yaml"), "--countries", str(a.countries),
                "--out", str(a.out)]
    exec(compile(src, str(GEO / "contract-eval" / "evaluate.py"), "exec"),
         {"__name__": "__main__", "_LOOKUP_OVERRIDES": overrides})


if __name__ == "__main__":
    main()
