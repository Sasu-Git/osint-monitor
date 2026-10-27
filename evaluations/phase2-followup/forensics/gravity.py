"""Gravity and representation diagnostics for a reconstructed Development (read-only; descriptive only).

    python gravity.py --raw d398-raw.json --analysis d398/analysis.json --db COPY.db --code-wt ../osint-monitor-timing --out d398/

- cosine sweep: connectivity of the attach-time link graph if only links at or above t were kept (diagnostic,
  not a proposed threshold);
- representation drift: each continuation item's cosine to the centroid of the members stored before it and to the
  seed's centroid, and the drift of the Development centroid from the seed centroid, per attachment day;
- a static SVG of the attachment tree (each member drawn to its best attach-time partner).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--raw", type=Path, required=True)
    p.add_argument("--analysis", type=Path, required=True)
    p.add_argument("--db", type=Path, required=True)
    p.add_argument("--code-wt", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--svg", action="store_true")
    a = p.parse_args()
    raw = json.loads(a.raw.read_text(encoding="utf-8"))
    ana = json.loads(a.analysis.read_text(encoding="utf-8"))
    M, L = raw["members"], [l for l in raw["links"] if l["kind"].startswith("attach")]
    ids = [m["item_id"] for m in M]
    os.environ["OSINT_DB_URL"] = f"sqlite:///{a.db.resolve().as_posix()}"
    sys.path.insert(0, str(a.code_wt.resolve()))
    from osint_monitor.core.database import RawItem, get_session
    from osint_monitor.processors.embeddings import blob_to_embedding
    s = get_session()
    vec = {i: blob_to_embedding(e) for i, e in s.query(RawItem.id, RawItem.embedding).filter(RawItem.id.in_(ids)) if e}
    vec = {i: v / np.linalg.norm(v) for i, v in vec.items()}

    import networkx as nx
    sweep = []
    for t in (0.53, 0.55, 0.58, 0.60, 0.62, 0.65, 0.70, 0.75):
        g = nx.Graph()
        g.add_nodes_from(ids)
        g.add_edges_from((l["from"], l["to"]) for l in L if l["cosine"] >= t)
        comps = sorted((len(c) for c in nx.connected_components(g)), reverse=True)
        sweep.append({"min_cosine": t, "largest": comps[0], "components_ge5": sum(c >= 5 for c in comps),
                      "singletons": sum(c == 1 for c in comps), "top5": comps[:5]})

    seed = [m["item_id"] for m in M if m["path"] == "created the Development"]
    seed_c = np.mean([vec[i] for i in seed if i in vec], axis=0)
    seed_c /= np.linalg.norm(seed_c)
    stored, rows = [], []
    for m in M:
        n = m["item_id"]
        if m["path"] == "continuation" and stored and n in vec:
            c = np.mean([vec[i] for i in stored], axis=0)
            c /= np.linalg.norm(c)
            rows.append({"day": m["added_at"][:10], "to_centroid": float(vec[n] @ c), "to_seed": float(vec[n] @ seed_c),
                         "centroid_vs_seed": float(c @ seed_c), "linked": m["linked_existing_members"]})
        if n in vec:
            stored.append(n)
    by_day = defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)
    drift = [{"day": d, "n": len(rs), "mean_cos_to_current_centroid": round(float(np.mean([r["to_centroid"] for r in rs])), 3),
              "mean_cos_to_seed_centroid": round(float(np.mean([r["to_seed"] for r in rs])), 3),
              "share_below_0.53_to_seed": round(sum(r["to_seed"] < 0.53 for r in rs) / len(rs), 2),
              "centroid_vs_seed": round(float(np.mean([r["centroid_vs_seed"] for r in rs])), 3)} for d, rs in sorted(by_day.items())]
    overall = {"continuations": len(rows),
               "share_below_0.53_to_seed_centroid": round(sum(r["to_seed"] < 0.53 for r in rows) / len(rows), 3),
               "share_below_0.53_to_current_centroid": round(sum(r["to_centroid"] < 0.53 for r in rows) / len(rows), 3)}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "gravity.json").write_text(json.dumps({"cosine_sweep": sweep, "drift": drift, "overall": overall}, indent=1),
                                        encoding="utf-8")
    for r in sweep:
        print(r)
    for r in drift:
        print(r)
    print(overall)

    if a.svg:
        # attachment tree: x = attachment time, y = hop distance from the seed; edge to the best partner
        hop = {n["id"]: n["hop_from_seed"] for n in json.loads((a.out / "attachment-graph.json").read_text(encoding="utf-8"))["nodes"]}
        sub = {}
        for row in ana["substories"]:
            pass
        graph = json.loads((a.out / "attachment-graph.json").read_text(encoding="utf-8"))
        subs = {n["id"]: n["substory"] for n in graph["nodes"]}
        top = [f"S{r['substory']}" for r in ana["substories"][:8]]
        palette = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#bcf60c"]
        colour = {s: palette[k] for k, s in enumerate(top)}
        from datetime import datetime
        t = {m["item_id"]: datetime.fromisoformat(m["added_at"][:19]) for m in M}
        t0, t1 = min(t.values()), max(t.values())
        W, H, pad = 1400, 520, 40
        x = lambda i: pad + (t[i] - t0).total_seconds() / max(1, (t1 - t0).total_seconds()) * (W - 2 * pad)  # noqa: E731
        y = lambda i: pad + (hop.get(i) if hop.get(i) is not None else 11) * (H - 2 * pad) / 11 + (i % 7) * 3  # noqa: E731
        best = {m["item_id"]: m["best_partner"] for m in M}
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H + 60}" font-family="sans-serif" font-size="11">',
                 f'<rect width="100%" height="100%" fill="#ffffff"/>',
                 f'<text x="{pad}" y="20" font-size="13">D{raw["event"]["id"]} attachment tree: x = when the member was stored, '
                 f'y = hops from the seed over attach-time links; line = best partner (highest cosine)</text>']
        for k in range(12):
            yy = pad + k * (H - 2 * pad) / 11
            parts.append(f'<text x="4" y="{yy + 4:.0f}" fill="#888">{k if k < 11 else "n/a"}</text>')
        for n, b in best.items():
            if b:
                parts.append(f'<line x1="{x(n):.1f}" y1="{y(n):.1f}" x2="{x(b):.1f}" y2="{y(b):.1f}" stroke="#bbb" stroke-width="0.5"/>')
        for m in M:
            n = m["item_id"]
            c = colour.get(subs[n], "#777")
            r = 4 if m["path"] == "created the Development" else 2.2
            parts.append(f'<circle cx="{x(n):.1f}" cy="{y(n):.1f}" r="{r}" fill="{c}"><title>{n} {subs[n]}: '
                         f'{(m["title"] or "").replace("&", "&amp;").replace("<", "&lt;")[:120]}</title></circle>')
        ly = H + 20
        for k, s_ in enumerate(top):
            title = next(r for r in ana["substories"] if f"S{r['substory']}" == s_)["sample_titles"][0][:28]
            parts.append(f'<circle cx="{pad + k * 170}" cy="{ly}" r="4" fill="{colour[s_]}"/>'
                         f'<text x="{pad + k * 170 + 8}" y="{ly + 4}">{s_}: {title.replace("&", "&amp;").replace("<", "&lt;")}</text>')
        parts.append(f'<text x="{pad}" y="{ly + 30}" fill="#666">Grey dots: the other sub-stories. Hover a dot for the item.</text></svg>')
        (a.out / "attachment-tree.svg").write_text("\n".join(parts), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
