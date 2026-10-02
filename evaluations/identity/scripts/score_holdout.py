"""One-time holdout scoring for Phase 2 (identity gold revision 2, the 30 sealed holdout cases).

Two steps, each run once:

  --freeze   record the frozen implementation (branch, HEAD, clean tree, config hash, model versions, benchmark and
             gold hashes) in runs/phase2-holdout-freeze.json. Commit that file before scoring.
  --score    refuse unless the freeze record exists, HEAD and the tree still match it, and no holdout result exists;
             replay the holdout window twice (determinism) and score run 1 against the holdout labels, once.
             Writes runs/phase2-holdout.json.

Holdout labels are read only in --score.
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
FREEZE = ROOT / "runs" / "phase2-holdout-freeze.json"
RESULT = ROOT / "runs" / "phase2-holdout.json"


def git(*args) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_dirty() -> bool:
    return bool(git("status", "--porcelain", "--untracked-files=no"))


def freeze() -> int:
    from osint_monitor.core.runs import config_hash, model_versions
    if tracked_dirty():
        print("refusing: tracked files have uncommitted changes")
        return 1
    if FREEZE.exists():
        print("refusing: a freeze record already exists")
        return 1
    record = {
        "frozen_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "branch": git("branch", "--show-current"), "head": git("rev-parse", "HEAD"),
        "config_hash": config_hash(), "models": model_versions(),
        "benchmarks": {
            "clustering_manifest": sha(REPO / "evaluations" / "clustering" / "manifest.yaml"),
            "entity_gold_manifest": sha(REPO / "evaluations" / "entities" / "gold" / "manifest.yaml"),
            "identity_windows_manifest": sha(ROOT / "manifest.yaml"),
        },
        "identity_gold": {"revision": 2, "sha256": sha(ROOT / "gold" / "identity-gold.yaml"),
                          "manifest_sha256": sha(ROOT / "gold" / "manifest.yaml")},
        "rule": "no code change after holdout scoring begins; the holdout is scored exactly once",
    }
    FREEZE.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(record, indent=1))
    return 0


def score_holdout() -> int:
    import yaml

    import replay_current
    from phase2_baseline import comparable, diff_traces, score
    if not FREEZE.exists():
        print("refusing: no freeze record (run --freeze and commit it first)")
        return 1
    rec = json.loads(FREEZE.read_text(encoding="utf-8"))
    head = git("rev-parse", "HEAD")
    frozen_commit = git("log", "-1", "--format=%H", "--", str(FREEZE.relative_to(REPO)))
    changed = git("diff", "--name-only", rec["head"], head, "--", "osint_monitor", "config")
    if tracked_dirty() or changed or not frozen_commit:
        print(f"refusing: code/config differ from the frozen head ({changed or 'tree dirty or freeze not committed'})")
        return 1
    if RESULT.exists():
        print("refusing: the holdout has already been scored")
        return 1
    if sha(ROOT / "gold" / "identity-gold.yaml") != rec["identity_gold"]["sha256"]:
        print("refusing: identity gold changed since the freeze")
        return 1
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    window = next(w for w in manifest["windows"] if w["split"] == "holdout")
    runs = [replay_current.replay(window) for _ in range(2)]
    diffs = diff_traces(comparable(runs[0]), comparable(runs[1]))
    gold = {k: v for k, v in yaml.safe_load((ROOT / "gold" / "identity-gold.yaml").read_text(encoding="utf-8")).items()
            if v["split"] == "holdout"}                                   # labels opened here, once
    assert len(gold) == 30, len(gold)
    result = score(runs[0], gold)
    out = {"scored_at": datetime.utcnow().isoformat(timespec="seconds") + "Z", "freeze": rec, "scored_head": head,
           "window": window["id"], "cases": len(gold), "result": result,
           "determinism": {"identical": not diffs, "diffs": diffs[:10]}}
    RESULT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    traces = ROOT / "runs" / "phase2-holdout-traces"
    traces.mkdir(parents=True, exist_ok=True)
    (traces / f"{window['id']}.json").write_text(json.dumps(comparable(runs[0]), indent=1, ensure_ascii=False) + "\n",
                                                 encoding="utf-8", newline="\n")
    print(json.dumps({"window": window["id"], "tally": result["tally"], "determinism": not diffs}, indent=1))
    return 0


if __name__ == "__main__":
    if "--freeze" in sys.argv:
        raise SystemExit(freeze())
    if "--score" in sys.argv:
        raise SystemExit(score_holdout())
    print(__doc__)
    raise SystemExit(2)
