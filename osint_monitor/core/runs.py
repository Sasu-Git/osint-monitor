"""Pipeline run ledger (audit Phase 1): every daemon tier tick and one-shot run is a ``PipelineRun`` row with an
opaque UUID, its start/finish, per-stage outcome and the code / config / model versions it ran with.

While a run is active, its id is the *current run* (a context variable, so concurrent tier threads each see
their own). Writers stamp it as facts, without interpreting them:

- ``raw_items.ingested_run_id``: the run that stored the item;
- ``event_items.added_run_id`` / ``added_at``: the run and time a membership was created.

Later logic can then tell apart a newly ingested item, an existing item newly attached to a Development, and
reprocessing that created no membership at all. Phase 1 records; nothing reads these fields for decisions.
"""

from __future__ import annotations

import contextvars
import hashlib
import subprocess
import uuid
from datetime import datetime
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"

_current_run: contextvars.ContextVar[str | None] = contextvars.ContextVar("pipeline_run", default=None)


def current_run_id() -> str | None:
    return _current_run.get()


def new_run_id() -> str:
    return uuid.uuid4().hex


@lru_cache(maxsize=1)
def code_version() -> tuple[str | None, bool | None]:
    """(git HEAD sha, working tree has uncommitted changes to tracked files), or (None, None) outside git."""
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True,
                             timeout=10).stdout.strip() or None
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=REPO_ROOT,
                               capture_output=True, text=True, timeout=10).stdout.strip() != ""
        return sha, (dirty if sha else None)
    except (OSError, subprocess.SubprocessError):
        return None, None


def config_hash(config_dir: Path = CONFIG_DIR) -> str | None:
    """SHA-256 over every config file (relative path + bytes), in path order."""
    try:
        h = hashlib.sha256()
        for path in sorted(p for p in config_dir.rglob("*") if p.is_file()):
            h.update(path.relative_to(config_dir).as_posix().encode())
            h.update(b"\0")
            h.update(path.read_bytes())
        return h.hexdigest()
    except OSError:
        return None


def model_versions() -> dict:
    """NER model per language (with its installed state) and the embedding model."""
    from osint_monitor.core.config import get_settings
    from osint_monitor.processors.nlp import ner_status
    out = {f"ner_{lang}": f"{model} ({state})" for lang, (model, state) in ner_status().items()}
    out["embedding"] = get_settings().embedding_model
    return out


def start_run(session, kind: str, tier: str | None = None, started_at: datetime | None = None):
    """Create the run row (committed, status "running") and make it the current run. Returns (run, token)."""
    from osint_monitor.core.database import PipelineRun
    sha, dirty = code_version()
    run = PipelineRun(id=new_run_id(), kind=kind, tier=tier, started_at=started_at or datetime.utcnow(),
                      status="running", code_sha=sha, code_dirty=dirty, config_hash=config_hash(),
                      models=model_versions())
    session.add(run)
    session.commit()
    return run, _current_run.set(run.id)


def finish_run(session, run, token, stats: dict | None = None, items_collected: int | None = None,
               error: BaseException | None = None) -> None:
    """Record the outcome and end the current run. Status: failed on an exception, partial when a stage
    failed, else ok."""
    stats = stats or {}
    stages = stats.get("stages") or {}
    try:
        run.finished_at = datetime.utcnow()
        run.items_collected = items_collected
        run.items_new = stats.get("new_items")
        run.stages = dict(stages)
        if error is not None:
            run.status, run.error = "failed", f"{type(error).__name__}: {error}"[:2000]
        elif any(str(v).startswith("failed") for v in stages.values()):
            run.status = "partial"
        else:
            run.status = "ok"
        session.commit()
    finally:
        _current_run.reset(token)
