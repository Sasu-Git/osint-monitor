"""Freeze the new parts of the Development-admission development dataset (selection only; no labels, no measurement).

    python build_dataset.py --db data/eval/snapshot-20261027-forensic.db \
        --blast ../../forensics/giant-developments/blast-radius.csv --out .

Opens the snapshot read-only (sqlite3, mode=ro). Writes, with fixed seeds:
- relay-set.json: the 24 relay-signature Developments (forensic categories A and B) and their member item ids;
- giant-label-sample.json: per giant Development, its founder items and a stratified sample of later members for
  owner labelling (SAME_AS_FOUNDER_OCCURRENCE / DIFFERENT / AMBIGUOUS); strata are attachment-time quartiles;
- large-occurrence-candidates.json: the largest Developments without the relay signature, with a sample of members
  each, for owner review as possible legitimate large single occurrences (SAME controls);
- small-controls.json: a random sample of corroborated Developments with 2-5 members (stability controls);
- FREEZE.json: sha256 of every input and output.
Nothing here reads a sealed holdout or changes pipeline behaviour.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sqlite3
from pathlib import Path

SEED = 20261027
GIANTS = [398, 397, 449, 639, 399, 626, 514, 182]
PER_GIANT = 16                # 4 attachment-time quartiles x 4
LARGE_CANDIDATES = 6
PER_LARGE = 8
SMALL_CONTROLS = 60


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--blast", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    db = sqlite3.connect(f"file:{a.db.resolve().as_posix()}?mode=ro", uri=True)
    rng = random.Random(SEED)
    rows = list(csv.DictReader(open(a.blast, encoding="utf-8")))
    sig = {int(r["event_id"]): set(filter(None, r["signatures"].split(";"))) for r in rows}
    size = {int(r["event_id"]): int(r["size"]) for r in rows}

    def members(eid):
        return [dict(item_id=i, added_at=t, run=r, title=ti, source=s, published_at=p) for i, t, r, ti, s, p in db.execute(
            """select ei.item_id, ei.added_at, ei.added_run_id, ri.title, so.name, ri.published_at
               from event_items ei join raw_items ri on ri.id = ei.item_id join sources so on so.id = ri.source_id
               where ei.event_id = ? order by ei.added_at, ei.item_id""", (eid,))]

    relay = sorted((e for e, s in sig.items() if {"long", "chain"} <= s), key=lambda e: -size[e])
    relay_out = {"rule": "forensic signatures long + chain (categories A and B of blast-radius.csv)",
                 "developments": [{"event_id": e, "signatures": sorted(sig[e]), "item_ids": [m["item_id"] for m in members(e)]}
                                  for e in relay]}

    giant_out = []
    for e in GIANTS:
        ms = members(e)
        first = ms[0]["run"]
        founders = [m for m in ms if m["run"] == first]
        later = [m for m in ms if m["run"] != first]
        q = len(later) / 4
        sample = []
        for k in range(4):
            stratum = later[int(k * q):int((k + 1) * q)]
            sample += [dict(m, stratum=f"Q{k + 1}") for m in rng.sample(stratum, min(PER_GIANT // 4, len(stratum)))]
        giant_out.append({"event_id": e, "founders": founders, "sample": sample})

    relay_set = set(relay)
    large = [e for e in sorted(size, key=lambda e: -size[e])
             if e not in relay_set and e not in GIANTS and size[e] >= 20][:LARGE_CANDIDATES]
    large_out = []
    for e in large:
        ms = members(e)
        large_out.append({"event_id": e, "size": size[e], "signatures": sorted(sig[e]),
                          "sample": rng.sample(ms, min(PER_LARGE, len(ms)))})

    small = sorted(e for e in size if 2 <= size[e] <= 5)
    small_out = {"rule": f"random {SMALL_CONTROLS} corroborated Developments with 2-5 members, seed {SEED}",
                 "developments": [{"event_id": e, "item_ids": [m["item_id"] for m in members(e)]}
                                  for e in sorted(rng.sample(small, SMALL_CONTROLS))]}

    a.out.mkdir(parents=True, exist_ok=True)
    outputs = {"relay-set.json": relay_out, "giant-label-sample.json": giant_out,
               "large-occurrence-candidates.json": large_out, "small-controls.json": small_out}
    for name, data in outputs.items():
        (a.out / name).write_text(json.dumps(data, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    freeze = {"seed": SEED, "snapshot": str(a.db), "snapshot_sha256": hashlib.sha256(a.db.read_bytes()).hexdigest(),
              "blast_radius_csv_sha256": sha(a.blast), "script_sha256": sha(Path(__file__)),
              "outputs": {n: sha(a.out / n) for n in outputs}}
    (a.out / "FREEZE.json").write_text(json.dumps(freeze, indent=1), encoding="utf-8")
    print(f"relay {len(relay)} ({sum(len(d['item_ids']) for d in relay_out['developments'])} items); "
          f"giant sample {sum(len(g['sample']) for g in giant_out)} + founders {sum(len(g['founders']) for g in giant_out)}; "
          f"large candidates {large} ; small controls {SMALL_CONTROLS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
