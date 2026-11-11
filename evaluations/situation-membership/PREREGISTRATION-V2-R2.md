# Preregistration: Situation membership v2 (revision 2) on a fresh holdout — FROZEN 2026-11-11

**Status.** Frozen with the contract (hashes in `V2-R2-FREEZE.md`). Nothing is sampled, labelled or scored. Gates are
the owner's OD8 rulings (2026-11-11). Lines marked `DEF` are deterministic definitions written to implement those
rulings, and the window and sample sizes were frozen as drafted. The owner may amend any of these by a dated amendment
**before the holdout window opens**; after it opens, any amendment voids the window.

## 1. Sets and their roles

| Set | Role | Rule |
|---|---|---|
| 126-case subsample (`evalset/subsample/`, frozen `57fef39`, scored `e8943fd`) | **development / diagnostic** | preserved unchanged; the v2 candidate may be built and debugged against it; never used for acceptance |
| remaining 253 cases of the 379-case set | **not a holdout** | same snapshot and Situations as the diagnostic set; descriptive use only |
| CONTRACT-V2 seed cases | **not gold** | the owner's labels contradict 6 of 29; not reused as acceptance cases |
| 126-review scope overrides (OD7) | **design input** | adopted as versioned overrides; not acceptance evidence |
| **Fresh holdout** (this file) | **acceptance** | Developments first reported **after** the code freeze |

## 2. Order (no step skipped)

1. Contract and preregistration frozen (done 2026-11-11, this file).
2. Candidate implemented on a branch and replayable on a snapshot. Developed against the diagnostic set only. The OD7
   scope mapping is shown to the owner. **Code frozen** (commit + hash). No runtime deploy.
3. Holdout window opens at the code-freeze time T0 and closes at T0 + 14 days.
4. Snapshot from the **VM DB** (backup API, `mode=ro`) after the window closes; hash recorded.
5. Baseline (today's runtime grouper, `production-stable-20261111`) and candidate replayed on the same snapshot window.
6. Sample drawn with a recorded seed and frozen (hash) before labelling.
7. Owner labels blind; a second opinion only after each label is saved; history kept; first answer = primary basis.
8. Labels frozen (hash).
9. Score once, on both bases (first answers primary, final secondary). A pass/fail difference between bases is
   **inconclusive**. No tuning after scoring: a revised candidate needs a new window.

## 3. What is evaluated

v2 changes Situation identity, so two things are labelled.

- **A. Situation creation.** Every automatic Situation (actor-process, single-party, hazard) created in the window by
  either system; if more than 40, a seeded random 40 with each mode represented. The owner labels each `COHERENT` /
  `INCOHERENT` / `DUPLICATE_OF:<slug>`, plus its intended scope.
- **B. Membership pairs** (Development, Situation), drawn from the union of both systems' decisions. The proposing
  system is sealed in a key file.

## 4. Sampling

**Population for B.** Every pair in the window where either system (i) admitted the Development, (ii) considered it a
candidate (baseline: score in [0.4, 0.6); candidate: passed E1 and was not `MEMBER`), or (iii) gave an outcome other
than `NOT_MEMBER` (`CONTEXT`, `SPILLOVER`, `OTHER_SITUATION`, `AMBIGUOUS`, `PENDING`).

**Target: 220 pairs**, stratified. A stratum smaller than its target is taken whole and the remainder reallocated
proportionally.

| Stratum | Definition | Target |
|---|---|---|
| Agreed members | both systems admit | 45 |
| Disagreements | exactly one system admits (oversampled boundary) | 50 |
| Near-misses | a candidate for either system, admitted by neither | 25 |
| Commentary | either system or the item headline kinds mark it commentary-led | 20 |
| Spillover | family in scope, every known place outside the place scope | 15 |
| Other-Situation | a candidate for two or more Situations | 20 |
| No principals | no principal actors | 10 |
| Single-party | pairs on single-party Situations (OD1) | 15 |
| Hazard | pairs on hazard Situations (OD2) | 10 |
| Pending | candidate `PENDING` at snapshot time (OD3) | 10 |

**Constraints.**
- At least 30% of pairs are on seeded Situations. Every open Situation in the window with any pair gets at least 2.
- Expected owner-`MEMBER` count at least 80, so the recall gate has about ±7 points of 95% interval. If the drawn
  sample is short, the agreed-member and disagreement strata are topped up before labelling.
- Language proportional to the window; non-English at least 20%.

**Labels.** `MEMBER`, `CONTEXT`, `SPILLOVER`, `OTHER_SITUATION`, `NOT_MEMBER`, `AMBIGUOUS`, each with a one-line reason.
The owner labels what the evidence supports at snapshot time. `PENDING` is a system outcome, not a label; a pending
pair counts as **not admitted**.

## 5. Metrics (reported, no composite)

Baseline and candidate, on the same pairs, overall and per mode and per Situation kind:
- MEMBER recall and precision (owner-`AMBIGUOUS` excluded and reported separately);
- non-member rejection, pooled and for each label (`CONTEXT`, `SPILLOVER`, `OTHER_SITUATION`, `NOT_MEMBER`);
- `AMBIGUOUS` and `PENDING` rates;
- creation: counts of `COHERENT`, `INCOHERENT` and duplicates per mode;
- auditability: share of decisions with a reason code and a complete provenance record (§6 of the contract);
- upstream preconditions, separately: share of pairs whose Development is `mixed`, has a name-variant or non-actor
  anchor, has no family, or has event country `NONE`.

## 6. Gates (OD8, frozen; applied to the fresh holdout only)

| Gate | Threshold |
|---|---|
| MEMBER recall (owner-`MEMBER` pairs the candidate admits) | ≥ 0.90 |
| Non-member rejection (DEF: pooled over owner `NOT_MEMBER`, `OTHER_SITUATION`, `CONTEXT`, `SPILLOVER`) | ≥ 0.80 |
| Membership precision (owner-`MEMBER` share of candidate-admitted pairs, owner-`AMBIGUOUS` excluded) | ≥ 0.85 |
| Positive seeded regressions (DEF: owner-`MEMBER` pairs on seeded Situations that the baseline admits and the candidate does not) | 0 |
| Situation coherence | 0 candidate-created Situations labelled `INCOHERENT` in the creation sample |

**Veto (OD8).** No acceptance if an improvement comes from materially worsening another measure relative to the
baseline. DEF: on the same pairs, the candidate must not be worse than the baseline by **5 percentage points or more**
on any of: MEMBER recall, MEMBER precision, each per-label rejection rate, or the share of pairs left `AMBIGUOUS` or
`PENDING`.

**Acceptance** = every gate passes and the veto does not fire, on **both** label bases. If the bases disagree on any
gate or on the veto: **inconclusive**.
