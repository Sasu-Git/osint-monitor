"""Replay a benchmark window through the real pipeline in a throwaway database.

Items go through ``process_new_items`` (dedup, NER, entity resolution, embeddings) and
then the production narrative clusterer (``cluster_narrative``), exactly as a one-shot
``collect`` would process them. Nothing outside a temporary directory is written; the
benchmark files are only read.

This measures one-shot clustering of a window. The daemon's incremental behaviour
(later ticks extending existing events) is not replayed.
"""

from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.benchmark.format import BenchmarkItem

ACTOR_TYPES = {"PERSON", "ORG", "GPE", "NORP"}
LOCATION_TYPES = {"GPE", "LOC", "FAC"}


@dataclass
class ItemFeatures:
    id: str
    source: str
    title: str
    published_at: datetime
    vector: np.ndarray | None = None
    actors: set[str] = field(default_factory=set)          # canonical keys of every mentioned actor
    principals: set[str] = field(default_factory=set)      # canonical principal actors of the item
    organisations: set[str] = field(default_factory=set)
    locations: set[str] = field(default_factory=set)
    event_type: str | None = None
    event_domain: str | None = None


@dataclass
class ReplayResult:
    features: dict[str, ItemFeatures]                       # benchmark id -> features (surviving items)
    clusters: list[list[str]]                               # benchmark ids per production cluster
    deduplicated: list[str]                                 # benchmark ids the pipeline dropped as duplicates

    def cluster_of(self) -> dict[str, int]:
        return {i: n for n, members in enumerate(self.clusters) for i in members}


def replay_window(items: list[BenchmarkItem]) -> ReplayResult:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")           # cached models only, never the network
    from osint_monitor.core.database import Base, Entity, ItemEntity, RawItem
    from osint_monitor.core.models import ClusterContext, ContextItem, RawItemModel
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.classification import RuleBasedClassifier
    from osint_monitor.processors.clustering import cluster_narrative
    from osint_monitor.processors.embeddings import blob_to_embedding
    from osint_monitor.processors.entity_resolver import normalise
    from osint_monitor.processors.nlp import get_nlp
    from osint_monitor.processors.pipeline import process_new_items
    from osint_monitor.processors.principals import _lead, principal_keys

    with tempfile.TemporaryDirectory(prefix="osint-benchmark-") as tmp:
        engine = create_engine(f"sqlite:///{Path(tmp) / 'replay.db'}")
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        try:
            raw = [RawItemModel(title=i.title, content=i.excerpt, url=i.url, published_at=i.published_at,
                                source_name=i.source, source_type="rss", external_id=i.id,
                                fetched_at=i.published_at) for i in items]
            process_new_items(session, raw)
            stored = {r.external_id: r for r in session.query(RawItem).filter(RawItem.external_id.isnot(None))}
            by_raw_id = {r.id: bid for bid, r in stored.items()}
            groups = cluster_narrative([r for r in stored.values() if r.embedding is not None])

            normalizer, nlp, classifier = ActorNormalizer.load(), get_nlp(), RuleBasedClassifier()
            entity_rows = (session.query(ItemEntity.item_id, Entity.canonical_name, Entity.entity_type)
                           .join(Entity, Entity.id == ItemEntity.entity_id))
            mentions: dict[int, list[tuple[str, str]]] = {}
            for raw_id, name, etype in entity_rows:
                mentions.setdefault(raw_id, []).append((name, etype))

            source = {i.id: i for i in items}
            features: dict[str, ItemFeatures] = {}
            for bid, r in stored.items():
                f = ItemFeatures(id=bid, source=source[bid].source, title=source[bid].title,
                                 published_at=source[bid].published_at,
                                 vector=blob_to_embedding(r.embedding) if r.embedding is not None else None)
                for name, etype in mentions.get(r.id, []):
                    if etype in ACTOR_TYPES and (k := normalizer.key(name)):
                        f.actors.add(k)
                    if etype == "ORG" and (k := normalizer.surface(name)):
                        f.organisations.add(k)
                    if etype in LOCATION_TYPES and (k := normalise(name)):
                        f.locations.add(k)
                f.principals = principal_keys(nlp, [(r.title or "", _lead(r.content))], normalizer)
                c = classifier.classify(ClusterContext(items=[ContextItem(title=r.title or "", excerpt=r.content or "",
                                                                          source_name=f.source)]))
                f.event_type, f.event_domain = c.event_type.value, c.event_domain.value
                features[bid] = f
            clusters = sorted((sorted(by_raw_id[i] for i in g) for g in groups), key=lambda g: g[0])
            return ReplayResult(features=features, clusters=clusters,
                                deduplicated=sorted(set(source) - set(stored)))
        finally:
            session.close()
            engine.dispose()
