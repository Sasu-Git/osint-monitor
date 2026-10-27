"""Summarise reconstructed giant Developments side by side (read-only; descriptive).

    python compare.py --dir SCRATCH/forensics --events 398 397 ... --blast giant-developments/blast-radius.csv \
        --csv giant-developments/giant-development-summary.csv [--show 397]

Reads, per event, reconstruct.py output (d<id>-raw.json), analyze.py output (d<id>/analysis.json) and gravity.py
output (d<id>/gravity.json). --show prints the seed and the first attachments that opened a new sub-story, for
reading the first semantic split by hand.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def load(d: Path, e: int):
    raw = json.loads((d / f"d{e}-raw.json").read_text(encoding="utf-8"))
    sub = d / f"d{e}"
    ana = json.loads((sub / "analysis.json").read_text(encoding="utf-8"))
    grav = json.loads((sub / "gravity.json").read_text(encoding="utf-8"))
    return raw, ana, grav


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", type=Path, required=True)
    p.add_argument("--events", type=int, nargs="+", required=True)
    p.add_argument("--blast", type=Path)
    p.add_argument("--csv", type=Path)
    p.add_argument("--show", type=int)
    a = p.parse_args()
    blast = {int(r["event_id"]): r for r in csv.DictReader(open(a.blast, encoding="utf-8"))} if a.blast else {}
    rows = []
    for e in a.events:
        raw, ana, grav = load(a.dir, e)
        M, st = raw["members"], ana["stats"]
        cuts = {c["cut"].split(" (")[0].split(":")[0]: c for c in ana["cuts"]}
        sweep = {r["min_cosine"]: r["largest"] for r in grav["cosine_sweep"]}
        b = blast.get(e, {})
        cont = st["continuation_total"] or 1
        rows.append({
            "event_id": e, "summary": raw["event"]["summary"][:100], "size": len(M),
            "span_days": b.get("span_days"), "growth_days": b.get("growth_days"), "outlets": b.get("outlets"),
            "languages": len({m["language_recomputed"] for m in M}), "actors": b.get("actors"), "places": b.get("places"),
            "paths": dict(st["paths"]),
            "continuation_reconstructed": f'{st["continuation_reconstructed"]}/{st["continuation_total"]}',
            "single_link_share": round(st["single_link_attachments"] / cont, 2),
            "links_per_member": round(st["attach_links"] / len(M), 1),
            "near_threshold_link_share": round(st["attach_links_near_threshold"] / max(1, st["attach_links"]), 2),
            "p7_or_override_links": st["attach_links_p7"] + st["attach_links_override"],
            "commentary_bridge_link_share": round(st["attach_links_commentary_bridge"] / max(1, st["attach_links"]), 2),
            "max_hop": max(int(k) for k in st["hop_distance"] if k not in ("null", "None")),
            "direct_to_seed_component": next(c["seed_component"] for c in ana["cuts"] if c["cut"].startswith("direct-to-seed")),
            "largest_without_commentary_links": next(c["largest"][0] for c in ana["cuts"] if c["cut"].startswith("remove commentary")),
            "largest_at_cosine_0.65": sweep.get(0.65), "largest_at_cosine_0.70": sweep.get(0.7),
            "substories": st["substories"], "substories_ge5": st["substories_ge5"],
            "drift_share_below_0.53_to_seed": grav["overall"]["share_below_0.53_to_seed_centroid"],
            "drift_share_below_0.53_to_current": grav["overall"]["share_below_0.53_to_current_centroid"],
            "headline_kinds": dict(Counter(m["headline_kind"] for m in M)),
            "languages_list": dict(Counter(m["language_recomputed"] for m in M)),
        })
    for r in rows:
        print({k: v for k, v in r.items() if k != "summary"}, "|", r["summary"])
    if a.csv:
        a.csv.parent.mkdir(parents=True, exist_ok=True)
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    if a.show:
        raw, ana, _ = load(a.dir, a.show)
        M = raw["members"]
        links = {}
        for l in raw["links"]:
            if l["kind"].startswith("attach"):
                links.setdefault(l["from"], []).append(l)
        print("\nSEED")
        for m in M:
            if m["path"] == "created the Development":
                print("  ", m["item_id"], m["published_at"][:16], m["source"][:16], "|", m["title"][:110])
        print("\nFIRST 30 ATTACHMENTS (links to earlier members, best cosine, best partner title)")
        for m in [m for m in M if m["path"] != "created the Development"][:30]:
            ls = links.get(m["item_id"], [])
            b = max(ls, key=lambda l: l["cosine"]) if ls else None
            bt = next((x["title"][:50] for x in M if b and x["item_id"] == b["to"]), "")
            print("  ", m["added_at"][5:16], m["item_id"], m["source"][:12].ljust(12), "L", len(ls), "best", b["cosine"] if b else None,
                  "|", m["title"][:75], "  <=", bt)
        print("\nTOP SUB-STORIES")
        for s in ana["substories"][:12]:
            print("  ", s["substory"], s["size"], s["first_published"], "->", s["last_published"], "|", " || ".join(t[:55] for t in s["sample_titles"][:3]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
