# Chronological replay instrument for the Situation v2 resume decision

An instrument, not a result. Situation v2 stays paused; its frozen contract (`CONTRACT-V2-R2`, amendment 1) is not
changed; no membership rule is tuned and no threshold is chosen here. Nothing in this directory is evidence about v2.

## What it does

Replays every Development of a snapshot **copy** in chronological order (`first_reported_at`, ties by Development id)
through the pinned v2 engine (`engine/situation_v2_4f4f85d.py`, an unmodified copy of the candidate at `4f4f85d`).
Each step decides the Development against the open Situations (seeded, plus those v2 creates: actor-process,
single-party, hazard), pools unassigned Developments by creation key, creates Situations and assigns pooled ones, as
the engine's own `chronological` does. `driver.step_replay` is that loop with trace hooks only; every run re-runs the
engine's `chronological` on the same features and records whether assignments, created Situations and per-step
decisions are equal (`engine_parity` in `summary.json` and `manifest.json`).

### Providers (the four upstream inputs)

| Role | Stored now | Model, later |
|---|---|---|
| `topic` | family from `events.event_type` (contract 1.1 mapping) | frozen predictions JSONL: `topic_family`, `confidence`, `abstain_reason` (event-topic SPEC section 1) |
| `location` | specific places from item entities + gazetteer containment, interim event country | frozen predictions JSONL: `event_location`, `event_country`, `target_location`, `places[{place,country,role}]`, `confidence` (event-location SPEC section 1) |
| `principals` | `event_entities.is_principal`, canonical parties | optional JSONL: `principal_parties` |
| `components` | `report-components-v1` JSONL (read-only, pinned copy) | n/a |

A model provider reads `<name>.jsonl` (one object per line, key `development_id`, no duplicates) and its sidecar
`<name>.jsonl.meta.json`:

```json
{"model_id": "...", "predictions_sha256": "<sha256 of the jsonl>", "spec_ref": "...",
 "acceptance_eval": {"record_path": "<relative to the sidecar>", "record_sha256": "<sha256 of that record>"}}
```

The eval record is JSON with `model_id`, `predictions_sha256` and `acceptance: {"scored": true, ...}`. Providers never
compute anything: model output is consumed only as stored. Consumption rules (choices, see "Open choices"): topic
family only when it is a v2 family and confidence is `high` or `medium` (owner ruling T3); location places only from the
`event` and `target` roles and only at `high`/`medium` confidence. The raw record stays visible in the trace.

The owner's V4 condition (at least two report components of at least two items each) is derived on read from the
component evidence and is never stored as a field. `--mixed-from v4` (default) feeds it to the engine's `mixed` flag
(E5, `PENDING_MIXED`); `--mixed-from none` leaves the flag unset, as the earlier diagnostic replay did.

## Run

```bash
HF_HUB_OFFLINE=1 PYTHONPATH=<this worktree> <main checkout>/.venv/Scripts/python.exe \
  evaluations/situation-membership/chrono-replay-v1/run_replay.py \
  --snapshot <main checkout>/data/eval/upstream-gold-20261123/gold-snap.db \
  --evalset-dir <frozen eval set> --out-root <dir>        # smoke, first 50 Developments
```

The snapshot sha256 (default: the pinned gold snapshot, `7463859a...`) is verified first and a mismatch stops the run.
The snapshot is opened read-only and a backup-API copy in a temporary directory (`query_only`) is used; the temporary
copy is deleted afterwards. `--evalset-dir` is a checkout of the frozen eval set
(`origin/design/situation-membership-v2-r2`, `evaluations/situation-membership/evalset`); `cases.json`, `key.json`,
`scopes.json` and `subsample/manifest.json` are verified against `PINS.json` (a smoke run needs only these four files).
The eval set was built on the 2026-11-02 snapshot; every run reports how many of its Developments are present with the
same headline and first-report time in the replayed snapshot (`eval_set.alignment`).

Smoke (default): `--limit` (default 50) Developments, stored providers, output directory `SMOKE-NOT-A-RESULT-<run id>`,
`NOT-A-RESULT.txt`, `status: "SMOKE / NOT A RESULT"` in every file, **no label read**. It writes:

| File | Content |
|---|---|
| `trace.jsonl` | one row per Development: id, time, inputs (base text features, each provider's value and provenance, derived V4 and `mixed`), open Situations, each candidate's outcome, reason and compact evidence, creation attempts (key, pool size, founded), retro assignments, decision, final assignment, reason |
| `summary.json` | structural counts only (assignments, row reasons, creations by mode, input coverage), engine parity, eval-set alignment |
| `case-decisions.json` | decisions for the eval-set cases inside the window, in the frozen scorer's candidate format |
| `manifest.json` | git sha and dirty flag, snapshot sha, provider ids and hashes, config hashes, pins, seed (none: no randomness), timestamps |

`trace.jsonl`, `summary.json` and `case-decisions.json` hold no wall-clock time or temporary path: a rerun on the same
inputs is byte-identical (tested). `manifest.json` differs only in `started_utc` / `finished_utc`.

## What final requires

`--mode final` refuses (exit with `REFUSED` and the list of problems) before touching the snapshot unless **all** hold:

1. `--topic` and `--location` are frozen model predictions files (stored values cannot stand in), each with a
   verified sidecar hash and an acceptance-evaluation record that exists, hashes as the sidecar says, names the same
   `model_id` and `predictions_sha256`, and shows `acceptance.scored: true`. The record's numbers are not judged here.
2. `--owner-approved <reference>`: a specific reference (at least 8 characters, not a placeholder such as `yes`).
3. The full window (no `--limit`), the frozen labels (`subsample/LABELS-FREEZE-subsample.json`) present in
   `--evalset-dir`, and a clean git tree (the `runs/` directory is excluded from that check).

Only final mode loads the frozen owner labels (through the frozen scorer's own loader in `--evalset-dir`).

## What it measures (final mode, computed by code, no verdict)

On the 126 diagnostic cases: MEMBER recall and precision (owner `AMBIGUOUS` excluded, as in the frozen scorer), false
joins (admitted cases whose owner label is not `MEMBER`, with the label breakdown), per-label rejection of non-member
labels, positive-seed regressions, and the share of runtime automatic Situations that gained a v2 counterpart
(creations), plus creations by mode for the whole replay. The PROPOSED gates of the preregistration are not applied;
a metric with no approved or PROPOSED threshold is reported without a verdict. `case-decisions.json` can be fed to
the frozen `score.py` / `score_subsample.py` unchanged. The 126-case set is diagnostic, not acceptance.

## Open choices (left for the owner or the final-run brief)

- Whether `mixed` = derived V4 (default) or unset; the component evidence file was declared "no downstream use" by the
  owner on 2026-11-23, so using it as the E5 flag is a decision.
- Ordering key: `events.first_reported_at` (row creation, i.e. processing time), not source publication time.
- Model consumption rules above (T3 confidence classes; event/target roles only; `out_of_scope` as no family).
- Hazard family stays text-derived from headlines and leads (contract 1.4 lexicon), not a topic-model output.
- The replay snapshot differs from the one the eval set was built on; alignment is reported, not enforced.
- Stored place containment uses the worktree's `config/geography.yaml` (hash in the manifest), not the 86 parent entries
  of `fix/v2-upstream-places`.

## Files

`PINS.json` (hashes of every pinned input), `engine/`, `inputs/` (seeded scopes v1, component evidence), `chrono_replay/`
(`providers`, `driver`, `guard`, `metrics`, `runner`, `snapshot`), `run_replay.py`, tests in
`tests/test_chrono_replay_v1.py`, `runs/` (committed smoke output).
