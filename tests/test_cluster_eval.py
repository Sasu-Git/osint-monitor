"""Clustering recall diagnostics: noise items, their cross-source neighbours, the review sample
and its scoring. Measures clustering; does not change it."""

import os
from datetime import datetime, timedelta

import pytest

from osint_monitor.core.database import RawItem, Source
from osint_monitor.processors import cluster_eval

# live 2026-09-25: one contract, two outlets, cosine 0.52 -- just under the link threshold
DESTROYER = [
    ("Breaking Defense", "OCCAR awards $4.2B DDX destroyer contract to Fincantieri, Leonardo joint venture",
     "“The DDX programme is set to redefine the Italian Navy’s capability profile in the field of air and "
     "missile defence” said the two Italian manufacturers in a joint statement."),
    ("Defense News", "Italy taps state-owned firms to build two naval destroyers in $4.2 billion deal",
     "ROME — Italy has signed to buy two new naval destroyers that will mark a quantum leap in capabilities "
     "for the Italian navy, the ships’ builders have promised.In a deal brokered by European procurement "
     "office OCCAR, Italy signed a €3.7 billion ($4.2 billion) for two so-called DDX destroyers for delivery "
     "in 2033 and 2035.The deal was signed with Orizzonte Sistemi Navali (OSN), an Italian joint venture in "
     "which state shipyard Fincantieri holds 51% and state defense giant Leonardo has the remaining 49%."),
]
UNRELATED = [
    ("BBC World", "Priest killed and four injured in knife attack at Polish abbey",
     "A male suspect from Ukraine was arrested after the stabbings in the town of Jarosław, police say."),
    ("Al Jazeera", "Young men flee Tigray amid fears of forced recruitment",
     "Years after the war, unresolved tensions are again leaving young people fearful of being drawn into fighting."),
]


@pytest.fixture(scope="module")
def embed():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    from osint_monitor.processors.embeddings import embed_item, embedding_to_blob
    try:
        embed_item("probe", "")
    except Exception as e:
        pytest.skip(f"needs the cached embedding model (run `python main.py smoke` once): {e}")
    return lambda title, content: embedding_to_blob(embed_item(title, content))


def ingest(session, embed, articles):
    now = datetime.utcnow()
    ids = {}
    for n, (source, title, content) in enumerate(articles):
        src = session.query(Source).filter_by(name=source).first() or Source(name=source, type="rss", url=source)
        session.add(src)
        session.flush()
        item = RawItem(source_id=src.id, title=title, content=content, content_hash=f"h{n}",
                       published_at=now - timedelta(minutes=30 * n), fetched_at=now, embedding=embed(title, content))
        session.add(item)
        session.flush()
        ids[title] = item.id
    session.commit()
    return ids


def test_same_story_under_the_link_threshold_is_reported_as_a_candidate_missed_join(session, embed):
    ids = ingest(session, embed, DESTROYER + UNRELATED)
    report = cluster_eval.clustering_report(session)
    assert report["items"]["noise"] == 4 and report["clusters"] == []
    candidates = {x["item_id"]: x["best_cross_source"]["item_id"] for x in report["candidate_missed_joins"]}
    occar, italy = ids[DESTROYER[0][1]], ids[DESTROYER[1][1]]
    assert candidates.get(occar) == italy and candidates.get(italy) == occar
    assert not {ids[t] for _, t, _ in UNRELATED} & set(candidates)


def test_clustered_items_are_not_noise(session, embed):
    summit = [("Reuters", "Trump and Xi agree to extend trade truce at White House summit",
               "US President Donald Trump and Chinese President Xi Jinping agreed to extend a tariff truce."),
              ("Associated Press", "Xi and Trump extend tariff truce after White House talks",
               "Chinese leader Xi Jinping and President Donald Trump agreed to extend their trade truce.")]
    ingest(session, embed, summit + UNRELATED)
    report = cluster_eval.clustering_report(session)
    assert report["cluster_sizes"] == {2: 1} and report["sources_per_cluster"] == {2: 1}
    assert {x["title"] for x in report["noise"]} == {t for _, t, _ in UNRELATED}


# --- sample and scoring (no model needed) -----------------------------------------------------

def fake_report(n_near=6, n_far=30):
    noise = [{"item_id": i, "source": "A", "title": f"t{i}", "band": "near" if i < n_near else "far",
              "best_cross_source": {"item_id": 1000 + i, "similarity": 0.5 if i < n_near else 0.2},
              "neighbours": []} for i in range(n_near + n_far)]
    return {"noise": noise, "now": "2026-09-25T08:00:00", "window_hours": 48,
            "items": {"noise": len(noise)}, "noise_by_band": {"near": n_near, "far": n_far}}


def test_review_sample_is_reproducible_and_keeps_close_calls():
    report = fake_report()
    a = cluster_eval.sample_noise(report, n=12, seed=7)
    assert a == cluster_eval.sample_noise(report, n=12, seed=7)
    assert a != cluster_eval.sample_noise(report, n=12, seed=8)
    assert len(a) == 12 and sum(1 for x in a if x["band"] == "near") >= 3


def test_scoring_separates_multi_source_misses_from_same_outlet_follow_ups():
    review = cluster_eval.review_file(fake_report(2, 3), fake_report(2, 3)["noise"], db="x", seed=1)
    items = review["items"]
    items[0].update(label="missed_new_event", partner=1000, partner_source="B")   # another outlet
    items[1].update(label="missed_new_event", partner=7, partner_source="A")      # same outlet
    items[2].update(label="singleton")
    items[3].update(label="low_value")
    scores = cluster_eval.score_review(review)
    assert scores["counts"] == {"singleton": 1, "missed_member": 0, "missed_new_event": 2, "low_value": 1}
    assert scores["missed_multi_source_stories"] == 1 and scores["missed_same_outlet"] == 1
    assert scores["missed_similarities"] == [0.5]
    assert scores["unlabelled"] == [items[4]["item_id"]]


def test_pair_scoring_reports_how_the_time_and_actor_rule_separates_labelled_pairs():
    def pair(hours, shared, same):
        return {"hours_apart": hours, "shared_actors": [f"a{i}" for i in range(shared)], "same_story": same}
    pairs = [pair(1.5, 3, True), pair(3.0, 2, True), pair(5.0, 1, False), pair(6.8, 2, False),
             pair(30, 2, False), {"hours_apart": 2, "shared_actors": ["x", "y"], "same_story": None}]
    scores = cluster_eval.score_pairs(pairs)
    assert scores["rule"] == {"max_hours": 6.0, "min_shared": 2, "tp": 2, "fp": 0, "fn": 0, "tn": 3}
    assert scores["sweep"]["<=9h,>=2"]["fp"] == 1        # a looser time cut-off admits the 6.8 h pair
    assert scores["false_with_enough_actors_hours"] == [6.8, 30]
    assert scores["unlabelled"] == 1
