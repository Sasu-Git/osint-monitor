"""Gate replay for the 2026-10-16 actor defects: run once per code version (that version's worktree on PYTHONPATH),
then diff the two outputs. Never writes the snapshot: works on a backup-API copy in a temporary directory.

    python gate_replay.py SNAPSHOT_DB OUT.json

1. Defect items (D1, D2): headline + body re-extracted and resolved as the pipeline does; every mention recorded.
2. Situation regression: principals re-derived (``mark_principal_actors``) for every Development that belongs to a
   Situation, plus the D1/D2 Developments; recorded per Development as principal entity names and actor keys, with
   each Situation's primary actor keys.
"""
import json
import os
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
DEFECT_DEVS = [320, 447, 402, 429]


def main(snapshot: str, out: str) -> int:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem, Situation
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.entity_resolver import EntityResolver
    from osint_monitor.processors.language import item_language
    from osint_monitor.processors import nlp as NLP
    from osint_monitor.processors.principals import mark_principal_actors

    tmp = Path(tempfile.mkdtemp(prefix="actor-gate-")) / "copy.db"
    src = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    norm = ActorNormalizer.load()
    ner_text = getattr(NLP, "ner_text", lambda t, c: f"{t} {c}")      # the baseline code joins with a bare space

    # 1. defect items
    resolver = EntityResolver(s)
    defect_items = {}
    for (iid,) in s.query(EventItem.item_id).filter(EventItem.event_id.in_(DEFECT_DEVS)).distinct():
        r = s.get(RawItem, iid)
        lang = item_language(r.source.name if r.source else None, r.title or "")
        got = []
        for m in NLP.extract_entities(ner_text(r.title, r.content), lang):
            e = resolver.resolve(m)
            got.append({"text": m.text, "type": m.entity_type.value, "entity": e.canonical_name,
                        "entity_type": e.entity_type, "method": resolver.last_method})
        defect_items[str(iid)] = {"title": r.title, "mentions": got}
    s.rollback()

    # 2. principals for every Situation Development (and the defect Developments), all at once
    devs = sorted({e for (e,) in s.query(Event.id).filter(Event.situation_id.isnot(None))} | set(DEFECT_DEVS))
    now = datetime.utcnow()
    s.query(Event).filter(Event.id.in_(devs)).update({Event.last_updated_at: now}, synchronize_session=False)
    s.commit()
    mark_principal_actors(s, now=now + timedelta(seconds=1), window_days=1, normalizer=norm)
    per_dev = {}
    for eid in devs:
        names = sorted(ee.entity.canonical_name for ee in s.query(EventEntity).filter_by(event_id=eid, is_principal=True)
                       if ee.entity is not None)
        ev = s.get(Event, eid)
        per_dev[str(eid)] = {"situation_id": ev.situation_id, "principals": names,
                             "keys": sorted({k for k in (norm.key(n) for n in names) if k})}
    situations = {str(x.id): {"slug": x.slug, "status": x.status,
                              "keys": sorted({k for k in (norm.key(n) for n in (x.primary_actors or [])) if k})}
                  for x in s.query(Situation)}
    Path(out).write_text(json.dumps({"snapshot": snapshot, "defect_items": defect_items, "developments": per_dev,
                                     "situations": situations}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(defect_items)} defect items, {len(per_dev)} Developments, {len(situations)} Situations -> {out}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1], sys.argv[2]))
