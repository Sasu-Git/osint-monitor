"""Summary metrics. Two kinds, kept apart:

* ``structural_summary``: label-free counts (assignments, reasons, creations, input coverage). Safe in smoke.
* ``score_cases``: membership recall / precision, false joins and creation matches against FROZEN owner labels.
  Called only in final mode (and in tests with synthetic labels). It reports numbers and no verdict: the PROPOSED gates
  of the frozen preregistration are attached as PROPOSED context by the caller, never applied here.

Case mapping (the frozen eval set names a runtime Situation per case). The v2 counterparts of a runtime Situation
are its seeded twin (same slug), or the v2 Situations whose anchor parties equal the runtime Situation's
re-normalised primary actors, or whose founders include one of the runtime Situation's founders. Same rule as the
earlier diagnostic replay, so results stay comparable.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Callable

NON_MEMBER = ("CONTEXT", "SPILLOVER", "OTHER_SITUATION", "NOT_MEMBER")


def structural_summary(result, bases_n: int) -> dict:
    rows = result.rows
    created = result.created
    feats = result.features.values()
    return {
        "developments_replayed": len(rows),
        "developments_in_snapshot_window": bases_n,
        "assigned_at_step": sum(1 for r in rows if r["decision"]["assigned"]),
        "assigned_final": len(result.assigned),
        "assignments_by_situation": dict(sorted(Counter(result.assigned.values()).items())),
        "row_reasons": dict(sorted(Counter(r["reason"].split(":")[0] if r["reason"].startswith("ASSIGNED_RETRO")
                                           else r["reason"] for r in rows).items())),
        "situations_seeded": sum(1 for s in result.situations if s.mode == "seeded"),
        "situations_created": len(created),
        "situations_created_by_mode": dict(sorted(Counter(c["mode"] for c in created).items())),
        "situations_created_slugs": [c["slug"] for c in created],
        "input_coverage": {
            "family_none": sum(1 for f in feats if not f.family),
            "no_principals": sum(1 for f in result.features.values() if not f.has_principals),
            "no_event_country": sum(1 for f in result.features.values() if not f.event_country),
            "mixed_true": sum(1 for f in result.features.values() if f.mixed),
            "mixed_unknown": sum(1 for f in result.features.values() if f.mixed is None),
        },
    }


def counterparts(slug: str, sits: list, anchors_of: dict, founders_of: dict) -> list[str]:
    if any(x.slug == slug and x.mode == "seeded" for x in sits):
        return [slug]
    return [x.slug for x in sits if x.mode != "seeded" and (
        (anchors_of.get(slug) and x.anchors == anchors_of[slug]) or set(x.founders) & founders_of.get(slug, set()))]


def case_decisions(result, key: dict, case_ids: list[str], anchors_of: dict, founders_of: dict,
                   contract_version: str) -> tuple[dict, dict]:
    """Per eval-set case: decision in the frozen scorer's candidate format, plus details. Cases whose Development was
    not replayed (smoke window) are listed as ``not_replayed`` and left out of the decisions."""
    sits, assigned = result.situations, result.assigned
    by_dev = {r["development_id"]: r for r in result.rows}
    decisions, details, not_replayed = {}, {}, []
    for c in case_ids:
        k = key[c]
        eid = k["development_id"]
        if eid not in by_dev:
            not_replayed.append(c)
            continue
        cps = counterparts(k["situation"], sits, anchors_of, founders_of)
        got = assigned.get(eid)
        cand = {x["slug"]: x for x in by_dev[eid]["candidates"]}
        if got in cps:
            outcome, reason, dec = "MEMBER", "ASSIGNED", "entered"
        else:
            last = [cand[cp] for cp in cps if cp in cand]
            if not cps:
                outcome, reason = "NOT_MEMBER", "NO_COUNTERPART"
            elif got:
                outcome, reason = "OTHER_SITUATION", f"ASSIGNED_ELSEWHERE:{got}"
            elif last:
                outcome, reason = last[-1]["outcome"], last[-1]["reason"]
            else:
                outcome, reason = "NOT_MEMBER", "COUNTERPART_CREATED_LATER"
            dec = "linked_context" if outcome == "CONTEXT" else "rejected"
        decisions[c] = {"decision": dec, "reason": reason,
                        "evidence": {"counterparts": cps, "assigned": got, "contract_version": contract_version}}
        details[c] = {"development_id": eid, "situation": k["situation"], "counterparts": cps, "assigned": got,
                      "outcome": outcome, "reason": reason}
    return decisions, {"cases": details, "not_replayed": not_replayed}


def _ratio(n: int, d: int) -> dict:
    return {"n": n, "of": d, "rate": round(n / d, 4) if d else None}


def score_cases(decisions: dict, labels: dict[str, str], key: dict) -> dict:
    """Membership against frozen labels. AMBIGUOUS owner labels are excluded from precision and recall (as the frozen
    scorer does). A false join is a case the engine admitted whose owner label is neither MEMBER nor AMBIGUOUS."""
    ids = [c for c in decisions if c in labels]
    entered = {c for c in ids if decisions[c]["decision"] == "entered"}
    scored = [c for c in ids if labels[c] != "AMBIGUOUS"]
    owner_member = {c for c in scored if labels[c] == "MEMBER"}
    sys_member = {c for c in scored if c in entered}
    tp = owner_member & sys_member
    false_joins = sorted(c for c in sys_member if labels[c] != "MEMBER")
    pos = [c for c in ids if key[c].get("seed_group") == "positive"]
    return {
        "cases_scored": len(ids), "cases_without_label": sorted(set(decisions) - set(labels)),
        "member_recall": _ratio(len(tp), len(owner_member)),
        "member_precision": _ratio(len(tp), len(sys_member)),
        "false_joins": {"n": len(false_joins), "cases": false_joins,
                        "by_label": dict(sorted(Counter(labels[c] for c in false_joins).items()))},
        "non_member_label_rejected": {
            l: _ratio(sum(1 for c in scored if labels[c] == l and c not in entered),
                      sum(1 for c in scored if labels[c] == l)) for l in NON_MEMBER},
        "owner_ambiguous": _ratio(len(ids) - len(scored), len(ids)),
        "positive_seed_regressions": {"n": sum(1 for c in pos if c not in entered), "of": len(pos)},
    }


def creation_match(result, scopes: dict, anchors_of: dict, founders_of: dict) -> dict:
    """Of the runtime automatic Situations in the frozen eval set, how many have a v2 counterpart; and how many v2
    Situations were created in all (creations are reported by mode in the structural summary)."""
    autos = [x["slug"] for x in scopes["automatic"]]
    matched = [s for s in autos if counterparts(s, result.situations, anchors_of, founders_of)]
    return {"runtime_automatic_situations": _ratio(len(matched), len(autos)),
            "without_counterpart": sorted(set(autos) - set(matched)),
            "v2_situations_created": len(result.created)}


def evalset_alignment(cases: list[dict], conn, parse: Callable[[str], datetime]) -> dict:
    """The frozen eval set was built on an earlier snapshot. Check each case's Development against this one: present,
    same headline, same first_reported_at. Structural; no label."""
    rows = {i: (s, f) for i, s, f in conn.execute("SELECT id, summary, first_reported_at FROM events")}
    present = same = 0
    diff = []
    for c in cases:
        d = c["development"]
        r = rows.get(d["development_id"])
        if r is None:
            diff.append({"case_id": c["case_id"], "why": "missing"})
            continue
        present += 1
        if (r[0] or "") == (d["headline"] or "") and parse(r[1]) == parse(d["first_reported_at"]):
            same += 1
        else:
            diff.append({"case_id": c["case_id"], "why": "headline_or_time_differs"})
    return {"cases": len(cases), "development_present": present, "headline_and_time_equal": same,
            "differing": diff[:20], "differing_n": len(diff)}
