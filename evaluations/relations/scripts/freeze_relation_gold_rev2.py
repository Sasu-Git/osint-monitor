"""Freeze relation gold revision 2 (development split): one file, occurrence-level sides, resolved third-event links.

    python evaluations/relations/scripts/freeze_relation_gold_rev2.py

Inputs (revision 1, unchanged): gold/relation-gold.yaml (141 cases), gold/relation-gold-reaction-batch.yaml (45),
gold/relation-gold.candidate.yaml (R055, excluded from revision 1), review/cases.json and
review-reaction-batch/cases.json (side member items), gold/owner-decisions-2026-10-07b.yaml.

Outputs:
- gold/relation-sides-rev2.yaml: every side as an item set {window, members}. A side is one occurrence.
- gold/relation-gold-rev2.yaml: all 187 cases. Sides are side IDs from the sides file; there are no free-text
  endpoints anywhere.
- gold/manifest.yaml: revision 2, with revision 1 moved to previous_revisions.

Owner rulings applied (2026-10-07b and 2026-10-09):
- R055: NO_RELATION; its link to the Xi-Trump summit is unresolved (no summit Development in the window).
- T025: AMBIGUOUS (identity verdict DIFFERENT; the relation was not assessed).
- Sides that mix occurrences point at the occurrence the relation concerns: R064 -> the Macron-visit items, T033 and
  T039 -> the rial occurrence, R114 -> the live-blog occurrence sx-400. R010, T016, T035 keep their sides (the
  NO_RELATION label holds for every occurrence in them).
- Third-event links resolve to a gold side or are recorded as unresolved and non-canonical. In the development
  windows none resolves: neither the summit nor Trump's rejection of the Hormuz plan is reported as its own
  occurrence inside its window.
- Pairs whose two sides the system merges into one Development keep their gold label and are scored as
  BLOCKED_BY_IDENTITY (a scoring rule, recorded in the manifest).
The sealed holdout is not read.
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "gold"
REV1_GIT = "0233855"
ML = "2026-09-30-multilingual"

REMAPS = {   # case -> side -> (new side id, members, reason)
    "R064": {"a": (f"{ML}:D9~macron-visit", ["sx-271", "sx-188"],
                   "owner 2026-10-09: only the Macron-visit items of system D9 relate (owner note on R064)")},
    "T033": {"b": (f"{ML}:D19~rial", ["sx-264", "sx-536"],
                   "owner 2026-10-07b: D19 split; the rial record-low occurrence")},
    "T039": {"b": (f"{ML}:D19~rial", ["sx-264", "sx-536"],
                   "owner 2026-10-07b: D19 split; the rial record-low occurrence")},
    "R114": {"b": (f"{ML}:sx-400", ["sx-400"],
                   "owner 2026-10-09: the lifecycle link is to the live blog sx-400, not the Security Council "
                   "meeting records sx-423 / sx-416")},
}
IDENTITY_VERDICTS = {"R012": "SAME_DEVELOPMENT", "R138": "SAME_DEVELOPMENT", "T008": "SAME_DEVELOPMENT",
                     "T034": "SAME_DEVELOPMENT", "T041": "SAME_DEVELOPMENT", "T033": "SAME_DEVELOPMENT",
                     "T039": "SAME_DEVELOPMENT", "T025": "DIFFERENT_DEVELOPMENT"}
SCORING = {
    "scored_labels": "cases with scored: true; AMBIGUOUS and SAME_DEVELOPMENT_SUSPECTED are excluded and reported "
                     "separately",
    "canonical": "only canonical (explicit-evidence) positives count as positives; inferred positives are "
                 "non-canonical and never expected at runtime",
    "sides": "a side is an item set; a system Development covers a side when it contains the side's items",
    "BLOCKED_BY_IDENTITY": "the system puts both sides of a pair into one Development: no distinct Development pair "
                           "exists to link. Counted against end-to-end relation coverage, not against the relation "
                           "classifier's precision or recall (owner 2026-10-09)",
    "external_links": "a third-event link counts only when its target is a gold side (resolved); unresolved links are "
                      "non-canonical and never scored as relations",
}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def normalise_external(links):
    out = []
    for l in links or []:
        desc = l.get("event") or l.get("trigger") or l.get("description")
        out.append({"side": l["side"], "relation": l["relation"], "role": l.get("role"), "target": None,
                    "description": desc, "status": "unresolved", "canonical": False})
    return out or None


def main() -> int:
    m = yaml.safe_load((GOLD / "manifest.yaml").read_text(encoding="utf-8"))
    if m.get("revision") != 1:
        print(f"refusing: gold manifest is revision {m.get('revision')}, not 1")
        return 1
    for rel in ("gold/relation-gold.yaml", "gold/relation-gold-reaction-batch.yaml"):
        if sha256(ROOT / rel) != m["sha256"][rel]:
            print(f"refusing: {rel} changed since revision 1")
            return 1
    main_gold = yaml.safe_load((GOLD / "relation-gold.yaml").read_text(encoding="utf-8"))
    batch = yaml.safe_load((GOLD / "relation-gold-reaction-batch.yaml").read_text(encoding="utf-8"))
    cand = yaml.safe_load((GOLD / "relation-gold.candidate.yaml").read_text(encoding="utf-8"))
    decisions = yaml.safe_load((GOLD / "owner-decisions-2026-10-07b.yaml").read_text(encoding="utf-8"))

    sides: dict[str, dict] = {}
    for f in (ROOT / "review" / "cases.json", ROOT / "review-reaction-batch" / "cases.json"):
        for c in json.loads(f.read_text(encoding="utf-8"))["cases"]:
            for s in ("a", "b"):
                side = {"window": c[s]["window"], "members": sorted(c[s]["members"])}
                if c[s]["id"] in sides and sides[c[s]["id"]] != side:
                    print(f"refusing: side {c[s]['id']} has two member sets")
                    return 1
                sides[c[s]["id"]] = side

    cases = {**{k: dict(v, source="revision 1") for k, v in main_gold.items()},
             **{k: dict(v, source="revision 1 reaction batch") for k, v in batch.items()}}
    r055 = decisions["relation_cases"]["R055"]
    cases["R055"] = {"a": cand["R055"]["a"], "b": cand["R055"]["b"], "label": "NO_RELATION", "roles": None,
                     "evidence": None, "canonical": False, "scored": True,
                     "external_links": [{"side": "a", "relation": "reaction_to", "role": "reaction", "target": None,
                                         "description": "Xi-Trump summit (Washington)", "status": "unresolved",
                                         "canonical": False}],
                     "owner_label": cand["R055"]["owner_label"], "owner_note": cand["R055"]["owner_note"],
                     "resolution": "owner 2026-10-07b: " + r055["reason"], "annotation": None,
                     "source": "owner decision 2026-10-07b"}
    t025 = decisions["relation_cases"]["T025"]
    cases["T025"].update({"label": "AMBIGUOUS", "scored": False, "canonical": False,
                          "resolution": "owner 2026-10-07b: " + t025["reason"]})

    changes = [{"case": "R055", "change": "added: NO_RELATION, summit link unresolved"},
               {"case": "T025", "change": "SAME_DEVELOPMENT_SUSPECTED -> AMBIGUOUS"}]
    for cid, remap in REMAPS.items():
        for s, (new_id, members, reason) in remap.items():
            old = cases[cid][s]
            if new_id in sides and sides[new_id]["members"] != sorted(members):
                print(f"refusing: side {new_id} exists with other members")
                return 1
            sides[new_id] = {"window": sides[old]["window"], "members": sorted(members)}
            if not set(members) <= set(sides[old]["members"]):
                print(f"refusing: {cid} remap members are not inside {old}")
                return 1
            cases[cid][s] = new_id
            cases[cid].setdefault("remaps", []).append({"side": s, "from": old, "to": new_id, "reason": reason})
            changes.append({"case": cid, "change": f"side {s}: {old} -> {new_id}"})
    for cid, e in cases.items():
        e["external_links"] = normalise_external(e.get("external_links")) if cid != "R055" else e["external_links"]
        e["identity_verdict"] = IDENTITY_VERDICTS.get(cid)
        for s in ("a", "b"):
            if e[s] not in sides:
                print(f"refusing: {cid} side {e[s]} has no member set")
                return 1
        if e["roles"]:
            for role, sid in e["roles"].items():
                if sid not in (e["a"], e["b"]):     # a role names a remapped side by its old ID
                    e["roles"][role] = next(r["to"] for r in e.get("remaps", []) if r["from"] == sid)
        e.setdefault("remaps", None)
    used = {e[s] for e in cases.values() for s in ("a", "b")}
    sides = {k: v for k, v in sorted(sides.items()) if k in used}

    (GOLD / "relation-sides-rev2.yaml").write_text(
        "# Relation gold revision 2: every side as an occurrence-level item set. Do not edit.\n"
        + yaml.safe_dump(sides, sort_keys=True, allow_unicode=True, width=120), encoding="utf-8", newline="\n")
    order = sorted(cases, key=lambda k: (k[0], int(k[1:])))
    out = {k: cases[k] for k in order}
    (GOLD / "relation-gold-rev2.yaml").write_text(
        "# Phase 3 relation gold, revision 2, development split. Do not edit: changes need a new revision.\n"
        "# Sides are IDs in relation-sides-rev2.yaml (item sets). Roles name each side. External links resolve to a\n"
        "# side or are unresolved and non-canonical.\n"
        + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8", newline="\n")

    labels = Counter(e["label"] for e in out.values())
    canon = Counter(e["label"] for e in out.values() if e["canonical"] and e["scored"])
    prev = {k: v for k, v in m.items() if k != "previous_revisions"}
    prev["git"] = REV1_GIT
    new = {"revision": 2, "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "state": "FROZEN: relation gold revision 2 (development split); holdout sealed, not opened",
           "cases": len(out), "scored_cases": sum(1 for e in out.values() if e["scored"]),
           "labels": dict(sorted(labels.items())), "canonical_positives": dict(sorted(canon.items())),
           "runtime_taxonomy": m["runtime_taxonomy"], "scoring": SCORING, "changes_from_previous": changes,
           "sha256": {"gold/relation-gold-rev2.yaml": sha256(GOLD / "relation-gold-rev2.yaml"),
                      "gold/relation-sides-rev2.yaml": sha256(GOLD / "relation-sides-rev2.yaml"),
                      "gold/owner-decisions-2026-10-07b.yaml": sha256(GOLD / "owner-decisions-2026-10-07b.yaml"),
                      "taxonomy.md": sha256(ROOT / "taxonomy.md"),
                      "scripts/freeze_relation_gold_rev2.py": sha256(Path(__file__))},
           "holdout_seal": "holdout/SEALED.yaml unchanged; not opened",
           "previous_revisions": [prev] + (m.get("previous_revisions") or [])}
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(new, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    print(f"revision 2: {len(out)} cases, {new['scored_cases']} scored; labels {dict(labels)}")
    print("canonical positives:", dict(canon))
    for c in changes:
        print(" ", c["case"], c["change"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
