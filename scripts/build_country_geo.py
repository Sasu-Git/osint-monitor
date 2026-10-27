"""Build the country geometry the workspace map uses, from Natural Earth admin-0 countries (public domain).

    python scripts/build_country_geo.py NE_110M.geojson NE_50M.geojson

Source: https://github.com/nvkelso/natural-earth-vector, tag v5.1.2, geojson/ne_{110m,50m}_admin_0_countries.geojson.

Writes two files, both keyed by one stable country id (ISO 3166-1 alpha-3 where Natural Earth has one, its own
ADM0_A3 code otherwise: Kosovo KOS, Northern Cyprus CYN, Somaliland SOL):
- web/static/geo/countries.geojson     110m outlines for the browser map (id + name only, 2-decimal coordinates)
- osint_monitor/api/data/countries.json 50m outlines for server-side point-in-country lookups, with the names
                                        Natural Earth gives each country (3-decimal coordinates)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_FIELDS = ("ADMIN", "NAME", "NAME_LONG", "FORMAL_EN", "NAME_EN")


def country_id(p: dict) -> str:
    return p["ISO_A3_EH"] if p["ISO_A3_EH"] not in ("-99", "", None) else p["ADM0_A3"]


def rounded(coords, digits):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], digits), round(coords[1], digits)]
    return [rounded(c, digits) for c in coords]


def polygons(geometry) -> list:
    return [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]


def main(small: str, large: str) -> int:
    features = []
    for f in json.loads(Path(small).read_text(encoding="utf-8"))["features"]:
        p = f["properties"]
        features.append({"type": "Feature", "id": country_id(p),
                         "properties": {"id": country_id(p), "name": p["NAME"]},
                         "geometry": {"type": f["geometry"]["type"], "coordinates": rounded(f["geometry"]["coordinates"], 2)}})
    out = ROOT / "web/static/geo/countries.geojson"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"type": "FeatureCollection", "features": features}, separators=(",", ":")), encoding="utf-8")

    # several features can share one id (Australia's external territories are AUS too): merge them, and name
    # the country after the feature whose own code is the id (the mainland)
    merged: dict[str, dict] = {}
    for f in json.loads(Path(large).read_text(encoding="utf-8"))["features"]:
        p = f["properties"]
        cid = country_id(p)
        c = merged.setdefault(cid, {"id": cid, "name": p["NAME"], "names": set(), "polygons": []})
        if p["ADM0_A3"] == cid:
            c["name"] = p["NAME"]
            c["names"] |= {p[k] for k in NAME_FIELDS if p.get(k)}
        for poly in polygons(f["geometry"]):
            rings = rounded(poly, 3)
            xs, ys = [pt[0] for pt in rings[0]], [pt[1] for pt in rings[0]]
            c["polygons"].append({"bbox": [min(xs), min(ys), max(xs), max(ys)], "rings": rings})
    countries = [{**c, "names": sorted(c["names"] or {c["name"]})} for c in merged.values()]
    data = ROOT / "osint_monitor/api/data/countries.json"
    data.parent.mkdir(parents=True, exist_ok=True)
    data.write_text(json.dumps(countries, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print(f"{len(features)} map outlines -> {out.relative_to(ROOT)}; {len(countries)} lookup outlines -> {data.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
