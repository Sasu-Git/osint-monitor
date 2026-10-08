"""Development-identity gold revision 4: the owner's corrections of four revision 3 additions (2026-10-08).

    python evaluations/identity/scripts/freeze_rev4.py

The owner resolved the four contract-conflict flags of revision 3:
- V004, V037, V057 -> DIFFERENT_DEVELOPMENT (commentary is a separate Development, as the contract says);
- V014 -> SAME_DEVELOPMENT (one mass attack and its side effect, as C076).

The verdicts are applied to review-rev3/owner-verdicts.yaml (notes unchanged, verbatim). The additions are
rewritten with the new labels, their flags cleared, and ``source: owner corrected (2026-10-08)``. The manifest
becomes revision 4, revision 3 (git ad5ef16) moves to previous_revisions, and the changes are recorded. Revision
2's 189 cases are untouched.
"""
import hashlib
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GOLD, REV3 = ROOT / "gold", ROOT / "review-rev3"
REV3_GIT = "ad5ef16"
CORRECTIONS = {"V004": "DIFFERENT_DEVELOPMENT", "V037": "DIFFERENT_DEVELOPMENT", "V057": "DIFFERENT_DEVELOPMENT",
               "V014": "SAME_DEVELOPMENT"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    m = yaml.safe_load((GOLD / "manifest.yaml").read_text(encoding="utf-8"))
    if m["revision"] != 3:
        print(f"refusing: gold is revision {m['revision']}, not 3")
        return 1
    adds_path = GOLD / "identity-gold-rev3-additions.yaml"
    if sha256(adds_path) != m["sha256"]["gold/identity-gold-rev3-additions.yaml"]:
        print("refusing: additions changed since revision 3")
        return 1
    vpath = REV3 / "owner-verdicts.yaml"
    verdicts = yaml.safe_load(vpath.read_text(encoding="utf-8"))
    adds = yaml.safe_load(adds_path.read_text(encoding="utf-8"))
    changes = []
    for cid, label in CORRECTIONS.items():
        changes.append({"case": cid, "from": adds[cid]["label"], "to": label})
        verdicts[cid]["verdict"] = label
        verdicts[cid]["reviewed_at"] = "2026-10-08T00:00:00Z"
        adds[cid].update({"label": label, "source": "owner corrected (2026-10-08)", "contract_conflict": None})
    vpath.write_text(yaml.safe_dump(verdicts, sort_keys=True, allow_unicode=True, width=120), encoding="utf-8",
                     newline="\n")
    adds_path.write_text("# Development-identity gold additions (revision 3 cases; labels as of revision 4). Do not edit.\n"
                         + yaml.safe_dump(adds, sort_keys=True, allow_unicode=True, width=120), encoding="utf-8",
                         newline="\n")
    prev = {k: v for k, v in m.items() if k != "previous_revisions"}
    prev["git"] = REV3_GIT
    counts = Counter(e["label"] for e in adds.values())
    new = {**{k: v for k, v in m.items() if k not in ("previous_revisions", "changes_from_previous")},
           "revision": 4, "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "note": "Revision 4: owner corrections of four revision 3 additions (V004, V037, V057 -> DIFFERENT: commentary "
                   "is a separate Development; V014 -> SAME: one mass attack and its side effect, as C076). Revision 2's "
                   "189 cases unchanged.",
           "additions": {"cases": len(adds), "labels": dict(counts), "contract_conflicts": []},
           "changes_from_previous": changes,
           "previous_revisions": [prev] + (m.get("previous_revisions") or [])}
    new["sha256"] = {**m["sha256"], "gold/identity-gold-rev3-additions.yaml": sha256(adds_path),
                     "review-rev3/owner-verdicts.yaml": sha256(vpath)}
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(new, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    print(f"revision 4: additions {dict(counts)}; changes {changes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
