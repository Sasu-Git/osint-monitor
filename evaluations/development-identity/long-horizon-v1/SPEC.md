# Long-horizon Development identity evaluation: SPEC

**Status: FROZEN 2026-11-23** (owner approval of O1-O11, section 12; freeze record `SPEC-FREEZE.md`). Nothing here is labelled,
scored or run through any model or guard. The sample, case files, split and scoring rules change only by a dated amendment. Markers
`[O#]` point to the approved decision in section 12.

## 1. Purpose

The existing identity gold (`evaluations/identity/`) judges pairs inside 48 h windows with at most 12 items per Development. It cannot
judge what the live system does over weeks. Development growth (`development_identity.reconcile`) attaches a new item to any member it is
`compatible_link`ed to (cosine >= 0.53, within 72 h), with no size or age cap. Chaining diagnostics on the 2026-11-23 snapshot show the
result: D398 holds 2,344 items over 41 days in one compatible component (late items median cosine 0.40 to the founding story), and in
152 of 162 Developments with members added after day 3, late members have no direct link to the founders
(`origin/eval/d398-identity-diagnostic`, `origin/eval/identity-chaining-diagnostic`).

This evaluation measures, against blind human labels, **how often a late segment of a stored Development is not the same occurrence or
episode as its founding segment**, and gives any future guard a two-sided yardstick: it must cut chains that cross occurrences (over-merge)
without cutting legitimate multi-day episodes (over-split). It is a measuring instrument only. No model, guard or rule work is in scope.

## 2. Owner definition (adopted 2026-11-23, verbatim)

> "A Development is one occurrence or tightly bounded event episode. Longer-running storylines belong at the Situation layer."

The existing contract (`evaluations/identity/development-identity-contract.md`) adds: different outlets, languages, framing, detail,
casualty counts, follow-up *factual updates*, official documents and roundups of the same occurrence are the same Development; a distinct
action inside the same crisis, conflict, summit or campaign (attack vs retaliation, meeting vs later agreement, proposal vs adoption) is a
different Development. The labels below are chosen so they map onto that contract without redefining it.

## 3. Unit of labelling

A **case** is a pair of sides drawn from **one stored Development** (a row in `events`):

- **Side A (earlier)**: up to 3 founding reports (published within 6 h of the Development's earliest member, earliest first).
- **Side B (later)**: a random anchor report published in a target time-gap band after the earliest founder, plus up to 2 of its nearest
  (embedding cosine) non-founder companions published within 24 h of the anchor, so the side reads as one coherent late segment rather than
  a single stray headline.

The labeller answers one question: *are the later reports part of the same occurrence or tightly bounded episode as the earlier reports?*
Founders-vs-late is the unit because the failure under test is "the Development's identity has drifted from its founding occurrence".
Adjacent-segment cases (late vs its own chain parent) are not included `[O10]`.

Each Development contributes 1 to 3 cases (D398: 6), taken from distinct gap bands and with disjoint B items. Cases from one Development
are not independent; they always fall on the same side of the dev / acceptance split and metrics report both case-level and
Development-level numbers (section 6).

## 4. Label set `[O1, O2]`

| Label | Meaning | Under the owner definition |
|---|---|---|
| `SAME_EPISODE` | The later reports are about the same occurrence or tightly bounded episode as the earlier ones: same event with more detail, casualty updates, official documents, direct aftermath inside the episode, a multi-day event that is one episode (storm, summit, siege, trial week). | one Development |
| `FOLLOW_UP_SAME_STORYLINE` | A different, later occurrence that follows from the earlier one: reaction, consequence, response, next step (attack then retaliation, meeting then later agreement). | not one Development; same storyline (Situation layer) |
| `RECURRING_SEPARATE_OCCURRENCE` | Another instance of a repeating kind of event with the same actors or place, not caused by the earlier one (another strike wave, another meeting, another fixture). | not one Development; possibly the same Situation |
| `DIFFERENT` | Unrelated, or sharing only a broad topic, theme, country or actor. | not one Development |
| `CANNOT_TELL` | The reports do not give enough information to decide. Not for complicated cases. Excluded from rates, reported separately. | excluded |

Optional per case: `confidence` (high / medium / low) and a free-text note. Labellers judge only what the reports say and are told not to
use outside knowledge of later events.

Scoring uses a **binary projection** `[O1]`: *same* = `SAME_EPISODE`; *not-same* = `FOLLOW_UP_SAME_STORYLINE`, `RECURRING_SEPARATE_OCCURRENCE`,
`DIFFERENT`. This follows the owner definition and the identity contract. The four-way label is kept so (a) the follow-up boundary can be
re-scored the other way as a sensitivity run and (b) the same labels can seed a later Situation-membership evaluation.

Mapping to the existing identity vocabulary: `SAME_EPISODE` ~ `SAME_DEVELOPMENT`; the three not-same labels ~ `DIFFERENT_DEVELOPMENT`;
`CANNOT_TELL` ~ `AMBIGUOUS`. "Tightly bounded" is **not** given a numeric duration cap `[O3]`; the owner's examples decide it, and the
time-gap band of each case is analysed afterwards (so a duration profile of `SAME_EPISODE` is observed, not assumed).

## 5. Time-gap bands `[O4]`

Gap = hours from the earliest founder's publication time to the B anchor's publication time (publication time = `published_at`, else
`fetched_at`).

| Band | Gap | Purpose |
|---|---|---|
| G1 | 6 h to < 48 h | short-occurrence control (should be mostly `SAME_EPISODE`; tests over-split) |
| G2 | 2 d to < 7 d | legitimate multi-day episodes vs first drift |
| G3 | 7 d to < 21 d | long-running |
| G4 | >= 21 d | chain failure territory |

## 6. Metrics a future guard is judged on

A guard (or any alternative Development-growth rule) is replayed on the same snapshot window and yields, per case, a **system decision**:
*kept together* iff the majority of the case's B items sit in the same Development as the majority of its A items after replay; else
*separated*. Items missing in the replay count as separated. (The decision is computed by the future scorer from `key.json`; it is never
shown to labellers.)

With gold projected to same / not-same and `CANNOT_TELL` excluded:

- **Over-merge rate** = (not-same cases kept together) / (not-same cases). Reported overall and by gold label, band and stratum.
- **Over-split rate** = (`SAME_EPISODE` cases separated) / (`SAME_EPISODE` cases). Reported overall and by band and stratum.
- **Balanced error** = mean of the two rates (a convenience summary, never the only number).
- **Development-level contamination** = share of sampled Developments with at least one not-same case kept together.
- **Baseline row**: the stored (production) decisions give the unguarded over-merge and over-split rates the guard is compared against.
- Wilson 95% intervals on every rate; counts always shown beside rates. Stratum-weighted population estimates use the pool sizes in
  `key.json` (strata are stratified samples, not a random sample of Developments: raw pooled rates are not population rates).
- Sensitivity run: the same metrics with `FOLLOW_UP_SAME_STORYLINE` moved to *same* `[O1]`.
- Items detached by a guard must be re-homed or left unclustered; that fate is outside this evaluation (reported, not scored).

**Thresholds.** No approved threshold exists. The scorer reports every metric **without a verdict** until the owner approves or
PROPOSES numeric targets `[O5]`. This spec proposes none.

## 7. Sampling frame, strata, size `[O6, O7, O9]`

Frame: Developments in `gold-snap.db` (VM snapshot 2026-11-23 09:43Z, sha256 `7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c`)
with >= 3 embedded members, minus the overlap exclusions of section 8. Features are label-free (span, size, chain depth, cosine to
founders, gap structure); `build_sample.py` header holds the exact definitions.

Strata, first match wins, in this order (thresholds are PROPOSED, adjustable under `[O6]`):

| Stratum | Rule | Stands in for |
|---|---|---|
| E_CHAIN_FAILURE | span >= 7 d and max chain depth >= 8 (D398 pinned) | known chaining failures |
| C_RECURRING_GAP | >= 2 late members, >= 2 bursts (runs of reports separated by a silent gap >= 24 h) and the second-largest burst has >= 2 reports | recurring events (same actors, repeating, with silence between) |
| D_DRIFT_MULTIDAY | >= 2 late members, median cosine of late members to the founder centroid < 0.55 | follow-ups and drift (later reaction / consequence reports) |
| B_CONTINUOUS_MULTIDAY | 2 d <= span <= 14 d, no gap >= 24 h between consecutive reports | legitimate multi-day episodes |
| A_SHORT | 12 h <= span < 48 h | short occurrences |

The strata are **sampling aids, not labels**: "recurring" and "follow-up" strata are only proxies built from time and embedding structure.
The labels decide what each case really is, and every stratum is expected to contain several label values.

Proposed size: **~160 cases** (A 30, B 30, C 30, D 30, E 40), drawn as 30 / 30 / 15 x 2 / 15 x 2 / ~14 x 3 Developments. Built at the proposal: **157
cases from 104 Developments** (A 30, B 30, C 28, D 25, E 44; gap bands G1 30, G2 101, G3 23, G4 3; development 74 / acceptance 83;
see `SAMPLE.md` and `manifest.json`). The >= 21 d band is thin (3 cases, only a handful of Developments are that long, D398 dominates). Rationale: a binary rate near 10 to 20% with ~50
cases per side gives a Wilson half-width of about 8 to 11 points; with the development / acceptance split each half is ~80 cases. Larger
is better for the rare labels but labelling effort grows linearly `[O9]`.

## 8. Overlap policy

- Developments containing any item of the existing identity gold (cases' a/b in `evaluations/identity/gold/identity-gold.yaml`,
  matched by normalised URL or exact outlet+headline) are excluded from the frame.
- Developments listed in the upstream topic/location gold `cases.json` files (`osint-monitor-gold`, ids > 1341) are excluded.
- The windows of the identity gold (all replay-window items, not only gold-case items) are matched too and reported, not excluded.
- Exact counts are in `SAMPLE.md` / `manifest.json`. Not touched: sealed holdouts (`evaluations/relations/holdout/`,
  `evaluations/identity/holdout-xlang/`).

## 9. Blindness protocol

- Labellers see, per side: outlet, publication time, headline and lead (<= 600 characters). They do **not** see Development ids, item ids,
  cosines, strata, gap bands, stored summaries or types, the Situation, or any system decision. The gap is only visible through the printed
  publication times.
- `cases.json` is the only file the labelling UI reads. `key.json` (case -> Development, items, strata, features) is never opened by the UI.
- Case ids are opaque (`LH001...`) and the case order is a seeded shuffle, so neither id nor order reveals the stratum or the Development.
- Label history is appended to `label-history.jsonl` on every save; the **first answer per case is the blind primary basis**; later edits
  are kept in the history and flagged in the report.
- The labeller does not run, read or look at any guard or system output before labels are frozen. Labelling is done by the owner (primary
  blind labeller) `[O8]`.

## 10. Dev / acceptance split

Split at the Development level (all cases of a Development on the same side), stratified by stratum, deterministic: per stratum the sorted
Development ids are shuffled with `random.Random(f"{SEED}-split-{stratum}")` and the first 50% (rounded) go to acceptance `[O9]`.
Seed `20261124`. `split.json` maps case id to `development` / `acceptance`. Guard design may inspect development cases only; acceptance
cases are scored once, after the guard rule is frozen, and are never used to tune it. All cases are labelled in one pass (so labeller
judgement is not split-dependent); the split is applied when scoring.

## 11. Freeze procedure

1. Owner reviews this spec and resolves section 12; the spec is edited to final and committed with its sha256 recorded in `manifest.json`.
2. `build_sample.py` is run (verifies the snapshot sha256, builds in a backup-API copy); `cases.json`, `key.json`, `split.json`,
   `manifest.json` are committed with hashes. After this point the sample, case files and scoring rules change only by a dated amendment.
3. Labelling: `label_server.py` (127.0.0.1:8795); `--validate` then `--freeze` writes `labels-freeze.json` (sha256 of labels and history);
   the server refuses edits afterwards.
4. Only then may any guard be scored against the development half; the acceptance half stays unscored until the guard is frozen.

## 12. Owner decisions (approved 2026-11-23)

| # | Decision | Approved |
|---|---|---|
| O1 | Does a follow-up (reaction, consequence, next step) belong to the same Development? | **No** in the primary definition: only `SAME_EPISODE` is *same*. A sensitivity run that counts `FOLLOW_UP_SAME_STORYLINE` as *same* is kept in every report. |
| O2 | Label set | The 5 labels of section 4: same episode (`SAME_EPISODE`), follow-up (`FOLLOW_UP_SAME_STORYLINE`), recurring separate occurrence (`RECURRING_SEPARATE_OCCURRENCE`), different (`DIFFERENT`), cannot tell (`CANNOT_TELL`). |
| O3 | What counts as "tightly bounded" | No numeric maximum duration; the owner's labels decide it case by case. Durations of `SAME_EPISODE` are observed afterwards by gap band. |
| O4 | Time-gap bands | `6-48 h`, `2-7 d`, `7-21 d`, `>= 21 d` (section 5). |
| O5 | Pass / fail thresholds for over-merge and over-split | Defined by the owner **before the first guard is scored**, not before labelling. None are set by this spec. |
| O6 | Stratum definitions and cut-offs | Kept as proposed (depth >= 8, late cosine < 0.55, 24 h silent gap, 24 h continuity, 14 d multi-day ceiling). They shape sampling only, not semantics. |
| O7 | Stratification features | Time and embedding features only; no stored attributes. |
| O8 | Who labels | The owner labels all cases. A second labeller on ~20% is optional, not required. |
| O9 | Size and split | Keep the 157 built cases and the ~50/50 development / acceptance split by Development (74 / 83). The `>= 21 d` band is **not** padded. |
| O10 | Case types | Founding vs late segments only. |
| O11 | Side content | Report evidence on each side (outlet, time, headline, lead); no stored summaries. |

## 13. Files

`SPEC.md` (this), `SAMPLE.md` (counts, overlap, strata), `build_sample.py`, `label_server.py`, `cases.json` (blind label input),
`key.json` (case to Development, items, strata, features; not for labellers), `split.json`, `manifest.json` (snapshot sha, seed, script hash,
counts, overlap, output hashes), `tests/test_long_horizon_identity.py` (determinism, freeze, blindness).
