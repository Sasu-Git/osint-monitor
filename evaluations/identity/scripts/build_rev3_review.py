"""Identity gold revision 3: review set for the owner (cross-language candidates + owner-given verdicts).

    python evaluations/identity/scripts/build_rev3_review.py
      -> review-rev3/review-cases.json, owner-verdicts.yaml (owner-given cases pre-filled), labeller-input.md

Cases:
- G-cases: verdicts the owner already gave (2026-10-07: Phase 3 identity suspects, the D19 split, the
  cross-language regression pairs). Pre-filled, not reviewed again.
- V-cases: a stratified sample of the cross-language candidate pairs (xlang_candidates.py). For each proposed unit
  pair, the cross-language item pair with the highest multilingual cosine. Duplicates and pairs already in the
  identity gold are dropped. The sample is stratified by cosine band and by whether the anchor guard accepted it.
  **The guard's decision is not shown**: the review is blind to the stage under test.

Development windows only; the identity holdout is never used.
"""
import json
import os
import random
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-rev3"
SEED, PER_STRATUM = 20261008, 10
BANDS = [(0.55, 0.65), (0.65, 0.75), (0.75, 1.01)]

import yaml  # noqa: E402

GIVEN = [  # case, window, a, b, verdict, owner basis
    ("G01", "2026-09-30-multilingual", "sx-100", "sx-170", "SAME_DEVELOPMENT", "R012: one matter, BBC / France 24"),
    ("G02", "2026-09-30-multilingual", "sx-132", "sx-168", "SAME_DEVELOPMENT", "R138: White House AI luncheon, it / en"),
    ("G03", "2026-09-30-multilingual", "sx-263", "sx-168", "SAME_DEVELOPMENT", "R138: America.gov launch at the luncheon, es / en"),
    ("G04", "2026-10-03-live", "s-1124", "s-1316", "SAME_DEVELOPMENT", "T008: Spain's eviction measures, same day"),
    ("G05", "2026-10-03-live", "s-1200", "s-1233", "SAME_DEVELOPMENT", "T034: evicted woman returns home"),
    ("G06", "2026-10-03-live", "s-1525", "s-1663", "SAME_DEVELOPMENT", "T041: Tennessee halts executions (Christa Pike)"),
    ("G07", "2026-10-03-live", "s-1228", "s-1380", "DIFFERENT_DEVELOPMENT", "T025: two days of the protest wave"),
    ("G08", "2026-09-30-multilingual", "sx-535", "sx-536", "SAME_DEVELOPMENT", "T033: rial record low (GDELT)"),
    ("G09", "2026-09-30-multilingual", "sx-540", "sx-536", "SAME_DEVELOPMENT", "T039: rial record low (GDELT)"),
    ("G10", "2026-09-30-multilingual", "sx-264", "sx-75", "DIFFERENT_DEVELOPMENT", "D19 split: rial low vs US response"),
    ("G11", "2026-09-30-multilingual", "sx-536", "sx-75", "DIFFERENT_DEVELOPMENT", "D19 split: rial low vs US response"),
    ("G12", "2026-10-05-live", "s-2277", "s-2623", "SAME_DEVELOPMENT", "regression: RAF Fairford bombers, en / es"),
    ("G13", "2026-10-05-live", "s-2314", "s-2639", "SAME_DEVELOPMENT", "regression: RAF Fairford bombers, en / es"),
    ("G14", "2026-10-05-live", "s-2299", "s-2432", "SAME_DEVELOPMENT", "regression: Siberian plague case, en / es"),
]


def main() -> int:
    from osint_monitor.processors.cross_language import model_and_revision
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    windows = {w["id"]: w for w in manifest["windows"]}
    items = {}
    for wid in {g[1] for g in GIVEN} | {"2026-09-30-multilingual", "2026-10-03-live", "2026-10-05-live"}:
        for line in (ROOT / windows[wid]["items_file"]).read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                items[(wid, r["id"])] = r
    gold = yaml.safe_load((ROOT / "gold" / "identity-gold.yaml").read_text(encoding="utf-8"))
    in_gold = {(c["window"], frozenset((c["a"], c["b"]))) for c in gold.values()}
    in_gold |= {(w, frozenset((a, b))) for _, w, a, b, _, _ in GIVEN}

    model, rev = model_and_revision("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    cand = json.loads((OUT / "xlang-candidates.json").read_text(encoding="utf-8"))["pairs"]
    text = lambda r: f"{r['title']}. {(r.get('excerpt') or '')[:300]}"          # noqa: E731
    keys = sorted({(p["window"], i) for p in cand for i in p["a"] + p["b"]})
    vec = dict(zip(keys, model.encode([text(items[k]) for k in keys], normalize_embeddings=True)))
    best = {}
    for p in cand:
        if p["cosine"] < BANDS[0][0]:
            continue
        w = p["window"]
        pairs = [(float(vec[(w, a)] @ vec[(w, b)]), a, b) for a in p["a"] for b in p["b"]
                 if (items[(w, a)].get("lang") or "en") != (items[(w, b)].get("lang") or "en")]
        if not pairs:
            continue
        cos, a, b = max(pairs)
        key = (w, frozenset((a, b)))
        if key in in_gold:
            continue
        if key not in best or cos > best[key]["cos"]:
            best[key] = {"window": w, "a": a, "b": b, "cos": round(cos, 3), "accepted": p["accepted"]}
    rng = random.Random(SEED)
    sample = []
    for lo, hi in BANDS:
        for acc in (True, False):
            stratum = sorted((x for x in best.values() if lo <= x["cos"] < hi and x["accepted"] == acc),
                             key=lambda x: (x["window"], x["a"], x["b"]))
            rng.shuffle(stratum)
            sample += stratum[:PER_STRATUM]
    rng.shuffle(sample)

    def item_view(w, i):
        r = items[(w, i)]
        return {"id": i, "published_at": r.get("published_at"), "source": r["source"], "source_type": r.get("source_type"),
                "lang": r.get("lang"), "title": r["title"], "excerpt": (r.get("excerpt") or "")[:600]}

    cases, strata = [], {}
    for n, x in enumerate(sample, 1):
        cid = f"V{n:03d}"
        cases.append({"case": cid, "window": x["window"], "split": "development",
                      "items": [item_view(x["window"], x["a"]), item_view(x["window"], x["b"])],
                      "multilingual": True, "flags": [],
                      "system": {"relation": "cross-language candidate", "why": ["proposed by multilingual similarity"],
                                 "rules": ["xlang"], "same_developments": [], "item_developments": [[], []],
                                 "developments": {}, "cosine": None}})
        strata[cid] = {"cosine": x["cos"], "guard_accepted": x["accepted"]}
    for cid, w, a, b, verdict, basis in GIVEN:
        cases.append({"case": cid, "window": w, "split": "development", "items": [item_view(w, a), item_view(w, b)],
                      "multilingual": (items[(w, a)].get("lang") != items[(w, b)].get("lang")), "flags": ["owner-given"],
                      "system": {"relation": "owner-given verdict", "why": [basis], "rules": ["given"],
                                 "same_developments": [], "item_developments": [[], []], "developments": {},
                                 "cosine": None}})
    OUT.mkdir(exist_ok=True)
    (OUT / "review-cases.json").write_text(json.dumps(cases, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "strata.json").write_text(json.dumps({"model_revision": rev, "strata": strata}, indent=1) + "\n",
                                     encoding="utf-8")
    verdicts = {c["case"]: {"verdict": None, "confidence": None, "boundary_reason": None, "note": None,
                            "reviewed_at": None} for c in cases}
    for cid, _, _, _, verdict, basis in GIVEN:
        verdicts[cid] = {"verdict": verdict, "confidence": "high", "boundary_reason": None,
                         "note": f"owner, 2026-10-07: {basis}", "reviewed_at": "2026-10-07T00:00:00Z"}
    (OUT / "owner-verdicts.yaml").write_text(yaml.safe_dump(verdicts, sort_keys=True, allow_unicode=True, width=120),
                                             encoding="utf-8")
    lines = ["# Identity labelling input, revision 3 (blind)", "",
             "For each case decide SAME_DEVELOPMENT / DIFFERENT_DEVELOPMENT / AMBIGUOUS under the identity contract:",
             "one Development is one coherent real-world occurrence (same action or event, whatever the language,",
             "outlet or detail); distinct actions inside one crisis, summit or campaign are DIFFERENT.", ""]
    for c in cases:
        if c["case"].startswith("G"):
            continue
        lines.append(f"## {c['case']}")
        for tag, it in zip("AB", c["items"]):
            lines.append(f"**{tag}** {str(it['published_at'])[:16]} [{it['source']}] ({it['lang']}) {it['title']}")
            if it["excerpt"]:
                lines.append(f"> {it['excerpt'][:300]}")
        lines.append("")
    (OUT / "labeller-input.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(sample)} candidate cases ({len(best)} distinct pairs), {len(GIVEN)} owner-given")
    return 0


if __name__ == "__main__":
    sys.exit(main())
