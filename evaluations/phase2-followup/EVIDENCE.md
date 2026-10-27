# Phase 2 Development-identity: evidence for the decision memo

Collected 2026-10-27, read-only from committed refs in `C:\Users\EugenioVardiero\osint-monitor`. Sealed paths
(`evaluations/relations/holdout/`, `evaluations/identity/holdout-xlang/`) were never opened. No pipeline, replay or
benchmark was run. All numbers are copied from committed files, or are exact counts taken from committed JSON/YAML
with a few lines of Python (marked "counted").

Citation format: `path@branch (commit that last touched the file)`.

## Branch heads at collection time (two moved since the brief)

| branch | brief said | head now | note |
|---|---|---|---|
| fix/identity-defects | 7fdd674 | 7fdd674 | |
| feat/phase3-relations | bbae126 | bbae126 | eval/relations-review-ui (0233855) is an ancestor of it |
| eval/relations-review-ui | 0233855 | 0233855 | |
| fix/actor-hygiene | 79b7892 | **7b1b8f0** | only adds `evaluations/actor-hygiene/CANDIDATE-B-READINESS.md`; defect README/RESULTS and runs are unchanged |
| eval/coverage-diagnosis-20261013 | 528c020 | **d27f1bc** | only adds `review/labels_tool.py` and edits `review/score.py`; FINDINGS.md is unchanged (df33560) |
| fix/cross-language-identity | 0eff3ea | 0eff3ea | |
| main | | 5f046b3 | |

## Source key

| key | file |
|---|---|
| DS | `evaluations/identity/defects/defect-cases.json` + `defect-review.md` + `manifest.yaml` @fix/identity-defects (e98a0fe). 128 cases, baseline identity code 0eff3ea, cross-language stage disabled, frozen 2026-10-09T13:20:26Z |
| DSV | `evaluations/identity/defects/owner-verdicts.yaml` @fix/identity-defects (e98a0fe): **all 128 entries are null** (no owner verdict recorded on the defect set) |
| FP | `evaluations/identity/defects/fix-plan.md` @fix/identity-defects (pre-registered 6afe152; amendment 1 in 7fdd674) |
| FR | `evaluations/identity/defects/followup-results.md` @fix/identity-defects (7fdd674) |
| P3S | `evaluations/relations/PHASE3-STATUS.md` @feat/phase3-relations (bbae126) |
| ELIG | `evaluations/relations/runtime-eligibility-rev2.yaml` @feat/phase3-relations (a4724c6) |
| CGR | `evaluations/relations/candidate-generation-results.md` @feat/phase3-relations (2264b22) |
| RTG | `evaluations/relations/runtime/gold/runtime-gold.yaml` @feat/phase3-relations (28c69e4) |
| TGG | `evaluations/relations/runtime-targeted/gold/targeted-gold.yaml` @feat/phase3-relations (bbae126) |
| OD7b | `evaluations/relations/gold/owner-decisions-2026-10-07b.yaml` @eval/relations-review-ui (0233855) |
| ORS | `evaluations/relations/owner-review-summary.md` @feat/phase3-relations |
| AH-README / AH-RESULTS / AH-EV | `evaluations/entities/defects/2026-10-16/{README.md, RESULTS.md (b1f1ee9), evidence.json}` @fix/actor-hygiene |
| COV | `evaluations/coverage/2026-10-13/FINDINGS.md` @eval/coverage-diagnosis-20261013 (df33560) |
| COVR | `evaluations/coverage/2026-10-13/review/{FREEZE.md, sample-manifest.json}` @eval/coverage-diagnosis-20261013 |
| P2B / P2AH / P2F / P2H | `evaluations/identity/runs/{phase2-baseline.json (4ad3def), phase2-dev-actor-hygiene.json (79b7892), phase2-dev-final.json, phase2-holdout.json (3dab07b)}` @fix/actor-hygiene |
| P2B-md / P2H-md | `evaluations/identity/phase2-baseline.md`, `phase2-holdout.md` (3dab07b) @fix/actor-hygiene |
| XS / XGR / XTP / XRS | `evaluations/identity/{xlang-status.md (0eff3ea), xlang-guard-results.md (712875e), xlang-guard-tuning-plan.md (ab83607), runs/rev4-xlang-rescore.json (f4d9212)}` @fix/cross-language-identity |
| GDH | `evaluations/identity/decisions/2026-10-08-gdelt-headline-only.yaml` @fix/cross-language-identity |
| CLU | `osint_monitor/processors/clustering.py` @main (34300c6), lines 30-37 |
| SEG / PCH / DID | `evaluations/clustering/{segmentation-compatibility.md (85a9a0f), phase-c-holdout.md (6a9ae6f), development-identity-diagnosis.md (262b5f9)}` @main |

## Defect set overview (DS)

| defect class | cases | blocks a Phase 3 endpoint | memo bucket |
|---|---:|---|---|
| OVERMERGE | 42 | yes (42) | A |
| CROSS_LANGUAGE_MISS | 43 | "disputed"/n.a. (43) | B (cross-language) |
| SAME_LANGUAGE_RECALL_MISS | 17 | yes (17) | B (same-language) / D |
| SPLIT | 2 | n.a. | B (split) |
| LATE_ATTACHMENT_MISS | 0 | | B (late attachment): **0 in the defect set** |
| AMBIGUOUS | 1 | unknown | - |
| CORRECT_BEHAVIOR (controls) | 23 (13 SAME, 10 DIFFERENT) | no | C (controls) |
| **total** | **128** (105 wrong, 23 correct; FP) | | |

By source (DS manifest.yaml `by_source`): IG = identity gold (OVERMERGE 23, AMBIGUOUS 1, SAME_LANGUAGE_RECALL_MISS 17,
CROSS_LANGUAGE_MISS 35); RB = relation gold rev 2 (OVERMERGE 22); RT = runtime/targeted relation benchmark
(CROSS_LANGUAGE_MISS 8, SPLIT 2); CT = controls (CORRECT_BEHAVIOR 23).

By window (counted from DS): OVERMERGE 2026-09-30-multilingual 14, 2026-09-27-live 9, 2026-08-21 7, 2026-10-03-live 5,
2026-09-29-live 4, 2026-09-25 2, 2026-08-31 1. CROSS_LANGUAGE_MISS 2026-09-30-multilingual 21, 2026-10-05-live 19,
2026-10-08-live 3. SAME_LANGUAGE_RECALL_MISS 2026-09-30-multilingual 14, 2026-09-25 3.

---

## A. Overmerge

### A.1 Defect set: 42 OVERMERGE cases (DS), by suspected root cause (counted)

| root cause (DS `root_cause`) | cases |
|---|---:|
| relation pair inside one Development (relation gold says two distinct occurrences) | 22 |
| distinct occurrences of one storyline linked above the similarity threshold in one cluster; segmentation did not cut them | 14 (2-item Dev 6, 3-item 4, 12-item 4) |
| a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) | 5 (D048, D055, D058, D062, D071) |
| whole-storyline overmerge (shared Development [5], 12 items) | 1 (D100) |

Representative examples (DS):

- **Cross-day storyline creep (follow-ups merged):** D101/D102/D103/D104 = RB T012/T013/T014/T040 (`follow_up_to`),
  2026-10-03-live, Development 19 (14 items): "US Supreme Court denies Christa Pike's last-ditch bid" / "US appeals court
  halts Tennessee execution of Christa Pike" / "Christa Pike's execution ... fails" vs "Tennessee halts executions after
  Christa Pike survives two lethal injection attempts".
- **Crisis sequence collapsed (Hormuz):** D019, D022-D027 = RB R014 (`reaction_to`), R115, R132 (`co_caused_with`),
  T018 (`reaction_to`), T029, T037 (`follow_up_to`), T045; 2026-09-27-live, Development 3 (5 items): "Tehran awaits
  official response as Trump rejects Hormuz plan" vs "Iranian minister says only negotiation can end conflict" vs
  "Trump expects new Iran talks despite rejecting deal offer" vs "Tehran ... ready for 'apocalyptic war'".
- **Distinct actions within one visit/person (same day):** D021 = RB R046 (`same_convened_event`), Pope in Lourdes,
  Development 2 (3 items): "Pope pledges action on clergy child abuse in meeting with French survivors" vs "'Scourge' of
  abuse must be rooted out, says Pope during Lourdes visit". D017 = IG B008, Development 3: "Trump gives Xi a tour of his
  pet White House building projects" vs "Xi got Trump's red carpet welcome - but not everything he wanted". D028 = RB R100
  (`same_convened_event`): "UAE confirms Netanyahu visit to Abu Dhabi" vs "Israel security agency files complaint over TV
  report that Netanyahu visited UAE".
- **Calamity lifecycle collapsed:** D005/D006/D011 = IG A021/A022, RB R082 (`same_calamity_lifecycle`), 2026-08-21,
  Development 3 (Ebola vaccine trial vs 16,000 doses arrive). D012 = RB R030, 2026-08-31 Development 2 (Malaysia haze vs
  Borneo orangutans). D020 = RB R031, Development 9 (Nepal floods one month on vs new floods).
- **Late overlap-merge (es/it):** D048/D055/D062/D071, 2026-09-30-multilingual Development 9 (12 items): Trump
  Super-Intelligence order / AI accord vs "Politica e scienza divise, gli esperti..." commentary / diesel export ban.
- **Whole-storyline:** D100 = IG G07 (owner 2026-10-07: "two days of the protest wave"), 2026-10-03-live Development 5
  (12 items): "More than 400 detained as France student protests escalate" vs "Dozens hurt and hundreds arrested in wave
  of French school protests".
- **Commentary/testimony merged into the report (owner notes):** D054 (C017, "one is a commentary on the other"), D055 /
  D071 (C022 / C106, "commentary_or_analysis"), D064 (C079, "divide testimony from actual event reporting"), D066 (C094,
  "one is the commentary ... vs the raid itself").

### A.2 Relation cases blocked because two occurrences became one Development

| measurement | value | source |
|---|---|---|
| BLOCKED_BY_IDENTITY, scored relation gold cases | **22** (in 11 Developments, counted) | ELIG `counts.scored`; P3S says "22 scored gold pairs in 12 Developments" (12 = including unscored) |
| BLOCKED_BY_IDENTITY, all cases (incl. unscored) | **28** | ELIG `counts.all` |
| BLOCKED_BY_IDENTITY among canonical positives | **13** | ELIG `counts.canonical_positives` |
| runtime-type canonical positives blocked | 6 of 30 (same_calamity_lifecycle 2 of 13: R030, R082; same_convened_event 2 of 10: R046, R100; reaction_to 2 of 7: R014, T018) | CGR |
| scored blocked cases by gold label (counted) | NO_RELATION 8, follow_up_to 5, reaction_to 3, same_calamity_lifecycle 2, same_convened_event 2, co_caused_with 1, commentary_on 1 | ELIG |
| per Development (scored, counted) | 2026-09-27-live D3 (Hormuz) 7 (+1 unscored R019 = 8; P3S text says "9 pairs"); 2026-10-03-live D19 (Pike, 14 items) 4 (+1 unscored T041); 2026-08-21 D5 (West Bank) 2; 2026-09-29-live D6 (Najaf flights) 2; one each: 2026-08-21 D4 (Carney), D3 (Ebola); 2026-08-31 D2 (haze); 2026-09-27-live D9 (Nepal), D2 (Pope); 2026-09-29-live D8 (Netanyahu), D16 (Malaysia/Rohingya) | ELIG |

Note the Hormuz count discrepancy: ELIG holds 8 BLOCKED cases on 2026-09-27-live D3 (7 scored), P3S text says 9.

### A.3 Live over-merge: Development 447 (actor-hygiene)

AH-README D1 item 4 and AH-RESULTS "Not done here": Development 447 "merges unrelated Spanish items"; "a
Development-identity over-merge, recorded for the identity defect review. It is not an entity fix." AH-EV lists its
**13 items** (counted), all Spanish: Musk midterm donations (Clarín 8556, France 24 Español 9382); US ambassador to
Greece Kimberly Guilfoyle resigns/dismissed (El País 9392, Clarín 9403, BBC Mundo 9840, France 24 Español 10064, Europa
Press 10171); judge extends CNN/Politico/MS NOW White House access (Europa Press 10165, El País 10493); Maine senator
distances from Trump (El País 10426); press secretary Katie Zacharia (Clarín 11263, El País 11323, BBC Mundo 12540).
Principals: Trump, Donald Trump, EEUU, Estados Unidos, Washington, EE. UU., EE.UU. Not in the frozen defect set (live
soak, after it was frozen).

Same RESULTS: four Situations rest on one actor counted twice or on storms (`elon-musk-musk`, `rachel-simon`,
`christa-pike-pike`, `donald-j-trump-united-states`); entity-level, not identity, but `christa-pike-pike` sits on the
Pike storyline.

### A.4 Phase 2 error ledger (split failures = DIFFERENT kept together)

| run | whole-storyline overmerge | late attachment | single-source promotion | roundup contamination | source |
|---|---:|---:|---:|---:|---|
| phase2-baseline (pre-Phase 2) | 17 | 12 | 1 | 1 | P2B (counted; = P2B-md) |
| phase2-dev-final / phase2-dev-actor-hygiene (identical) | 17 | 5 | 0 | 0 | P2F, P2AH (counted) |
| phase2 holdout 2026-08-31 (aggregate only) | 1 | 0 | 0 | 0 | P2H (counted) |

Note: "late attachment" in the Phase 2 ledger is a split failure (a later-tick cluster extends a Development with a
*different* occurrence, overlap-merge), i.e. an **overmerge** mechanism, not an attachment-recall miss.

Actor-hygiene ledger examples:
- whole-storyline overmerge (17): A002 (Carney "miscalculation" vs "not to be trusted"), A021/A022 (Ebola trial vs
  doses), A023/A013 (West Bank settlement / settlers / activists), B008 (Xi tour vs red-carpet), B011 (Pakistan strikes),
  C007/C012/C017/C112 (Trump AI order cluster, Development 10, es/it), C026/C033 (Iran rial vs "Iran received US reply"),
  C079 (Gaza testimony vs strike), C094 (US Senate vote vs West Bank raid), C105 (Burnham), C115 (DW aviation sanctions
  vs State Dept release).
- late attachment (5): C002, C022, C073, C106 (all Development 10, AI order vs expert commentary / diesel ban), C037
  (French public-worker protests vs Maricarmen eviction, Development 9).

### A.5 Diagnoses and what was tried

- DID (main): pre-Phase 2 benchmark, 54 clusters, 32 mixed; 60 absorbed units: analysis/explainer 14, different action
  same actors 13, reaction 8, follow-up 6, repeated action different date 6, rolling coverage 4, unrelated topical 4,
  unrelated template 3, preview 1, policy response 1. "50 of 60 absorbed units link directly to the core (cosine >=
  0.53)"; "joining links sit well above threshold (0.53-0.83; repeated actions 0.60-0.76), so no threshold change
  separates them without destroying recall". Mixed clusters median span 22.5 h (max 46 h) vs pure 5.0 h.
- PCH (main): "Storyline-level over-merging is the main error (33 of 46 mixed clusters in dev + hold-out merge
  developments of one storyline)".
- FP diagnosis table: storyline creep across days "distinct occurrences 14-41 h apart linked one report at a time; no
  guard fires (cosine 0.53-0.82)"; chains across a guard (C012, C037, C073, C094, C112, C115); same-day distinct actions
  (Pope R046, Netanyahu R100, Malaysia T009, Xi B008) "nothing in the text separates them"; es/it "SAME and DIFFERENT
  pairs have the same cosine distribution (median 0.44 vs 0.47)".
- FR (T24, 24 h occurrence span, implemented, **off**): defect set correct 23 -> 31 (8 OVERMERGE fixed: D004 A002,
  D008 R013, D009 R029, D010 R060, D074 C115, D101-D103 Pike T012-T014; 0 broken); identity gold rev 4 (232 scored)
  157 -> 161; Phase 2 dev split failures 21/100 -> 17/100, mixed 12/31 -> 9/29; **Phase 2 holdout recall 7/10 -> 5/10,
  ID stability 5/8 -> 3/8 (H003, H017 lost)**. "The overmerges T24 fixes are 31-41 h apart (A023 31.8 h, A002 39.1 h,
  Pike T012 41 h); the one-occurrence pairs it breaks in the holdout are 32-34 h apart. No time threshold separates
  them." Situation impact 78 -> 83 Developments, 6 -> 6 Situations.
- FR remaining blockers: cross-day creep (Pike T040, Ebola A021/A022, French protests G07, Hormuz sequence (7)) "needs
  an action-level signal"; chains across a guard (forbidding them costs C011, C014, C030, C036, C043, C058, C077);
  same-day distinct actions "no text signal separates them".
- FP rules rejected: R1 no chain across a guard (recall cost equals gain: 6 vs 7); T12 (would split 9 correct SAME
  merges 12-24 h apart); higher es/it threshold (11 SAME together vs 14 DIFFERENT together, not separable).

---

## B. Split / attachment recall

### B.1 Defect set (DS)

| sub-class | cases | shape (counted from DS developments) |
|---|---:|---|
| CROSS_LANGUAGE_MISS | 43 | one side in a Development, other not 21; two different Developments 14; neither side in a Development 8 |
| SAME_LANGUAGE_RECALL_MISS | 17 | neither side in a Development 11; one side in, other not 6 |
| SPLIT (one occurrence, two Developments, same language) | 2 | both two different Developments |
| LATE_ATTACHMENT_MISS | **0** | - |

SAME_LANGUAGE_RECALL_MISS root causes (counted): same-tick items not grouped (below link threshold / noise) 4; one item
in a Development, other left out 3; segmentation cut (disjoint_locations) 3; report not clustered 3; segmentation cut
(headline_similarity) 2; later item did not join earlier item's Development 2.

All 43 CROSS_LANGUAGE_MISS have root cause "English-only clustering embeddings; the cross-language stage is disabled
(rejected 2026-10-09)".

Examples:
- **Split (same language, formed in different ticks):** D123 = RT U131, 2026-10-05-live D19 vs D22 (it): "Marea sociale
  contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne" vs "Spagna, il Psoe in pressing su Sanchez
  per il voto anticipato". D127 = RT U110, 2026-10-08-live D33 vs D17 (es, Maduro/Flores vs Cabello). FP: "formed in
  different ticks; reconcile never merges existing Developments (ID stability)".
- **Cross-language, two Developments:** D110/D112 = IG V009/V024 (Sánchez snap election, it D22 vs es D18 / en D30);
  D107 = IG G14 (Siberian plague, en D40 vs es D27; owner regression case); D085 = IG V020 (Morocco first female PM, it
  D16 vs es D19).
- **Cross-language, one side outside:** D105/D106/D115/D117 = IG G12/G13/V045/V054 (RAF Fairford bombers, en D17 vs es
  not in a Development; owner regression cases); D069 = IG C104 (Pentagon statement D5 vs Italian report).
- **Same-language, place guard:** D061/D065/D073 = IG C066/C092/C113 (FlyDubai diversion, Italian outlets; one side in
  D24; `disjoint_locations` cut; owner rule P7 forbids outweighing).
- **Same-language, release package:** D057/D068 = IG C034/C103 (Commission proposal vs its Q&A / Factsheet, same outlet,
  one side in D1). FP P1 fix "no effect": single-source holdback keeps them below the layer (FR).
- **Same-language, below threshold:** D014 = IG B002 (OCCAR DDX contract, Breaking Defense vs Defense News; lexical
  doc: cosine 0.524, just under 0.53); D015 = IG B004 (Trump-Xi state dinner, BBC vs SCMP); D075 = IG G01 (Trump ads,
  BBC vs France 24; FP: 0.52).

### B.2 Relation benchmarks: identity splits found (P3S, RTG, TGG)

- Runtime benchmark (155 pairs of distinct Developments): **7 SAME_DEVELOPMENT_SUSPECTED** (U001, U110, U116, U124,
  U131, U143, U151); targeted batch (34 pairs): **3** (P118, P123, P125). Total 10. P3S: "mostly one occurrence
  reported in two languages". All 10 are in DS: 8 as CROSS_LANGUAGE_MISS (D119-D122, D124-D126, D128), 2 as SPLIT
  (D123 U131, D127 U110).

### B.3 Owner identity verdicts routed from relation review (OD7b, 2026-10-07)

| case | verdict | cause (verbatim) |
|---|---|---|
| R012 | SAME | "same-language recall miss (BBC / France 24)" |
| R138 | SAME | "cross-language split (es/it vs en)" |
| T008 | SAME | "same outlet, same day update (Spain's eviction measures)" |
| T034 | SAME | "same-language recall miss (SCMP / Al Jazeera)" |
| T041 | SAME | "late-attachment miss (Christa Pike)" |
| T033, T039 | SAME | "GDELT headline-only item not attached" |
| T025 | DIFFERENT | "distinct days of one protest wave" |
| D19 (2026-09-30-multilingual) | SPLIT_REQUIRED | "mixed: the rial record low plus a separate 'Iran confirms it received the US response' occurrence" |

At the defect-set baseline (0eff3ea) T008, T034, T041 are CORRECT_BEHAVIOR (D097-D099, "blocked relation pair, correct
merge"), so the late-attachment miss T041 is not reproduced there; LATE_ATTACHMENT_MISS = 0 in DS.

### B.4 Phase 2 ledger, merge failures (SAME kept apart)

| run | segmentation interaction | missed continuation | other | total |
|---|---:|---:|---:|---:|
| phase2-baseline | 8 | 7 | 2 | 17 |
| phase2-dev-final / actor-hygiene | 5 | 6 | 4 | 15 |
| phase2 holdout (aggregate) | 1 | 2 | 0 | 3 |

Actor-hygiene examples: segmentation interaction B007 (Air Force China think tank, headline_similarity), C051 (UN live
vs UN Press DRC), C066/C092/C113 (FlyDubai, disjoint_locations); missed continuation C005 (UN Press nuclear), C034/C103
(Commission Q&A / Factsheet), C064 (Security Council record vs summary), C096 (FlyDubai), C104 (Pentagon vs Italian,
cross-language); other (same-tick not grouped) B002, B004, C013 (Russian strikes Kyiv Independent vs France 24 live),
C076 (Moldova drone vs same attack).

### B.5 Cross-language is the largest recall bucket; prior decision in "Prior decisions"

FP: "English-only model on es/it text ... SAME and DIFFERENT pairs have the same cosine distribution (median 0.44 vs
0.47): similarity carries no identity signal".

---

## C. Correct non-surfacing

- **Controls (DS):** 23 CORRECT_BEHAVIOR (13 SAME, 10 DIFFERENT). 5 controls are "neither side in a Development" and
  correctly so (DIFFERENT): D001 A006 (Singapore fund incentives vs HK tax breaks), D037 C044 (AFCON results), D040
  C071, D042 C086 (two Hegseth directives), D044 C100 (AI accord vs "is it enough?" commentary).
- **Coverage policy share (COV, live 2026-10-13 backup, code 3eda6d0):** 9,002 items; 3,073 (34%) in a Development;
  5,929 (66%) not. Of the unsurfaced, **4,240 (72%) policy**: never_viable_cluster 2,760 (47%; best cross-source cosine
  within 48 h < 0.45, no second report), structured_record 831 (14%), commentary_analysis 572 (10%),
  single_source_holdback 77 (1%). Caveat in COV: some never-viable items "may be a source-coverage gap rather than a
  deliberate exclusion".
- **Single-source holdback works as designed:** FR: P1 release-package links formed "but come from one outlet, so the
  single-source holdback (unchanged) keeps them below the Development layer". Phase 2 baseline had 1 single-source
  Development (2026-09-30-multilingual D1, two Federal Register accreditation items, case C003); after Phase 2: 0
  (P2B vs P2AH, counted). Holdout: 0 (P2H-md).
- **Commentary is not corroboration:** Phase 2 commit cd78d97 "Live blogs, roundups and analysis headlines are
  commentary, not corroboration" (P2H-md). Roundup Developments 3 -> 1 (P2B vs P2AH, counted); roundup contamination 1
  -> 0.
- **Relation gold sides that are lone articles (CGR):** NOT_SURFACED 149 of 173 scored; "Only 407 of 1946 window items
  (21%) belong to any system Development ... most gold sides are lone articles: an explainer, a commentary, one outlet's
  report." Owner, 2026-10-09 (P3S): "Endpoints stay Development IDs only: raw items are evidence, not occurrences."
  NOT_SURFACED by label (scored, counted from ELIG): NO_RELATION 114, same_calamity_lifecycle 11, same_convened_event 8,
  commentary_on 6, reaction_to 6, follow_up_to 2, same_attack_wave 2. **Not found:** a split of the 149 into
  correct vs recoverable non-surfacing; no committed evaluation labels the sides.
- **GDELT headline-only (owner-accepted cost, GDH):** the rule loses C006 (SAME) and fixes C033 (DIFFERENT);
  "Reintroducing metadata to recover C006 would be the wrong trade". OD7b: "headline-only items do not carry full
  evidentiary weight".
- **Below-threshold near misses that are correct separations:** COV caveat "calibration placed distinct occurrences at
  cosine <= 0.51, so many near misses are correct separations" (calibration source: CLU, see Metrics).

---

## D. Recoverable non-surfacing (only where evaluation evidence says it should have joined/surfaced)

- **Defect set (DS), SAME pairs where neither item is in any Development** (gold says SAME, so the occurrence should
  have surfaced): **11 same-language** (D014 B002, D015 B004, D016 B007, D049 C005, D053 C013, D059 C051, D060 C064,
  D063 C076, D075 G01, D078 G08, D079 G09) + **8 cross-language** (D082 V010, D088 V034, D092 V046, D109 V007, D111
  V019, D113 V026, D114 V033, D116 V051). Caveats: G08/G09 are GDELT headline-only (owner-accepted cost, GDH / FP
  "accepted cost"); B002/B004/G01 are sub-threshold (FR: "only a lower threshold, which is a precision trade").
  Whether each pair has two independent origins (i.e. would pass single-source holdback) is not recorded in DS.
- **Owner verdicts of items not attached (OD7b):** T033, T039 (GDELT rial item not attached), R012 (BBC / France 24),
  T034 (SCMP / Al Jazeera), T041 (Pike late attachment).
- **Coverage review share (COV), upper bound only:** 1,689 (28%) of unsurfaced: below_link_threshold 1,028 (17%; cosine
  [0.45, 0.53)), segmentation_rejected 379 (6%), cross_language_candidate 190 (3%; multilingual MiniLM >= 0.60 within
  24 h), other_ambiguous 92 (2%). Concentration: English 25% review, Spanish 69%, Italian 96% (92 of 166 Italian items
  segmentation_rejected); ANSA Mondo 96%, Europa Press 100%; guards per item: headline_similarity 239,
  disjoint_locations 169, analysis_headline 90. Before 10-05 (22 sources) 84% policy, from 10-05 (52 sources) 66%.
  COV: "They also contain true negatives, so the true loss is lower."
- **Coverage recoverability sample (COVR):** frozen 2026-10-13, 120 cases, 30 per stratum (pools: below_threshold 1028,
  segmentation_es 69, segmentation_it 92, cross_language 190); labels SHOULD_JOIN / SHOULD_NOT_JOIN / AMBIGUOUS.
  **No labels are committed on any ref.** An *uncommitted* `owner-labels.yaml` exists in the worktree
  `C:\Users\EugenioVardiero\osint-monitor-deploycheck\evaluations\coverage\2026-10-13\review\` (mtime 2026-10-14):
  44 of 120 labelled by `owner` (SHOULD_JOIN 17, SHOULD_NOT_JOIN 25, AMBIGUOUS 2), 76 unlabelled. INTERIM and
  unscored. Per-stratum split deliberately not computed (FREEZE.md keeps `key.json` closed until review ends; the
  manifest would reveal strata too).
- **Prior benchmark evidence against recovering by threshold or actor-first:** PCH: secondary link rule (0.45-0.53, <=6 h,
  >=2 shared actors) "adds 0 true joins and 13 false joins (7 dev + 6 hold-out)"; actor-first retrieval finds 2 of 3
  low-similarity misses among 180 candidates; recommendation KEEP current clusterer.

---

## Prior decisions

| date | decision | numbers | source |
|---|---|---|---|
| 2026-09-28 | Clustering Phase C: **KEEP** current clusterer; no secondary 0.45-0.53 link rule; no actor-first candidates | rule adds 0 true / 13 false joins over six blind windows; hold-out: current clusterer 6/7 multi-source developments, 7/8 cross-source SAME pairs, mixed 8/14, 52 related-but-distinct + 3 unrelated wrong links | PCH |
| (segmentation) | Segmentation v2 **enabled** (recommended, later on) | out-of-sample (08-31, 09-10, 09-27-live, 09-29-live): cross-source SAME 44/49 vs 46/49 baseline; related wrong links 37 vs 98 (doc text; domain-model.md also says unrelated 13 -> 7); 09-29-live holdout: SAME 15/16 -> 14/16, wrong links 11 -> 6, unrelated 3 -> 0 | SEG; `docs/domain-model.md`@fix/cross-language-identity line 53 |
| 2026-10-01 | Phase 2 identity merged after one-time holdout | holdout 2026-08-31: continuity precision 7/8, recall 7/10, split correctness 19/20, merge 7/10, ID stability 5/8, mixed 1/5, duplicates 0/12, single-source 0 | P2H-md |
| 2026-10-07 | Cross-language model scope: paraphrase-multilingual-MiniLM-L12-v2, candidate generation only; P7 anchors are the acceptance guard; "multilingual cosine alone never merges"; benchmark on gold rev 3 before enabling; same-language misses belong to Phase 2 logic | regression cases RAF Fairford, Siberian plague, R138 | OD7b |
| 2026-10-08 | GDELT headline-only rule **accepted** | Phase 2 dev 43/65 -> 42/63 precision, 43/58 -> 42/58 recall, splits 22/100 -> 21/100, merges 15/58 -> 16/58, ID stability 16/19 -> 15/19, mixed 12/31 unchanged; loses C006, fixes C033 | GDH |
| 2026-10-09 | Cross-language identity **KEEP DISABLED**, branch paused, holdout-xlang sealed | starting point (gold rev 4, 74 additions): stage on P 0.41 / R 0.38 / F1 0.39 (tp 15 / fp 22 / fn 24); stage-added merges 12 true / 20 false (precision 0.375) (XTP). Earlier rescore `rev4-xlang-rescore.json` all.on: tp 12 / fp 21 / fn 27, **precision 0.3636**, recall 0.3077 (XRS; this is the "0.36" cited in COV). Guards E0-E7: none qualifies; **E5 best** (G2 broad anchors k=3 + G3 direct links + G4 exact places): TP/FP/FN 11/5/28, 8 stage-added true / 3 false (limit 2), 1 new Phase 2 false merge C090 (limit 0), 38 links; G1 variants fail mandatory G12/G13 | XS, XGR, XTP, XRS |
| 2026-10-09 | Phase 3 relations **PAUSED** (not rejected), evaluation-blocked upstream | gold rev 2: 2 RUNTIME_ELIGIBLE, 149 NOT_SURFACED, 22 BLOCKED_BY_IDENTITY (scored); runtime benchmark 155 pairs: 0 runtime positives (147 NO_RELATION, 7 SAME_DEVELOPMENT_SUSPECTED, 1 caused_by); targeted 34: 0 positives (31 NO_RELATION, 3 suspects); resume after (1) over-merge follow-up + splits, (2) coverage if chosen, (3) prospective live data | P3S |
| 2026-10-09 | Identity follow-up **BLOCKED**: T24 implemented, off (`max_occurrence_span_hours: null`); P1 removed | see A.5 | FR |
| (FP) | Not implemented by owner rule/constraint: outweigh place guard (contradicts P7), merge existing Developments (breaks ID stability), R1, T12, higher es/it threshold | | FP |
| 2026-10-16 | Actor defects fixed in entity layer, not identity; Development 447 over-merge left to identity follow-up | Phase 2 dev unchanged: 43/65, 43/58, 22/100, 15/58, 16/19, 12/31 | AH-RESULTS |
| owner verdicts on the defect set | **not recorded**: all 128 entries null | | DSV |

---

## Metrics

### Link-rule calibration (CLU, main `osint_monitor/processors/clustering.py` lines 30-37)

"Calibrated on live data: reports of the same development from different outlets score 0.55-0.67 cosine; different
developments on the same topic score <= 0.51; templated single-source feeds ... score 0.45-0.85 among themselves."
`LINK_SIMILARITY = 0.53` ("midpoint between 0.51 (different) and 0.55 (same)"), `MEMBER_SIMILARITY = 0.45`,
`MAX_LINK_HOURS = 72`. Note DID contradicts the separation in practice: over-merging links sit at 0.53-0.83.

### Phase 2 identity, development windows (gold rev 2, 158 scored pairs; counted from run JSON with the formulas of `scripts/render_baseline.py`)

| run | continuity precision | continuity recall | split failures (of DIFFERENT) | merge failures (of SAME) | ID stability | mixed Devs (of labelled) | mixed / multi-item | single-source Devs | roundup Devs | late memberships |
|---|---|---|---|---|---|---|---|---|---|---|
| phase2-baseline (P2B) | 41/72 | 41/58 | 31/100 | 17/58 | 14/19 | 14/33 | 14/39 | 1 | 3 | 12 in 3 Devs |
| phase2-dev-final (P2F) | 43/65 | 43/58 | 22/100 | 15/58 | 16/19 | 12/31 | 12/37 | 0 | 1 | 7 in 3 |
| phase2-dev-actor-hygiene (P2AH) | 43/65 | 43/58 | 22/100 | 15/58 | 16/19 | 12/31 | 12/37 | 0 | 1 | 7 in 3 |
| 0eff3ea + GDELT rule, xlang off, fixed clock (FR / GDH baseline) | 42/63 | 42/58 | 21/100 | 16/58 | 15/19 | 12/31 | | 0 | | |
| same + T24 on (FR, not enabled) | 42/59 | 42/58 | 17/100 | 16/58 | 15/19 | 9/29 | | 0 | | |
| Phase 2 holdout 2026-08-31, 30 pairs (P2H aggregate) | 7/8 | 7/10 | 1/20 | 3/10 | 5/8 | 1/5 | | 0 | 0 | 2 in 1 |

Duplicate memberships: 0 in every run (0/118 baseline, 0/110 final/actor-hygiene, 0/12 holdout).

Per-window, actor-hygiene: 2026-08-21 7/12, 7/7, 5/25, 0/7, 1/1; 2026-09-25 2/4, 2/5, 2/6, 3/5, 1/2;
2026-09-30-multilingual 34/49, 34/46, 15/69, 12/46, 14/16 (precision, recall, splits, merges, ID stability).

### Error classes per run (ledger; counted)

| error class | baseline | dev-final = actor-hygiene | holdout (aggregate) |
|---|---:|---:|---:|
| whole-storyline overmerge (split) | 17 | 17 | 1 |
| late attachment (split, overlap-merge) | 12 | 5 | 0 |
| single-source promotion (split) | 1 | 0 | 0 |
| roundup contamination (split) | 1 | 0 | 0 |
| segmentation interaction (merge) | 8 | 5 | 1 |
| missed continuation (merge) | 7 | 6 | 2 |
| other (merge; same-tick not grouped) | 2 | 4 | 0 |
| **total** | **48** (31 split, 17 merge) | **37** (22 split, 15 merge) | **4** (1 split, 3 merge) |

Holdout case contents were not used (only aggregate tally and class counts).

### Identity gold / defect set gates (FR)

Frozen defect set correct: baseline 23/128, T24 31/128. Identity gold rev 4 (232 scored, development): 157 -> 161.

### Coverage (COV)

9,002 items; 34% in a Development (eval windows: 21%, 407/1946, CGR). Unsurfaced 5,929: policy 4,240 (72%), review
1,689 (28%).

### Not found / not available

- Owner verdicts on the 128-case defect set (all null).
- A committed scored result of the coverage recoverability sample (only an uncommitted, 44/120 partial label file).
- A breakdown of the 149 NOT_SURFACED relation cases into correct vs recoverable.
- A committed doc stating "multilingual precision 0.36" as a decision number; the 0.36 matches `rev4-xlang-rescore.json`
  all.on precision 0.3636 (12/33); the decision baseline in XTP uses P 0.41 and stage-added precision 0.375.
- `phase2-holdout.json` case-level details: deliberately not used.
