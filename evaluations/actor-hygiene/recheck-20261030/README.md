# Candidate B final readiness pass (2026-10-30, against the new `main`)

`main` (`3fa650d` = `production-stable-20261030` plus the supervisor scripts) was merged into `fix/actor-hygiene`
(`f91a671`, no conflict). Every gate was rerun on the merged code. The comparison baseline is the same gate run on `main`.

## Gates

| Gate | Result |
|---|---|
| Scope against `main` | The 6 files of the readiness note only: `nlp.py`, `entity_resolver.py`, `principals.py`, `pipeline.py` (1 line), `models.py` (in-memory field), `scripts/repair_entity_names.py`. No frontend, workspace, user-state or provenance code |
| Schema | No change: `core/migrations.py` and `core/database.py` are identical to `main` (head 6) |
| Targeted tests | `test_actor_hygiene`, `test_entity_resolution`, `test_situations`: 122 passed |
| Full pytest | 727 passed, 3 xfailed |
| Entity benchmark (gold rev 3) | No unit changed against `main`; identical metric table. One unscored prediction differs: a bare "Macron" beside "Emmanuel Macron" is typed PERSON (was ORG). That is the surname rule as intended |
| Identity gold check | Passed (checks 1-6; revision 2; holdout untouched) |
| Phase 2 identity (development windows) | 43/65, 43/58, 22/100, 15/58, 16/19, 12/31; 0 duplicate memberships. **Identical** to the 2026-10-16 gate (`runs/phase2-dev-actor-hygiene-recheck-20261030.json`) |
| Defect replay (`gate_replay.py`, frozen snapshot; sha unchanged) | 15 of 99 Developments change principals. Exactly 4 Situations lose support: `christa-pike-pike` 2/2 -> 0/2, `donald-j-trump-united-states` 3/3 -> 0/3, `elon-musk-musk` 1/2 -> 0/2, `rachel-simon` 1/2 -> 0/2. No Development gains an actor key. Identical to `../../entities/defects/2026-10-16/RESULTS.md` |

## Live repair dry run (nothing applied)

- **Input:** a fresh backup-API copy of the live DB, taken 2026-10-30 12:29Z from a `mode=ro` source. It held 1,118 Developments and 29 Situations.
- **Scope:** the copy and its outputs stay outside the repository.

**Situations.** The four target Situations are still open and two have grown since the 10-16 gate:

| Situation | Status | Primary actors | Developments now | At the 10-16 gate |
|---|---|---|---|---|
| `elon-musk-musk` | active | Elon Musk, Musk | 5 | 2 |
| `donald-j-trump-united-states` | active | Donald J. Trump, United States | 7 | 3 |
| `rachel-simon` | dormant | Rachel, Simon | 2 | 2 |
| `christa-pike-pike` | dormant | Christa Pike, Pike | 2 | 2 |

**`scripts/repair_situations.py` dry run** (`repair-situations-dryrun.json`): "no invalid created Situations", under both
`main` and Candidate B.
- The script judges stored primary-actor names with the actor normaliser. None of the four fails that test:
  - "Musk", "Pike", "Rachel" and "Simon" stay distinct actor names;
  - "Donald J. Trump" and "United States" are two actors.
- Candidate B removes the cause (the principals a Development gets), not the stored names. So each repair needs its own
  detection rule, a dry run and an approval before anything is applied, as the readiness note anticipated.

**Defect in the script, pre-existing and also on `main`:** `occurrence_reason` reads `policy.founder_same_occurrence_hours`.
That field went with the founder-guard split (`d12550d`, branch `feat/situation-founder-guard`), so every run raises
`AttributeError`.
- The dry run here used `dryrun_situations.py`, which supplies the production value (`None`, guard off) and refuses
  `--apply`.
- A one-line fix (`getattr(..., None)`) belongs with the first Situation repair, under its own approval.

**`scripts/repair_entity_names.py` dry run** (`repair-entity-names-dryrun.json`):
- **579 safe renames:** a stale possessive, quote or HTML entity, where the clean name is free.
- **80 collisions, reported and never merged.** Examples: `Israel&#039;s` and `Israel`, `Hamas&#039;s` and `Hamas`,
  `Renee Good’s` and `Renee Good&#039;s`.
- **Console encoding:** on a cp1252 console the report needs `PYTHONIOENCODING=utf-8` (a non-Latin-1 name raises
  `UnicodeEncodeError` when printed).
- **Not applied.** It is a separate approved step.

## Verdict

The gates are unchanged and green against the new `main`. Candidate B is ready for the deployment runbook. The
repairs stay separate, one by one.
