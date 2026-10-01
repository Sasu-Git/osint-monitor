"""Replay the frozen identity windows tick by tick through the CURRENT pipeline (main behaviour), in a temporary
database, and generate the candidate relationships for the review sheet.

The system's grouping is recorded only to fill the sheet's "current Development / why grouped" columns and to
find candidates worth labelling. It is never shown to the labeller (see make_labeller_input.py).

Per window: 4 ticks of 12 h; publication times are moved into the present by one common offset (order and
spacing kept) so the 48 h clustering window holds them; fetched_at = the tick's wall-clock time.

Candidates (item pairs), each tagged with the rule that proposed it:
  late_attach     earliest member of a Development vs each member attached at a later tick
  within          earliest member vs other members attached at the same tick (up to 3 per Development)
  within_far      the least similar pair of members of a Development with 3+ members (over-merge probe)
  cross_dev       the most similar item pair of two Developments with cosine >= 0.55 or 2+ shared principals
  near_miss       an unattached narrative item vs its closest Development member, cosine >= 0.55
  seg_cut         a link segmentation cut (the pair the guard separated)
  hard_negative   same-tick pairs from different sources with cosine 0.40-0.53 (below the link threshold)
  cross_tick      items from different ticks with cosine >= 0.60, however the system grouped them (continuity)
  cross_lang      a non-English item vs the English item sharing most places + entities (same or adjacent
                  tick): the embedding model is English-only, so similarity cannot propose these

Usage: python evaluations/identity/scripts/replay_current.py [WINDOW ...] [--out DIR]
"""
import json
import os
import random
import sys
import tempfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
SEED = 20261001
CAPS = {"late_attach": 40, "within": 30, "within_far": 20, "cross_dev": 25, "near_miss": 25, "seg_cut": 25, "hard_negative": 6, "cross_tick": 20,
        "cross_lang": 15}


def load_items(window: dict) -> list[dict]:
    path = (ROOT / window["items_file"]).resolve()
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def when(item: dict) -> datetime | None:
    v = item.get("published_at") or item.get("fetched_at")
    return datetime.fromisoformat(str(v).replace("Z", "")) if v else None


def replay(window: dict) -> dict:
    import numpy as np

    from osint_monitor.core import runs
    from osint_monitor.core.database import (Entity, EventEntity, EventItem, Event, ItemEntity, RawItem, Situation,
                                             get_session, init_db, reset_engine)
    from osint_monitor.core.models import RawItemModel
    from osint_monitor.processors import clustering as CL
    from osint_monitor.processors import development_segmentation as DS
    from osint_monitor.processors.actor_roles import is_roundup
    from osint_monitor.processors.embeddings import blob_to_embedding
    from osint_monitor.processors.language import item_language
    from osint_monitor.processors.pipeline import process_new_items, run_post_processing

    tmp = Path(tempfile.mkdtemp(prefix=f"osint-identity-{window['id']}-"))
    os.environ["OSINT_DB_URL"] = f"sqlite:///{tmp / 'replay.db'}"
    reset_engine()
    init_db(os.environ["OSINT_DB_URL"], backup_dir=tmp / "backups")
    session = get_session()

    items = load_items(window)
    by_ext = {i["id"]: i for i in items}
    tick_of = {}
    for i in items:
        t = when(i)
        for tk in window["ticks"]:
            if t is not None and datetime.fromisoformat(tk["from"]) <= t < datetime.fromisoformat(tk["to"]):
                tick_of[i["id"]] = tk["tick"]
        tick_of.setdefault(i["id"], 1)                # no time at all: first tick
    shift = datetime.utcnow() - datetime.fromisoformat(window["end"])

    # record what the current system does at each tick
    trace_ticks = []
    current = {"hdbscan": [], "cuts": []}
    orig_cluster, orig_segment = CL.cluster_narrative, DS.segment

    def rec_cluster(items_, *a, **k):
        groups = orig_cluster(items_, *a, **k)
        current["hdbscan"].extend([list(g) for g in groups])
        return groups

    def rec_segment(seg_items, *a, **k):
        seg = orig_segment(seg_items, *a, **k)
        current["cuts"].extend([(x, y, guard) for x, y, guard in seg.cuts])
        return seg

    CL.cluster_narrative, DS.segment = rec_cluster, rec_segment
    run_tick = {}
    try:
        for tk in window["ticks"]:
            n = tk["tick"]
            batch = [i for i in items if tick_of[i["id"]] == n]
            run, token = runs.start_run(session, "identity-replay", tier=f"t{n}")
            run_tick[run.id] = n
            now = datetime.utcnow()
            models = []
            for i in batch:
                pub = when(i) if i.get("published_at") else None
                models.append(RawItemModel(
                    title=i["title"], content=i.get("excerpt") or "", url=i.get("url") or "",
                    published_at=(pub + shift) if pub else None, source_name=i["source"],
                    source_type=i.get("source_type") or "rss", external_id=i["id"], fetched_at=now))
            current["hdbscan"], current["cuts"] = [], []
            stats = process_new_items(session, models) if models else {"new_items": 0}
            stats.update(run_post_processing(session, quiet=True, offline=True))
            runs.finish_run(session, run, token, stats, items_collected=len(batch))
            ext_of = dict((rid, ext) for rid, ext in session.query(RawItem.id, RawItem.external_id))
            trace_ticks.append({
                "tick": n, "items_in": len(batch), "items_stored": stats.get("new_items", 0),
                "clusters_before_segmentation": [[ext_of[x] for x in g if x in ext_of] for g in current["hdbscan"]],
                "segmentation_cuts": [[ext_of.get(x), ext_of.get(y), g] for x, y, g in current["cuts"]],
            })
    finally:
        CL.cluster_narrative, DS.segment = orig_cluster, orig_segment

    # final state
    stored = {r.external_id: r for r in session.query(RawItem)}
    ext_of = {r.id: e for e, r in stored.items()}
    events = {}
    member_of = defaultdict(list)
    slugs = {s.id: s.slug for s in session.query(Situation)}
    situations = {s.slug: {"title": s.title, "status": s.status, "primary_actors": sorted(s.primary_actors or [])}
                  for s in session.query(Situation)}
    for ev in session.query(Event).order_by(Event.id):
        mems = session.query(EventItem).filter_by(event_id=ev.id).all()
        ticks = {ext_of[m.item_id]: run_tick.get(m.added_run_id) for m in mems}
        principals = sorted({e.canonical_name for e, ee in session.query(Entity, EventEntity)
                            .join(EventEntity, EventEntity.entity_id == Entity.id)
                            .filter(EventEntity.event_id == ev.id, EventEntity.is_principal.is_(True))})
        events[ev.id] = {"summary": ev.summary, "created_tick": min(t for t in ticks.values() if t) if ticks else None,
                         "members": ticks, "principals": principals,
                         "corroboration": ev.corroboration_level, "sources": sorted({stored[x].source.name for x in ticks}),
                         "situation": slugs.get(ev.situation_id)}
        for x in ticks:
            member_of[x].append(ev.id)
    places = defaultdict(set)
    actors = defaultdict(set)
    for iid, name, etype in (session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                             .join(Entity, Entity.id == ItemEntity.entity_id)):
        if iid not in ext_of:
            continue
        if etype in ("GPE", "LOC", "FAC"):
            places[ext_of[iid]].add(name)
        elif etype in ("PERSON", "ORG", "NORP"):
            actors[ext_of[iid]].add(name)
    vec = {e: blob_to_embedding(r.embedding) for e, r in stored.items() if r.embedding is not None}

    def cos(a, b):
        if a not in vec or b not in vec:
            return None
        va, vb = vec[a], vec[b]
        return float(np.dot(va, vb) / (np.linalg.norm(va) * np.linalg.norm(vb) + 1e-9))

    item_rows = {}
    for ext, i in by_ext.items():
        r = stored.get(ext)
        item_rows[ext] = {
            "id": ext, "tick": tick_of[ext], "source": i["source"], "source_type": i.get("source_type") or "rss",
            "lang": i.get("lang") or item_language(i["source"], i["title"]), "title": i["title"],
            "excerpt": (i.get("excerpt") or "")[:400], "published_at": i.get("published_at"),
            "stored": r is not None, "developments": member_of.get(ext, []),
            "places": sorted(places.get(ext, ())), "entities": sorted(actors.get(ext, ())),
            "roundup": is_roundup(i["title"]),
        }

    # candidates
    rng = random.Random(SEED)
    cands: dict[tuple, dict] = {}

    def add(a, b, rule, why):
        if a == b or a not in item_rows or b not in item_rows:
            return
        key = tuple(sorted((a, b)))
        c = cands.setdefault(key, {"a": key[0], "b": key[1], "rules": [], "why": [], "cosine": cos(*key)})
        if rule not in c["rules"]:
            c["rules"].append(rule)
            c["why"].append(why)

    per_rule = defaultdict(list)
    for eid, ev in events.items():
        mems = sorted(ev["members"], key=lambda x: (ev["members"][x] or 99, x))
        if not mems:
            continue
        anchor = mems[0]
        later = [m for m in mems[1:] if (ev["members"][m] or 0) > (ev["members"][anchor] or 0)]
        same = [m for m in mems[1:] if m not in later]
        for m in later:
            per_rule["late_attach"].append((anchor, m, f"D{eid}: attached at tick {ev['members'][m]} to a Development "
                                                        f"created at tick {ev['members'][anchor]}"))
        for m in same[:3]:
            per_rule["within"].append((anchor, m, f"D{eid}: grouped together at tick {ev['members'][anchor]}"))
        if len(mems) >= 3:
            worst = min(((cos(a, b) if cos(a, b) is not None else 1.0, a, b)
                         for n, a in enumerate(mems) for b in mems[n + 1:]), default=None)
            if worst:
                per_rule["within_far"].append((worst[1], worst[2], f"D{eid}: least similar members of a "
                                               f"{len(mems)}-item Development (cosine {worst[0]:.2f})"))
    eids = list(events)
    for x in range(len(eids)):
        for y in range(x + 1, len(eids)):
            ex, ey = events[eids[x]], events[eids[y]]
            shared = set(ex["principals"]) & set(ey["principals"])
            best = max(((cos(a, b) or 0, a, b) for a in ex["members"] for b in ey["members"] if a != b), default=None)
            if best and (best[0] >= 0.55 or len(shared) >= 2):
                per_rule["cross_dev"].append((best[1], best[2], f"separate Developments D{eids[x]} and D{eids[y]} "
                                              f"(closest items cosine {best[0]:.2f}; shared principals {sorted(shared)})"))
    members_all = {m for ev in events.values() for m in ev["members"]}
    for ext, row in item_rows.items():
        if row["developments"] or not row["stored"] or row["source_type"] != "rss":
            continue
        best = max(((cos(ext, m) or 0, m) for m in members_all), default=None)
        if best and best[0] >= 0.55:
            per_rule["near_miss"].append((ext, best[1], f"not in any Development; closest member (cosine "
                                          f"{best[0]:.2f}) is in D{member_of[best[1]][0]}"))
    for tk in trace_ticks:
        for a, b, guard in tk["segmentation_cuts"]:
            if a and b:
                per_rule["seg_cut"].append((a, b, f"tick {tk['tick']}: link cut by segmentation guard '{guard}'"))
    for tk in window["ticks"]:
        pool = [e for e, r in item_rows.items() if r["tick"] == tk["tick"] and r["stored"] and r["source_type"] == "rss"]
        pairs = [(a, b) for a in pool for b in pool if a < b and item_rows[a]["source"] != item_rows[b]["source"]
                 and cos(a, b) is not None and 0.40 <= cos(a, b) < 0.53]
        for a, b in rng.sample(pairs, min(2, len(pairs))):
            per_rule["hard_negative"].append((a, b, f"same tick, different outlets, cosine {cos(a, b):.2f}: "
                                              "below the link threshold, never grouped"))
    narrative = [e for e, r in item_rows.items() if r["stored"] and r["source_type"] == "rss"]
    for x, a in enumerate(narrative):
        for b in narrative[x + 1:]:
            if item_rows[a]["tick"] != item_rows[b]["tick"] and (cos(a, b) or 0) >= 0.60:
                rel = ("same Development" if set(item_rows[a]["developments"]) & set(item_rows[b]["developments"])
                       else "not grouped together")
                per_rule["cross_tick"].append((a, b, f"ticks {item_rows[a]['tick']} and {item_rows[b]['tick']}, "
                                               f"cosine {cos(a, b):.2f}: {rel}"))
    english = [e for e in narrative if item_rows[e]["lang"] == "en"]
    for a in narrative:
        ra = item_rows[a]
        if ra["lang"] == "en":
            continue
        best = None
        for b in english:
            rb = item_rows[b]
            if abs(rb["tick"] - ra["tick"]) > 1:
                continue
            shared_places = set(ra["places"]) & set(rb["places"])
            shared_ents = set(ra["entities"]) & set(rb["entities"])
            score = len(shared_places) + len(shared_ents)
            if shared_places and shared_ents and (best is None or score > best[0]):
                best = (score, b, shared_places | shared_ents)
        if best:
            rel = ("same Development" if set(ra["developments"]) & set(item_rows[best[1]]["developments"])
                   else "not grouped together")
            per_rule["cross_lang"].append((a, best[1], f"{ra['lang']} vs en, shared {sorted(best[2])[:4]}: {rel}"))
    for rule, rows in per_rule.items():
        rng.shuffle(rows)
        for a, b, why in rows[:CAPS[rule]]:
            add(a, b, rule, why)

    session.close()
    reset_engine()
    return {"window": window["id"], "split": window["split"], "shift_hours": round(shift.total_seconds() / 3600, 1),
            "ticks": trace_ticks, "developments": {str(k): v for k, v in events.items()}, "items": item_rows,
            "situations": situations,
            "candidates": sorted(cands.values(), key=lambda c: (c["a"], c["b"]))}


def main() -> int:
    import yaml
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else ROOT / "review" / "system-trace"
    wanted = [a for a in sys.argv[1:] if not a.startswith("--") and a != str(out)]
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    out.mkdir(parents=True, exist_ok=True)
    for w in manifest["windows"]:
        if wanted and w["id"] not in wanted:
            continue
        trace = replay(w)
        (out / f"{w['id']}.json").write_text(json.dumps(trace, indent=1, ensure_ascii=False, default=str) + "\n",
                                             encoding="utf-8", newline="\n")
        print(w["id"], len(trace["developments"]), "Developments,", len(trace["candidates"]), "candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
