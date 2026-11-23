"""Chronological replay of the Situation v2 candidate against a COPY of a snapshot.

Default mode is smoke: the first --limit Developments (default 50), current stored-value providers, output labelled
SMOKE / NOT A RESULT, no label read. Final mode refuses unless the guards pass (see chrono_replay/guard.py and README).

  HF_HUB_OFFLINE=1 PYTHONPATH=<worktree> <main .venv python> run_replay.py \
      --snapshot <gold-snap.db> --evalset-dir <frozen evalset> --out-root <dir>
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from chrono_replay import guard                                            # noqa: E402
from chrono_replay.providers import (ComponentEvidenceProvider, FrozenPredictions, ModelLocationProvider,  # noqa: E402
                                     ModelPrincipalsProvider, ModelTopicProvider, StoredLocationProvider,
                                     StoredPrincipalsProvider, StoredTopicProvider)
from chrono_replay.util import load_pins, sha256_file, verify              # noqa: E402

SMOKE_DEFAULT_LIMIT = 50


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=("smoke", "final"), default="smoke")
    ap.add_argument("--snapshot", type=Path, required=True, help="read-only snapshot db (a backup-API copy is used)")
    ap.add_argument("--snapshot-sha256", help="default: the pinned gold snapshot hash")
    ap.add_argument("--evalset-dir", type=Path, help="frozen v2 eval set (cases/key/scopes/subsample manifest)")
    ap.add_argument("--out-root", type=Path, default=HERE / "runs")
    ap.add_argument("--limit", type=int, help="smoke only: number of Developments (default %d)" % SMOKE_DEFAULT_LIMIT)
    ap.add_argument("--topic", default="stored", help="'stored' or a frozen predictions .jsonl (model)")
    ap.add_argument("--location", default="stored", help="'stored' or a frozen predictions .jsonl (model)")
    ap.add_argument("--principals", default="stored", help="'stored' or a frozen predictions .jsonl (model)")
    ap.add_argument("--components", default="pinned", help="'pinned', a report-components JSONL path, or 'none'")
    ap.add_argument("--mixed-from", choices=("v4", "none"), default="none",
                    help="engine mixed flag: none (default; component evidence has no downstream use, owner 2026-11-23) "
                         "or v4 (explicit opt-in, OWNER DECISION PENDING)")
    ap.add_argument("--owner-approved", help="reference to the owner's approval of the final run (final mode)")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = parse_args(argv)
    pins = load_pins()
    sys.path.insert(0, str(Path.cwd()))
    from chrono_replay import snapshot as snap

    worktree = Path(os.environ.get("PYTHONPATH", "").split(os.pathsep)[0] or Path.cwd()).resolve()
    git = snap.git_state(worktree, exclude=["evaluations/situation-membership/chrono-replay-v1/runs"])

    def pred(arg):
        return None if arg == "stored" else FrozenPredictions(Path(arg))

    topic_pred, loc_pred, pr_pred = pred(a.topic), pred(a.location), pred(a.principals)
    if a.mode == "final":
        labels_present = bool(a.evalset_dir and (a.evalset_dir / "subsample" / "LABELS-FREEZE-subsample.json").exists())
        guard.require_final(topic=topic_pred, location=loc_pred, owner_approved=a.owner_approved, limit=a.limit,
                            evalset_labels_present=labels_present, git_dirty=git["dirty"],
                            mixed_from=a.mixed_from)
        limit = None
    else:
        if a.owner_approved:
            print("note: --owner-approved is ignored in smoke mode", file=sys.stderr)
        limit = a.limit if a.limit is not None else SMOKE_DEFAULT_LIMIT

    engine = snap.load_engine(HERE / pins["engine"]["path"], pins["engine"]["sha256"])
    seeded_path = HERE / pins["seeded_scopes"]["path"]
    verify(seeded_path, pins["seeded_scopes"]["sha256"], "seeded scopes")
    snapshot_sha = a.snapshot_sha256 or pins["default_snapshot"]["sha256"]

    evalset = None
    if a.evalset_dir:
        for rel, h in pins["evalset"]["files"].items():
            verify(a.evalset_dir / rel, h, f"eval set {rel}")

    import yaml
    from osint_monitor.core.config import load_situations_config
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.development_segmentation import REPORT, LOCATION_TYPES, gazetteer, headline_kind
    from osint_monitor.processors.entity_resolver import normalise
    from osint_monitor.processors.geography import Gazetteer
    from osint_monitor.processors.principals import _lead
    from osint_monitor.processors.situations.canonical import ActorCanonicalizer

    tmp = snap.make_tmpdir()
    try:
        conn, _copy = snap.copy_snapshot(a.snapshot, snapshot_sha, tmp)
        norm = ActorNormalizer.load()
        canon = ActorCanonicalizer(normalizer=norm)
        geo = gazetteer(False)
        geo_sha = sha256_file(worktree / "config" / "geography.yaml")

        providers = {
            "topic": ModelTopicProvider(topic_pred) if topic_pred else StoredTopicProvider(conn, engine.family_of),
            "location": (ModelLocationProvider(loc_pred) if loc_pred else
                         StoredLocationProvider(conn, geo, norm, normalise, tuple(LOCATION_TYPES), geo_sha)),
            "principals": (ModelPrincipalsProvider(pr_pred, canon.keys) if pr_pred else
                           StoredPrincipalsProvider(conn, canon.keys)),
        }
        if a.components != "none":
            cpath = HERE / pins["component_evidence"]["path"] if a.components == "pinned" else Path(a.components)
            if a.components == "pinned":
                verify(cpath, pins["component_evidence"]["sha256"], "component evidence")
            providers["components"] = ComponentEvidenceProvider(cpath, pins["component_evidence"]["algorithm_version"])

        def party_countries(keys) -> set:
            return {geo.canonical(k) for k in keys if geo.is_country(k)}

        seeded_meta = {x["slug"]: x for x in yaml.safe_load(seeded_path.read_text(encoding="utf-8"))["situations"]}
        seed_cfgs = load_situations_config().situations

        def seeded_factory():
            return snap.build_seeded(engine, seeded_meta, seed_cfgs, canon, party_countries)

        bases = snap.load_bases(conn, engine, headline_kind, REPORT, _lead)

        labels = None
        if a.evalset_dir:
            ev = a.evalset_dir
            key = json.loads((ev / "key.json").read_text(encoding="utf-8"))["cases"]
            scopes = json.loads((ev / "scopes.json").read_text(encoding="utf-8"))
            cases = json.loads((ev / "cases.json").read_text(encoding="utf-8"))["cases"]
            case_ids = json.loads((ev / "subsample" / "manifest.json").read_text(encoding="utf-8"))["case_ids"]
            evalset = {
                "key": key, "scopes": scopes, "case_ids": case_ids,
                "anchors_of": {x["slug"]: canon.keys(x["primary_actors"]) for x in scopes["automatic"]},
                "founders_of": {x["slug"]: {f["development_id"] for f in x["founders"]} for x in scopes["automatic"]},
                "alignment": snap_alignment(conn, cases, snap),
            }
            if a.mode == "final":
                labels = load_final_labels(ev)

        from chrono_replay.runner import execute
        git_now = snap.git_state(worktree, exclude=["evaluations/situation-membership/chrono-replay-v1/runs"])
        identity = {"snapshot_sha256": snapshot_sha, "engine_sha256": pins["engine"]["sha256"],
                    "seeded_scopes_sha256": pins["seeded_scopes"]["sha256"],
                    "config_sha256": snap.config_hashes(worktree)}
        extra = {"git": git_now, "snapshot": {"name": a.snapshot.name, "sha256": snapshot_sha, "opened": "read-only; "
                 "backup-API copy in a temporary directory, query_only"},
                 "pins": pins, "config_sha256": identity["config_sha256"],
                 "evalset_dir_files": ({rel: sha256_file(a.evalset_dir / rel) for rel in pins["evalset"]["files"]}
                                       if a.evalset_dir else None),
                 "guard": {"final_requires": "see chrono_replay/guard.py", "owner_approved": a.owner_approved
                           if a.mode == "final" else None}}
        res = execute(engine=engine, bases=bases, providers=providers, seeded_factory=seeded_factory,
                      party_countries=party_countries, mode=a.mode, limit=limit, mixed_from=a.mixed_from,
                      out_root=a.out_root, identity=identity, manifest_extra=extra, evalset=evalset, labels=labels)
        conn.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    s = res["summary"]
    print(f"{s['status']}: wrote {res['out']}")
    print(f"trace rows {s['trace_rows']}; engine parity {s['engine_parity']['engine_chronological_equal']}")
    return 0


def snap_alignment(conn, cases, snap):
    from chrono_replay import metrics
    return metrics.evalset_alignment(cases, conn, snap.parse_ts)


def load_final_labels(ev: Path) -> dict[str, str]:
    """Final mode only: the frozen owner labels through the frozen scorer's own loader (unchanged, from --evalset-dir)."""
    sys.path[:0] = [str(ev / "subsample"), str(ev)]
    import score_subsample
    frozen = score_subsample.load_frozen_labels(ev / "subsample")
    return {c: e["label"] for c, e in frozen.items()}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
