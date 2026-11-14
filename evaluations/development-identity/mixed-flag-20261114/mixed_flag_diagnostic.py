"""Read-only diagnostic: how many stored Developments would the segmentation compatibility check call "mixed".

Usage: python mixed_flag_diagnostic.py <snapshot.db> <expected sha256> <out dir>
Opens the snapshot read-only, copies it with the sqlite backup API into a temp dir, opens the copy with
PRAGMA query_only=ON, computes connected components over compatible_link pairs per Development. Nothing is written
to the copy; membership/identity fingerprints are compared before and after.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import sqlite3
import sys
import tempfile
from collections import Counter
from pathlib import Path

SEED = 20261114
KNOWN = [49, 439, 447, 542, 810]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def components(ids, link):
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in itertools.combinations(ids, 2):
        if link(a, b):
            parent[find(a)] = find(b)
    comps = {}
    for i in ids:
        comps.setdefault(find(i), []).append(i)
    return list(comps.values())


def membership_fingerprint(con):
    h = hashlib.sha256()
    for q in ("select id, summary, situation_id from events order by id",
              "select event_id, item_id from event_items order by event_id, item_id"):
        for r in con.execute(q):
            h.update(repr(r).encode())
    return h.hexdigest()


def main(snap, want, out):
    from sqlalchemy import create_engine, event, text
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.core.database import RawItem
    from osint_monitor.processors.development_segmentation import compatible_link, headline_kind, segment_items
    from osint_monitor.processors.language import item_language

    got = sha256(snap)
    if got != want:
        sys.exit(f"HASH MISMATCH {got} != {want}")
    tmp = Path(tempfile.mkdtemp(prefix="mixeddiag-"))
    copy = tmp / "copy.db"
    src = sqlite3.connect(f"file:{Path(snap).as_posix()}?mode=ro", uri=True)
    dst = sqlite3.connect(copy)
    src.backup(dst)
    dst.close()
    src.close()
    ro = sqlite3.connect(f"file:{copy.as_posix()}?mode=ro", uri=True)
    fp_before = membership_fingerprint(ro)
    ro.close()

    engine = create_engine(f"sqlite:///{copy.as_posix()}")

    @event.listens_for(engine, "connect")
    def _q(c, _):
        c.execute("PRAGMA query_only=ON")

    session = sessionmaker(bind=engine)()
    cfg = load_event_grouping_config().development_segmentation

    members: dict[int, list[int]] = {}
    for eid, iid in session.execute(text("select event_id, item_id from event_items order by event_id, item_id")):
        members.setdefault(eid, []).append(iid)
    multi = {e: m for e, m in members.items() if len(m) >= 2}
    summaries = dict(session.execute(text("select id, summary from events")).all())
    print("developments with >=1 item", len(members), "with >=2 items", len(multi), flush=True)

    results = []
    eids = sorted(multi)
    CH = 200
    for s in range(0, len(eids), CH):
        chunk = eids[s:s + CH]
        ids = sorted({i for e in chunk for i in multi[e]})
        sitems = segment_items(session, ids, cfg)
        raw = {r.id: r for r in session.query(RawItem).filter(RawItem.id.in_(ids))}
        for e in chunk:
            its = [i for i in multi[e] if i in sitems]
            n_all = len(multi[e])
            if len(its) < 2:
                results.append({"id": e, "size": n_all, "scored": len(its), "skipped": True, "items": []})
                continue
            comps = components(its, lambda a, b: compatible_link(sitems[a], sitems[b], cfg))
            kinds = {i: headline_kind(sitems[i].title) for i in its}
            rep = [i for i in its if kinds[i] == "report"]
            rcomps = components(rep, lambda a, b: compatible_link(sitems[a], sitems[b], cfg)) if rep else []
            langs = Counter()
            for i in its:
                r = raw[i]
                sname = r.source.name if getattr(r, "source", None) else None
                langs[item_language(sname, f"{r.title or ''} {(r.content or '')[:300]}")] += 1
            comp_of = {i: k for k, c in enumerate(comps) for i in c}
            sizes = sorted((len(c) for c in comps), reverse=True)
            rsizes = sorted((len(c) for c in rcomps), reverse=True)
            results.append({
                "id": e, "size": n_all, "scored": len(its), "skipped": False,
                "dominant_language": langs.most_common(1)[0][0], "languages": dict(langs),
                "components": sizes, "report_components": rsizes, "n_report_items": len(rep),
                "V1": len(sizes) >= 2, "V2": sum(1 for x in sizes if x >= 2) >= 2,
                "V3": len(rsizes) >= 2, "V4": sum(1 for x in rsizes if x >= 2) >= 2,
                "items": [{"id": i, "comp": comp_of[i], "kind": kinds[i], "title": sitems[i].title,
                           "source": raw[i].source.name if getattr(raw[i], "source", None) else None}
                          for i in its],
            })
        print(f"{min(s + CH, len(eids))}/{len(eids)}", flush=True)

    scored = [r for r in results if not r["skipped"]]
    V = ["V1", "V2", "V3", "V4"]

    def band(n):
        return "2" if n == 2 else "3-5" if n <= 5 else "6+"

    def table(rs):
        return {"n": len(rs), **{v: sum(r[v] for r in rs) for v in V}}

    summary = {"overall": table(scored), "by_size": {}, "by_language": {}}
    for b in ("2", "3-5", "6+"):
        summary["by_size"][b] = table([r for r in scored if band(r["size"]) == b])
    for l in sorted({r["dominant_language"] for r in scored}):
        summary["by_language"][l] = table([r for r in scored if r["dominant_language"] == l])
    byid = {r["id"]: r for r in results}
    known = {}
    for k in KNOWN:
        r = byid.get(k)
        known[f"D{k}"] = None if r is None else (
            {"size": r["size"], "skipped": True} if r["skipped"] else
            {"size": r["size"], "components": r["components"], "report_components": r["report_components"],
             **{v: r[v] for v in V}, "summary": summaries.get(k)})
    rng = random.Random(SEED)
    v1_not_v2 = sorted(r["id"] for r in scored if r["V1"] and not r["V2"])
    v4 = sorted(r["id"] for r in scored if r["V4"])

    def samp(pool):
        return sorted(rng.sample(pool, min(15, len(pool))))

    s_a, s_b = samp(v1_not_v2), samp(v4)

    def detail(ids):
        return [{"id": i, "size": byid[i]["size"], "components": byid[i]["components"],
                 "report_components": byid[i]["report_components"], "items": byid[i]["items"]} for i in ids]

    session.close()
    engine.dispose()
    ro = sqlite3.connect(f"file:{copy.as_posix()}?mode=ro", uri=True)
    fp_after = membership_fingerprint(ro)
    ro.close()
    doc = {"input": str(snap), "sha256": got, "seed": SEED,
           "config": cfg.model_dump() if hasattr(cfg, "model_dump") else str(cfg),
           "developments_total": len(members), "developments_ge2": len(multi), "scored": len(scored),
           "skipped_lt2_embedded": len(results) - len(scored),
           "summary": summary, "known": known,
           "pool_sizes": {"V1_not_V2": len(v1_not_v2), "V4": len(v4)},
           "sample_V1_not_V2": detail(s_a), "sample_V4": detail(s_b),
           "read_only": {"membership_fingerprint_before": fp_before, "after": fp_after,
                         "unchanged": fp_before == fp_after, "query_only_pragma": True},
           "per_development": [{k: v for k, v in r.items() if k != "items"} for r in results]}
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(doc, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: doc[k] for k in ("scored", "skipped_lt2_embedded", "summary", "known", "pool_sizes", "read_only")},
                     indent=1, default=str))


if __name__ == "__main__":
    main(*sys.argv[1:4])
