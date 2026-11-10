# Situation membership: project learnings

## 2026-11-10: today's membership mechanism is not an acceptable v2 baseline

**Evidence.** Frozen 126-case subsample (`evalset/subsample/`), owner labels frozen in `57fef39`, scored in `e8943fd`
(`results-first.json`, `results-final.json`). The system scored is today's runtime membership (`key.json`
`current_member`, 2026-11-03 snapshot). The results are not altered here.

**What we learned.**

- The current Situation-membership mechanism is **not acceptable as the baseline for v2**.
- The blind owner labels (first answer per case) and the final adjudicated labels **agree on the failure**.
- The failure is **not only false positives**. The system also **drops too many true members**:
  - MEMBER retention about 81–86% (0.810 blind, 0.857 adjudicated);
  - precision of current Situation memberships about 68–70% (0.681 / 0.696);
  - commentary is usually admitted when it should not be (1 of 7 blind, 1 of 5 adjudicated owner-`CONTEXT` cases
    rejected);
  - Developments that belong to other Situations are often admitted (only 15/24 blind and 18/27 adjudicated
    `OTHER_SITUATION` cases rejected);
  - seed preservation was **not** the problem (0 positive-seed regressions, all 10 positive seeds kept).
- Actor overlap plus today's scope logic (a weighted score with no scope requirement) is **insufficient** for
  Situation membership.
- The thresholds (≥ 90% members kept, ≥ 70% NOT_MEMBER rejected, 0 seed regressions) were **PROPOSED and not formally
  approved before scoring**. They are not preregistered hard gates and must not be described as such. The substantive
  conclusion does not depend on them: blind and adjudicated labels both show that current Situation membership needs a
  redesign.
- The 126-case set is now **design evidence** (a development / diagnostic set), not a clean unseen acceptance holdout.
  Any v2 candidate whose design it informs must be accepted on a **fresh holdout** drawn after the v2 contract is frozen.

**Structural failure modes found during the review.**

| Failure mode | Example |
|---|---|
| Party or ideology terms become actors | `Democrat` keys `democrat-united-states` |
| Person-name variants are not normalised, so one person satisfies the two-actor creation rule | `javier-milei-milei`, `elon-musk-musk`, `christa-pike-pike`, `machado-maria-corina-machado`, `emmanuel-macron-france-macron`, `bukele-el-salvador-nayib-bukele` |
| Generic half coverage via "United States" | any US-led Development is a candidate for every "X – United States" Situation (`democrat-united-states`, `russia-united-states`) |
| No topic split at Situation creation | Macron's Gulf visit and his response to student protests share one Situation |
| Merged Developments contaminate membership | D49 (Pope headline, 17 reports of the Xi–Trump summit), D542, D439, D810 |
| No conditional / pending membership state | S273: a member only once suspicions are confirmed; membership is decided once and never revisited |
| No disaster-type + country Situation key | `rachel-simon` exists only because storm names were read as person names |
| Accidental Situation names and scopes differ from the de-facto topic | `democrat-united-states` is in practice "US midterms"; four Situations' own founders were labelled non-members by the owner |

**How to apply.** Use the 126 cases for diagnosis only. Do not tune a candidate to individual case outcomes. Accept v2
only on a fresh holdout with a frozen contract, frozen code, frozen sample and approved gates. See
`CONTRACT-V2-R2.md` and `PREREGISTRATION-V2-R2.md` on `design/situation-membership-v2-r2`.
