"""Verify the relation holdout is unchanged since sealing (hashes only; prints no content).

    python evaluations/relations/scripts/check_sealed.py
"""
import hashlib
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sealed = yaml.safe_load((ROOT / "holdout" / "SEALED.yaml").read_text(encoding="utf-8"))
    bad = [p for p, h in sealed["files"].items()
           if not (ROOT / p).exists() or hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h]
    for p, h in sealed["scripts"].items():          # informational: the sealed cases stay as generated
        if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h:
            print("note:", p, "changed since sealing; holdout cases remain the sealed v1 output")
    present = {str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "holdout").rglob("*.json")}
    extra = sorted(present - set(sealed["files"]))
    for p in bad:
        print("CHANGED", p)
    for p in extra:
        print("UNSEALED FILE", p)
    print("seal intact" if not bad and not extra else "seal BROKEN")
    return 1 if bad or extra else 0


if __name__ == "__main__":
    sys.exit(main())
