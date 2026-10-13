import json
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(sys.argv[1], encoding="utf-8"))
rows = d["rows"]
POLICY = ["never_viable_cluster", "structured_record", "commentary_analysis", "single_source_holdback"]
REVIEW = ["below_link_threshold", "segmentation_rejected", "cross_language_candidate", "other_ambiguous"]
ORDER = POLICY + REVIEW


def table(key, top=None, min_n=0):
    groups = defaultdict(Counter)
    for r in rows:
        groups[r[key]][r["reason"]] += 1
    items = sorted(groups.items(), key=lambda kv: -sum(kv[1].values()))
    if top:
        items = items[:top]
    print(f"\n## by {key}\n")
    print("| " + key + " | unsurfaced | policy | review | " + " | ".join(o.replace("_", " ") for o in ORDER) + " |")
    print("|---" * (len(ORDER) + 4) + "|")
    for k, c in items:
        n = sum(c.values())
        if n < min_n:
            continue
        pol, rev = sum(c[o] for o in POLICY), sum(c[o] for o in REVIEW)
        print(f"| {k} | {n} | {100 * pol / n:.0f}% | {100 * rev / n:.0f}% | " + " | ".join(str(c[o]) for o in ORDER) + " |")


table("lang")
table("kind")
for r in rows:
    r["period"] = "before 10-05 (22 sources)" if (r["day"] or "") < "2026-10-05" else "from 10-05 (52 sources)"
table("period")
table("day")
table("source", top=25)
segs = Counter()
for r in rows:
    if r["reason"] == "segmentation_rejected" and isinstance(r["detail"], dict):
        for g, n in r["detail"].items():
            segs[g] += 1
print("\nsegmentation guard involved (items):", dict(segs))
