# Candidate B (actor hygiene): readiness note

Prepared 2026-10-27, during the Candidate A soak. **Not deployed, not tagged, not merged** with `feat/run-timing`.
Deploy only after Candidate A's soak and timing baseline, on separate owner approval (deploy order of 2026-10-27).

| | |
|---|---|
| Branch / SHA | `fix/actor-hygiene` at **`79b7892`**: fix `b1f1ee9`, Phase 2 gate run `79b7892`. Clean and pushed (`origin/fix/actor-hygiene` = `79b7892`) |
| Base | `production-stable-20261016` (`3eda6d0`). Merges cleanly with Candidate A `adacb83` (both touch `pipeline.py` in different places: `git merge-tree` shows no conflict) |
| Database schema | **No change.** No migration, `core/database.py` untouched. `core/models.py` gains one optional field on the in-memory `ExtractedEntity` (`refers_to`), not a database column |
| Tests | 714 passed / 3 xfailed at the gate (2026-10-16). Re-run 2026-10-27, lightweight only: `test_actor_hygiene`, `test_entity_resolution`, `test_situations`: 122 passed |
| Evaluation | All green on 2026-10-16 (`evaluations/entities/defects/2026-10-16/RESULTS.md`): entity benchmark (gold rev 3) no unit changed; identity gold check passed; Phase 2 identity identical to stable (43/65, 43/58, 22/100, 15/58, 16/19, 12/31); smoke passed; D1/D2 expectations met; Situation re-derivation: only 4 actor-identity-defect Situations lose support; no new actor merges |

## Code files changed (against `3eda6d0`)

| File | Change |
|---|---|
| `osint_monitor/processors/nlp.py` | `ner_text` (headline and body as separate sentences); `storm_names` (named storms, en/es/it); `_link_surnames` (a bare surname resolves to the full name in the same item, only when exactly one person there has it) |
| `osint_monitor/processors/entity_resolver.py` | resolves a mention through `refers_to` (never stored as an alias) |
| `osint_monitor/processors/principals.py` | storm names are not actor candidates; one actor, one identity among a Development's principals (entities normalising to a different actor than the best match are not flagged principal) |
| `osint_monitor/processors/pipeline.py` | the item's NER input uses `ner_text` |
| `osint_monitor/core/models.py` | `ExtractedEntity.refers_to` (optional) |
| `scripts/repair_entity_names.py` | new; dry-run by default; not run by any deploy step |
| tests, evaluation artifacts | `tests/test_actor_hygiene.py`; `evaluations/entities/defects/2026-10-16/`; Phase 2 run outputs |

## Expected live effects after deploy (new items only)

- No more headline/body glued names ("Elon Musk jab Musk", "Musk Anduril").
- Bare surnames resolve to the person the same item names in full (also Trump to Donald Trump, Collins to Susan
  Collins, and so on). Ambiguous surnames stay unlinked; there is no global surname alias.
- Storm names become storm events, not PERSON entities or actors.
- Principal flags change only where two entities matched one holder but normalised to different actors.
  - In the 2026-10-16 replay this affected 15 of 99 Situation Developments.
  - It dropped polluted or duplicate entities: `Ukraine&#039;s`, `Southwest Syria`, `Zacharia`.
  - Borderline: `Israel` beside `Ejército de Israel` in Development 400.
- **Existing Situations are not changed by the deploy.** Situations are sticky; the defect Situations stay until a
  separate repair.
- Entity rows already stored keep their names. The stale-name script is separate (below).

## Repair actions that remain separately gated (not part of the deploy)

Each needs a fresh live snapshot, a dry run, review of the exact proposed changes, separate approval, a backup, apply,
and post-repair integrity checks:

1. Retire `elon-musk-musk`: D1, one person counted twice.
2. Retire `rachel-simon`: D2, storms counted as people.
3. Retire `christa-pike-pike`: same class as D1, a person and her own surname.
4. Retire `donald-j-trump-united-states`: `DONALD J. TRUMP` and `Trump`, one person who represents the United States.
5. Stale canonical names: `scripts/repair_entity_names.py --db <snapshot>` dry run first. It renames only when the
   clean name is free, and reports collisions without merging them.

The current repair script (`scripts/repair_situations.py`) retires Situations whose actor identity is invalid under
the actor normaliser. Whether it detects cases 1-4 under the new code must be confirmed by its dry run after deploy;
`donald-j-trump-united-states` may need the normaliser to read `DONALD J. TRUMP` as Trump.

## Gate for the deploy itself

The deployment runbook as for Candidate A (HOLD, backups, migrate expecting no delta, launcher start, re-pin, C1 / ~2 h
/ C2), plus at C2:
- the entity-type mix of new items (no PERSON storm names; no glued spans);
- principal-flag churn on Developments updated during the soak;
- no Situation created from a surname or storm pair.
