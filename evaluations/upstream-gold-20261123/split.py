"""Development / acceptance split of the frozen gold samples (owner ruling 2026-11-23: 40 / 60, fixed seed,
stratified), frozen while 0 labels existed. Development = confidence calibration; acceptance = scored once.

    python split.py        # writes topic/split.json and location/split.json (deterministic)
"""
import json
import random
from collections import defaultdict
from pathlib import Path

SEED, DEV_SHARE = 20261126, 0.40
HERE = Path(__file__).resolve().parent


def split(cases: list[dict], key) -> dict:
    strata = defaultdict(list)
    for c in cases:
        strata[key(c)].append(c["development_id"])
    dev, acc, per = [], [], {}
    for name in sorted(strata):
        ids = sorted(strata[name])
        random.Random(f"{SEED}:{name}").shuffle(ids)
        k = round(DEV_SHARE * len(ids))
        dev += ids[:k]
        acc += ids[k:]
        per[name] = {"n": len(ids), "development": k, "acceptance": len(ids) - k}
    return {"seed": SEED, "dev_share": DEV_SHARE, "stratified_by": None, "per_stratum": per,
            "development": sorted(dev), "acceptance": sorted(acc)}


for name in ("topic", "location"):
    m = json.loads((HERE / name / "manifest.json").read_text(encoding="utf-8"))
    roles = set(m.get("role_subset") or [])
    key = (lambda c: c["stratum"]) if name == "topic" else (lambda c: f"{c['stratum']}|roles={c['development_id'] in roles}")
    out = split(m["cases"], key)
    out["stratified_by"] = "sampling stratum" + (" x role-subset membership" if name == "location" else "")
    assert not set(out["development"]) & set(out["acceptance"])
    assert len(out["development"]) + len(out["acceptance"]) == len(m["cases"])
    (HERE / name / "split.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(name, len(out["development"]), "dev /", len(out["acceptance"]), "acc", out["per_stratum"])
