"""Pair-matcher equivalence and performance harness (read-only on a snapshot).

The matcher under test is ProvenanceResolver._mark_syndicated_copies (processors/provenance/resolve.py): for each
item, in publication order, its normalised 400-character prefix is compared with every earlier item of another origin
by SequenceMatcher(None, prefix, other_prefix, autojunk=False).ratio() >= syndication_similarity (0.95); the first
match marks the item a derivative copy.

Variants (pre-registered 2026-11-02, before any variant was run):
  P0  current code, unchanged.
  P1  before ratio(): skip the pair when SequenceMatcher(...).quick_ratio() < threshold.
  P2  before constructing SequenceMatcher: skip the pair when 2*m/(len(a)+len(b)) < threshold, where m is the size of
      the multiset intersection of the two prefixes' characters (precomputed Counter per prefix). m is exactly the
      `matches` that quick_ratio() counts, and the bound is computed with the same expression as difflib's
      _calculate_ratio, so P2 skips exactly the pairs P1 skips, without the per-pair SequenceMatcher set-up.
  impl  whatever the checked-out code does (no patch): used to verify the implementation branch.

Why P1/P2 cannot change a decision: ratio() = 2*M/T where M is the total size of the matching blocks, and every
matching block character is matched to a distinct equal character of the other string, so M <= m (the multiset
intersection); same T, and float division by the same T is monotone. So bound < threshold implies ratio() <
threshold: a skipped pair is one ratio() would reject. Pairs are visited in the same order and the loop still stops
at the first ratio() >= threshold, so the first accepted earlier item (and hence origin and derived_from) is the
same. The harness checks this empirically anyway, against frozen P0 outputs.

    python harness.py freeze  --db <snapshot> --out <dir>     # select benchmark, P0 pair log + outputs, timings
    python harness.py run     --db <snapshot> --out <dir> --variant P1|P2|impl [--full]
"""
from __future__ import annotations

import argparse, csv, hashlib, json, random, sqlite3, statistics as st, sys, time
from collections import Counter
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.models import EvidenceType
from osint_monitor.processors.provenance import resolve as R
from osint_monitor.processors.provenance.context import build_evidence
from osint_monitor.processors.provenance.confidence import assess_confidence

ORIG = R.ProvenanceResolver._mark_syndicated_copies
LOG: list | None = None          # pair log: (event, item_i, item_j, decision, ratio or bound)
EVENT = [None]
CLOCK = Counter()


def _variant(kind: str):
    """A copy of ProvenanceResolver._mark_syndicated_copies with an optional pre-check; logs every pair it decides."""
    def mark(self, items, resolved):
        t = time.perf_counter()
        cfg = self.config
        n = cfg.syndication_min_chars
        thr = cfg.syndication_similarity
        order = sorted(range(len(items)), key=lambda i: (items[i].published_at or datetime.min, i))
        earlier: list = []   # (prefix, index, Counter)
        for i in order:
            body = R._normalize(items[i].text)
            if len(body) < n:
                continue
            prefix = body[: n * 2]
            counts = Counter(prefix) if kind == "P2" else None
            prov = resolved[i]
            if prov.evidence_type not in (EvidenceType.PRIMARY, EvidenceType.COMMENTARY):
                for other_prefix, j, other_counts in earlier:
                    if resolved[j].origin == prov.origin:
                        continue
                    if kind == "P2":
                        m = sum((counts & other_counts).values())
                        bound = 2.0 * m / (len(prefix) + len(other_prefix))
                        if bound < thr:
                            if LOG is not None:
                                LOG.append((EVENT[0], items[i].item_id, items[j].item_id, "skip", bound))
                            continue
                    sm = SequenceMatcher(None, prefix, other_prefix, autojunk=False)
                    if kind == "P1":
                        q = sm.quick_ratio()
                        if q < thr:
                            if LOG is not None:
                                LOG.append((EVENT[0], items[i].item_id, items[j].item_id, "skip", q))
                            continue
                    r = sm.ratio()
                    if LOG is not None:
                        LOG.append((EVENT[0], items[i].item_id, items[j].item_id, "accept" if r >= thr else "reject", r))
                    if r >= thr:
                        origin = resolved[j].origin
                        resolved[i] = prov.model_copy(update={
                            "evidence_type": EvidenceType.DERIVATIVE, "origin": origin, "derived_from": origin,
                            "note": f"near-identical copy of {resolved[j].source_name}",
                        })
                        break
            earlier.append((prefix, i, counts))
        CLOCK["matcher"] += time.perf_counter() - t
    return mark


def _timed_impl(self, items, resolved):
    t = time.perf_counter()
    try:
        return CURRENT(self, items, resolved)
    finally:
        CLOCK["matcher"] += time.perf_counter() - t


CURRENT = ORIG


def install(variant: str, log: bool):
    global LOG, CURRENT
    LOG = [] if log else None
    if variant == "impl":                      # the checked-out code itself, only timed
        CURRENT = ORIG
        R.ProvenanceResolver._mark_syndicated_copies = _timed_impl
    else:
        R.ProvenanceResolver._mark_syndicated_copies = _variant(variant)


def serialize(assessment) -> str:
    return json.dumps(assessment.model_dump(mode="json"), sort_keys=True)


def run(db: str, event_ids: list[int], variant: str, log: bool, corroboration: bool) -> dict:
    """Provenance (and optionally corroboration) for each event under a variant. Returns outputs and timings."""
    install(variant, log)
    session = sessionmaker(bind=create_engine(f"sqlite:///file:{db}?mode=ro&uri=true"))()
    resolver = R.ProvenanceResolver()
    out = {"provenance": {}, "corroboration": {}, "timing": {}}
    if corroboration:
        from osint_monitor.processors.corroboration import compute_corroboration_score
    for eid in event_ids:
        EVENT[0] = eid
        evidence = build_evidence(session, eid)
        CLOCK.clear()
        t = time.perf_counter()
        assessment = assess_confidence(evidence, resolver)
        prov_s = time.perf_counter() - t
        matcher_s = CLOCK["matcher"]
        out["provenance"][eid] = serialize(assessment)
        rec = {"items": len(evidence), "provenance_s": prov_s, "matcher_s": matcher_s}
        if corroboration:
            CLOCK.clear()
            t = time.perf_counter()
            score = compute_corroboration_score(session, eid)
            rec["corroboration_s"] = time.perf_counter() - t
            rec["corroboration_matcher_s"] = CLOCK["matcher"]
            out["corroboration"][eid] = json.dumps(score, sort_keys=True, default=str)
        out["timing"][eid] = rec
    out["pairs"] = LOG or []
    return out


def select_benchmark(db: str) -> dict:
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    sizes = dict(c.execute("select e.id, count(ei.item_id) from events e join event_items ei on ei.event_id = e.id "
                           "group by e.id"))
    by_size = sorted(sizes, key=lambda e: (-sizes[e], e))
    rnd = random.Random(20261102)
    pick = lambda lo, hi, k: sorted(rnd.sample(sorted(e for e, n in sizes.items() if lo <= n <= hi), k))
    groups = {
        "largest_5": by_size[:5],
        "named": [398, 449, 514],
        "large_151_300": pick(151, 300, 2),
        "medium_51_150": pick(51, 150, 6),
        "medium_11_50": pick(11, 50, 8),
        "normal_2_10": pick(2, 10, 12),
    }
    ids = sorted({e for g in groups.values() for e in g})
    items = {e: [r[0] for r in c.execute("select item_id from event_items where event_id = ? order by item_id", (e,))]
             for e in ids}
    return {"groups": groups, "event_ids": ids, "items": items, "sizes": {e: sizes[e] for e in ids}}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_pairs(path: Path, pairs):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["event_id", "item_i", "item_j", "decision", "value"])
        for p in pairs:
            w.writerow([*p[:4], repr(p[4])])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["freeze", "run"])
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--variant", default="P0")
    ap.add_argument("--full", action="store_true", help="all Developments, with corroboration")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.cmd == "freeze":
        bench = select_benchmark(a.db)
        (out / "benchmark.json").write_text(json.dumps(bench, indent=1))
        res = run(a.db, bench["event_ids"], "P0", log=True, corroboration=True)
        write_pairs(out / "p0_pairs.csv", res["pairs"])
        (out / "p0_outputs.json").write_text(json.dumps({"provenance": res["provenance"],
                                                          "corroboration": res["corroboration"]}, sort_keys=True))
        (out / "p0_timing_logged.json").write_text(json.dumps(res["timing"], indent=1))
        print({f: sha(out / f) for f in ("benchmark.json", "p0_pairs.csv", "p0_outputs.json")})
        return
    bench = json.loads((out / "benchmark.json").read_text())
    ids = None
    tag = a.variant + ("-full" if a.full else "")
    if a.full:
        c = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
        ids = [r[0] for r in c.execute("select id from events order by id")]
    else:
        ids = bench["event_ids"]
    res = run(a.db, ids, a.variant, log=not a.full and a.variant != "P0", corroboration=True)
    (out / f"{tag}_timing.json").write_text(json.dumps(res["timing"], indent=1))
    (out / f"{tag}_outputs.json").write_text(json.dumps({"provenance": res["provenance"],
                                                          "corroboration": res["corroboration"]}, sort_keys=True))
    if res["pairs"]:
        write_pairs(out / f"{tag}_pairs.csv", res["pairs"])
    t = res["timing"].values()
    print(f"{tag}: {len(ids)} Developments, matcher {sum(r['matcher_s'] for r in t):.1f} s, provenance "
          f"{sum(r['provenance_s'] for r in t):.1f} s, corroboration {sum(r['corroboration_s'] for r in t):.1f} s")


if __name__ == "__main__":
    sys.exit(main())
