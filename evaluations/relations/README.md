# Phase 3: typed relationships between Developments (gold design)

Status: **gold design, ready for owner review.** No runtime relation logic exists. Situation grouping is unchanged.

```text
Situation            (exact actor set, unchanged)
  ↓ membership
Developments         (Phase 2 identity, frozen)
  ↕ typed relations  (this phase)
Developments
  ↓
Evidence             (items, provenance roles)
```

## 1. Accepted Situation baseline

- **Situation creation** stays `create_by: actor_set` on `main`.
  - Situation hold-out, scored once on 2026-10-05, branch `eval/situation-holdout-2026-10-03`:
    - exact set: precision 1.00;
    - actor pair ≥ 0.40: 0.20;
    - actor pair ≥ 0.50: 0.33.
  - Both actor-pair thresholds created a false US–China Situation.
  - Decision: **KEEP EXACT ACTOR-SET**. `feat/situation-coverage` is not merged.
- **Not used:** actor-pair creation. **Unchanged:** Situation thresholds and Situation grouping.
- **Development identity** is the Phase 2 contract, frozen and regression-protected (identity gold revision 2).
  Relations never merge Developments.
- **Relations do not touch Situations.** A relation between two Developments never adds, removes or moves a
  Situation membership. The review sheet shows each side's production Situation as context only.

## 2. Relation taxonomy

Full definitions, required evidence and precedence are in [taxonomy.md](taxonomy.md).

| Label | Kind | Direction |
|---|---|---|
| `same_calamity_lifecycle` | episode | symmetric |
| `same_visit_or_summit` | episode | symmetric |
| `same_attack_wave` | episode | symmetric |
| `reaction_to` | directed | source → target (reaction → original) |
| `follow_up_to` | directed | source → target (later step → earlier step) |
| `caused_by` | directed | effect → cause |
| `co_caused_with` | symmetric | none |
| `NO_RELATION`, `AMBIGUOUS` | review labels | none |

**Precedence.**
1. The same occurrence is identity, not a relation.
2. Episode types come first.
3. Then the directed types: `reaction_to`, `follow_up_to`, `caused_by`.
4. `co_caused_with` comes last.

One primary label per pair.

**No `official_package`.** A release, Q&A, factsheet and daily-news mention of one act are one Development (gold
C034 and C103, revision 2). A pair like that is flagged `SAME_DEVELOPMENT_SUSPECTED`, not given a relation.

## 3. Positive and negative examples

All of these are real pairs in the review sheet. The expected label is the design intent; the owner verdict decides.
The identity-gold case (`A/B/C/H…`) that motivated each pair is given where there is one.

### Positive (expected relation)

| Case | Pair | Expected | Why |
|---|---|---|---|
| R045, R075 | Nepal/Tibet flood: rescue and death toll vs trapped hydropower-tunnel workers; foreign rescue teams question vs tunnel traps | `same_calamity_lifecycle` | One flood episode, one area (H006, H024: "not one occurrence but should be clustered, natural calamity") |
| R082, R068 | DR Congo Ebola: vaccine trial vs Ervebo dose arrival; outbreak growth vs dose arrival | `same_calamity_lifecycle` | One outbreak response (A021, A022, A032) |
| R133, R026 | Xi's Washington visit: White House joke at the state event vs the state dinner / red-carpet welcome | `same_visit_or_summit` | One visit occasion (B005: "same visit though, only the juice … should be extracted") |
| R069 | Russia strikes the Academy of Sciences vs Russia pounds Kyiv after that strike | `same_attack_wave` or `follow_up_to` | Tests the episode-vs-directed precedence and the C076 identity boundary |
| R102 | US economic isolation of Iran vs "Iran says new US sanctions violate sovereignty" | `reaction_to` (B->A) | A named actor responds explicitly |
| R013, R095 | Trump tariffs vs Carney calling them a "miscalculation" | `reaction_to` | Explicit response by a different actor |
| R002 | Lindsay Clancy jury deadlocked vs the jury's options | `follow_up_to` or `NO_RELATION` (commentary) | The same procedure, or an explainer |
| R029 | West Bank settlement re-established vs activists push back | `reaction_to` or `co_caused_with` | A023: "action-reaction or co-causation", which the evidence must settle |

### Negative (expected `NO_RELATION`): required control families

| Family | Case | Pair | Why it is a trap |
|---|---|---|---|
| **Broad bilateral pair** (Situation hold-out) | R025, R038, R044 | Xi–Trump summit vs China in Latin America vs Europe/Spain–China | The hold-out's false US–China Situation, all three member pairs |
| Broad bilateral pair | R092 | Xi–Trump summit vs the F-16V delivery to Taiwan | Labelled AMBIGUOUS in the Situation hold-out |
| Broad bilateral pair | R085, R005 | summit pieces sharing only US + China | Shared pair, separate occurrences |
| **Same actors, unrelated action** | R137 | two Raytheon missile contracts (AMRAAM, SM-6) | Same company and customer, separate awards (hold-out AMBIGUOUS) |
| Same actors, unrelated action | R009, R032 | Harry and Meghan: UK return vs Netflix role | The same people, unrelated actions |
| **Same place, unrelated action** | R078, R104 | two Hong Kong police cases | Location and institution only |
| **Same crisis, distinct actions** | R040, R107, R091 | West Bank evictions vs settler arson; Ebola spread warning vs vaccine trial | The owner's boundary: the same Situation is not a relation (A017) |
| **Chronological adjacency** | R061 | EU trade powers vs the Commission's Daily News an hour later | Time and institution only |
| **Official package** | R066 | Council space-threat decision vs the Daily News mention | C048: inside one Development or unrelated, never `official_package` |
| Same actor, different matters | R124, R130 | Pope's AI remarks vs the France visit; Harry's legal costs vs UK return | One shared actor |

## 4. Candidate generation (gold selection, not runtime)

`scripts/build_cases.py`, seeded (`20261005`) and capped per window. **The rules choose which pairs are reviewed,
never their labels.** The selecting rule is hidden from the labeller and the owner (`review/candidate-rules.json`).

**Unit.** One case is two distinct Developments.

| Window kind | Developments |
|---|---|
| Windows with clustering gold | the blind gold occurrences |
| Other windows (multilingual, live 10-03) | the replayed system Developments, plus each unclustered item as a provisional single-item Development |

In both cases, occurrences that identity gold revision 2 labels SAME are merged first, so no case is two halves of
one Development.

**Context per side.** These come from `scripts/replay_windows.py`, which runs the `main` pipeline tick by tick on a
temporary DB:
- actors and places (item NER plus system principals);
- the system Development;
- the production Situation.

| Rule | Selects | Cap per window |
|---|---|---|
| `situation_holdout_control` | the hold-out's US–China and Raytheon pairs (live 10-03 window only) | all |
| `owner_note` | identity gold DIFFERENT cases whose owner note describes a grouping above the Development (`owner-notes-proposals.md` §3) | all |
| `gold_related` | clustering gold `related_pairs` (blind "related but distinct" with a note) | 4 |
| `storyline_mates` | distinct occurrences in one gold storyline | 3 |
| `cue` | they share an actor or place, cosine ≥ 0.35, and the later text has a reaction, follow-up or causal cue | 3 |
| `lifecycle` | both match a calamity / attack / visit lexicon, plus a shared place (calamity, attack) or ≥ 2 shared actors (visit) | 2 per kind |
| `neg_same_actors` | ≥ 2 shared canonical actors, cosine < 0.35 | 2 |
| `neg_same_place` | shared place, no shared actor, cosine < 0.35 | 1 |
| `neg_same_crisis` | same storyline or Situation, cosine < 0.45, no cue | 2 |
| `neg_chrono_adjacent` | first reports ≤ 3 h apart, sharing an actor or place, 0.30 ≤ cosine < 0.50, no cue | 1 |
| `neg_broad_pair` | both contain one broad pair: US–China, US–Iran, Russia–Ukraine, Israel–Iran, Israel–Palestine, China–Taiwan, US–Russia, China–Japan | 2 per pair |

The lexicons are deliberately crude. They raise recall for the review. They are not the future runtime candidate
generator, and Phase 3 implementation must be scored on the holdout, whose cases these same rules selected
blind.

## 5. Gold review design

The same protocol as the identity gold (`../identity/README.md`).

1. **Windows frozen by hash** (`manifest.yaml`). Existing frozen files are referenced in place. The live 10-03
   export is new: news sources only, taken from the backup-API snapshot.
2. **Replay and cases:** `replay_windows.py development`, then `build_cases.py development`.
3. **Blind draft.** A separate annotator sees only item text, outlet, time and the taxonomy
   (`review/labeller-input.md`) and writes `review/draft-labels.json`. That file has label, direction, flags,
   rationale and confidence.
4. **Owner sheet** (`review/relation-review-sheet.md`). Each case shows:
   - the case ID;
   - Developments A and B;
   - titles, timestamps, actors and places;
   - the system Development and the current Situation;
   - evidence excerpts;
   - the proposed relation, direction, rationale and confidence;
   - a blank verdict.
5. **Owner verdicts** (`review/owner-verdicts.yaml`). Each verdict is `label` (or `ACCEPT`), `direction`,
   `identity_flag` and `note`.
   - The owner may correct the type, the direction or both. Notes are stored verbatim.
   - Regenerating the sheet never overwrites verdicts.
6. **Freeze** the gold with SHA-256, as `gold/relation-gold.yaml` plus `gold/manifest.yaml`. This happens only
   after owner review, before any relation code.
7. **Scoring later** (Phase 3 implementation), computed per relation type:
   - precision and recall;
   - direction accuracy on directed types;
   - the false-positive rate on each hard-negative family;
   - `AMBIGUOUS` excluded and reported separately.

   `SAME_DEVELOPMENT_SUSPECTED` flags go back to identity review. They never feed a relation.

## 5a. Blind draft outcome (before owner review)

The development split has **142 cases from 7 windows**. Two separate-context annotators drafted them; each saw
only `labeller-input.md`.

| Draft label | Cases |
|---|---:|
| `NO_RELATION` | 118, of which 45 flagged `commentary` |
| `same_calamity_lifecycle` | 11 |
| `same_visit_or_summit` | 7 |
| `AMBIGUOUS` | 4 |
| `same_attack_wave` | 1 |
| `reaction_to` | 1 |
| `follow_up_to`, `caused_by`, `co_caused_with` | 0 |

Three cases were flagged `SAME_DEVELOPMENT_SUSPECTED`: R012, R045 and R138. **R045 conflicts with identity gold**:
the owner labelled H006, H016 and H026 DIFFERENT. The owner should look at it.

**Relation drafted, by selecting rule.** The figure is relation-drafted cases out of all cases the rule selected.

| Rule | Drafted / selected |
|---|---|
| `owner_note` | 10/17 |
| `lifecycle` | 8/38 |
| `storyline_mates` | 4/15 |
| `neg_broad_pair` | 1/10 |
| `neg_same_actors` | 1/10 |
| `neg_same_crisis` | 1/10 |
| `situation_holdout_control` | 0/5 |
| `cue` | 0/21 |
| `gold_related` | 0/16 |
| `neg_same_place` | 0/7 |
| `neg_chrono_adjacent` | 0/7 |

**What this shows:**
- **The episode types have real support.** All three episode-type kinds have it: calamity (Nepal/Tibet flood,
  DRC Ebola, Borneo haze), visit or summit (Xi's state visit, the SCO summit, Macron in Spain, Pope Leo in
  Lourdes, Netanyahu in the UAE), and one attack wave.
- **The directed and causal types have almost none.** Under the strict evidence rule the annotators rejected:
  - R102 (Iran condemns sanctions; the analysis piece is not the sanctions act);
  - R013 and R095 (Carney's tariffs answer the fresh US tariffs, not the paired item);
  - R029 (A023's "action-reaction or co-causation").

  The candidate rules surfaced pairs on the same topic, not the actual action → reaction pairs.
- **No hard-negative family produced a false relation beyond chance.** All five Situation hold-out controls,
  including the false US–China join, were drafted `NO_RELATION`.

**Consequence before any implementation.**
1. Owner review settles the four directed and causal types on what exists.
2. If any type still has fewer than 3 owner-confirmed positives, either:
   - draw a **supplementary, positive-targeted batch** for it from the development windows only (for example,
     pairs whose text names the other Development's action), reviewed the same way; or
   - merge or drop the type (risk 5).
3. The sealed holdout is not used for this.

## 6. Holdout design

- **Windows:** 2026-07-21, 2026-08-07, 2026-08-15 and 2026-09-10. None of them has been used for identity or
  relation work. All four have blind clustering-gold occurrences.
- **Sealed now, before any implementation.** `scripts/seal_holdout.py` replays the windows and generates cases with
  the same frozen rules, then writes `holdout/SEALED.yaml`. That file holds the SHA-256 of every file and of the
  generator scripts. No case content was printed or read.
- **`scripts/check_sealed.py`** verifies the seal using hashes only.
- **Labelling** happens only after the relation implementation is frozen. A blind annotator drafts, then the owner
  gives verdicts, then the labels are frozen. After that comes **one** scored run, with no tuning afterwards. This
  is the same discipline as the Phase 2 and Situation hold-outs.
- **Optional prospective check.** After the `main` deploy, take a live window with continuous collection, using
  the same rules and the same seal procedure.

## 7. Major risks

| Risk | Where it bites | Guard in this design |
|---|---|---|
| **False causality** | `caused_by` and `co_caused_with` inferred from sequence or shared topic | Causal labels need an attributed causal statement in the evidence. Otherwise the label is `AMBIGUOUS`. The chronological-adjacency negatives measure it. A runtime rule must cite the evidence span. |
| **Relation explosion** | O(n²) pairs in a busy Situation; every Gaza item "related" to every other | Pairwise and evidence-bound, one primary label. Same crisis / Situation / storyline is an explicit negative family. A later runtime cap per Development will need its own gate. |
| **Whole-storyline overgrouping** | episode types becoming "everything about the flood" or "everything about the war" | Episode types require one bounded episode: the same hazard event, the same visit occasion, the same attack wave. `storyline_mates` cases test that the storyline is not the unit. |
| **Broad actor-pair contamination** | US–China, Russia–Ukraine, Israel–Palestine pairs linked on shared actors | Shared actors are never sufficient. `neg_broad_pair` is a required control family. The hold-out's false US–China Situation is a named example. |
| **Sparse directed types** | `follow_up_to`, `caused_by`, `co_caused_with` have 0 draft positives; `reaction_to` has 1 | Section 5a: owner review first, then a positive-targeted supplementary batch from development data, or merge or drop the type. No implementation of a type without ≥ 3 owner-confirmed positives. |
| **Duplicate semantic relation types** | `follow_up_to` vs `caused_by`; `reaction_to` vs `caused_by`; episode types vs `follow_up_to`; `same_attack_wave` vs the identity rule (C076: one overnight attack and its side effects are **one** Development) | There is one precedence order and one primary label. Owner corrections show whether two types collapse. Any type with fewer than 3 owner-confirmed positives after review is merged or dropped before implementation. |
| **Identity leakage** | relations used to patch clustering recall (H001/H018/H009/H021) | `SAME_DEVELOPMENT_SUSPECTED` routes back to identity. A relation never substitutes for a merge, and never for a split. |
| **Unit mismatch** | gold occurrences vs system Developments (most single-source items are not surfaced) | The gold is system-independent. The sheet shows the system Development, or "not surfaced", per side. Scoring can only credit pairs whose two sides exist as Developments, and reports coverage separately. |

## Files

| Path | What |
|---|---|
| `manifest.yaml` | windows and hashes, split development / holdout |
| `taxonomy.md` | the definitions given to the annotator and the owner |
| `scripts/` | export, replay, cases, labeller input, sheet, seal and check |
| `runs/` | development replays (system Developments, Situations, item places and actors) |
| `review/cases.json`, `review/candidate-rules.json` | development cases and their (hidden) selecting rules |
| `review/labeller-input.md`, `review/draft-labels.json` | blind draft |
| `review/relation-review-sheet.md`, `review/owner-verdicts.yaml` | owner review |
| `holdout/` | **sealed**: do not open |
