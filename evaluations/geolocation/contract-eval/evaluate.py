"""Evaluate the location contract (osint_monitor/processors/event_location.py) on frozen inputs, read-only.

    PYTHONPATH=<this branch> python evaluate.py --db <snapshot> --audit <audit cases.json> \
        --acceptance ../acceptance-cases.yaml --countries <web code tree> --out results.json

Inputs (hashes in FREEZE.md, frozen before the first run):
  - the 2026-11-02 snapshot (sha b5bb5728...), opened mode=ro;
  - the geolocation audit's hand-labelled cases (cases.json, eval/soak-safe-20261102 b794902): stored point country
    (point_country, ISO3) and stored verdict (C right / W wrong / P partly right);
  - the 15 acceptance cases (acceptance-cases.yaml, PROPOSED expectations).
Country names are mapped to ISO3 with the web code's CountryIndex (presentation lookup, read-only), disputed entities
(U4) to the outline they lie in for comparison only: west bank / gaza / east jerusalem -> PSE, crimea -> UKR,
western sahara -> ESH.

Metrics (no composite):
  - audit W (wrong stored point): REMOVED when the contract does not put it in the stored point's country again;
  - audit C (right stored point): PRESERVED when the contract's country is the stored point's country;
  - audit P: distribution only;
  - acceptance cases: role / country / confidence vs expectation; cases depending on unresolved decisions reported.
PROPOSED gates (owner approval needed; not established): W removed >= 80%, C preserved >= 90%.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--audit", required=True)
ap.add_argument("--acceptance", required=True)
ap.add_argument("--countries", required=True, help="a checkout with osint_monitor/api/geo.py (web code)")
ap.add_argument("--out", required=True)
a = ap.parse_args()

from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.event_location import Role, decide, mentions_for_event
from osint_monitor.processors.geography import Gazetteer
from osint_monitor.processors.provenance import ProvenanceResolver

import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("web_geo", Path(a.countries) / "osint_monitor" / "api" / "geo.py")
_web_geo = importlib.util.module_from_spec(_spec)   # the web code's country lookup, loaded by path (ISO mapping only)
_spec.loader.exec_module(_web_geo)
CountryIndex = _web_geo.CountryIndex

DISPUTED_ISO = {"west bank": "PSE", "gaza": "PSE", "east jerusalem": "PSE", "crimea": "UKR", "western sahara": "ESH"}
index, geo, normalizer, resolver = CountryIndex.load(), Gazetteer.load(), ActorNormalizer.load(), ProvenanceResolver()
iso = lambda c: None if c is None else DISPUTED_ISO.get(c) or index.of_place(c)
session = sessionmaker(bind=create_engine(f"sqlite:///file:{a.db}?mode=ro&uri=true"))()

def locate(eid):
    mentions, principals = mentions_for_event(session, eid, resolver)
    loc = decide(mentions, principals, geo, actor_key=normalizer.key)
    return loc, {"role": loc.role.value, "confidence": loc.confidence.value, "place": loc.place, "country": loc.country,
                 "country_iso": iso(loc.country), "places": loc.places, "region": loc.region, "reason": loc.reason,
                 "rejected": loc.rejected[:12], "mentions": len(mentions)}

audit = json.load(open(a.audit, encoding="utf-8"))
rows, tally = [], Counter()
for c in audit:
    loc, rec = locate(c["development_id"])
    v = c["stored_verdict"]
    stored = c.get("point_country")
    if v == "W":
        outcome = "REMOVED" if rec["country_iso"] != stored else "STILL_WRONG"
    elif v == "C":
        outcome = "PRESERVED" if rec["country_iso"] == stored else ("LOST_TO_NONE" if loc.role == Role.NONE else "CHANGED")
    else:
        outcome = "P:" + rec["role"]
    tally[(v, outcome)] += 1
    rows.append({"development_id": c["development_id"], "set": c["set"], "stored_verdict": v, "root_cause": c["root_cause"],
                 "stored_country": stored, "outcome": outcome, **rec, "headline": c["summary"][:120]})

accept = yaml.safe_load(open(a.acceptance, encoding="utf-8"))["cases"]
acc_rows = []
for case in accept:
    loc, rec = locate(case["development"])
    exp = case["expected"]
    checks = {}
    if "role" in exp and isinstance(exp["role"], str):
        checks["role"] = rec["role"] == exp["role"]
    if "country" in exp:
        checks["country"] = rec["country_iso"] == exp["country"]
    if "confidence" in exp:
        checks["confidence"] = rec["confidence"] == exp["confidence"]
    acc_rows.append({"id": case["id"], "development": case["development"], "depends_on": case.get("depends_on"),
                     "expected": exp, "got": rec, "checks": checks, "pass": all(checks.values()) if checks else None})

W = sum(n for (v, o), n in tally.items() if v == "W"); C = sum(n for (v, o), n in tally.items() if v == "C")
summary = {
    "audit_cases": len(rows),
    "W_total": W, "W_removed": tally[("W", "REMOVED")], "W_removed_share": round(tally[("W", "REMOVED")] / W, 3) if W else None,
    "C_total": C, "C_preserved": tally[("C", "PRESERVED")], "C_preserved_share": round(tally[("C", "PRESERVED")] / C, 3) if C else None,
    "C_lost_to_none": tally[("C", "LOST_TO_NONE")], "C_changed": tally[("C", "CHANGED")],
    "P_outcomes": {o: n for (v, o), n in tally.items() if v == "P"},
    "acceptance_pass": sum(1 for r in acc_rows if r["pass"]), "acceptance_total": len(acc_rows),
    "acceptance_failed": [r["id"] for r in acc_rows if r["pass"] is False],
    "proposed_gates": {"W_removed_share": ">= 0.80 (PROPOSED)", "C_preserved_share": ">= 0.90 (PROPOSED)"},
}
json.dump({"summary": summary, "audit": rows, "acceptance": acc_rows}, open(a.out, "w", encoding="utf-8"),
          indent=1, ensure_ascii=False, default=str)
print(json.dumps(summary, indent=1))
