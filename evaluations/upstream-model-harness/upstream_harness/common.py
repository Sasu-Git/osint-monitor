"""Shared helpers: hashing, canonical JSON, run metadata."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

TRACKS = ("topic", "location")
PACKAGES = ("spacy", "en_core_web_lg", "es_core_news_md", "it_core_news_md", "numpy", "torch",
            "sentence-transformers", "transformers", "PyYAML")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path | str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text_lf(p: Path | str) -> str:
    """sha256 of a text file with CRLF folded to LF (frozen hashes are of LF content; Windows checkouts may use CRLF)."""
    return sha256_bytes(Path(p).read_bytes().replace(b"\r\n", b"\n"))


def canonical(obj) -> bytes:
    """Deterministic serialisation used for every content hash and cache file."""
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=1, allow_nan=False) + "\n").encode("utf-8")


def write_canonical(path: Path, obj) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    b = canonical(obj)
    path.write_bytes(b)
    return sha256_bytes(b)


def package_versions() -> dict:
    out = {"python": sys.version.split()[0]}
    for p in PACKAGES:
        try:
            out[p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            out[p] = None
    return out


def git_state(repo: Path) -> dict:
    def run(*a):
        r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    sha = run("rev-parse", "HEAD")
    dirty = run("status", "--porcelain")
    return {"git_sha": sha, "dirty": bool(dirty) if dirty is not None else None}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
