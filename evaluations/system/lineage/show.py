import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
ids = sys.argv[2:] or list(r["all_events"])
for k in ids:
    e = r["all_events"][str(k)]
    print(f"== E{e['id']} n={e['n_items']} src={e['n_sources']}/{e['source_count']} {e['admiralty']} {e['confidence_class']} dom={e['domain']} sit={e['situation']} rank={e['rank_score'] and round(e['rank_score'],2)} {e['rank_reasons']} region={e['region']}")
    print(f"   first={e['first_reported_at'][:16]} last={e['last_updated_at'][:16]} items {str(e['item_pub_min'])[:16]}..{str(e['item_pub_max'])[:16]}")
    print(f"   SUMMARY: {e['summary'][:150]}")
    print(f"   DBprinc={e['db_principals']}  MAINprinc={e.get('main_principals')}")
    for i in e["items"]:
        fl = ("R" if i["roundup"] else "") + (i["hkind"][0].upper() if i["hkind"]!="report" else "") + (f" also{i['other_events']}" if i["other_events"] else "")
        print(f"     {i['id']:>5} {i['source'][:18]:18} {str(i['pub'])[:16]} {i['lang']} {fl:4} {i['title'][:110]}")
