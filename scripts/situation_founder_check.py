"""Read-only detector (owner rule, 2026-11-23): flag a created Situation when its founding Developments, re-derived
with the current principal-actor logic, no longer support ANY of the Situation actors that caused its creation.

    python scripts/situation_founder_check.py --db SNAPSHOT.db --out OUT.json

Never retires anything: candidates are for owner review. Works on a backup-API copy of --db in a temporary
directory (principals are re-derived there with ``mark_principal_actors``); --db itself is opened read-only.

Founders: the Situation's members first reported at or before its ``created_at`` (the Developments present when it
was created). When none qualifies, the two earliest members, flagged ``founders_fallback``. Actor keys on both sides
are Situation keys (``ActorCanonicalizer.keys``), the same function Situation grouping uses.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_situations_config
    from osint_monitor.core.database import Event, EventEntity, Situation
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.principals import mark_principal_actors
    from osint_monitor.processors.situations.canonical import ActorCanonicalizer

    tmp = Path(tempfile.mkdtemp(prefix="founder-check-")) / "copy.db"
    src = sqlite3.connect(f"file:{a.db.as_posix()}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    norm = ActorNormalizer.load()
    canon = ActorCanonicalizer(normalizer=norm)
    seeds = {x.slug for x in load_situations_config().situations}

    sits = [x for x in s.query(Situation).order_by(Situation.id) if x.slug not in seeds and x.status != "closed"]
    founders: dict[int, tuple[list[int], bool]] = {}
    for x in sits:
        members = s.query(Event).filter(Event.situation_id == x.id).order_by(Event.first_reported_at, Event.id).all()
        f = [e.id for e in members if e.first_reported_at and x.created_at and e.first_reported_at <= x.created_at]
        founders[x.id] = (f, False) if f else ([e.id for e in members[:2]], True)

    ids = sorted({e for f, _ in founders.values() for e in f})
    now = datetime.utcnow()
    s.query(Event).filter(Event.id.in_(ids)).update({Event.last_updated_at: now}, synchronize_session=False)
    s.commit()
    mark_principal_actors(s, now=now + timedelta(seconds=1), window_days=1, normalizer=norm)

    rows, candidates = [], []
    for x in sits:
        keys = canon.keys(x.primary_actors or [])
        fids, fallback = founders[x.id]
        per = []
        for eid in fids:
            names = sorted(ee.entity.canonical_name for ee in s.query(EventEntity).filter_by(event_id=eid, is_principal=True)
                           if ee.entity)
            fk = canon.keys(names)
            per.append({"development_id": eid, "principals": names, "keys": sorted(fk),
                        "supports": sorted(fk & keys)})
        supported = sorted({k for p in per for k in p["supports"]})
        row = {"id": x.id, "slug": x.slug, "status": x.status, "actors": list(x.primary_actors or []),
               "actor_keys": sorted(keys), "founders": per, "founders_fallback": fallback,
               "actor_keys_still_supported": supported, "flag": not supported}
        rows.append(row)
        if row["flag"]:
            candidates.append(row)
            print(f"CANDIDATE {x.slug} ({x.id}): no founder supports any of {sorted(keys)}; founders {fids}")
    print(f"{len(sits)} open created Situations checked; {len(candidates)} candidate(s) for owner review")
    a.out.write_text(json.dumps({"db": str(a.db), "at_utc": now.isoformat(timespec="seconds"), "retires": False,
                                 "candidates": [c["slug"] for c in candidates], "situations": rows},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
