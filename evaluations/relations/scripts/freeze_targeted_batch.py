"""Freeze the positive-targeted runtime batch (runtime-targeted-design.md): rounds 1 and 2, owner verdicts.

    python evaluations/relations/scripts/freeze_targeted_batch.py   # -> runtime-targeted/gold/

Reads runtime-targeted/review-r*/ (cases, hidden targeting rules, blind draft, owner verdicts; ACCEPT or an empty
label keeps the draft) and writes runtime-targeted/gold/targeted-gold.yaml plus a manifest with SHA-256 and the yield
per targeted type. Refuses when a case has no owner verdict or when the gold folder exists. This batch is for
engineering validation only: it never estimates prevalence or unbiased recall. The sealed holdouts are not read.
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "runtime-targeted"
GOLD = BASE / "gold"
RUNTIME = ("same_calamity_lifecycle", "same_convened_event", "reaction_to")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if GOLD.exists():
        print(f"refusing: {GOLD} exists")
        return 1
    gold, hashes, eligible = {}, {}, {}
    for rd in sorted(BASE.glob("review-r*")):
        cases = json.loads((rd / "cases.json").read_text(encoding="utf-8"))["cases"]
        rules = json.loads((rd / "candidate-rules.json").read_text(encoding="utf-8"))
        drafts = json.loads((rd / "draft-labels.json").read_text(encoding="utf-8"))
        verdicts = yaml.safe_load((rd / "owner-verdicts.yaml").read_text(encoding="utf-8"))
        missing = [c["case"] for c in cases if not (verdicts.get(c["case"]) or {}).get("reviewed_at")]
        if missing:
            print(f"refusing: no owner verdict for {missing}")
            return 1
        for c in cases:
            cid, v, d, r = c["case"], verdicts[c["case"]], drafts[c["case"]], rules[c["case"]]
            label = d["label"] if v.get("label") in (None, "ACCEPT") else v["label"]
            gold[cid] = {"round": int(rd.name[-1]), "window": c["a"]["window"], "targeted": r["targeted"],
                         "rank": r["rank"], "cosine": r["cosine"],
                         "a": {"development": c["a"]["id"], "members": c["a"]["members"]},
                         "b": {"development": c["b"]["id"], "members": c["b"]["members"]},
                         "label": label, "direction": v.get("direction") or (d["direction"] if label in RUNTIME else None),
                         "identity_flag": v.get("identity_flag") or d["identity_flag"], "draft_label": d["label"],
                         "draft_flag": d["flag"], "owner_note": v.get("note")}
            eligible.setdefault(f"round {rd.name[-1]} {r['targeted']}", r["eligible"])
        for f in ("cases.json", "candidate-rules.json", "draft-labels.json", "owner-verdicts.yaml"):
            hashes[f"runtime-targeted/{rd.name}/{f}"] = sha256(rd / f)
    GOLD.mkdir()
    (GOLD / "targeted-gold.yaml").write_text(
        "# Positive-targeted runtime batch, frozen. Engineering validation only; never a prevalence or recall estimate.\n"
        + yaml.safe_dump(gold, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8", newline="\n")
    hashes["runtime-targeted/gold/targeted-gold.yaml"] = sha256(GOLD / "targeted-gold.yaml")
    yield_ = {t: sum(1 for e in gold.values() if e["label"] == t) for t in RUNTIME}
    manifest = {"frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "state": "FROZEN: positive-targeted runtime batch, rounds 1-2 (runtime-targeted-design.md)",
                "cases": len(gold), "labels": dict(Counter(e["label"] for e in gold.values())),
                "drawn_by_targeted_type": dict(Counter(e["targeted"] for e in gold.values())),
                "eligible_pairs": eligible, "confirmed_runtime_positives": yield_, "target_per_type": "8-12",
                "sha256": hashes}
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    print(f"frozen {len(gold)} cases: {manifest['labels']}; runtime positives {yield_}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
