"""Forensic reconstruction of how one Development's members attached (read-only; no pipeline change).

    python reconstruct.py --code-wt ../osint-monitor-timing --db COPY.db --event 398 --out d398/raw.json

Membership decisions are not logged and narrative clusters are not persisted, so each attachment is
reconstructed by re-applying the production link and guard code unchanged (imported from --code-wt, which must be
at the identity code the Development formed under) to the stored embeddings, entities and membership timestamps:

- members in the order they were stored (event_items.added_at), with the run that stored them;
- for each member, the links it has, under ``development_segmentation.compatible_link``, to the members stored
  in earlier runs (the partners the continuation rule could have used), with cosine, headline cosine, time
  delta, shared places, shared actors, shared anchors, the guard verdict and whether an override rule fired;
- members stored by the dedup path (similarity_score < 1) are marked; their duplicate partner is not stored.

What cannot be reconstructed (the HDBSCAN cluster each decision saw, the exact decision boundary inside a run, any
per-item classification) is written as NOT RECOVERABLE in the output, never inferred.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

NR = "NOT RECOVERABLE FROM CURRENT PROVENANCE"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--code-wt", type=Path, required=True)
    p.add_argument("--db", type=Path, required=True, help="a working copy of a read-only snapshot")
    p.add_argument("--event", type=int, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    os.environ["OSINT_DB_URL"] = f"sqlite:///{a.db.resolve().as_posix()}"
    sys.path.insert(0, str(a.code_wt.resolve()))

    from rapidfuzz import fuzz
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.core.database import Entity, Event, EventItem, ItemEntity, PipelineRun, RawItem, get_session
    from osint_monitor.core.models import EvidenceItem
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.clustering import LINK_SIMILARITY, MAX_LINK_HOURS
    from osint_monitor.processors.development_segmentation import (
        ACTOR_TYPES, _cosine, _headline_mismatch_outweighed, compatible_link, headline_kind, incompatibility,
        occurrence_evidence, segment_items)
    from osint_monitor.processors.language import item_language
    from osint_monitor.processors.provenance import ProvenanceResolver
    from osint_monitor.processors.actor_roles import is_roundup
    from sqlalchemy.orm import joinedload

    config = load_event_grouping_config().development_segmentation
    s = get_session()
    ev = s.get(Event, a.event)
    rows = (s.query(EventItem).filter(EventItem.event_id == a.event).all())
    runs = {r.id: r for r in s.query(PipelineRun).filter(PipelineRun.id.in_({r.added_run_id for r in rows}))}
    order = sorted(rows, key=lambda r: (r.added_at, r.item_id))
    ids = [r.item_id for r in order]
    items = {i.id: i for i in s.query(RawItem).options(joinedload(RawItem.source)).filter(RawItem.id.in_(ids))}
    seg = segment_items(s, ids, config)

    normalizer = ActorNormalizer.load()
    actors: dict[int, set[str]] = defaultdict(set)
    for item_id, name, etype in (s.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                                 .join(Entity, Entity.id == ItemEntity.entity_id).filter(ItemEntity.item_id.in_(ids))):
        if etype in ACTOR_TYPES and (k := normalizer.key(name)):
            actors[item_id].add(k)

    resolver = ProvenanceResolver()
    ev_items = [EvidenceItem(item_id=i, source_name=items[i].source.name if items[i].source else "",
                             source_category=items[i].source.category if items[i].source else None,
                             collector_type=items[i].source.type if items[i].source else None,
                             title=items[i].title, text=(items[i].content or "")[:2000], url=items[i].url or "",
                             published_at=items[i].published_at or items[i].fetched_at) for i in ids]
    prov = {p.item_id: p for p in resolver.resolve(ev_items)}

    def pair(x: int, y: int) -> dict:
        A, B = seg.get(x), seg.get(y)
        if A is None or B is None:
            return {"linked": False, "why": "no embedding"}
        hours = abs((A.published_at - B.published_at).total_seconds()) / 3600 if A.published_at and B.published_at else None
        cos = _cosine(A.vector, B.vector)
        hcos = _cosine(A.headline_vector, B.headline_vector) if A.headline_vector is not None and B.headline_vector is not None else None
        same_source = A.source == B.source
        out = {"cosine": round(cos, 4), "headline_cosine": round(hcos, 4) if hcos is not None else None,
               "hours": round(hours, 1) if hours is not None else None, "same_source": same_source,
               "shared_places": sorted(A.locations & B.locations), "shared_actors": sorted(actors[x] & actors[y]),
               "shared_anchors": sorted(A.anchors & B.anchors)}
        if same_source:
            out["title_ratio"] = round(fuzz.ratio((A.title or "").lower(), (B.title or "").lower()), 1)
        guard = incompatibility(A, B, config)
        out["guard"] = guard
        out["headline_override"] = bool(hcos is not None and hcos < config.min_headline_similarity and not same_source
                                        and _headline_mismatch_outweighed(A, B, config))
        p7 = occurrence_evidence(A, B, config) if hcos is not None and hcos < config.min_headline_similarity else None
        out["p7_occurrence_match"] = p7
        out["linked"] = compatible_link(A, B, config)
        if not out["linked"]:
            out["why"] = ("over %dh" % MAX_LINK_HOURS if hours is not None and hours > MAX_LINK_HOURS
                          else "same source, headline not near-identical" if same_source
                          else f"cosine below {LINK_SIMILARITY}" if cos < LINK_SIMILARITY else f"guard {guard}")
        return out

    first_run = order[0].added_run_id
    members_out, links = [], []
    stored: list[int] = []                        # members stored in earlier runs, in order
    run_of = {r.item_id: r.added_run_id for r in order}
    for r in order:
        n = r.item_id
        it, sg, pv = items[n], seg.get(n), prov.get(n)
        run = runs.get(r.added_run_id)
        earlier = [m for m in stored if run_of[m] != r.added_run_id]
        same_run_before = [m for m in stored if run_of[m] == r.added_run_id]
        window = [m for m in earlier if sg and seg.get(m) and seg[m].published_at and sg.published_at
                  and abs((seg[m].published_at - sg.published_at).total_seconds()) <= MAX_LINK_HOURS * 3600]
        partner_links = []
        for m in earlier:
            pr = pair(n, m)
            if pr["linked"]:
                partner_links.append({"partner": m, **pr})
        path = "dedup (near-duplicate from another source)" if (r.similarity_score or 1.0) < 1.0 else \
            ("created the Development" if r.added_run_id == first_run else "continuation")
        same_run_links = []
        if path == "created the Development" or not partner_links:
            for m in same_run_before:
                pr = pair(n, m)
                if pr["linked"]:
                    same_run_links.append({"partner": m, **pr})
        best = max(partner_links, key=lambda x: x["cosine"]) if partner_links else None
        members_out.append({
            "item_id": n, "source": it.source.name if it.source else None,
            "source_type": it.source.type if it.source else None, "source_category": it.source.category if it.source else None,
            "source_role": pv.source_role.value if pv else None, "evidence_type": pv.evidence_type.value if pv else None,
            "origin": pv.origin if pv else None,
            "language_recomputed": item_language(it.source.name if it.source else None, f"{it.title or ''}. {(it.content or '')[:500]}"),
            "published_at": str(it.published_at) if it.published_at else None, "fetched_at": str(it.fetched_at),
            "title": it.title, "headline_kind": headline_kind(it.title or ""), "roundup": is_roundup(it.title or ""),
            "actors": sorted(actors[n]), "places": sorted(sg.locations) if sg else [], "anchors": sorted(sg.anchors) if sg else [],
            "cited_source": sg.cited if sg else None,
            "item_domain_or_type": NR + " (classification is stored per Development, not per item)",
            "added_at": str(r.added_at), "added_run_id": r.added_run_id,
            "run_tier": run.tier if run else None, "run_code": (run.code_sha or "")[:7] if run else None,
            "stored_similarity_score": r.similarity_score, "path": path,
            "existing_members": len(earlier), "existing_members_within_72h": len(window),
            "linked_existing_members": len(partner_links),
            "best_partner": best["partner"] if best else None,
            "best_partner_cosine": best["cosine"] if best else None,
            "same_run_links": len(same_run_links),
            "cluster_seen_by_decision": NR, "decision_boundary_within_run": NR if same_run_before else "n/a",
        })
        for pl in partner_links:
            links.append({"from": n, "to": pl["partner"], "kind": "attach (earlier run)", **pl})
        for pl in same_run_links:
            links.append({"from": n, "to": pl["partner"], "kind": "same run (decision boundary not recoverable)", **pl})
        stored.append(n)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps({
        "event": {"id": ev.id, "summary": ev.summary, "event_type": ev.event_type, "event_domain": ev.event_domain,
                  "confidence_class": ev.confidence_class, "source_count": ev.source_count,
                  "situation_id": ev.situation_id, "first_reported_at": str(ev.first_reported_at),
                  "last_updated_at": str(ev.last_updated_at)},
        "rules": {"link_similarity": LINK_SIMILARITY, "max_link_hours": MAX_LINK_HOURS,
                  "min_headline_similarity": config.min_headline_similarity,
                  "code": str(a.code_wt)},
        "members": members_out, "links": links}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(f"D{a.event}: {len(members_out)} members, {len(links)} reconstructed links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
