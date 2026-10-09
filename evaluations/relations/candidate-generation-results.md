# Phase 3 Session 1: candidate generation results (measured once, 2026-10-09)

Plan: `candidate-generation-plan.md` (`a381cc8`). Gold: revision 2 (`82bea89`). Replays: `runs-rev2/` (current code,
fixed replay clock). Summary: `runs-rev2/candidates-summary.json`. Nothing was changed after the measurement.

## Result: the gold is almost entirely outside the system's Developments

| | cases |
|---|---|
| scored gold cases | 173 |
| NOT_SURFACED (a side has no Development) | **149** |
| BLOCKED_BY_IDENTITY (both sides in one Development) | **22** |
| COVERED (a distinct Development pair exists) | **2** (both `NO_RELATION`) |

Canonical positives of the three runtime types:

| type | positives | COVERED | BLOCKED_BY_IDENTITY | NOT_SURFACED |
|---|---|---|---|---|
| `same_calamity_lifecycle` | 13 | 0 | 2 (R030, R082) | 11 |
| `same_convened_event` | 10 | 0 | 2 (R046, R100) | 8 |
| `reaction_to` | 7 | 0 | 2 (R014, T018) | 5 |

Candidate recall cannot be measured: no covered positive exists. Candidates on covered `NO_RELATION` cases: 0 of 2.

## Why

Only 407 of 1946 window items (21%) belong to any system Development. A Development needs a multi-item cluster, so a
lone article is never one, and most gold sides are lone articles: an explainer, a commentary, one outlet's report.

| window | items | in a Development |
|---|---|---|
| 2026-08-21 | 162 | 18 (11%) |
| 2026-08-31 | 166 | 12 (7%) |
| 2026-09-25 | 90 | 8 (9%) |
| 2026-09-27-live | 173 | 43 (25%) |
| 2026-09-29-live | 210 | 35 (17%) |
| 2026-09-30-multilingual | 392 | 81 (21%) |
| 2026-10-03-live | 753 | 210 (28%) |

Under the runtime contract (both endpoints are real Development IDs), a relation can only exist between two
multi-item Developments. On this data the relation layer could reach 2 of 173 gold cases.

Where both sides do reach the system, the larger problem is identity: whole calamity, visit and reaction sequences
fall into one Development (22 cases), so the pair the relation should connect does not exist.

## Candidate volume (for reference)

| window | Developments | pairs | candidates |
|---|---|---|---|
| 2026-08-21 | 7 | 21 | reaction_to 1 |
| 2026-08-31 | 5 | 10 | 0 |
| 2026-09-25 | 4 | 6 | 0 |
| 2026-09-27-live | 15 | 105 | same_convened_event 1 |
| 2026-09-29-live | 16 | 120 | reaction_to 1 |
| 2026-09-30-multilingual | 25 | 300 | reaction_to 1 |
| 2026-10-03-live | 52 | 1326 | reaction_to 18, same_convened_event 2 |

## Consequence

Tuning candidate generation is pointless until the unit question is settled. It is an owner decision, not a tuning
choice, because every option changes either the runtime contract or the Development identity contract.
