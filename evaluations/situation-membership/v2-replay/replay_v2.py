"""Development replay of the Situation-v2 candidate on the frozen 126-case DIAGNOSTIC set (not acceptance).

Blind to the owner labels: reads the evaluation set's case list (manifest), key (Development and Situation per case)
and founders (scopes.json), never the labels. Works on a backup-API copy of the snapshot; nothing is written to it.

    python replay_v2.py SNAPSHOT_DB EVALSET_DIR OUT_DIR [--overrides SCOPE_OVERRIDES_YAML]

Writes OUT_DIR/decisions-<variant>.json (the frozen scorer's candidate format: entered | rejected | linked_context)
and OUT_DIR/details-<variant>.json (v2 outcome, reason, evidence per case; the v2 Situations built).
Variants: ``derived`` (founder-derived scope) and, with --overrides, ``overrides`` (OD7 scopes mapped by
``map_override`` -- a proposed mapping the owner reviews before any code freeze).
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")

FAMILY_WORDS = {
    "diplomacy": ["diplomacy", "diplomatic", "meeting", "summit", "visit", "statement", "negotiation", "talks"],
    "armed_conflict": ["military", "war", "attack", "strike", "drone", "missile", "army", "clashes", "ceasefire"],
    "security": ["security", "espionage", "spy", "sabotage", "terror", "warning", "threat", "crime"],
    "economic": ["economic", "economy", "sanction", "sanctions", "trade", "tariff", "investment", "finance"],
    "politics": ["political", "politics", "election", "elections", "midterms", "government", "protest", "protests"],
    "hazard": ["natural calamities", "calamity", "disaster", "hurricane", "storm", "earthquake", "flood"],
}


def map_override(entry: dict, geo, norm) -> tuple[set[str], set[str]]:
    """Owner free text -> (families, countries). Deterministic word and gazetteer matching; a proposal for review."""
    from osint_monitor.processors.situations.v2 import FAMILY_OF, fold
    text = fold(" ".join(entry["new_value"].get("domains_or_types") or [])).lower()
    fams = {f for f, words in FAMILY_WORDS.items() if any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in words)}
    fams |= {FAMILY_OF[t] for t in FAMILY_OF if re.search(r"\b" + t + r"\b", text)}
    countries = set()
    for chunk in re.split(r"[;,/()]| and ", " ; ".join(entry["new_value"].get("places") or [])):
        c = chunk.strip()
        if not c:
            continue
        countries |= place_countries(c, geo, norm)
    return fams, countries


def place_countries(name: str, geo, norm) -> set[str]:
    from osint_monitor.processors.entity_resolver import normalise
    k = norm.key(name) or normalise(name)
    out = set()
    for cand in (k, normalise(name)):
        c = geo.canonical(cand)
        if c in geo.countries:
            out.add(c)
        else:
            out |= set(geo.ancestors(c)) & set(geo.countries)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot")
    ap.add_argument("evalset", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--overrides", type=Path)
    a = ap.parse_args()

    import yaml
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_situations_config
    from osint_monitor.core.database import Event, EventEntity, EventItem, RawItem, Situation
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.development_segmentation import REPORT, headline_kind
    from osint_monitor.processors.geography import Gazetteer
    from osint_monitor.processors.principals import _lead, mark_principal_actors
    from osint_monitor.processors.situations.canonical import ActorCanonicalizer
    from osint_monitor.processors.situations.store import _specific_places
    from osint_monitor.processors.situations import v2 as V

    ids = json.loads((a.evalset / "subsample" / "manifest.json").read_text(encoding="utf-8"))["case_ids"]
    key = json.loads((a.evalset / "key.json").read_text(encoding="utf-8"))["cases"]
    scopes = json.loads((a.evalset / "scopes.json").read_text(encoding="utf-8"))
    founders_of = {x["slug"]: [f["development_id"] for f in x["founders"]] for x in scopes["automatic"]}

    tmp = Path(tempfile.mkdtemp(prefix="sitv2-")) / "copy.db"
    src = sqlite3.connect(f"file:{a.snapshot}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    norm = ActorNormalizer.load()
    canon = ActorCanonicalizer(normalizer=norm)
    geo = Gazetteer.load()

    need = sorted({key[c]["development_id"] for c in ids} | {d for fs in founders_of.values() for d in fs})
    now = datetime.utcnow()
    s.query(Event).filter(Event.id.in_(need)).update({Event.last_updated_at: now}, synchronize_session=False)
    s.commit()
    mark_principal_actors(s, now=now + timedelta(seconds=1), window_days=1, normalizer=norm)

    def country_of_place(p: str) -> str | None:
        anc = set(geo.ancestors(p)) & set(geo.countries)
        return sorted(anc)[0] if len(anc) == 1 else None

    def features(eid: int) -> "V.DevFeatures":
        ev = s.get(Event, eid)
        names = [ee.entity.canonical_name for ee in s.query(EventEntity).filter_by(event_id=eid, is_principal=True)
                 if ee.entity]
        rows = s.query(RawItem).join(EventItem, EventItem.item_id == RawItem.id).filter(EventItem.event_id == eid).all()
        titles = [r.title or "" for r in rows]
        head_row = next((r for r in rows if (r.title or "") == (ev.summary or "")), rows[0] if rows else None)
        lead = _lead(head_row.content) if head_row is not None else ""
        places = {p: country_of_place(p) for p in _specific_places(s, eid)}
        countries = {c for c in places.values() if c}
        reports = sum(1 for t in titles if headline_kind(t) == REPORT)
        return V.DevFeatures(
            event_id=eid, headline=ev.summary or "", lead=lead or "", first_reported_at=ev.first_reported_at,
            parties=canon.keys(names), has_principals=bool(names), family=V.family_of(ev.event_type),
            places=places, event_country=next(iter(countries)) if len(countries) == 1 else None,
            report_share=reports / len(titles) if titles else 0.0,
            hazard=V.hazard_of(titles + [_lead(r.content) or "" for r in rows]),
            hedges=V.hedge_terms(f"{ev.summary or ''} {lead or ''}"), mixed=None)

    feats = {eid: features(eid) for eid in need}
    status = {x.slug: x.status for x in s.query(Situation)}

    def party_countries(keys) -> set[str]:
        return {geo.canonical(k) for k in keys if geo.is_country(k)}

    overrides = {}
    if a.overrides:
        ov = yaml.safe_load(a.overrides.read_text(encoding="utf-8"))
        overrides = {e["slug"]: e for e in ov["overrides"]}

    def build(variant: str):
        sits: dict[str, list] = {}
        why: dict[str, str] = {}
        mapping = {}
        for seed in load_situations_config().situations:
            anchors = canon.keys(seed.primary_actors)
            sits[seed.slug] = [V.Situation2(seed.slug, "seeded", anchors, frozenset(), frozenset(party_countries(anchors)),
                                            keywords=tuple(seed.keywords), status=status.get(seed.slug, "active"),
                                            scope_source="seed")]
        for x in scopes["automatic"]:
            slug = x["slug"]
            anchors = canon.keys(x["primary_actors"])
            made, reason = V.derive_automatic(slug, anchors, [feats[d] for d in founders_of[slug]],
                                              party_countries(anchors))
            for m in made:
                m.status = status.get(slug, "active")
                if variant == "overrides" and slug in overrides:
                    fams, cs = map_override(overrides[slug], geo, norm)
                    mapping[slug] = {"families": sorted(fams), "countries": sorted(cs)}
                    if fams:
                        m.families = frozenset(fams) if m.mode != "single_party" else m.families
                    if cs:
                        m.place_scope = frozenset(cs | party_countries(anchors))
                    m.scope_source, m.scope_version = "owner_override", 2
            sits[slug] = made
            if not made:
                why[slug] = reason
        return sits, why, mapping

    a.out.mkdir(parents=True, exist_ok=True)
    for variant in (["derived"] + (["overrides"] if a.overrides else [])):
        sits, why, mapping = build(variant)
        everything = [m for ms in sits.values() for m in ms]
        decisions, details = {}, {}
        for c in ids:
            k = key[c]
            d = feats[k["development_id"]]
            mine = sits.get(k["situation"], [])
            if not mine:
                dec = V.Decision("NOT_MEMBER", "SITUATION_NOT_REPRODUCED",
                                 {"why": why.get(k["situation"], "unknown"), "contract_version": V.CONTRACT_VERSION})
            else:
                target = next((m for m in mine if d.family and d.family in m.families), mine[0])
                dec = V.decide(d, target, everything)
            decisions[c] = {"decision": {"MEMBER": "entered", "CONTEXT": "linked_context"}.get(dec.outcome, "rejected"),
                            "reason": dec.reason, "evidence": dec.evidence}
            details[c] = {"development_id": k["development_id"], "situation": k["situation"],
                          "outcome": dec.outcome, "reason": dec.reason}
        rule = f"situation-v2 candidate ({variant} scope), {V.CONTRACT_VERSION}"
        (a.out / f"decisions-{variant}.json").write_text(json.dumps({"rule": rule, "decisions": decisions},
                                                                    ensure_ascii=False, indent=1) + "\n",
                                                         encoding="utf-8", newline="\n")
        (a.out / f"details-{variant}.json").write_text(json.dumps({
            "rule": rule, "cases": details,
            "situations": {slug: [{"slug": m.slug, "mode": m.mode, **m.snapshot(), "scope_source": m.scope_source,
                                   "founders": list(m.founders)} for m in ms] for slug, ms in sits.items()},
            "not_reproduced": why, "override_mapping": mapping,
            "features": {str(e): {"parties": sorted(f.parties), "family": f.family, "event_country": f.event_country,
                                  "places": f.places, "report_share": round(f.report_share, 3),
                                  "hazard": f.hazard, "hedges": f.hedges} for e, f in feats.items()},
        }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print(variant, "decisions:", {o: sum(1 for x in details.values() if x["outcome"] == o)
                                      for o in sorted({x["outcome"] for x in details.values()})})
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
