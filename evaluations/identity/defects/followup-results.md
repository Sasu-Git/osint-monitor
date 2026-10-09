# Identity follow-up: results (2026-10-09) — BLOCKED

Plan: `fix-plan.md` (pre-registered `6afe152`, amendment 1). Baseline: identity code `0eff3ea`, cross-language stage
disabled. Neither sealed holdout (relation holdout, multilingual identity holdout) was read.

## What was implemented

| rule | outcome |
|---|---|
| **T24**: a Development's reports span at most 24 h (a later report never continues it; new Developments group strongest links first while the group spans at most 24 h) | fixes 8 overmerges on development data, but **regresses the Phase 2 holdout**; implemented, **off** in `config/event_grouping.yaml` (`max_occurrence_span_hours: null`) |
| **P1**: an outlet's release links to its own Q&A / factsheet | **no effect**: the items link, but come from one outlet, so the single-source holdback keeps them below the Development layer; removed |

## Scores (T24 on, run `t24p1-v2`, against the baseline replays)

| gate | baseline | T24 | |
|---|---|---|---|
| frozen defect set (128) correct | 23 | **31** | 8 OVERMERGE fixed: D004 A002, D008 R013, D009 R029, D010 R060, D074 C115, D101-D103 Pike T012-T014; 0 broken |
| identity gold rev 4 (232 scored, development) correct | 157 | **161** | A002, A013, A023, C115 now apart (all DIFFERENT); 0 lost |
| Phase 2 development: continuity precision / recall | 42/63, 42/58 | 42/59, 42/58 | |
| split failures / merge failures | 21/100, 16/58 | **17/100**, 16/58 | |
| ID stability / mixed Developments | 15/19, 12/31 | 15/19, **9/29** | |
| duplicate membership / single-source Developments | 0, 0 | 0, 0 | invariants hold |
| **Phase 2 holdout** (regression check of the one-time scored holdout) | recall 7/10, ID stability 5/8 | **recall 5/10, ID stability 3/8** | **H003, H017 lost** |
| clustering benchmark (development) | | identical | |
| segmentation benchmark (development) | | identical (only the config field differs) | |
| entity benchmark | | no unit changed | |
| Situation impact (5-day window) | 78 Developments, 6 Situations | 83, 6 | 2 membership changes, all explained by Development changes; no Situation created or removed, no actor-set change |

First run `t24p1` (chronological span chunks) also broke control C114 (SAME): an unrelated earlier report anchored the
span. Amendment 1 replaced the chunking with strongest-link-first grouping under the span (`t24p1-v2`), which fixed it.

## Every changed gold case

- **A002** (DIFFERENT, Carney's two statements 39 h apart): the earlier Development cannot be continued 39 h later.
- **A013, A023** (DIFFERENT, West Bank settlement re-established / settler raids / activists): the baseline Development
  spanned 34.8 h; the later reports no longer continue it.
- **C115** (DIFFERENT, DW aviation sanctions vs the State Department release): the strongest links group the State
  Department release with the Kyiv Independent report (C114, SAME, kept); adding the earlier DW report would exceed
  24 h.
- **Holdout H003, H017** (SAME, the Nepal tunnel flood: a survivor's account 32-34 h after the rescue / death-toll
  reports): one occurrence reported beyond 24 h is cut. The contract counts follow-up factual updates as the same
  Development.

## Why it stops here

The overmerges T24 fixes are 31-41 h apart (A023 31.8 h, A002 39.1 h, Pike T012 41 h); the one-occurrence pairs it
breaks in the holdout are 32-34 h apart. No time threshold separates them, so the gain requires a recall regression on
held-out data. Per the owner's stop condition, T24 is not enabled.

## Remaining blockers (from the defect set)

| failure mode | cases | why no generalizable fix exists inside the constraints |
|---|---|---|
| cross-day storyline creep | Pike T040, Ebola A021/A022, French protests G07, Hormuz sequence (7) | time does not separate it from multi-day coverage of one occurrence (above); needs an action-level signal (what happened) rather than similarity or time |
| es/it overmerges and splits | C002 ... C112, 43 cross-language misses | the English-only clustering model carries no identity signal on Spanish and Italian text; needs a multilingual clustering model (a change beyond the rejected cross-language stage) |
| chains across a guard | C012, C037, C073, C094, C112, C115 | forbidding them costs as many correct merges (C011, C014, C030, C036, C043, C058, C077) |
| place-guard splits | FlyDubai C066, C092, C113; C005 | owner rule P7 (a place conflict is never outweighed) |
| sub-threshold and unclustered recall | B002, B004, C013, C064, G01 (0.52) | only a lower threshold, which is a precision trade |
| same-day distinct actions | Pope R046, Netanyahu R100, Malaysia T009, Xi visit B008 | no text signal separates them |
| one occurrence formed twice | U110, U131 | merging Developments breaks ID stability |
