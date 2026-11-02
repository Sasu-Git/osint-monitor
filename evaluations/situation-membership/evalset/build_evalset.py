"""Build the blind Situation-membership evaluation set (CONTRACT-V2 section 4). Builds, never scores.

Reads ONLY a frozen snapshot, opened read-only (sqlite ``mode=ro``); verifies its sha256 first. Writes, next to this
script: ``cases.json`` (blind), ``key.json`` (sealed), ``scopes.json``, ``owner-labels.yaml`` (empty template).

Population (deterministic, seed 20261102):
  (a) every current member of every open Situation (status active or dormant; closed/retired excluded);
  (b) near-misses: unassigned Developments that today's grouper scores in [0.4, 0.6) against an open Situation
      (``SituationGrouper().explain`` on ``signature_for_event`` / ``load_profiles``), capped per Situation and
      sampled deterministically;
  (c) the seed cases of CONTRACT-V2 section 4, each paired with its current Situation (or, if unassigned, the
      best-scoring open candidate).
A (Development, Situation) pair appears once; its origin is ``seed`` > ``member`` > ``near_miss`` and every origin
it qualifies under is kept in the key.

Usage:
  PYTHONPATH=<worktree> PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 python build_evalset.py --snapshot <snap.db>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.config import load_situations_config
from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem, Situation, Source
from osint_monitor.processors.situations import SituationGrouper
from osint_monitor.processors.situations.store import ACTOR_ENTITY_TYPES, load_profiles, signature_for_event

HERE = Path(__file__).resolve().parent
SEED = 20261102
EXPECTED_SNAPSHOT_SHA256 = "b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40"
OPEN_STATUSES = ("active", "dormant")
NEAR_MISS_BAND = (0.4, 0.6)          # [low, high)
NEAR_MISS_CAP_PER_SITUATION = 10
MAX_REPORTS = 8
LF = "\n"   # outputs are written with LF on every platform, so their hashes are reproducible

SEED_CASES = {
    "positive": [84, 99, 124, 417, 1086, 303, 395, 884, 2, 497],
    "negative": [959, 880, 387, 439, 49, 34, 542, 1010, 1145, 1138],
    "boundary": [12, 64, 811, 214, 242, 112, 1147, 710, 188],
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iso(dt) -> str | None:
    return dt.isoformat() if dt else None


def open_readonly(snapshot: Path):
    url = f"sqlite:///file:{snapshot.as_posix()}?mode=ro&uri=true"
    engine = create_engine(url, connect_args={"uri": True})
    return engine, sessionmaker(bind=engine)()


def principal_and_mentioned(session, event_id: int) -> tuple[list[str], list[str]]:
    rows = (session.query(Entity.canonical_name, Entity.entity_type, EventEntity.is_principal)
            .join(EventEntity, EventEntity.entity_id == Entity.id)
            .filter(EventEntity.event_id == event_id).order_by(Entity.canonical_name).all())
    principals = sorted({n for n, _, p in rows if p and n})
    mentioned = sorted({n for n, t, p in rows if not p and n and t in ACTOR_ENTITY_TYPES} - set(principals))
    return principals, mentioned


def reports(session, event_id: int) -> tuple[list[dict], int]:
    rows = (session.query(RawItem.title, Source.name, RawItem.published_at, RawItem.id)
            .join(EventItem, EventItem.item_id == RawItem.id)
            .outerjoin(Source, Source.id == RawItem.source_id)
            .filter(EventItem.event_id == event_id).all())
    rows.sort(key=lambda r: (r[2] is None, r[2] or 0, r[3]))
    return ([{"headline": t or "", "source": s or "", "published_at": iso(p)} for t, s, p, _ in rows[:MAX_REPORTS]],
            len(rows))


def development_view(session, event: Event) -> dict:
    principals, mentioned = principal_and_mentioned(session, event.id)
    reps, n = reports(session, event.id)
    return {
        "development_id": event.id,
        "headline": event.summary,
        "summary": event.development_summary,
        "first_reported_at": iso(event.first_reported_at),
        "principal_actors": principals,
        "other_mentioned_actors": mentioned,
        "domain": event.event_domain,
        "event_type": event.event_type,
        "region": event.region,
        "report_count": n,
        "reports": reps,
    }


def build(snapshot: Path, out: Path, verify: bool = True) -> dict:
    if verify:
        got = sha256(snapshot)
        if got != EXPECTED_SNAPSHOT_SHA256:
            sys.exit(f"snapshot sha256 mismatch: {got} != {EXPECTED_SNAPSHOT_SHA256}")
    engine, session = open_readonly(snapshot)
    cfg = load_situations_config()
    grouper = SituationGrouper(cfg)
    seeded = {s.slug: s for s in cfg.situations}

    open_sits = (session.query(Situation).filter(Situation.status.in_(OPEN_STATUSES))
                 .order_by(Situation.id).all())
    open_by_id = {s.id: s for s in open_sits}
    profiles = {p.slug: p for p in load_profiles(session, cfg) if p.situation_id in open_by_id}

    sig_cache: dict[int, object] = {}

    def sig(event):
        if event.id not in sig_cache:
            sig_cache[event.id] = signature_for_event(session, event)
        return sig_cache[event.id]

    def explain(event, slug):
        e = grouper.explain(sig(event), profiles[slug])
        s = sig(event)
        e["actors_are_principal"] = s.actors_are_principal
        e["signature_actors"] = list(s.actors)
        e["specific_places"] = list(s.places)
        return e

    pairs: dict[tuple[int, str], dict] = {}

    def add(event_id: int, slug: str, origin: str, **extra):
        p = pairs.setdefault((event_id, slug), {"origins": [], "seed_group": None})
        if origin not in p["origins"]:
            p["origins"].append(origin)
        p.update({k: v for k, v in extra.items() if v is not None})

    # (a) members
    for s in open_sits:
        for (eid,) in session.query(Event.id).filter(Event.situation_id == s.id).order_by(Event.id):
            add(eid, s.slug, "member")

    # (b) near-misses
    unassigned = session.query(Event).filter(Event.situation_id.is_(None)).order_by(Event.id).all()
    band: dict[str, list[tuple[int, float]]] = defaultdict(list)
    near_miss_explain: dict[tuple[int, str], dict] = {}
    for ev in unassigned:
        for slug in profiles:
            e = explain(ev, slug)
            if e["candidate"] and NEAR_MISS_BAND[0] <= e["score"] < NEAR_MISS_BAND[1]:
                band[slug].append((ev.id, e["score"]))
                near_miss_explain[(ev.id, slug)] = e
    rng = random.Random(SEED)
    near_miss_population = {slug: len(v) for slug, v in sorted(band.items())}
    for slug in sorted(band):
        ids = sorted(eid for eid, _ in band[slug])
        chosen = ids if len(ids) <= NEAR_MISS_CAP_PER_SITUATION else sorted(rng.sample(ids, NEAR_MISS_CAP_PER_SITUATION))
        for eid in chosen:
            add(eid, slug, "near_miss")

    # (c) seed cases
    seed_unpaired = []
    for group, ids in SEED_CASES.items():
        for eid in ids:
            ev = session.get(Event, eid)
            if ev is None:
                seed_unpaired.append({"development_id": eid, "why": "not in snapshot"})
                continue
            if ev.situation_id in open_by_id:
                slug = open_by_id[ev.situation_id].slug
            else:
                cands = [e for e in (explain(ev, s) for s in profiles) if e["candidate"]]
                if not cands:
                    seed_unpaired.append({"development_id": eid, "why": "unassigned and no open candidate"})
                    continue
                slug = max(cands, key=lambda e: (e["score"], e["slug"]))["slug"]
            add(eid, slug, "seed", seed_group=group)

    # case records
    sit_by_slug = {s.slug: s for s in open_sits}
    situations_view = {}
    for s in open_sits:
        seed = seeded.get(s.slug)
        situations_view[s.slug] = {
            "slug": s.slug, "title": s.title,
            "kind": "seeded" if seed else "automatic",
            "primary_actors": list(s.primary_actors or []),
            "description": (seed.short_description if seed else (s.short_description or "")),
            "region": s.region,
        }

    keys = sorted(pairs)
    order = list(range(len(keys)))
    random.Random(SEED + 1).shuffle(order)
    cases, key = [], {}
    for n, idx in enumerate(order, start=1):
        eid, slug = keys[idx]
        case_id = f"S{n:03d}"
        ev = session.get(Event, eid)
        sit = sit_by_slug[slug]
        cases.append({"case_id": case_id, "situation": situations_view[slug], "development": development_view(session, ev)})
        info = pairs[(eid, slug)]
        origins = info["origins"]
        origin = "seed" if "seed" in origins else ("member" if "member" in origins else "near_miss")
        e = near_miss_explain.get((eid, slug)) or explain(ev, slug)
        current_slug = open_by_id[ev.situation_id].slug if ev.situation_id in open_by_id else None
        key[case_id] = {
            "development_id": eid, "situation": slug, "situation_kind": situations_view[slug]["kind"],
            "origin": origin, "origins": sorted(origins), "seed_group": info["seed_group"],
            "current_member": ev.situation_id == sit.id,
            "current_situation_of_development": current_slug,
            "grouper_explain_today": e,
            "is_routine_commentary": ev.is_routine_commentary,
        }

    # scopes
    scopes = {"note": ("Derived facts only. The owner's intended scope for each automatic Situation is recorded in "
                       "owner-labels.yaml under situation_scopes (this file stays frozen)."),
              "founder_derivation": ("No founder record is stored. Founders = members whose first_reported_at is at or "
                                     "before the Situation's created_at; exact_actor_set says whether the member's "
                                     "canonical principal actor set equals the Situation's actor set (the creation "
                                     "rule). If none qualify, the two earliest members are used and flagged. The derived scope uses the "
                                     "exact-actor-set founders when there are any, else all listed founders "
                                     "(derived_from says which). Domains and event types come from the rules "
                                     "classifier, whose reliability for scope is unmeasured (CONTRACT-V2 D5)."),
              "automatic": [], "seeded": []}
    for s in open_sits:
        if s.slug in seeded:
            seed = seeded[s.slug]
            scopes["seeded"].append({"slug": s.slug, "title": seed.title, "scope_source": "seed (config/situations.yaml)",
                                     "primary_actors": list(seed.primary_actors), "region": seed.region,
                                     "description": seed.short_description, "keywords": list(seed.keywords),
                                     "status": s.status})
            continue
        members = session.query(Event).filter(Event.situation_id == s.id).order_by(Event.first_reported_at, Event.id).all()
        founders = [m for m in members if m.first_reported_at and s.created_at and m.first_reported_at <= s.created_at]
        fallback = not founders
        if fallback:
            founders = members[:2]
        sit_keys = grouper.actors.keys(s.primary_actors or [])
        fl = []
        for m in founders:
            sg = sig(m)
            fl.append({"development_id": m.id, "headline": m.summary, "first_reported_at": iso(m.first_reported_at),
                       "domain": m.event_domain, "event_type": m.event_type, "region": m.region,
                       "specific_places": list(sg.places),
                       "exact_actor_set": sg.actors_are_principal and grouper.actors.keys(sg.actors) == sit_keys})
        exact = [f for f in fl if f["exact_actor_set"]]
        basis = exact or fl
        scopes["automatic"].append({
            "slug": s.slug, "title": s.title, "status": s.status, "created_at": iso(s.created_at),
            "primary_actors": list(s.primary_actors or []), "region": s.region,
            "founders_fallback_two_earliest": fallback, "founders": fl,
            "derived_from": "exact_actor_set founders" if exact else "all listed founders (none has the exact actor set)",
            "derived": {"domains": sorted({f["domain"] for f in basis if f["domain"]}),
                        "event_types": sorted({f["event_type"] for f in basis if f["event_type"]}),
                        "specific_places": sorted({p for f in basis for p in f["specific_places"]})},
            "owner_intended_scope": None,
        })

    session.close()
    engine.dispose()

    # labels template
    automatic_slugs = [a["slug"] for a in scopes["automatic"]]
    template = {
        "instructions": ("Fill label (MEMBER | CONTEXT | SPILLOVER | OTHER_SITUATION | NOT_MEMBER | AMBIGUOUS), a "
                         "one-line reason and reviewer for every case; for every automatic Situation fill its intended "
                         "scope. See PREREGISTRATION.md. Do not open key.json."),
        "cases": [{"case_id": c["case_id"], "label": None, "reason": None, "reviewer": None} for c in cases],
        "situation_scopes": [{"slug": slug, "domains_or_types": None, "places": None, "note": None, "reviewer": None}
                             for slug in automatic_slugs],
    }

    out.mkdir(parents=True, exist_ok=True)
    dump = lambda obj: json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False)
    (out / "cases.json").write_text(dump({"evalset": "situation-membership", "seed": SEED,
                                          "situations": situations_view, "cases": cases}) + "\n", encoding="utf-8", newline=LF)
    counts = {"total": len(key), "by_origin": dict(Counter(v["origin"] for v in key.values())),
              "by_situation": dict(sorted(Counter(v["situation"] for v in key.values()).items(),
                                          key=lambda t: (-t[1], t[0]))),
              "by_situation_origin": {s: dict(Counter(v["origin"] for v in key.values() if v["situation"] == s))
                                      for s in sorted({v["situation"] for v in key.values()})},
              "seed_by_group": dict(Counter(v["seed_group"] for v in key.values() if v["seed_group"])),
              "near_miss_population_in_band": near_miss_population,
              "near_miss_cap_per_situation": NEAR_MISS_CAP_PER_SITUATION,
              "seed_cases_unpaired": seed_unpaired,
              "unassigned_developments_scanned": len(unassigned)}
    (out / "key.json").write_text(dump({"sealed": "Do not open before LABELS-FREEZE.json exists.",
                                        "snapshot_sha256": EXPECTED_SNAPSHOT_SHA256, "seed": SEED,
                                        "counts": counts, "cases": key}) + "\n", encoding="utf-8", newline=LF)
    (out / "scopes.json").write_text(dump(scopes) + "\n", encoding="utf-8", newline=LF)
    with open(out / "owner-labels.yaml", "w", encoding="utf-8", newline=LF) as f:
        yaml.safe_dump(template, f, allow_unicode=True, sort_keys=False, width=120)
    return counts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=HERE)
    a = ap.parse_args()
    counts = build(a.snapshot, a.out)
    print(json.dumps({k: counts[k] for k in ("total", "by_origin", "by_situation", "seed_by_group",
                                             "near_miss_population_in_band", "seed_cases_unpaired")}, indent=1))


if __name__ == "__main__":
    main()
