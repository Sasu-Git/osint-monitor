"""Baseline vs lexical-guard candidate on the frozen development windows, one replay per window,
both configurations clustering the same stored items. Temp DBs only; benchmark files read-only."""
import json, os, sys, tempfile
from itertools import combinations
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.benchmark.evaluation import segmentation_config
from osint_monitor.benchmark.format import BENCHMARK_DIR, Gold, Split, load_items, load_labels, load_manifest, verify_frozen
from osint_monitor.benchmark.metrics import combine, evaluate
from osint_monitor.core.config import load_event_grouping_config
from osint_monitor.core.database import Base, RawItem
from osint_monitor.core.models import RawItemModel
from osint_monitor.processors import lexical as L
from osint_monitor.processors.clustering import cluster_narrative
from osint_monitor.processors.development_segmentation import segment_groups
from osint_monitor.processors.pipeline import process_new_items

out = Path(sys.argv[1])
base_cfg = load_event_grouping_config().lexical
cand_cfg = base_cfg.model_copy(update={"guard": base_cfg.guard.model_copy(update={"enabled": True})})
print("candidate guard:", cand_cfg.guard.model_dump(), flush=True)
seg_cfg = segmentation_config()

report = {"candidate": cand_cfg.guard.model_dump(), "windows": {}, "changed": []}
totals = {k: [] for k in ("base_pre", "cand_pre", "base_seg", "cand_seg")}
for w in [w for w in load_manifest(BENCHMARK_DIR).windows if w.split == Split.DEVELOPMENT]:
    verify_frozen(w, BENCHMARK_DIR)
    items = load_items(BENCHMARK_DIR / w.items_file)
    gold = Gold(load_labels(BENCHMARK_DIR / w.labels_file, items), items)
    with tempfile.TemporaryDirectory(prefix="osint-lexcand-") as tmp:
        engine = create_engine(f"sqlite:///{Path(tmp) / 'replay.db'}")
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        process_new_items(session, [RawItemModel(title=i.title, content=i.excerpt, url=i.url, published_at=i.published_at,
                                                 source_name=i.source, source_type="rss", external_id=i.id,
                                                 fetched_at=i.published_at) for i in items])
        stored = {r.external_id: r for r in session.query(RawItem).filter(RawItem.external_id.isnot(None))}
        bid = {r.id: b for b, r in stored.items()}
        narrative = [r for r in stored.values() if r.embedding is not None]
        runs = {}
        for name, cfg in (("base", base_cfg), ("cand", cand_cfg)):
            L.use_settings(cfg)
            try:
                pre = cluster_narrative(narrative)
                seg, _ = segment_groups(session, pre, seg_cfg)
            finally:
                L.use_settings(None)
            runs[name] = ([sorted(bid[i] for i in g) for g in pre], [sorted(bid[i] for i in g) for g in seg])
        terms = L.batch_terms(narrative)
        present = set(stored)
        for name in ("base", "cand"):
            totals[f"{name}_pre"].append(evaluate(runs[name][0], gold, present))
            totals[f"{name}_seg"].append(evaluate(runs[name][1], gold, present))

        def pairs(groups):
            return {tuple(sorted(p)) for g in groups for p in combinations(g, 2)}
        for stage, k in (("before segmentation", 0), ("after segmentation", 1)):
            b, c = pairs(runs["base"][k]), pairs(runs["cand"][k])
            for a, bb in sorted((b ^ c)):
                ra, rb = stored[a], stored[bb]
                va, vb = np.frombuffer(ra.embedding, dtype=np.float32), np.frombuffer(rb.embedding, dtype=np.float32)
                sim = float(va @ vb / (np.linalg.norm(va) * np.linalg.norm(vb)))
                ev = L.keyword_link_evidence(terms[ra.id], terms[rb.id], same_source=ra.source_id == rb.source_id,
                                             a_title=ra.title, b_title=rb.title, similarity=sim)
                report["changed"].append({
                    "window": w.id, "stage": stage, "a": a, "b": bb, "gold": gold.label(a, bb).value,
                    "sources": [ra.source.name, rb.source.name], "titles": [ra.title, rb.title],
                    "similarity": round(sim, 3), "before": "linked" if (a, bb) in b else "not linked",
                    "after": "linked" if (a, bb) in c else "not linked",
                    "actors": ev.shared_actors, "high": ev.shared_high, "medium": ev.shared_medium,
                    "generic": ev.shared_generic, "lexical_result": ev.result, "weighted_overlap": ev.weighted_overlap})
        session.close(); engine.dispose()
    print(w.id, "done", flush=True)
for k, v in totals.items():
    report[k] = combine(v)
out.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str), encoding="utf-8")


def line(m):
    d, p, pr = m["developments"]["multi_source"], m["pairs"], m["precision"]
    return (f"multi-source recovered {d['recovered']}/{d['developments']} (partial {d['partial']}, missed {d['missed']}); "
            f"cross-source SAME linked {p['cross_source_same_linked']}/{p['cross_source_same_pairs']}; "
            f"wrong links related {p['related_linked']}, unrelated {p['unrelated_linked']}; "
            f"mixed clusters {pr['mixed_clusters']}/{pr['clusters']}")
for k in ("base_pre", "cand_pre", "base_seg", "cand_seg"):
    print(f"{k:9} {line(report[k])}")
print("changed links:", len(report["changed"]))
for ch in report["changed"]:
    print(f"  [{ch['window']}] {ch['stage']}: {ch['before']} -> {ch['after']} gold={ch['gold']} sim={ch['similarity']} "
          f"{ch['lexical_result']}\n     {ch['sources'][0]}: {ch['titles'][0]}\n     {ch['sources'][1]}: {ch['titles'][1]}")
