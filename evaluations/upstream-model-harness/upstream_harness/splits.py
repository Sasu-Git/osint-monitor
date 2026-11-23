"""Split handling: verified split, phase guard (no acceptance cases during calibration), acceptance-once lock."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

from .checker import split_problems
from .common import now_utc
from .gold import GoldError, GoldTrack


class AcceptanceInCalibration(GoldError):
    pass


class AcceptanceAlreadyScored(GoldError):
    pass


class SplitGuard:
    """Gives out only the case ids and labels of one phase.

    phase "calibration" -> development cases only; acceptance ids are unreachable (asking for one raises).
    phase "acceptance"  -> acceptance cases only.
    """

    def __init__(self, gold: GoldTrack, phase: str):
        if phase not in ("calibration", "acceptance"):
            raise ValueError(phase)
        bad = split_problems(gold.root, gold)
        if bad:
            raise GoldError("split not verified: " + "; ".join(bad[:5]))
        self.gold, self.phase = gold, phase
        self._ids = gold.split_ids("development" if phase == "calibration" else "acceptance")
        self._forbidden = set(gold.split_ids("acceptance")) if phase == "calibration" else set()

    @property
    def case_ids(self) -> list[int]:
        return list(self._ids)

    def check_id(self, i: int) -> int:
        if i in self._forbidden:
            raise AcceptanceInCalibration(f"D{i} is an acceptance case; refused during calibration")
        if i not in self._ids:
            raise GoldError(f"D{i} is not in the {self.phase} set")
        return i

    def labels(self, basis: str) -> dict[int, dict]:
        """basis: "primary" (first answers) or "secondary" (final answers); restricted to this phase's cases."""
        src = self.gold.load_primary() if basis == "primary" else self.gold.load_final()
        return {i: src[i] for i in self._ids if i in src}


def _safe(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name)


def acquire_acceptance_lock(lock_dir: Path, track: str, model_id: str, meta: dict, force_rescore: bool = False,
                            force_reason: str | None = None) -> Path:
    """Create the one-shot lock for (track, model_id) atomically. A second attempt raises unless force_rescore, in which
    case it is appended to ``rescore-log.jsonl`` (with the reason) and allowed. The lock is taken before scoring, so a
    crashed first attempt still counts as the one attempt."""
    lock_dir = Path(lock_dir) / track
    lock_dir.mkdir(parents=True, exist_ok=True)
    path = lock_dir / f"{_safe(model_id)}.lock.json"
    rec = {"track": track, "model_id": model_id, "locked_at": now_utc(), **meta}
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        if not force_rescore:
            first = json.loads(path.read_text(encoding="utf-8"))
            raise AcceptanceAlreadyScored(
                f"acceptance for {track}/{model_id} already scored at {first.get('locked_at')}; "
                "a second scoring requires --force-rescore (logged)") from None
        with open(lock_dir / "rescore-log.jsonl", "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({**rec, "forced": True, "reason": force_reason}, ensure_ascii=False) + "\n")
        return path
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    return path
