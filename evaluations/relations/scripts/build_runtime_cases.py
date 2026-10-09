"""Draw the runtime-eligible relation benchmark (runtime-benchmark-design.md; owner approval 2026-10-09).

    python evaluations/relations/scripts/build_runtime_cases.py   # -> runtime/runs/, runtime/review/

Per window of runtime/manifest.yaml: replay with the current code (fixed replay clock), take the system
Developments, and draw pairs of distinct Developments (first reports at most 7 days apart) in four strata:

- generator: every pair the v1 candidate generator proposes (fully enumerated, so candidate precision is exact);
- probe: pairs not proposed that share a principal actor or a compatible place, first reports within 72 h; up to
  30, sampled independently per window with random.Random(f"{seed}:{window}");
- hard_negative: remaining pairs (not proposed, not drawn as probe) where both Developments involve both actors of
  one broad pair (US-China, US-Iran, Russia-Ukraine, Israel-Iran, Israel-Palestine, China-Taiwan, US-Russia,
  China-Japan) or that sit in the same Situation; up to 10. Recall estimates use the probe draws only;
- random: uniform remaining pairs; up to 10.

Writes runtime/review/cases.json (the review format of review/cases.json; side A is the earlier Development) and
runtime/review/candidate-rules.json (each case's stratum and, for generator pairs, the proposed types; hidden from
the labeller and the owner), with population sizes per stratum for recall weights. Cases are shuffled so their
order does not reveal the stratum. The sealed holdouts are never read.
"""
import hashlib
import json
import os
import random
import sys
from datetime import datetime, timedelta
from itertools import combinations
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT.parent / "identity" / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import yaml  # noqa: E402

PAIR_GAP = timedelta(days=7)
PROBE_GAP = timedelta(hours=72)
BROAD = [({"united states"}, {"china"}), ({"united states"}, {"iran"}), ({"russia"}, {"ukraine"}),
         ({"israel"}, {"iran"}), ({"israel"}, {"palestine", "gaza", "west bank"}), ({"china"}, {"taiwan"}),
         ({"united states"}, {"russia"}), ({"china"}, {"japan"})]


def when(v):
    return datetime.fromisoformat(str(v).replace("Z", "")) if v else None


def windows(manifest):
    out = []
    for w in manifest["windows"]:
        path = (RUNTIME / w["items_file"]).resolve()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == w["items_sha256"], f"{w['id']}: items changed"
        start, end = datetime.fromisoformat(w["start"]), datetime.fromisoformat(w["end"])
        ticks, t, n = [], start, 1
        while t < end:
            ticks.append({"tick": n, "from": t.isoformat(),
                          "to": min(t + timedelta(hours=manifest["tick_hours"]), end).isoformat()})
            t, n = t + timedelta(hours=manifest["tick_hours"]), n + 1
        out.append({**w, "split": "development", "items_file": str(path), "ticks": ticks})
    return out


def replay(w):
    path = RUNTIME / "runs" / f"{w['id']}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    import replay_current
    t = replay_current.replay(w)
    keep = {"window": w["id"],
            "developments": {k: {f: v.get(f) for f in ("summary", "members", "principals", "sources", "situation")}
                             for k, v in t["developments"].items()},
            "items": {i: {f: r[f] for f in ("source", "lang", "title", "excerpt", "published_at", "developments",
                                            "places", "entities", "roundup")} for i, r in t["items"].items()}}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(keep, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8",
                    newline="\n")
    return keep


def side(t, dev_id, wid):
    d = t["developments"][str(dev_id)]
    rows = sorted(((m, t["items"][m]) for m in d["members"] if m in t["items"]),
                  key=lambda kv: kv[1]["published_at"] or "")
    times = [r["published_at"] for _, r in rows if r["published_at"]]
    return {"id": f"{wid}:D{dev_id}", "window": wid, "members": [m for m, _ in rows], "storyline": None,
            "first": min(times) if times else None, "last": max(times) if times else None,
            "actors": sorted(d["principals"] or []), "places": sorted({p for _, r in rows for p in r["places"] or []}),
            "system_developments": [dev_id], "situations": [d["situation"]] if d["situation"] else [],
            "sources": sorted({r["source"] for _, r in rows}), "langs": sorted({r["lang"] for _, r in rows if r["lang"]}),
            "roundup_only": all(r["roundup"] for _, r in rows),
            "evidence": [{"item": m, "source": r["source"], "published_at": r["published_at"], "title": r["title"],
                          "excerpt": (r["excerpt"] or "")[:400]} for m, r in rows]}


def main() -> int:
    from measure_candidates import views_of
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.development_segmentation import gazetteer
    from osint_monitor.processors.relation_candidates import METHOD, generate
    manifest = yaml.safe_load((RUNTIME / "manifest.yaml").read_text(encoding="utf-8"))
    geo, norm = gazetteer(False), ActorNormalizer.load()
    cases, rules, populations = [], {}, {}
    for w in windows(manifest):
        t = replay(w)
        wid = w["id"]
        print(wid, len(t["developments"]), "Developments", flush=True)
        views = {v.id: v for v in views_of(t, geo)}
        proposed = {}
        for c in generate(list(views.values()), geo):
            proposed.setdefault(frozenset((c.source_event_id, c.target_event_id)), []).append(
                f"{c.relation_type} {c.source_event_id}->{c.target_event_id}")
        universe = [frozenset(p) for p in combinations(sorted(views), 2)
                    if views[min(p)].first and views[max(p)].first and abs(views[min(p)].first - views[max(p)].first)
                    <= PAIR_GAP]
        keys = {d: {norm.key(a) for a in views[d].principals} - {None} for d in views}
        situ = {d: t["developments"][str(d)]["situation"] for d in views}

        def shares(p):
            a, b = sorted(p)
            gap = abs(views[a].first - views[b].first)
            places = any(geo.same_or_contains(x, y) for x in views[a].places for y in views[b].places)
            return gap <= PROBE_GAP and bool((views[a].principals & views[b].principals) or places)

        def broad(p):   # both Developments involve both actors of one broad pair, or they share a Situation
            a, b = sorted(p)
            pair = any(x & keys[a] and y & keys[a] and x & keys[b] and y & keys[b] for x, y in BROAD)
            return pair or (situ[a] is not None and situ[a] == situ[b])

        rng = random.Random(f"{manifest['seed']}:{wid}")
        generator = [p for p in universe if p in proposed]
        rest = [p for p in universe if p not in proposed]
        probe_pop = [p for p in rest if shares(p)]
        probe = rng.sample(probe_pop, min(manifest["caps"]["probe"], len(probe_pop)))
        rest = [p for p in rest if p not in set(probe)]
        hard_pop = [p for p in rest if broad(p)]    # may include undrawn probe-population pairs (recall uses probe draws only)
        hard = rng.sample(hard_pop, min(manifest["caps"]["hard_negative"], len(hard_pop)))
        rest = [p for p in rest if p not in set(hard)]
        rand = rng.sample(rest, min(manifest["caps"]["random"], len(rest)))
        populations[wid] = {"developments": len(views), "pairs": len(universe), "generator": len(generator),
                            "probe_population": len(probe_pop), "probe_drawn": len(probe),
                            "hard_negative_population": len(hard_pop), "hard_negative_drawn": len(hard),
                            "random_population": len(rest), "random_drawn": len(rand)}
        for stratum, pairs in (("generator", generator), ("probe", probe), ("hard_negative", hard), ("random", rand)):
            for p in sorted(pairs, key=sorted):
                a, b = sorted(p, key=lambda d: (views[d].first, d))
                cases.append({"a": side(t, a, wid), "b": side(t, b, wid), "_rule": {
                    "stratum": stratum, "window": wid, "proposed": proposed.get(p, [])}})
        print(" ", populations[wid], flush=True)

    random.Random(f"{manifest['seed']}:order").shuffle(cases)
    out, hidden = [], {}
    for n, c in enumerate(cases, 1):
        cid = f"U{n:03d}"
        hidden[cid] = c.pop("_rule")
        out.append({"case": cid, **c})
    review = RUNTIME / "review"
    review.mkdir(parents=True, exist_ok=True)
    meta = {"design": "runtime-benchmark-design.md", "seed": manifest["seed"], "caps": manifest["caps"],
            "generator": METHOD, "populations": populations, "cases": len(out)}
    (review / "cases.json").write_text(json.dumps({"meta": meta, "cases": out}, indent=1, ensure_ascii=False) + "\n",
                                       encoding="utf-8", newline="\n")
    (review / "candidate-rules.json").write_text(json.dumps(hidden, indent=1, ensure_ascii=False) + "\n",
                                                 encoding="utf-8", newline="\n")
    print(len(out), "cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
