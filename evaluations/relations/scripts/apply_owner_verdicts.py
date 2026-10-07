"""Apply the owner's relation verdicts: build the relation gold candidate and the hash record.

    python evaluations/relations/scripts/apply_owner_verdicts.py

Reads review/owner-verdicts.yaml (authoritative), review/cases.json and review/draft-labels.json. Writes:

- gold/owner-verdicts.snapshot.yaml: the owner's verdicts and notes, verbatim, frozen as reviewed (2026-10-07)
- gold/relation-gold.candidate.yaml: one entry per case with its status
- gold/manifest.yaml: SHA-256 of every input and output

A case is ``settled`` unless it is listed below as pending owner discussion or as an identity suspect. Pending
and identity-suspect cases stay in the candidate with their owner label, but they are not settled gold. Only
settled cases count as confirmed positives. Nothing under holdout/ is read.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REVIEW, GOLD = ROOT / "review", ROOT / "gold"

# Owner questions, conditional or contradicting verdicts, and taxonomy-policy questions (owner-review-summary.md §3)
PENDING = {
    "R002": "direction convention; owner reads it as 'follow-up or commentary' (commentary policy)",
    "R005": "conditional verdict ('if they are both analysis pieces'); commentary policy",
    "R008": "note says 'a reaction to', label caused_by; direction convention -> proposed reaction_to A->B",
    "R029": "inferred reaction (owner: activists 'precisely because' of the re-establishment); explicit-evidence rule",
    "R036": "commentary labelled reaction_to ('without the speech there is no commentary'); commentary policy",
    "R055": "verdict NO_RELATION but owner leans to reaction_to",
    "R056": "follow_up_to although 'not specifically linked as one thing'; direction convention",
    "R059": "caused_by through the object of an analysis piece (the cause is the rejection, not in the pair)",
    "R060": "label co_caused_with but note begins 'No relation'",
    "R076": "inferred reaction ('not important that the reaction be to the exact event'); explicit-evidence rule",
    "R087": "owner asks 'are we sure ... should be a followup' while the verdict is NO_RELATION",
    "R105": "two commentaries on one event labelled same_visit_or_summit; commentary policy",
    "R115": "owner asks for a take: co_caused_with for two commentary pieces",
    "R123": "owner: 'separate acts but same development'; follow_up_to or co_caused_with",
    "R127": "caused_by contradicted by the text: B's rescue follows the previous day's mall attack, not A's strikes",
    "R132": "owner asks for a take: co_caused_with (both name Trump's rejection)",
}
IDENTITY = {
    "R012": "agree: one matter (taxpayer-funded Trump ads) by two outlets -> identity review",
    "R098": "evidence suggests two different General Assembly meetings (general debate vs the 28 Sep "
            "high-level nuclear meeting) -> owner discussion",
    "R134": "evidence: a government statistics release vs a leasing-market feature, same topic -> owner discussion",
    "R138": "agree: the 29 Sep White House AI luncheon / America.gov, es-it vs en (cross-language split) -> identity review",
}
ANNOTATIONS = {
    "R045": "owner keeps the lifecycle relation even if the two sides are one Development ('one lifecycle is fine')",
    "R064": "side A (system D9) is a mixed Development: Macron's visit plus Spain's housing crisis; the relation holds "
            "for its Macron items; D9 routed to identity review",
    "R066": "the Daily News body is truncated in the feed (only the opening item is stored): the verdict was given on "
            "limited evidence",
    "R114": "condition met: B's coverage includes 'Security Council LIVE: ... as Ebola deepens crisis'",
    "R124": "owner confirms the AI remarks were made during the France tour",
}
RELATIONS = ["same_calamity_lifecycle", "same_visit_or_summit", "same_attack_wave", "reaction_to", "follow_up_to",
             "caused_by", "co_caused_with"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    verdicts = yaml.safe_load((REVIEW / "owner-verdicts.yaml").read_text(encoding="utf-8"))
    cases = {c["case"]: c for c in json.loads((REVIEW / "cases.json").read_text(encoding="utf-8"))["cases"]}
    drafts = json.loads((REVIEW / "draft-labels.json").read_text(encoding="utf-8"))
    assert set(verdicts) == set(cases) and all((verdicts[c] or {}).get("label") for c in cases), "unreviewed cases"
    GOLD.mkdir(exist_ok=True)
    snap = GOLD / "owner-verdicts.snapshot.yaml"
    snap.write_bytes((REVIEW / "owner-verdicts.yaml").read_bytes())          # verbatim
    out = {}
    for cid in sorted(cases):
        v, c, d = verdicts[cid], cases[cid], drafts[cid]
        status = "pending_owner_discussion" if cid in PENDING else "identity_suspect" if cid in IDENTITY else "settled"
        out[cid] = {
            "a": c["a"]["id"], "b": c["b"]["id"],
            "owner_label": v["label"], "owner_direction": v.get("direction"), "owner_note": v.get("note"),
            "draft_label": d["label"], "draft_direction": d["direction"] if d["direction"] != "none" else None,
            "status": status,
            "open_question": PENDING.get(cid) or IDENTITY.get(cid),
            "annotation": ANNOTATIONS.get(cid),
        }
    cand = GOLD / "relation-gold.candidate.yaml"
    cand.write_text("# Relation gold candidate (owner verdicts applied). NOT a frozen gold: cases with status\n"
                    "# pending_owner_discussion / identity_suspect are unsettled. See ../owner-review-summary.md.\n"
                    + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8",
                    newline="\n")
    status = Counter(x["status"] for x in out.values())
    labels = Counter(x["owner_label"] for x in out.values())
    settled_pos = Counter(x["owner_label"] for x in out.values()
                          if x["status"] == "settled" and x["owner_label"] in RELATIONS)
    all_pos = Counter(x["owner_label"] for x in out.values() if x["owner_label"] in RELATIONS)
    manifest = {
        "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "state": "owner verdicts frozen verbatim; gold NOT frozen (owner discussion required)",
        "cases": len(out), "status": dict(status), "owner_labels": dict(labels),
        "confirmed_positives_settled": {r: settled_pos.get(r, 0) for r in RELATIONS},
        "positives_incl_pending": {r: all_pos.get(r, 0) for r in RELATIONS},
        "sha256": {p: sha(ROOT / p) for p in ("gold/owner-verdicts.snapshot.yaml", "gold/relation-gold.candidate.yaml",
                                               "review/cases.json", "review/draft-labels.json",
                                               "review/relation-review-sheet.md", "taxonomy.md")},
        "holdout_seal": "holdout/SEALED.yaml unchanged; not opened",
    }
    (GOLD / "manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
                                        encoding="utf-8", newline="\n")
    print(json.dumps({k: manifest[k] for k in ("status", "owner_labels", "confirmed_positives_settled",
                                               "positives_incl_pending")}, indent=1))


if __name__ == "__main__":
    main()
