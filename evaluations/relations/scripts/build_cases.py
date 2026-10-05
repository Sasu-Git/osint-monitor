"""Candidate Development pairs for the Phase 3 relation gold.

    python evaluations/relations/scripts/build_cases.py development   # -> review/cases.json, review/candidate-rules.json
    python evaluations/relations/scripts/build_cases.py holdout       # -> holdout/cases.sealed.json (counts only)

Unit (one Development = one occurrence, Phase 2 contract):
- windows with clustering gold: the gold occurrences ("developments" in the labels file);
- otherwise: the replayed system Developments, plus every unclustered item as a provisional single-item
  Development;
- in both cases occurrences that identity gold revision 2 labels SAME_DEVELOPMENT are merged first, so a pair is
  never two halves of one Development.

Candidate rules decide which pairs are reviewed, never their labels. They are seeded, capped and hidden from the
labeller and from the owner sheet (recorded separately in candidate-rules.json).
"""
import hashlib
import json
import os
import random
import re
import sys
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
IDENTITY_GOLD = ROOT.parent / "identity" / "gold" / "identity-gold.yaml"
SEED = 20261005

import yaml  # noqa: E402

# Identity-gold cases whose owner notes describe a grouping above the Development (owner-notes-proposals.md, s.3).
# SAME cases (C034, C064, C076, C103) are one Development under gold revision 2 and so never become pairs.
OWNER_NOTE_CASES = ("A021 A022 A032 H003 H006 H008 H015 H020 H021 H024 H026 C048 B005 B008 A006 A013 A023 C094 "
                    "A017 H016 H029 C016 C032 C039 C105 C115").split()

CUES = {
    "reaction": r"\b(condemn\w*|react\w*|respond\w*|in response|retaliat\w*|denounc\w*|reject\w*|welcom\w*|slam\w*|"
                r"vow\w*|warn\w* .{0,30}against|hits? back|criticis\w*|criticiz\w*)",
    "follow_up": r"\b(after|following|days after|aftermath|inquiry|investigat\w*|arrest\w*|charged|death toll|"
                 r"rises? to|latest|second day|resum\w*|again)\b",
    "causal": r"\b(because of|due to|caused|triggered|sparked|led to|prompted|blamed? (on|for)|result of|"
              r"fuell?ed by|driven by)\b",
}
LIFECYCLE = {
    "calamity": r"\b(earthquake|quake|flood\w*|landslide\w*|hurricane|typhoon|cyclone|storm|wildfire\w*|eruption|"
                r"tsunami|monsoon|drought|heatwave|avalanche|cloudburst|outbreak|ebola|cholera|mpox)\b",
    "attack": r"\b(strike\w*|drone\w*|missile\w*|attack\w*|barrage|shelling|bombard\w*|air ?raid\w*|rocket\w*)\b",
    "visit": r"\b(visit\w*|summit|talks|meets?|meeting|trip|state dinner|tour|hosts?|bilateral)\b",
}
# Named controls from the Situation hold-out (2026-10-05): the actor-pair rule joined these on a shared broad
# pair (US-China) or shared corporate actors. Matched by title prefix within the window they occur in.
SITUATION_HOLDOUT_CONTROLS = {"2026-10-03-live": [
    ("Xi-Trump summit drew Chinese CEOs", "China backs Cuba, Beijing"),
    ("Xi-Trump summit drew Chinese CEOs", "Can Europe still compete"),
    ("Can Europe still compete", "China backs Cuba, Beijing"),
    ("US delivers F-16V fighter jets", "Xi-Trump summit drew Chinese CEOs"),
    ("Pentagon awards Raytheon up to", "US Navy awards RTX"),
]}
BROAD_PAIRS = [("America", "China"), ("America", "Iran"), ("Russia", "Ukraine"), ("Iran", "Israel"),
               ("Israel", "Palestinians"), ("China", "Taiwan"), ("America", "Russia"), ("China", "Japan")]
CAPS = {"owner_note": None, "situation_holdout_control": None, "gold_related": 4, "storyline_mates": 3, "cue": 3, "lifecycle": 2,
        "neg_same_actors": 2, "neg_same_place": 1, "neg_same_crisis": 2, "neg_chrono_adjacent": 1, "neg_broad_pair": 2}
# caps are per window (lifecycle: per kind; neg_broad_pair: per broad pair); owner_note takes every listed case


def when(s):
    return datetime.fromisoformat(str(s)[:19]) if s else None


def load_window(w, split):
    run = json.loads(((ROOT / ("runs" if split == "development" else "holdout/runs")) / f"{w['id']}.json")
                     .read_text(encoding="utf-8"))
    items = run["items"]
    groups, meta = [], []
    if w.get("occurrences"):
        labels = yaml.safe_load((ROOT / w["occurrences"]).read_text(encoding="utf-8"))
        for d in labels["developments"]:
            groups.append([m for m in d["members"] if m in items])
            meta.append({"gold_id": d["id"], "storyline": d.get("storyline")})
        related = [(p[0], p[1], p[2] if len(p) > 2 else "") for p in labels.get("related_pairs") or []]
    else:
        seen = set()
        for k, dev in sorted(run["developments"].items(), key=lambda kv: int(kv[0])):
            mem = [m for m in dev["members"] if m not in seen]
            seen |= set(mem)
            if mem:
                groups.append(mem)
                meta.append({"gold_id": None, "storyline": None})
        for i in items:
            if i not in seen:
                groups.append([i])
                meta.append({"gold_id": None, "storyline": None})
        related = []
    # merge occurrences that identity gold rev 2 says are one Development
    gold = yaml.safe_load(IDENTITY_GOLD.read_text(encoding="utf-8"))
    idx = {m: n for n, g in enumerate(groups) for m in g}
    parent = list(range(len(groups)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    merges = []
    for cid, c in gold.items():
        if c["window"] == w["id"] and c["label"] == "SAME_DEVELOPMENT" and c["a"] in idx and c["b"] in idx:
            ra, rb = find(idx[c["a"]]), find(idx[c["b"]])
            if ra != rb:
                parent[rb] = ra
                merges.append(cid)
    merged = defaultdict(list)
    for n in range(len(groups)):
        merged[find(n)].append(n)
    occ = []
    for root, ns in merged.items():
        mem = sorted({m for n in ns for m in groups[n]}, key=lambda m: (items[m]["published_at"] or "", m))
        if not mem:
            continue
        gid = meta[root]["gold_id"]
        sys_devs = sorted({d for m in mem for d in items[m]["developments"]}, key=int)
        oid = f"{w['id']}:{gid}" if gid else (f"{w['id']}:D{sys_devs[0]}" if len(mem) > 1 and sys_devs
                                              else f"{w['id']}:{mem[0]}")
        times = [when(items[m]["published_at"]) for m in mem if items[m]["published_at"]]
        occ.append({
            "id": oid, "window": w["id"], "members": mem, "storyline": meta[root]["storyline"],
            "first": min(times).isoformat() if times else None, "last": max(times).isoformat() if times else None,
            "actors": sorted({a for m in mem for a in items[m]["entities"]} |
                             {p for d in sys_devs for p in run["developments"][str(d)]["principals"]}),
            "places": sorted({p for m in mem for p in items[m]["places"]}),
            "system_developments": [int(d) for d in sys_devs],
            "situations": sorted({run["developments"][str(d)]["situation"] for d in sys_devs
                                  if run["developments"][str(d)]["situation"]}),
            "sources": sorted({items[m]["source"] for m in mem}),
            "langs": sorted({items[m]["lang"] for m in mem if items[m]["lang"]}),
            "roundup_only": all(items[m]["roundup"] for m in mem),
            "evidence": [{"item": m, "source": items[m]["source"], "published_at": items[m]["published_at"],
                          "title": items[m]["title"], "excerpt": (items[m]["excerpt"] or "")[:300]} for m in mem[:4]],
        })
    return occ, related, merges, gold


def text_of(o):
    return " ".join(e["title"] + ". " + e["excerpt"] for e in o["evidence"][:3])


def main(split):
    import numpy as np
    from replay_windows import windows
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.embeddings import embed_texts

    norm = ActorNormalizer.load()
    rng = random.Random(SEED)
    cases, rules_of, merges_all, occ_all = {}, defaultdict(set), {}, {}

    for w in windows(split):
        occ, related, merges, gold = load_window(w, split)
        merges_all[w["id"]] = merges
        by_item = {m: o for o in occ for m in o["members"]}
        vecs = embed_texts([text_of(o) for o in occ])
        vecs = vecs / (np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9)
        pos = {o["id"]: n for n, o in enumerate(occ)}
        keys = {o["id"]: norm.keys(o["actors"]) for o in occ}
        txt = {o["id"]: text_of(o).lower() for o in occ}
        for o in occ:
            occ_all[o["id"]] = o

        def cos(a, b):
            return float(vecs[pos[a["id"]]] @ vecs[pos[b["id"]]])

        def cue(a, b, kind):
            later = b if (b["first"] or "") >= (a["first"] or "") else a
            return re.search(CUES[kind], txt[later["id"]]) is not None

        def any_cue(a, b):
            return any(cue(a, b, k) for k in CUES)

        def shares(a, b):
            return bool(keys[a["id"]] & keys[b["id"]]) or bool(set(a["places"]) & set(b["places"]))

        def hours(a, b):
            if not a["first"] or not b["first"]:
                return None
            return abs((when(a["first"]) - when(b["first"])).total_seconds()) / 3600

        def add(a, b, rule, why):
            if a["id"] == b["id"]:
                return
            x, y = sorted((a, b), key=lambda o: ((o["first"] or ""), o["id"]))
            k = (x["id"], y["id"])
            cases.setdefault(k, {"a": x["id"], "b": y["id"], "cosine": round(cos(x, y), 3)})
            rules_of[k].add(f"{rule}: {why}")

        # positives-leaning seeds -------------------------------------------------------------------------------
        for cid in OWNER_NOTE_CASES:
            c = gold.get(cid)
            if c and c["window"] == w["id"] and c["a"] in by_item and c["b"] in by_item:
                add(by_item[c["a"]], by_item[c["b"]], "owner_note", cid)
        for ta, tb in SITUATION_HOLDOUT_CONTROLS.get(w["id"], []):
            oa = [o for o in occ if any(e["title"].startswith(ta) for e in o["evidence"])]
            ob = [o for o in occ if any(e["title"].startswith(tb) for e in o["evidence"])]
            if oa and ob:
                add(oa[0], ob[0], "situation_holdout_control", f"{ta[:30]} / {tb[:30]}")
        rel = [(by_item[a], by_item[b], note) for a, b, note in related if a in by_item and b in by_item]
        rng.shuffle(rel)
        for a, b, note in rel[:CAPS["gold_related"]]:
            add(a, b, "gold_related", note[:80])
        story = defaultdict(list)
        for o in occ:
            if o["storyline"]:
                story[o["storyline"]].append(o)
        mates = [(a, b, s) for s, os_ in sorted(story.items()) for a, b in combinations(os_, 2)]
        rng.shuffle(mates)
        for a, b, s in mates[:CAPS["storyline_mates"]]:
            add(a, b, "storyline_mates", s)
        pairs = [(a, b) for a, b in combinations(occ, 2) if shares(a, b)]
        rng.shuffle(pairs)
        n_cue = 0
        for a, b in pairs:
            if n_cue < CAPS["cue"] and any_cue(a, b) and cos(a, b) >= 0.35:
                add(a, b, "cue", ",".join(k for k in CUES if cue(a, b, k)))
                n_cue += 1
        n_life = defaultdict(int)
        for a, b in pairs:
            for kind, rx in LIFECYCLE.items():
                ok = re.search(rx, txt[a["id"]]) and re.search(rx, txt[b["id"]])
                need = (len(keys[a["id"]] & keys[b["id"]]) >= 2 if kind == "visit"
                        else bool(set(a["places"]) & set(b["places"])))
                if ok and need and n_life[kind] < CAPS["lifecycle"]:
                    add(a, b, "lifecycle", kind)
                    n_life[kind] += 1
        # hard negatives ----------------------------------------------------------------------------------------
        neg = defaultdict(int)
        allpairs = list(combinations(occ, 2))
        rng.shuffle(allpairs)
        for a, b in allpairs:
            c = cos(a, b)
            ka, kb = keys[a["id"]], keys[b["id"]]
            if len(ka & kb) >= 2 and c < 0.35 and neg["same_actors"] < CAPS["neg_same_actors"]:
                add(a, b, "neg_same_actors", ",".join(sorted(ka & kb)))
                neg["same_actors"] += 1
            elif (set(a["places"]) & set(b["places"])) and not (ka & kb) and c < 0.35 \
                    and neg["same_place"] < CAPS["neg_same_place"]:
                add(a, b, "neg_same_place", ",".join(sorted(set(a["places"]) & set(b["places"]))))
                neg["same_place"] += 1
            elif ((a["storyline"] and a["storyline"] == b["storyline"]) or
                  (set(a["situations"]) & set(b["situations"]))) and c < 0.45 and not any_cue(a, b) \
                    and neg["same_crisis"] < CAPS["neg_same_crisis"]:
                add(a, b, "neg_same_crisis", a["storyline"] or ",".join(set(a["situations"]) & set(b["situations"])))
                neg["same_crisis"] += 1
            elif (h := hours(a, b)) is not None and h <= 3 and shares(a, b) and not any_cue(a, b) \
                    and 0.3 <= c < 0.5 and neg["chrono"] < CAPS["neg_chrono_adjacent"]:
                add(a, b, "neg_chrono_adjacent", f"{h:.1f} h")
                neg["chrono"] += 1
        for pair in BROAD_PAIRS:
            pk = frozenset(norm.keys(pair))
            if len(pk) != 2:
                continue
            members = [o for o in occ if pk <= keys[o["id"]]]
            bp = list(combinations(members, 2))
            rng.shuffle(bp)
            for a, b in bp[:CAPS["neg_broad_pair"]]:
                add(a, b, "neg_broad_pair", "-".join(pair))

    chosen = sorted(cases)
    rng.shuffle(chosen)                                   # review order unrelated to any rule
    prefix = "R" if split == "development" else "RH"
    out_cases, out_rules = [], {}
    for n, k in enumerate(chosen, 1):
        cid = f"{prefix}{n:03d}"
        c = cases[k]
        out_cases.append({"case": cid, "a": occ_all[c["a"]], "b": occ_all[c["b"]], "cosine": c["cosine"]})
        out_rules[cid] = sorted(rules_of[k])
    meta = {"split": split, "seed": SEED, "caps": CAPS, "cases": len(out_cases),
            "identity_same_merges": merges_all,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if split == "development":
        (ROOT / "review" / "cases.json").write_text(json.dumps({"meta": meta, "cases": out_cases}, indent=1,
                                                              ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        (ROOT / "review" / "candidate-rules.json").write_text(json.dumps(out_rules, indent=1, ensure_ascii=False)
                                                             + "\n", encoding="utf-8", newline="\n")
        tally = defaultdict(int)
        for rs in out_rules.values():
            for r in {r.split(":")[0] for r in rs}:
                tally[r] += 1
        print(len(out_cases), "cases; by rule", dict(sorted(tally.items())))
    else:
        path = ROOT / "holdout" / "cases.sealed.json"
        path.write_text(json.dumps({"meta": meta, "cases": out_cases, "rules": out_rules}, indent=1,
                                   ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print("sealed:", len(out_cases), "cases", hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main(sys.argv[1])
