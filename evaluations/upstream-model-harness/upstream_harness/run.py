"""calibrate / score entry points. Both call the gold-completion checker first.

    python -m upstream_harness.run calibrate --gold-root G --track topic --features F --model pkg.mod:factory \
        (--high-min X --medium-min Y | --rule pkg.mod:fn) --out-dir OUT
    python -m upstream_harness.run score --gold-root G --track topic --features F --model pkg.mod:factory \
        --calibration OUT/calibrations/topic/<model_id>.json --out-dir OUT [--force-rescore --reason TEXT]

``factory()`` returns an object with ``model_id``, ``track`` and ``predict(case) -> (label, score)``.
No band boundary, selection rule or threshold has a default. ``score`` touches acceptance cases exactly once per model id.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .checker import GoldIncomplete, require_complete
from .common import TRACKS, canonical, git_state, now_utc, package_versions, sha256_bytes, sha256_file, sha256_text_lf, write_canonical
from .features import load_features
from .gold import GoldError, GoldTrack
from .metrics import BOOTSTRAP_N, BOOTSTRAP_SEED, TOPIC_PRECISION_BAR, build_records, evaluate_basis, verdict
from .model import Bands, calibrate, load_rule, predict_all
from .splits import SplitGuard, acquire_acceptance_lock


def run_metadata(gold: GoldTrack, features: dict, model_id: str, seed: int) -> dict:
    repo = Path(__file__).resolve().parent
    top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    return {**git_state(Path(top or repo)),
            "snapshot_sha256": features["header"]["snapshot_sha256"],
            "split_json_sha256_lf": sha256_text_lf(gold.split_path),
            "gold_labels_yaml_sha256": gold.label_file_sha(),
            "gold_history_sha256": sha256_file(gold.history_path) if gold.history_path.exists() else None,
            "gold_freeze_record_sha256": sha256_file(gold.freeze_path) if gold.freeze_path.exists() else None,
            "features_hash": features["content_hash"], "package_versions": package_versions(),
            "bootstrap_seed": seed, "timestamp_utc": now_utc(), "model_id": model_id}


def _load_model(spec: str, track: str):
    mod, _, fn = spec.partition(":")
    import importlib
    m = importlib.import_module(mod)
    model = getattr(m, fn)()
    if model.track != track:
        raise GoldError(f"model track {model.track!r} != requested {track!r}")
    return model


def do_calibrate(gold_root, track, features_path, model, out_dir, *, bands=None, rule=None, rule_name=None,
                 contains=None) -> dict:
    require_complete(gold_root, (track,), "development")
    gold = GoldTrack(Path(gold_root), track)
    features = load_features(features_path)
    guard = SplitGuard(gold, "calibration")
    out = Path(out_dir) / "calibrations" / track / f"{model.model_id}.json"
    rec = calibrate(model, features, guard, bands=bands, selection_rule=rule, selection_rule_name=rule_name,
                    contains=contains, out_path=out)
    rec["metadata"] = run_metadata(gold, features, model.model_id, BOOTSTRAP_SEED)
    rec["record_sha256"] = write_canonical(out, {k: v for k, v in rec.items() if k != "record_sha256"})
    return rec


def do_score(gold_root, track, features_path, model, calibration_path, out_dir, *, force_rescore=False, reason=None,
             contains=None, precision_bar=TOPIC_PRECISION_BAR, n_boot=BOOTSTRAP_N, seed=BOOTSTRAP_SEED) -> dict:
    # 1. gold completion first, before anything else
    require_complete(gold_root, (track,), "all")
    gold = GoldTrack(Path(gold_root), track)
    features = load_features(features_path)
    cal = json.loads(Path(calibration_path).read_text(encoding="utf-8"))
    dev_guard = SplitGuard(gold, "calibration")
    problems = []
    if cal.get("phase") != "calibration" or cal.get("track") != track or cal.get("model_id") != model.model_id:
        problems.append("calibration record is not for this track/model")
    if cal.get("features_hash") != features["content_hash"]:
        problems.append("calibration used different features")
    if cal.get("development_ids_sha256") != sha256_bytes(canonical(dev_guard.case_ids)):
        problems.append("calibration was not computed on exactly the development split")
    if problems:
        raise GoldError("; ".join(problems))
    bands = Bands(**cal["bands"])
    meta = run_metadata(gold, features, model.model_id, seed)
    # 2. acceptance-once lock (before any acceptance case is predicted)
    lock = acquire_acceptance_lock(Path(out_dir) / "locks", track, model.model_id,
                                   {"calibration_sha256": sha256_file(calibration_path), "bands": cal["bands"],
                                    "features_hash": features["content_hash"], "git_sha": meta["git_sha"]},
                                   force_rescore=force_rescore, force_reason=reason)
    guard = SplitGuard(gold, "acceptance")
    preds = predict_all(model, features, guard)
    prim, sec = guard.labels("primary"), guard.labels("secondary")
    recs = build_records(preds, bands, prim, sec, features, track)
    per_basis = {b: evaluate_basis(recs, b, track, contains, n_boot, seed) for b in ("primary", "secondary")}
    report = {"phase": "acceptance", "track": track, "model_id": model.model_id, "bands": cal["bands"],
              "calibration_selection": cal.get("selection"), "n": len(recs),
              "scoring_bases": {"primary": "first saved answer per case (blind)", "secondary": "final answer"},
              "per_basis": per_basis, "verdict": verdict(track, per_basis, precision_bar),
              "containment_table_supplied": bool(contains), "lock": str(lock), "metadata": meta}
    rp = Path(out_dir) / "reports" / track / f"{model.model_id}.acceptance.json"
    report["report_sha256_excluding_this_field"] = write_canonical(rp, report)
    write_canonical(rp, report)
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("calibrate", "score"):
        p = sub.add_parser(name)
        p.add_argument("--gold-root", required=True, type=Path)
        p.add_argument("--track", required=True, choices=TRACKS)
        p.add_argument("--features", required=True, type=Path)
        p.add_argument("--model", required=True)
        p.add_argument("--out-dir", required=True, type=Path)
        p.add_argument("--containment-json", type=Path, help="location only: {code: [contained codes]}")
        if name == "calibrate":
            p.add_argument("--high-min", type=float)
            p.add_argument("--medium-min", type=float)
            p.add_argument("--rule", help="module:function over development records -> Bands (owner decision)")
        else:
            p.add_argument("--calibration", required=True, type=Path)
            p.add_argument("--force-rescore", action="store_true")
            p.add_argument("--reason")
    a = ap.parse_args(argv)
    contains = None
    if a.containment_json:
        contains = {k: set(v) for k, v in json.loads(a.containment_json.read_text(encoding="utf-8")).items()}
    try:
        model = _load_model(a.model, a.track)
        if a.cmd == "calibrate":
            have = [a.high_min is not None and a.medium_min is not None, a.rule is not None]
            if sum(have) != 1:
                ap.error("pass either --high-min and --medium-min, or --rule (no default boundaries exist)")
            rec = do_calibrate(a.gold_root, a.track, a.features, model, a.out_dir,
                               bands=Bands(a.high_min, a.medium_min) if have[0] else None,
                               rule=load_rule(a.rule) if a.rule else None, rule_name=a.rule, contains=contains)
            print(json.dumps({k: rec[k] for k in ("model_id", "bands", "selection", "development_per_band")}, indent=1))
        else:
            if a.force_rescore and not a.reason:
                ap.error("--force-rescore requires --reason")
            rep = do_score(a.gold_root, a.track, a.features, model, a.calibration, a.out_dir,
                           force_rescore=a.force_rescore, reason=a.reason, contains=contains)
            print(json.dumps({"verdict": rep["verdict"], "n": rep["n"]}, indent=1))
    except GoldIncomplete as e:
        print(str(e), file=sys.stderr)
        print("REFUSED: gold is not complete; nothing was scored.", file=sys.stderr)
        return 1
    except GoldError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
