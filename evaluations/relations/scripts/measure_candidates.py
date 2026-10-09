"""Measure Session 1 candidate generation once on relation gold revision 2 (candidate-generation-plan.md).

    python evaluations/relations/scripts/measure_candidates.py

Replays every development window with the current code (fixed replay clock) into runs-rev2/WINDOW.json, builds
Development views, generates candidates (osint_monitor/processors/relation_candidates.py) and scores them against
gold/relation-gold-rev2.yaml: coverage (COVERED / BLOCKED_BY_IDENTITY / NOT_SURFACED), candidate recall on covered
canonical positives of the runtime types, candidate volume, and candidates on scored NO_RELATION cases per
hard-negative family. Writes runs-rev2/candidates-summary.json. The sealed holdout is never read.
"""
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT.parent / "identity" / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import yaml  # noqa: E402

OUT = ROOT / "runs-rev2"
RUNTIME = ("same_calamity_lifecycle", "same_convened_event", "reaction_to")


def when(v):
    return datetime.fromisoformat(str(v).replace("Z", "")) if v else None


def replay_all() -> dict:
    import replay_current
    from replay_windows import windows
    OUT.mkdir(exist_ok=True)
    traces = {}
    for w in windows("development"):
        path = OUT / f"{w['id']}.json"
        if path.exists():
            traces[w["id"]] = json.loads(path.read_text(encoding="utf-8"))
            continue
        t = replay_current.replay(w)
        keep = {"window": w["id"],
                "developments": {k: {"members": sorted(v["members"]), "principals": v["principals"],
                                     "summary": v["summary"]} for k, v in t["developments"].items()},
                "items": {i: {f: r[f] for f in ("title", "excerpt", "published_at", "places", "developments", "lang")}
                          for i, r in t["items"].items()}}
        path.write_text(json.dumps(keep, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8",
                        newline="\n")
        traces[w["id"]] = keep
        print(w["id"], len(keep["developments"]), "Developments", flush=True)
    return traces


def views_of(trace, geo):
    from osint_monitor.processors.entity_resolver import normalise
    from osint_monitor.processors.relation_candidates import BODY_CHARS, DevelopmentView
    items = trace["items"]
    out = []
    for k, d in trace["developments"].items():
        rows = [items[m] for m in d["members"] if m in items]
        times = [when(r["published_at"]) for r in rows if r["published_at"]]
        out.append(DevelopmentView(
            id=int(k), first=min(times) if times else None,
            texts=[f"{r['title']} {(r['excerpt'] or '')[:BODY_CHARS]}" for r in rows],
            principals=set(d["principals"] or []),
            places={geo.canonical(normalise(p)) for r in rows for p in (r["places"] or [])}))
    return out


def main() -> int:
    from osint_monitor.processors.development_segmentation import gazetteer
    from osint_monitor.processors.relation_candidates import METHOD, generate
    geo = gazetteer(False)
    gold = yaml.safe_load((ROOT / "gold" / "relation-gold-rev2.yaml").read_text(encoding="utf-8"))
    sides = yaml.safe_load((ROOT / "gold" / "relation-sides-rev2.yaml").read_text(encoding="utf-8"))
    rules = {**json.loads((ROOT / "review" / "candidate-rules.json").read_text(encoding="utf-8")),
             **json.loads((ROOT / "review-reaction-batch" / "candidate-rules.json").read_text(encoding="utf-8"))}
    traces = replay_all()

    cands, volume = {}, {}
    for wid, t in traces.items():
        views = views_of(t, geo)
        found = generate(views, geo)
        cands[wid] = {(c.relation_type, c.source_event_id, c.target_event_id): c for c in found}
        n = len(views)
        volume[wid] = {"developments": n, "pairs": n * (n - 1) // 2,
                       "candidates": dict(Counter(c.relation_type for c in found))}

    def devs_of(side_id):
        s = sides[side_id]
        items = traces[s["window"]]["items"]
        return {d for m in s["members"] for d in (items.get(m, {}).get("developments") or [])}

    def has(wid, rtype, x, y):
        if rtype == "reaction_to":
            return (rtype, x, y) in cands[wid]
        return (rtype, min(x, y), max(x, y)) in cands[wid]

    rows = []
    for cid, e in gold.items():
        wid = sides[e["a"]]["window"]
        da, db = devs_of(e["a"]), devs_of(e["b"])
        if not da or not db:
            coverage = "NOT_SURFACED"
        elif da == db and len(da) == 1:
            coverage = "BLOCKED_BY_IDENTITY"
        else:
            coverage = "COVERED"
        pairs = [(x, y) for x in da for y in db if x != y]
        if e["label"] == "reaction_to" and e.get("roles"):
            src = devs_of(e["roles"]["reaction"])
            dst = devs_of(e["roles"]["trigger"])
            hit = any(has(wid, "reaction_to", x, y) for x in src for y in dst if x != y)
            reversed_hit = any(has(wid, "reaction_to", y, x) for x in src for y in dst if x != y)
        else:
            hit = e["label"] in RUNTIME and any(has(wid, e["label"], x, y) for x, y in pairs)
            reversed_hit = False
        any_type = sorted({r for r in RUNTIME for x, y in pairs if has(wid, r, x, y) or has(wid, r, y, x)})
        rows.append({"case": cid, "window": wid, "label": e["label"], "canonical": e["canonical"],
                     "scored": e["scored"], "coverage": coverage, "hit": hit, "reversed": reversed_hit,
                     "candidate_types": any_type, "families": rules.get(cid, [])})

    report = {"method": METHOD, "volume": volume, "by_type": {}, "negatives": {}, "reference": {}, "rows": rows}
    for r in RUNTIME:
        pos = [x for x in rows if x["label"] == r and x["canonical"] and x["scored"]]
        cov = [x for x in pos if x["coverage"] == "COVERED"]
        report["by_type"][r] = {
            "canonical_positives": len(pos), "coverage": dict(Counter(x["coverage"] for x in pos)),
            "recalled": sorted(x["case"] for x in cov if x["hit"]),
            "missed": sorted(x["case"] for x in cov if not x["hit"]),
            "reversed_direction": sorted(x["case"] for x in cov if x["reversed"] and not x["hit"]),
            "blocked": sorted(x["case"] for x in pos if x["coverage"] == "BLOCKED_BY_IDENTITY"),
            "not_surfaced": sorted(x["case"] for x in pos if x["coverage"] == "NOT_SURFACED")}
    neg = [x for x in rows if x["label"] == "NO_RELATION" and x["scored"] and x["coverage"] == "COVERED"]
    fam = defaultdict(lambda: [0, 0])
    for x in neg:
        for f in {f.split(":")[0] for f in x["families"]} or {"(none)"}:
            fam[f][0] += 1
            fam[f][1] += bool(x["candidate_types"])
    report["negatives"] = {"covered_no_relation": len(neg),
                           "with_any_candidate": sum(1 for x in neg if x["candidate_types"]),
                           "by_type": dict(Counter(t for x in neg for t in x["candidate_types"])),
                           "by_family": {f: {"cases": n, "with_candidate": k} for f, (n, k) in sorted(fam.items())}}
    other = [x for x in rows if not (x["label"] in RUNTIME and x["canonical"] and x["scored"]) and
             x["label"] != "NO_RELATION"]
    report["reference"] = {f"{x['case']} {x['label']}{'' if x['canonical'] else ' (inferred)'}":
                           {"coverage": x["coverage"], "candidates": x["candidate_types"]} for x in other}
    (OUT / "candidates-summary.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n",
                                                 encoding="utf-8", newline="\n")

    print("\nvolume:")
    for wid, v in volume.items():
        print(f"  {wid:26s} devs {v['developments']:3d} pairs {v['pairs']:5d} candidates {v['candidates']}")
    for r, v in report["by_type"].items():
        print(f"\n{r}: {v['canonical_positives']} canonical positives, coverage {v['coverage']}")
        print(f"  recalled {len(v['recalled'])}: {v['recalled']}")
        print(f"  missed {len(v['missed'])}: {v['missed']}  reversed-direction: {v['reversed_direction']}")
        print(f"  blocked: {v['blocked']}  not surfaced: {v['not_surfaced']}")
    n = report["negatives"]
    print(f"\nNO_RELATION covered {n['covered_no_relation']}, with any candidate {n['with_any_candidate']}, "
          f"by type {n['by_type']}")
    for f, v in n["by_family"].items():
        print(f"  {f:28s} {v['with_candidate']}/{v['cases']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
