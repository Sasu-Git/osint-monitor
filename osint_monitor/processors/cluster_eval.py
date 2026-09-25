"""Clustering recall diagnostics: what narrative clustering leaves out, and why.

Read-only. Re-runs narrative clustering on the items the pipeline would see and looks
at the *noise* -- items no cluster took. For each noise item it finds the nearest
neighbours by embedding and, in particular, the closest item from a *different*
source: two outlets covering the same development is exactly what clustering should
catch, so a noise item with a close cross-source neighbour is a candidate missed join.

A reproducible stratified sample of noise items can be exported as a review file,
labelled by hand, and scored:

    python main.py inspect clustering --export review.json   # sample to label
    python main.py inspect clustering --review review.json    # metrics from labels

Labels:
    singleton         legitimate one-outlet story
    missed_member     should have joined an existing cluster
    missed_new_event  should have formed a new event with another noise item
    low_value         noise content (listings, promos, live-blog furniture)

The review file also lists every cross-source *pair* scoring in the near band
(0.45 <= cosine < LINK_SIMILARITY) with its time gap and shared canonical actors.
Labelling ``same_story`` on those pairs tests a candidate secondary link rule
(close in time + shared actors) without changing clustering.

For a missed join, ``partner`` is the item id it should have joined and
``partner_source`` that item's source: a miss is multi-source only when the two
sources differ (same-outlet follow-ups are deliberately not linked today).
"""

from __future__ import annotations

import json
import random
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
from sqlalchemy.orm import Session

from osint_monitor.core.config import load_event_grouping_config
from osint_monitor.core.database import ItemEntity, RawItem
from osint_monitor.processors.actors import ActorNormalizer
from osint_monitor.processors.clustering import (
    DEFAULT_WINDOW_HOURS, LINK_SIMILARITY, MAX_LINK_HOURS, MEMBER_SIMILARITY, _ClusterMember, _linked,
    cluster_narrative, recent_items,
)
from osint_monitor.processors.embeddings import blob_to_embedding
from osint_monitor.processors.event_grouping import partition

LABELS = ("singleton", "missed_member", "missed_new_event", "low_value")
# bands of the best cross-source neighbour's cosine: where the linking threshold would bite
BANDS = [("linkable", LINK_SIMILARITY), ("near", MEMBER_SIMILARITY), ("related", 0.35), ("far", -1.0)]
PROBE_SIMILARITY = MEMBER_SIMILARITY        # below this, a cross-source neighbour is almost never the same story
RULE_HOURS, RULE_SHARED = 6.0, 2            # candidate secondary link rule under evaluation
SWEEP_HOURS, SWEEP_SHARED = (3, 6, 9, 12, 24), (1, 2, 3)


def band(similarity: float | None) -> str:
    if similarity is None:
        return "far"
    return next(name for name, low in BANDS if similarity >= low)


@dataclass
class Neighbour:
    item_id: int
    source: str
    title: str
    similarity: float
    hours_apart: float | None
    cluster: int | None
    linkable: bool                  # would the clustering link graph connect the two?

    def as_dict(self) -> dict:
        return {"item_id": self.item_id, "source": self.source, "title": self.title,
                "similarity": round(self.similarity, 3),
                "hours_apart": None if self.hours_apart is None else round(self.hours_apart, 1),
                "cluster": self.cluster, "linkable": self.linkable}


def _time(item: RawItem) -> datetime | None:
    return item.published_at or item.fetched_at


def clustering_report(session: Session, window_hours: int = DEFAULT_WINDOW_HOURS,
                      now: datetime | None = None, k: int = 3) -> dict:
    """Clusters, noise, and each noise item's nearest neighbours for the narrative items
    the pipeline would cluster at ``now``."""
    recent = recent_items(session, window_hours, now)
    narrative, structured = partition(recent, load_event_grouping_config())
    embedded = [i for i in narrative if i.embedding is not None]
    groups = cluster_narrative(embedded)
    cluster_of = {item_id: n for n, ids in enumerate(groups) for item_id in ids}

    by_id = {i.id: i for i in embedded}
    ids = [i.id for i in embedded]
    V = np.array([blob_to_embedding(by_id[i].embedding) for i in ids], dtype=float)
    V /= np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-12, None)
    sims = V @ V.T
    members = {i: _ClusterMember.of(by_id[i], V[n]) for n, i in enumerate(ids)}

    def neighbour(a: int, b: int, sim: float) -> Neighbour:
        ta, tb = _time(by_id[a]), _time(by_id[b])
        return Neighbour(b, by_id[b].source.name if by_id[b].source else "?", by_id[b].title or "", float(sim),
                         abs((ta - tb).total_seconds()) / 3600 if ta and tb else None,
                         cluster_of.get(b), _linked(members[a], members[b]))

    noise = []
    for n, item_id in enumerate(ids):
        if item_id in cluster_of:
            continue
        order = [j for j in np.argsort(-sims[n]) if j != n]
        top = [neighbour(item_id, ids[j], sims[n, j]) for j in order[:k]]
        cross = next((neighbour(item_id, ids[j], sims[n, j]) for j in order
                      if by_id[ids[j]].source_id != by_id[item_id].source_id), None)
        noise.append({
            "item_id": item_id,
            "source": by_id[item_id].source.name if by_id[item_id].source else "?",
            "title": by_id[item_id].title or "",
            "band": band(cross.similarity if cross else None),
            "best_cross_source": cross.as_dict() if cross else None,
            "neighbours": [nb.as_dict() for nb in top],
        })

    normalizer = ActorNormalizer.load()
    actors: dict[int, set[str]] = {}
    for ie in session.query(ItemEntity).filter(ItemEntity.item_id.in_(ids)):
        if ie.entity is not None and (k := normalizer.key(ie.entity.canonical_name)):
            actors.setdefault(ie.item_id, set()).add(k)
    pairs = []
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            x, y = by_id[ids[a]], by_id[ids[b]]
            if x.source_id == y.source_id or not PROBE_SIMILARITY <= sims[a, b] < LINK_SIMILARITY:
                continue
            tx, ty = _time(x), _time(y)
            pairs.append({
                "a": x.id, "b": y.id,
                "sources": [x.source.name if x.source else "?", y.source.name if y.source else "?"],
                "titles": [x.title or "", y.title or ""],
                "similarity": round(float(sims[a, b]), 3),
                "hours_apart": round(abs((tx - ty).total_seconds()) / 3600, 1) if tx and ty else None,
                "shared_actors": sorted(actors.get(x.id, set()) & actors.get(y.id, set())),
                "clusters": [cluster_of.get(x.id), cluster_of.get(y.id)],
            })
    pairs.sort(key=lambda p: -p["similarity"])

    sources_per_cluster = Counter(len({by_id[i].source_id for i in g}) for g in groups)
    return {
        "now": (now or datetime.utcnow()).isoformat(timespec="seconds"),
        "window_hours": window_hours,
        "items": {"recent": len(recent), "structured": len(structured), "narrative": len(narrative),
                  "narrative_without_embedding": len(narrative) - len(embedded),
                  "clustered": len(cluster_of), "noise": len(noise)},
        "clusters": [{"size": len(g), "sources": sorted({by_id[i].source.name for i in g if by_id[i].source}),
                      "titles": [by_id[i].title for i in g]} for g in groups],
        "cluster_sizes": dict(sorted(Counter(len(g) for g in groups).items())),
        "sources_per_cluster": dict(sorted(sources_per_cluster.items())),
        "narrative_by_source": dict(Counter(i.source.name for i in narrative if i.source).most_common()),
        "noise_by_source": dict(Counter(x["source"] for x in noise).most_common()),
        "noise_by_band": {name: sum(1 for x in noise if x["band"] == name) for name, _ in BANDS},
        "candidate_missed_joins": sorted(
            (x for x in noise if x["best_cross_source"] and x["best_cross_source"]["similarity"] >= PROBE_SIMILARITY),
            key=lambda x: -x["best_cross_source"]["similarity"]),
        "noise": noise,
        "band_pairs": pairs,
    }


def sample_noise(report: dict, n: int = 40, seed: int = 20260925) -> list[dict]:
    """Stratified sample of noise items: every candidate missed join band is over-represented
    relative to its share, so rare-but-important cases are reviewed; the rest is random."""
    rng = random.Random(seed)
    by_band = {name: [x for x in report["noise"] if x["band"] == name] for name, _ in BANDS}
    # close bands are where tuning decisions live: take all of them up to half the sample
    picked: list[dict] = []
    for name in ("linkable", "near"):
        pool = sorted(by_band[name], key=lambda x: x["item_id"])
        picked += rng.sample(pool, min(len(pool), max(0, n // 4)))
    rest = sorted((x for x in report["noise"] if x not in picked), key=lambda x: x["item_id"])
    picked += rng.sample(rest, min(len(rest), n - len(picked)))
    return sorted(picked, key=lambda x: x["item_id"])


def review_file(report: dict, sample: list[dict], db: str, seed: int) -> dict:
    return {
        "about": "Manual review of clustering noise. Set `label` to one of "
                 f"{list(LABELS)}; `cause` is free text for missed joins.",
        "db": db, "now": report["now"], "window_hours": report["window_hours"], "seed": seed,
        "population": {"noise": report["items"]["noise"], "noise_by_band": report["noise_by_band"]},
        "items": [{**x, "label": None, "partner": None, "partner_source": None, "cause": ""} for x in sample],
        "pairs": [{**p, "same_story": None} for p in report.get("band_pairs", [])],
    }


def rule_passes(pair: dict, max_hours: float = RULE_HOURS, min_shared: int = RULE_SHARED) -> bool:
    return (pair["hours_apart"] is not None and pair["hours_apart"] <= max_hours
            and len(pair["shared_actors"]) >= min_shared)


def score_pairs(pairs: list[dict]) -> dict | None:
    """How well "close in time + shared actors" separates labelled same-story pairs."""
    labelled = [p for p in pairs if isinstance(p.get("same_story"), bool)]
    if not labelled:
        return None

    def confusion(h, k):
        c = Counter((p["same_story"], rule_passes(p, h, k)) for p in labelled)
        return {"tp": c[(True, True)], "fp": c[(False, True)], "fn": c[(True, False)], "tn": c[(False, False)]}

    true = [p for p in labelled if p["same_story"]]
    false = [p for p in labelled if not p["same_story"]]
    return {
        "labelled": len(labelled), "same_story": len(true), "different": len(false),
        "rule": {"max_hours": RULE_HOURS, "min_shared": RULE_SHARED, **confusion(RULE_HOURS, RULE_SHARED)},
        "sweep": {f"<={h}h,>={k}": confusion(h, k) for h in SWEEP_HOURS for k in SWEEP_SHARED},
        "true_hours": sorted(p["hours_apart"] for p in true if p["hours_apart"] is not None),
        "true_shared": sorted(len(p["shared_actors"]) for p in true),
        # the different-story pairs that come closest to passing: the rule's margin
        "false_with_enough_actors_hours": sorted(p["hours_apart"] for p in false
                                                 if len(p["shared_actors"]) >= RULE_SHARED
                                                 and p["hours_apart"] is not None),
        "unlabelled": sum(1 for p in pairs if not isinstance(p.get("same_story"), bool)),
    }


def score_review(review: dict) -> dict:
    """Counts per label, overall and per similarity band, from a labelled review file."""
    items = review["items"]
    unlabelled = [x["item_id"] for x in items if x.get("label") not in LABELS]
    labelled = [x for x in items if x.get("label") in LABELS]
    per_band: dict[str, Counter] = {}
    for x in labelled:
        per_band.setdefault(x["band"], Counter())[x["label"]] += 1
    counts = Counter(x["label"] for x in labelled)
    missed = [x for x in labelled if x["label"] in ("missed_member", "missed_new_event")]
    multi_source = [x for x in missed if x.get("partner_source") and x["partner_source"] != x["source"]]
    same_outlet = [x for x in missed if x.get("partner_source") == x["source"]]
    partner_sim = {}
    for x in multi_source:
        nb = next((n for n in [x.get("best_cross_source"), *x.get("neighbours", [])]
                   if n and n["item_id"] == x.get("partner")), None)
        partner_sim[x["item_id"]] = nb["similarity"] if nb else None
    return {
        "sampled": len(items),
        "labelled": len(labelled),
        "unlabelled": unlabelled,
        "counts": {label: counts.get(label, 0) for label in LABELS},
        "missed_multi_source_stories": len(multi_source),
        "missed_same_outlet": len(same_outlet),
        "missed_share": round(len(missed) / len(labelled), 3) if labelled else None,
        "per_band": {b: {label: c.get(label, 0) for label in LABELS} for b, c in per_band.items()},
        # cosine to the partner when it is among the recorded neighbours
        "missed_similarities": sorted(v for v in partner_sim.values() if v is not None),
        "missed_partner_not_nearest": sorted(k for k, v in partner_sim.items() if v is None),
        "causes": Counter(x.get("cause") or "unspecified" for x in missed).most_common(),
        "pairs": score_pairs(review.get("pairs", [])),
    }


def load_review(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def format_report(report: dict, limit: int = 15) -> str:
    it = report["items"]
    lines = [
        f"Narrative clustering at {report['now']} (window {report['window_hours']}h)",
        f"  items: {it['recent']} recent, {it['structured']} structured (not clustered here), "
        f"{it['narrative']} narrative ({it['narrative_without_embedding']} without embedding)",
        f"  clustered: {it['clustered']} in {len(report['clusters'])} clusters | noise: {it['noise']}",
        f"  cluster sizes: {report['cluster_sizes']}   sources per cluster: {report['sources_per_cluster']}",
        f"  noise by best cross-source similarity: {report['noise_by_band']} "
        f"(linkable >= {LINK_SIMILARITY}, near >= {MEMBER_SIMILARITY}, related >= 0.35)",
        f"  narrative by source: {report['narrative_by_source']}",
        f"  noise by source:     {report['noise_by_source']}",
        "",
        f"Candidate missed joins (best cross-source neighbour >= {PROBE_SIMILARITY}), top {limit}:",
    ]
    for x in report["candidate_missed_joins"][:limit]:
        nb = x["best_cross_source"]
        where = f"cluster {nb['cluster']}" if nb["cluster"] is not None else "noise"
        lines.append(f"  {nb['similarity']:.3f} {'L' if nb['linkable'] else '-'} {nb['hours_apart']}h "
                     f"[{x['source']}] {x['title'][:70]!r}\n"
                     f"        ~ [{nb['source']}, {where}] {nb['title'][:70]!r}")
    lines.append(f"  (L = the link graph would connect them; MAX_LINK_HOURS={MAX_LINK_HOURS})")
    return "\n".join(lines)


def format_scores(scores: dict) -> str:
    c = scores["counts"]
    lines = [
        f"sampled noise items: {scores['sampled']} ({scores['labelled']} labelled)",
        f"  legitimate singletons:      {c['singleton']}",
        f"  low-value / noise content:  {c['low_value']}",
        f"  missed event members:       {c['missed_member']}",
        f"  missed new events:          {c['missed_new_event']}",
        f"  missed multi-source stories: {scores['missed_multi_source_stories']} "
        f"(+{scores['missed_same_outlet']} same-outlet; share of labelled missed: {scores['missed_share']})",
        f"  per band: {scores['per_band']}",
        f"  similarity of missed multi-source joins: {scores['missed_similarities']}"
        + (f" (partner not among recorded neighbours: {scores['missed_partner_not_nearest']})"
           if scores["missed_partner_not_nearest"] else ""),
        f"  causes: {scores['causes']}",
    ]
    if scores["unlabelled"]:
        lines.append(f"  unlabelled item ids: {scores['unlabelled']}")
    p = scores.get("pairs")
    if p:
        r = p["rule"]
        lines += [
            f"near-band cross-source pairs: {p['labelled']} labelled "
            f"({p['same_story']} same story, {p['different']} different; {p['unlabelled']} unlabelled)",
            f"  rule <= {r['max_hours']}h and >= {r['min_shared']} shared actors: "
            f"tp={r['tp']} fp={r['fp']} fn={r['fn']} tn={r['tn']}",
            f"  same-story pairs: hours apart {p['true_hours']}, shared actors {p['true_shared']}",
            f"  different pairs with >= {r['min_shared']} shared actors: hours apart "
            f"{p['false_with_enough_actors_hours']}",
            "  sweep (tp/fp/fn): " + ", ".join(f"{k} {v['tp']}/{v['fp']}/{v['fn']}" for k, v in p["sweep"].items()),
        ]
    return "\n".join(lines)
