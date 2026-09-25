"""Build benchmark windows from past data. Read-only on every input.

- ``from_database``: narrative items already collected in a local SQLite database,
  opened read-only (``mode=ro``).
- ``from_wayback``: Wayback Machine snapshots of the configured RSS feeds, fetched raw
  (``id_``) and parsed by the live RSS collector's own entry parser, so archived items
  look exactly like collected ones. Each item records the snapshot it came from.

Both return BenchmarkItems whose ``published_at`` lies in [start, end). Adding a window to
the manifest is a separate step (``add_window``), so importing never freezes anything.
"""

from __future__ import annotations

import logging
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Iterable

import feedparser
import requests

from osint_monitor.benchmark.format import (
    BENCHMARK_DIR, EXCERPT_CHARS, BenchmarkError, BenchmarkItem, Manifest, Split, WindowEntry, WindowSource,
    item_id, write_items, write_labels_template, write_manifest,
)
from osint_monitor.collectors.rss import RSSCollector
from osint_monitor.core.config import load_event_grouping_config, load_sources_config
from osint_monitor.processors.event_grouping import NARRATIVE, source_class

logger = logging.getLogger(__name__)

CDX_URL = "https://web.archive.org/cdx/search/cdx"
SNAPSHOT_URL = "https://web.archive.org/web/{timestamp}id_/{url}"   # id_: the original bytes, unrewritten
# a feed snapshot holds the latest ~20-50 entries, roughly the previous day: look a day past the window
SNAPSHOT_LOOKAHEAD = timedelta(days=1)


def _item(source: str, title: str, excerpt: str, url: str, published_at: datetime, provenance: dict) -> BenchmarkItem:
    return BenchmarkItem(id=item_id(source, title, published_at), published_at=published_at, source=source,
                         title=" ".join(title.split()), excerpt=(excerpt or "").strip()[:EXCERPT_CHARS],
                         url=url or "", provenance=provenance)


# --- local database ----------------------------------------------------------------------------

def from_database(db_path: str | Path, start: datetime, end: datetime) -> list[BenchmarkItem]:
    db_path = Path(db_path)
    if not db_path.exists():
        raise BenchmarkError(f"{db_path}: database not found")
    grouping = load_event_grouping_config()
    con = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT r.id, s.name, s.type, r.title, r.content, r.url, COALESCE(r.published_at, r.fetched_at) "
            "FROM raw_items r JOIN sources s ON s.id = r.source_id").fetchall()
    finally:
        con.close()
    items: dict[str, BenchmarkItem] = {}
    for raw_id, source, stype, title, content, url, when in rows:
        if not title or source_class(source, stype, grouping) != NARRATIVE:
            continue
        published = datetime.fromisoformat(str(when)) if when else None
        if published is None or not start <= published < end:
            continue
        item = _item(source, title, content, url, published, {
            "benchmark_source": "local_db", "database": db_path.name, "raw_item_id": raw_id,
            "original_feed": source})
        items.setdefault(item.id, item)
    return sorted(items.values(), key=lambda i: (i.published_at, i.source, i.id))


# --- Wayback Machine ---------------------------------------------------------------------------

Fetcher = Callable[[str, dict | None], str]


def http_fetch(url: str, params: dict | None = None, retries: int = 2, pause: float = 1.0) -> str:
    """GET with (connect, read) timeouts, retries and a pause between calls (archive.org is shared)."""
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            time.sleep(pause)
            resp = requests.get(url, params=params, timeout=(10, 60),
                                headers={"User-Agent": "osint-monitor-benchmark/1.0 (research; low volume)"})
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            last = e
            logger.info("fetch failed (%s), attempt %d: %s", url, attempt + 1, e)
    raise BenchmarkError(f"could not fetch {url}: {last}")


def snapshots(feed_url: str, start: datetime, end: datetime, fetch: Fetcher = http_fetch) -> list[str]:
    """Timestamps of archived 200 responses for a feed between start and end + lookahead."""
    text = fetch(CDX_URL, {"url": feed_url, "from": start.strftime("%Y%m%d%H%M%S"),
                           "to": (end + SNAPSHOT_LOOKAHEAD).strftime("%Y%m%d%H%M%S"),
                           "fl": "timestamp", "filter": "statuscode:200"})
    return sorted({line.strip() for line in text.splitlines() if line.strip().isdigit()})


def from_wayback(feeds: Iterable[tuple[str, str]], start: datetime, end: datetime,
                 fetch: Fetcher = http_fetch, max_snapshots_per_feed: int = 8) -> tuple[list[BenchmarkItem], dict]:
    """Items published in [start, end) from archived snapshots of (name, url) feeds.
    An item seen in several snapshots keeps the earliest. Returns (items, per-feed report)."""
    items: dict[str, BenchmarkItem] = {}
    report: dict[str, dict] = {}
    for name, url in feeds:
        stamps = snapshots(url, start, end, fetch)
        if len(stamps) > max_snapshots_per_feed:              # spread evenly: coverage, not volume
            step = len(stamps) / max_snapshots_per_feed
            stamps = [stamps[int(i * step)] for i in range(max_snapshots_per_feed)]
        kept = 0
        for stamp in stamps:
            archive_url = SNAPSHOT_URL.format(timestamp=stamp, url=url)
            try:
                feed = feedparser.parse(fetch(archive_url, None))
            except BenchmarkError as e:
                logger.warning("%s", e)
                continue
            for raw in RSSCollector.entries_to_items(feed.entries, name):
                if raw.published_at is None or not start <= raw.published_at < end:
                    continue
                item = _item(name, raw.title, raw.content, raw.url, raw.published_at, {
                    "benchmark_source": "wayback", "original_feed": name, "feed_url": url,
                    "snapshot_timestamp": stamp, "archive_url": archive_url})
                if item.id not in items:
                    items[item.id] = item
                    kept += 1
        report[name] = {"snapshots": len(stamps), "items": kept}
    return sorted(items.values(), key=lambda i: (i.published_at, i.source, i.id)), report


def configured_feeds(names: Iterable[str] | None = None) -> list[tuple[str, str]]:
    feeds = [(f.name, f.url) for f in load_sources_config().rss_feeds if f.enabled]
    if names:
        wanted = set(names)
        feeds = [f for f in feeds if f[0] in wanted]
        missing = wanted - {f[0] for f in feeds}
        if missing:
            raise BenchmarkError(f"unknown feed names: {sorted(missing)}")
    return feeds


# --- manifest ---------------------------------------------------------------------------------

def add_window(manifest: Manifest, window_id: str, split: Split, start: datetime, end: datetime,
               source: WindowSource, items: list[BenchmarkItem], root: Path = BENCHMARK_DIR) -> WindowEntry:
    """Write the items file and a labels template, and record the window (not frozen)."""
    if any(w.id == window_id for w in manifest.windows):
        existing = manifest.window(window_id)
        if existing.items_sha256:
            raise BenchmarkError(f"window {window_id!r} is frozen; choose a new id instead of overwriting it")
        manifest.windows = [w for w in manifest.windows if w.id != window_id]
    entry = WindowEntry(
        id=window_id, split=split, start=start, end=end, source=source,
        items_file=f"windows/{window_id}.items.jsonl", labels_file=f"labels/{window_id}.labels.yaml",
        stats={"items": len(items), "sources": len({i.source for i in items}),
               "per_source": dict(sorted(_count(i.source for i in items).items()))})
    entry.overlaps = sorted(w.id for w in manifest.windows if w.start < end and start < w.end)
    for w in manifest.windows:
        if w.id in entry.overlaps and window_id not in w.overlaps:
            w.overlaps = sorted([*w.overlaps, window_id])
    write_items(root / entry.items_file, items)
    write_labels_template(root / entry.labels_file, window_id)
    manifest.windows.append(entry)
    manifest.windows.sort(key=lambda w: w.start)
    write_manifest(root / "manifest.yaml", manifest)
    return entry


def _count(values) -> dict:
    out: dict = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return out
