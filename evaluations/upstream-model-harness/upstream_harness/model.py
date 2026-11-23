"""Model interface, confidence bands and the development-only calibration step.

The band boundaries are parameters with NO default. A caller passes explicit ``Bands`` or a ``selection_rule``
(callable over development records only). Any selection rule is an owner decision; none is provided here.
"""
from __future__ import annotations

import importlib
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

from .common import canonical, sha256_bytes, write_canonical
from .gold import GoldError
from .splits import SplitGuard

ABSTAIN_LABELS = {None, "unknown"}      # topic: `unknown` is the abstention class; location: None only
LOCATION_ABSTAIN = {None}


class Model(Protocol):
    model_id: str
    track: str  # "topic" | "location"

    def predict(self, case: dict) -> tuple[str | None, float]:
        """case = one entry of the features file (no gold, no stored system output). Returns (label, confidence_score).
        label None (or `unknown` for topic) = abstain. Topic label = action_type incl. out_of_scope; location label =
        ISO3 | NONE | MULTI | SEA_OR_REGION | DISPUTED."""


def is_abstain(track: str, label) -> bool:
    return label in (ABSTAIN_LABELS if track == "topic" else LOCATION_ABSTAIN)


@dataclass(frozen=True)
class Bands:
    high_min: float
    medium_min: float   # no defaults on purpose

    def __post_init__(self):
        for v in (self.high_min, self.medium_min):
            if not isinstance(v, (int, float)) or math.isnan(v):
                raise ValueError("band boundaries must be numbers")
        if self.medium_min > self.high_min:
            raise ValueError("medium_min must be <= high_min")

    def band(self, score: float) -> str:
        if score >= self.high_min:
            return "high"
        if score >= self.medium_min:
            return "medium"
        return "low"


def _match(track: str, pred, gold, contains: dict | None) -> dict:
    """exact and containment-aware correctness of one emitted prediction.

    Topic: exact label equality (containment-aware == exact). Location: ``contains`` maps a code to the set of codes it
    contains (caller-supplied; None = no table chosen, containment-aware then equals exact)."""
    exact = pred == gold
    aware = exact
    if track == "location" and not exact and contains:
        aware = gold in contains.get(pred, ()) or pred in contains.get(gold, ())
    return {"exact": exact, "aware": aware}


def correctness(track: str, pred, gold, contains: dict | None = None) -> dict:
    return _match(track, pred, gold, contains)


def predict_all(model: Model, features: dict, guard: SplitGuard) -> dict[int, tuple[str | None, float]]:
    out = {}
    for i in guard.case_ids:
        guard.check_id(i)
        label, score = model.predict(features["cases"][str(i)])
        if not isinstance(score, (int, float)) or math.isnan(score):
            raise GoldError(f"model returned a non-numeric score for D{i}")
        out[i] = (label, float(score))
    return out


def load_rule(spec: str) -> Callable:
    mod, _, fn = spec.partition(":")
    return getattr(importlib.import_module(mod), fn)


def calibrate(model: Model, features: dict, guard: SplitGuard, *, bands: Bands | None = None,
              selection_rule: Callable | None = None, selection_rule_name: str | None = None,
              contains: dict | None = None, out_path: Path | None = None) -> dict:
    """Development-only. Returns (and optionally writes) the calibration record holding the band boundaries.

    Exactly one of ``bands`` / ``selection_rule`` must be given. ``selection_rule(dev_records) -> Bands`` sees only
    development records (id, label, score, correct flags per basis); it never sees acceptance cases or label values.
    """
    if guard.phase != "calibration":
        raise GoldError("calibrate() requires a calibration-phase SplitGuard")
    if (bands is None) == (selection_rule is None):
        raise ValueError("pass exactly one of bands or selection_rule (no default boundaries exist)")
    preds = predict_all(model, features, guard)
    prim, sec = guard.labels("primary"), guard.labels("secondary")
    key = "event_country" if model.track == "location" else "action_type"
    recs = []
    for i in guard.case_ids:
        label, score = preds[i]
        r = {"case": i, "label": label, "score": score, "abstain": is_abstain(model.track, label)}
        for name, basis in (("primary", prim), ("secondary", sec)):
            m = _match(model.track, label, basis[i][key], contains) if not r["abstain"] else None
            r[f"correct_{name}"] = None if m is None else m["aware"]
        recs.append(r)
    if selection_rule is not None:
        bands = selection_rule(recs)
        how = selection_rule_name or getattr(selection_rule, "__name__", "rule")
    else:
        how = "explicit"
    per_band = {}
    for b in ("high", "medium", "low"):
        rs = [r for r in recs if not r["abstain"] and bands.band(r["score"]) == b]
        per_band[b] = {"n": len(rs)}
        for name in ("primary", "secondary"):
            c = sum(bool(r[f"correct_{name}"]) for r in rs)
            per_band[b][f"precision_{name}"] = (c / len(rs)) if rs else None
    rec = {"phase": "calibration", "track": model.track, "model_id": model.model_id,
           "bands": {"high_min": bands.high_min, "medium_min": bands.medium_min}, "selection": how,
           "features_hash": features["content_hash"],
           "development_ids_sha256": sha256_bytes(canonical(guard.case_ids)),
           "n_development": len(recs), "development_per_band": per_band, "development_records": recs}
    if out_path is not None:
        rec["record_sha256"] = write_canonical(Path(out_path), rec)
    return rec
