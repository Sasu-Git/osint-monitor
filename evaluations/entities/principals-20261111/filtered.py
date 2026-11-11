"""Sub-classify the ``actor_filtered`` misses of diagnose.py (same snapshot copy, same code).

For each Development with an ``actor_filtered`` key, recompute ``development_roles`` and report, for that key:
the holders that stand for it with their "actor" weights, the key-level sum, the threshold, and whether the
headline gate (a holder acting in a headline) passes at holder or key level.

    python filtered.py SNAPSHOT_DB DIAG.json OUT.json

  split_support   no single holder reaches the threshold, but the holders of the key together do
  below_support   the holders of the key together stay under the threshold
  headline_gate   support reached, but no holder of the key acts in a headline
"""
import json
import os
import sqlite3
import sys
import tempfile
from collections import Counter
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")


def main(snapshot: str, diag: str, out: str) -> int:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.database import EventItem, RawItem
    from osint_monitor.processors.actor_roles import development_roles
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.language import item_language
    from osint_monitor.processors.principals import _lead, required_support

    d = json.loads(Path(diag).read_text(encoding="utf-8"))["developments"]
    todo = {e: [k for k, m in v["missing"].items() if m["cause"] == "actor_filtered"] for e, v in d.items()}
    todo = {e: ks for e, ks in todo.items() if ks}
    tmp = Path(tempfile.mkdtemp(prefix="prinfilt-")) / "copy.db"
    src = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    norm = ActorNormalizer.load()
    res, counts = {}, Counter()
    for e, keys in todo.items():
        rows = s.query(RawItem).join(EventItem, EventItem.item_id == RawItem.id).filter(EventItem.event_id == int(e)).all()
        items = [{"title": r.title or "", "lead": _lead(r.content),
                  "lang": item_language(r.source.name if r.source else None, r.title or ""),
                  "source": r.source.name if r.source else None} for r in rows]
        dev = development_roles(items, norm)
        need = required_support(len(dev.items))
        for k in keys:
            holders = {h: w.get("actor", 0.0) for h, w in dev.weights.items() if (norm.key(h) or h) == k}
            total = sum(holders.values())
            in_headline = bool(set(holders) & dev.headline_actors)
            if not in_headline:
                cls = "headline_gate" if total >= need else "below_support"
            elif max(holders.values(), default=0.0) >= need:
                cls = "other"
            elif total >= need:
                cls = "split_support"
            else:
                cls = "below_support"
            counts[cls] += 1
            res.setdefault(e, {})[k] = {"class": cls, "holders": holders, "total": round(total, 2), "need": need,
                                        "in_headline": in_headline, "title": d[e]["titles"][0][:120]}
    Path(out).write_text(json.dumps({"counts": dict(counts), "developments": res}, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8", newline="\n")
    print(dict(counts))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(*sys.argv[1:4]))
