"""Snapshot replay for the Situation-v2 normalisation prerequisite (gates G1, G5, G6 of DEFECTS.md).

Run once per code version, with that version's worktree first on PYTHONPATH, then diff the two outputs with
``compare.py``. Never writes the snapshot: works on a backup-API copy in a temporary directory.

    python replay_actors.py SNAPSHOT_DB OUT.json

Per Development (all of them): principals re-derived with ``mark_principal_actors`` under the running code, recorded
as entity names and types, the topic keys (``ActorNormalizer.keys``, what Development identity uses) and the
Situation keys (``ActorCanonicalizer.keys``, what Situation grouping uses). Per Situation: the keys of its stored
primary actors. Plus the probe names of the defect list, through ``surface`` / ``key``.
"""
import json
import os
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")

PROBE_NAMES = ["Milei", "Javier Milei", "Musk", "Elon Musk's", "Pike", "Christa Pike's", "Machado",
               "Maria Corina Machado", "Bukele", "Nayib Bukele", "Macron", "Emmanuel Macron", "Vance", "J.D. Vance",
               "DONALD J. TRUMP", "Trump", "Democrat", "Democrats", "Democratic", "Republican", "Republicans",
               "Democratici", "English", "Chinas Long March", "China's Long March", "Long March", "Rachel", "Simon",
               "Bolsonaro", "Flávio Bolsonaro", "Jair Bolsonaro"]
PROBE_SETS = {
    "A1": ["Javier Milei", "Milei"], "A2": ["Elon Musk's", "Musk"], "A3": ["Christa Pike's", "Pike"],
    "A4": ["Maria Corina Machado", "Machado"], "A5": ["Nayib Bukele", "Bukele", "El Salvador"],
    "A6": ["Emmanuel Macron", "Macron", "France"], "A7": ["America", "Vance", "J.D. Vance"],
    "A8": ["DONALD J. TRUMP", "Trump"], "C1": ["Democrat", "United States"], "C3": ["China", "Chinas Long March"],
    "guard-bolsonaro": ["Jair Bolsonaro", "Flávio Bolsonaro", "Bolsonaro"],
    "guard-lone-surname": ["Musk", "Germany"],
}


def main(snapshot: str, out: str) -> int:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.database import Event, EventEntity, Situation
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.principals import mark_principal_actors
    from osint_monitor.processors.situations.canonical import ActorCanonicalizer

    tmp = Path(tempfile.mkdtemp(prefix="actnorm-")) / "copy.db"
    src = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    norm = ActorNormalizer.load()
    canon = ActorCanonicalizer(normalizer=norm)

    probes = {n: {"surface": norm.surface(n), "key": norm.key(n)} for n in PROBE_NAMES}
    probe_sets = {k: {"topic_keys": sorted(norm.keys(v)), "situation_keys": sorted(canon.keys(v))}
                  for k, v in PROBE_SETS.items()}

    now = datetime.utcnow()
    s.query(Event).update({Event.last_updated_at: now}, synchronize_session=False)
    s.commit()
    stats = mark_principal_actors(s, now=now + timedelta(seconds=1), window_days=1, normalizer=norm)
    per_dev = {}
    for ev in s.query(Event).order_by(Event.id):
        links = [ee for ee in s.query(EventEntity).filter_by(event_id=ev.id, is_principal=True) if ee.entity]
        names = sorted(ee.entity.canonical_name for ee in links)
        per_dev[str(ev.id)] = {
            "situation_id": ev.situation_id,
            "principals": names,
            "principal_types": sorted(ee.entity.entity_type or "?" for ee in links),
            "topic_keys": sorted(norm.keys(names)),
            "situation_keys": sorted(canon.keys(names)),
        }
    situations = {str(x.id): {"slug": x.slug, "status": x.status,
                              "topic_keys": sorted(norm.keys(x.primary_actors or [])),
                              "situation_keys": sorted(canon.keys(x.primary_actors or []))}
                  for x in s.query(Situation)}
    Path(out).write_text(json.dumps({"snapshot": snapshot, "stats": stats, "probes": probes, "probe_sets": probe_sets,
                                     "developments": per_dev, "situations": situations},
                                    ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(per_dev)} Developments, {len(situations)} Situations, stats {stats} -> {out}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1], sys.argv[2]))
