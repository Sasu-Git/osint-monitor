# Development admission: acceptance gate (pre-registered)

Applies to every variant DA1–DA4 against DA0, on the frozen development data (`DATASET-MANIFEST.md`). Thresholds are
fixed now, before any measurement. **Every line must pass**; there is no composite score. Baselines in brackets are
the current code.

## Overmerge control (must improve)

| # | Metric | Harness | Pass |
|---|---|---|---|
| G1 | Giants split: the Development holding the L1 founding occurrence keeps ≤ 20% of its L2-DIFFERENT sampled members | H2 | for **≥ 6 of 8** giants, and pooled over the 8 giants |
| G2 | Relay-signature Developments (long + chain, the forensic definition) | H2 | count and their items each **≤ 50%** of DA0's |
| G3 | Defect-set OVERMERGE cases fixed | H1 rescoring | **≥ DA0 + 6** (T24 reference: +8) |
| G4 | Phase 2 development DIFFERENT pairs kept together [22/100] | H1 | **≤ 19/100** |

## SAME preservation (must not regress)

| # | Metric | Harness | Pass |
|---|---|---|---|
| G5 | Continuity recall [43/58] | H1 | **≥ 42/58** (at most 1 pair lost) |
| G6 | SAME kept apart [15/58] | H1 | **≤ 16/58** |
| G7 | Late attachment / ID stability: cross-tick SAME retained [16/19] | H1 | **≥ 16/19** (no loss) |
| G8 | Defect-set SAME controls [13/13] | H1 | **13/13** |
| G9 | Owner-approved SAME cases (C034/C103, C064, C076, C018/C082; recall cases R012, T034, T041) | H1 | **all kept** where DA0 keeps them; the recall cases no worse than DA0 |
| G10 | Giants: L2-SAME sampled members kept in the founder's Development | H2 | **≥ 90%** pooled |
| G11 | Large-occurrence controls: L3 members labelled SAME, in Developments the owner labelled one occurrence | H2 | **≥ 90%** kept. If no candidate is labelled one occurrence, G11 is *not applicable* and is reported so |
| G12 | Identity gold rev 4 development correct | H1 | **≥ DA0** |
| G13 | Clustering out-of-sample cross-source SAME [44/49] | H1 | **≥ 43/49** |

## Stability and policy (must hold)

| # | Metric | Harness | Pass |
|---|---|---|---|
| G14 | Small controls with membership identical to DA0 | H2 | **≥ 57/60**; each changed control listed and reviewed |
| G15 | Unnecessary splits: L2- and L3-SAME members ending outside the founder's Development | H2 | **≤ 10%** |
| G16 | Single-source Developments | H1, H2 | **0** |
| G17 | Duplicate memberships | H1, H2 | **0** |
| G18 | Situation code, Situation config and the cross-language stage | diff | **unchanged**; cross-language stays disabled |
| G19 | Mixed-Development rate, Phase 2 development [12/31] | H1 | **≤ DA0** |

## Reported, not gated (round 1)

- Relation BLOCKED_BY_IDENTITY pairs separated (of 22).
- Size and span distributions.
- Maximum member-to-core distance.
- Relay depth.
- Developments created per 1,000 items.
- Dedup-path attachments.
- Situation impact on a snapshot copy.
- Spanish/Italian (F2) giants, separately.

## Feasibility gate (before any implementation; H3)

- **F1:** DA1 would reject **≥ 60%** of L2-DIFFERENT sampled members of the 8 giants.
- **F2:** DA1 would reject **≤ 10%** of L2-SAME sampled members.

If either fails: stop, and implement nothing.

## Holdout veto (once, after the candidate is frozen)

The Phase 2 holdout (2026-08-31; already scored for Phase 2 and T24, so a regression check, not an unbiased
estimate) must keep **recall ≥ 7/10** and **ID stability ≥ 5/8**. Failing it rejects the candidate. The holdout is not
reused for a variant or for tuning. Sealed holdouts are never used.

## Deployment (outside this gate)

A passing candidate becomes its own deploy candidate under the deployment runbook, after Candidates A and B, with its
own approval. Existing Developments are not repaired by it.
