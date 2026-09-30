"""Lexical audit of the frozen development windows (cached replay). Read-only analysis."""
import json, os, pickle, sys
from collections import Counter
from itertools import combinations
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np

from osint_monitor.benchmark.format import BENCHMARK_DIR, Gold, PairLabel, load_items, load_labels, load_manifest
from osint_monitor.processors import lexical as L
from osint_monitor.processors.clustering import LINK_SIMILARITY
from osint_monitor.processors.nlp import get_nlp
from osint_monitor.processors.principals import item_participants

cache = pickle.loads(Path(sys.argv[1]).read_bytes())
out = Path(sys.argv[2])
nlp = get_nlp()
ex = L.TermExtractor()
manifest = {w.id: w for w in load_manifest(BENCHMARK_DIR).windows}


def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def window_terms(c):
    raw = {i: ex.raw_terms(d["title"], L.lead_of(d["content"]), c["mentions"].get(i, [])) for i, d in c["items"].items()}
    df, n = L.document_frequencies([[t.text for t in ts] for ts in raw.values()])
    terms = {}
    for i, d in c["items"].items():
        parts = item_participants(nlp, d["title"], L.lead_of(d["content"]), ex.normalizer)
        terms[i] = ex.extract(i, d["title"], L.lead_of(d["content"]), c["mentions"].get(i, []), df, n, parts)
    return terms


report = {"windows": {}, "false_merges": [], "true_links": [], "missed": []}
agg = Counter()
generic_in_false, generic_in_true, specific_in_false = Counter(), Counter(), Counter()
for wid, c in cache.items():
    w = manifest[wid]
    items = load_items(BENCHMARK_DIR / w.items_file)
    gold = Gold(load_labels(BENCHMARK_DIR / w.labels_file, items), items)
    terms = window_terms(c)
    seg_of = {i: n for n, g in enumerate(c["segmented"]) for i in g}
    pre_of = {i: n for n, g in enumerate(c["clusters"]) for i in g}
    ids = sorted(i for i in c["items"] if i in c["vectors"])
    for a, b in combinations(ids, 2):
        label = gold.label(a, b)
        da, db = c["items"][a], c["items"][b]
        same_src = da["source"] == db["source"]
        sim = cos(c["vectors"][a], c["vectors"][b])
        linked_final = a in seg_of and seg_of.get(a) == seg_of.get(b)
        linked_pre = a in pre_of and pre_of.get(a) == pre_of.get(b)
        if same_src:
            direct = "same-source headline" if L.same_source_update(da["title"], db["title"]) else "none"
        else:
            direct = "embedding" if sim >= LINK_SIMILARITY else "none"
        if not (linked_final or linked_pre or label == PairLabel.SAME):
            continue
        ev = L.keyword_link_evidence(terms[a], terms[b], same_source=same_src, a_title=da["title"], b_title=db["title"],
                                     similarity=sim, linked=linked_final)
        row = {"window": wid, "a": a, "b": b, "gold": label.value, "same_source": same_src,
               "sources": [da["source"], db["source"]], "titles": [da["title"], db["title"]],
               "similarity": round(sim, 3), "direct_link": direct, "linked_pre": linked_pre, "linked_final": linked_final,
               **{k: v for k, v in ev.as_dict().items() if k not in ("similarity", "same_source")}}
        if linked_final and label in (PairLabel.RELATED, PairLabel.UNRELATED):
            report["false_merges"].append(row)
            agg[f"false:{label.value}:{direct}:{ev.result}"] += 1
            generic_in_false.update(ev.shared_generic)
            specific_in_false.update(ev.event_specific)
        elif linked_final and label == PairLabel.SAME:
            report["true_links"].append(row)
            agg[f"true:{'same' if same_src else 'cross'}:{direct}:{ev.result}"] += 1
            generic_in_true.update(ev.shared_generic)
        elif label == PairLabel.SAME and not linked_final:
            report["missed"].append(row)
            agg[f"missed:{'same' if same_src else 'cross'}:{direct}:{ev.result}"] += 1
report["summary"] = dict(sorted(agg.items()))
report["generic_terms_in_false_merges"] = generic_in_false.most_common(30)
report["generic_terms_in_true_links"] = generic_in_true.most_common(30)
report["specific_terms_in_false_merges"] = specific_in_false.most_common(30)
out.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
for k, v in sorted(agg.items()):
    print(f"{v:5}  {k}")
print("generic in false merges:", generic_in_false.most_common(15))
print("generic in true links:", generic_in_true.most_common(15))
print("specific in false merges:", specific_in_false.most_common(15))
