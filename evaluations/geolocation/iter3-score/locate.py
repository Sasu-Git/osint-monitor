"""Iteration 3 scoring, run step 2: one system's country per sample case. Read-only (snapshot opened mode=ro).

    PYTHONPATH=<that system's code> python locate.py --system I3-all --rules 2a,3a,4a,5a \
        --db snap-20261105.db --countries <ab45312 checkout> --out outputs/I3-all.json

--rules is passed to decide(rules=...) only when given (iteration 1 and 2 code has no such parameter).
The country is mapped to ISO3 with the frozen lookup (LOOKUP-FREEZE.md): lookup-overrides.json, then DISPUTED_ISO,
then the web CountryIndex at ab45312.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import lookup_audit as la

HERE = Path(__file__).resolve().parent
MANIFEST = HERE.parent / "iter3-sample" / "manifest.json"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--system", required=True)
    ap.add_argument("--rules")
    ap.add_argument("--db", required=True)
    ap.add_argument("--countries", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    from osint_monitor.processors import event_location as el
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.geography import Gazetteer
    from osint_monitor.processors.provenance import ProvenanceResolver

    overrides = json.loads((HERE / "lookup-overrides.json").read_text(encoding="utf-8"))["overrides"]
    iso = la.make_iso(la.load_index(a.countries), overrides)
    geo, normalizer, resolver = Gazetteer.load(), ActorNormalizer.load(), ProvenanceResolver()
    session = sessionmaker(bind=create_engine(f"sqlite:///file:{a.db}?mode=ro&uri=true"))()
    kwargs = {"rules": [r for r in a.rules.split(",") if r]} if a.rules is not None else {}
    ids = [c["development_id"] for c in json.loads(MANIFEST.read_text(encoding="utf-8"))["cases"]]

    rows = {}
    for eid in ids:
        mentions, principals = el.mentions_for_event(session, eid, resolver)
        loc = el.decide(mentions, principals, geo, actor_key=normalizer.key, **kwargs)
        code = None if loc.role == el.Role.NONE or loc.country is None else iso(loc.country)
        rows[str(eid)] = {"country": code or "NONE", "role": loc.role.value, "confidence": loc.confidence.value,
                          "module_country": loc.country, "place": loc.place, "region": loc.region,
                          "reason": loc.reason}
    module = Path(el.__file__)
    out = {"system": a.system, "rules": kwargs.get("rules"), "module_path": str(module),
           "module_sha256": hashlib.sha256(module.read_bytes()).hexdigest(), "cases": rows}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(a.system, sum(1 for r in rows.values() if r["country"] != "NONE"), "of", len(rows), "with a country")


if __name__ == "__main__":
    main()
