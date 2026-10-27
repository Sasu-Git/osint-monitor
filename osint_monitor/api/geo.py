"""Country lookups for the workspace map: which country a point lies in, which country a place or an actor
names, and whether a Development's stored coordinates can be shown on the map.

Presentation only. Nothing here geocodes, writes coordinates or changes what the pipeline stored; it decides
which stored points the map may plot and which countries a Development concerns, from data already stored.

Country ids are stable codes (ISO 3166-1 alpha-3, or Natural Earth's own code where there is none; see
scripts/build_country_geo.py).
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).parent / "data" / "countries.json"
COAST_DEGREES = (0.05, 0.15)      # probe distances for coastal points outside the 1:50m outlines (~5 and ~15 km)


def _in_ring(lon: float, lat: float, ring: list) -> bool:
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


@dataclass(frozen=True)
class Country:
    id: str
    name: str
    names: tuple[str, ...]
    polygons: tuple = field(repr=False)      # ({"bbox": [x0, y0, x1, y1], "rings": [outer, *holes]}, ...)

    def contains(self, lat: float, lon: float) -> bool:
        for poly in self.polygons:
            x0, y0, x1, y1 = poly["bbox"]
            if x0 <= lon <= x1 and y0 <= lat <= y1:
                outer, *holes = poly["rings"]
                if _in_ring(lon, lat, outer) and not any(_in_ring(lon, lat, h) for h in holes):
                    return True
        return False


class CountryIndex:
    """The country outlines plus name lookups through the existing gazetteer and actor normaliser, so
    "Estados Unidos", "US", "Washington" (as an actor) and "United States of America" meet at one id."""

    def __init__(self, countries: list[Country], gazetteer, normalizer):
        self.countries = {c.id: c for c in countries}
        self.gazetteer = gazetteer
        self.normalizer = normalizer
        self._by_place: dict[str, str] = {}      # gazetteer country name -> id
        self._by_actor: dict[str, str] = {}      # actor key -> id
        for c in countries:
            for n in c.names:
                place = gazetteer.canonical(n)
                if place in gazetteer.countries:
                    self._by_place.setdefault(place, c.id)
                key = normalizer.key(n)
                if key:
                    self._by_actor.setdefault(key, c.id)
        for c in countries:                      # an actor key that is a gazetteer country name ("turkiye")
            for n in c.names:
                self._by_actor.setdefault(gazetteer.canonical(n), c.id)

    @classmethod
    @lru_cache(maxsize=1)
    def load(cls) -> "CountryIndex":
        from osint_monitor.processors.actors import ActorNormalizer
        from osint_monitor.processors.geography import Gazetteer
        raw = json.loads(DATA.read_text(encoding="utf-8"))
        countries = [Country(r["id"], r["name"], tuple(r["names"]), tuple(r["polygons"])) for r in raw]
        return cls(countries, Gazetteer.load(), ActorNormalizer.load())

    def name(self, country_id: str) -> str:
        c = self.countries.get(country_id)
        return c.name if c else country_id

    def all(self) -> list[tuple[str, str]]:
        """(id, name) for every country, by name."""
        return sorted(((c.id, c.name) for c in self.countries.values()), key=lambda x: x[1])

    def _inside(self, lat: float, lon: float) -> str | None:
        for c in self.countries.values():
            if c.contains(lat, lon):
                return c.id
        return None

    @lru_cache(maxsize=4096)
    def at(self, lat: float, lon: float) -> str | None:
        """The country a point lies in. A coastal point just outside the simplified outline (a harbour
        city) takes the country found within COAST_DEGREES, but only when every probe that lands in a
        country lands in the same one. None at sea, or between two countries."""
        inside = self._inside(lat, lon)
        if inside:
            return inside
        found = set()
        for d in COAST_DEGREES:
            for dy, dx in ((d, 0), (-d, 0), (0, d), (0, -d), (d, d), (d, -d), (-d, d), (-d, -d)):
                c = self._inside(lat + dy, lon + dx)
                if c:
                    found.add(c)
            if found:
                return next(iter(found)) if len(found) == 1 else None
        return None

    def within_extent(self, country_id: str, lat: float, lon: float) -> bool:
        c = self.countries.get(country_id)
        if c is None:
            return False
        xs = [v for p in c.polygons for v in (p["bbox"][0], p["bbox"][2])]
        ys = [v for p in c.polygons for v in (p["bbox"][1], p["bbox"][3])]
        return min(xs) <= lon <= max(xs) and min(ys) <= lat <= max(ys)

    def of_place(self, name: str) -> str | None:
        """The country a place mention names or lies in, when the gazetteer knows it."""
        place = self.gazetteer.canonical(name)
        if place in self.gazetteer.countries:
            return self._by_place.get(place)
        inside = [a for a in self.gazetteer.ancestors(place) if a in self.gazetteer.countries]
        return self._by_place.get(inside[0]) if len(inside) == 1 else None

    def of_actor(self, actor_key: str) -> str | None:
        """The country an actor key stands for ("china", "united states"); None for bodies and groups."""
        return self._by_actor.get(actor_key)


def valid_point(lat, lon) -> bool:
    return (lat is not None and lon is not None and -90 <= lat <= 90 and -180 <= lon <= 180
            and not (lat == 0 and lon == 0))


@dataclass
class Placement:
    """Where a Development is on the map, if anywhere, and why."""
    mapped: bool
    country: str | None = None               # country of the event's place (map point, else the place mentioned)
    label: str | None = None                 # the stored place name, shortened
    country_level: bool = False              # the stored point is a whole country, not a place in it
    reason: str = ""                         # why it is or is not on the map


def placement(index: CountryIndex, lat, lon, location_name: str | None, place_mentions: Counter) -> Placement:
    """Whether the stored point agrees with the places the Development's own reports mention.

    The pipeline geocodes the most-mentioned place name of a Development (processors/geocoding.py) and
    keeps the first result, which is sometimes another place of the same name (a "Gaza" in Mozambique).
    The point is shown only when the country it lies in is the country of a most-mentioned place the
    gazetteer knows; or, when none of those is known, the country of some mentioned place. Otherwise the
    Development stays in the feed without a marker.
    """
    label = (location_name or "").split(",")[0].strip() or None
    level = bool(location_name) and "," not in location_name
    expected_top, expected_any = set(), set()
    if place_mentions:
        top = max(place_mentions.values())
        for name, n in place_mentions.items():
            c = index.of_place(name)
            if c:
                expected_any.add(c)
                if n == top:
                    expected_top.add(c)
    if not valid_point(lat, lon):
        only = expected_top if len(expected_top) == 1 else set()
        return Placement(False, country=next(iter(only), None), label=label, reason="no stored coordinates")
    at = index.at(round(lat, 3), round(lon, 3))
    expected = expected_top or expected_any
    if at is None and level and len(expected_top) == 1:
        # a whole-country point of an archipelago can fall at sea between islands (Indonesia, Philippines):
        # keep it when it is within the extent of the one country the reports mention most
        c = next(iter(expected_top))
        if index.within_extent(c, lat, lon):
            return Placement(True, country=c, label=label, country_level=True, reason="confirmed by mentioned place")
    if at is None:
        return Placement(False, country=next(iter(expected_top), None) if len(expected_top) == 1 else None,
                         label=label, reason="stored point is outside every country outline")
    if not expected:
        return Placement(False, country=None, label=label,
                         reason="no mentioned place confirms the stored point")
    if at not in expected:
        return Placement(False, country=next(iter(expected_top), None) if len(expected_top) == 1 else None,
                         label=label, reason=f"stored point lies in {index.name(at)}, the reports mention "
                                             + ", ".join(sorted(index.name(c) for c in expected)))
    return Placement(True, country=at, label=label, country_level=level, reason="confirmed by mentioned place")
