"""Clean stale canonical entity names (a possessive, quotes or stray punctuation kept from before names were cleaned).

    python scripts/repair_entity_names.py --db PATH                       # dry run: report only (read-only)
    python scripts/repair_entity_names.py --db PATH --apply --backup-dir DIR

An entity is renamed to ``clean_name(canonical_name)`` only when that is safe: the clean name is not empty, differs,
and no other entity already has it (or a surface variant of it) -- a collision would be a merge, which this script
never does; collisions are reported for review. The old name stays as an alias. Nothing else changes.

Resolution no longer depends on this repair ("Elon Musk" finds "Elon Musk's" as a surface variant); it only fixes
the displayed names. Never run against the live database without the owner's explicit approval.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


def plan(conn: sqlite3.Connection) -> tuple[list[dict], list[dict]]:
    from osint_monitor.processors.entity_resolver import variant_key
    from osint_monitor.processors.text_normalize import clean_name
    rows = conn.execute("SELECT id, canonical_name, entity_type, aliases FROM entities").fetchall()
    by_variant: dict[str, set[int]] = {}
    for eid, name, _, _ in rows:
        by_variant.setdefault(variant_key(name), set()).add(eid)
    safe, collisions = [], []
    for eid, name, etype, aliases in rows:
        clean = clean_name(name)
        if not clean or clean == name:
            continue
        others = (by_variant.get(variant_key(clean), set()) - {eid}) | {
            oid for oid, oname, _, _ in rows if oid != eid and oname.lower() == clean.lower()}
        entry = {"id": eid, "from": name, "to": clean, "type": etype}
        if others:
            collisions.append({**entry, "would_merge_with": sorted(others)})
        else:
            safe.append({**entry, "aliases": sorted(set(json.loads(aliases or "[]")) | {name})})
    return safe, collisions


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if a.apply and not a.backup_dir:
        ap.error("--apply needs --backup-dir")
    ro = sqlite3.connect(f"file:{a.db.as_posix()}?mode=ro", uri=True)
    safe, collisions = plan(ro)
    for s in safe:
        print(f"RENAME {s['id']}: {s['from']!r} -> {s['to']!r} ({s['type']})")
    for c in collisions:
        print(f"SKIP   {c['id']}: {c['from']!r} -> {c['to']!r} would merge with {c['would_merge_with']}")
    report = {"db": str(a.db), "at_utc": datetime.utcnow().isoformat(timespec="seconds"), "applied": False,
              "rename": safe, "collisions": collisions}
    if a.apply:
        a.backup_dir.mkdir(parents=True, exist_ok=True)
        dest = a.backup_dir / f"{a.db.stem}.pre-entity-names-{datetime.utcnow():%Y%m%d-%H%M%S}.db"
        out = sqlite3.connect(dest)
        ro.backup(out)
        out.close()
        ro.close()
        rw = sqlite3.connect(a.db)
        with rw:
            for s in safe:
                rw.execute("UPDATE entities SET canonical_name=?, aliases=? WHERE id=?",
                           (s["to"], json.dumps(s["aliases"], ensure_ascii=False), s["id"]))
        rw.close()
        report.update(applied=True, backup=str(dest))
        print(f"renamed {len(safe)}; backup {dest}")
    if a.out:
        a.out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(safe)} safe rename(s), {len(collisions)} collision(s) for review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
