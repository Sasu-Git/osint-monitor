"""Deterministic feature extraction for the gold cases, from a read-only snapshot.

Per case: every member item (title, whitespace-collapsed lead, source, published_at, item language, headline kind,
whether the labeller was shown it), spaCy parses (title and lead) and multilingual sentence embeddings (title and
title + lead). NOT included, on purpose: stored event_type, summary, principals, location, situation or any other system
output, and the sampling stratum (derived from a stored type). The features file is canonical JSON with a content hash;
re-running on the same inputs gives byte-identical output.

    python -m upstream_harness.features --gold-root <dir> --track topic --snapshot <gold-snap.db> --out <features.json>
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

from .common import (TRACKS, canonical, package_versions, sha256_bytes, sha256_file, sha256_text_lf)
from .gold import GoldError, GoldTrack

SCHEMA = 1
LEAD_CHARS = 600
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBED_REVISION = "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
EMBED_BATCH = 16
EMBED_DECIMALS = 6
SPACY_MODELS = {"en": "en_core_web_lg", "es": "es_core_news_md", "it": "it_core_news_md"}


class SnapshotMismatch(GoldError):
    pass


def lead_text(content: str | None) -> str:
    return re.sub(r"\s+", " ", html.unescape(content or "")).strip()[:LEAD_CHARS]


@contextmanager
def snapshot_copy(snapshot: Path, expected_sha: str):
    """Verify the snapshot sha256, then yield a connection to a backup-API copy in a temp dir (snapshot opened ro)."""
    got = sha256_file(snapshot)
    if got != expected_sha:
        raise SnapshotMismatch(f"snapshot sha256 mismatch: {got} != {expected_sha}")
    tmp = Path(tempfile.mkdtemp(prefix="upstream-feat-"))
    try:
        src = sqlite3.connect(f"file:{Path(snapshot).as_posix()}?mode=ro", uri=True)
        db = sqlite3.connect(tmp / "copy.db")
        src.backup(db)
        src.close()
        yield db
        db.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- real parsers / embedders
class SpacyParser:
    def __init__(self):
        import spacy
        self._spacy = spacy
        self._nlp = {}

    def _get(self, lang):
        if lang not in self._nlp:
            self._nlp[lang] = self._spacy.load(SPACY_MODELS[lang])
        return self._nlp[lang]

    def info(self) -> dict:
        import importlib
        v = {"spacy": self._spacy.__version__}
        for m in SPACY_MODELS.values():
            v[m] = importlib.import_module(m).__version__
        return v

    def parse(self, text: str, lang: str):
        if lang not in SPACY_MODELS or not text:
            return None
        doc = self._get(lang)(text)
        return {"tokens": [[t.text, t.lemma_, t.pos_, t.dep_, t.head.i] for t in doc],
                "ents": [[e.text, e.label_, e.start, e.end] for e in doc.ents]}


class STEmbedder:
    def __init__(self, hub: Path | None = None):
        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        hub = Path(hub or os.environ.get("HF_HUB_CACHE") or Path.home() / ".cache" / "huggingface" / "hub")
        self.dir = hub / "models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2" / "snapshots" / EMBED_REVISION
        if not self.dir.is_dir():
            raise GoldError(f"embedding model revision {EMBED_REVISION} not cached at {self.dir} (no downloads)")
        self._model = None

    def info(self) -> dict:
        import sentence_transformers
        files = {str(p.relative_to(self.dir)).replace("\\", "/"): sha256_file(p)
                 for p in sorted(self.dir.rglob("*")) if p.is_file()}
        return {"model": EMBED_MODEL, "revision": EMBED_REVISION, "files_sha256": files,
                "sentence_transformers": sentence_transformers.__version__, "batch_size": EMBED_BATCH,
                "decimals": EMBED_DECIMALS, "normalized": False}

    def encode(self, texts: list[str]) -> list[list[float]]:
        import torch
        torch.set_num_threads(1)
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(str(self.dir), device="cpu")
        arr = self._model.encode(texts, batch_size=EMBED_BATCH, convert_to_numpy=True, show_progress_bar=False)
        return [[round(float(x), EMBED_DECIMALS) for x in row] for row in arr]


# ---------------------------------------------------------------- extraction
def _items(db, event_id: int):
    return db.execute(
        "select r.id, s.name, r.published_at, r.title, r.content from event_items ei"
        " join raw_items r on r.id = ei.item_id left join sources s on s.id = r.source_id"
        " where ei.event_id = ? order by r.id", (event_id,)).fetchall()


def build_features(gold_root: Path, track: str, db, parser, embedder, snapshot_sha: str) -> dict:
    from osint_monitor.processors.development_segmentation import headline_kind
    from osint_monitor.processors.language import item_language
    tr = GoldTrack(Path(gold_root), track)
    cases_in = tr.cases()
    cases, texts = {}, set()
    for i in sorted(cases_in):
        shown = {it["item_id"] for it in cases_in[i]["items"]}
        items, langs = [], {}
        for rid, source, pub, title, content in _items(db, i):
            lang = item_language(source, title or "")
            langs[lang] = langs.get(lang, 0) + 1
            items.append({"item_id": rid, "source": source, "published_at": pub, "title": title or "",
                          "lead": lead_text(content), "lang": lang, "headline_kind": headline_kind(title),
                          "shown_to_labeller": rid in shown})
        if len(items) != cases_in[i]["members"]:
            raise GoldError(f"D{i}: snapshot has {len(items)} items, case file says {cases_in[i]['members']}")
        if not items:
            raise GoldError(f"D{i}: no items in snapshot")
        dom = sorted(langs.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        for it in items:
            texts.add(it["title"])
            texts.add(f"{it['title']} {it['lead']}".strip())
        cases[str(i)] = {"development_id": i, "lang": dom, "members": len(items), "items": items}
    order = sorted(t for t in texts if t)
    vecs = dict(zip(order, embedder.encode(order))) if order else {}
    for c in cases.values():
        for it in c["items"]:
            it["parse"] = {"title": parser.parse(it["title"], it["lang"]),
                           "lead": parser.parse(it["lead"], it["lang"])}
            tl = f"{it['title']} {it['lead']}".strip()
            it["embedding"] = {"title": vecs.get(it["title"]), "title_lead": vecs.get(tl)}
    header = {"schema": SCHEMA, "track": track, "snapshot_sha256": snapshot_sha,
              "cases_json_sha256_lf": sha256_text_lf(tr.cases_path),
              "lead": f"html.unescape, whitespace-collapsed, first {LEAD_CHARS} chars of content",
              "spacy": parser.info(), "embedding": embedder.info(), "n_cases": len(cases),
              "excluded": ["event_type", "summary", "principals", "location", "situation", "sampling stratum"]}
    body = {"header": header, "cases": cases}
    body["content_hash"] = sha256_bytes(canonical({"header": header, "cases": cases}))
    return body


def write_features(body: dict, out: Path) -> str:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(canonical(body))
    return sha256_file(out)


def load_features(path: Path | str) -> dict:
    """Load a features file and verify its content hash."""
    body = json.loads(Path(path).read_text(encoding="utf-8"))
    want = sha256_bytes(canonical({"header": body["header"], "cases": body["cases"]}))
    if body.get("content_hash") != want:
        raise GoldError("features file content hash does not match its content")
    return body


def main(argv=None) -> int:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    ap = argparse.ArgumentParser(description="Extract deterministic features for the gold cases")
    ap.add_argument("--gold-root", required=True, type=Path)
    ap.add_argument("--track", required=True, choices=TRACKS)
    ap.add_argument("--snapshot", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    tr = GoldTrack(a.gold_root, a.track)
    expected = json.loads(tr.manifest_path.read_text(encoding="utf-8"))["snapshot_sha256"]
    with snapshot_copy(a.snapshot, expected) as db:
        body = build_features(a.gold_root, a.track, db, SpacyParser(), STEmbedder(), expected)
    file_sha = write_features(body, a.out)
    print(json.dumps({"out": str(a.out), "content_hash": body["content_hash"], "file_sha256": file_sha,
                      "cases": body["header"]["n_cases"], "snapshot_sha256": expected}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
