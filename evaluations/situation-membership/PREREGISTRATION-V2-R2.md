# Preregistration draft: Situation membership v2 (revision 2) on a fresh holdout — PROPOSED, not frozen

**Status.** Draft. Nothing is sampled, labelled or scored. Every number below is `PROPOSED` until the owner approves
it **before** any scoring. This file is frozen (hash recorded) only after the owner approves it.

## 1. Sets and their roles

| Set | Role | Rule |
|---|---|---|
| 126-case subsample (`evalset/subsample/`, frozen `57fef39`, scored `e8943fd`) | **development / diagnostic** | preserved unchanged; informs design; never used for acceptance |
| remaining 253 cases of the 379-case set | **not a holdout** | same snapshot and same Situations as the diagnostic set, so design has seen their population; descriptive use only |
| CONTRACT-V2 seed cases | **not gold** | the owner's labels changed 6 of 29; not reused as fixed acceptance cases |
| **Fresh holdout** (this file) | **acceptance** | drawn from Developments first reported **after** the contract and code are frozen |

## 2. Order (no step skipped)

1. Owner rules on OD1–OD6 (`CONTRACT-V2-R2.md` §8); the contract is frozen (hash).
2. Candidate implemented on a branch, replayable on a snapshot; **code frozen** (commit + hash). No runtime deploy.
3. Holdout window opens at the code-freeze time T0 and closes at T0 + 14 days (`PROPOSED`).
4. Snapshot taken **from the VM DB** (backup API, `mode=ro`) after the window closes; hash recorded.
5. Baseline (today's runtime grouper) and candidate are replayed on the same snapshot window.
6. Sample drawn with a recorded seed; sample frozen (hash) before labelling.
7. Owner labels blind; second opinion only after each label is saved (history kept; first answer = primary).
8. Labels frozen (hash).
9. Gates approved by the owner (this file's section 6, as approved).
10. Score once, on both bases (first answers primary, final secondary). A pass/fail difference between bases is
    **inconclusive**. No tuning after scoring; a revised candidate needs a new window.

## 3. Two things are evaluated, because v2 changes Situation identity

Replaying the candidate creates different Situations from the baseline, so pairwise labels on baseline Situations
alone cannot judge it.

- **A. Situation identity** (candidate and baseline). Every automatic Situation created in the window by either system
  (expected 15–40). The owner labels each: `COHERENT` / `INCOHERENT` / `DUPLICATE_OF:<slug>`, plus its intended scope
  (families and places).
- **B. Membership pairs** (Development, Situation). Drawn from the union of both systems' decisions, so the labeller
  cannot tell which system proposed a pair (system origin is sealed in a key file).

## 4. Sampling (PROPOSED)

**Population for B.** In the window, every pair where either system (i) admitted the Development, (ii) considered it
a candidate (baseline: score in [0.4, 0.6); candidate: passed E1 but was not `MEMBER`), or (iii) gave it a non-member
outcome other than `NOT_MEMBER` (`CONTEXT`, `SPILLOVER`, `OTHER_SITUATION`, `AMBIGUOUS`).

**Target: 220 pairs** (`PROPOSED`), stratified; a stratum smaller than its target is taken whole and the remainder
reallocated proportionally.

| Stratum | Definition | Target |
|---|---|---|
| Agreed members | both systems admit | 50 |
| Disagreements | exactly one system admits (the boundary; oversampled) | 50 |
| Near-misses | candidate by either system, admitted by neither | 30 |
| Commentary | either system or the item headline kinds mark it commentary-led | 25 |
| Spillover | E1 passes, family in scope, every known place outside the place scope | 20 |
| Other-Situation | the Development is a candidate for two or more Situations | 25 |
| No principals | no principal actors (tests X1) | 10 |
| Hazard (only if OD2 is approved) | hazard-kind candidates | 10 |

**Coverage constraints.**
- Seeded vs automatic: at least 30% of pairs on seeded Situations; every open Situation in the window with at least
  one pair gets at least 2.
- Expected owner-`MEMBER` count at least 80, so the members-kept rate has a 95% interval of about ±7 points at 90%.
  If the drawn sample is short of that, the agreed-member and disagreement strata are topped up before labelling.
- Language: proportional to the window's Development languages; non-English at least 20%.

**Labels.** As the 126-case set: `MEMBER`, `CONTEXT`, `SPILLOVER`, `OTHER_SITUATION`, `NOT_MEMBER`, `AMBIGUOUS`,
each with a one-line reason; `PENDING` is not a label (the owner labels what the evidence supports now).

## 5. Metrics (reported, no composite)

For baseline and candidate on the same pairs, overall and per Situation kind:
- MEMBER precision and recall (members kept);
- rejection rates for each non-member label (`CONTEXT`, `SPILLOVER`, `OTHER_SITUATION`, `NOT_MEMBER`);
- `AMBIGUOUS` rate (owner and system);
- Situation identity: share of created Situations labelled `COHERENT`; duplicates;
- auditability: share of decisions with a reason code and a complete provenance record;
- upstream preconditions, reported separately: share of pairs whose Development is `mixed`, has a name-variant or
  non-actor anchor, or has an `unknown` family.

## 6. Gates (all PROPOSED; must be approved before step 10)

| Gate | PROPOSED threshold |
|---|---|
| Members kept (owner `MEMBER` admitted) | ≥ 0.90 |
| MEMBER precision | ≥ 0.85 |
| Owner-`NOT_MEMBER` rejected | ≥ 0.80 |
| Owner-`CONTEXT` admitted as `MEMBER` | ≤ 0.10 |
| Owner-`OTHER_SITUATION` admitted as `MEMBER` | ≤ 0.15 |
| Candidate-created Situations labelled `COHERENT` | ≥ 0.90 |
| Seeded-Situation regressions (owner-`MEMBER` pairs on seeded Situations that the baseline admits and the candidate rejects) | 0 |
| Candidate vs baseline | candidate not worse than baseline on any gate above |

Acceptance needs every approved gate on **both** label bases. If the bases disagree on any gate's pass/fail: inconclusive.
