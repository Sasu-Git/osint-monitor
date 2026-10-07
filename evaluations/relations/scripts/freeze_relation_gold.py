"""Freeze the Phase 3 relation gold (development split) from the owner verdicts and the owner's resolutions.

    python evaluations/relations/scripts/freeze_relation_gold.py

Inputs (unchanged, hashed):
- gold/owner-verdicts.snapshot.yaml: the owner's verdicts and notes, verbatim, frozen 2026-10-07
- review/cases.json: the cases

Owner decisions applied (2026-10-07, locked):
- named semantic roles instead of arrows:
  - reaction_to: reaction -> trigger
  - follow_up_to: follow_up -> original
  - caused_by: effect -> cause
  - commentary_on: commentary -> subject
- commentary_on joins the gold taxonomy (runtime deferred)
- runtime canonical relations are explicit-only; inferred links are kept with evidence: inferred (non-canonical)
- same_visit_or_summit is renamed same_convened_event (a bounded scheduled gathering and its distinct
  actions/outcomes)
- per-case resolutions in RESOLUTIONS below

A link to a third event that is not one of the pair's two sides is recorded under ``external_links``. It is not
scored.

Writes gold/relation-gold.yaml and updates gold/manifest.yaml. The sealed holdout is not read.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GOLD = ROOT / "gold"
RENAME = {"same_visit_or_summit": "same_convened_event"}
SYMMETRIC = {"same_calamity_lifecycle", "same_convened_event", "same_attack_wave", "co_caused_with"}
ROLES = {"reaction_to": ("reaction", "trigger"), "follow_up_to": ("follow_up", "original"),
         "caused_by": ("effect", "cause"), "commentary_on": ("commentary", "subject")}
RUNTIME = {"same_calamity_lifecycle": "implement", "same_convened_event": "implement",
           "reaction_to": "targeted batch first", "same_attack_wave": "defer", "follow_up_to": "defer",
           "commentary_on": "defer", "caused_by": "dropped from Phase 3 runtime",
           "co_caused_with": "dropped from Phase 3 runtime"}

REJECTION = "Trump rejects Iran's Strait of Hormuz plan (27 Sep)"
# case -> (label, roles {role: 'a'|'b'} or None, evidence, external_links, resolution)
RESOLUTIONS = {
    "R002": ("commentary_on", {"commentary": "b", "subject": "a"}, "explicit", [],
             "D2: B explains the jury options in the impasse A reports"),
    "R005": ("commentary_on", {"commentary": "b", "subject": "a"}, "explicit", [],
             "owner condition met (both analysis); B is a reader Q&A from the summit that A (system D3) reports"),
    "R008": ("reaction_to", {"reaction": "a", "trigger": "b"}, "explicit", [],
             "owner agrees: A presses 'after Singapore unveiled a rival tax-exemption scheme' (B's subject)"),
    "R014": ("reaction_to", {"reaction": "b", "trigger": "a"}, "explicit", [], "settled at review"),
    "R029": ("reaction_to", {"reaction": "b", "trigger": "a"}, "inferred", [],
             "owner verdict kept; the reaction is inferred, so it is non-canonical (D3)"),
    "R036": ("commentary_on", {"commentary": "b", "subject": "a"}, "explicit", [],
             "D2: B comments on the speech A reports"),
    "R056": ("follow_up_to", {"follow_up": "b", "original": "a"}, "inferred", [],
             "owner verdict kept; shared aim inferred, no textual link, so non-canonical (D3)"),
    "R059": ("NO_RELATION", None, "explicit",
             [{"side": "a", "relation": "commentary_on", "role": "commentary", "event": REJECTION},
              {"side": "b", "relation": "caused_by", "role": "effect", "event": REJECTION,
               "evidence": "'Oil prices surge after Trump rejects Iran's plan'"}],
             "owner: link to the cause as a third event"),
    "R060": ("NO_RELATION", None, "explicit", [], "owner: no relation stands; note was a West Bank watchpoint"),
    "R076": ("reaction_to", {"reaction": "b", "trigger": "a"}, "inferred", [],
             "owner verdict kept; the reaction is inferred, so it is non-canonical (D3)"),
    "R087": ("NO_RELATION", None, "explicit",
             [{"side": "b", "relation": "same_convened_event", "event": "Xi-Trump summit (Washington)",
               "note": "a stated outcome: goods listed for tariff cuts following the summit"},
              {"side": "a", "relation": "follow_up_to", "role": "follow_up", "event": "Xi-Trump summit (Washington)",
               "note": "Trump's later remarks about the summit's Taiwan talk"}],
             "owner: link to the third event (the summit or its outcomes)"),
    "R105": ("commentary_on", {"commentary": "a", "subject": "b"}, "explicit", [],
             "D2: A comments on Netanyahu's UNGA appearance, which B's Day Three report covers"),
    "R115": ("NO_RELATION", None, "explicit",
             [{"side": "a", "relation": "commentary_on", "role": "commentary", "event": REJECTION},
              {"side": "b", "relation": "commentary_on", "role": "commentary", "event": REJECTION}],
             "owner agrees: link both to the event"),
    "R123": ("follow_up_to", {"follow_up": "b", "original": "a"}, "inferred", [],
             "owner: follow-up or co-cause both fine; follow_up_to (budget -> troop decree) is inferred, so non-canonical"),
    "R127": ("NO_RELATION", None, "explicit",
             [{"side": "b", "relation": "follow_up_to", "role": "follow_up",
               "event": "Russian strike on a Ukrainian shopping complex (Friday, 16 killed)"},
              {"side": "a", "relation": "context", "event": "Russian strike on a Ukrainian shopping complex (Friday, 16 killed)",
               "note": "A's headline anchors to it ('day after shopping complex attack')"}],
             "owner: link to the cause (third event)"),
    "R132": ("co_caused_with", None, "explicit",
             [{"side": "both", "relation": "common_cause", "event": REJECTION}],
             "owner agrees: both texts name the rejection, neither responds to the other"),
    "R134": ("NO_RELATION", None, "explicit", [], "owner agrees: different events, same topic"),
    "R098": ("AMBIGUOUS", None, "explicit", [],
             "owner: two events, not one Development. Their relation was not assessed: a candidate is "
             "same_convened_event (both on 28 Sep at the UN General Assembly). Excluded from scoring."),
    "R012": ("SAME_DEVELOPMENT_SUSPECTED", None, "explicit", [], "identity review (one matter, two outlets)"),
    "R138": ("SAME_DEVELOPMENT_SUSPECTED", None, "explicit", [], "identity review (cross-language split)"),
}
DEFERRED_DEBATE = {
    "R055": "owner leans reaction_to; disputed: A (08:06) was published before B's Taiwan remarks (09:43), and A "
            "reacts to the summit as a whole. To settle in discussion; excluded from the frozen gold.",
}
ANNOTATIONS = {
    "R045": "owner: one lifecycle even if the two sides were one Development",
    "R064": "side A (system D9) is a mixed Development; the relation holds for its Macron items; D9 -> identity review",
    "R066": "verdict given on limited evidence: the Daily News body is truncated in the feed",
    "R114": "condition met: B covers 'Security Council LIVE: ... as Ebola deepens crisis'",
    "R124": "owner confirms the AI remarks were made during the France tour",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    snap = GOLD / "owner-verdicts.snapshot.yaml"
    verdicts = yaml.safe_load(snap.read_text(encoding="utf-8"))
    cases = {c["case"]: c for c in json.loads((ROOT / "review" / "cases.json").read_text(encoding="utf-8"))["cases"]}
    gold = {}
    for cid in sorted(cases):
        v, c = verdicts[cid], cases[cid]
        if cid in DEFERRED_DEBATE:
            continue
        if cid in RESOLUTIONS:
            label, roles, evidence, external, resolution = RESOLUTIONS[cid]
        else:
            label, roles, evidence, external, resolution = RENAME.get(v["label"], v["label"]), None, "explicit", [], None
            assert label not in ROLES, f"{cid}: directed label without a resolution"
        label = RENAME.get(label, label)
        if label in ROLES:
            assert roles and set(roles) == set(ROLES[label]), f"{cid}: roles {roles}"
        side = {"a": c["a"]["id"], "b": c["b"]["id"]}
        gold[cid] = {
            "a": side["a"], "b": side["b"], "label": label,
            "roles": {r: side[s] for r, s in roles.items()} if roles else None,
            "evidence": evidence if label not in ("NO_RELATION", "AMBIGUOUS", "SAME_DEVELOPMENT_SUSPECTED") else None,
            "canonical": label in SYMMETRIC | set(ROLES) and evidence == "explicit",
            "scored": label not in ("AMBIGUOUS", "SAME_DEVELOPMENT_SUSPECTED"),
            "external_links": external or None,
            "owner_label": v["label"], "owner_note": v.get("note"),
            "resolution": resolution, "annotation": ANNOTATIONS.get(cid),
        }
    out = GOLD / "relation-gold.yaml"
    out.write_text("# Phase 3 relation gold, development split (frozen 2026-10-07). Do not edit: changes need a new revision.\n"
                   "# Roles name each side (reaction/trigger, follow_up/original, effect/cause, commentary/subject).\n"
                   + yaml.safe_dump(gold, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8", newline="\n")
    labels = Counter(g["label"] for g in gold.values())
    canon = Counter(g["label"] for g in gold.values() if g["canonical"])
    inferred = Counter(g["label"] for g in gold.values() if g["evidence"] == "inferred")
    types = sorted(RUNTIME)
    manifest = yaml.safe_load((GOLD / "manifest.yaml").read_text(encoding="utf-8"))
    manifest.update({
        "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "state": "FROZEN: relation gold revision 1 (development split); owner verdict snapshot unchanged",
        "revision": 1,
        "cases_frozen": len(gold), "deferred_owner_debate": DEFERRED_DEBATE,
        "labels": dict(labels),
        "canonical_positives": {t: canon.get(t, 0) for t in types},
        "inferred_positives (non-canonical)": {t: inferred.get(t, 0) for t in types if inferred.get(t)},
        "scored_cases": sum(1 for g in gold.values() if g["scored"]),
        "runtime_taxonomy": RUNTIME,
    })
    manifest["sha256"].update({"gold/relation-gold.yaml": sha(out), "gold/owner-verdicts.snapshot.yaml": sha(snap),
                               "scripts/freeze_relation_gold.py": sha(Path(__file__))})
    manifest.pop("confirmed_positives_settled", None)
    manifest.pop("positives_incl_pending", None)
    manifest.pop("status", None)
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=120),
                                        encoding="utf-8", newline="\n")
    print(json.dumps({k: manifest[k] for k in ("cases_frozen", "labels", "canonical_positives",
                                               "inferred_positives (non-canonical)", "scored_cases")},
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
