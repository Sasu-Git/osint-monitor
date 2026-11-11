"""Full chronological replay of the Situation-v2 candidate, scored on the 126-case DIAGNOSTIC set (not acceptance).

Replaces the founder-only rebuild of ``replay_v2.py``. Every Development of the snapshot is processed in first-report
order through ``v2.chronological``: seeded Situations (scope from the curated ``seeded-scopes.yaml``) plus the
Situations that v2 itself creates (actor-process, single-party per OD1, hazard per OD2). Blind to the owner labels.

Per case (Development D, runtime Situation S): S's v2 counterparts are the seeded Situation of the same slug, or the
v2 Situations whose anchor parties equal S's re-normalised primary actors or whose founders include one of S's
founders. Decision: D assigned to a counterpart -> MEMBER (entered); D's last decision against a counterpart was
CONTEXT -> linked_context; otherwise rejected, with the reason (assigned elsewhere, the decision's reason, or no
counterpart).

    python replay_v2_chrono.py SNAPSHOT_DB EVALSET_DIR SEEDED_SCOPES_YAML OUT_DIR
"""
import json
import os
import sqlite3
import sys
import tempfile
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")


def main(snapshot: str, evalset: str, seeded_path: str, out: str) -> int:
    import yaml
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_situations_config
    from osint_monitor.core.database import Event, EventEntity, EventItem, RawItem
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.development_segmentation import REPORT, headline_kind
    from osint_monitor.processors.geography import Gazetteer
    from osint_monitor.processors.principals import _lead, mark_principal_actors
    from osint_monitor.processors.situations.canonical import ActorCanonicalizer
    from osint_monitor.processors.situations.store import _specific_places
    from osint_monitor.processors.situations import v2 as V

    ev_dir, out_dir = Path(evalset), Path(out)
    ids = json.loads((ev_dir / "subsample" / "manifest.json").read_text(encoding="utf-8"))["case_ids"]
    key = json.loads((ev_dir / "key.json").read_text(encoding="utf-8"))["cases"]
    scopes = json.loads((ev_dir / "scopes.json").read_text(encoding="utf-8"))
    seeded_meta = {x["slug"]: x for x in yaml.safe_load(Path(seeded_path).read_text(encoding="utf-8"))["situations"]}

    tmp = Path(tempfile.mkdtemp(prefix="sitv2c-")) / "copy.db"
    src = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    norm = ActorNormalizer.load()
    canon = ActorCanonicalizer(normalizer=norm)
    geo = Gazetteer.load()

    now = datetime.utcnow()
    s.query(Event).update({Event.last_updated_at: now}, synchronize_session=False)
    s.commit()
    mark_principal_actors(s, now=now + timedelta(seconds=1), window_days=1, normalizer=norm)

    def country_of_place(p: str):
        anc = set(geo.ancestors(p)) & set(geo.countries)
        if geo.canonical(p) in geo.countries:
            return geo.canonical(p)
        return sorted(anc)[0] if len(anc) == 1 else None

    def features(ev) -> "V.DevFeatures":
        names = [ee.entity.canonical_name for ee in s.query(EventEntity).filter_by(event_id=ev.id, is_principal=True)
                 if ee.entity]
        rows = s.query(RawItem).join(EventItem, EventItem.item_id == RawItem.id).filter(EventItem.event_id == ev.id).all()
        titles = [r.title or "" for r in rows]
        head = next((r for r in rows if (r.title or "") == (ev.summary or "")), rows[0] if rows else None)
        lead = (_lead(head.content) if head is not None else "") or ""
        places = {p: country_of_place(p) for p in _specific_places(s, ev.id)}
        countries = {c for c in places.values() if c}
        return V.DevFeatures(
            event_id=ev.id, headline=ev.summary or "", lead=lead, first_reported_at=ev.first_reported_at,
            parties=canon.keys(names), has_principals=bool(names), family=V.family_of(ev.event_type),
            places=places, event_country=next(iter(countries)) if len(countries) == 1 else None,
            report_share=sum(1 for t in titles if headline_kind(t) == REPORT) / len(titles) if titles else 0.0,
            hazard=V.hazard_of(titles + [_lead(r.content) or "" for r in rows]),
            hedges=V.hedge_terms(f"{ev.summary or ''} {lead}"), mixed=None)

    devs = [features(ev) for ev in s.query(Event).order_by(Event.id)]
    feats = {d.event_id: d for d in devs}

    def party_countries(keys) -> set:
        return {geo.canonical(k) for k in keys if geo.is_country(k)}

    seeded = []
    for seed in load_situations_config().situations:
        meta = seeded_meta.get(seed.slug, {})
        anchors = canon.keys(seed.primary_actors)
        seeded.append(V.Situation2(seed.slug, "seeded", anchors, frozenset(meta.get("families", [])),
                                   frozenset(meta.get("place_scope", [])) or frozenset(party_countries(anchors)),
                                   keywords=tuple(seed.keywords), scope_source="seed_metadata_v1" if meta else "seed"))
    res = V.chronological(devs, seeded, party_countries)
    sits, assigned, log = res["situations"], res["assigned"], res["log"]

    founders_of = {x["slug"]: {f["development_id"] for f in x["founders"]} for x in scopes["automatic"]}
    anchors_of = {x["slug"]: canon.keys(x["primary_actors"]) for x in scopes["automatic"]}

    def counterparts(slug: str) -> list:
        if any(x.slug == slug and x.mode == "seeded" for x in sits):
            return [slug]
        return [x.slug for x in sits if x.mode != "seeded" and (
            (anchors_of.get(slug) and x.anchors == anchors_of[slug]) or set(x.founders) & founders_of.get(slug, set()))]

    decisions, details = {}, {}
    for c in ids:
        k = key[c]
        eid, cps = k["development_id"], counterparts(k["situation"])
        got = assigned.get(eid)
        if got in cps:
            outcome, reason, dec = "MEMBER", "ASSIGNED", "entered"
        else:
            last = [log[eid][cp] for cp in cps if cp in log.get(eid, {})]
            if not cps:
                outcome, reason = "NOT_MEMBER", "NO_COUNTERPART"
            elif got:
                outcome, reason = "OTHER_SITUATION", f"ASSIGNED_ELSEWHERE:{got}"
            elif last:
                outcome, reason = last[-1].outcome, last[-1].reason
            else:
                outcome, reason = "NOT_MEMBER", "COUNTERPART_CREATED_LATER"
            dec = "linked_context" if outcome == "CONTEXT" else "rejected"
        decisions[c] = {"decision": dec, "reason": reason,
                        "evidence": {"counterparts": cps, "assigned": got, "contract_version": V.CONTRACT_VERSION}}
        details[c] = {"development_id": eid, "situation": k["situation"], "counterparts": cps, "assigned": got,
                      "outcome": outcome, "reason": reason}

    rule = f"situation-v2 candidate, chronological replay, {V.CONTRACT_VERSION} + seeded-scopes v1"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "decisions-chrono.json").write_text(json.dumps({"rule": rule, "decisions": decisions}, ensure_ascii=False,
                                                              indent=1) + "\n", encoding="utf-8", newline="\n")
    created = [x for x in sits if x.mode != "seeded"]
    (out_dir / "details-chrono.json").write_text(json.dumps({
        "rule": rule, "cases": details,
        "situations": [{"slug": x.slug, "mode": x.mode, **x.snapshot(), "founders": list(x.founders),
                        "members": sum(1 for v in assigned.values() if v == x.slug)} for x in sits],
        "assignment_counts": dict(Counter(assigned.values())),
        "features_summary": {"developments": len(devs), "family_unknown": sum(1 for d in devs if not d.family),
                             "no_principals": sum(1 for d in devs if not d.has_principals),
                             "no_event_country": sum(1 for d in devs if not d.event_country)},
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(devs)} Developments; {len(created)} Situations created "
          f"({dict(Counter(x.mode for x in created))}); assigned {len(assigned)}; "
          f"case outcomes {dict(Counter(v['outcome'] for v in details.values()))}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(*sys.argv[1:5]))
