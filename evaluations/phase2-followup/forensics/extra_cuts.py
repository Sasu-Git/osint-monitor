"""Extra counterfactual cuts on a reconstructed attachment graph (GDELT headline-only items, pair time).

    python extra_cuts.py d398-raw.json d398/attachment-graph.json

Read-only and descriptive: connected components of the attach-time link graph after removing a class of edges.
"""
import json
import sys

import networkx as nx


def main(raw_path: str, graph_path: str) -> int:
    d = json.load(open(raw_path, encoding="utf-8"))
    M = {m["item_id"]: m for m in d["members"]}
    sub = {n["id"]: n["substory"] for n in json.load(open(graph_path, encoding="utf-8"))["nodes"]}
    A = [l for l in d["links"] if l["kind"].startswith("attach")]
    seed = [m["item_id"] for m in d["members"] if m["path"] == "created the Development"]
    gd = lambda i: M[i]["source"] == "GDELT"  # noqa: E731
    roll = lambda l: "rolling" in (M[l["from"]]["headline_kind"], M[l["to"]]["headline_kind"])  # noqa: E731
    comm = lambda l: "commentary" in (M[l["from"]]["evidence_type"], M[l["to"]]["evidence_type"])  # noqa: E731

    def run(name, keep, nodes=None):
        nodes = nodes or list(M)
        g, ns = nx.Graph(), set(nodes)
        g.add_nodes_from(nodes)
        g.add_edges_from((l["from"], l["to"]) for l in A if keep(l) and l["from"] in ns and l["to"] in ns)
        cs = sorted(nx.connected_components(g), key=len, reverse=True)
        sc = next((c for c in cs if seed[0] in c), set())
        print(f"{name}: components {len(cs)}, largest {[len(c) for c in cs[:5]]}, seed component {len(sc)}, "
              f"sub-stories in the largest {len({sub[i] for i in cs[0]})}")

    run("remove links touching GDELT (headline-only items)", lambda l: not gd(l["from"]) and not gd(l["to"]))
    run("non-GDELT members only", lambda l: True, [i for i in M if not gd(i)])
    run("non-GDELT, no live-blog, no commentary links",
        lambda l: not gd(l["from"]) and not gd(l["to"]) and not roll(l) and not comm(l))
    run("non-GDELT and cosine >= 0.58", lambda l: not gd(l["from"]) and not gd(l["to"]) and l["cosine"] >= 0.58)
    run("links within 24 h only", lambda l: (l["hours"] or 0) <= 24)
    run("links within 24 h, non-GDELT", lambda l: (l["hours"] or 0) <= 24 and not gd(l["from"]) and not gd(l["to"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
