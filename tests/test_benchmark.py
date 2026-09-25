"""Clustering benchmark tooling: format, freezing, labels, importers, pairs, metrics, rules and
the development / hold-out protocol. Tests the tooling, not benchmark outcomes."""

import hashlib
import random
from datetime import datetime, timedelta

import numpy as np
import pytest
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.benchmark import evaluation, importers
from osint_monitor.benchmark import format as bf
from osint_monitor.benchmark.format import BenchmarkError, Gold, PairLabel, Split
from osint_monitor.benchmark.metrics import combine, evaluate
from osint_monitor.benchmark.pairs import all_pairs, path_recall
from osint_monitor.benchmark.replay import ItemFeatures, ReplayResult
from osint_monitor.benchmark.rules import PROPOSED, LinkRule, apply_rule, freeze_rule, rule_effect

T0 = datetime(2026, 8, 15, 6, 0)


def item(n, source, title, hours=0.0, excerpt=""):
    published = T0 + timedelta(hours=hours)
    return bf.BenchmarkItem(id=bf.item_id(source, title, published), published_at=published, source=source,
                            title=title, excerpt=excerpt, provenance={"benchmark_source": "test", "n": n})


@pytest.fixture()
def corpus():
    return [
        item(0, "BBC World", "Xi and Trump hold summit in Washington", 0),
        item(1, "Al Jazeera", "Trump hosts Xi at White House summit", 1),
        item(2, "SCMP", "Xi-Trump summit state dinner heavy on symbolism", 3),
        item(3, "BBC World", "Earthquake strikes northern Chile", 2),
        item(4, "Al Jazeera", "Pope arrives in Paris", 4),
        item(5, "BBC World", "Pope visit draws crowds in France", 9),
    ]


def labels_for(c, **extra):
    d = {"window": "w1", "labelled_by": "tester",
         "developments": [{"id": "summit", "members": [c[0].id, c[1].id], "storyline": "us-china"},
                          {"id": "dinner", "members": [c[2].id], "storyline": "us-china"},
                          {"id": "pope", "members": [c[4].id, c[5].id]}]}
    d.update(extra)
    return d


def make_window(root, corpus, labels, split=Split.DEVELOPMENT, window_id="w1", freeze=True):
    entry = importers.add_window(bf.load_manifest(root), window_id, split, T0, T0 + timedelta(days=1),
                                 bf.WindowSource(kind="test", reference="unit"), corpus, root=root)
    (root / entry.labels_file).write_text(yaml.safe_dump({**labels, "window": window_id}), encoding="utf-8")
    if freeze:
        bf.freeze_window(window_id, root=root)
    return entry


def fake_replay(corpus, clusters, vectors=None, actors=None):
    rng = np.random.default_rng(0)
    feats = {}
    for n, i in enumerate(corpus):
        v = vectors[n] if vectors is not None else rng.normal(size=8)
        feats[i.id] = ItemFeatures(id=i.id, source=i.source, title=i.title, published_at=i.published_at,
                                   vector=np.asarray(v, dtype=float), actors=set((actors or {}).get(n, set())))
    return lambda items: ReplayResult(features=feats, clusters=[[corpus[k].id for k in c] for c in clusters],
                                      deduplicated=[])


# --- format ----------------------------------------------------------------------------------

def test_export_is_deterministic_and_ids_are_stable(tmp_path, corpus):
    a, b = tmp_path / "a.jsonl", tmp_path / "b.jsonl"
    shuffled = corpus[:]
    random.Random(1).shuffle(shuffled)
    bf.write_items(a, corpus)
    bf.write_items(b, shuffled)
    assert a.read_bytes() == b.read_bytes()
    assert bf.item_id("BBC World", "Xi  and Trump hold SUMMIT", T0) == bf.item_id("bbc world", "Xi and Trump hold summit", T0)
    assert [i.id for i in bf.load_items(a)] == [i.id for i in sorted(corpus, key=lambda i: (i.published_at, i.source, i.id))]


def test_gold_labels_load_with_all_three_relations(tmp_path, corpus):
    path = tmp_path / "labels.yaml"
    extra = {"related_pairs": [[corpus[3].id, corpus[4].id, "explicit"]], "uncertain_pairs": [[corpus[0].id, corpus[5].id]]}
    path.write_text(yaml.safe_dump(labels_for(corpus, **extra)), encoding="utf-8")
    gold = Gold(bf.load_labels(path, corpus), corpus)
    assert gold.label(corpus[0].id, corpus[1].id) == PairLabel.SAME
    assert gold.label(corpus[1].id, corpus[2].id) == PairLabel.RELATED          # same storyline
    assert gold.label(corpus[4].id, corpus[3].id) == PairLabel.RELATED          # explicit, either order
    assert gold.label(corpus[0].id, corpus[5].id) == PairLabel.UNCERTAIN
    assert gold.label(corpus[0].id, corpus[3].id) == PairLabel.UNRELATED
    assert set(gold.multi_item_developments()) == {"summit", "pope"}


@pytest.mark.parametrize("mutate, message", [
    (lambda d, c: d["developments"][0]["members"].append("b-nope"), "unknown item"),
    (lambda d, c: d["developments"][1]["members"].append(c[0].id), "is in both"),
    (lambda d, c: d["developments"].append({"id": "summit", "members": [c[3].id]}), "duplicate development"),
    (lambda d, c: d.update(related_pairs=[[c[0].id]]), "related_pairs"),
    (lambda d, c: d.update(colour="blue"), "malformed labels"),
])
def test_malformed_labels_give_clear_errors(tmp_path, corpus, mutate, message):
    d = labels_for(corpus)
    mutate(d, corpus)
    path = tmp_path / "labels.yaml"
    path.write_text(yaml.safe_dump(d), encoding="utf-8")
    with pytest.raises(BenchmarkError, match=message):
        bf.load_labels(path, corpus)


def test_malformed_items_give_clear_errors(tmp_path, corpus):
    path = tmp_path / "items.jsonl"
    bf.write_items(path, corpus)
    path.write_text(path.read_text(encoding="utf-8") + "{not json\n", encoding="utf-8")
    with pytest.raises(BenchmarkError, match=r"items.jsonl:7: malformed item"):
        bf.load_items(path)


# --- freezing ---------------------------------------------------------------------------------

def test_changed_files_are_refused_until_deliberately_refrozen(tmp_path, corpus):
    entry = make_window(tmp_path, corpus, labels_for(corpus))
    frozen = bf.load_manifest(tmp_path).window("w1")
    bf.verify_frozen(frozen, tmp_path)
    labels_path = tmp_path / entry.labels_file
    labels_path.write_text(labels_path.read_text(encoding="utf-8") + "notes: changed\n", encoding="utf-8")
    with pytest.raises(BenchmarkError, match="labels file .* changed since it was frozen"):
        bf.verify_frozen(bf.load_manifest(tmp_path).window("w1"), tmp_path)
    with pytest.raises(BenchmarkError, match="--refreeze"):
        bf.freeze_window("w1", root=tmp_path)
    bf.freeze_window("w1", root=tmp_path, refreeze=True)
    bf.verify_frozen(bf.load_manifest(tmp_path).window("w1"), tmp_path)


def test_labels_cannot_be_frozen_unsigned_and_frozen_windows_are_not_overwritten(tmp_path, corpus):
    make_window(tmp_path, corpus, {**labels_for(corpus), "labelled_by": ""}, freeze=False)
    bf.freeze_window("w1", root=tmp_path, items_only=True)
    with pytest.raises(BenchmarkError, match="labelled_by"):
        bf.freeze_window("w1", root=tmp_path)
    with pytest.raises(BenchmarkError, match="is frozen"):
        importers.add_window(bf.load_manifest(tmp_path), "w1", Split.DEVELOPMENT, T0, T0 + timedelta(days=1),
                             bf.WindowSource(kind="test", reference="x"), corpus, root=tmp_path)


def test_overlapping_windows_are_recorded(tmp_path, corpus):
    make_window(tmp_path, corpus, labels_for(corpus), freeze=False)
    importers.add_window(bf.load_manifest(tmp_path), "w2", Split.HOLDOUT, T0 + timedelta(hours=12),
                         T0 + timedelta(days=2), bf.WindowSource(kind="test", reference="x"), corpus, root=tmp_path)
    m = bf.load_manifest(tmp_path)
    assert m.window("w1").overlaps == ["w2"] and m.window("w2").overlaps == ["w1"]


def test_label_sheet_shows_no_similarity_or_clusters(tmp_path, corpus):
    make_window(tmp_path, corpus, labels_for(corpus), freeze=False)
    sheet = bf.label_sheet("w1", tmp_path)
    assert all(i.id in sheet for i in corpus)
    assert "similar" not in sheet.lower() and "cluster" not in sheet.lower()


# --- importers (read-only) -----------------------------------------------------------------------

def test_database_import_is_read_only_and_keeps_provenance(tmp_path):
    from osint_monitor.core.database import Base, RawItem, Source
    db = tmp_path / "source.db"
    engine = create_engine(f"sqlite:///{db}")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    news = Source(name="BBC World", type="rss", url="u")
    quake = Source(name="USGS Seismic", type="structured_api", url="q")
    s.add_all([news, quake])
    s.flush()
    s.add_all([RawItem(source_id=news.id, title="Summit opens", content="Leaders met.", content_hash="1",
                       published_at=T0 + timedelta(hours=1), fetched_at=T0),
               RawItem(source_id=news.id, title="Too late", content="", content_hash="2",
                       published_at=T0 + timedelta(days=3), fetched_at=T0),
               RawItem(source_id=quake.id, title="Earthquake M5", content="", content_hash="3",
                       published_at=T0 + timedelta(hours=2), fetched_at=T0)])
    s.commit()
    s.close()
    engine.dispose()
    before = hashlib.sha256(db.read_bytes()).hexdigest()
    items = importers.from_database(db, T0, T0 + timedelta(days=1))
    assert hashlib.sha256(db.read_bytes()).hexdigest() == before
    assert [i.title for i in items] == ["Summit opens"]                 # structured feeds excluded
    assert items[0].provenance["benchmark_source"] == "local_db" and items[0].provenance["raw_item_id"]


RSS = """<?xml version="1.0"?><rss version="2.0"><channel><title>t</title>
<item><title>Summit opens in Washington</title><link>https://x/1</link>
<description>&lt;p&gt;Leaders met on Thursday.&lt;/p&gt;</description><pubDate>Sat, 15 Aug 2026 08:00:00 GMT</pubDate></item>
<item><title>Old story</title><link>https://x/2</link><pubDate>Mon, 10 Aug 2026 08:00:00 GMT</pubDate></item>
</channel></rss>"""


def test_wayback_import_uses_the_live_parser_and_records_the_snapshot():
    calls = []

    def fetch(url, params):
        calls.append(url)
        if "cdx" in url:
            return "20260815120000\n20260816030000\n"
        return RSS
    items, report = importers.from_wayback([("BBC World", "https://feeds.example/rss.xml")],
                                           T0, T0 + timedelta(days=1), fetch=fetch)
    assert [i.title for i in items] == ["Summit opens in Washington"]
    assert items[0].excerpt == "Leaders met on Thursday."              # HTML stripped as live
    p = items[0].provenance
    assert p["benchmark_source"] == "wayback" and p["original_feed"] == "BBC World"
    assert p["snapshot_timestamp"] == "20260815120000" and "id_/https://feeds.example/rss.xml" in p["archive_url"]
    assert report["BBC World"] == {"snapshots": 2, "items": 1}           # seen twice, kept once


# --- pairs, metrics and rules --------------------------------------------------------------------

def test_candidate_pairs_carry_signals_decision_and_gold(tmp_path, corpus):
    gold = Gold(bf.WindowLabels(**labels_for(corpus)), corpus)
    vectors = np.eye(6) + 0.0
    vectors[1] = vectors[0] * 0.8 + vectors[1] * 0.6                      # summit reports close
    replay = fake_replay(corpus, [[0, 1]], vectors, actors={0: {"china", "united states"},
                                                           1: {"china", "united states"}, 2: {"china"}})
    pairs = {(p.a, p.b): p for p in all_pairs(replay(corpus), gold, top_k=1)}
    key = tuple(sorted([corpus[0].id, corpus[1].id]))
    summit = pairs[key]
    assert summit.gold == PairLabel.SAME and summit.clusterer == "same_cluster"
    assert summit.shared_actors == ["china", "united states"] and summit.actor_coverage == 1.0
    assert {"semantic", "actors", "time"} <= set(summit.paths)
    pope = pairs[tuple(sorted([corpus[4].id, corpus[5].id]))]
    assert pope.gold == PairLabel.SAME and pope.clusterer == "both_noise" and "time" in pope.paths
    recall = path_recall(list(pairs.values()))
    assert recall["actors"]["same_found"] == 1 and recall["actors"]["same_total"] == 2


def test_metrics_count_recovered_partial_missed_mixed_and_noise(corpus):
    gold = Gold(bf.WindowLabels(**labels_for(corpus)), corpus)
    present = {i.id for i in corpus}
    ids = [i.id for i in corpus]
    m = evaluate([[ids[0], ids[1], ids[3]]], gold, present)                 # summit + unrelated quake
    d = m["developments"]
    assert d["multi_source"] == {"developments": 2, "recovered": 1, "partial": 0, "missed": 1}
    assert m["precision"]["mixed_clusters"] == 1
    assert m["noise"] == {"singletons": 2, "singletons_left_unclustered": 1, "singletons_clustered": 1,
                          "members": 4, "members_left_as_noise": 2}
    assert m["pairs"]["same_linked"] == 1 and m["pairs"]["unrelated_linked"] == 2
    both = combine([m, m])
    assert both["developments"]["multi_source"]["developments"] == 4 and "rows" not in both["developments"]


def test_a_rule_links_only_pairs_inside_its_band_time_and_actor_limits(corpus):
    gold = Gold(bf.WindowLabels(**labels_for(corpus)), corpus)
    base = np.zeros((6, 8))
    base[:, 0] = 1.0
    vectors = base.copy()
    vectors[5, 1] = 1.05          # pope reports point in different directions: similarity is
    vectors[4, 2] = 1.9           # irrelevant here, the rules below accept any similarity
    actors = {4: {"vatican", "france"}, 5: {"vatican", "france"}}
    replay = fake_replay(corpus, [], vectors, actors)(corpus)
    pairs = all_pairs(replay, gold)
    pope = next(p for p in pairs if {p.a, p.b} == {corpus[4].id, corpus[5].id})
    rule = LinkRule("wide", min_similarity=-1.0, max_similarity=1.0, max_hours=6.0, min_shared=2)
    assert pope.hours_apart == 5.0 and rule.passes(pope)
    assert not LinkRule("tight", min_similarity=-1.0, max_similarity=1.0, max_hours=4.0).passes(pope)
    assert not LinkRule("actors", min_similarity=-1.0, max_similarity=1.0, min_shared=3).passes(pope)
    clusters = apply_rule([], [pope], rule)
    assert clusters == [sorted([corpus[4].id, corpus[5].id])]
    assert rule_effect([pope], rule)["added_same"] == 1


# --- development / hold-out protocol ---------------------------------------------------------------

def test_development_runs_the_sweep_and_holdout_needs_a_frozen_rule(tmp_path, corpus):
    make_window(tmp_path, corpus, labels_for(corpus), Split.DEVELOPMENT, "dev")
    make_window(tmp_path, corpus, labels_for(corpus), Split.HOLDOUT, "held")
    replay = fake_replay(corpus, [[0, 1]])
    dev = evaluation.evaluate_split(Split.DEVELOPMENT, root=tmp_path, replay=replay)
    assert dev["windows"] == ["dev"] and PROPOSED.name in dev["rules"] and len(dev["rules"]) > 1
    assert "actor_first" in dev and "BENCHMARK RESULTS" in evaluation.format_report(dev)
    with pytest.raises(BenchmarkError, match="no frozen rule"):
        evaluation.evaluate_split(Split.HOLDOUT, root=tmp_path, replay=replay)
    freeze_rule(PROPOSED, "chosen on development windows", root=tmp_path)
    with pytest.raises(BenchmarkError, match="already frozen"):
        freeze_rule(PROPOSED, "again", root=tmp_path)
    held = evaluation.evaluate_split(Split.HOLDOUT, root=tmp_path, replay=replay)
    assert held["windows"] == ["held"] and list(held["rules"]) == [PROPOSED.name] and "actor_first" not in held
    runs = evaluation.previous_holdout_runs(tmp_path)
    assert len(runs) == 1 and runs[0]["rule"] == PROPOSED.name and "held" in runs[0]["windows"]


def test_unfrozen_windows_are_not_evaluated(tmp_path, corpus):
    make_window(tmp_path, corpus, labels_for(corpus), freeze=False)
    with pytest.raises(BenchmarkError, match="not frozen"):
        evaluation.evaluate_split(Split.DEVELOPMENT, root=tmp_path, replay=fake_replay(corpus, []))


# --- real replay (needs cached models) ---------------------------------------------------------------

def test_real_replay_is_read_only_and_uses_the_production_clusterer(tmp_path):
    import os
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    try:
        from osint_monitor.processors.embeddings import embed_item
        from osint_monitor.processors.nlp import get_nlp
        embed_item("probe", "")
        get_nlp()
    except Exception as e:
        pytest.skip(f"needs cached spaCy and embedding models: {e}")
    from osint_monitor.benchmark.replay import replay_window
    corpus = [
        item(0, "Reuters", "Trump and Xi agree to extend trade truce at White House summit", 0,
             "US President Donald Trump and Chinese President Xi Jinping agreed to extend a tariff truce."),
        item(1, "Associated Press", "Xi and Trump extend tariff truce after White House talks", 1,
             "Chinese leader Xi Jinping and President Donald Trump agreed to extend their trade truce."),
        item(2, "BBC World", "Priest killed in knife attack at Polish abbey", 2, "A suspect was arrested."),
    ]
    path = tmp_path / "items.jsonl"
    bf.write_items(path, corpus)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = replay_window(bf.load_items(path))
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before
    assert result.clusters == [sorted([corpus[0].id, corpus[1].id])]
    assert {"china", "united states"} <= result.features[corpus[0].id].actors
