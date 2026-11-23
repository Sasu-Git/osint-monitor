"""Build per-Development report-item component evidence (report-components-v1).

Usage: python build_partition.py <snapshot.db> <expected sha256> <out.jsonl>
Algorithm reused from origin/eval/mixed-flag-diagnostic (mixed_flag_diagnostic.py, report-only components):
segment_items + development_segmentation config; keep headline_kind == "report"; connected components over
compatible_link pairs. Snapshot opened read-only, worked on via backup-API copy with query_only.
"""
from __future__ import annotations

import hashlib, itertools, json, sqlite3, sys, tempfile
from pathlib import Path

ALGO = "report-components-v1"


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


def main(snap, want, out):
    from sqlalchemy import create_engine, event, text
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.processors.development_segmentation import compatible_link, headline_kind, segment_items

    got = sha256(snap)
    if got != want:
        sys.exit(f"HASH MISMATCH {got} != {want}")
    tmp = Path(tempfile.mkdtemp(prefix="rcp-"))
    copy = tmp / "copy.db"
    src = sqlite3.connect(f"file:{Path(snap).as_posix()}?mode=ro", uri=True)
    dst = sqlite3.connect(copy)
    src.backup(dst)
    dst.close(); src.close()
    engine = create_engine(f"sqlite:///{copy.as_posix()}")

    @event.listens_for(engine, "connect")
    def _q(c, _):
        c.execute("PRAGMA query_only=ON")

    session = sessionmaker(bind=engine)()
    cfg = load_event_grouping_config().development_segmentation
    members = {}
    for eid, iid in session.execute(text("select event_id, item_id from event_items order by event_id, item_id")):
        members.setdefault(eid, []).append(iid)
    run_id = f"rcp-v1-20261123-{want[:8]}"
    eids = sorted(members)
    rows = []
    CH = 200
    for s in range(0, len(eids), CH):
        chunk = eids[s:s + CH]
        ids = sorted({i for e in chunk for i in members[e]})
        sitems = segment_items(session, ids, cfg)
        for e in chunk:
            rep = [i for i in members[e] if i in sitems and headline_kind(sitems[i].title) == "report"]
            rc = components(rep, lambda a, b: compatible_link(sitems[a], sitems[b], cfg)) if rep else []
            rows.append({"development_id": e, "algorithm_version": ALGO, "report_item_count": len(rep),
                         "component_sizes": sorted((len(c) for c in rc), reverse=True),
                         "snapshot_sha256": want, "run_id": run_id})
        print(f"{min(s + CH, len(eids))}/{len(eids)}", flush=True)
    session.close(); engine.dispose()
    rows.sort(key=lambda r: r["development_id"])
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")
    print("lines", len(rows), "out sha256", sha256(out))


if __name__ == "__main__":
    main(*sys.argv[1:4])
