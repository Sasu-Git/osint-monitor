"""Freeze the Development-identity gold from the owner's verdicts (step 5 of the protocol).

The label of each case is the owner's verdict (ACCEPT = the draft label). Owner confidence, boundary reason and
note are kept verbatim; the draft label is kept for audit only and never decides anything. Writes
gold/identity-gold.yaml and gold/manifest.yaml (SHA-256 of the gold and of every input it was built from).

Refuses to freeze while any case is unreviewed.

A later revision (``--revision N --reason TEXT --previous-git SHA``) keeps the previous manifest, with its hashes
and the commit that froze it, under ``previous_revisions``, and records exactly which case labels changed.

Usage: python evaluations/identity/scripts/freeze_gold.py [--revision N --reason TEXT --previous-git SHA]
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verdicts as V  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "gold"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main() -> int:
    revision = int(arg("--revision", 1))
    previous, previous_gold = None, {}
    if revision > 1:
        previous = yaml.safe_load((GOLD / "manifest.yaml").read_text(encoding="utf-8"))
        if previous["revision"] != revision - 1:
            print(f"refusing: current gold is revision {previous['revision']}, not {revision - 1}")
            return 1
        if sha256(GOLD / "identity-gold.yaml") != previous["sha256"]["gold/identity-gold.yaml"]:
            print("refusing: gold/identity-gold.yaml changed since revision", previous["revision"], "was frozen")
            return 1
        previous_gold = yaml.safe_load((GOLD / "identity-gold.yaml").read_text(encoding="utf-8"))
    cases = json.loads((ROOT / "review" / "review-cases.json").read_text(encoding="utf-8"))
    ids = [c["case"] for c in cases]
    verdicts = V.load(ids)
    missing = [i for i in ids if not verdicts[i]["verdict"]]
    if missing:
        print(f"refusing to freeze: {len(missing)} unreviewed cases ({', '.join(missing[:10])} ...)")
        return 1
    out = {}
    for c in cases:
        v = verdicts[c["case"]]
        label = c["draft"]["label"] if v["verdict"] == "ACCEPT" else v["verdict"]
        out[c["case"]] = {
            "window": c["window"], "split": c["split"],
            "a": c["items"][0]["id"], "b": c["items"][1]["id"],
            "label": label,
            "source": "owner (agrees with draft)" if label == c["draft"]["label"] else "owner (corrected draft)",
            "owner_confidence": v["confidence"], "boundary_reason": v["boundary_reason"], "note": v["note"],
            "draft_label": c["draft"]["label"],
        }
    GOLD.mkdir(exist_ok=True)
    gold_path = GOLD / "identity-gold.yaml"
    header = ("# Development-identity gold (frozen). Labels are the owner's verdicts after blind review of drafts\n"
              "# written by an annotator that saw only item text, outlet, time, language and the definition.\n"
              "# Item ids refer to the windows in ../manifest.yaml. Do not edit: changes need a new revision.\n")
    gold_path.write_text(header + yaml.safe_dump(out, sort_keys=True, allow_unicode=True, width=120),
                         encoding="utf-8", newline="\n")
    labels = Counter(e["label"] for e in out.values())
    per_split = {s: dict(Counter(e["label"] for e in out.values() if e["split"] == s))
                 for s in sorted({e["split"] for e in out.values()})}
    inputs = ["manifest.yaml", "review/review-cases.json", "review/draft-labels.json", "review/owner-verdicts.yaml",
              "review/labeller-input.md", "review/cases.json"]
    changes = [{"case": k, "from": previous_gold[k]["label"], "to": out[k]["label"]}
               for k in sorted(out) if previous_gold and previous_gold[k]["label"] != out[k]["label"]]
    manifest = {
        "revision": revision,
        "frozen_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "note": ("Owner-reviewed identity gold: 189 cases, every verdict given by the owner in the blind review "
                 "page (draft label hidden until the verdict). Notes are the owner's, verbatim."
                 + (f" Revision {revision}: {arg('--reason')} Supersedes revision {revision - 1} for Phase 2 "
                    "evaluation." if revision > 1 else "")),
        **({"changes_from_previous": changes} if revision > 1 else {}),
        "cases": len(out), "labels": dict(labels), "per_split": per_split,
        "corrected_drafts": sum(1 for e in out.values() if e["label"] != e["draft_label"]),
        "sha256": {"gold/identity-gold.yaml": sha256(gold_path), **{p: sha256(ROOT / p) for p in inputs}},
    }
    if previous:
        prior = {k: v for k, v in previous.items() if k != "previous_revisions"}
        prior["git"] = arg("--previous-git")
        manifest["previous_revisions"] = [prior] + list(previous.get("previous_revisions") or [])
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, width=110), encoding="utf-8",
                                        newline="\n")
    print(json.dumps({k: manifest[k] for k in ("revision", "cases", "labels", "per_split", "corrected_drafts")}))
    for ch in changes:
        print("changed", ch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
