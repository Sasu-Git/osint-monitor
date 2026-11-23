"""Read-only Development-identity diagnostic of one Development (default D398).

Usage: python d398_diagnostic.py <snapshot.db> <expected sha256> <out.json> [event_id]
Opens the snapshot read-only, copies it with the sqlite backup API into a temp dir, opens the copy with
PRAGMA query_only=ON. Evidence only; no verdicts. The pairwise component construction follows
evaluations/development-identity/mixed-flag-20261114/mixed_flag_diagnostic.py (branch eval/mixed-flag-diagnostic):
connected components over segmentation compatible_link pairs, all items, report-only not applied here.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import statistics
import sys
import tempfile
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def pdt(s):
    return None if s is None else datetime.fromisoformat(str(s))


def quant(xs, qs=(0, .05, .25, .5, .75, .95, 1)):
    xs = sorted(xs)
    if not xs:
        return {}
    return {f"q{int(q * 100)}": round(float(xs[min(len(xs) - 1, int(q * (len(xs) - 1)))]), 4) for q in qs}


def main(snap, want, out, eid=398):
    from sqlalchemy import create_engine, event, text
    from sqlalchemy.orm import sessionmaker, joinedload
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.core.database import RawItem, Entity, ItemEntity
    from osint_monitor.core.models import ClusterContext, ContextItem
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.classification.rules import RuleBasedClassifier
    from osint_monitor.processors.development_segmentation import (
        ACTOR_TYPES, LOCATION_TYPES, compatible_link, gazetteer, segment_items)
    from osint_monitor.processors.entity_resolver import normalise
    from osint_monitor.processors.language import item_language
    from osint_monitor.processors.clustering import LINK_SIMILARITY, MEMBER_SIMILARITY, MAX_LINK_HOURS
    import networkx as nx

    got = sha256(snap)
    if got != want:
        sys.exit(f"HASH MISMATCH {got} != {want}")
    tmp = Path(tempfile.mkdtemp(prefix="d398diag-"))
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
    R = {"snapshot_sha256": got, "event_id": eid}

    ev = session.execute(text("select id, summary, event_type, location_name, lat, lon, region, first_reported_at, "
                              "last_updated_at, earliest_published_at, source_count, situation_id from events where id=:e"),
                         {"e": eid}).mappings().one()
    R["stored_event"] = {k: (str(v) if v is not None else None) for k, v in ev.items()}
    eis = session.execute(text("select item_id, similarity_score, added_at, added_run_id from event_items "
                               "where event_id=:e"), {"e": eid}).all()
    ids = sorted(r[0] for r in eis)
    ei = {r[0]: (r[1], pdt(r[2]), r[3]) for r in eis}
    raw = {r.id: r for r in session.query(RawItem).options(joinedload(RawItem.source)).filter(RawItem.id.in_(ids))}

    def sname(i):
        return raw[i].source.name if raw[i].source else None

    # ---------------- 1. size, spans, weekly, runs
    pubs = [raw[i].published_at for i in ids if raw[i].published_at]
    fets = [raw[i].fetched_at for i in ids if raw[i].fetched_at]
    R["1_size_span"] = {
        "item_count": len(ids), "items_without_published_at": len(ids) - len(pubs),
        "published_at": [str(min(pubs)), str(max(pubs))], "fetched_at": [str(min(fets)), str(max(fets))],
        "added_at": [str(min(v[1] for v in ei.values())), str(max(v[1] for v in ei.values()))],
        "items_also_in_other_events": session.execute(text(
            "select count(*) from event_items where item_id in (select item_id from event_items where event_id=:e) "
            "and event_id<>:e"), {"e": eid}).scalar(),
    }

    def week(d):
        y, w, _ = d.isocalendar()
        return f"{y}-W{w:02d}"
    R["1_added_per_week_by_added_at"] = dict(sorted(Counter(week(v[1]) for v in ei.values()).items()))
    R["1_published_per_week"] = dict(sorted(Counter(week(p) for p in pubs).items()))
    cut = datetime(2026, 11, 2, 23, 59, 59)
    R["1_items_added_by_2026-11-02"] = sum(1 for v in ei.values() if v[1] <= cut)
    R["1_items_added_after_2026-11-02"] = sum(1 for v in ei.values() if v[1] > cut)
    runs = Counter(v[2] for v in ei.values())
    runinfo = {r[0]: r[1:] for r in session.execute(text(
        "select id, kind, tier, started_at, code_sha, status from pipeline_runs"))}
    blank = [None] * 5
    per_run = sorted(({"run": r, "items": n, "kind": runinfo.get(r, blank)[0], "tier": runinfo.get(r, blank)[1],
                       "started_at": str(runinfo.get(r, blank)[2]), "code_sha": runinfo.get(r, blank)[3]}
                      for r, n in runs.items()), key=lambda x: -x["items"])
    R["1_runs"] = {"distinct_runs": len(runs), "items_per_run_distribution": dict(sorted(Counter(runs.values()).items())),
                   "top_10_runs": per_run[:10],
                   "runs_by_kind_tier": dict(Counter(f"{x['kind']}/{x['tier']}" for x in per_run)),
                   "items_by_code_sha": dict(Counter(runinfo.get(v[2], blank)[3] for v in ei.values()).most_common())}
    R["1_added_per_day"] = dict(sorted(Counter(str(v[1].date()) for v in ei.values()).items()))
    R["1_similarity_score"] = {"==1.0 (persist_clusters path)": sum(1 for v in ei.values() if v[0] == 1.0),
                               "<1.0 (pipeline near_different_source dedup path)": sum(1 for v in ei.values() if v[0] != 1.0)}

    # ---------------- 2. sources, language
    R["2_sources_top20"] = Counter(sname(i) for i in ids).most_common(20)
    R["2_distinct_sources"] = len({sname(i) for i in ids})
    lang = {i: item_language(sname(i), f"{raw[i].title or ''} {(raw[i].content or '')[:300]}") for i in ids}
    R["2_language"] = dict(Counter(lang.values()).most_common())
    R["2_dominant_language"] = Counter(lang.values()).most_common(1)[0][0]

    # ---------------- 3. rule classifier per item (single-item ClusterContext, as benchmark/replay.py does)
    clf = RuleBasedClassifier()
    types, doms = Counter(), Counter()
    for i in ids:
        r = raw[i]
        c, _ = clf.assess(ClusterContext(items=[ContextItem(title=r.title or "", excerpt=(r.content or "")[:1000],
                                                            source_name=sname(i) or "")]))
        types[c.event_type.value] += 1
        doms[c.event_domain.value] += 1
    R["3_item_event_type_rules"] = dict(types.most_common())
    R["3_item_event_domain_rules"] = dict(doms.most_common())
    R["3_stored_development_event_type"] = ev["event_type"]

    # ---------------- 4/5. principals, actor keys, places
    R["4_stored_principals"] = [dict(r._mapping) for r in session.execute(text(
        "select e.canonical_name, e.entity_type, ee.role, ee.actor_role from event_entities ee "
        "join entities e on e.id=ee.entity_id where ee.event_id=:e and ee.is_principal=1"), {"e": eid})]
    norm = ActorNormalizer.load()
    rows = session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type).join(
        Entity, Entity.id == ItemEntity.entity_id).filter(ItemEntity.item_id.in_(ids)).all()
    akeys, places, plkeys = defaultdict(set), defaultdict(set), defaultdict(set)
    geo = gazetteer(False)
    for iid, name, etype in rows:
        if etype in ACTOR_TYPES and (k := norm.key(name)):
            akeys[iid].add(k)
        if etype in LOCATION_TYPES and name:
            plkeys[iid].add(normalise(name))
            place = geo.canonical(normalise(name))
            surface = norm.surface(name) or ""
            if place and not geo.is_country(place) and norm.represents(surface) == surface:
                places[iid].add(place)
    R["4_top20_actor_keys_items_with_key"] = Counter(k for s in akeys.values() for k in s).most_common(20)
    R["4_items_with_no_actor_key"] = sum(1 for i in ids if not akeys.get(i))
    R["5_stored_location"] = {"location_name": ev["location_name"], "lat": ev["lat"], "lon": ev["lon"]}
    R["5_top20_specific_places_items_with_place"] = Counter(p for s in places.values() for p in s).most_common(20)
    R["5_items_with_no_specific_place"] = sum(1 for i in ids if not places.get(i))
    R["5_top20_all_location_keys"] = Counter(p for s in plkeys.values() for p in s).most_common(20)
    R["5_distinct_specific_places"] = len({p for s in places.values() for p in s})

    # ---------------- 6. segment items, full pairwise compatible_link
    t0 = time.time()
    seg = segment_items(session, set(ids), cfg)
    R["6_segment_items_built"] = len(seg)
    R["6_segment_items_seconds"] = round(time.time() - t0, 1)
    sid = [i for i in ids if i in seg]
    n = len(sid)
    pos = {i: k for k, i in enumerate(sid)}
    V = np.array([seg[i].vector for i in sid], dtype=np.float64)
    Vn = V / np.maximum(np.linalg.norm(V, axis=1, keepdims=True), 1e-12)
    COS = Vn @ Vn.T
    t0 = time.time()
    A = np.zeros((n, n), dtype=bool)
    for a in range(n):
        sa = seg[sid[a]]
        for b in range(a + 1, n):
            if compatible_link(sa, seg[sid[b]], cfg):
                A[a, b] = A[b, a] = True
    R["6_pairs_evaluated"] = n * (n - 1) // 2
    R["6_pair_seconds"] = round(time.time() - t0, 1)
    R["6_compatible_pairs"] = int(A.sum() // 2)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in zip(*np.nonzero(np.triu(A))):
        parent[find(int(a))] = find(int(b))
    comps = defaultdict(list)
    for k in range(n):
        comps[find(k)].append(sid[k])
    cl = sorted(comps.values(), key=lambda c: -len(c))
    sizes = [len(c) for c in cl]
    R["6_components"] = {"n_components": len(cl), "sizes_top30": sizes[:30], "singletons": sum(1 for s in sizes if s == 1),
                         "components_size_ge2": sum(1 for s in sizes if s >= 2),
                         "size_histogram": dict(sorted(Counter(sizes).items(), reverse=True)),
                         "items_not_scored": len(ids) - n}
    R["6_compatible_degree"] = quant(A.sum(axis=1).tolist())

    # ---------------- 7. examples
    def ex(c, k=8):
        c = sorted(c, key=lambda i: (seg[i].published_at or datetime.max, i))
        idx = sorted({int(round(x)) for x in np.linspace(0, len(c) - 1, k)})
        return [{"id": i, "published_at": str(seg[i].published_at), "source": sname(i), "title": seg[i].title}
                for i in (c[x] for x in idx)]
    top = min(3, len(cl))
    R["7_examples"] = [{"component_rank": r + 1, "size": len(cl[r]),
                        "published_span": [str(min(seg[i].published_at for i in cl[r])),
                                           str(max(seg[i].published_at for i in cl[r]))],
                        "headlines_evenly_spaced_by_date": ex(cl[r])} for r in range(top)]
    R["7_component_top_actor_keys_and_places"] = [
        {"component_rank": r + 1,
         "actors": Counter(k for i in cl[r] for k in akeys.get(i, ())).most_common(6),
         "places": Counter(p for i in cl[r] for p in places.get(i, ())).most_common(6)} for r in range(top)]

    # ---------------- 8. attachment mechanism
    runs_order = sorted({ei[i][2] for i in sid}, key=lambda r: (min(ei[i][1] for i in sid if ei[i][2] == r), r))
    batch_of = {r: k for k, r in enumerate(runs_order)}
    bidx = np.array([batch_of[ei[i][2]] for i in sid])
    addt = [ei[i][1] for i in sid]
    seed = np.nonzero(bidx == bidx.min())[0]
    R["8_first_batch"] = {"run": runs_order[0], "items": int(len(seed)), "added_at": str(addt[int(seed[0])]),
                          "titles": [seg[sid[int(k)]].title for k in seed][:10]}
    order = sorted(range(n), key=lambda k: (batch_of[ei[sid[k]][2]], addt[k], sid[k]))
    rank = {k: r for r, k in enumerate(order)}
    seedv = Vn[[int(k) for k in seed]].mean(axis=0)
    seedv = seedv / max(np.linalg.norm(seedv), 1e-12)
    rows8 = []
    for r, k in enumerate(order):
        prior = [m for m in order[:r] if bidx[m] < bidx[k]]     # members added in earlier runs
        if not prior:
            continue
        P = np.array(prior)
        pc = Vn[P].mean(axis=0)
        pc = pc / max(np.linalg.norm(pc), 1e-12)
        linked = P[A[k, P]]
        row = {"id": sid[k], "week": week(addt[k]), "batch": int(bidx[k]), "n_prior": len(prior),
               "max_cos_prior": float(COS[k, P].max()), "cos_prior_centroid": float(Vn[k] @ pc),
               "cos_seed_centroid": float(Vn[k] @ seedv), "max_cos_seed": float(COS[k, seed].max()),
               "n_compat_prior": int(len(linked)), "compat_seed": int(A[k, seed].sum())}
        if len(linked):
            best = int(linked[np.argmax(COS[k, linked])])
            row.update(best_linked_prior=sid[best], best_link_cos=float(COS[k, best]),
                       best_link_gap_h=abs((seg[sid[k]].published_at - seg[sid[best]].published_at).total_seconds()) / 3600)
        rows8.append(row)
    R["8_items_after_first_batch"] = len(rows8)

    def q(key, f=lambda r: True):
        return quant([r[key] for r in rows8 if key in r and f(r)])
    R["8_attach_summary"] = {
        "compat_link_to_>=1_earlier_member": sum(1 for r in rows8 if r["n_compat_prior"] >= 1),
        "compat_link_to_0_earlier_members": sum(1 for r in rows8 if r["n_compat_prior"] == 0),
        "compat_link_to_exactly_1_earlier_member": sum(1 for r in rows8 if r["n_compat_prior"] == 1),
        "compat_link_to_>=5_earlier_members": sum(1 for r in rows8 if r["n_compat_prior"] >= 5),
        "n_compat_prior_quantiles": q("n_compat_prior"),
        "best_link_cosine_quantiles": q("best_link_cos"),
        "best_link_gap_hours_quantiles": q("best_link_gap_h"),
        "max_cos_to_any_earlier_member_quantiles": q("max_cos_prior"),
        "cos_to_seed_centroid_quantiles": q("cos_seed_centroid"),
        "cos_to_earlier_centroid_quantiles": q("cos_prior_centroid"),
        "max_cos_to_any_seed_item_quantiles": q("max_cos_seed"),
        "cos_seed_centroid_below_MEMBER_SIMILARITY_0.45": sum(1 for r in rows8 if r["cos_seed_centroid"] < MEMBER_SIMILARITY),
        "cos_seed_centroid_below_LINK_SIMILARITY_0.53": sum(1 for r in rows8 if r["cos_seed_centroid"] < LINK_SIMILARITY),
        "max_cos_seed_below_0.53": sum(1 for r in rows8 if r["max_cos_seed"] < LINK_SIMILARITY),
        "compat_linked_to_a_seed_item": sum(1 for r in rows8 if r["compat_seed"] >= 1),
        "constants": {"LINK_SIMILARITY": LINK_SIMILARITY, "MEMBER_SIMILARITY": MEMBER_SIMILARITY,
                      "MAX_LINK_HOURS": MAX_LINK_HOURS},
    }
    byw = defaultdict(list)
    for r in rows8:
        byw[r["week"]].append(r)
    R["8_by_added_week"] = {w: {"items": len(v),
                                "median_cos_seed_centroid": round(statistics.median(x["cos_seed_centroid"] for x in v), 3),
                                "median_best_link_cos": (round(statistics.median(x["best_link_cos"] for x in v if "best_link_cos" in x), 3)
                                                         if any("best_link_cos" in x for x in v) else None),
                                "share_compat_link_to_seed": round(sum(1 for x in v if x["compat_seed"] >= 1) / len(v), 3),
                                "median_n_compat_prior": statistics.median(x["n_compat_prior"] for x in v)}
                            for w, v in sorted(byw.items())}
    byk = {pos[r["id"]]: r for r in rows8}
    depth = {}
    for k in order:
        r = byk.get(k)
        depth[k] = depth[pos[r["best_linked_prior"]]] + 1 if r and "best_linked_prior" in r else 0
    dv = [depth[k] for k in order]
    R["8_chain_depth_via_best_linked_earlier_member"] = {
        "max": max(dv), "quantiles": quant(dv), "depth0_including_unlinked": sum(1 for d in dv if d == 0),
        "histogram": dict(sorted(Counter(dv).items()))}

    def cn(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    chunks = [order[i:i + 200] for i in range(0, n, 200)]
    cents = [Vn[c].mean(axis=0) for c in chunks]
    R["8_centroid_drift_chunks_of_200_by_added_order"] = {
        "cos_each_chunk_centroid_to_first_chunk": [round(cn(cents[0], c), 3) for c in cents],
        "cos_each_chunk_centroid_to_previous_chunk": [round(cn(cents[i - 1], cents[i]), 3) for i in range(1, len(cents))]}
    ov = COS[np.triu_indices(n, 1)]
    R["8_all_pairs_cosine"] = {"quantiles": quant(ov.tolist()), "share_ge_0.53": round(float((ov >= LINK_SIMILARITY).mean()), 4),
                               "share_ge_0.45": round(float((ov >= MEMBER_SIMILARITY).mean()), 4)}
    allc = Vn.mean(axis=0)
    ca = [cn(Vn[k], allc) for k in range(n)]
    R["8_cos_to_overall_centroid"] = {"quantiles": quant(ca), "below_0.45": sum(1 for x in ca if x < MEMBER_SIMILARITY)}
    ea, eb = np.nonzero(np.triu(A))
    R["8_compat_edges_same_source_share"] = round(float(np.mean([seg[sid[a]].source == seg[sid[b]].source
                                                                 for a, b in zip(ea, eb)])), 4) if len(ea) else None
    R["8_batches"] = {"runs": len(runs_order), "runs_with_1_item": sum(1 for r in runs.values() if r == 1),
                      "runs_with_gt1_items": sum(1 for r in runs.values() if r > 1)}
    big = [pos[i] for i in cl[0]]
    bs = set(big)
    G = nx.Graph()
    G.add_nodes_from(big)
    for a in big:
        for b in np.nonzero(A[a])[0]:
            if int(b) > a and int(b) in bs:
                G.add_edge(a, int(b))
    conn = nx.is_connected(G)
    R["8_largest_component_graph"] = {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(),
                                      "articulation_points": len(list(nx.articulation_points(G))),
                                      "diameter": nx.diameter(G) if conn else None,
                                      "avg_shortest_path": round(nx.average_shortest_path_length(G), 2) if conn else None}
    outp = Path(out)
    outp.with_name("d398_attach_rows.json").write_text(json.dumps(rows8), encoding="utf-8")
    outp.write_text(json.dumps(R, indent=1, default=str, ensure_ascii=False), encoding="utf-8")
    print("wrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 398)
