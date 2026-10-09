# Cross-language acceptance guard: pre-registered tuning plan

Status: **frozen before any logic change** (2026-10-09). Nothing in this file may be edited after the experiments
start; amendments go in a new, dated section at the end, with the reason, before the run they affect.

## 1. Starting point

Benchmark of the current stage (`processors/cross_language.py`, commit `f4d9212`) on identity gold revision 4,
development windows only, fixed replay harness (`runs/rev4-xlang-clock-scored.json`):

| | value |
|---|---|
| stage on, all 74 rev4 additions | P 0.41 / R 0.38 / F1 0.39 (tp 15 / fp 22 / fn 24) |
| merges the stage itself adds | 12 true, **20 false** (precision 0.375) |
| accepted links | 103 |
| regression cases | RAF Fairford G12, G13 and Siberian plague G14 pass only with the stage; R138 G02, G03 fail either way |

The 20 stage-added false merges, by the anchor that accepted the first link (from the link evidence):

| failure mode | cases | count |
|---|---|---|
| broad person/org anchor | V006, V013, V023, V027, V030, V041, V042, V049, V050, V055 (Bolsonaro / Flávio Bolsonaro / Lula); V004, V057 (Hamas); V017 (Houthis); V008, V018 (Sánchez); V025 (European Union) | 16 |
| broad place anchor | V015, V021 (Gaza); V037 (Irkutsk / Shelekhov ~ Siberia, by containment) | 3 (+ V004, V008 also share a place) |
| chaining | V036 (no direct link: merged through other accepted links) | 1 |

## 2. What is fixed during tuning

- The multilingual model (`paraphrase-multilingual-MiniLM-L12-v2`, pinned revision), its role (candidate generation
  only), the similarity floor `min_cosine: 0.60` and `max_hours: 24`. **The floor is not lowered** in any variant.
- Cosine alone never merges.
- The P7 place-conflict rejection.
- Every component outside the acceptance guard and the merge step: clustering, segmentation, Phase 2 identity
  logic, the GDELT headline-only rule, the gazetteer and `actors.yaml`. In particular, no names are added to
  `actors.yaml` or to any list because they appear in the failures above (adding Lula as a leader would fix ten cases
  by name; that is fitting to the development set, not a guard).
- Gold revision 4 and the replay harness at `f4d9212`.

## 3. Guard components (each behind a config flag, default = current behaviour)

Each component is implemented once, before any experiment runs, and is general, with no names or case IDs:

- **G1, two independent anchor classes.** Classes: *actor* (shared specific named entity), *place* (shared specific
  place), *number* (shared non-year number of 3+ digits). Accept only when the pair shares anchors from at least two
  classes: actor + place, actor + number or place + number. Date anchors are not extracted today; adding a date
  extractor is a new feature and is out of scope for this round.
- **G2, broad anchors are not decisive.** An anchor (actor or place) is *broad* when it occurs in more than `k` units
  of the same run (units = the segmented groups and singles the stage sees, all languages). A broad anchor still
  counts for nothing toward acceptance; it does not veto. This is data-driven (storyline-level frequency), not a
  blacklist. Pre-registered values: `k = 3` (one unit per language for one occurrence) and `k = 5`.
- **G3, direct pairwise support (no chaining).** Units merge only through a direct accepted link between them. A
  merged component of three or more units is kept only if every cross-language unit pair in it has an accepted
  link. Otherwise each unit keeps only its highest-cosine accepted link, and the rest are dropped. The
  same-language structure that segmentation produced is untouched.
- **G4, exact specific places only.** A place anchor requires the same canonical place on both sides. Containment
  (`irkutsk~siberia`) no longer counts as a match. Containment still prevents a place conflict, as today.

## 4. Experiments (the complete list; nothing else is run)

| id | components | targets |
|---|---|---|
| E0 | none (current stage) | baseline, rerun to confirm `rev4-xlang-clock` |
| E1 | G1 | broad person/org, broad place |
| E2a | G2 (k = 3) | broad person/org, broad place |
| E2b | G2 (k = 5) | as E2a, looser |
| E3 | G3 | chaining |
| E4 | G4 | broad place (containment) |
| E5 | G2 (best k from E2a/E2b by the selection rule below) + G3 + G4 | all three, single-anchor allowed |
| E6 | G1 + G3 + G4 | all three, two-class requirement |
| E7 | G1 + G2 (same k as E5) + G3 + G4 | all components |

Each experiment is one replay of the development windows holding rev4 additions (stage on, config changed in memory
only) plus one Phase 2 identity score with the stage on, and runs once. Single-component runs (E1–E4) diagnose; only
E5–E7 (and E1–E4 if they qualify) are candidates.

## 5. What is measured (development only)

For each experiment:

1. Rev4 additions (74 pairs): P / R / F1 stage on; stage-added true merges, stage-added false merges (with case IDs
   and the evidence of the accepting link); results by cosine band and by language pair.
2. Phase 2 identity gold (development windows), stage on vs stage off: any pair that changes. A DIFFERENT pair newly
   together is a false merge; it counts with the rev4 false merges.
3. Regression cases: G12, G13, G14 (must pass); R138 G02, G03 (must-recover, reported, never tuned to); C006 (the
   GDELT recall case, reported).
4. Accepted link count and the share of accepted links that touch no gold pair (unlabelled volume).

The sealed multilingual holdout (`holdout-xlang/`) and the Phase 3 relation holdout are not opened at any point of
this plan.

## 6. Selection and enablement rule (pre-registered)

A variant **qualifies** when all of these hold:

- stage-added false merges on rev4 additions **≤ 2**, and **zero** new false merges on the Phase 2 identity gold;
- G12, G13 and G14 still pass;
- at least **8** stage-added true merges on rev4 additions (two-thirds of today's 12; a guard that removes all false
  merges by removing all merges has no value);
- all gates unchanged: pytest, smoke, clustering benchmark, entity benchmark, Situation dry-run, `gold_check`.

Among qualifying variants, pick the most stage-added true merges. Ties go to fewer components, then to the
lower-numbered experiment. R138 is reported for the chosen variant but is not a selection criterion.

Outcomes:

- **One or more qualify:** freeze the chosen variant (code + config, one commit) and recommend
  `ENABLE CROSS-LANGUAGE STAGE` *for holdout evaluation*. The sealed multilingual holdout is then labelled and scored
  once against the frozen variant, and enablement in production waits for that result.
- **None qualifies:** `KEEP DISABLED`. If no variant gets stage-added false merges under 5 while keeping 8 true
  merges, the recommendation becomes `REJECT CURRENT APPROACH` (anchor-based acceptance over this candidate
  generator cannot reach precision).

## 7. Known limits of this evaluation

- The rev4 V-cases were drawn from this stage's own candidates, and the failure analysis above was done on the same
  cases. Every variant is therefore evaluated on data that shaped it. The components are general rules, chosen to
  limit that bias, but the development numbers will be optimistic. The sealed holdout is the honest test.
- 74 pairs are few: a difference of one or two cases between variants is not meaningful. Read the selection rule's
  thresholds with that in mind; they are set as counts for that reason.
- Stage-added precision is measured on labelled pairs only; unlabelled accepted links (item 4 above) are reported
  but not scored.
