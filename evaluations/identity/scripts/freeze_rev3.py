"""Freeze Development-identity gold revision 3: owner-reviewed additions (cross-language candidates and the Phase 3
identity suspects). Revision 2's cases are unchanged.

    python evaluations/identity/scripts/freeze_rev3.py

- gold/identity-gold.yaml stays byte-identical (revision 2, 189 cases).
- gold/identity-gold-rev3-additions.yaml: the 74 owner-reviewed cases from review-rev3/ (V001-V060 cross-language
  candidates, G01-G14 owner-given verdicts). Labels are the owner's verdicts and notes are verbatim.
- Cases whose note departs from the identity contract or earlier gold are flagged ``contract_conflict``. They are
  frozen as the owner labelled them; the benchmark reports scores with and without them.
- gold/manifest.yaml: revision 3. Revision 2 (git e9f7b6b) moves to ``previous_revisions``; hashes of every input.

Refuses while any rev3 case is unreviewed or revision 2's gold has changed.
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GOLD, REV3 = ROOT / "gold", ROOT / "review-rev3"
REV2_GIT = "e9f7b6b"
CONTRACT_CONFLICT = {
    "V004": "commentary pieces on the Oct 7 anniversary labelled SAME; the contract and gold rev 1-2 keep commentary "
            "a separate Development (e.g. C094), and V036/V042/V047 here keep it DIFFERENT",
    "V037": "an explainer on the plague case labelled SAME (commentary as same Development)",
    "V057": "a 3-year timeline piece labelled SAME (commentary as same Development)",
    "V014": "Kyiv-region strike vs drone crash in Moldova during the same mass attack labelled DIFFERENT; gold rev 2 "
            "C076 labelled a Moldova drone crash during the overnight attack SAME",
}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    m = yaml.safe_load((GOLD / "manifest.yaml").read_text(encoding="utf-8"))
    if m["revision"] != 2:
        print(f"refusing: gold is revision {m['revision']}, not 2")
        return 1
    if sha256(GOLD / "identity-gold.yaml") != m["sha256"]["gold/identity-gold.yaml"]:
        print("refusing: identity-gold.yaml changed since revision 2")
        return 1
    cases = json.loads((REV3 / "review-cases.json").read_text(encoding="utf-8"))
    verdicts = yaml.safe_load((REV3 / "owner-verdicts.yaml").read_text(encoding="utf-8"))
    missing = [c["case"] for c in cases if not (verdicts.get(c["case"]) or {}).get("verdict")]
    if missing:
        print("refusing: unreviewed", missing)
        return 1
    out = {}
    for c in cases:
        v = verdicts[c["case"]]
        a, b = c["items"]
        out[c["case"]] = {
            "a": a["id"], "b": b["id"], "window": c["window"], "split": "development",
            "label": v["verdict"], "note": v.get("note"), "owner_confidence": v.get("confidence"),
            "boundary_reason": v.get("boundary_reason"),
            "draft_label": c["draft"]["label"],
            "source": "owner-given (2026-10-07)" if c["case"].startswith("G") else
                      ("owner (agrees with draft)" if v["verdict"] == c["draft"]["label"] else "owner (corrected draft)"),
            "languages": sorted({a.get("lang") or "en", b.get("lang") or "en"}),
            "contract_conflict": CONTRACT_CONFLICT.get(c["case"]),
        }
    adds = GOLD / "identity-gold-rev3-additions.yaml"
    adds.write_text("# Development-identity gold revision 3: additions (owner-reviewed 2026-10-08). Do not edit.\n"
                    + yaml.safe_dump(out, sort_keys=True, allow_unicode=True, width=120), encoding="utf-8", newline="\n")
    counts = Counter(e["label"] for e in out.values())
    prev = {k: m[k] for k in ("revision", "frozen_at", "note", "cases", "labels", "per_split", "corrected_drafts",
                              "sha256") if k in m}
    prev["git"] = REV2_GIT
    new = {
        "revision": 3,
        "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": "Revision 3 adds 74 owner-reviewed development cases (cross-language candidates V001-V060; owner-given "
                "verdicts G01-G14: Phase 3 identity suspects, the D19 split, the RAF Fairford and Siberian plague "
                "regression pairs) in windows 2026-09-30-multilingual, 2026-10-03-live and 2026-10-05-live. Revision 2's "
                "189 cases are unchanged. Four additions carry a contract_conflict flag.",
        "cases": m["cases"], "labels": m["labels"], "per_split": m["per_split"],
        "additions": {"cases": len(out), "labels": dict(counts),
                      "contract_conflicts": sorted(CONTRACT_CONFLICT)},
        "changes_from_previous": [],
        "sha256": {**m["sha256"],
                   "gold/identity-gold-rev3-additions.yaml": sha256(adds),
                   "manifest.yaml": sha256(ROOT / "manifest.yaml"),
                   "review-rev3/review-cases.json": sha256(REV3 / "review-cases.json"),
                   "review-rev3/owner-verdicts.yaml": sha256(REV3 / "owner-verdicts.yaml"),
                   "review-rev3/draft-labels.json": sha256(REV3 / "draft-labels.json"),
                   "review-rev3/labeller-input.md": sha256(REV3 / "labeller-input.md")},
        "previous_revisions": [prev] + (m.get("previous_revisions") or []),
    }
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(new, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    print(f"revision 3: +{len(out)} cases {dict(counts)}; contract conflicts {sorted(CONTRACT_CONFLICT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
