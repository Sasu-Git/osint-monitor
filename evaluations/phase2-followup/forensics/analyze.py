"""Analyse a reconstructed attachment history (reconstruct.py output): sub-stories, chaining, gravity over time,
attachment graph and counterfactual cuts. Read-only; descriptive, not a rule.

    python analyze.py --raw d398-raw.json --db COPY.db --code-wt ../osint-monitor-timing --out d398/

Sub-stories are a descriptive grouping used only to read the Development: average-linkage clustering of the
members' headline embeddings (the same model the segmentation guard uses), cut at SUBSTORY_DISTANCE. They are an
analyst's aid, not a gold label and not a proposed rule.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

SUBSTORY_DISTANCE = 0.45          # average-linkage cut on 1 - headline cosine
NEAR_THRESHOLD = 0.58             # accepted links with cosine in [0.53, 0.58) are "near the threshold"
STATE_LEVEL_PLACES = None         # filled from the gazetteer: countries and regions


def load_vectors(db: Path, code_wt: Path, ids: list[int]):
    os.environ["OSINT_DB_URL"] = f"sqlite:///{db.resolve().as_posix()}"
    sys.path.insert(0, str(code_wt.resolve()))
    from osint_monitor.core.database import RawItem, get_session
    from osint_monitor.processors.embeddings import embed_texts
    s = get_session()
    titles = {r.id: r.title or "" for r in s.query(RawItem.id, RawItem.title).filter(RawItem.id.in_(ids))}
    order = sorted(titles)
    return dict(zip(order, embed_texts([titles[i] for i in order])))


def substories(ids, hv):
    import numpy as np
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import pdist
    X = np.array([hv[i] / np.linalg.norm(hv[i]) for i in ids])
    if len(ids) < 2:
        return {ids[0]: 1} if ids else {}
    Z = linkage(pdist(X, "cosine"), "average")
    labels = fcluster(Z, SUBSTORY_DISTANCE, "distance")
    # renumber by first appearance (attachment order), so S1 is the seed's sub-story
    renum, out = {}, {}
    for i, lab in zip(ids, labels):
        renum.setdefault(lab, len(renum) + 1)
        out[i] = renum[lab]
    return out


def components(nodes, edges):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    seen, comps = set(), []
    for n in nodes:
        if n in seen:
            continue
        q, comp = deque([n]), []
        seen.add(n)
        while q:
            x = q.popleft()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        comps.append(comp)
    return sorted(comps, key=len, reverse=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--raw", type=Path, required=True)
    p.add_argument("--db", type=Path, required=True)
    p.add_argument("--code-wt", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--full", action="store_true", help="write the full deliverables (deep-dive case)")
    a = p.parse_args()
    raw = json.loads(a.raw.read_text(encoding="utf-8"))
    M, L = raw["members"], raw["links"]
    by = {m["item_id"]: m for m in M}
    ids = [m["item_id"] for m in M]
    hv = load_vectors(a.db, a.code_wt, ids)
    sub = substories(ids, hv)

    from osint_monitor.processors.geography import Gazetteer
    gz = Gazetteer.load()

    def broad_place(pl):                     # a country or a supra-national region, not a place in a country
        c = gz.canonical(pl)
        return c in gz.countries or not gz.ancestors(pl) & gz.countries

    countries = {gz.canonical(c) for c in gz.countries}

    # attach-time links (accepted under the production rule to members stored in earlier runs)
    attach = [l for l in L if l["kind"].startswith("attach")]
    seed = [m["item_id"] for m in M if m["path"] == "created the Development"]
    # hop distance from the seed over attach-time links, in attachment order (shortest chain the rule allowed)
    hop = {s: 0 for s in seed}
    links_of = defaultdict(list)
    for l in attach:
        links_of[l["from"]].append(l)
    for m in M:
        n = m["item_id"]
        if n in hop:
            continue
        hs = [hop[l["to"]] for l in links_of[n] if hop.get(l["to"]) is not None]
        hop[n] = min(hs) + 1 if hs else None

    def edge_class(l):
        A, B = by[l["from"]], by[l["to"]]
        kinds = {A["headline_kind"], B["headline_kind"]}
        commentary = (A["evidence_type"] == "commentary" or B["evidence_type"] == "commentary"
                      or "analysis" in kinds or A["roundup"] or B["roundup"])
        liveblog = "rolling" in kinds
        specific_place = [x for x in l["shared_places"] if not broad_place(x)]
        actor_only_states = bool(l["shared_actors"]) and all(x in countries for x in l["shared_actors"])
        return {
            "commentary_bridge": commentary, "liveblog_bridge": liveblog,
            "broad_actor_only": not l["shared_anchors"] and not specific_place and actor_only_states,
            "broad_place_only": not l["shared_anchors"] and bool(l["shared_places"]) and not specific_place,
            "no_shared_entities": not l["shared_anchors"] and not l["shared_places"] and not l["shared_actors"],
            "near_threshold": l["cosine"] < NEAR_THRESHOLD,
            "cross_substory": sub[l["from"]] != sub[l["to"]],
            "p7": bool(l["p7_occurrence_match"]), "override": bool(l["headline_override"]),
        }

    for l in attach:
        l["class"] = edge_class(l)

    # single-link attachments and chains: a member whose only partners were themselves single-link attachees
    single = {m["item_id"] for m in M if m["linked_existing_members"] == 1}

    out = a.out
    out.mkdir(parents=True, exist_ok=True)

    # --- sub-story table
    groups = defaultdict(list)
    for i in ids:
        groups[sub[i]].append(i)
    sub_rows = []
    for g, members in sorted(groups.items(), key=lambda x: -len(x[1])):
        times = sorted(by[i]["published_at"] or "" for i in members)
        sub_rows.append({"substory": g, "size": len(members), "first_published": times[0][:16], "last_published": times[-1][:16],
                         "first_attached": min(by[i]["added_at"] for i in members)[:16],
                         "sample_titles": [by[i]["title"] for i in members[:4]]})

    # --- gravity time series (per attachment day)
    series, seen_actor, seen_place, seen_src, seen_lang, seen_kind, seen_sub = [], set(), set(), set(), set(), set(), set()
    pub = []
    day_rows = defaultdict(list)
    for k, m in enumerate(M, start=1):
        seen_actor |= set(m["actors"]); seen_place |= set(m["places"]); seen_src.add(m["source"])
        seen_lang.add(m["language_recomputed"]); seen_kind.add(m["headline_kind"]); seen_sub.add(sub[m["item_id"]])
        if m["published_at"]:
            pub.append(m["published_at"])
        day_rows[m["added_at"][:10]].append(m)
        series.append({"n": k, "added_at": m["added_at"][:16], "size": k, "actors": len(seen_actor), "places": len(seen_place),
                       "sources": len(seen_src), "languages": len(seen_lang), "headline_kinds": len(seen_kind),
                       "substories": len(seen_sub), "span_days": None,
                       "window_members": m["existing_members_within_72h"], "linked": m["linked_existing_members"]})
    from datetime import datetime
    first_pub = None
    for row, m in zip(series, M):
        t = m["published_at"]
        if t:
            first_pub = t if first_pub is None or t < first_pub else first_pub
            row["span_days"] = round((datetime.fromisoformat(max(r["published_at"] for r in M[:row["n"]] if r["published_at"])) -
                                      datetime.fromisoformat(first_pub)).total_seconds() / 86400, 1)
    daily = []
    for day, ms in sorted(day_rows.items()):
        last = series[M.index(ms[-1])]
        cont = [m for m in ms if m["path"] == "continuation"]
        daily.append({"day": day, "attached": len(ms), "size_end": last["size"], "actors": last["actors"], "places": last["places"],
                      "sources": last["sources"], "languages": last["languages"], "substories": last["substories"],
                      "span_days": last["span_days"],
                      "mean_window_members": round(sum(m["existing_members_within_72h"] for m in cont) / len(cont), 1) if cont else None,
                      "mean_linked": round(sum(m["linked_existing_members"] for m in cont) / len(cont), 1) if cont else None,
                      "single_link_share": round(sum(m["linked_existing_members"] == 1 for m in cont) / len(cont), 2) if cont else None,
                      "new_substory_share": round(sum(1 for m in cont if all(sub[l["to"]] != sub[m["item_id"]] for l in links_of[m["item_id"]])) / len(cont), 2) if cont else None})

    # --- counterfactual cuts over attach-time links (connectivity of the stored members)
    def run_cut(name, keep_edge, nodes=None):
        nodes = nodes or ids
        edges = [(l["from"], l["to"]) for l in attach if keep_edge(l) and l["from"] in set(nodes) and l["to"] in set(nodes)]
        comps = components(nodes, edges)
        big = [c for c in comps if len(c) > 1]
        splits = []                    # sub-stories spread over several non-trivial components
        comp_of = {i: k for k, c in enumerate(comps) for i in c}
        for g, ms in groups.items():
            ks = Counter(comp_of[i] for i in ms if i in comp_of)
            if len(ms) >= 5 and len([k for k, v in ks.items() if v >= 2]) > 1:
                splits.append(g)
        seed_comp = comps[comp_of[seed[0]]] if seed and seed[0] in comp_of else []
        return {"cut": name, "components": len(comps), "non_singleton": len(big), "largest": [len(c) for c in comps[:6]],
                "singletons": sum(1 for c in comps if len(c) == 1), "seed_component": len(seed_comp),
                "substories_in_seed_component": len({sub[i] for i in seed_comp}),
                "substories_split_across_components": splits,
                "largest_component_samples": {len(c): [by[i]["title"][:90] for i in sorted(c, key=lambda x: by[x]["added_at"])[:3]]
                                              for c in comps[:4]}}

    cuts = [run_cut("baseline (all reconstructed attach-time links)", lambda l: True)]
    first_wrong = [int(x) for x in os.environ.get("FIRST_WRONG", "").split(",") if x]
    if first_wrong:
        # the links the named items attached with (their own attach-time links), not later links to them
        cuts.append(run_cut(f"remove the attach-time links of the earliest clearly wrong attachment(s) {first_wrong}",
                            lambda l: l["from"] not in first_wrong))
        cuts.append(run_cut(f"remove every link touching {first_wrong} (as if never attached)",
                            lambda l: l["from"] not in first_wrong and l["to"] not in first_wrong))
    for extra in [int(x) for x in os.environ.get("ENTRY_POINTS", "").split(",") if x]:
        cuts.append(run_cut(f"remove the attach-time links of sub-story entry item {extra}", lambda l, e=extra: l["from"] != e))
    cuts += [
        run_cut("remove commentary / analysis / roundup bridge links", lambda l: not l["class"]["commentary_bridge"]),
        run_cut("remove live-blog links", lambda l: not l["class"]["liveblog_bridge"]),
        run_cut("remove links whose only shared entities are states (broad actor anchor)", lambda l: not l["class"]["broad_actor_only"]),
        run_cut("remove links whose only shared places are countries/regions (broad place anchor)", lambda l: not l["class"]["broad_place_only"]),
        run_cut("remove links with no shared entity at all", lambda l: not l["class"]["no_shared_entities"]),
        run_cut(f"remove near-threshold links (cosine < {NEAR_THRESHOLD})", lambda l: not l["class"]["near_threshold"]),
        run_cut("remove links crossing sub-stories (descriptive grouping)", lambda l: not l["class"]["cross_substory"]),
        run_cut("direct-to-seed only (no chaining): members linked directly to a seed item",
                lambda l: l["to"] in seed or l["from"] in seed),
    ]
    boundary = os.environ.get("BOUNDARY")
    if boundary:
        before = {m["item_id"] for m in M if m["added_at"] < boundary}
        cuts.append(run_cut(f"remove links crossing the first occurrence boundary ({boundary})",
                            lambda l: (l["from"] in before) == (l["to"] in before)))

    # --- edge statistics
    acc = attach
    stats = {
        "members": len(M), "paths": Counter(m["path"] for m in M),
        "continuation_reconstructed": sum(1 for m in M if m["path"] == "continuation" and m["linked_existing_members"] > 0),
        "continuation_total": sum(1 for m in M if m["path"] == "continuation"),
        "single_link_attachments": sum(1 for m in M if m["path"] == "continuation" and m["linked_existing_members"] == 1),
        "attach_links": len(acc),
        "attach_links_near_threshold": sum(l["class"]["near_threshold"] for l in acc),
        "attach_links_p7": sum(l["class"]["p7"] for l in acc), "attach_links_override": sum(l["class"]["override"] for l in acc),
        "attach_links_commentary_bridge": sum(l["class"]["commentary_bridge"] for l in acc),
        "attach_links_broad_actor_only": sum(l["class"]["broad_actor_only"] for l in acc),
        "attach_links_broad_place_only": sum(l["class"]["broad_place_only"] for l in acc),
        "attach_links_no_shared_entity": sum(l["class"]["no_shared_entities"] for l in acc),
        "attach_links_cross_substory": sum(l["class"]["cross_substory"] for l in acc),
        "hop_distance": Counter(hop.values()), "substories": len(groups),
        "substories_ge5": sum(1 for g in groups.values() if len(g) >= 5),
        "best_link_cosine_quartiles": sorted(m["best_partner_cosine"] for m in M if m["best_partner_cosine"]),
    }
    q = stats["best_link_cosine_quartiles"]
    stats["best_link_cosine_quartiles"] = [q[0], q[len(q) // 4], q[len(q) // 2], q[3 * len(q) // 4], q[-1]] if q else []

    # --- outputs
    (out / "analysis.json").write_text(json.dumps({"stats": stats, "substories": sub_rows, "daily": daily, "cuts": cuts,
                                                   "series": series}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    if a.full:
        with open(out / "attachment-history.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["order", "item_id", "source", "source_role", "evidence_type", "origin", "language_recomputed",
                        "published_at", "fetched_at", "added_at", "added_run_id", "run_tier", "run_code", "path",
                        "headline_kind", "roundup", "title", "actors", "places", "anchors", "item_domain_or_type",
                        "existing_members", "existing_members_within_72h", "linked_existing_members", "hop_from_seed",
                        "substory", "best_partner", "best_partner_title", "best_cosine", "best_headline_cosine",
                        "best_hours", "best_shared_places", "best_shared_actors", "best_shared_anchors", "best_guard",
                        "best_p7", "best_headline_override", "partner_was_single_link_attachee",
                        "cluster_seen_by_decision", "decision_boundary_within_run"])
            for k, m in enumerate(M, start=1):
                n = m["item_id"]
                ls = links_of[n]
                b = max(ls, key=lambda l: l["cosine"]) if ls else None
                w.writerow([k, n, m["source"], m["source_role"], m["evidence_type"], m["origin"], m["language_recomputed"],
                            m["published_at"], m["fetched_at"], m["added_at"], m["added_run_id"], m["run_tier"], m["run_code"],
                            m["path"], m["headline_kind"], m["roundup"], m["title"], "; ".join(m["actors"]),
                            "; ".join(m["places"]), "; ".join(m["anchors"]), m["item_domain_or_type"],
                            m["existing_members"], m["existing_members_within_72h"], m["linked_existing_members"],
                            hop.get(n), f"S{sub[n]}",
                            b["to"] if b else "", by[b["to"]]["title"] if b else "", b["cosine"] if b else "",
                            b["headline_cosine"] if b else "", b["hours"] if b else "", "; ".join(b["shared_places"]) if b else "",
                            "; ".join(b["shared_actors"]) if b else "", "; ".join(b["shared_anchors"]) if b else "",
                            b["guard"] if b else "", "; ".join(b["p7_occurrence_match"] or []) if b else "",
                            b["headline_override"] if b else "",
                            (b["to"] in single) if b else "", m["cluster_seen_by_decision"], m["decision_boundary_within_run"]])
        deg = Counter()
        for l in acc:
            deg[l["from"]] += 1
            deg[l["to"]] += 1
        graph = {
            "description": "Nodes: D398 members. Edges: links the production rule accepts between a member and members "
                           "stored in earlier runs (attach-time links), reconstructed with the unchanged link and guard code. "
                           "Same-run links are omitted (decision boundary not recoverable).",
            "nodes": [{"id": m["item_id"], "source": m["source"], "published_at": m["published_at"], "added_at": m["added_at"],
                       "title": m["title"], "kind": m["headline_kind"], "evidence_type": m["evidence_type"],
                       "substory": f"S{sub[m['item_id']]}", "hop_from_seed": hop.get(m["item_id"]), "degree": deg[m["item_id"]],
                       "seed": m["path"] == "created the Development"} for m in M],
            "edges": [{"source": l["from"], "target": l["to"], "cosine": l["cosine"], "headline_cosine": l["headline_cosine"],
                       "hours": l["hours"], "shared_places": l["shared_places"], "shared_actors": l["shared_actors"],
                       "shared_anchors": l["shared_anchors"], "guard": l["guard"], "p7": l["p7_occurrence_match"],
                       "headline_override": l["headline_override"], "rule": "clustering._linked + no segmentation guard "
                       "(development_segmentation.compatible_link)", **{k: v for k, v in l["class"].items()}} for l in acc],
        }
        (out / "attachment-graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(stats, default=str, indent=1)[:3000])
    for c in cuts:
        print(c["cut"], "| comps", c["components"], "largest", c["largest"], "seed comp", c["seed_component"],
              "subs in seed comp", c["substories_in_seed_component"], "split subs", c["substories_split_across_components"][:8])
    return 0


if __name__ == "__main__":
    sys.exit(main())
