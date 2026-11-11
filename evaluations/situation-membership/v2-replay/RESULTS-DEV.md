# Situation v2 candidate: development replay on the 126-case diagnostic set (2026-11-11)

**Development evidence only, not acceptance.** The 126 cases informed the design (`LEARNINGS.md`). This replay
measures how the frozen contract (`CONTRACT-V2-R2.md`, `bf57ed7`) behaves when implemented. Nothing below was used to
change a rule, and no rule was changed after the replay.

**Code.** `feat/situation-membership-v2-candidate` on top of the normalisation prerequisite
(`feat/actor-normalization-v2pre` `b695aa0`):
- `osint_monitor/processors/situations/v2.py`: pure rules, not wired into the pipeline;
- `replay_v2.py`;
- `score_dev.py`, which uses the frozen metric code;
- `tests/test_situation_v2.py` (9 tests, passing).

The replay ran on a backup-API copy of `snap-20261102.db`. It is blind to the labels (it reads the case key and the
founders only).

**How the replay rebuilds Situations.**
- **Seeded Situations:** taken from `config/situations.yaml`.
- **Automatic Situations:** each runtime Situation is rebuilt the way v2 would create it from its own founders (the
  `scopes.json` founders, judged with v2 features). Its anchors come from the stored primary actors, re-normalised.
- **Two variants:** founder-derived scope, and the OD7 overrides mapped by a proposed word and gazetteer mapping. The
  two variants gave identical decisions.
- **Limitation:** creation is not simulated chronologically over all Developments, so v2 Situations that would form
  later from non-founders are missing. The mixed-Development flag and the geolocation event country are not available
  on `main` (§0 preconditions): E5 never fires, and the event country is the single country of the specific places, or
  none.

## Results (same frozen metrics as the 126-case score)

| | Runtime, blind | v2, blind | Runtime, final | v2, final |
|---|---|---|---|---|
| MEMBER recall | 47/58 | **9/58** | 48/56 | **10/56** |
| MEMBER precision | 47/69 | 9/12 | 48/69 | 10/12 |
| NOT_MEMBER rejected | 0.75 | 1.00 | 0.71 | 1.00 |
| CONTEXT rejected | 0.14 | 0.71 | 0.20 | 0.80 |
| OTHER_SITUATION rejected | 0.63 | 0.96 | 0.67 | 0.96 |
| positive seeds lost | 0 | **6** | 0 | **6** |

The rejection side is fixed. Recall collapses, and 6 positive seeds of `russia-ukraine-war` are lost.

## Remaining failures by root cause (final labels; 46 missed members, 2 wrong admissions)

| Class | Cases | Root cause | Kind |
|---|---|---|---|
| Situation not rebuilt: no two founders share parties and a family | 14 | 35% of founders have no family (classifier `unknown`). Topic split (OD4) with only two founders. Re-derived principals lack the second party (`nato-russia` founders: `russia` only) | upstream classifier + principal extraction; OD4 interaction |
| Situation not rebuilt: single party | 7 | generic single party excluded (OD1/OD6: Macron → France, Democrat → United States, Long March → China); single-party founders without family or event country | contract (OD1/OD6) + upstream |
| `GENERIC_ANCHOR_ONLY` on seeded Situations | 9 | seeded Situations have **no families** in `situations.yaml`, so the OD6 strong match (family in scope) can never hold. Russian strikes on Dnipro with principal `Russia` only are rejected. This causes the 6 lost seeds | **contract gap** (seeded scope) |
| `NO_SCOPE_SIGNAL` at full coverage | 7 | OD5 requires a signal; seeded Situations have only keywords and anchor countries; places such as `rostov oblast`, `azov`, `black sea` resolve to no country | contract gap (seeded scope) + upstream gazetteer coverage |
| `LOW_COVERAGE` | 4 | place scope of a seeded Situation with a non-country party has no place for it (`gaza-ceasefire`: Hamas, so Gaza / Palestine is out of scope); second party not extracted | contract gap (seeded place scope) + principal extraction |
| `OUT_OF_SCOPE_DOMAIN` | 2 | frozen scope narrower than the owner's labels (`china-united-states` = diplomacy; trade members rejected) | scope (D5 / OD7 as written) |
| `NO_SHARED_ACTORS` | 2 | principals missing or wrong (`g20`; panda names) | principal extraction |
| `PENDING_ATTRIBUTION` | 1 | a hedge term on a confirmed member | hedge lexicon (DEF) |
| Wrong admissions | 2 | S166: merged Development (Pope headline, summit reports; no mixed flag on `main`). S307: testimony with a report-style headline | segmentation + commentary detection (upstream) |

## Verdict

**Not ready to freeze the code. Do not open the 14-day window.** The membership rules reject well. What fails is
mainly:
- missing seeded scope (a contract gap);
- the creation rules meeting an unreliable event-type classifier;
- upstream extraction and place coverage.

None of this is fixed by case rules.

**Needed before a code freeze** (owner decisions or upstream tracks, each before the window opens):
1. **Seeded scope amendment:** topic families and place scopes for the five seeded Situations, owner-written
   (allowed by D5 and contract §1.5).
2. **The `unknown` family:** about 30% of Developments have it. Either an upstream classifier fix, or an amendment
   saying how unknown-family founders and members are treated under OD4/OD5.
3. **OD1 with OD6:** single-party processes on a generic party (for example US domestic politics) have no home under
   the current definitions.
4. **Gazetteer coverage** for sub-national places and seas used for place scope (upstream).
5. **Replay fidelity:** a chronological creation simulation over all Developments before any code freeze.
