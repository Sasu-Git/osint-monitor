"""Coverage diagnosis (observational): why items are not in any Development, on a read-only DB copy.

    python coverage_diag.py DB OUT.json   (run with the deployed code on PYTHONPATH)

Every item that is in no Development is classified by the first rule that explains it, using the production
functions (link rule, segmentation guards, independent origins, headline forms, headline-only rule):

  structured_record          not a narrative source: structured records are grouped by record identity, not here
  commentary_analysis        an analysis / explainer / live-blog headline (not report evidence)          [policy]
  single_source_holdback     it links compatibly to other items, but all from one origin                  [policy]
  never_viable_cluster       no other item within 48 h comes near it (best cross-source cosine < 0.45)   [policy: no
                             second report observed]
  segmentation_rejected      it links to other items, but a segmentation guard cuts every link          [review]
  below_link_threshold       best cross-source cosine within 48 h in [0.45, 0.53): a near miss            [review]
  cross_language_candidate   no same-language link, but a report in another language within 24 h scores [review]
                             >= 0.60 with the multilingual model (an English-only model cannot link it)
  other_ambiguous            it links compatibly to another origin and still formed no Development        [review]

Policy = intentional exclusion under the current contract. Review = potentially recoverable recall loss; each
needs a sample judgement before it can be called a loss (thresholds and guards also reject true negatives).
"""
import json
import sys
from collections import Counter, defaultdict
from datetime import timedelta

import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker

sys.stdout.reconfigure(encoding="utf-8")
LINK, NEAR, ML_FLOOR = 0.53, 0.45, 0.60
WINDOW = timedelta(hours=48)


def main(db: str, out: str) -> int:
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.core.database import EventItem, RawItem
    from osint_monitor.processors import lexical
    from osint_monitor.processors.development_identity import independent_origins
    from osint_monitor.processors.development_segmentation import (ANALYSIS, REPORT, ROLLING, headline_kind,
                                                                   incompatibility, segment_items)
    from osint_monitor.processors.embeddings import blob_to_embedding
    import re
    meta = re.compile(r"^\s*Domain:\s*\S+\s*\|\s*Language:[^|]*\|\s*Source country:[^|]*$", re.I)

    def headline_only(content):            # slice label only: the deployed code has no headline-only rule
        return bool(meta.match(content or ""))
    from osint_monitor.processors.event_grouping import NARRATIVE, partition
    from osint_monitor.processors.language import item_language

    s = sessionmaker(bind=create_engine(f"sqlite:///file:{db}?mode=ro&uri=true", connect_args={"uri": True}))()
    cfg = load_event_grouping_config()
    items = s.query(RawItem).options(joinedload(RawItem.source)).order_by(RawItem.id).all()
    member = {i for (i,) in s.query(EventItem.item_id)}
    narrative, structured = partition(items, cfg)
    narr = [r for r in narrative if r.embedding is not None]
    t = {r.id: (r.published_at or r.fetched_at) for r in items}
    lang = {r.id: item_language(r.source.name if r.source else None, r.title or "") for r in items}
    src = {r.id: r.source_id for r in items}
    print(f"{len(items)} items: {len(member)} in a Development; {len(narrative)} narrative, {len(structured)} structured",
          flush=True)

    ids = [r.id for r in narr]
    X = np.array([blob_to_embedding(r.embedding) for r in narr], dtype=np.float32)
    X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    times = np.array([t[i].timestamp() for i in ids])
    pos = {i: k for k, i in enumerate(ids)}
    by_id = {r.id: r for r in narr}

    # first pass: linked partners (production link rule) and best cross-source cosine, within 48 h
    unsurfaced = [i for i in ids if i not in member]
    linked, best = {}, {}
    for i in unsurfaced:
        k = pos[i]
        near = np.where(np.abs(times - times[k]) <= WINDOW.total_seconds())[0]
        near = near[near != k]
        cos = X[near] @ X[k]
        other = np.array([src[ids[j]] != src[i] for j in near])
        best[i] = float(cos[other].max()) if other.any() else 0.0
        links = [ids[j] for j, c, o in zip(near, cos, other) if o and c >= LINK]
        links += [ids[j] for j, c, o in zip(near, cos, other) if not o and c >= 0.5
                  and lexical.same_source_update(by_id[i].title or "", by_id[ids[j]].title or "")]
        linked[i] = links
    need_seg = {i for i in unsurfaced if linked[i]} | {j for i in unsurfaced for j in linked[i]}
    print(f"{len(unsurfaced)} narrative items unsurfaced; {len({i for i in unsurfaced if linked[i]})} have a link; "
          f"segmentation features for {len(need_seg)} items", flush=True)
    seg = segment_items(s, need_seg, cfg.development_segmentation)

    # multilingual candidates for items without any same-language link (lazy: only those)
    from sentence_transformers import SentenceTransformer
    ml_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    texts = [((r.title or "") if headline_only(r.content) else f"{r.title or ''}. {(r.content or '')[:300]}") for r in narr]
    M = np.asarray(ml_model.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=False))

    rows = []
    for i in unsurfaced:
        r = by_id[i]
        kind = headline_kind(r.title or "")
        reason, detail = None, None
        if kind in (ANALYSIS, ROLLING):
            reason = "commentary_analysis"
        elif linked[i]:
            compat = [j for j in linked[i] if i in seg and j in seg and incompatibility(seg[i], seg[j],
                                                                                       cfg.development_segmentation) is None]
            if compat:
                origins = independent_origins(s, [i] + compat)
                reason = "single_source_holdback" if origins < 2 else "other_ambiguous"
                detail = f"{len(compat)} compatible partner(s), {origins} independent origin(s)"
            else:
                guards = Counter(incompatibility(seg[i], seg[j], cfg.development_segmentation) or "no features"
                                 for j in linked[i] if i in seg and j in seg)
                reason, detail = "segmentation_rejected", dict(guards)
        else:
            k = pos[i]
            near = np.where(np.abs(times - times[k]) <= 24 * 3600)[0]
            cross = [j for j in near if lang[ids[j]] != lang[i]]
            ml = float((M[cross] @ M[k]).max()) if cross else 0.0
            if ml >= ML_FLOOR:
                reason, detail = "cross_language_candidate", round(ml, 3)
            elif best[i] >= NEAR:
                reason, detail = "below_link_threshold", round(best[i], 3)
            else:
                reason, detail = "never_viable_cluster", round(best[i], 3)
        rows.append({"id": i, "reason": reason, "detail": detail, "source": r.source.name if r.source else None,
                     "lang": lang[i], "kind": "headline_only" if headline_only(r.content) else kind,
                     "day": t[i].date().isoformat() if t[i] else None, "title": (r.title or "")[:140]})
    for r in structured:
        if r.id not in member:
            rows.append({"id": r.id, "reason": "structured_record", "detail": None,
                         "source": r.source.name if r.source else None, "lang": lang[r.id], "kind": "structured",
                         "day": t[r.id].date().isoformat() if t[r.id] else None, "title": (r.title or "")[:140]})
    surfaced = Counter("narrative" if by_id.get(i) else "structured" for i in member)
    json.dump({"db": db, "items": len(items), "in_development": len(member), "surfaced_by_type": dict(surfaced),
               "narrative": len(narrative), "structured": len(structured), "rows": rows},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(Counter(r["reason"] for r in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
