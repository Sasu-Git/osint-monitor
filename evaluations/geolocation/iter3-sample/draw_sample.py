"""Draw the fresh blind geolocation sample for iteration 3 (owner ruling 2026-11-05, option b).

Frame: every Development with id > 1198 (created after the 2026-11-02 12:55Z audit snapshot) up to D1341, the max id
in the 2026-11-05 backup-API snapshot. Map status comes from the frozen audit script (evaluations/geolocation/2026-11-02/
audit.py on eval/soak-safe-20261102) run with the deployed-map code d06af11 on that snapshot:

    unmapped = not shown (hidden by the map, or no stored point)  -> all taken
    shown    = shown on the map                                   -> 100 - len(unmapped), allocated by dominant
                                                                     language, proportional, largest remainder

Dominant language: the language with the most member items in the audit's `languages` counts ('?' = source language
not declared); ties go to a declared language over '?', then to the alphabetically first code. Within a stratum: random.Random(SEED).sample over the
stratum's ids in ascending order, strata processed in sorted order.

    python draw_sample.py --audit audit-all-20261105.json --out manifest.json
"""
import argparse, json, random

SEED = 20261105
FIRST_NEW, LAST = 1199, 1341
SIZE = 100


def dominant(langs):
    return sorted(langs.items(), key=lambda kv: (-kv[1], kv[0] == "?", kv[0]))[0][0] if langs else "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rows = [r for r in json.load(open(a.audit, encoding="utf-8")) if FIRST_NEW <= r["development_id"] <= LAST]
    assert len(rows) == LAST - FIRST_NEW + 1, len(rows)
    unmapped = sorted(r["development_id"] for r in rows if not r["shown"])
    shown = {}
    for r in rows:
        if r["shown"]:
            shown.setdefault(dominant(r["languages"]), []).append(r["development_id"])

    quota_total = SIZE - len(unmapped)
    n_shown = sum(len(v) for v in shown.values())
    exact = {k: len(v) * quota_total / n_shown for k, v in shown.items()}
    quota = {k: int(x) for k, x in exact.items()}
    for k in sorted(exact, key=lambda k: (-(exact[k] - quota[k]), k))[: quota_total - sum(quota.values())]:
        quota[k] += 1

    rng = random.Random(SEED)
    picked = {k: sorted(rng.sample(sorted(shown[k]), quota[k])) for k in sorted(shown)}
    cases = [{"development_id": i, "stratum": "unmapped"} for i in unmapped]
    for k, ids in picked.items():
        cases += [{"development_id": i, "stratum": f"shown/{k}"} for i in ids]
    cases.sort(key=lambda c: c["development_id"])

    manifest = {
        "frame": {"first_id": FIRST_NEW, "last_id": LAST, "size": len(rows), "unmapped": len(unmapped),
                  "shown_by_language": {k: len(v) for k, v in sorted(shown.items())}},
        "allocation": {"unmapped": len(unmapped), **{f"shown/{k}": quota[k] for k in sorted(quota)}},
        "seed": SEED,
        "cases": cases,
    }
    json.dump(manifest, open(a.out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(manifest["frame"]), json.dumps(manifest["allocation"]), len(cases))


if __name__ == "__main__":
    main()
