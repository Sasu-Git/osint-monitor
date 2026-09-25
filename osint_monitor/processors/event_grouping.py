"""Narrative vs structured items, and identity-based grouping for structured records.

Semantic clustering assumes that two texts reading alike describe the same development.
That holds for prose news and fails for machine-generated records: "Earthquake M5.3 -
51 km WSW of Arauco, Argentina" and "Earthquake M5 - Mariana Islands region" are
near-identical templates of unrelated events (live 2026-09-24: 18 quakes in one event).

So items are split by source class (config/event_grouping.yaml):

- **narrative** -> ``clustering.cluster_recent_items`` (embeddings + link graph), unchanged;
- **structured** -> a per-source strategy here, grouping only records of the *same*
  real-world thing:
    - ``seismic``: shared USGS event id, else origin time + epicentre + magnitude all close;
    - ``standalone`` (default): each record is its own observation and is never merged.

Both paths return plain item-id groups, so persistence, classification, ranking and
situations see ordinary Events and never need to know which path built them.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from osint_monitor.core.config import EventGroupingConfig, SeismicFusionConfig, load_event_grouping_config
from osint_monitor.core.database import RawItem

NARRATIVE, STRUCTURED = "narrative", "structured"
STANDALONE, SEISMIC = "standalone", "seismic"


def source_class(source_name: str | None, source_type: str | None, config: EventGroupingConfig) -> str:
    if source_name in config.narrative_sources:
        return NARRATIVE
    if source_name in config.structured.sources or source_type in config.structured.source_types:
        return STRUCTURED
    return NARRATIVE


def partition(items: Iterable[RawItem], config: EventGroupingConfig) -> tuple[list[RawItem], list[RawItem]]:
    """(narrative, structured) items."""
    narrative, structured = [], []
    for item in items:
        src = item.source
        kind = source_class(src.name if src else None, src.type if src else None, config)
        (structured if kind == STRUCTURED else narrative).append(item)
    return narrative, structured


# --- seismic -------------------------------------------------------------------------------

_EVENT_PAGE = re.compile(r"eventpage/([A-Za-z0-9]+)")
_ID_PREFIX = re.compile(r"^(?:usgs_|seis_exp_)")
_LOCATION = re.compile(r"Location:\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)")
_MAGNITUDE = re.compile(r"Magnitude:\s*(-?\d+(?:\.\d+)?)")


@dataclass(frozen=True)
class SeismicReading:
    item_id: int
    event_ids: frozenset[str]           # catalogue ids (a quake can carry several: "ak2026x,us6000y")
    time: datetime | None
    lat: float | None
    lon: float | None
    magnitude: float | None


def parse_seismic(item: RawItem) -> SeismicReading:
    ids = set()
    if item.url and (m := _EVENT_PAGE.search(item.url)):
        ids.add(m.group(1).lower())
    if item.external_id:
        ids.update(p.lower() for p in _ID_PREFIX.sub("", item.external_id).split(",") if p)
    text = item.content or ""
    loc, mag = _LOCATION.search(text), _MAGNITUDE.search(text)
    return SeismicReading(
        item.id, frozenset(ids), item.published_at,
        float(loc.group(1)) if loc else None, float(loc.group(2)) if loc else None,
        float(mag.group(1)) if mag else None,
    )


def _km(a: SeismicReading, b: SeismicReading) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (a.lat, a.lon, b.lat, b.lon))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def same_earthquake(a: SeismicReading, b: SeismicReading, cfg: SeismicFusionConfig) -> bool:
    if a.event_ids & b.event_ids:
        return True
    if None in (a.time, b.time, a.lat, b.lat, a.magnitude, b.magnitude):
        return False                  # without identity or a full reading, never guess
    return (abs((a.time - b.time).total_seconds()) <= cfg.max_seconds_apart
            and _km(a, b) <= cfg.max_km_apart
            and abs(a.magnitude - b.magnitude) <= cfg.max_magnitude_difference)


def _components(n: int, linked) -> list[list[int]]:
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if linked(i, j):
                parent[find(i)] = find(j)
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def group_seismic(items: list[RawItem], cfg: SeismicFusionConfig) -> list[list[int]]:
    readings = [parse_seismic(i) for i in items]
    parts = _components(len(readings), lambda i, j: same_earthquake(readings[i], readings[j], cfg))
    return [[readings[i].item_id for i in part] for part in parts]


# --- dispatch ------------------------------------------------------------------------------

STRATEGIES = {STANDALONE, SEISMIC}


def strategy_for(item: RawItem, config: EventGroupingConfig) -> str:
    strategy = config.strategies.get(item.source.name if item.source else "", STANDALONE)
    if strategy not in STRATEGIES:
        raise ValueError(f"Unknown structured grouping strategy {strategy!r} in event_grouping.yaml "
                         f"(options: {sorted(STRATEGIES)})")
    return strategy


def group_structured(items: list[RawItem], config: EventGroupingConfig | None = None,
                     min_size: int = 2) -> list[list[int]]:
    """Groups of structured item ids that record the same real-world thing (>= ``min_size``).
    Standalone records form no group: one reading is an observation, not a development."""
    config = config or load_event_grouping_config()
    by_strategy: dict[str, list[RawItem]] = {}
    for item in items:
        by_strategy.setdefault(strategy_for(item, config), []).append(item)
    groups: list[list[int]] = []
    if SEISMIC in by_strategy:
        groups += group_seismic(by_strategy[SEISMIC], config.seismic)
    return [g for g in groups if len(g) >= min_size]
