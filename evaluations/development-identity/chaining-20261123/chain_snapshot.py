"""Part 1 (prevalence of chaining) and the snapshot side of Part 2 (what each illustrative guard would block).
Read-only: verifies the snapshot sha256, copies it with the sqlite backup API into a temp dir, opens the copy
query_only.  Usage: python chain_snapshot.py <snapshot.db> <expected sha256> <out.json>
Definitions (fixed before any result was seen):
  members ordered by (added_at, item id); first run = members with the earliest member's added_run_id (members with
  added_at within 5 min of the first, when that run id is NULL); links = development_segmentation.compatible_link
  (the exact runtime pair test) restricted to members of the same Development.
  chain depth: parent = most cosine-similar compatibly-linked EARLIER member (earlier in the order); no earlier
  link = depth 0.  Reported per Development: max depth, and median item depth.
  late member: added_at > first added_at + 3 days.  Centroid of the first run = mean of its member vectors.
  no-direct-link share: members outside the first run with no compatible link to any first-run member.
Guard simulation (snapshot): runs are processed in time order; a run's items attach against the members accepted
before that run (as reconcile does); the first run is founders, never guarded.  Guard families: size (accepted
members >= S), age (item added_at - first added_at > N h), centroid (cos to centroid of accepted < c),
founder-link (needs a link to an accepted member added within K h of the first).  An item with no passing link
is detached (not an accepted member; later items cannot link through it).
"""
import hashlib
import json
import os
import sqlite3
import statistics
import sys
import tempfile
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")

SWEEP = {"size": [4, 6, 8, 12, 25, 50, 100, 200], "age_h": [6, 12, 24, 36, 72, 168, 336],
         "centroid": [0.40, 0.45, 0.50, 0.55], "founder_k_h": [6, 12, 24, 36, 72, 168]}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pq(xs, qs=(0, .05, .25, .5, .75, .9, .95, .99, 1)):
    xs = sorted(xs)
    if not xs:
        return {}
    return {f"p{int(q * 100)}": round(float(xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))]), 4) for q in qs}


def unit(v):
    n = np.linalg.norm(v)
    return v / n if n else v


def main(snap, want, out):
    from sqlalchemy import create_engine, event, text
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.processors.development_segmentation import compatible_link, segment_items

    got = sha256(snap)
    if got != want:
        sys.exit(f"HASH MISMATCH {got} != {want}")
    tmp = Path(tempfile.mkdtemp(prefix="chain-snap-"))
    copy = tmp / "copy.db"
    src = sqlite3.connect(f"file:{Path(snap).as_posix()}?mode=ro", uri=True)
    dst = sqlite3.connect(copy)
    src.backup(dst)
    dst.close()
    src.close()
    engine = create_engine(f"sqlite:///{copy.as_posix()}")

    @event.listens_for(engine, "connect")
    def _q(c, _):
        c.execute("PRAGMA query_only=ON")

    session = sessionmaker(bind=engine)()
    cfg = load_event_grouping_config().development_segmentation

    rows = session.execute(text("select event_id, item_id, added_at, added_run_id from event_items")).all()
    by_ev = defaultdict(list)
    for e, i, a, r in rows:
        by_ev[e].append((datetime.fromisoformat(str(a)), i, r))
    devs = {e: sorted(v) for e, v in by_ev.items() if len(v) >= 3}
    summaries = dict(session.execute(text("select id, summary from events")).all())
    all_ids = sorted({i for v in devs.values() for _, i, _ in v})
    print(len(devs), "developments >=3 items;", len(all_ids), "items", flush=True)
    seg = {}
    t0 = time.time()
    for k in range(0, len(all_ids), 4000):
        seg.update(segment_items(session, all_ids[k:k + 4000], cfg))
    print("segment items", len(seg), round(time.time() - t0), "s", flush=True)

    results, sims = {}, {}
    t0 = time.time()
    for n_done, (e, mem) in enumerate(sorted(devs.items(), key=lambda kv: len(kv[1]))):
        mem = [m for m in mem if m[1] in seg]
        if len(mem) < 3:
            continue
        ids = [m[1] for m in mem]
        n = len(ids)
        V = np.stack([unit(seg[i].vector) for i in ids])
        C = V @ V.T
        # link matrix: exact runtime pair test, prefiltered by the cosine condition _linked applies cross-source
        L = np.zeros((n, n), dtype=bool)
        for a in range(n):
            for b in range(a + 1, n):
                same_src = seg[ids[a]].source == seg[ids[b]].source
                if not same_src and C[a, b] < 0.53:
                    continue
                if compatible_link(seg[ids[a]], seg[ids[b]], cfg):
                    L[a, b] = L[b, a] = True
        added = [m[0] for m in mem]
        runs = [m[2] for m in mem]
        first_t = added[0]
        first_run = {k for k in range(n) if (runs[0] is not None and runs[k] == runs[0])
                     or (runs[0] is None and (added[k] - first_t).total_seconds() <= 300)}
        depth = [0] * n
        for k in range(1, n):
            cand = [j for j in range(k) if L[k, j]]
            if cand:
                depth[k] = depth[max(cand, key=lambda j: C[k, j])] + 1
        fr = sorted(first_run)
        cen = unit(V[fr].mean(axis=0))
        late = [k for k in range(n) if (added[k] - first_t).total_seconds() > 3 * 86400]
        late_cos = [float(V[k] @ cen) for k in late]
        rest = [k for k in range(n) if k not in first_run]
        nolink = [k for k in rest if not L[k, fr].any()]
        nolink_late = [k for k in late if not L[k, fr].any()]
        span = (added[-1] - first_t).total_seconds() / 86400
        results[e] = {
            "event_id": e, "summary": (summaries.get(e) or "")[:90], "size": n, "span_days": round(span, 3),
            "first_run_size": len(fr), "chain_depth_max": max(depth), "chain_depth_median": statistics.median(depth),
            "late_members": len(late),
            "late_median_cos_first_run_centroid": round(statistics.median(late_cos), 4) if late_cos else None,
            "members_outside_first_run": len(rest),
            "no_direct_link_to_first_run_share": round(len(nolink) / len(rest), 4) if rest else None,
            "late_no_direct_link_to_first_run_share": round(len(nolink_late) / len(late), 4) if late else None,
        }
        # guard simulation: runs in time order against the members accepted before the run
        groups = []
        for k in range(n):
            if k in first_run:
                continue
            key = runs[k] if runs[k] is not None else ("t", added[k].replace(second=0, microsecond=0))
            if groups and groups[-1][0] == key:
                groups[-1][1].append(k)
            else:
                groups.append((key, [k]))
        families = [("none", 0)] + [(f, v) for f, vs in SWEEP.items() for v in vs]
        sim = {}
        for fam, val in families:
            acc = list(fr)
            csum = V[fr].sum(axis=0)
            blocked = no_link = 0
            for _, ks in groups:
                accepted_now = list(acc)
                cen_now = unit(csum)
                add_now = []
                for k in ks:
                    links = [j for j in accepted_now if L[k, j]]
                    if not links:
                        no_link += 1
                        continue
                    ok = True
                    if fam == "size":
                        ok = len(accepted_now) < val
                    elif fam == "age_h":
                        ok = (added[k] - first_t).total_seconds() <= val * 3600
                    elif fam == "centroid":
                        ok = float(V[k] @ cen_now) >= val
                    elif fam == "founder_k_h":
                        ok = any((added[j] - first_t).total_seconds() <= val * 3600 for j in links)
                    if ok:
                        add_now.append(k)
                    else:
                        blocked += 1
                acc += add_now
                for k in add_now:
                    csum = csum + V[k]
            sim["none" if fam == "none" else f"{fam}={val}"] = {
                "final_size": len(acc), "blocked_by_guard": blocked, "no_accepted_link": no_link}
        sims[e] = sim
        if (n_done + 1) % 100 == 0 or n >= 300:
            print(n_done + 1, "devs done; last size", n, round(time.time() - t0), "s", flush=True)

    per = list(results.values())
    R = {"snapshot_sha256": got, "developments_ge3": len(per), "items_in_them": sum(r["size"] for r in per)}
    keys = ("size", "span_days", "chain_depth_max", "chain_depth_median", "late_median_cos_first_run_centroid",
            "no_direct_link_to_first_run_share", "late_no_direct_link_to_first_run_share")
    R["distributions"] = {k: pq([r[k] for r in per if r[k] is not None]) for k in keys}
    R["n_with_value"] = {k: sum(1 for r in per if r[k] is not None) for k in keys}
    R["d398"] = results.get(398)
    R["top20_by_size"] = sorted(per, key=lambda r: -r["size"])[:20]
    like = {}
    d398 = results.get(398)
    if d398:
        for key in keys:
            v0 = d398[key]
            if v0 is None:
                continue
            direction = "le" if key.startswith("late_median_cos") else "ge"
            vals = [r[key] for r in per if r[key] is not None]
            if direction == "ge":
                grid = {f"{f:g}x D398 ({v0 * f:.4g})": sum(1 for x in vals if x >= v0 * f) for f in (1.0, 0.5, 0.25, 0.1)}
            else:
                grid = {f"<= D398 +{dv:g} ({v0 + dv:.3g})": sum(1 for x in vals if x <= v0 + dv) for dv in (0.0, 0.1, 0.2)}
            like[key] = {"d398_value": v0, "direction": direction, "n_with_value": len(vals), "count_at_grid": grid}
    R["look_like_d398"] = like
    tot = {}
    for e, sim in sims.items():
        base = sim["none"]
        for k, v in sim.items():
            t = tot.setdefault(k, {"developments_changed": 0, "blocked_by_guard": 0, "no_accepted_link": 0,
                                   "non_founder_items_attached": 0})
            t["blocked_by_guard"] += v["blocked_by_guard"]
            t["no_accepted_link"] += v["no_accepted_link"]
            t["non_founder_items_attached"] += v["final_size"] - results[e]["first_run_size"]
            t["developments_changed"] += int(v["final_size"] != base["final_size"])
    R["guard_sim_all_developments_ge3"] = tot
    R["guard_sim_d398"] = sims.get(398)
    R["sweep_points_note"] = "every value is an illustrative sweep point, not a proposal"
    Path(out).write_text(json.dumps(R, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8", newline="\n")
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:4])
