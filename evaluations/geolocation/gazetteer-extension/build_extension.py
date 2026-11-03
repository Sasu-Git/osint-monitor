"""Build the location layer's frozen gazetteer extension from GeoNames (one-time, offline after download).

    python build_extension.py --cities <dir>/cities15000.txt --countries <dir>/countryInfo.txt \
        --out osint_monitor/processors/data/place_extension.json

Source: GeoNames "cities15000" (every populated place with population >= 15,000) and countryInfo.txt, downloaded
2026-11-03 from https://download.geonames.org/export/dump/ (CC BY 4.0, GeoNames.org). Hashes in SOURCE.md.

Read only by osint_monitor/processors/event_location.py. The shared gazetteer (config/geography.yaml) is unchanged and
always takes precedence: a name the gazetteer knows is never looked up here.

Rules (frozen, independent of any evaluation case):
  - names: the GeoNames name, its ASCII name, and alternate names that are Latin-script, start with an upper-case
    letter, are at least 4 characters and not all capitals (drops airport codes and lower-case romanisations);
  - country: the GeoNames country code mapped to the gazetteer's country through countryInfo's English name
    (gazetteer canonical form), else through COUNTRY_OVERRIDES below (country names only), else the place is dropped;
  - each name keeps every candidate country with that country's largest population for the name; event_location
    resolves among them (L2: only inside the countries the reports name);
  - names the gazetteer already knows are not written.
"""
import argparse, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--cities", required=True)
ap.add_argument("--countries", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

from osint_monitor.processors.geography import Gazetteer

geo = Gazetteer.load()

# GeoNames English country names the gazetteer writes differently (country-name spelling only)
COUNTRY_OVERRIDES = {
    "Palestinian Territory": "palestine", "Republic of the Congo": "congo", "DR Congo": "democratic republic of the congo",
    "Ivory Coast": "cote d'ivoire", "The Netherlands": "netherlands", "Bahamas": "bahamas", "Gambia": "gambia",
    "Macedonia": "north macedonia", "North Macedonia": "north macedonia", "Czechia": "czech republic",
    "Myanmar": "myanmar", "Eswatini": "eswatini", "Timor Leste": "timor-leste", "Cabo Verde": "cape verde",
    "Vatican": "vatican city", "Micronesia": "micronesia", "South Korea": "south korea", "North Korea": "north korea",
}

def country_name(gn_name: str) -> str | None:
    for cand in (gn_name, COUNTRY_OVERRIDES.get(gn_name)):
        if not cand:
            continue
        k = geo.canonical(cand)
        if k in geo.countries:
            return k
        inside = [x for x in geo.ancestors(k) if x in geo.countries]
        if len(inside) == 1:                     # Hong Kong, Macau: the gazetteer files them under China
            return inside[0]
    return None

cc_country, unmapped = {}, []
for line in open(a.countries, encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    f = line.rstrip("\n").split("\t")
    c = country_name(f[4])
    if c:
        cc_country[f[0]] = c
    else:
        unmapped.append(f"{f[0]} {f[4]}")

def latin(s: str) -> bool:
    return all(not ch.isalpha() or "LATIN" in unicodedata.name(ch, "") for ch in s)

def usable_alt(s: str) -> bool:
    return len(s) >= 4 and s[0].isupper() and not s.isupper() and latin(s) and not re.search(r"\d", s)

places: dict[str, dict[str, list]] = {}      # name -> {country: [population, lat, lon]}
stats = Counter()
for line in open(a.cities, encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    name, ascii_name, alts, lat, lon, cc, pop = f[1], f[2], f[3], float(f[4]), float(f[5]), f[8], int(f[14] or 0)
    country = cc_country.get(cc)
    if country is None:
        stats["place_dropped_unmapped_country"] += 1
        continue
    stats["places"] += 1
    names = {name, ascii_name} | {x for x in alts.split(",") if usable_alt(x)}
    for n in names:
        key = n.strip().lower()
        if len(key) < 3 or key in geo.known or geo.canonical(key) in geo.known:
            continue
        cur = places.setdefault(key, {}).get(country)
        if cur is None or pop > cur[0]:
            places[key][country] = [pop, round(lat, 4), round(lon, 4)]

stats["names"] = len(places)
stats["names_multi_country"] = sum(1 for v in places.values() if len(v) > 1)
out = {"_source": "GeoNames cities15000 + countryInfo, downloaded 2026-11-03, CC BY 4.0 (geonames.org); "
                   "built by evaluations/geolocation/gazetteer-extension/build_extension.py",
       "places": {k: places[k] for k in sorted(places)}}
Path(a.out).parent.mkdir(parents=True, exist_ok=True)
Path(a.out).write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":"), sort_keys=False), encoding="utf-8")
print(json.dumps({**stats, "unmapped_countries": unmapped}, indent=1, ensure_ascii=False))
