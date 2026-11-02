"""Score Situation membership against the owner's frozen labels (CONTRACT-V2 section 4). NOT RUN ON REAL LABELS YET.

Scoring requires (1) owner labels frozen with ``labels_tool.py freeze`` (LABELS-FREEZE.json) and (2) a separate owner
approval to score, passed as ``--approval "<who, when, what>"``. Without both it refuses to run.

  python score.py --approval "..." [--dir DIR] [--candidate-decisions FILE] [--out FILE]
  python score.py --self-test        synthetic labels in a temporary directory; writes nothing here

Systems scored:
  * current_runtime: today's stored membership (key.json ``current_member``): member = entered, else rejected.
  * candidate (HOOK): a future rule's decisions, see ``load_candidate_decisions``. Not implemented as a rule here.

Reported, per system, overall and per Situation (no composite score):
  precision and recall of MEMBER; members kept; off-scope (owner NOT_MEMBER) rejected, and the rejection rate of each
  other non-member label; ambiguous rate; auditability (candidate only); positive-seed regressions.
Owner AMBIGUOUS cases are excluded from precision and recall and reported separately.
The gates are PROPOSED (PREREGISTRATION.md) and are reported as PROPOSED, never as a verdict on their own.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import labels_tool  # noqa: E402

DECISIONS = ("entered", "rejected", "linked_context")
NON_MEMBER = ("CONTEXT", "SPILLOVER", "OTHER_SITUATION", "NOT_MEMBER")
GATES_PROPOSED = {"owner_member_kept_min": 0.90, "owner_not_member_rejected_min": 0.70,
                  "positive_seed_regressions_max": 0}


# -- inputs ---------------------------------------------------------------------------------------

def load_frozen_labels(d: Path) -> dict[str, dict]:
    lf = d / labels_tool.LABELS_FREEZE_FILE
    if not lf.exists():
        sys.exit("no LABELS-FREEZE.json: owner labels must be frozen before scoring")
    rec = json.loads(lf.read_text(encoding="utf-8"))
    if labels_tool.sha256(d / labels_tool.LABELS_FILE) != rec["labels_sha256"]:
        sys.exit("owner-labels.yaml changed after the freeze")
    errors = labels_tool.validate(d)
    if errors:
        sys.exit("labels or frozen set not valid:\n  " + "\n  ".join(errors[:20]))
    labels = yaml.safe_load((d / labels_tool.LABELS_FILE).read_text(encoding="utf-8"))
    return {e["case_id"]: e for e in labels["cases"]}


def load_key(d: Path) -> dict[str, dict]:
    return json.loads((d / "key.json").read_text(encoding="utf-8"))["cases"]


def runtime_decisions(key: dict[str, dict]) -> dict[str, dict]:
    """Today's runtime: a stored member is 'entered'; anything else 'rejected'. No evidence record exists."""
    return {cid: {"decision": "entered" if k["current_member"] else "rejected", "reason": None, "evidence": None}
            for cid, k in key.items()}


# ---------------------------------------------------------------------------------------------------
# HOOK: CANDIDATE RULE DECISIONS (future). A candidate rule (for example the CONTRACT-V2 rule once approved) is
# replayed on the same frozen snapshot, blind to the labels, and writes a JSON file:
#   {"rule": "<name and code sha>",
#    "decisions": {"S001": {"decision": "entered" | "rejected" | "linked_context",
#                           "reason": "<CONTRACT-V2 section 3 reason code>",
#                           "evidence": {...decision record fields...}}, ...}}
# Every case must have a decision. This function only loads and checks that file; the rule itself is not here.
# ---------------------------------------------------------------------------------------------------
def load_candidate_decisions(path: Path, key: dict[str, dict]) -> tuple[str, dict[str, dict]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    dec = raw["decisions"]
    missing = set(key) - set(dec)
    if missing:
        sys.exit(f"candidate decisions missing {len(missing)} cases, e.g. {sorted(missing)[:5]}")
    bad = {c: d.get("decision") for c, d in dec.items() if d.get("decision") not in DECISIONS}
    if bad:
        sys.exit(f"candidate decisions with values outside {DECISIONS}: {dict(list(bad.items())[:5])}")
    return raw.get("rule", "candidate"), {c: dec[c] for c in key}


# -- metrics --------------------------------------------------------------------------------------

def ratio(n: int, d: int) -> dict:
    return {"n": n, "of": d, "rate": round(n / d, 4) if d else None}


def metrics(cids: list[str], labels: dict, decisions: dict, key: dict, with_audit: bool) -> dict:
    lab = {c: labels[c]["label"] for c in cids}
    entered = {c for c in cids if decisions[c]["decision"] == "entered"}
    scored = [c for c in cids if lab[c] != "AMBIGUOUS"]
    owner_member = {c for c in scored if lab[c] == "MEMBER"}
    sys_member = {c for c in scored if c in entered}
    tp = owner_member & sys_member
    out = {
        "cases": len(cids),
        "precision_member": ratio(len(tp), len(sys_member)),
        "recall_member": ratio(len(tp), len(owner_member)),
        "members_kept": ratio(len(tp), len(owner_member)),
        "not_member_rejected": ratio(sum(1 for c in scored if lab[c] == "NOT_MEMBER" and c not in entered),
                                     sum(1 for c in scored if lab[c] == "NOT_MEMBER")),
        "non_member_label_rejected": {l: ratio(sum(1 for c in scored if lab[c] == l and c not in entered),
                                               sum(1 for c in scored if lab[c] == l)) for l in NON_MEMBER},
        "owner_ambiguous": ratio(len(cids) - len(scored), len(cids)),
    }
    if with_audit:
        out["system_ambiguous"] = ratio(sum(1 for c in cids if decisions[c].get("reason") == "AMBIGUOUS"), len(cids))
        # Mechanical part only: does a decision carry a reason code and an evidence record? Whether that record alone
        # explains the owner's label is a reviewer judgement and is not computed here.
        out["decisions_with_reason_and_evidence"] = ratio(
            sum(1 for c in cids if decisions[c].get("reason") and decisions[c].get("evidence")), len(cids))
    pos = [c for c in cids if key[c]["seed_group"] == "positive"]
    regress = [c for c in pos if c not in entered]
    out["positive_seed_regressions"] = {
        "all": {"n": len(regress), "of": len(pos), "cases": sorted(regress)},
        "seeded_situations_only": {"n": sum(1 for c in regress if key[c]["situation_kind"] == "seeded"),
                                   "of": sum(1 for c in pos if key[c]["situation_kind"] == "seeded")},
    }
    return out


def score_system(name: str, labels: dict, decisions: dict, key: dict, with_audit: bool) -> dict:
    by_sit = defaultdict(list)
    for c in key:
        by_sit[key[c]["situation"]].append(c)
    overall = metrics(sorted(key), labels, decisions, key, with_audit)
    gates = {
        "status": "PROPOSED (not approved; reported for information only)",
        "owner_member_kept": {"threshold": GATES_PROPOSED["owner_member_kept_min"],
                              "value": overall["members_kept"]["rate"]},
        "owner_not_member_rejected": {"threshold": GATES_PROPOSED["owner_not_member_rejected_min"],
                                      "value": overall["not_member_rejected"]["rate"]},
        "positive_seed_regressions": {"threshold": GATES_PROPOSED["positive_seed_regressions_max"],
                                      "value_all": overall["positive_seed_regressions"]["all"]["n"],
                                      "value_seeded_situations_only":
                                          overall["positive_seed_regressions"]["seeded_situations_only"]["n"]},
    }
    return {"system": name, "overall": overall, "gates_proposed": gates,
            "per_situation": {s: metrics(sorted(cs), labels, decisions, key, with_audit)
                              for s, cs in sorted(by_sit.items())}}


def run(d: Path, approval: str, candidate: Path | None) -> dict:
    labels = load_frozen_labels(d)
    key = load_key(d)
    if set(labels) != set(key):
        sys.exit("labels and key cover different cases")
    report = {"approval": approval, "evalset_dir": str(d),
              "labels_freeze": json.loads((d / labels_tool.LABELS_FREEZE_FILE).read_text(encoding="utf-8")),
              "systems": [score_system("current_runtime", labels, runtime_decisions(key), key, with_audit=False)]}
    if candidate:
        name, dec = load_candidate_decisions(candidate, key)
        report["systems"].append(score_system(f"candidate: {name}", labels, dec, key, with_audit=True))
    return report


# -- self-test (synthetic, temporary directory only) -------------------------------------------------

def self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        # 6 synthetic cases on two Situations; nothing real is read or written.
        key = {
            "S001": {"situation": "a-b", "situation_kind": "seeded", "seed_group": "positive", "current_member": True},
            "S002": {"situation": "a-b", "situation_kind": "seeded", "seed_group": None, "current_member": True},
            "S003": {"situation": "a-b", "situation_kind": "seeded", "seed_group": None, "current_member": False},
            "S004": {"situation": "c-d", "situation_kind": "automatic", "seed_group": "negative", "current_member": True},
            "S005": {"situation": "c-d", "situation_kind": "automatic", "seed_group": None, "current_member": False},
            "S006": {"situation": "c-d", "situation_kind": "automatic", "seed_group": "boundary", "current_member": True},
        }
        labels = {"S001": "MEMBER", "S002": "NOT_MEMBER", "S003": "MEMBER", "S004": "NOT_MEMBER",
                  "S005": "NOT_MEMBER", "S006": "AMBIGUOUS"}
        (d / "key.json").write_text(json.dumps({"cases": key}), encoding="utf-8")
        (d / "cases.json").write_text(json.dumps({"cases": [{"case_id": c} for c in key]}), encoding="utf-8")
        (d / "scopes.json").write_text(json.dumps({"automatic": [{"slug": "c-d"}], "seeded": []}), encoding="utf-8")
        hashes = "\n".join(f"{labels_tool.sha256(d / n)}  {n}" for n in ("cases.json", "key.json", "scopes.json"))
        (d / "FREEZE.md").write_text(f"# synthetic\n\n```sha256\n{hashes}\n```\n", encoding="utf-8")
        (d / labels_tool.LABELS_FILE).write_text(yaml.safe_dump({
            "cases": [{"case_id": c, "label": l, "reason": "synthetic", "reviewer": "self-test"} for c, l in labels.items()],
            "situation_scopes": [{"slug": "c-d", "domains_or_types": [], "places": [], "note": None,
                                  "reviewer": "self-test"}]}), encoding="utf-8")
        assert labels_tool.validate(d) == [], labels_tool.validate(d)
        labels_tool.freeze(d)
        cand = d / "candidate.json"
        cand.write_text(json.dumps({"rule": "synthetic", "decisions": {
            "S001": {"decision": "entered", "reason": "CONTINUATION", "evidence": {"coverage": 1.0}},
            "S002": {"decision": "rejected", "reason": "NO_SCOPE_SIGNAL", "evidence": {"coverage": 1.0}},
            "S003": {"decision": "entered", "reason": "CONTINUATION", "evidence": {"coverage": 1.0}},
            "S004": {"decision": "rejected", "reason": "OUT_OF_SCOPE_DOMAIN", "evidence": None},
            "S005": {"decision": "rejected", "reason": "LOW_COVERAGE", "evidence": {"coverage": 0.5}},
            "S006": {"decision": "rejected", "reason": "AMBIGUOUS", "evidence": {"runner_up": "a-b"}}}}),
            encoding="utf-8")
        r = run(d, "self-test (synthetic)", cand)
        rt, ca = r["systems"][0]["overall"], r["systems"][1]["overall"]
        # runtime: members entered S001,S002,S004 (S006 ambiguous excluded); owner MEMBER S001,S003
        assert rt["precision_member"] == {"n": 1, "of": 3, "rate": 0.3333}, rt["precision_member"]
        assert rt["recall_member"] == {"n": 1, "of": 2, "rate": 0.5}, rt["recall_member"]
        assert rt["not_member_rejected"] == {"n": 1, "of": 3, "rate": 0.3333}, rt["not_member_rejected"]
        assert rt["owner_ambiguous"]["n"] == 1
        assert rt["positive_seed_regressions"]["all"]["n"] == 0
        # candidate: entered S001,S003 -> precision 1, recall 1, NOT_MEMBER all rejected
        assert ca["precision_member"]["rate"] == 1.0 and ca["recall_member"]["rate"] == 1.0
        assert ca["not_member_rejected"]["rate"] == 1.0
        assert ca["system_ambiguous"]["n"] == 1
        assert ca["decisions_with_reason_and_evidence"]["n"] == 5
        assert r["systems"][0]["per_situation"]["c-d"]["recall_member"]["of"] == 0
        # a changed labels file after the freeze must be refused
        (d / labels_tool.LABELS_FILE).write_text((d / labels_tool.LABELS_FILE).read_text() + "\n# edited\n")
        try:
            load_frozen_labels(d)
        except SystemExit:
            pass
        else:
            raise AssertionError("edited labels were accepted after the freeze")
    print("self-test passed (synthetic labels in a temporary directory; nothing written to the evalset)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", type=Path, default=HERE)
    ap.add_argument("--approval", help="the owner's separate approval to score (who, when, what)")
    ap.add_argument("--candidate-decisions", type=Path, help="HOOK: a candidate rule's decisions (see source)")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
        return
    if not (a.approval and a.approval.strip()):
        sys.exit("scoring needs a separate owner approval: pass --approval")
    report = run(a.dir, a.approval, a.candidate_decisions)
    text = json.dumps(report, indent=1, ensure_ascii=False)
    if a.out:
        a.out.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
