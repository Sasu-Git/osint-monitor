"""Freeze the targeted reaction_to batch as an addendum to the relation gold (revision 1).

    python evaluations/relations/scripts/freeze_reaction_batch.py

Reads review-reaction-batch/owner-verdicts.yaml (owner, authoritative), freezes it verbatim as
gold/reaction-batch-verdicts.snapshot.yaml, and writes gold/relation-gold-reaction-batch.yaml. Same schema as
relation-gold.yaml: named roles, evidence, canonical, scored, external_links. A direction is turned into roles:
A->B means A holds the first role (reaction, follow-up, effect, commentary). Updates gold/manifest.yaml with the
combined counts. Development windows only; the sealed holdout is not read.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GOLD, BATCH = ROOT / "gold", ROOT / "review-reaction-batch"
ROLES = {"reaction_to": ("reaction", "trigger"), "follow_up_to": ("follow_up", "original"),
         "caused_by": ("effect", "cause"), "commentary_on": ("commentary", "subject")}
SYMMETRIC = {"same_calamity_lifecycle", "same_convened_event", "same_attack_wave", "co_caused_with"}
REJECTION = "Trump rejects Iran's Strait of Hormuz plan (27 Sep)"
EXTERNAL = {   # owner: "link to third occurrence ... should be linked and modelled"
    "T005": [{"side": "a", "relation": "follow_up_to", "event": REJECTION},
             {"side": "b", "relation": "commentary_on", "event": REJECTION}],
    "T007": [{"side": "a", "relation": "commentary_on", "event": REJECTION},
             {"side": "b", "relation": "commentary_on", "event": REJECTION}],
    "T029": [{"side": "b", "relation": "reaction_to", "event": REJECTION},
             {"side": "a", "relation": "commentary_on", "event": REJECTION}],
    "T042": [{"side": "a", "relation": "commentary_on", "event": REJECTION},
             {"side": "b", "relation": "follow_up_to", "event": REJECTION}],
    "T045": [{"side": "a", "relation": "reaction_to", "event": REJECTION},
             {"side": "b", "relation": "commentary_on", "event": REJECTION}],
    "T044": [{"side": "both", "relation": "context", "event": "Hong Kong National Day 'golden week' holiday"}],
}
ANNOTATIONS = {
    "T003": "owner: B is a news-in-brief roundup; only its Malaysia-repatriation item comments on A",
    "T043": "the same Iran statement also reacts to the sanctions vow in T030: one reaction, two triggers",
    "T019": "the protests at Netanyahu's UN visit belong to the convened event (UN General Assembly)",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    verdicts = yaml.safe_load((BATCH / "owner-verdicts.yaml").read_text(encoding="utf-8"))
    cases = {c["case"]: c for c in json.loads((BATCH / "cases.json").read_text(encoding="utf-8"))["cases"]}
    assert set(verdicts) == set(cases) and all((verdicts[c] or {}).get("label") for c in cases), "unreviewed cases"
    snap = GOLD / "reaction-batch-verdicts.snapshot.yaml"
    snap.write_bytes((BATCH / "owner-verdicts.yaml").read_bytes())
    gold = {}
    for cid in sorted(cases):
        v, c = verdicts[cid], cases[cid]
        label, side = v["label"], {"a": c["a"]["id"], "b": c["b"]["id"]}
        roles = None
        if label in ROLES:
            first, second = ROLES[label]
            assert v.get("direction") in ("A->B", "B->A"), cid
            f, s = ("a", "b") if v["direction"] == "A->B" else ("b", "a")
            roles = {first: side[f], second: side[s]}
        relation = label in ROLES or label in SYMMETRIC
        gold[cid] = {"a": side["a"], "b": side["b"], "label": label, "roles": roles,
                     "evidence": "explicit" if relation else None, "canonical": relation,
                     "scored": label not in ("AMBIGUOUS", "SAME_DEVELOPMENT_SUSPECTED"),
                     "external_links": EXTERNAL.get(cid), "owner_note": v.get("note"),
                     "annotation": ANNOTATIONS.get(cid)}
    out = GOLD / "relation-gold-reaction-batch.yaml"
    out.write_text("# Relation gold revision 1 addendum: targeted reaction_to batch (development windows), frozen.\n"
                   + yaml.safe_dump(gold, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8",
                   newline="\n")
    main_gold = yaml.safe_load((GOLD / "relation-gold.yaml").read_text(encoding="utf-8"))
    combined = list(main_gold.values()) + list(gold.values())
    canon = Counter(g["label"] for g in combined if g["canonical"])
    m = yaml.safe_load((GOLD / "manifest.yaml").read_text(encoding="utf-8"))
    m["reaction_batch"] = {
        "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "cases": len(gold),
        "labels": dict(Counter(g["label"] for g in gold.values())),
        "canonical_reaction_to": sum(1 for g in gold.values() if g["label"] == "reaction_to")}
    m["combined_canonical_positives"] = {t: canon.get(t, 0) for t in sorted(m["runtime_taxonomy"])}
    m["combined_scored_cases"] = sum(1 for g in combined if g["scored"])
    m["runtime_taxonomy"]["reaction_to"] = "implement (targeted batch passed: 7 canonical positives, 5 triggers)"
    m["sha256"].update({"gold/relation-gold-reaction-batch.yaml": sha(out),
                        "gold/reaction-batch-verdicts.snapshot.yaml": sha(snap),
                        "review-reaction-batch/cases.json": sha(BATCH / "cases.json"),
                        "review-reaction-batch/draft-labels.json": sha(BATCH / "draft-labels.json"),
                        "taxonomy.md (revision 1)": sha(ROOT / "taxonomy.md"),
                        "scripts/freeze_reaction_batch.py": sha(Path(__file__))})
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(m, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    print(json.dumps({"batch": m["reaction_batch"], "combined": m["combined_canonical_positives"],
                      "scored": m["combined_scored_cases"]}, indent=1))


if __name__ == "__main__":
    main()
