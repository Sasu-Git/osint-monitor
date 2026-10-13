"""Score the coverage-recoverability review: per stratum, the share of sampled items the owner labelled SHOULD_JOIN.

    python score.py            (reads owner-labels.yaml, key.json, sample-manifest.json; prints markdown)

Recoverable rate = SHOULD_JOIN / labelled, with a Wilson 95% interval; AMBIGUOUS is reported apart and bounds the rate
(as if all ambiguous were not-join / join). The pool estimate scales the rate to the stratum's unsurfaced items.
"""
import json
import math
import sys
from collections import Counter
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent


def wilson(k, n, z=1.96):
    if not n:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main() -> int:
    key = json.loads((HERE / "key.json").read_text(encoding="utf-8"))
    pools = json.loads((HERE / "sample-manifest.json").read_text(encoding="utf-8"))["pool_sizes"]
    labels = yaml.safe_load((HERE / "owner-labels.yaml").read_text(encoding="utf-8")) or {}
    print("| stratum | pool | labelled | SHOULD_JOIN | SHOULD_NOT_JOIN | AMBIGUOUS | recoverable rate (95% CI) "
          "| with ambiguous as join | pool estimate |")
    print("|---|---|---|---|---|---|---|---|---|")
    for stratum in pools:
        got = Counter(labels[c]["label"] for c, k in key.items()
                      if k["stratum"] == stratum and (labels.get(c) or {}).get("label"))
        n, j, a = sum(got.values()), got["SHOULD_JOIN"], got["AMBIGUOUS"]
        lo, hi = wilson(j, n)
        rate = j / n if n else 0.0
        print(f"| {stratum} | {pools[stratum]} | {n} | {j} | {got['SHOULD_NOT_JOIN']} | {a} | "
              f"{rate:.0%} ({lo:.0%}–{hi:.0%}) | {(j + a) / n if n else 0:.0%} | "
              f"~{rate * pools[stratum]:.0f} ({lo * pools[stratum]:.0f}–{hi * pools[stratum]:.0f}) |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
