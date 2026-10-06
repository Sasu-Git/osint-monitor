"""Retire created Situations whose actor identity is invalid under the current actor normalisation.

    python scripts/repair_situations.py --db PATH                 # dry run: report only (read-only)
    python scripts/repair_situations.py --db PATH --apply [--regroup] --backup-dir DIR

Situations are sticky: a Development's Situation is never moved, so a Situation founded on an actor set that the
normaliser now reads differently stays wrong until it is repaired. Post-soak fix 1 (2026-10-06): "Estados Unidos"
and "United States" were two actors, which founded `estados-unidos-united-states`; a bare "Bolsonaro" was merged
with "Flávio Bolsonaro".

A created (non-seed, not closed) Situation is invalid when, under the current normaliser, its primary actors:
- include a name that is no longer an actor (an ambiguous family name, a non-actor topic), or
- collapse onto fewer distinct actors (two names of one state), or
- fall below the policy's ``min_actors_to_create``.

Repair, per invalid Situation:
- status ``closed`` (never auto-joined or reopened)
- slug renamed ``<slug>--retired-<date>`` so a later regroup can found a correct one
- a note in ``short_description``
- its Developments detached (``situation_id`` = NULL), so the next grouping run can place them.

--regroup then runs the normal grouping stage (``assign_situations``). It only considers Developments updated
within the policy's creation window. Seeds and valid created Situations are never touched. --apply first writes
a backup with the SQLite online API and verifies its integrity.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def invalid_reason(actors: list[str], normalizer, min_actors: int) -> str | None:
    keys = [normalizer.key(a) for a in actors]
    dropped = [a for a, k in zip(actors, keys) if k is None]
    if dropped:
        return f"no longer actors: {dropped}"
    distinct = sorted(set(keys))
    if len(distinct) < len(actors):
        return f"actors collapse to {distinct}"
    if len(distinct) < min_actors:
        return f"fewer than {min_actors} actors: {distinct}"
    return None


def find_invalid(session, normalizer, config) -> list[dict]:
    from osint_monitor.core.database import Event, Situation
    seeds = {s.slug for s in config.situations}
    out = []
    for s in session.query(Situation).order_by(Situation.id):
        if s.slug in seeds or s.status == "closed":
            continue
        reason = invalid_reason(list(s.primary_actors or []), normalizer, config.policy.min_actors_to_create)
        if reason:
            members = [e.id for e in session.query(Event.id).filter(Event.situation_id == s.id)]
            out.append({"id": s.id, "slug": s.slug, "actors": list(s.primary_actors or []), "reason": reason,
                        "developments": members})
    return out


def retire(session, invalid: list[dict], today: str) -> None:
    from osint_monitor.core.database import Event, Situation
    for row in invalid:
        s = session.get(Situation, row["id"])
        s.status = "closed"
        s.slug = f"{row['slug']}--retired-{today}"[:200]
        s.short_description = f"Retired {today}: invalid actor identity ({row['reason']})."
        session.query(Event).filter(Event.situation_id == s.id).update({Event.situation_id: None},
                                                                      synchronize_session=False)
    session.commit()


def readonly_session(db: Path):
    """A session on a SQLite connection opened with mode=ro: the dry run cannot write."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    engine = create_engine("sqlite://", creator=lambda: sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True))
    return Session(bind=engine)


def writable_session(db: Path):
    """A session bound to exactly this file. (core.database.get_session keeps one process-global engine and
    would silently ignore the path once any other engine exists.)"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    if not db.exists():
        raise FileNotFoundError(db)
    return Session(bind=create_engine(f"sqlite:///{db.as_posix()}"))


def backup(db: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / f"{db.stem}.pre-situation-repair-{datetime.utcnow():%Y%m%d-%H%M%S}.db"
    src = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
    out = sqlite3.connect(dest)
    try:
        src.backup(out)
        out.execute("PRAGMA journal_mode=DELETE")
    finally:
        out.close()
        src.close()
    check = sqlite3.connect(f"file:{dest.as_posix()}?mode=ro", uri=True)
    try:
        assert check.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "backup integrity check failed"
    finally:
        check.close()
    return dest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--regroup", action="store_true")
    ap.add_argument("--backup-dir", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if a.apply and not a.backup_dir:
        print("--apply needs --backup-dir")
        return 2
    from osint_monitor.core.config import load_situations_config
    from osint_monitor.processors.actors import ActorNormalizer
    session = writable_session(a.db) if a.apply else readonly_session(a.db)
    config, normalizer = load_situations_config(), ActorNormalizer.load()
    invalid = find_invalid(session, normalizer, config)
    report = {"db": str(a.db), "at_utc": datetime.utcnow().isoformat(timespec="seconds"), "applied": False,
              "invalid": invalid}
    for row in invalid:
        print(f"INVALID {row['slug']}: {row['reason']}; {len(row['developments'])} Developments {row['developments']}")
    if not invalid:
        print("no invalid created Situations")
    if a.apply and invalid:
        session.close()
        report["backup"] = str(backup(a.db, a.backup_dir))
        session = writable_session(a.db)
        retire(session, invalid, datetime.utcnow().strftime("%Y%m%d"))
        report["applied"] = True
        print(f"retired {len(invalid)}; backup {report['backup']}")
        if a.regroup:
            from osint_monitor.processors.situations import assign_situations, get_grouper
            assigned = [x for x in assign_situations(session, get_grouper()) if x.slug]
            report["regroup"] = [{"event_id": x.event_id, "slug": x.slug, "created": x.created} for x in assigned]
            print(f"regrouped: {len(assigned)} assignments, created {sorted({x.slug for x in assigned if x.created})}")
    session.close()
    if a.out:
        a.out.write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
