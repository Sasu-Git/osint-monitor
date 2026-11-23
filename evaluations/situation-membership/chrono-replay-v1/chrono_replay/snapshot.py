"""Snapshot handling and the osint-monitor-dependent parts (kept out of the driver so the driver stays testable).

The snapshot is opened read-only, its sha256 is verified first (mismatch stops the run), and the work happens on a
backup-API copy in a temporary directory opened with ``PRAGMA query_only=ON``. Nothing is ever written to the source.
"""
from __future__ import annotations

import importlib.util
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from .driver import BaseDev
from .util import HERE, sha256_file, verify


def load_engine(path: Path, expected_sha256: str):
    verify(path, expected_sha256, "pinned Situation v2 engine")
    spec = importlib.util.spec_from_file_location("situation_v2_pinned", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["situation_v2_pinned"] = mod       # dataclasses resolve their module through sys.modules
    spec.loader.exec_module(mod)
    return mod


def copy_snapshot(src: Path, expected_sha256: str, tmpdir: Path) -> tuple[sqlite3.Connection, Path]:
    verify(src, expected_sha256, "snapshot")
    dst_path = tmpdir / "copy.db"
    ro = sqlite3.connect(f"file:{Path(src).as_posix()}?mode=ro", uri=True)
    dst = sqlite3.connect(dst_path)
    ro.backup(dst)
    dst.close()
    ro.close()
    conn = sqlite3.connect(dst_path)
    conn.execute("PRAGMA query_only=ON")
    return conn, dst_path


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace(" ", "T")) if s else datetime.min


def load_bases(conn: sqlite3.Connection, engine, headline_kind, report_label: str, lead_fn) -> list[BaseDev]:
    """One BaseDev per Development with at least one member (the Developments the pipeline can decide on)."""
    items: dict[int, list[tuple[int, str, str]]] = {}
    for eid, rid, title, content in conn.execute(
            "SELECT ei.event_id, r.id, r.title, r.content FROM event_items ei JOIN raw_items r ON r.id = ei.item_id "
            "ORDER BY ei.event_id, r.id"):
        items.setdefault(eid, []).append((rid, title or "", content or ""))
    out = []
    for eid, summary, first in conn.execute("SELECT id, summary, first_reported_at FROM events ORDER BY id"):
        rows = items.get(eid)
        if not rows:
            continue
        titles = [t for _, t, _ in rows]
        head = next((r for r in rows if r[1] == (summary or "")), rows[0])
        lead = lead_fn(head[2]) or ""
        out.append(BaseDev(
            dev_id=eid, headline=summary or "", lead=lead, first_reported_at=parse_ts(first) if first else None,
            report_share=sum(1 for t in titles if headline_kind(t) == report_label) / len(titles),
            hazard=engine.hazard_of(titles + [lead_fn(c) or "" for _, _, c in rows]),
            hedges=engine.hedge_terms(f"{summary or ''} {lead}")))
    return out


def build_seeded(engine, seeded_meta: dict, seed_cfgs, canon, party_countries) -> list:
    seeded = []
    for seed in seed_cfgs:
        meta = seeded_meta.get(seed.slug, {})
        anchors = canon.keys(seed.primary_actors)
        seeded.append(engine.Situation2(
            seed.slug, "seeded", anchors, frozenset(meta.get("families", [])),
            frozenset(meta.get("place_scope", [])) or frozenset(party_countries(anchors)),
            keywords=tuple(seed.keywords), scope_source="seed_metadata_v1" if meta else "seed"))
    return seeded


def git_state(worktree: Path, exclude: list[str]) -> dict:
    def run(*a):
        return subprocess.run(["git", "-C", str(worktree), *a], capture_output=True, text=True, check=False)
    sha = run("rev-parse", "HEAD").stdout.strip() or None
    spec = [":(exclude)" + e for e in exclude]
    st = run("status", "--porcelain", "--", ".", *spec)
    dirty = None if st.returncode != 0 else bool(st.stdout.strip())
    return {"sha": sha, "dirty": dirty, "branch": run("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() or None}


def config_hashes(worktree: Path) -> dict:
    out = {}
    for rel in ("config/geography.yaml", "config/actors.yaml", "config/situations.yaml",
                "config/development_types.yaml", "config/event_grouping.yaml"):
        p = worktree / rel
        out[rel] = sha256_file(p) if p.exists() else None
    return out


def make_tmpdir() -> Path:
    return Path(tempfile.mkdtemp(prefix="chronoreplay-"))


def default_worktree() -> Path:
    return HERE.parent.parent.parent if (HERE.parent.parent.parent / "osint_monitor").exists() else Path.cwd()
