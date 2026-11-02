"""Map-only alias table: which audited Developments change from hidden to shown (or back), read-only.

    PYTHONPATH=<this branch> python check_aliases.py --db <snapshot> --cases <audit cases.json> --out result.json

Same placement code twice: the map's CountryIndex with its alias table emptied (the deployed behaviour; checked
against the audit's recorded `shown`) and with place_aliases.json. Place mentions are counted exactly as the
workspace does (LOC/GPE/FAC entity canonical names over the Development's items).
Rule for semantic neutrality: only stored-verdict C (right point) may flip hidden -> shown; no W (wrong point) may
become shown; nothing shown may become hidden.
"""
import argparse, json, sqlite3
from collections import Counter, defaultdict

from osint_monitor.api.geo import CountryIndex, placement

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--cases", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

cases = json.load(open(a.cases, encoding="utf-8"))
c = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
mentions = defaultdict(Counter)
for eid, name in c.execute("select ei.event_id, en.canonical_name from event_items ei join item_entities ie on ie.item_id = "
                           "ei.item_id join entities en on en.id = ie.entity_id where en.entity_type in "
                           "('LOC','GPE','FAC','LOCATION','FACILITY')"):
    mentions[eid][name] += 1
index = CountryIndex.load()
aliases = dict(index.map_aliases)

def shown(case, with_aliases):
    index.map_aliases = aliases if with_aliases else {}
    p = placement(index, case["lat"], case["lon"], case["stored_place"], mentions.get(case["development_id"], Counter()))
    return p.mapped

rows, tally = [], Counter()
for case in cases:
    before, after = shown(case, False), shown(case, True)
    flip = "same" if before == after else ("hidden->shown" if after else "shown->hidden")
    tally[(case["stored_verdict"], flip)] += 1
    rows.append({"development_id": case["development_id"], "set": case["set"], "verdict": case["stored_verdict"],
                 "root_cause": case["root_cause"], "recorded_shown": case["shown"], "before": before, "after": after,
                 "flip": flip})
summary = {
    "cases": len(rows),
    "before_matches_recorded_audit": sum(r["before"] == r["recorded_shown"] for r in rows),
    "C_hidden_to_shown": tally[("C", "hidden->shown")],
    "W_hidden_to_shown": tally[("W", "hidden->shown")],
    "P_hidden_to_shown": tally[("P", "hidden->shown")],
    "any_shown_to_hidden": sum(n for (v, f), n in tally.items() if f == "shown->hidden"),
    "C_still_hidden": [r["development_id"] for r in rows if r["verdict"] == "C" and not r["after"]],
    "flipped": [(r["development_id"], r["verdict"], r["flip"]) for r in rows if r["flip"] != "same"],
}
summary["neutral"] = summary["W_hidden_to_shown"] == 0 and summary["any_shown_to_hidden"] == 0
json.dump({"summary": summary, "rows": rows}, open(a.out, "w", encoding="utf-8"), indent=1)
print(json.dumps(summary, indent=1))
