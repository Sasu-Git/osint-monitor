"""Alias pollution on the frozen entity tables: learned aliases unlike their entity (rapidfuzz < 90, not seeded,
not a substring), and how many still resolve to that entity with the current resolver (temp DB copies only)."""
import json, sys, tempfile
from pathlib import Path

from rapidfuzz import fuzz
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.config import load_entities_config
from osint_monitor.core.database import Base, Entity
from osint_monitor.core.models import EntityType, ExtractedEntity
from osint_monitor.processors.entity_resolver import EntityResolver, normalise

GOLD = Path("evaluations/entities/gold")
seeded = {(normalise(e.canonical_name), normalise(a)) for e in load_entities_config() for a in e.aliases}
report = {}
for db in ("en", "ml"):
    rows = json.loads((GOLD / f"entities-{db}.json").read_text(encoding="utf-8"))
    suspects = [(r["id"], a, r["canonical_name"], r["entity_type"]) for r in rows for a in r["aliases"]
                if not (normalise(r["canonical_name"]) == normalise(a) or (normalise(r["canonical_name"]), normalise(a)) in seeded
                        or normalise(a) in normalise(r["canonical_name"]) or normalise(r["canonical_name"]) in normalise(a))
                and fuzz.ratio(normalise(r["canonical_name"]), normalise(a)) < 90]
    with tempfile.TemporaryDirectory() as tmp:
        engine = create_engine(f"sqlite:///{Path(tmp) / 'e.db'}")
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        for r in rows:
            session.add(Entity(id=r["id"], canonical_name=r["canonical_name"], entity_type=r["entity_type"], aliases=r["aliases"]))
        session.commit()
        resolver = EntityResolver(session)
        still = []
        for eid, alias, canonical, etype in suspects:
            try:
                et = EntityType(etype)
            except ValueError:
                et = EntityType.ORG
            entity = resolver.resolve(ExtractedEntity(text=alias, entity_type=et))
            if entity.id == eid:
                still.append({"alias": alias, "entity": canonical, "method": resolver.last_method})
            session.rollback()
            resolver._alias_map = None
        session.close()
        engine.dispose()
    report[db] = {"suspect_aliases": len(suspects), "still_resolving": still}
    print(f"{db}: {len(suspects)} suspect learned aliases; {len(still)} still resolve to that entity")
    for x in still:
        print(f"    {x['alias']!r} -> {x['entity']!r} [{x['method']}]")
if len(sys.argv) > 1:
    Path(sys.argv[1]).write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
