"""Equivalence gate and complexity tables: a variant's outputs and pair log against the frozen P0.

    python compare.py <dir> P1 P2 impl        # dir holds p0_* and <variant>_* files written by harness.py

Gate per variant (0 allowed):
  - provenance / corroboration output differs from P0 for any Development (byte-identical JSON);
  - accepted pair set differs from P0's;
  - a skipped pair that P0 accepted;
  - for P1/P2: a full ratio() decision that differs from P0's on the same pair.
P1 vs P2: the skipped pair sets and the bound values must be identical (P2's bound is quick_ratio()).
"""
import csv, json, sys
from collections import defaultdict

d, variants = sys.argv[1], sys.argv[2:]


def pairs(path):
    out = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            out[(int(r["event_id"]), int(r["item_i"]), int(r["item_j"]))] = (r["decision"], float(r["value"]))
    return out


p0_out = json.load(open(f"{d}/p0_outputs.json"))
p0_pairs = pairs(f"{d}/p0_pairs.csv")
p0_acc = {k for k, v in p0_pairs.items() if v[0] == "accept"}
report = {}
logs = {}
for v in variants:
    out = json.load(open(f"{d}/{v}_outputs.json"))
    diffs = {kind: sorted(int(e) for e in p0_out[kind] if p0_out[kind][e] != out[kind].get(e))
             for kind in ("provenance", "corroboration")}
    missing = {kind: sorted(set(p0_out[kind]) ^ set(out[kind])) for kind in ("provenance", "corroboration")}
    r = {"provenance_mismatches": len(diffs["provenance"]), "corroboration_mismatches": len(diffs["corroboration"]),
         "missing_or_extra": sum(len(x) for x in missing.values()), "mismatched_events": diffs}
    try:
        vp = pairs(f"{d}/{v}_pairs.csv")
    except FileNotFoundError:
        vp = None
    if vp is not None:
        logs[v] = vp
        acc = {k for k, x in vp.items() if x[0] == "accept"}
        skipped = {k for k, x in vp.items() if x[0] == "skip"}
        full = {k: x for k, x in vp.items() if x[0] != "skip"}
        r.update({
            "pairs_decided": len(vp), "pairs_skipped": len(skipped), "pairs_full_ratio": len(full),
            "accepted_set_identical": acc == p0_acc, "accepted": len(acc),
            "skipped_but_p0_accepted": len(skipped & p0_acc),
            "skipped_not_in_p0_log": len(skipped - set(p0_pairs)),
            "full_ratio_decision_differs": sum(1 for k, x in full.items() if k in p0_pairs and p0_pairs[k][0] != x[0]),
            "full_ratio_value_differs": sum(1 for k, x in full.items() if k in p0_pairs and p0_pairs[k][1] != x[1]),
            "pair_set_identical_to_p0": set(vp) == set(p0_pairs),
            "max_skipped_bound": max((vp[k][1] for k in skipped), default=None),
            "skipped_bound_below_p0_ratio": sum(1 for k in skipped if k in p0_pairs and vp[k][1] < p0_pairs[k][1]),
        })
    report[v] = r
if "P1" in logs and "P2" in logs:
    s1 = {k: x[1] for k, x in logs["P1"].items() if x[0] == "skip"}
    s2 = {k: x[1] for k, x in logs["P2"].items() if x[0] == "skip"}
    report["P1_vs_P2"] = {"skip_sets_identical": set(s1) == set(s2),
                          "bound_values_identical": all(s1[k] == s2[k] for k in s1.keys() & s2.keys())}

# complexity by bucket (P2 log; P0 log for compared pairs)
bench = json.load(open(f"{d}/benchmark.json"))
sizes = {int(k): v for k, v in bench["sizes"].items()}
buckets = [(2, 10), (11, 50), (51, 150), (151, 300), (301, 10**6)]
if "P2" in logs:
    rows = defaultdict(lambda: [0, 0, 0, 0, 0])   # devs, possible pairs, P0 full comparisons, P2 skipped, P2 full
    for e, n in sizes.items():
        b = next(bk for bk in buckets if bk[0] <= n <= bk[1])
        rows[b][0] += 1
        rows[b][1] += n * (n - 1) // 2
    for (e, i, j), (dec, _) in p0_pairs.items():
        b = next(bk for bk in buckets if bk[0] <= sizes[e] <= bk[1]); rows[b][2] += 1
    for (e, i, j), (dec, _) in logs["P2"].items():
        b = next(bk for bk in buckets if bk[0] <= sizes[e] <= bk[1]); rows[b][3 if dec == "skip" else 4] += 1
    report["buckets"] = {f"{lo}-{hi if hi < 10**6 else '+'}": dict(zip(
        ["developments", "possible_pairs", "p0_full_comparisons", "p2_skipped", "p2_full_comparisons"], v))
        for (lo, hi), v in sorted(rows.items())}
json.dump(report, open(f"{d}/compare.json", "w"), indent=1)
print(json.dumps(report, indent=1))
