"""Score the subsample on the owner's FIRST saved answer per case (the blind labels). Owner decision 2026-11-10.

Primary basis = the first line per case in owner-label-history.jsonl (``baseline`` lines included: labels saved before
the second opinion existed). Secondary basis = the frozen final labels, scored by score_subsample.py unchanged.

Uses score_subsample.score_restricted and ../score.py unchanged (imported). Refuses to run unless the final labels are
frozen and the history file matches the hash given with --history-sha256 (recorded in the freeze commit).

  python score_first_answers.py --approval "<who, when, what>" --history-sha256 <hex> [--out FILE]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import labels_subsample  # noqa: E402
import score  # noqa: E402
import score_subsample  # noqa: E402

HISTORY = HERE / "owner-label-history.jsonl"


def first_answers(ids: list[str]) -> dict[str, dict]:
    first: dict[str, dict] = {}
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            first.setdefault(rec["case"], rec)
    missing = [c for c in ids if c not in first]
    if missing:
        sys.exit(f"no history line for {len(missing)} cases, e.g. {missing[:5]}")
    return {c: {"case_id": c, "label": first[c]["label"], "reason": first[c].get("reason")} for c in ids}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--approval", required=True)
    ap.add_argument("--history-sha256", required=True)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    score_subsample.load_frozen_labels()  # final labels must be frozen and valid
    got = hashlib.sha256(HISTORY.read_bytes()).hexdigest()
    if got != a.history_sha256:
        sys.exit(f"{HISTORY.name} sha256 {got} != expected {a.history_sha256}")
    ids = labels_subsample.manifest_ids()
    labels = first_answers(ids)
    bad = [c for c, e in labels.items() if e["label"] not in labels_subsample.labels_tool.LABELS]
    if bad:
        sys.exit(f"first answers with invalid labels: {bad}")
    key = score.load_key(HERE.parent)
    report = {"approval": a.approval, "basis": "first_answers (primary, blind)", "history_sha256": got,
              **score_subsample.score_restricted(labels, key, ids, None)}
    text = json.dumps(report, indent=1, ensure_ascii=False)
    if a.out:
        a.out.write_text(text + "\n", encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
