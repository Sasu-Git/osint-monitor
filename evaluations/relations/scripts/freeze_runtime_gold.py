"""Freeze the runtime-eligible relation benchmark (runtime-benchmark-design.md) from the owner verdicts.

    python evaluations/relations/scripts/freeze_runtime_gold.py   # -> runtime/gold/

Reads runtime/review/owner-verdicts.yaml (authoritative; ACCEPT or an empty label keeps the blind draft) and
writes, with SHA-256 in runtime/gold/manifest.yaml:
- runtime/gold/owner-verdicts.snapshot.yaml: the verdicts verbatim;
- runtime/gold/runtime-gold.yaml: one entry per case: the two Development sides (window:D<id>, member items), the
  label, named roles for directed types, the stratum (hidden during labelling) and the identity flag.
Refuses to run when a case has no verdict or when runtime/gold/ already exists. The sealed holdouts are not read.
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REVIEW, GOLD = ROOT / "runtime" / "review", ROOT / "runtime" / "gold"
ROLES = {"reaction_to": ("reaction", "trigger"), "follow_up_to": ("follow_up", "original"),
         "caused_by": ("effect", "cause"), "commentary_on": ("commentary", "subject")}
RUNTIME = ("same_calamity_lifecycle", "same_convened_event", "reaction_to")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if GOLD.exists():
        print(f"refusing: {GOLD} exists (the runtime benchmark is frozen once)")
        return 1
    cases = {c["case"]: c for c in json.loads((REVIEW / "cases.json").read_text(encoding="utf-8"))["cases"]}
    drafts = json.loads((REVIEW / "draft-labels.json").read_text(encoding="utf-8"))
    rules = json.loads((REVIEW / "candidate-rules.json").read_text(encoding="utf-8"))
    verdicts = yaml.safe_load((REVIEW / "owner-verdicts.yaml").read_text(encoding="utf-8"))
    missing = [k for k in cases if not (verdicts.get(k) or {}).get("reviewed_at")]
    if missing:
        print(f"refusing: no owner verdict for {missing}")
        return 1
    gold = {}
    for cid, c in sorted(cases.items()):
        v, d = verdicts[cid], drafts[cid]
        label = d["label"] if v.get("label") in (None, "ACCEPT") else v["label"]
        direction = v.get("direction") or d["direction"]
        roles = None
        if label in ROLES:
            first, second = ROLES[label]
            x, y = (c["a"]["id"], c["b"]["id"]) if direction == "A->B" else (c["b"]["id"], c["a"]["id"])
            roles = {first: x, second: y}
        gold[cid] = {"window": c["a"]["window"],
                     "a": {"development": c["a"]["id"], "members": c["a"]["members"]},
                     "b": {"development": c["b"]["id"], "members": c["b"]["members"]},
                     "label": label, "roles": roles,
                     "scored": label not in ("AMBIGUOUS", "SAME_DEVELOPMENT_SUSPECTED"),
                     "runtime_type": label in RUNTIME,
                     "identity_flag": v.get("identity_flag") or d["identity_flag"],
                     "stratum": rules[cid]["stratum"], "proposed": rules[cid]["proposed"],
                     "owner_note": v.get("note"), "draft_label": d["label"]}
    GOLD.mkdir(parents=True)
    (GOLD / "owner-verdicts.snapshot.yaml").write_text((REVIEW / "owner-verdicts.yaml").read_text(encoding="utf-8"),
                                                        encoding="utf-8", newline="\n")
    (GOLD / "runtime-gold.yaml").write_text(
        "# Runtime-eligible relation benchmark (development), frozen. Do not edit.\n"
        + yaml.safe_dump(gold, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8", newline="\n")
    labels = Counter(e["label"] for e in gold.values())
    by_stratum = {s: dict(Counter(e["label"] for e in gold.values() if e["stratum"] == s))
                  for s in sorted({e["stratum"] for e in gold.values()})}
    meta = json.loads((REVIEW / "cases.json").read_text(encoding="utf-8"))["meta"]
    manifest = {"frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "state": "FROZEN: runtime-eligible relation benchmark (development); before Session 2 acceptance logic",
                "design": "runtime-benchmark-design.md (with amendment 1)", "cases": len(gold),
                "labels": dict(labels), "by_stratum": by_stratum,
                "runtime_type_positives": sum(1 for e in gold.values() if e["runtime_type"]),
                "populations": meta["populations"], "seed": meta["seed"], "generator": meta["generator"],
                "sha256": {p: sha256(ROOT / p) for p in (
                    "runtime/gold/runtime-gold.yaml", "runtime/gold/owner-verdicts.snapshot.yaml",
                    "runtime/review/cases.json", "runtime/review/candidate-rules.json",
                    "runtime/review/draft-labels.json", "runtime/manifest.yaml", "taxonomy.md")}}
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    print(f"frozen {len(gold)} cases: {dict(labels)}")
    print("by stratum:", by_stratum)
    return 0


if __name__ == "__main__":
    sys.exit(main())
