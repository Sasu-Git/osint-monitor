"""Extract the frozen evidence for the 2026-10-16 actor-identity defects from the snapshot (read-only).

    python extract.py SNAPSHOT_DB > evidence.json

For each case: the Situation as created, its Developments with their principal actors, every item in them with the
entity mentions on the defect names (span, resolved entity, type, resolution method and evidence).
"""
import json
import sqlite3
import sys

CASES = {
    "D1-elon-musk": {"situation": "elon-musk-musk", "names": ["Musk"]},
    "D2-storm-names": {"situation": "rachel-simon", "names": ["Rachel", "Simon", "Simón"]},
}


def main(db: str) -> int:
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    out = {}
    for case, spec in CASES.items():
        sid, slug, actors, created = c.execute("SELECT id, slug, primary_actors, created_at FROM situations WHERE slug=?",
                                               (spec["situation"],)).fetchone()
        like = " OR ".join(["en.canonical_name LIKE ? OR ie.span_text LIKE ?"] * len(spec["names"]))
        args = [a for n in spec["names"] for a in (f"%{n}%", f"%{n}%")]
        devs = []
        for (eid,) in c.execute("SELECT id FROM events WHERE situation_id=? ORDER BY id", (sid,)).fetchall():
            principals = [dict(zip(("entity_id", "canonical_name", "entity_type", "actor_role"), r)) for r in c.execute(
                "SELECT en.id, en.canonical_name, en.entity_type, ee.actor_role FROM event_entities ee "
                "JOIN entities en ON en.id=ee.entity_id WHERE ee.event_id=? AND ee.is_principal ORDER BY en.id", (eid,))]
            items = []
            for iid, source, title in c.execute(
                    "SELECT i.id, s.name, i.title FROM event_items ei JOIN raw_items i ON i.id=ei.item_id "
                    "JOIN sources s ON s.id=i.source_id WHERE ei.event_id=? ORDER BY i.id", (eid,)).fetchall():
                mentions = [dict(zip(("span_text", "entity_id", "canonical_name", "entity_type", "method", "evidence"), r))
                            for r in c.execute(
                                "SELECT ie.span_text, en.id, en.canonical_name, en.entity_type, ie.resolution_method, "
                                f"ie.resolution_evidence FROM item_entities ie JOIN entities en ON en.id=ie.entity_id "
                                f"WHERE ie.item_id=? AND ({like}) ORDER BY ie.id", [iid] + args)]
                items.append({"item_id": iid, "source": source, "title": title, "defect_mentions": mentions})
            devs.append({"development_id": eid, "principals": principals, "items": items})
        entities = [dict(zip(("entity_id", "canonical_name", "entity_type", "aliases"), r)) for r in c.execute(
            "SELECT id, canonical_name, entity_type, aliases FROM entities WHERE " +
            " OR ".join(["canonical_name LIKE ?"] * len(spec["names"])) + " ORDER BY id", [f"%{n}%" for n in spec["names"]])]
        out[case] = {"situation": {"id": sid, "slug": slug, "primary_actors": json.loads(actors), "created_at": created},
                     "developments": devs, "entities_named": entities}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    sys.exit(main(sys.argv[1]))
