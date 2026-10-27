"""Blast radius: how many Developments show D398-like signatures (read-only; descriptive, not a rule).

    python blast.py --db COPY.db --code-wt ../osint-monitor-timing --out giant-developments/blast-radius.csv

Per corroborated Development (source_count >= 2), from stored data only:
- size, publication span, membership growth days (distinct days members were stored), outlets, languages (the
  source's configured language, else "en"), distinct actors, places and specific anchors among members;
- analysis / live-blog / roundup members;
- representation drift: share of members stored after the first run whose cosine to the first run's centroid is
  below 0.53 (the cross-source link threshold);
- chaining: over the base link rule (cosine >= 0.53, within 72 h, different outlet; segmentation guards NOT
  applied, so this over-approximates links), the hop distance of each member from the first run's members through
  members stored before it; and the share of members whose best earlier link is below 0.58 (near the threshold).
Event-level classification (domain, type) is one value per Development; mixed domains per item are not stored.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

import numpy as np

LINK, NEAR, HOURS = 0.53, 0.58, 72


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--db", type=Path, required=True)
    p.add_argument("--code-wt", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    os.environ["OSINT_DB_URL"] = f"sqlite:///{a.db.resolve().as_posix()}"
    sys.path.insert(0, str(a.code_wt.resolve()))
    from osint_monitor.core.database import Entity, Event, EventItem, ItemEntity, RawItem, Source, get_session
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.actor_roles import is_roundup
    from osint_monitor.processors.development_segmentation import ACTOR_TYPES, LOCATION_TYPES, headline_kind
    from osint_monitor.processors.embeddings import blob_to_embedding
    from osint_monitor.processors.entity_resolver import normalise
    from osint_monitor.processors.language import configured_language

    s = get_session()
    events = {e.id: e for e in s.query(Event).filter(Event.source_count >= 2)}
    members = defaultdict(list)
    for ei in s.query(EventItem).filter(EventItem.event_id.in_(list(events))):
        members[ei.event_id].append(ei)
    item_ids = {ei.item_id for ms in members.values() for ei in ms}
    items = {}
    for r, src in (s.query(RawItem, Source.name).join(Source, Source.id == RawItem.source_id)
                   .filter(RawItem.id.in_(list(item_ids)))):
        items[r.id] = (r, src)
    normalizer = ActorNormalizer.load()
    actors, places = defaultdict(set), defaultdict(set)
    for chunk in (list(item_ids)[i:i + 900] for i in range(0, len(item_ids), 900)):
        for iid, name, et in (s.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                              .join(Entity, Entity.id == ItemEntity.entity_id).filter(ItemEntity.item_id.in_(chunk))):
            if et in ACTOR_TYPES and (k := normalizer.key(name)):
                actors[iid].add(k)
            if et in LOCATION_TYPES and (k := normalise(name)):
                places[iid].add(k)
    vec = {}
    for iid, (r, _) in items.items():
        if r.embedding:
            v = blob_to_embedding(r.embedding)
            vec[iid] = v / np.linalg.norm(v)

    rows = []
    for eid, ms in members.items():
        ms = sorted(ms, key=lambda x: (x.added_at or datetime.min, x.item_id))
        ids = [m.item_id for m in ms if m.item_id in items]
        if not ids:
            continue
        pub = [items[i][0].published_at or items[i][0].fetched_at for i in ids]
        first_run = ms[0].added_run_id
        seed = [m.item_id for m in ms if m.added_run_id == first_run]
        later = [m.item_id for m in ms if m.added_run_id != first_run]
        seedv = [vec[i] for i in seed if i in vec]
        drift = None
        if seedv and later:
            c = np.mean(seedv, axis=0)
            c /= np.linalg.norm(c)
            vals = [float(vec[i] @ c) for i in later if i in vec]
            drift = round(sum(v < LINK for v in vals) / len(vals), 3) if vals else None
        # chaining over the base link rule, through members stored earlier
        hop = {i: 0 for i in seed}
        near = 0
        with_link = 0
        for m in ms:
            n = m.item_id
            if n in hop or n not in vec:
                continue
            rn, sn = items[n]
            tn = rn.published_at or rn.fetched_at
            best, hs = None, []
            for e in [x.item_id for x in ms if (x.added_at or datetime.min, x.item_id) < (m.added_at or datetime.min, n) and x.added_run_id != m.added_run_id]:
                if e not in vec:
                    continue
                re_, se = items[e]
                te = re_.published_at or re_.fetched_at
                if se == sn or (tn and te and abs((tn - te).total_seconds()) > HOURS * 3600):
                    continue
                c = float(vec[n] @ vec[e])
                if c >= LINK:
                    best = c if best is None else max(best, c)
                    if hop.get(e) is not None:
                        hs.append(hop[e])
            hop[n] = min(hs) + 1 if hs else None
            if best is not None:
                with_link += 1
                near += best < NEAR
        hops = [h for h in hop.values() if h is not None]
        kinds = [headline_kind(items[i][0].title or "") for i in ids]
        langs = {configured_language(items[i][1]) or "en" for i in ids}
        e = events[eid]
        rows.append({
            "event_id": eid, "summary": e.summary[:120], "event_type": e.event_type, "event_domain": e.event_domain,
            "size": len(ids), "span_days": round((max(pub) - min(pub)).total_seconds() / 86400, 1),
            "growth_days": len({(m.added_at or datetime.min).date() for m in ms}),
            "outlets": len({items[i][1] for i in ids}), "languages": len(langs),
            "actors": len(set().union(*(actors[i] for i in ids))), "places": len(set().union(*(places[i] for i in ids))),
            "analysis": kinds.count("analysis"), "live_blogs": kinds.count("rolling"),
            "roundups": sum(is_roundup(items[i][0].title or "") for i in ids),
            "drift_share_below_0.53_to_first_run": drift, "max_hop": max(hops) if hops else 0,
            "unreached_by_chain": sum(1 for h in hop.values() if h is None),
            "near_threshold_share": round(near / with_link, 3) if with_link else None,
        })

    def flags(r):
        f = []
        if r["size"] >= 30:
            f.append("large")
        if r["growth_days"] >= 4 or r["span_days"] >= 4:
            f.append("long")
        if (r["drift_share_below_0.53_to_first_run"] or 0) >= 0.5 and r["size"] >= 10:
            f.append("drift")
        if r["max_hop"] >= 4:
            f.append("chain")
        if r["actors"] >= 40:
            f.append("actor_diverse")
        return f

    for r in rows:
        f = flags(r)
        r["signatures"] = ";".join(f)
        r["d398_like"] = all(x in f for x in ("long", "drift", "chain"))
        r["inspect"] = len(f) >= 2 and not r["d398_like"]
        r["likely_coherent_large"] = r["size"] >= 30 and not r["d398_like"] and (r["drift_share_below_0.53_to_first_run"] or 0) < 0.3
    rows.sort(key=lambda r: -r["size"])
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    total = len(rows)
    print("developments", total)
    print("d398_like", sum(r["d398_like"] for r in rows), [r["event_id"] for r in rows if r["d398_like"]][:40])
    print("inspect", sum(r["inspect"] for r in rows))
    print("likely_coherent_large", sum(r["likely_coherent_large"] for r in rows), [r["event_id"] for r in rows if r["likely_coherent_large"]])
    for k in ("large", "long", "drift", "chain", "actor_diverse"):
        print(k, sum(k in r["signatures"].split(";") for r in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
