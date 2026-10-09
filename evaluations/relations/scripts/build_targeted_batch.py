"""Draw the positive-targeted runtime batch (runtime-targeted-design.md).

    python evaluations/relations/scripts/build_targeted_batch.py --round 1
    python evaluations/relations/scripts/build_targeted_batch.py --round 2 --types reaction_to,same_convened_event

Round 1 uses the primary pool (2026-10-05-live, 2026-10-08-live); round 2 the extension pool (2026-10-03-live),
only for the named types. Per type, eligible pairs of distinct system Developments are ranked by the cosine of their
title centroids (production embedding model) and the top 30 are drawn. Pairs already in the 155-case runtime
benchmark, or drawn in an earlier round, are excluded. A pair eligible for several types is drawn once (for the
first type that reaches it, in the order calamity, convened, reaction). Writes runtime-targeted/review-rN/cases.json
(review format; side A is the earlier Development) and candidate-rules.json (type targeted, rank, cosine; hidden
from the labeller and the owner). The sealed holdouts are never read.
"""
import json
import os
import random
import sys
from datetime import timedelta
from itertools import combinations
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runtime-targeted"
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT.parent / "identity" / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402

POOLS = {1: ["2026-10-05-live", "2026-10-08-live"], 2: ["2026-10-03-live"]}
ORDER = ["same_calamity_lifecycle", "same_convened_event", "reaction_to"]
CAP = 30
EPISODE_GAP, REACTION_GAP = timedelta(days=7), timedelta(hours=96)
SEED = 20261009


def main() -> int:
    from build_runtime_cases import side
    from measure_candidates import views_of
    from osint_monitor.processors.development_segmentation import gazetteer
    from osint_monitor.processors.embeddings import embed_texts
    from osint_monitor.processors.relation_candidates import GATHERING, REACTION, hazard_classes

    rnd = int(sys.argv[sys.argv.index("--round") + 1])
    types = sys.argv[sys.argv.index("--types") + 1].split(",") if "--types" in sys.argv else ORDER
    out = OUT / f"review-r{rnd}"
    if out.exists():
        print(f"refusing: {out} exists (each round is drawn once)")
        return 1
    geo = gazetteer(False)
    taken = set()
    for c in json.loads((ROOT / "runtime" / "review" / "cases.json").read_text(encoding="utf-8"))["cases"]:
        taken.add(frozenset((c["a"]["id"], c["b"]["id"])))
    for earlier in OUT.glob("review-r*/cases.json"):
        for c in json.loads(earlier.read_text(encoding="utf-8"))["cases"]:
            taken.add(frozenset((c["a"]["id"], c["b"]["id"])))

    eligible = {t: [] for t in types}
    traces = {}
    for wid in POOLS[rnd]:
        t = json.loads((ROOT / "runtime" / "runs" / f"{wid}.json").read_text(encoding="utf-8"))
        traces[wid] = t
        views = {v.id: v for v in views_of(t, geo)}
        ids = sorted(views)
        titles = {d: [t["items"][m]["title"] for m in t["developments"][str(d)]["members"] if m in t["items"]]
                  for d in ids}
        cent = {}
        for d in ids:
            v = np.mean(embed_texts(titles[d]), axis=0)
            cent[d] = v / (np.linalg.norm(v) + 1e-9)
        info = {d: (hazard_classes(views[d].text), bool(GATHERING.search(views[d].text)),
                    bool(REACTION.search(views[d].text))) for d in ids}
        for a, b in combinations(ids, 2):
            va, vb = views[a], views[b]
            if not (va.first and vb.first):
                continue
            key = frozenset((f"{wid}:D{a}", f"{wid}:D{b}"))
            if key in taken:
                continue
            gap = abs(va.first - vb.first)
            cos = float(cent[a] @ cent[b])
            shared = bool(va.principals & vb.principals)
            if "same_calamity_lifecycle" in types and gap <= EPISODE_GAP and info[a][0] and info[b][0] and (
                    info[a][0] & info[b][0] or any(geo.same_or_contains(x, y) for x in va.places for y in vb.places)):
                eligible["same_calamity_lifecycle"].append((cos, wid, a, b))
            if "same_convened_event" in types and gap <= EPISODE_GAP and info[a][1] and info[b][1] and shared:
                eligible["same_convened_event"].append((cos, wid, a, b))
            later = a if va.first > vb.first else b
            if "reaction_to" in types and va.first != vb.first and gap <= REACTION_GAP and info[later][2] and (
                    shared or cos >= 0.50):
                eligible["reaction_to"].append((cos, wid, a, b))

    drawn, hidden = [], {}
    for t in [x for x in ORDER if x in types]:
        ranked = sorted(eligible[t], key=lambda r: (-r[0], r[1], r[2], r[3]))
        n = 0
        for rank, (cos, wid, a, b) in enumerate(ranked, 1):
            key = frozenset((f"{wid}:D{a}", f"{wid}:D{b}"))
            if key in taken or n >= CAP:
                continue
            taken.add(key)
            n += 1
            tr = traces[wid]
            views_first = {d: side(tr, d, wid)["first"] for d in (a, b)}
            x, y = sorted((a, b), key=lambda d: (views_first[d] or "", d))
            drawn.append({"a": side(tr, x, wid), "b": side(tr, y, wid),
                          "_rule": {"targeted": t, "rank": rank, "cosine": round(cos, 3), "window": wid,
                                    "eligible": len(ranked)}})
        print(f"{t}: {len(ranked)} eligible, {n} drawn")
    random.Random(f"{SEED}:targeted:r{rnd}").shuffle(drawn)
    cases = []
    for n, c in enumerate(drawn, 1):
        cid = f"P{rnd}{n:02d}"
        hidden[cid] = c.pop("_rule")
        cases.append({"case": cid, **c})
    out.mkdir(parents=True)
    meta = {"design": "runtime-targeted-design.md", "round": rnd, "pools": POOLS[rnd], "types": types, "cap": CAP,
            "cases": len(cases)}
    (out / "cases.json").write_text(json.dumps({"meta": meta, "cases": cases}, indent=1, ensure_ascii=False) + "\n",
                                    encoding="utf-8", newline="\n")
    (out / "candidate-rules.json").write_text(json.dumps(hidden, indent=1, ensure_ascii=False) + "\n",
                                              encoding="utf-8", newline="\n")
    print(len(cases), "cases ->", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
