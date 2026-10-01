"""Read-only lineage sample. Usage: python sample.py <db-copy> <out.json>
Opens the copy with sqlite3 URI mode=ro. Seed 20261001. Calls only pure functions of osint_monitor."""
import sqlite3, sys, json, random, logging
from collections import Counter, defaultdict
logging.disable(logging.WARNING)
sys.path.insert(0, r"C:\Users\EugenioVardiero\osint-monitor")
from osint_monitor.processors.actor_roles import is_roundup
from osint_monitor.processors.development_segmentation import headline_kind
from osint_monitor.processors.language import item_language
from osint_monitor.processors.principals import development_actors, _lead
from osint_monitor.core.config import load_event_grouping_config
random.seed(20261001)
db, out = sys.argv[1], sys.argv[2]
c = sqlite3.connect(f"file:{db}?mode=ro", uri=True); c.row_factory = sqlite3.Row
q = lambda s, *a: [dict(r) for r in c.execute(s, a)]
cfg = load_event_grouping_config()
src = {r["id"]: r for r in q("select * from sources")}
st_types = set(cfg.structured.source_types) if hasattr(cfg, "structured") else set()
def structured(s):
    try:
        from osint_monitor.processors.event_grouping import partition
    except Exception: pass
    return None
items = {r["id"]: r for r in q("select id,source_id,title,content,url,published_at,fetched_at,external_id from raw_items")}
for i in items.values():
    s = src[i["source_id"]]; i["source"] = s["name"]; i["stype"] = s["type"]
    i["lang"] = item_language(s["name"], i["title"] or "")
    i["roundup"] = is_roundup(i["title"]); i["hkind"] = headline_kind(i["title"])
ev_items = defaultdict(list)
for r in q("select event_id,item_id from event_items"): ev_items[r["event_id"]].append(r["item_id"])
item_events = defaultdict(set)
for e, its in ev_items.items():
    for i in its: item_events[i].add(e)
sits = {r["id"]: r for r in q("select * from situations")}
events = {r["id"]: r for r in q("select * from events")}
ents = defaultdict(list)
for r in q("select ee.event_id,en.canonical_name,en.entity_type,ee.role,ee.is_principal from event_entities ee join entities en on en.id=ee.entity_id"):
    ents[r["event_id"]].append(r)
def trace(eid, current=True):
    e = events[eid]; its = sorted((items[i] for i in ev_items[eid]), key=lambda x: x["published_at"] or "")
    t = {"id": eid, "summary": e["summary"], "first_reported_at": e["first_reported_at"], "last_updated_at": e["last_updated_at"],
         "item_pub_min": min((x["published_at"] or x["fetched_at"]) for x in its) if its else None,
         "item_pub_max": max((x["published_at"] or x["fetched_at"]) for x in its) if its else None,
         "n_items": len(its), "n_sources": len({x["source_id"] for x in its}), "source_count": e["source_count"],
         "admiralty": e["admiralty_rating"], "corroboration": e["corroboration_level"], "confidence_class": e["confidence_class"],
         "contradictions": e["has_contradictions"], "domain": e["event_domain"], "event_type": e["event_type"],
         "mode": e["interaction_mode"], "concreteness": e["concreteness"], "significance": e["significance_class"],
         "rank_score": e["rank_score"], "rank_reasons": e["rank_reasons"], "region": e["region"], "location": e["location_name"],
         "situation": (sits[e["situation_id"]]["slug"] if e["situation_id"] else None),
         "db_principals": sorted({x["canonical_name"] for x in ents[eid] if x["is_principal"]}),
         "n_event_entities": len(ents[eid]),
         "items": [{"id": x["id"], "source": x["source"], "stype": x["stype"], "pub": x["published_at"], "lang": x["lang"],
                    "roundup": x["roundup"], "hkind": x["hkind"], "title": x["title"], "url": x["url"],
                    "other_events": sorted(item_events[x["id"]] - {eid})} for x in its]}
    if current:
        try:
            da = development_actors([{"title": x["title"] or "", "lead": _lead(x["content"]), "lang": x["lang"], "source": x["source"]} for x in its])
            t["main_principals"] = sorted(da.principals); t["main_roles"] = da.roles
        except Exception as ex:
            t["main_principals"] = f"ERR {ex!r}"
    return t
res = {"db": db}
order = sorted(events, key=lambda i: (events[i]["last_updated_at"], i), reverse=True)
res["recent20"] = order[:20]
multi = sorted(i for i in events if len({items[x]["source_id"] for x in ev_items[i]}) >= 2 and i not in order[:20])
res["multi10"] = sorted(random.sample(multi, min(10, len(multi))))
res["single_source_events"] = sorted(i for i in events if len({items[x]["source_id"] for x in ev_items[i]}) == 1)
res["all_events"] = {i: trace(i) for i in sorted(events)}
# unclustered narrative items
from osint_monitor.processors.event_grouping import partition
class _S:  # minimal shim for partition(): needs .source.type/.name
    def __init__(s, it): s.id = it["id"]; s.source = type("x", (), {"type": it["stype"], "name": it["source"]})()
nar, stru = partition([_S(i) for i in items.values()], cfg)
nar_ids = {x.id for x in nar}; stru_ids = {x.id for x in stru}
res["narrative_items"] = len(nar_ids); res["structured_items"] = len(stru_ids)
res["structured_in_events"] = sorted(i for i in stru_ids if item_events[i])
un = sorted(i for i in nar_ids if not item_events[i])
res["unclustered_narrative"] = len(un)
res["unclustered_sample10"] = [{k: items[i][k] for k in ("id", "source", "published_at", "fetched_at", "lang", "title", "url")} for i in sorted(random.sample(un, min(10, len(un))))]
res["unclustered_by_source"] = Counter(items[i]["source"] for i in un)
res["narrative_by_source_in_events"] = Counter(items[i]["source"] for i in nar_ids if item_events[i])
res["roundups"] = [{"id": i["id"], "source": i["source"], "title": i["title"], "events": sorted(item_events[i["id"]])} for i in items.values() if i["roundup"]]
res["lang_counts"] = Counter(i["lang"] for i in items.values())
res["situations"] = {s["slug"]: {**{k: s[k] for k in ("id", "title", "status", "region", "primary_actors", "created_at", "updated_at")},
                                  "events": sorted(e for e in events if events[e]["situation_id"] == sid)} for sid, s in sits.items()}
res["struct_by_source"] = Counter(items[i]["source"] for i in stru_ids)
res["struct_samples"] = {}
for sname in sorted({items[i]["source"] for i in stru_ids}):
    ids = sorted(i for i in stru_ids if items[i]["source"] == sname)
    res["struct_samples"][sname] = [{k: items[i][k] for k in ("id", "published_at", "fetched_at", "title", "url", "external_id")} for i in sorted(random.sample(ids, min(2, len(ids))))]
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("ok", len(events), "events")
