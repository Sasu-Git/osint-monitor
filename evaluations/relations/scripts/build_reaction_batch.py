"""Targeted reaction_to batch (Phase 3): candidate pairs from the development windows only.

    python evaluations/relations/scripts/build_reaction_batch.py   # -> review-reaction-batch/

The frozen gold has only 2 canonical reaction_to positives. This batch looks for explicit reactions. It uses the
same occurrence units as build_cases.py (clustering-gold occurrences, else system Developments plus provisional
single items, merged by identity gold revision 2), and the same replays under runs/. The sealed holdout is never
read.

A candidate is an ordered pair (earlier, later):
- first reports at most 96 h apart;
- the later text carries an explicit reaction cue (condemn, reject, respond, react, retaliate, welcome, slam,
  summon, protest against, vow to respond, hit back, criticise ...);
- they share a canonical actor or place, or their text cosine is at least 0.55;
- cosine at least 0.40, and the earlier side is not an analysis or commentary headline;
- the pair is not already a case in the frozen gold.

Pairs are ranked by cosine, with at most 8 per window, and shuffled for review. The rule selects pairs, never
labels. The selecting cue is kept apart from the labeller and the owner (candidate-rules.json).
"""
import hashlib
import json
import random
import re
import sys
from datetime import datetime
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cases as B  # noqa: E402
from replay_windows import windows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-reaction-batch"
SEED = 20261007
PER_WINDOW = 8
REACTION = re.compile(
    r"\b(condemn\w*|reject\w*|respond\w*|in response|react\w*|retaliat\w*|denounc\w*|welcom\w*|slam\w*|"
    r"summon\w*|protest\w* (against|over)|vow\w* to (respond|retaliate)|hits? back|criticis\w*|criticiz\w*|"
    r"rebuk\w*|lambast\w*|warn\w* (of|against) (retaliation|consequences)|deplor\w*|decr(y|ies|ied))\b", re.I)


def main():
    import numpy as np
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.classification.rules import COMMENTARY_TITLE
    from osint_monitor.processors.embeddings import embed_texts

    norm = ActorNormalizer.load()
    existing = {frozenset((c["a"]["id"], c["b"]["id"]))
                for c in json.loads((ROOT / "review" / "cases.json").read_text(encoding="utf-8"))["cases"]}
    rng = random.Random(SEED)
    cases, rules = [], {}
    for w in windows("development"):
        occ, _, _, _ = B.load_window(w, "development")
        occ = [o for o in occ if o["first"]]
        vec = embed_texts([B.text_of(o) for o in occ])
        vec = vec / (np.linalg.norm(vec, axis=1, keepdims=True) + 1e-9)
        idx = {o["id"]: i for i, o in enumerate(occ)}
        keys = {o["id"]: norm.keys(o["actors"]) | {p.lower() for p in o["places"]} for o in occ}
        found = []
        for x, y in combinations(occ, 2):
            early, late = sorted((x, y), key=lambda o: (o["first"], o["id"]))
            if frozenset((early["id"], late["id"])) in existing:
                continue
            hours = (datetime.fromisoformat(late["first"]) - datetime.fromisoformat(early["first"])).total_seconds() / 3600
            if hours > 96:
                continue
            cue = REACTION.search(B.text_of(late))
            if not cue or COMMENTARY_TITLE.search(early["evidence"][0]["title"]):
                continue
            cos = float(vec[idx[early["id"]]] @ vec[idx[late["id"]]])
            shared = keys[early["id"]] & keys[late["id"]]
            if cos < 0.40 or (not shared and cos < 0.55):
                continue
            found.append((cos, early, late, cue.group(0), sorted(shared)[:5]))
        found.sort(key=lambda t: -t[0])
        for cos, early, late, cue, shared in found[:PER_WINDOW]:
            cases.append({"a": early, "b": late, "cosine": round(cos, 3)})
            rules[(early["id"], late["id"])] = f"cue '{cue}', shared {shared}, cosine {cos:.2f}, window {w['id']}"
    rng.shuffle(cases)
    OUT.mkdir(exist_ok=True)
    out_cases, out_rules = [], {}
    for n, c in enumerate(cases, 1):
        cid = f"T{n:03d}"
        out_cases.append({"case": cid, **c})
        out_rules[cid] = rules[(c["a"]["id"], c["b"]["id"])]
    meta = {"batch": "reaction_to targeted batch", "split": "development", "seed": SEED, "per_window": PER_WINDOW,
            "cases": len(out_cases), "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT / "cases.json").write_text(json.dumps({"meta": meta, "cases": out_cases}, indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
    (OUT / "candidate-rules.json").write_text(json.dumps(out_rules, indent=1, ensure_ascii=False) + "\n",
                                              encoding="utf-8", newline="\n")
    print(len(out_cases), "cases ->", OUT)


if __name__ == "__main__":
    main()
