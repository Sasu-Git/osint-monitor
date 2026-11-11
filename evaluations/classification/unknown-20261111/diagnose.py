"""Measure and explain the UNKNOWN event-type rate on a snapshot (read-only; works on a backup copy).

    python diagnose.py SNAPSHOT_DB OUT.json [--sample 40] [--seed 20261111]

Per Development: stored type/domain, recomputed type under the running code (confirms stored = rules output),
dominant language, sources. Unknown Developments get a cause from deterministic checks:
  non_english_headlines   no English headline or lead matched; the Development's items are es/it
  statement_without_verb  headlines are statements/announcements the STATEMENT_TITLE lexicon missed
  suppressed_legal        the legal/migration guard suppressed every candidate (honest unknown by design)
  lexicon_gap_en          English headlines, no rule matched (candidate for missing words)
  empty_or_fragment       no usable headline text
A sample of unknowns (seeded) is dumped with headlines for manual grouping.
"""
import argparse, json, os, random, sqlite3, sys, tempfile
from collections import Counter, defaultdict
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot"); ap.add_argument("out"); ap.add_argument("--sample", type=int, default=40)
    ap.add_argument("--seed", type=int, default=20261111)
    a = ap.parse_args()

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.database import Event, EventItem, RawItem, Source
    from osint_monitor.processors.classification import RuleBasedClassifier
    from osint_monitor.processors.classification.context import build_cluster_context
    from osint_monitor.processors.classification.rules import STATEMENT_TITLE, _lead
    from osint_monitor.processors.language import item_language

    tmp = Path(tempfile.mkdtemp(prefix="topic-")) / "copy.db"
    src = sqlite3.connect(f"file:{a.snapshot}?mode=ro", uri=True); dst = sqlite3.connect(tmp)
    src.backup(dst); dst.close(); src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    clf = RuleBasedClassifier()

    rows = s.query(Event).order_by(Event.id).all()
    per = {}
    for ev in rows:
        items = (s.query(RawItem.title, RawItem.content, Source.name)
                 .join(EventItem, EventItem.item_id == RawItem.id)
                 .outerjoin(Source, Source.id == RawItem.source_id)
                 .filter(EventItem.event_id == ev.id).all())
        langs = Counter(item_language(src_name, t or "") for t, _, src_name in items)
        ctx = build_cluster_context(s, ev.id)
        got = clf.classify(ctx)
        per[ev.id] = {
            "stored": ev.event_type, "stored_domain": ev.event_domain, "recomputed": got.event_type.value,
            "lang": langs.most_common(1)[0][0] if langs else "?", "langs": dict(langs),
            "sources": sorted({src_name or "?" for _, _, src_name in items}),
            "titles": [t or "" for t, _, _ in items],
            "leads": [_lead(c or "") for _, c, _ in items],
            "notes": got.classification_notes,
        }
    unknown = {e: d for e, d in per.items() if d["recomputed"] == "unknown"}

    def cause(d) -> str:
        en_titles = [t for t, l in zip(d["titles"], [item_language(None, t) for t in d["titles"]])]
        if not any((t or "").strip() for t in d["titles"]):
            return "empty_or_fragment"
        if "legal/migration headline" in (d["notes"] or ""):
            return "suppressed_legal"
        if d["lang"] in ("es", "it") and not any(item_language(None, t) == "en" for t in d["titles"]):
            return "non_english_headlines"
        if any(STATEMENT_TITLE.search(t or "") for t in d["titles"]):
            return "statement_missed"          # should not happen; sanity check
        return "lexicon_gap_en" if d["lang"] == "en" else "mixed_language_gap"

    for d in unknown.values():
        d["cause"] = cause(d)

    total = len(per)
    out = {
        "snapshot": a.snapshot, "developments": total,
        "stored_unknown": sum(1 for d in per.values() if d["stored"] == "unknown"),
        "recomputed_unknown": len(unknown),
        "stored_vs_recomputed_differ": sum(1 for d in per.values() if d["stored"] != d["recomputed"]),
        "unknown_rate": round(len(unknown) / total, 4),
        "by_language": {l: {"developments": sum(1 for d in per.values() if d["lang"] == l),
                            "unknown": sum(1 for d in unknown.values() if d["lang"] == l)}
                        for l in sorted({d["lang"] for d in per.values()})},
        "unknown_by_cause": dict(Counter(d["cause"] for d in unknown.values())),
        "unknown_by_top_source": dict(Counter(d["sources"][0] for d in unknown.values() if d["sources"]).most_common(15)),
        "types_recomputed": dict(Counter(d["recomputed"] for d in per.values())),
    }
    rng = random.Random(a.seed)
    sample_ids = sorted(rng.sample(sorted(unknown), min(a.sample, len(unknown))))
    out["sample"] = {str(e): {k: unknown[e][k] for k in ("cause", "lang", "titles", "leads", "sources")}
                     for e in sample_ids}
    out["per_development"] = {str(e): {k: d[k] for k in ("stored", "recomputed", "lang", "cause") if k in d}
                              for e, d in per.items()}
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{total} Developments; unknown stored {out['stored_unknown']} recomputed {len(unknown)} "
          f"({out['unknown_rate']:.1%}); causes {out['unknown_by_cause']}; by lang "
          f"{{ {', '.join(f'{l}: {v['unknown']}/{v['developments']}' for l, v in out['by_language'].items())} }}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
