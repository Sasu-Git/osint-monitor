"""Owner labels for the Situation-membership evaluation set: validate and freeze. Never fills labels.

  python labels_tool.py validate [--dir DIR]   all cases labelled, allowed values only, reason and reviewer present,
                                               every automatic Situation's intended scope filled, and the frozen
                                               set (FREEZE.md hashes) unchanged
  python labels_tool.py freeze   [--dir DIR]   validate, then write LABELS-FREEZE.json (hashes of the labels and the
                                               frozen set); refuses to overwrite an existing freeze

The labels file is owner-labels.yaml. Labels are the six of CONTRACT-V2 section 4; no others are accepted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
LABELS = ("MEMBER", "CONTEXT", "SPILLOVER", "OTHER_SITUATION", "NOT_MEMBER", "AMBIGUOUS")
LABELS_FILE = "owner-labels.yaml"
FREEZE_FILE = "FREEZE.md"
LABELS_FREEZE_FILE = "LABELS-FREEZE.json"
# Files in FREEZE.md whose hash must still match. The snapshot lives outside the folder and the labels template is
# expected to change once filled, so neither is checked here.
NOT_CHECKED = {"owner-labels.yaml (empty template)"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def frozen_hashes(d: Path) -> dict[str, str]:
    """Parse the ```sha256 block of FREEZE.md: '<hex>  <path relative to the evalset folder>'."""
    text = (d / FREEZE_FILE).read_text(encoding="utf-8")
    m = re.search(r"```sha256\n(.*?)```", text, re.S)
    if not m:
        raise ValueError("FREEZE.md has no ```sha256 block")
    out = {}
    for line in m.group(1).splitlines():
        if line.strip():
            h, name = line.split(None, 1)
            out[name.strip()] = h
    return out


def check_frozen(d: Path) -> list[str]:
    errors = []
    try:
        hashes = frozen_hashes(d)
    except (OSError, ValueError) as e:
        return [f"cannot read frozen hashes: {e}"]
    for name, h in hashes.items():
        if name in NOT_CHECKED:
            continue
        p = d / name
        if not p.exists():
            errors.append(f"frozen file missing: {name}")
        elif sha256(p) != h:
            errors.append(f"frozen file changed: {name}")
    return errors


def validate(d: Path, check_freeze: bool = True) -> list[str]:
    errors: list[str] = []
    cases = json.loads((d / "cases.json").read_text(encoding="utf-8"))["cases"]
    scopes = json.loads((d / "scopes.json").read_text(encoding="utf-8"))
    labels = yaml.safe_load((d / LABELS_FILE).read_text(encoding="utf-8")) or {}

    want = [c["case_id"] for c in cases]
    entries = labels.get("cases") or []
    got = [e.get("case_id") for e in entries]
    dup = {x for x in got if got.count(x) > 1}
    if dup:
        errors.append(f"duplicate case ids: {sorted(dup)}")
    missing, extra = set(want) - set(got), set(got) - set(want)
    if missing:
        errors.append(f"{len(missing)} cases missing from labels, e.g. {sorted(missing)[:5]}")
    if extra:
        errors.append(f"unknown case ids: {sorted(extra)[:5]}")
    for e in entries:
        cid = e.get("case_id")
        if e.get("label") not in LABELS:
            errors.append(f"{cid}: label {e.get('label')!r} not in {LABELS}")
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
        errors += check_frozen(d)
    return errors


def freeze(d: Path) -> Path:
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
        "labels_sha256": sha256(d / LABELS_FILE),
        "freeze_md_sha256": sha256(d / FREEZE_FILE),
        "frozen_set": {k: v for k, v in frozen_hashes(d).items()},
        "case_count": len(labels["cases"]),
    }
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8", newline="\n")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["validate", "freeze"])
    ap.add_argument("--dir", type=Path, default=HERE)
    a = ap.parse_args()
    if a.command == "validate":
        errors = validate(a.dir)
        if errors:
            print(f"INVALID ({len(errors)} problems)")
            for e in errors[:50]:
                print("  " + e)
            if len(errors) > 50:
                print(f"  ... {len(errors) - 50} more")
            sys.exit(1)
        print("valid")
    else:
        print(f"wrote {freeze(a.dir)}")


if __name__ == "__main__":
    main()
