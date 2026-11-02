"""Read-only geolocation audit of stored Development locations (2026-11-02).

Run with PYTHONPATH = a checkout of deploy-web-20261102 (d06af11; it has osint_monitor/api/geo.py, the map's
placement check) against a backup-API snapshot of the live DB:

    python audit.py --db <snapshot.db> --sources <repo>/config/sources.yaml --out audit-all.json

Writes nothing to the database (opened mode=ro). For every Development it records the stored place, the
country the stored point lies in, the places its member items mention, the frontend placement decision, and
a rule-based root-cause label (reviewed by hand for the frozen case set, cases.json).
"""
import argparse, json, sqlite3
from collections import Counter, defaultdict

import yaml

from osint_monitor.api.geo import CountryIndex, placement, valid_point

LOC_TYPES = ("LOC", "GPE", "FAC", "LOCATION", "FACILITY")    # as processors/geocoding.py and workspace_views.py
CAPITALS = {"washington", "moscow", "beijing", "kyiv", "kiev", "tehran", "london", "paris", "berlin", "brussels",
            "jerusalem", "damascus", "ankara", "riyadh", "doha", "cairo", "tokyo", "seoul", "pyongyang",
            "taipei", "new delhi", "islamabad", "kabul", "baghdad", "beirut", "havana", "caracas", "minsk"}


def label_root_cause(r, index):
    at, top, anyc = r["point_country"], set(r["expected_top"]), set(r["expected_any"])
    stored_first = (r["stored_place"] or "").split(",")[0].strip().lower()
    names = {n.lower() for n in r["mentions"]}
    parts = [p.strip() for p in (r["stored_place"] or "").split(",")]
    if not r["valid_point"] or (at is None and not r["shown"]):
        return "INVALID_STORED_PLACE"
    if r["shown"]:
        if stored_first in CAPITALS and len(top) == 1 and len(anyc) > 1 and stored_first in names:
            return "CAPITAL_COUNTRY_CONFUSION"      # shown, but the capital may stand for the government
        return "CORRECT_LOCATION"
    if not anyc:
        return "MISSING_ALIAS" if r["mentions"] else "OTHER"
    if len(top) > 1 and at in anyc:
        return "MULTIPLE_PLACES_NO_DOMINANT_LOCATION"
    if at in anyc and at not in top:
        return "MULTIPLE_PLACES_NO_DOMINANT_LOCATION"
    expected_names = {index.name(c).lower() for c in anyc}
    if any(p.lower() in expected_names for p in parts[1:]):
        return "MISSING_CONTAINMENT"               # the geocoder's own address names an expected country
    if stored_first and stored_first in names:
        if stored_first in CAPITALS:
            return "CAPITAL_COUNTRY_CONFUSION"
        if index.gazetteer.canonical(stored_first) in index.gazetteer.countries:
            return "REGION_CITY_COLLISION"          # a country name resolved to a sub-national place elsewhere
        if len(parts) >= 5:
            return "FIRST_RESULT_WINS"              # a street / building / business hit, not the place
        return "AMBIGUOUS_NAME"                     # same name, another real place
    return "WRONG_COUNTRY_MATCH"                    # stored place is not one of the current mentions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--sources", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lang = {s["name"]: s.get("language", "?") for s in _sources(a.sources)}
    c = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    index = CountryIndex.load()
    mentions = defaultdict(Counter)
    q = (f"select ei.event_id, en.canonical_name from event_items ei join item_entities ie on ie.item_id = ei.item_id "
         f"join entities en on en.id = ie.entity_id where en.entity_type in ({','.join('?' * len(LOC_TYPES))})")
    for eid, name in c.execute(q, LOC_TYPES):
        mentions[eid][name] += 1
    langs = defaultdict(Counter)
    for eid, src in c.execute("select ei.event_id, s.name from event_items ei join raw_items r on r.id = ei.item_id "
                              "join sources s on s.id = r.source_id"):
        langs[eid][lang.get(src, "?")] += 1
    rows = []
    for eid, summary, lat, lon, loc, members, sid in c.execute(
            "select e.id, e.summary, e.lat, e.lon, e.location_name, (select count(*) from event_items where event_id = e.id), "
            "e.situation_id from events e order by e.id"):
        m = mentions.get(eid, Counter())
        p = placement(index, lat, lon, loc, m)
        top = max(m.values()) if m else 0
        r = {"development_id": eid, "summary": summary, "members": members, "situation_id": sid,
             "stored_place": loc, "lat": lat, "lon": lon, "valid_point": valid_point(lat, lon),
             "point_country": index.at(round(lat, 3), round(lon, 3)) if valid_point(lat, lon) else None,
             "mentions": dict(m.most_common(8)),
             "top_mentions": sorted(n for n, k in m.items() if k == top),
             "expected_top": sorted({index.of_place(n) for n, k in m.items() if k == top} - {None}),
             "expected_any": sorted({index.of_place(n) for n in m} - {None}),
             "unresolved_mentions": sorted(n for n in m if index.of_place(n) is None)[:8],
             "languages": dict(langs.get(eid, Counter())),
             "shown": p.mapped, "frontend_reason": p.reason, "frontend_country": p.country}
        r["root_cause_auto"] = label_root_cause(r, index) if loc or lat is not None else "NO_STORED_LOCATION"
        rows.append(r)
    json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(Counter(r["root_cause_auto"] for r in rows).most_common())


def _sources(path):
    raw = yaml.safe_load(open(path, encoding="utf-8"))
    out = []
    def walk(x):
        if isinstance(x, dict):
            if "name" in x and ("url" in x or "type" in x):
                out.append(x)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(raw)
    return out


if __name__ == "__main__":
    main()
