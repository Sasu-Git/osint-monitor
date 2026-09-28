"""Frozen clustering benchmark: file format, loading, validation and hashing.

Layout (under ``evaluations/clustering/`` by default):

    manifest.yaml                    windows, splits, provenance, SHA-256 of every frozen file
    windows/<id>.items.jsonl         one item per line: the replay input (title + excerpt), sorted
    labels/<id>.labels.yaml          gold developments for that window, written by a human

Items are *inputs* only. Actors, locations and event types are derived at replay time
by the current pipeline, so the benchmark measures the pipeline as it is, not as it was
when the window was frozen.

Gold labels (labels file):

    developments:
      - id: us-china-summit-2026-09-25
        members: [b-1a2b..., b-3c4d...]      # reports of one concrete occurrence
        storyline: us-china-summit            # optional: developments sharing a storyline
        notes: ""                             #   are RELATED_BUT_DISTINCT to each other
    related_pairs: [[b-..., b-..., "note"]]   # optional explicit RELATED_BUT_DISTINCT pairs
    uncertain_pairs: [[b-..., b-..., "note"]] # excluded from pair metrics

An item in no development is a singleton. Pairs not SAME and not RELATED are UNRELATED
(an assumption, since not every pair is reviewed; reports state it).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from itertools import combinations
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, ValidationError

from osint_monitor.core.config import BASE_DIR

BENCHMARK_DIR = BASE_DIR / "evaluations" / "clustering"
FORMAT_VERSION = 1
EXCERPT_CHARS = 1000        # the classifier context length; embeddings read only the first 200


class BenchmarkError(ValueError):
    """A benchmark file is malformed or does not match its frozen hash."""


class Split(str, Enum):
    DEVELOPMENT = "development"
    HOLDOUT = "holdout"


class PairLabel(str, Enum):
    SAME = "same_development"
    RELATED = "related_but_distinct"
    UNRELATED = "unrelated"
    UNCERTAIN = "uncertain"


class BenchmarkItem(BaseModel):
    id: str
    published_at: datetime
    source: str
    title: str
    excerpt: str = ""
    url: str = ""
    provenance: dict = Field(default_factory=dict)   # benchmark_source, original_feed, snapshot, archive_url ...

    model_config = {"extra": "forbid"}


class WindowSource(BaseModel):
    kind: str                                  # local_db | wayback
    reference: str                             # database path, or the feeds queried
    notes: str = ""


class WindowEntry(BaseModel):
    id: str
    split: Split
    start: datetime
    end: datetime
    source: WindowSource
    items_file: str
    labels_file: str
    items_sha256: Optional[str] = None
    labels_sha256: Optional[str] = None
    frozen_at: Optional[datetime] = None
    stats: dict = Field(default_factory=dict)  # items, sources, per_source
    overlaps: list[str] = Field(default_factory=list)


class Manifest(BaseModel):
    version: int = FORMAT_VERSION
    windows: list[WindowEntry] = Field(default_factory=list)

    def window(self, window_id: str) -> WindowEntry:
        for w in self.windows:
            if w.id == window_id:
                return w
        raise BenchmarkError(f"no window {window_id!r} in the manifest (have: {[w.id for w in self.windows]})")


class Development(BaseModel):
    id: str
    members: list[str]
    storyline: Optional[str] = None
    notes: str = ""

    model_config = {"extra": "forbid"}


class WindowLabels(BaseModel):
    window: str
    labelled_by: str = ""
    labelled_at: Optional[datetime] = None
    developments: list[Development] = Field(default_factory=list)
    related_pairs: list[list[str]] = Field(default_factory=list)
    uncertain_pairs: list[list[str]] = Field(default_factory=list)
    notes: str = ""

    model_config = {"extra": "forbid"}


# --- ids, hashing, deterministic writing ------------------------------------------------------

def item_id(source: str, title: str, published_at: datetime | None) -> str:
    """Stable id: the same report always gets the same id, whichever importer found it."""
    key = f"{source.strip().lower()}|{' '.join(title.split()).lower()}|{published_at.isoformat() if published_at else ''}"
    return "b-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_items(path: Path, items: list[BenchmarkItem]) -> None:
    """Deterministic JSONL: sorted by (published_at, source, id), sorted keys, LF endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(items, key=lambda i: (i.published_at, i.source, i.id))
    lines = [json.dumps(i.model_dump(mode="json"), sort_keys=True, ensure_ascii=False) for i in ordered]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))


def _yaml_dump(data) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120)


def write_manifest(path: Path, manifest: Manifest) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Clustering benchmark manifest. Hashes are set by `python main.py benchmark freeze`.\n")
        f.write(_yaml_dump(manifest.model_dump(mode="json")))


def write_labels_template(path: Path, window_id: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# Gold labels for {window_id}. See osint_monitor/benchmark/format.py for the format.\n")
        f.write(_yaml_dump(WindowLabels(window=window_id).model_dump(mode="json")))


# --- loading and validation --------------------------------------------------------------------

def load_manifest(root: Path = BENCHMARK_DIR) -> Manifest:
    path = root / "manifest.yaml"
    if not path.exists():
        return Manifest()
    try:
        return Manifest(**(yaml.safe_load(path.read_text(encoding="utf-8")) or {}))
    except (ValidationError, yaml.YAMLError, TypeError) as e:
        raise BenchmarkError(f"{path}: malformed manifest: {e}") from e


def load_items(path: Path) -> list[BenchmarkItem]:
    if not path.exists():
        raise BenchmarkError(f"{path}: items file missing")
    items, seen = [], set()
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = BenchmarkItem(**json.loads(line))
        except (json.JSONDecodeError, ValidationError, TypeError) as e:
            raise BenchmarkError(f"{path}:{n}: malformed item: {e}") from e
        if item.id in seen:
            raise BenchmarkError(f"{path}:{n}: duplicate item id {item.id}")
        seen.add(item.id)
        items.append(item)
    return items


def load_labels(path: Path, items: list[BenchmarkItem]) -> WindowLabels:
    if not path.exists():
        raise BenchmarkError(f"{path}: labels file missing")
    try:
        labels = WindowLabels(**(yaml.safe_load(path.read_text(encoding="utf-8")) or {}))
    except (ValidationError, yaml.YAMLError, TypeError) as e:
        raise BenchmarkError(f"{path}: malformed labels: {e}") from e
    known = {i.id for i in items}
    placed: dict[str, str] = {}
    dev_ids = set()
    for dev in labels.developments:
        if dev.id in dev_ids:
            raise BenchmarkError(f"{path}: duplicate development id {dev.id!r}")
        dev_ids.add(dev.id)
        if not dev.members:
            raise BenchmarkError(f"{path}: development {dev.id!r} has no members")
        for m in dev.members:
            if m not in known:
                raise BenchmarkError(f"{path}: development {dev.id!r} lists unknown item {m!r}")
            if m in placed:
                raise BenchmarkError(f"{path}: item {m} is in both {placed[m]!r} and {dev.id!r}")
            placed[m] = dev.id
    for kind, pairs in (("related_pairs", labels.related_pairs), ("uncertain_pairs", labels.uncertain_pairs)):
        for p in pairs:
            if len(p) < 2 or p[0] not in known or p[1] not in known:
                raise BenchmarkError(f"{path}: {kind} entry {p!r} must start with two known item ids")
    return labels


def verify_frozen(entry: WindowEntry, root: Path = BENCHMARK_DIR, need_labels: bool = True) -> None:
    """Refuse to evaluate a window whose files changed since they were frozen."""
    if entry.items_sha256 is None or (need_labels and entry.labels_sha256 is None):
        raise BenchmarkError(f"window {entry.id!r} is not frozen; run `python main.py benchmark freeze "
                             f"--window {entry.id}` after labelling")
    for name, rel, expected in (("items", entry.items_file, entry.items_sha256),
                                ("labels", entry.labels_file, entry.labels_sha256 if need_labels else None)):
        if expected is None:
            continue
        actual = sha256_file(root / rel)
        if actual != expected:
            raise BenchmarkError(f"window {entry.id!r}: {name} file {rel} changed since it was frozen "
                                 f"(sha256 {actual[:12]}… != {expected[:12]}…)")


# --- gold pair labels ------------------------------------------------------------------------

class Gold:
    """Pair and development lookups derived from a window's labels."""

    def __init__(self, labels: WindowLabels, items: list[BenchmarkItem]):
        self.labels = labels
        self.dev_of: dict[str, str] = {m: d.id for d in labels.developments for m in d.members}
        self.storyline = {d.id: d.storyline for d in labels.developments}
        self.developments = {d.id: d.members for d in labels.developments}
        self.source = {i.id: i.source for i in items}
        key = lambda a, b: (a, b) if a < b else (b, a)       # noqa: E731
        self.related = {key(p[0], p[1]) for p in labels.related_pairs}
        self.uncertain = {key(p[0], p[1]) for p in labels.uncertain_pairs}
        self._key = key

    def label(self, a: str, b: str) -> PairLabel:
        k = self._key(a, b)
        if k in self.uncertain:
            return PairLabel.UNCERTAIN
        da, db = self.dev_of.get(a), self.dev_of.get(b)
        if da is not None and da == db:
            return PairLabel.SAME
        if k in self.related:
            return PairLabel.RELATED
        if da and db and self.storyline.get(da) and self.storyline.get(da) == self.storyline.get(db):
            return PairLabel.RELATED
        return PairLabel.UNRELATED

    def multi_item_developments(self) -> dict[str, list[str]]:
        return {d: m for d, m in self.developments.items() if len(m) >= 2}

    def same_pairs(self) -> set[tuple[str, str]]:
        return {self._key(a, b) for m in self.developments.values() for a, b in combinations(m, 2)}


def freeze_window(window_id: str, root: Path = BENCHMARK_DIR, items_only: bool = False,
                  refreeze: bool = False) -> WindowEntry:
    """Record the SHA-256 of a window's items (and, unless items_only, its labels).

    Freeze items right after import, before labelling or replaying; freeze labels once
    labelling is finished. Changing a frozen hash needs ``refreeze`` and is visible in Git."""
    manifest = load_manifest(root)
    entry = manifest.window(window_id)
    items_path, labels_path = root / entry.items_file, root / entry.labels_file
    items = load_items(items_path)
    items_hash = sha256_file(items_path)
    if entry.items_sha256 and entry.items_sha256 != items_hash and not refreeze:
        raise BenchmarkError(f"window {window_id!r}: items changed since they were frozen; "
                             "pass --refreeze only if the change is deliberate")
    entry.items_sha256 = items_hash
    if not items_only:
        labels = load_labels(labels_path, items)
        if not labels.labelled_by:
            raise BenchmarkError(f"{labels_path}: set `labelled_by` before freezing labels")
        labels_hash = sha256_file(labels_path)
        if entry.labels_sha256 and entry.labels_sha256 != labels_hash and not refreeze:
            raise BenchmarkError(f"window {window_id!r}: labels changed since they were frozen; "
                                 "pass --refreeze only if the change is deliberate")
        entry.labels_sha256 = labels_hash
    entry.frozen_at = datetime.utcnow().replace(microsecond=0)
    write_manifest(root / "manifest.yaml", manifest)
    return entry


def label_sheet(window_id: str, root: Path = BENCHMARK_DIR) -> str:
    """Items in publication order with no similarity or clustering information, for blind labelling."""
    entry = load_manifest(root).window(window_id)
    lines = [f"# {window_id} ({entry.split.value}): {entry.start} .. {entry.end}, labels -> {entry.labels_file}"]
    for i in load_items(root / entry.items_file):
        lines.append(f"{i.id}  {i.published_at:%m-%d %H:%M}  [{i.source}]  {i.title}")
        if i.excerpt:
            lines.append(f"      {i.excerpt[:220]}")
    return "\n".join(lines)
