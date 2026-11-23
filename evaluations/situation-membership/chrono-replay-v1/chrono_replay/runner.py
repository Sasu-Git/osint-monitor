"""Orchestration: run the driver, write trace, summary, case decisions and the manifest.

``execute`` is database-free (it takes bases, providers and seeded Situations), so tests can drive it with synthetic
inputs. The snapshot-specific wiring is in ``run_replay.py``.

Determinism: trace.jsonl, summary.json and case-decisions.json contain no wall-clock time, no temporary path and no
randomness (the instrument uses none), so a rerun on the same inputs is byte-identical. manifest.json carries the
timestamps and is the only file that differs between runs.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from . import metrics
from .driver import BaseDev, check_parity, step_replay, trace_lines
from .guard import SMOKE_LABEL, final_dir_name, smoke_dir_name
from .providers import Provider
from .util import dumps, sha256_text, write_json, write_lines

SMOKE_NOTE = ("SMOKE RUN, NOT A RESULT. Limited window, current stored-value providers or stubs, no label read. It "
              "proves the plumbing only and must not be cited as evidence about Situation v2.")


def run_id_of(identity: dict) -> str:
    return sha256_text(dumps(identity))[:12]


def execute(*, engine, bases: list[BaseDev], providers: dict[str, Provider], seeded_factory, party_countries,
            mode: str, limit: int | None, mixed_from: str, out_root: Path, identity: dict, manifest_extra: dict,
            evalset: dict | None = None, labels: dict | None = None, canon_keys=None) -> dict:
    from .driver import chronological_order
    ordered = chronological_order(bases)
    window = ordered[:limit] if limit is not None else ordered
    run_mode = "smoke" if mode == "smoke" else "final"
    ident = {**identity, "mode": mode, "limit": limit, "mixed_from": mixed_from,
             "providers": {r: p.describe() for r, p in sorted(providers.items())},
             "window_size": len(window), "first_dev": window[0].dev_id if window else None,
             "last_dev": window[-1].dev_id if window else None}
    run_id = run_id_of(ident)
    out = Path(out_root) / (smoke_dir_name(run_id) if mode == "smoke" else final_dir_name(run_id))
    started = datetime.now(timezone.utc)

    result = step_replay(engine, window, providers, seeded_factory(), party_countries,
                         run_mode=SMOKE_LABEL if mode == "smoke" else "FINAL", mixed_from=mixed_from)
    parity = check_parity(engine, result, seeded_factory, party_countries)
    result.parity = parity

    summary = {
        "status": SMOKE_LABEL if mode == "smoke" else "FINAL (owner-approved)",
        "note": SMOKE_NOTE if mode == "smoke" else "No verdict is computed here; gates are PROPOSED context only.",
        "run_id": run_id, "mode": mode, "limit": limit, "mixed_from": mixed_from,
        "contract_version": engine.CONTRACT_VERSION,
        "engine_parity": parity,
        "structural": metrics.structural_summary(result, len(bases)),
        "trace_rows": len(result.rows),
        "label_metrics": None if mode == "smoke" else {},
    }
    case_out = None
    if evalset is not None:
        cdec, cdet = metrics.case_decisions(result, evalset["key"], evalset["case_ids"], evalset["anchors_of"],
                                            evalset["founders_of"], engine.CONTRACT_VERSION)
        case_out = {"rule": f"situation-v2 candidate, chronological replay ({mode}), {engine.CONTRACT_VERSION}",
                    "status": summary["status"], "decisions": cdec, "details": cdet}
        summary["eval_set"] = {"cases_in_set": len(evalset["case_ids"]), "cases_decided": len(cdec),
                               "cases_not_replayed": len(cdet["not_replayed"]),
                               "alignment": evalset.get("alignment")}
        if mode == "final":
            if labels is None:
                raise SystemExit("STOP: final mode needs the frozen labels")
            summary["label_metrics"] = {
                "membership": metrics.score_cases(cdec, labels, evalset["key"]),
                "creations": metrics.creation_match(result, evalset["scopes"], evalset["anchors_of"],
                                                    evalset["founders_of"]),
                "gates": "PROPOSED gates of PREREGISTRATION-V2-R2 are not applied by this instrument; no verdict."}

    write_lines(out / "trace.jsonl", trace_lines(result))
    write_json(out / "summary.json", summary)
    if case_out is not None:
        write_json(out / "case-decisions.json", case_out)
    if mode == "smoke":
        (out / "NOT-A-RESULT.txt").write_text(SMOKE_NOTE + "\n", encoding="utf-8", newline="\n")
    manifest = {**manifest_extra, "run_id": run_id, "mode": mode, "limit": limit, "seed": None,
                "seed_note": "no randomness is used by the driver or the engine",
                "mixed_from": mixed_from, "identity": ident,
                "providers": {r: p.describe() for r, p in sorted(providers.items())},
                "trace_sha256": sha256_text("\n".join(trace_lines(result)) + "\n"),
                "engine_parity": parity,
                "started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat()}
    write_json(out / "manifest.json", manifest)
    return {"out": out, "summary": summary, "result": result, "manifest": manifest}
