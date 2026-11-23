"""Metrics, both scoring bases, bootstrap CIs, verdicts.

Record = {"case", "lang", "label", "score", "band", "gold": {"primary": str, "secondary": str}}.

Definitions (all counts over the cases of one split):
  emitted(view)  : label is not an abstention AND band in view. Views: high_only = {high}; high_medium = {high, medium};
                   all_typed = every non-abstained prediction (diagnostic, not a consumable view).
  coverage       : emitted / n.            abstention : 1 - coverage.
  precision      : correct emitted / emitted (None if nothing emitted).
  recall         : correct emitted / n_recall_base. topic: cases whose gold is not `unknown` (an `unknown` gold has no
                   type to recall; an emitted type on it counts against precision). location: all cases.
  per class      : precision_c = correct emitted predicted c / emitted predicted c; recall_c = correct emitted of gold c
                   / support of gold c (support counts every gold-c case, emitted or not).
  confusion      : rows = gold label, columns = emitted label, or ABSTAIN for non-emitted cases.
Location: `correct` is exact-country agreement; the containment-aware variant is reported next to it (equal to exact when
no containment table is supplied). `other` counts as a typed topic label. MULTI / NONE are ordinary classes.
The bootstrap resamples cases with replacement (percentile interval, fixed seed).
"""
from __future__ import annotations

import random

from .model import correctness

VIEWS = {"high_only": ("high",), "high_medium": ("high", "medium"), "all_typed": ("high", "medium", "low")}
TOPIC_PRECISION_BAR = 0.90   # owner scoring bar, FREEZE.md 2026-11-23 ("topic precision >= 0.90"), applies to high_medium
BOOTSTRAP_SEED = 20261127
BOOTSTRAP_N = 2000
ABSTAIN = "ABSTAIN"


def _emitted(r, view, track) -> bool:
    from .model import is_abstain
    return (not is_abstain(track, r["label"])) and r["band"] in VIEWS[view]


def _basic(recs, basis, view, track, contains):
    n = len(recs)
    em = [r for r in recs if _emitted(r, view, track)]
    ok = [r for r in em if correctness(track, r["label"], r["gold"][basis], contains)["exact"]]
    ok_aware = [r for r in em if correctness(track, r["label"], r["gold"][basis], contains)["aware"]]
    base = [r for r in recs if not (track == "topic" and r["gold"][basis] == "unknown")]
    return {"n": n, "emitted": len(em), "correct": len(ok), "correct_containment_aware": len(ok_aware),
            "coverage": len(em) / n if n else None, "abstention": 1 - len(em) / n if n else None,
            "precision": len(ok) / len(em) if em else None,
            "precision_containment_aware": len(ok_aware) / len(em) if em else None,
            "recall": len(ok) / len(base) if base else None, "n_recall_base": len(base)}


def _scalar(recs, basis, view, track, contains, name):
    return _basic(recs, basis, view, track, contains)[name]


def bootstrap(recs, basis, view, track, contains, names=("precision", "recall", "coverage"),
              n_boot=BOOTSTRAP_N, seed=BOOTSTRAP_SEED, level=0.95):
    rng = random.Random(f"{seed}:{basis}:{view}")
    n = len(recs)
    draws = {k: [] for k in names}
    for _ in range(n_boot):
        samp = [recs[rng.randrange(n)] for _ in range(n)]
        b = _basic(samp, basis, view, track, contains)
        for k in names:
            if b[k] is not None:
                draws[k].append(b[k])
    lo_q, hi_q = (1 - level) / 2, 1 - (1 - level) / 2
    out = {}
    for k, v in draws.items():
        v.sort()
        out[k] = ({"lo": v[int(lo_q * (len(v) - 1))], "hi": v[int(round(hi_q * (len(v) - 1)))], "n_valid_draws": len(v)}
                  if v else None)
    return {"level": level, "n_boot": n_boot, "seed": seed, "intervals": out}


def _per_class(recs, basis, view, track):
    labels = sorted({r["gold"][basis] for r in recs} | {r["label"] for r in recs if _emitted(r, view, track)})
    out = {}
    for c in labels:
        pred_c = [r for r in recs if _emitted(r, view, track) and r["label"] == c]
        tp = [r for r in pred_c if r["gold"][basis] == c]
        sup = [r for r in recs if r["gold"][basis] == c]
        out[c] = {"predicted": len(pred_c), "tp": len(tp), "support": len(sup),
                  "precision": len(tp) / len(pred_c) if pred_c else None,
                  "recall": len(tp) / len(sup) if sup else None}
    return out


def _confusion(recs, basis, view, track):
    m: dict = {}
    for r in recs:
        col = r["label"] if _emitted(r, view, track) else ABSTAIN
        m.setdefault(r["gold"][basis], {}).setdefault(col, 0)
        m[r["gold"][basis]][col] += 1
    return {k: dict(sorted(v.items())) for k, v in sorted(m.items())}


def evaluate_basis(recs, basis, track, contains=None, n_boot=BOOTSTRAP_N, seed=BOOTSTRAP_SEED) -> dict:
    out = {}
    for view in VIEWS:
        v = _basic(recs, basis, view, track, contains)
        v["ci"] = bootstrap(recs, basis, view, track, contains, n_boot=n_boot, seed=seed)
        v["per_class"] = _per_class(recs, basis, view, track)
        v["confusion"] = _confusion(recs, basis, view, track)
        langs = sorted({r["lang"] for r in recs})
        v["by_language"] = {l: {k: _basic([r for r in recs if r["lang"] == l], basis, view, track, contains)[k]
                                for k in ("n", "emitted", "coverage", "abstention", "precision")} for l in langs}
        if track == "location":
            v["none"] = {"precision": v["per_class"].get("NONE", {}).get("precision"),
                         "recall": v["per_class"].get("NONE", {}).get("recall")}
            v["multi"] = {"precision": v["per_class"].get("MULTI", {}).get("precision"),
                          "recall": v["per_class"].get("MULTI", {}).get("recall")}
        else:
            unk = [r for r in recs if r["gold"][basis] == "unknown"]
            v["gold_unknown"] = {"n": len(unk), "abstained": sum(not _emitted(r, view, track) for r in unk),
                                 "emitted_a_type": sum(_emitted(r, view, track) for r in unk)}
        out[view] = v
    return out


def verdict(track: str, per_basis: dict, bar: float | None = TOPIC_PRECISION_BAR) -> dict:
    """Topic: high_medium precision >= bar (owner bar from FREEZE.md), per basis; INCONCLUSIVE if the bases differ.
    Location: no approved or PROPOSED threshold exists, so metrics only."""
    if track != "topic":
        return {"verdict": None, "note": "no approved or PROPOSED threshold for this track; metrics reported without verdict"}
    res = {}
    for basis, ev in per_basis.items():
        p = ev["high_medium"]["precision"]
        res[basis] = "NOT_EVALUABLE" if p is None else ("PASS" if p >= bar else "FAIL")
    vals = set(res.values())
    overall = vals.pop() if len(vals) == 1 else "INCONCLUSIVE"
    return {"rule": f"high_medium precision >= {bar} (owner bar, FREEZE.md; point estimate, CI not used)",
            "per_basis": res, "verdict": overall}


def build_records(preds: dict, bands, prim: dict, sec: dict, features: dict, track: str) -> list[dict]:
    key = "event_country" if track == "location" else "action_type"
    recs = []
    for i in sorted(preds):
        label, score = preds[i]
        recs.append({"case": i, "lang": features["cases"][str(i)].get("lang"), "label": label, "score": score,
                     "band": bands.band(score), "gold": {"primary": prim[i][key], "secondary": sec[i][key]}})
    return recs
