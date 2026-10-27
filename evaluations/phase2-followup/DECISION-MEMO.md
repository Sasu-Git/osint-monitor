# Phase 2 follow-up: decision memo (2026-10-27)

Written during the Candidate A soak; read-only and evaluation-only. Every number below comes from committed evaluation
artifacts and is cited with its source and commit in [`EVIDENCE.md`](EVIDENCE.md), which uses the source keys DS, FR, P2AH
and so on. No pipeline was replayed, and the sealed holdouts (`evaluations/relations/holdout/`,
`evaluations/identity/holdout-xlang/`) were not opened. For the Phase 2 holdout only aggregate tallies already
committed were read.

## Bottom line

1. **Overmerge (A) is the largest residual defect and the one that blocks Phase 3.** It accounts for:
   - 42 of the 128 frozen defect cases;
   - 22 of the 100 DIFFERENT pairs in the Phase 2 development windows still kept together (17 of them whole-storyline,
     a class Phase 2 did not move);
   - 22 scored relation cases (13 canonical positives) blocked because two occurrences became one Development.
2. **Recall (B) is mostly cross-language** (43 of 62 recall defects). The cross-language stage stays disabled: nothing
   since the 2026-10-09 decision changes its measured merge precision (0.375). The same-language misses (17) are spread
   over six root causes, with no single lever.
3. **Most non-surfacing is correct (C).**
   - 72% of unsurfaced live items are excluded by policy.
   - Single-source holdback and the commentary rules behave as designed.
   - One gap remains open: the 149 relation sides that are not surfaced have never been split into correct and
     recoverable.
4. **Recoverable non-surfacing (D) is small where it is evidenced**: 19 gold SAME pairs, of which 4 are accepted or
   precision-traded costs. The 1,689-item review share is an upper bound only. The coverage sample is 44 of 120
   labelled, so its rates are interim and drive no decision yet.

**Recommended next experiment** ([`EXPERIMENT-PLAN.md`](EXPERIMENT-PLAN.md)): a cross-day **action-divergence guard**
in development segmentation. Two report headlines more than 24 h apart whose main actions fall in different general
action classes are not linked. It goes behind a no-code feasibility gate. It targets exactly the failure that blocked
T24, where time alone could not separate the cases.

## A. Overmerge: two real occurrences become one Development

| | |
|---|---|
| Observed cases | **42** OVERMERGE in the defect set (DS). By root cause: 22 a relation pair inside one Development; 14 distinct occurrences of one storyline linked above threshold; 5 a later cluster extending a Development with a different occurrence (overlap-merge); 1 whole storyline. Phase 2 development: **22/100** DIFFERENT pairs kept together, 17 whole-storyline and 5 late overlap-merge (P2AH; baseline 31/100). Relations: **22** scored blocked cases in 11 Developments, 28 with unscored, **13** canonical positives, 6 of 30 runtime-type positives (ELIG, CGR). Live: Development 447, 13 unrelated Spanish items (AH-EV) |
| Representative examples | **Cross-day storyline creep:** the Christa Pike Development 19 (14 items: Supreme Court denies bid / appeals court halts / execution fails / Tennessee halts executions; T012-T014, T040); the Hormuz Development 3 (Trump rejects plan / Iranian minister / Trump expects talks / "apocalyptic war"; R014, R115, R132, T018, T029, T037, T045); Ebola trial vs doses arriving (A021/A022). **Same-day distinct actions:** the Pope in Lourdes (R046), Xi at the White House (B008), Netanyahu in the UAE (R100). **Whole storyline:** French protest wave (G07). **Commentary absorbed:** D054, D055/D071, D064, D066 (owner notes) |
| Likely subsystem | **Link rule and segmentation.** The wrong links sit at cosine 0.53-0.83, above the 0.53 threshold (DID). No segmentation guard separates distinct actions of one storyline. The **overlap-merge** in Development identity (a later cluster extends an existing Development) carries the 5 late cases |
| Generalizable fix? | **Cross-day: possibly**, and untested. FR: creep "needs an action-level signal". The tried rules failed or were rejected: T24 occurrence span (time alone; the overmerges are 31-41 h apart and the true pairs it broke are 32-34 h apart); R1 no chain across a guard (cost equals gain, 6 vs 7); T12; a higher es/it threshold (not separable). **Same day: no**. FR: "no text signal separates them" |
| Regression risk | **High.** Any guard that cuts above-threshold links risks multi-day same-occurrence reports (T24 lost holdout H003/H017: recall 7/10 to 5/10, ID stability 5/8 to 3/8). Existing Developments are never merged back (ID stability), so a wrong cut is permanent |
| Proposed gate | Defect set (42 OVERMERGE fixed, 23 controls kept); Phase 2 development tallies; identity gold rev 4; clustering out-of-sample cross-source SAME (segmentation v2: 44/49); the Phase 2 holdout as a one-time **veto** (recall at least 7/10, ID stability at least 5/8) |

## B. Split / attachment recall: one occurrence not kept together

| | |
|---|---|
| Observed cases | Defect set: **43** cross-language misses (21 one side outside a Development, 14 two Developments, 8 neither side in one); **17** same-language misses; **2** same-language splits; **0** late-attachment misses at the defect-set baseline. Phase 2 development: **15/58** SAME pairs kept apart (segmentation interaction 5, missed continuation 6, other / same tick not grouped 4; P2AH; baseline 17/58). Relation benchmarks: 10 SAME_DEVELOPMENT suspects, all already in the defect set (8 cross-language, 2 split) |
| Representative examples | **Cross-language:** Sánchez snap election (it / es / en, V009/V024); Siberian plague (en vs es, G14); RAF Fairford (G12/G13; owner regression cases). **Same-language:** FlyDubai diversion cut by the place guard (C066/C092/C113, owner rule P7); Commission proposal vs its Q&A / factsheet (C034/C103, kept below the layer by single-source holdback); OCCAR contract just under threshold (B002, cosine 0.524). **Split:** U131 (it, two ticks), U110 (es) |
| Likely subsystem | **Cross-language:** the English-only embedding with the cross-language stage disabled. **Same-language:** six root causes over 17 cases: below threshold or noise 4; one side left out 3; place guard 3; report not clustered 3; headline-similarity guard 2; later item not joining 2. **Splits:** reconcile never merges existing Developments, by design |
| Generalizable fix? | **Cross-language: not as built.** Stage on gave P 0.41 / R 0.38; stage-added merges 12 true vs 20 false (0.375). The best guard variant E5 still failed (one new Phase 2 false merge; a limit of 0) (XTP, XGR). **Same-language: no single lever.** The 0.45-0.53 secondary link rule added **0 true and 13 false** joins (PCH); the place guard is owner policy (P7). **Splits:** only by merging existing Developments, which conflicts with ID stability |
| Regression risk | High for any threshold or candidate widening (prior: 0/13); high for cross-language (false merges across languages are hard to see) |
| Proposed gate | Defect set recall classes; Phase 2 merge failures; the cross-language benchmark on gold rev 4 (P7 anchors as the acceptance guard, owner 2026-10-07) only if B is reopened |

**Cross-language decision unchanged (KEEP DISABLED).** The interim coverage sample has 9 of 12 cross-language
candidates labelled SHOULD_JOIN (Wilson 47-91%). That measures something different: whether an item has a true
counterpart among high-similarity candidates, not whether automatic merges are precise (0.375). It covers 12 of 30
cases, so it is not decision-grade. Revisit only when the 30 cross-language cases are labelled. Even then, the
experiment would be candidate generation with P7 anchors as the guard (the 2026-10-07 owner scope), never "multilingual
cosine alone merges".

## C. Correct non-surfacing

| | |
|---|---|
| Observed cases | Defect-set controls **23** (13 SAME, 10 DIFFERENT), 5 of them correctly outside any Development. Live coverage (9,002 items): **4,240** of 5,929 unsurfaced (72%) are policy: never formed a viable cluster 2,760; structured records 831; commentary / analysis 572; single-source holdback 77 (COV). Single-source Developments: 1 to **0** after Phase 2; roundup contamination 1 to 0 (P2B vs P2AH) |
| Representative examples | A Commission proposal and its own Q&A from one outlet held below the layer (C034/C103); "AI accord vs 'is it enough?' commentary" kept apart (C044); GDELT headline-only items (owner-accepted cost: loses C006, fixes C033) |
| Likely subsystem | Working as designed: single-source holdback; the commentary / roundup rules (cd78d97); the GDELT headline-only rule |
| Generalizable fix? | Not applicable. Keep these as invariants |
| Regression risk | Any recall work (B, D) can erode them. They are regression metrics for every experiment |
| Proposed gate | 0 single-source Developments; roundup Developments not above 1; the commentary share of Development members not rising; controls unbroken |

**Open gap:** 149 of 173 scored relation sides are not surfaced (CGR). Only 21% of eval-window items belong to any
Development, and no committed evaluation splits those 149 into correct and recoverable. Phase 3 should not resume on a
coverage argument until that split exists.

## D. Recoverable non-surfacing (only where evaluation evidence supports it)

| | |
|---|---|
| Observed cases | **19** gold SAME pairs where neither item is in any Development (DS). Of the **11 same-language** pairs, 2 are GDELT headline-only (an accepted cost) and 3 are below the threshold (B002, B004, G01: "only a lower threshold, which is a precision trade"). There are **8 cross-language** pairs. Owner verdicts on items left unattached: R012, T034, T041 (T033 / T039 are GDELT, an accepted cost). Coverage sample, **interim 44/120**: below threshold 4/11 SHOULD_JOIN (36%, Wilson 15-65%); segmentation-rejected es 1/8 (12%); segmentation-rejected it 3/13 (23%); cross-language 9/12 (75%) |
| Representative examples | B007 (Air Force China think tank, cut by headline similarity); C005 (UN Press nuclear); C064 (Security Council record vs summary); C076 (Moldova drone, same attack) |
| Likely subsystem | Mixed: the link threshold, the segmentation guards, and the English-only embedding |
| Generalizable fix? | Not yet shown. Whether each of the 19 pairs has two independent origins (and so would pass single-source holdback) is not recorded. The segmentation strata look mostly correct in the interim labels (12-23% recoverable), which supports leaving segmentation alone |
| Regression risk | As in B |
| Proposed gate | Finish the 120-case labels. Then decide per stratum: a high below-threshold rate points to candidate generation, not the threshold (PCH); a low segmentation rate leaves segmentation unchanged; cross-language as above |

## What is missing (does not block the experiment below)

- **Owner verdicts on the 128-case defect set: all null (DSV).** The defect classes come from the frozen gold labels,
  not from owner review of each defect.
- **Coverage sample:** 76 of 120 labels outstanding.
- **Relation sides:** no correct-vs-recoverable split of the 149 not-surfaced relation sides.
