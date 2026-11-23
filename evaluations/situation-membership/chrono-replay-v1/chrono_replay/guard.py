"""Guards: the final run cannot happen by accident.

Final mode needs every one of:
  (a) a topic model predictions file AND a location model predictions file (frozen JSONL + sidecar, hash verified),
      each with an acceptance-evaluation record that exists, hashes as the sidecar says, names the same model id and
      predictions hash, and says ``acceptance.scored`` is true. The record's numbers are not judged here: no threshold
      is chosen by this instrument;
  (b) an explicit ``--owner-approved <reference>`` (non-empty, not a placeholder);
  (c) the full window (no ``--limit``), stored providers not standing in for the topic or location role, the frozen
      eval-set labels present, and a clean git tree.
Anything else is smoke: a limited window, labelled SMOKE / NOT A RESULT, no label read.
"""
from __future__ import annotations

from pathlib import Path

from .providers import FrozenPredictions

SMOKE_LABEL = "SMOKE / NOT A RESULT"
PLACEHOLDERS = {"", "yes", "true", "ok", "approved", "todo", "tbd", "x", "none", "n/a", "1"}


def acceptance_problems(role: str, pred: FrozenPredictions | None) -> list[str]:
    if pred is None:
        return [f"{role}: no model predictions file (stored values cannot stand in for the {role} model in final mode)"]
    out = []
    rec = pred.acceptance_record()
    if rec is None:
        return [f"{role}: no acceptance-evaluation record, or its sha256 differs from the sidecar's "
                f"(model {pred.model_id})"]
    path, body = rec
    acc = body.get("acceptance") or {}
    if acc.get("scored") is not True:
        out.append(f"{role}: eval record {path.name} does not show acceptance scored (acceptance.scored is not true)")
    if body.get("model_id") != pred.model_id:
        out.append(f"{role}: eval record model_id {body.get('model_id')!r} != predictions model_id {pred.model_id!r}")
    if body.get("predictions_sha256") != pred.sha256:
        out.append(f"{role}: eval record predictions_sha256 does not match the predictions file")
    return out


def final_problems(*, topic: FrozenPredictions | None, location: FrozenPredictions | None,
                   owner_approved: str | None, limit: int | None, evalset_labels_present: bool,
                   git_dirty: bool | None, mixed_from: str = "none") -> list[str]:
    problems = acceptance_problems("topic", topic) + acceptance_problems("location", location)
    ref = (owner_approved or "").strip()
    if ref.lower() in PLACEHOLDERS or len(ref) < 8:
        problems.append("no --owner-approved reference (a dated, specific reference to the owner's approval is required)")
    if limit is not None:
        problems.append("final mode runs the full window: --limit is not allowed")
    if not evalset_labels_present:
        problems.append("frozen eval-set labels (LABELS-FREEZE-subsample.json) not found in --evalset-dir")
    if mixed_from != "none":
        problems.append("component evidence is diagnostic only (owner 2026-11-23): final mode requires --mixed-from none")
    if git_dirty is not False:
        problems.append("git tree is dirty or its state is unknown: commit before a final run")
    return problems


def require_final(**kw) -> None:
    problems = final_problems(**kw)
    if problems:
        raise SystemExit("REFUSED: final mode not allowed.\n  - " + "\n  - ".join(problems)
                         + "\nRun without --mode final for a smoke run (limited window, labelled NOT A RESULT).")


def smoke_dir_name(run_id: str) -> str:
    return f"SMOKE-NOT-A-RESULT-{run_id}"


def final_dir_name(run_id: str) -> str:
    return f"FINAL-{run_id}"
