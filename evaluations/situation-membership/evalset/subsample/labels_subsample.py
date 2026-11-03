"""Owner labels for the labelling subsample: validate and freeze. Never fills labels.

  python labels_subsample.py validate   every manifest case labelled (and no other), allowed values only, reason and
                                        reviewer present, every automatic Situation's intended scope filled; the full
                                        frozen set (../FREEZE.md) and the subsample files (FREEZE-SUBSAMPLE.md)
                                        unchanged
  python labels_subsample.py freeze     validate, then write LABELS-FREEZE-subsample.json; never overwritten

Same labels and rules as ../labels_tool.py (imported, not changed); only the case list is the manifest's.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
EVALSET = HERE.parent
sys.path.insert(0, str(EVALSET))
import labels_tool  # noqa: E402

LABELS_FILE = "owner-labels-subsample.yaml"
FREEZE_FILE = "FREEZE-SUBSAMPLE.md"
LABELS_FREEZE_FILE = "LABELS-FREEZE-subsample.json"
NOT_CHECKED = {"owner-labels-subsample.yaml (empty template)"}


def manifest_ids(d: Path = HERE) -> list[str]:
    return json.loads((d / "manifest.json").read_text(encoding="utf-8"))["case_ids"]


def check_subsample_frozen(d: Path = HERE) -> list[str]:
    text = (d / FREEZE_FILE).read_text(encoding="utf-8")
    m = re.search(r"```sha256\n(.*?)```", text, re.S)
    if not m:
        return [f"{FREEZE_FILE} has no ```sha256 block"]
    errors = []
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        h, name = line.split(None, 1)
        name = name.strip()
        if name in NOT_CHECKED:
            continue
        p = d / name
        if not p.exists():
            errors.append(f"subsample file missing: {name}")
        elif labels_tool.sha256(p) != h:
            errors.append(f"subsample file changed: {name}")
    return errors


def validate(d: Path = HERE, check_freeze: bool = True) -> list[str]:
    errors: list[str] = []
    scopes = json.loads((EVALSET / "scopes.json").read_text(encoding="utf-8"))
    labels = yaml.safe_load((d / LABELS_FILE).read_text(encoding="utf-8")) or {}
    want = manifest_ids(d)
    entries = labels.get("cases") or []
    got = [e.get("case_id") for e in entries]
    dup = {x for x in got if got.count(x) > 1}
    if dup:
        errors.append(f"duplicate case ids: {sorted(dup)}")
    missing, extra = set(want) - set(got), set(got) - set(want)
    if missing:
        errors.append(f"{len(missing)} cases missing from labels, e.g. {sorted(missing)[:5]}")
    if extra:
        errors.append(f"case ids outside the manifest: {sorted(extra)[:5]}")
    for e in entries:
        cid = e.get("case_id")
        if e.get("label") not in labels_tool.LABELS:
            errors.append(f"{cid}: label {e.get('label')!r} not in {labels_tool.LABELS}")
        if not (isinstance(e.get("reason"), str) and e["reason"].strip()):
            errors.append(f"{cid}: reason missing")
        if not (isinstance(e.get("reviewer"), str) and e["reviewer"].strip()):
            errors.append(f"{cid}: reviewer missing")
    want_scopes = {a["slug"] for a in scopes["automatic"]}
    got_scopes = {s.get("slug"): s for s in (labels.get("situation_scopes") or [])}
    if set(got_scopes) != want_scopes:
        errors.append(f"situation_scopes must list exactly the automatic Situations: missing "
                      f"{sorted(want_scopes - set(got_scopes))}, unknown {sorted(set(got_scopes) - want_scopes)}")
    for slug, s in got_scopes.items():
        if s.get("domains_or_types") is None or s.get("places") is None:
            errors.append(f"scope {slug}: domains_or_types and places must be filled (an empty list is allowed)")
        if not (isinstance(s.get("reviewer"), str) and s["reviewer"].strip()):
            errors.append(f"scope {slug}: reviewer missing")
    if check_freeze:
        errors += labels_tool.check_frozen(EVALSET) + check_subsample_frozen(d)
    return errors


def freeze(d: Path = HERE) -> Path:
    out = d / LABELS_FREEZE_FILE
    if out.exists():
        sys.exit(f"{out} exists; a freeze is never overwritten")
    errors = validate(d)
    if errors:
        sys.exit("not valid, not frozen:\n  " + "\n  ".join(errors))
    labels = yaml.safe_load((d / LABELS_FILE).read_text(encoding="utf-8"))
    reviewers = sorted({e["reviewer"] for e in labels["cases"]} | {s["reviewer"] for s in labels["situation_scopes"]})
    record = {
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "reviewers": reviewers,
        "labels_sha256": labels_tool.sha256(d / LABELS_FILE),
        "manifest_sha256": labels_tool.sha256(d / "manifest.json"),
        "freeze_subsample_md_sha256": labels_tool.sha256(d / FREEZE_FILE),
        "frozen_set": labels_tool.frozen_hashes(EVALSET),
        "case_count": len(labels["cases"]),
    }
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8", newline="\n")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["validate", "freeze"])
    a = ap.parse_args()
    if a.command == "validate":
        errors = validate()
        if errors:
            print(f"INVALID ({len(errors)} problems)")
            for e in errors[:50]:
                print("  " + e)
            if len(errors) > 50:
                print(f"  ... {len(errors) - 50} more")
            sys.exit(1)
        print("valid")
    else:
        print(f"wrote {freeze()}")


if __name__ == "__main__":
    main()
