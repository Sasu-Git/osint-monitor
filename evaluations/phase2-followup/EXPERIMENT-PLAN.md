# Phase 2 follow-up experiment E1: cross-day action-divergence guard (pre-registration)

Status: **PRE-REGISTERED, NOT IMPLEMENTED** (2026-10-27). Nothing below has been run. The rule, the datasets, the
metrics and the thresholds are fixed here before any code or any measurement, and amendments are appended, never edited
in. Category: **storyline-overmerge guard**. Evidence and source keys: [`DECISION-MEMO.md`](DECISION-MEMO.md),
[`EVIDENCE.md`](EVIDENCE.md).

## Why this one

- **Overmerge is the largest residual defect.** It has 42 defect cases and 17 whole-storyline split failures that
  Phase 2 did not move, and it blocks 22 scored relation cases (13 canonical positives), which keeps Phase 3 paused.
- **The prior time-only rule failed for a known reason.** The T24 occurrence span fixed 8 overmerges and lost two
  holdout pairs. The overmerges it fixed were 31-41 h apart; the true one-occurrence pairs it broke were 32-34 h
  apart. FR's conclusion: cross-day creep "needs an action-level signal".
- **This tests exactly that missing signal.** Time is kept only as a precondition. The cut is made only when the
  *action* differs too. Same-occurrence follow-ups across days ("execution halted" ... "execution halted, governor
  says") should keep the same action, which is precisely what protects the pairs T24 broke.
- **Not chosen:**
  - same-day distinct actions: FR says "no text signal separates them";
  - cross-language: KEEP DISABLED stands (merge precision 0.375; the interim coverage labels are not decision-grade);
  - same-language recall: 17 cases spread over six root causes, and the prior threshold rule added 0 true / 13 false
    joins;
  - segmentation recall: the interim labels say 12-23% recoverable, so the segmentation guards are mostly right.

## Hypothesis

Among report headlines in one narrative cluster, links between items more than 24 hours apart join
**different occurrences** mostly when their main actions differ, and **the same occurrence** mostly when their main
actions match. A guard that cuts such cross-day links when the action classes differ fixes cross-day storyline
overmerges without the recall loss of a time-only rule.

## Exact rule (one new segmentation guard; nothing else changes)

- **Placement.** A new incompatibility in `processors/development_segmentation.py`: `distinct_action_across_days`.
  It sits beside `headline_similarity`, `disjoint_locations` and `analysis_headline`. It is configured in
  `config/event_grouping.yaml` under `development_segmentation` and is off by default. It applies wherever segmentation
  already re-checks links inside a narrative cluster, which includes links to the members of an existing Development.
- **Fires only when all of the following hold:**
  1. both items are **report** headlines (`headline_kind` = REPORT; analysis, rolling and roundup forms are handled by
     the existing rules);
  2. their publication times differ by **more than 24 h**;
  3. each headline has a **main action**: the lemma of the dependency root when it is a verb, or of the root's head
     noun when the root is a nominal event noun. This uses the item's own language model (en / it / es), and the
     headline only;
  4. both main actions map to an **action class** in a fixed, general lexicon. Lemmas outside the lexicon, and the
     generic class (say, report, update, continue, make, take, hold, and their es/it equivalents), never fire;
  5. **the two classes differ.**
- **Action lexicon.** One YAML file, `config/action_classes.yaml`. It is general, with no names, places or case
  identifiers. It holds about 12 to 16 classes (for example: judicial ruling; halt / suspend; execute / carry out;
  reject / refuse; propose / offer; negotiate / meet; attack / strike; arrive / deliver; detain / arrest; resign /
  dismiss; approve / sign; announce / launch), each with en / es / it lemmas. **It is written and frozen before any
  dev measurement**, with its hash recorded in an amendment.
- **Effect.** The link is cut, exactly like the other guards. No Development is merged or deleted.

## Data

- **Development data** (allowed for every step):
  - the frozen Development-identity defect set: 128 cases, e98a0fe, `evaluations/identity/defects/`;
  - the Phase 2 development windows, identity gold rev 2: 2026-08-21, 2026-09-25, 2026-09-30-multilingual, 158 scored
    pairs;
  - identity gold rev 4, development split (232 scored);
  - the clustering out-of-sample windows used for segmentation v2: 08-31, 09-10, 09-27-live, 09-29-live.
- **Frozen cases tracked by name:**
  - OVERMERGE targets: Pike T012/T013/T014/T040; Hormuz R014, R115, R132, T018, T029, T037, T045; Ebola A021/A022;
    French protests G07; A002, A023, R013, R029, R060, C115;
  - must-keep SAME: the 13 SAME controls of the defect set; the multi-day SAME pairs of Phase 2 dev and identity gold
    rev 4.
- **Holdout:** the Phase 2 holdout (2026-08-31, 30 pairs) is used **once**, as a veto, only after the development
  acceptance below. It has already been scored for Phase 2 and for T24, so it is a regression check, not an unbiased
  estimate. **The sealed holdouts (`evaluations/relations/holdout/`, `evaluations/identity/holdout-xlang/`) are not
  used.**

## Procedure

0. **Baseline on the current code** (`production-stable-20261016`, or Candidate A if promoted; Phase 2 numbers are
   identical either way). Record the defect-set correct count, the Phase 2 dev tallies (expected 43/65, 43/58, 22/100,
   15/58, 16/19, 12/31) and identity gold rev 4 correct. Run off the live host's busy hours, at below-normal priority.
1. **Feasibility gate (no pipeline change).** Freeze the lexicon. Then compute the main action and class for both
   sides of every development pair more than 24 h apart: the defect set, Phase 2 dev and identity gold rev 4.
   Measure:
   - **F1** = the share of cross-day DIFFERENT (overmerge) pairs whose classes differ (both in the lexicon);
   - **F2** = the number of cross-day SAME pairs whose classes differ.

   **Proceed only if F1 ≥ 40% and F2 ≤ 1.** Otherwise **stop**: record "action classes do not separate cross-day
   occurrences" and implement nothing.
2. **Implement** the guard (off by default), with unit tests for each condition. Then score the development data
   with it on.
3. **Development decision** (thresholds below).
4. **One-time holdout veto**, only if step 3 accepts.
5. **Situation impact** on a snapshot copy (Developments and Situations before and after), as for T24. Report only.

## Metrics and thresholds

**Primary metrics:**
- defect-set OVERMERGE cases fixed, of 42 (T24 reference: 8);
- Phase 2 dev split failures (22/100).

**Regression metrics, with their limits:**

| Metric | Baseline | Limit |
|---|---|---|
| Phase 2 dev continuity recall | 43/58 | may drop by at most 1 pair |
| Phase 2 dev merge failures | 15/58 | at most 16/58 |
| Phase 2 dev ID stability | 16/19 | no drop |
| Defect-set SAME controls | 13 | none broken |
| Defect-set CORRECT total | baseline value | no case moves from correct to wrong except fixed-target trades listed explicitly |
| Identity gold rev 4 correct | baseline value | no decrease |
| Clustering out-of-sample cross-source SAME | 44/49 | at least 43/49 |
| Single-source Developments | 0 | stays 0 |
| Duplicate memberships | 0 | stays 0 |

**Acceptance (development):** all of the following.
- At least **6** OVERMERGE defect cases fixed.
- Phase 2 dev split failures down by at least **3** (to at most 19/100).
- Every regression limit above respected.

**Rejection (development):** any one of the following.
- Fewer than 4 OVERMERGE fixed.
- Any SAME control broken.
- Continuity recall down by 2 or more pairs.
- ID stability down.
- Out-of-sample cross-source SAME below 43/49.

**Holdout veto:** recall at least **7/10** and ID stability at least **5/8**, the exact T24 failure point. Failing it
rejects the guard, whatever the development result.

## Stop conditions

- **Feasibility gate fails** (F1 < 40% or F2 > 1): stop before implementing.
- **Between acceptance and rejection** (4-5 fixed, or 1-2 split failures removed): **one** lexicon revision is
  allowed. It must be written as an amendment with its reason, and the lexicon frozen again **before** re-scoring the
  development data. Then a final decision. No second revision.
- **Holdout veto fails:** reject. No tuning against the holdout, and no reuse of the holdout for a variant.
- **No exceptions for particular entities, names, places or cases** at any step. A rule that only works with such an
  exception is a rejection.

## Out of scope for E1

- Same-day distinct actions.
- Overlap-merge reconciliation of existing Developments (ID stability).
- Commentary detection changes.
- Cross-language identity.
- Any threshold change.
- Live deployment: if accepted, E1 becomes its own deploy candidate under the runbook, after Candidates A and B.

## Amendment 1 (2026-10-27): feasibility gate definitions, frozen before measurement

Owner approval 2026-10-27: "APPROVE E1 FEASIBILITY" (feasibility only; no implementation; no full replay before
Candidate A C2; the Phase 2 holdout is not opened). Written and committed before any pair was measured.

- **Lexicon frozen:** `e1/action_classes.yaml`, 16 classes, en / es / it, sha256 (LF bytes)
  `6de4875a69b9fc4850342e93139dcd520e86e911efd76e4ddc6c9a1374196150`. Written without reading any pair headline.
  No lemma is in two classes, or in a class and the generic list.
- **Measurement script frozen:** `e1/feasibility.py`, sha256 (LF bytes)
  `a3f736756fe90f11bd3590d7489381dfd8c8c91bd4588c69b0518558d4780929`. It records the sha256 of every input.
- **Main action.** The headline is HTML-unescaped and parsed with the pipeline's model for its language
  (en_core_web_lg, es_core_news_md, it_core_news_md). The main action is the root of the first sentence whose root is a
  VERB, NOUN or PROPN, as its lowercased spaCy lemma. Generic lemmas and lemmas outside the lexicon get no class.
  Other languages get no class. Items in the wayback clustering windows (2026-08-21, 2026-09-25) carry no language
  field and are read as English.
- **Report headline:** `headline_kind` from `osint_monitor/processors/development_segmentation.py` at `adacb83`
  (identical to `production-stable-20261016` for this function).
- **Guard on one link:** fires only when the two items are more than 24 h apart, both are report headlines, both main
  actions have a class, and the classes differ.
- **Pairs.** A case is two sides; a side is one item (identity gold) or several (relation-derived defect cases). Every
  item link between the sides is evaluated. Cases are deduplicated across sources by their item sets; a case with
  conflicting labels across sources is reported and left out. AMBIGUOUS is left out.
- **Data (development only).** Identity gold rev 4 entries with `split: development` (`identity-gold.yaml` and
  `identity-gold-rev3-additions.yaml`, which together hold the Phase 2 development pairs); the frozen defect set
  (`defect-cases.json`) except its one case in the holdout window 2026-08-31, which is dropped unread. Gold entries of
  the holdout split are dropped before any other field is used.
- **F1 population:** cross-day OVERMERGE pairs = DIFFERENT pairs that the current code keeps together: defect-set
  OVERMERGE cases, plus Phase 2 development DIFFERENT pairs ledgered "kept together" in
  `phase2-dev-actor-hygiene.json` (@fix/actor-hygiene). Cross-day means **every** item link is more than 24 h apart
  (a link within 24 h cannot be cut). **F1** = the share whose every link the guard cuts.
- **F2 population:** SAME pairs (all development sources) with **at least one** item link more than 24 h apart.
  **F2** = the number on which the guard cuts at least one link.
- **Gate unchanged:** proceed only if F1 >= 40% and F2 <= 1; otherwise stop and implement nothing. Secondary numbers
  (F1 counting any cut link; all cross-day DIFFERENT pairs) are reported for information and do not change the gate.

## Amendment 2 (2026-10-27): feasibility result

Feasibility gate **FAILED**: F1 = 0/5 (gate >= 40%), F2 = 0/7 (gate <= 1). E1 stops as pre-registered; nothing is
implemented. Only 5-6 of 41 development OVERMERGE cases are cross-day, fewer than the 6 the development acceptance
requires. Details: `e1/FEASIBILITY.md`, `e1/feasibility-results.json`.
