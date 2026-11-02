# H3 feasibility check: FAILED (2026-11-02)

**H3 FAILED — NO RUNTIME IMPLEMENTATION.** F1 passes. F2 fails: DA1's core-compatibility test rejects 3 of the 9 L2
members the owner labelled as the founding occurrence.

Per the plan (step 3): "core compatibility does not separate founder occurrence from relay members". The DA experiment
stops here:
- no DA1 or DA2 runtime code;
- no H2;
- no holdout.

Owner approval of the run: 2026-11-02 ("run the preregistered H3 Development-admission feasibility check").

## Frozen inputs (verified immediately before scoring)

| Input | Value |
|---|---|
| Labels | `labelling/owner-labels.yaml`, normalised sha256 `1a66ec001afc3fb31548c9271f56e44ed9dcf9183ec1b4e248d187df0ed0110b` = `LABELS-FREEZE.json` (`918c720`). `labels_tool.py validate`: 217/217, 0 problems. Worktree identical to `918c720`, which matches origin |
| Plan, scripts, cases, key, dataset | all 12 hashes in `FREEZE-LABELLING.json` re-verified, unchanged. No change to the plan, amendments or labels since the freeze |
| Code | `osint-monitor-timing` at `adacb83` (the frozen labelling code; the scorer asserts SHA and clean tree) |
| Snapshot | `snapshot-20261027-forensic.db`, sha256 `3c0b2cd9…0b4a39` (= freeze), opened read-only |
| Thresholds (asserted, unchanged) | link cosine 0.53; headline cosine 0.5; places: containment, `use_regions: false`; P7 occurrence match as configured at `adacb83` |
| Scorer | `h3_score.py`, sha256 `9af5cb81…62f3e2`; output `h3-results.json`, sha256 `6d724a23…29654f` |

**Scope, as preregistered** (plan step 3, "L2-DIFFERENT / L2-SAME sampled members"):
- the 128 L2 cases of the 8 giants, all scorable: SAME 9, DIFFERENT 117, AMBIGUOUS 2;
- AMBIGUOUS cases are reported separately and excluded from F1/F2.

The owner brief mentioned a SAME denominator of 16. That is the SAME count across all label sets (L1 2, L2 9, L2b 1,
L3a 4), not H3's preregistered set. On that reading F2 would be 3/16 = 18.8%, also above 10%, so the outcome does not
depend on it.

**Method** (`ARCHITECTURE.md` §4–§5, applied literally; nothing tuned).

The core is the DA1 kernel of each giant's actual founders:
- eligible = REPORT headlines plus primary evidence;
- seed = the cross-origin compatibly linked pair with the highest cosine;
- complete-link growth to at most 5 members;
- fallback = up to 5 founders.

A member is rejected when `core_compatible` is false. That requires all three conditions:
- **C-sem:** cosine >= 0.53 to at least ⌈|core|/2⌉ core members;
- **C-head:** for REPORT headlines, headline cosine >= 0.5 to a REPORT core member, or P7 occurrence evidence;
- **C-place:** no place conflict with the core's places.

**Cores found.** Every giant had a cross-origin kernel; no fallback was needed.

| Giant | Kernel size | Kernel items |
|---|---|---|
| D182 | 2 | 3094, 3146 |
| D397 | 4 | 8341, 8598, 8450, 8496 |
| D398 | 5 | 8455, 8490, 8331, 8572, 8440 |
| D399 | 2 | 8364, 8508 |
| D449 | 4 | 9375, 9406, 9295, 8355 |
| D514 | 2 | 8485, 10815 |
| D626 | 2 | 12402, 13666 |
| D639 | 2 | 13713, 14223 |

## Results

| Gate | Rejected / n | Share | Wilson 95% | Threshold | Result |
|---|---|---|---|---|---|
| **F1**: owner-DIFFERENT members rejected | 80 / 117 | 68.4% | 59.5–76.1% | >= 60% | **pass** (the lower bound sits just below 60%) |
| **F2**: owner-SAME members rejected | 3 / 9 | 33.3% | 12.1–64.6% | <= 10% | **FAIL** (even the lower bound is above 10%) |
| AMBIGUOUS (reported only) | 1 / 2 | 50% | — | — | — |

### SAME members DA1 would reject (the F2 failures)

| Case | Giant | Item | Fails | Headline |
|---|---|---|---|---|
| R046 | D182 | 7554 | C-sem 0/2, C-head | "Three years after October 7, prolonged war takes its toll on Israelis" |
| R153 | D182 | 5790 | C-sem 0/2, C-head | "Israel marks 3 years since Hamas attack with no hostages in Gaza" |
| R157 | D397 | 21181 | C-sem 0/4, C-head, C-place | "Time 'running out' to reach Yemen's Taiz amid deepening crisis, UN says" |

**Admitted SAME members (6):** R003 (D639), R018 (D182), R029 (D182), R060 (D397), R061 (D514), R146 (D514).

The two D182 rejections are the same anniversary occurrence in different words. Their full text shares no 0.53-cosine
link with a 2-item core, and their headlines differ. That is exactly the "same occurrence, different wording" family
the plan warned about (F2 family; quorum lenient by design). With a 2-member core, one quorum hit is required and
neither had one.

### DIFFERENT members DA1 would admit (37; the F1 misses)

By giant: D626 9, D449 8, D399 6, D398 4, D397 4, D639 4, D182 1, D514 1.

**Misses by giant:**

| Giant | Admitted DIFFERENT cases | What they are |
|---|---|---|
| D626 (French protests) | R027, R052, R059, R078, R080, R112, R121, R184, R202 | 9 different protest days and actions, all passing a 1-of-2 quorum against a "French protests" core |
| D449 (Brazil election) | R005, R019, R111, R114, R166, R181, R186, R199 | 8 different campaign events, debates and investigations; 4/4 quorum. The whole storyline is semantically one cluster |
| D399 (Ukraine strikes and diplomacy) | R009, R116, R129, R131, R168, R190 | 6 Italian/Spanish items: the English-only embedding is weak evidence |
| D398 (energy ceasefire and talks) | R004, R086, R105, R195 | — |
| D397 (Houthi attacks on Saudi Arabia) | R017, R083, R150, R205 | different interceptions |
| D639 (French protests, Spanish-language) | R094, R126, R128, R141 | — |
| D182, D514 | R148, R147 | — |

**Conditions behind the 80 rejections:** C-sem alone 14; C-sem + C-head 39; C-head alone 6; C-place alone 7; the
remaining combinations 14.

**Per giant, DIFFERENT members rejected:**

| Giant | Rejected / n |
|---|---|
| D182 | 10/11 |
| D514 | 13/14 |
| D639 | 11/15 |
| D398 | 12/16 |
| D397 | 10/14 |
| D399 | 10/16 |
| D449 | 8/16 |
| D626 | 6/15 |

### AMBIGUOUS members (excluded from F1/F2)

| Case | Giant | DA1 | Headline |
|---|---|---|---|
| R071 | D626 | admitted | "Midterms: Trump seizes on unrest in France for political gain" |
| R088 | D182 | rejected (C-sem, C-head) | "Global protests mark October 7 attack with calls for Gaza ceasefire" |

## Interpretation

The core test separates **some** relay drift. Two thirds of the owner-DIFFERENT members fail it, mostly on semantic
quorum together with the headline check. But it cannot do so without rejecting a material share of genuine
same-occurrence members.

The failures sit on both sides of one weakness. Full-text similarity to a small core measures **topic**, not
**occurrence**:
- the same occurrence in a different frame fails (D182 anniversary coverage);
- different occurrences of one storyline pass (D449 campaign events; D626 protest days; non-English members of D399
  pass and fail on embedding quality).

The small F2 denominator does not rescue it. The point estimate is 33%, and even the lower Wilson bound (12%) exceeds
the 10% limit.

**Plan rule (step 3):** "If either fails, stop: record 'core compatibility does not separate founder occurrence from
relay members' and implement nothing."

- **Recorded:** core compatibility, as specified for DA1, does not separate founder occurrence from relay members on
  the owner's labels.
- **Not done:**
  - no DA1 or DA2 implementation (DA2 uses the same `core_compatible` test for later members, so it inherits the F2
    failure);
  - no H2;
  - no holdout scoring;
  - no change to the plan, thresholds or labels after seeing these results.

## Next gate

There is no automatic next step. Any further Development-admission work needs a **new preregistration** approved by
the owner before measurement, for example a different occurrence signal than topic-level full-text cosine. These
results and labels may inform it only as **development evidence**. The labels stay frozen, and the Phase 2 holdout
stays unused.
