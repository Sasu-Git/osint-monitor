"""Replay each development window once through the production pipeline (as benchmark.replay does)
and cache what the lexical audit needs: titles, leads, entity mentions, vectors, clusters before
and after segmentation. Temp DB only; benchmark files read-only."""
import os, pickle, sys, tempfile
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.benchmark.format import BENCHMARK_DIR, Split, load_items, load_manifest, verify_frozen
from osint_monitor.benchmark.evaluation import segmentation_config
from osint_monitor.core.database import Base, Entity, ItemEntity, RawItem
from osint_monitor.core.models import RawItemModel
from osint_monitor.processors.clustering import cluster_narrative
from osint_monitor.processors.development_segmentation import segment_groups
from osint_monitor.processors.embeddings import blob_to_embedding
from osint_monitor.processors.pipeline import process_new_items

out_path = Path(sys.argv[1])
split = Split(sys.argv[2]) if len(sys.argv) > 2 else Split.DEVELOPMENT
manifest = load_manifest(BENCHMARK_DIR)
cache = {}
for w in [w for w in manifest.windows if w.split == split]:
    verify_frozen(w, BENCHMARK_DIR)
    items = load_items(BENCHMARK_DIR / w.items_file)
    with tempfile.TemporaryDirectory(prefix="osint-lexaudit-") as tmp:
        engine = create_engine(f"sqlite:///{Path(tmp) / 'replay.db'}")
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        raw = [RawItemModel(title=i.title, content=i.excerpt, url=i.url, published_at=i.published_at,
                            source_name=i.source, source_type="rss", external_id=i.id, fetched_at=i.published_at)
               for i in items]
        process_new_items(session, raw)
        stored = {r.external_id: r for r in session.query(RawItem).filter(RawItem.external_id.isnot(None))}
        by_raw = {r.id: bid for bid, r in stored.items()}
        groups = cluster_narrative([r for r in stored.values() if r.embedding is not None])
        seg, commentary = segment_groups(session, groups, segmentation_config())
        mentions = {}
        for raw_id, name, etype in (session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                                    .join(Entity, Entity.id == ItemEntity.entity_id)):
            mentions.setdefault(by_raw[raw_id], []).append((name, etype))
        src = {i.id: i for i in items}
        cache[w.id] = {
            "items": {bid: {"source": src[bid].source, "source_id": r.source_id, "title": src[bid].title,
                            "content": r.content or "", "published_at": src[bid].published_at}
                      for bid, r in stored.items()},
            "vectors": {bid: blob_to_embedding(r.embedding) for bid, r in stored.items() if r.embedding is not None},
            "mentions": mentions,
            "clusters": [sorted(by_raw[i] for i in g) for g in groups],
            "segmented": [sorted(by_raw[i] for i in g) for g in seg],
            "deduplicated": sorted(set(src) - set(stored)),
        }
        session.close(); engine.dispose()
    print(w.id, len(items), "items;", len(cache[w.id]["clusters"]), "clusters ->", len(cache[w.id]["segmented"]), flush=True)
out_path.write_bytes(pickle.dumps(cache))
