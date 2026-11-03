"""Score the labelling subsample against the owner's frozen subsample labels. NOT RUN ON REAL LABELS YET.

Requires LABELS-FREEZE-subsample.json (labels_subsample.py freeze) and a separate owner approval (--approval). The
metrics and PROPOSED gates are ../score.py's, unchanged (imported); only the cases are restricted to the manifest. The
positive-seed gate is reported on the seeded-Situation subset (SUBSAMPLE.md section 4), with all positive seeds next
to it for information.

  python score_subsample.py --approval "<who, when, what>" [--candidate-decisions FILE] [--out FILE]
  python score_subsample.py --self-test
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
EVALSET = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(EVALSET))
import labels_subsample  # noqa: E402
import labels_tool  # noqa: E402
import score  # noqa: E402

SEED_GATE_BASIS = "seeded_situations_only"


def load_frozen_labels(d: Path = HERE) -> dict[str, dict]:
    lf = d / labels_subsample.LABELS_FREEZE_FILE
    if not lf.exists():
        sys.exit(f"no {labels_subsample.LABELS_FREEZE_FILE}: subsample labels must be frozen before scoring")
    rec = json.loads(lf.read_text(encoding="utf-8"))
    if labels_tool.sha256(d / labels_subsample.LABELS_FILE) != rec["labels_sha256"]:
        sys.exit(f"{labels_subsample.LABELS_FILE} changed after the freeze")
    errors = labels_subsample.validate(d)
    if errors:
        sys.exit("labels or frozen files not valid:\n  " + "\n  ".join(errors[:20]))
    labels = yaml.safe_load((d / labels_subsample.LABELS_FILE).read_text(encoding="utf-8"))
    return {e["case_id"]: e for e in labels["cases"]}


def score_restricted(labels: dict, key: dict, ids: list[str], candidate: tuple[str, dict] | None) -> dict:
    key = {c: key[c] for c in ids}
    if set(labels) != set(key):
        sys.exit("labels and manifest cover different cases")
    systems = [score.score_system("current_runtime", labels, score.runtime_decisions(key), key, with_audit=False)]
    if candidate:
        name, dec = candidate
        systems.append(score.score_system(f"candidate: {name}", labels, {c: dec[c] for c in key}, key,
                                          with_audit=True))
    for s in systems:
        g = s["gates_proposed"]["positive_seed_regressions"]
        g["gate_basis"] = SEED_GATE_BASIS
        g["value"] = g["value_seeded_situations_only"]
    return {"cases": len(key), "systems": systems}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--approval")
    ap.add_argument("--candidate-decisions", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        key = {"S001": {"situation": "a-b", "situation_kind": "seeded", "seed_group": "positive", "current_member": False},
               "S002": {"situation": "c-d", "situation_kind": "automatic", "seed_group": "positive", "current_member": False},
               "S003": {"situation": "c-d", "situation_kind": "automatic", "seed_group": None, "current_member": True},
               "S004": {"situation": "c-d", "situation_kind": "automatic", "seed_group": None, "current_member": True}}
        labels = {c: {"label": l} for c, l in (("S001", "MEMBER"), ("S002", "MEMBER"), ("S003", "NOT_MEMBER"))}
        r = score_restricted(labels, key, ["S001", "S002", "S003"], None)
        g = r["systems"][0]["gates_proposed"]["positive_seed_regressions"]
        assert r["cases"] == 3 and g["value"] == 1 and g["value_all"] == 2, g
        print("self-test passed (synthetic; nothing read or written)")
        return
    if not (a.approval and a.approval.strip()):
        sys.exit("scoring needs a separate owner approval: pass --approval")
    labels = load_frozen_labels()
    key = score.load_key(EVALSET)
    ids = labels_subsample.manifest_ids()
    cand = score.load_candidate_decisions(a.candidate_decisions, key) if a.candidate_decisions else None
    report = {"approval": a.approval, "subsample": "manifest.json",
              "labels_freeze": json.loads((HERE / labels_subsample.LABELS_FREEZE_FILE).read_text(encoding="utf-8")),
              **score_restricted(labels, key, ids, cand)}
    text = json.dumps(report, indent=1, ensure_ascii=False)
    if a.out:
        a.out.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
