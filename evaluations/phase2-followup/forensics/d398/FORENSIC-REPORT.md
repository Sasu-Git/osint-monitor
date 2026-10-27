# Forensic report: how Development 398 formed

Diagnosis only. **No fix is proposed or implemented.** No rule, threshold, guard, lexicon, Situation, production data,
holdout or pipeline was changed or replayed.

## Method and evidence base

- **Data.** A read-only working copy of the live-database snapshot of 2026-10-27 (SQLite backup API from a `mode=ro`
  source; sha256 `3c0b2cd9…0b4a39`, the copy recorded in `../../diagnostics/ui-review-2026-10-27/`).
- **Code.** D398 formed under three code versions. The 7 seed items were stored by `5f046b3` (2026-10-13 07:47 UTC,
  before the 10-13 deploy), 580 members by `3eda6d0` and 5 by `adacb83`. `development_identity.py`, `clustering.py`,
  `development_segmentation.py`, `dedup.py`, `lexical.py` and `config/event_grouping.yaml` are **byte-identical** across
  the three (`git diff --stat` is empty), so every attachment was made under the current Phase 2 identity contract.
- **Provenance actually stored.** Per member, the membership time (`event_items.added_at`), the run that stored it
  (`added_run_id`, which gives tier and code), the path's similarity value (1.0 for clustering continuation; the dedup
  similarity for the near-duplicate path), and the item's embedding, entities, source, title and times.
  **Not stored:** membership decisions and their reasons (they are not logged; no "continues D…" line exists in the
  daemon logs), the narrative cluster each decision saw, the HDBSCAN output, and any per-item classification.
- **Reconstruction (`../reconstruct.py`).** For each member, in storage order, the production link rule and guards
  (`clustering._linked`, `development_segmentation.incompatibility`, `compatible_link`, imported unchanged from
  `adacb83`) are applied between the member and every member stored in an earlier run. Those are the partners the
  continuation rule (`development_identity.reconcile`, step 3) could use. The reconstruction reproduces **565 of 567**
  continuation attachments with at least one accepted link to an earlier member. The other 2 link only to members
  stored in the same run, where the decision boundary is not recoverable.
- **Sub-stories.** To read a 593-item Development, members are grouped descriptively: average-linkage clustering of
  headline embeddings cut at distance 0.45 (`../analyze.py`). This gives 114 sub-stories, 29 of them with 5 or more
  items. They are an analyst's aid, not gold and not a rule.

Files: `attachment-history.csv` (one row per member: every field requested, or `NOT RECOVERABLE FROM CURRENT
PROVENANCE`); `attachment-graph.json` (593 nodes, 5,198 attach-time edges with their metadata);
`attachment-tree.svg` (static view); `analysis.json`, `gravity.json` (time series, cuts, sweep);
`counterfactual-cuts.md`.

## 1. How the members arrived

| | |
|---|---|
| Members | 593: **7 created the Development**, **567 continuation** (clustering → `reconcile` step 3), **19 dedup path** (near-duplicate of an existing member from another outlet, `pipeline.py` dedup link) |
| Stored by | warm tier 558, hot 29, cold 6, over **345 runs** from 2026-10-13 07:47 to 2026-10-27 12:51 UTC |
| Publication span | 2026-10-11 14:47 to 2026-10-27 12:34 (15.9 days); 17 outlets; 3 languages (en 572, es 18, it 3, recomputed with the pipeline's `item_language`) |
| Headline kinds | report 548, analysis 33, live blog 12; 20 roundup headlines |
| Provenance (recomputed) | independent 530, commentary 52, derivative 8, primary 2, first-hand 1 |
| Sources | **GDELT 284 (48%)**, Kyiv Independent 133, France 24 53, Al Jazeera 39, BBC World 25, others ≤ 13 |
| GDELT items | **275 of 284 are headline-only** (stored text no longer than the headline + 20 characters); their embedding is the headline |

**Why each attachment happened.** Every one of the 5,198 reconstructed attach-time links passed the same test:

- cross-source cosine of the stored embeddings ≥ 0.53 (or, same outlet, headline ratio ≥ 90);
- publication times within 72 h;
- no segmentation guard: the analysis-vs-report, headline-similarity (< 0.5, unless the 6 h override or the P7
  occurrence match applies) and disjoint-place guards.

A new item joins the Development when it has **at least one** such link to **any** existing member. When several
Developments qualify, the one with the most linked members wins.

| Link evidence (attach-time links) | Count | Share |
|---|---|---|
| All accepted links | 5,198 | about 8.8 per member |
| Cosine in [0.53, 0.58), near the threshold | 2,121 | 41% |
| Accepted only because of the P7 occurrence match / the 6 h headline override | 122 / 169 | 2% / 3% |
| One side names no place, so the place guard cannot apply | 490 | 9% |
| Shared entities are only states (no specific anchor, no sub-national place) | 3,853 | 74% |
| Shared places are only countries or regions | 3,458 | 67% |
| No shared entity at all | 92 | 2% |
| Touching a GDELT headline-only item | 3,751 | 72% (77% of the near-threshold links) |

| Attachment evidence (567 continuations) | Count |
|---|---|
| Joined through exactly one link (single-link attachments) | 108 (19%) |
| Every link near the threshold (< 0.58) | 121 |
| Every link with headline cosine < 0.55 | 67 |
| Every link needed P7 or the headline override | 14 |
| Every link had one side with no place (place guard bypassed) | 50 |

Per member, `attachment-history.csv` gives the best partner and that link's cosine, headline cosine, time delta,
shared places, actors and anchors, guard verdict, P7 and override, and whether the partner itself had joined on a
single link.

## 2. The first semantic failure

Under the contract (`evaluations/identity/development-identity-contract.md`), a Development is "one coherent
real-world action, occurrence, decision or materially unified update". Distinct actions, such as an announcement vs
a later attack, or an attack vs a retaliation, are different Developments even inside one conflict. Each point below
uses only what the pipeline had at that moment: the members already stored and the new item.

**First questionable attachment: the creation itself (2026-10-13 07:47, run `c6b440e9`, 7 items).** The new
Development joined:

- Trump's claim that Russia and Ukraine agreed to an "energy ceasefire" (8440, DW, published 10-11 14:47);
- Zelensky's statements that Russia won't accept it and that it must cover the grid (8455, 8572);
- reports of Russian strikes on energy sites after the announcement (8331, 8490, 8491);
- Trump's "because I said they agreed" (8561).

19 of the 21 pairs among the seven are linked; the other two are same-outlet pairs whose headlines are not
near-identical. The links are strong (cosine 0.63–0.86, headline cosine 0.60–0.89), span up to 36.7 h, and no guard
applies: all are report headlines, the places are compatible (Russia, Ukraine, United States) and the
headlines are similar. The only shared entities are three states. The announcement and the subsequent strikes
are distinct actions under the contract, and so are the statements. So the Development was already a small
storyline ("the energy ceasefire and its violation") at birth, formed by single-link connectivity within one
narrative cluster.

**First clearly wrong attachment: item 8908, 10-13 09:45, run `33bb69c5`, the first continuation.** "Putin wants
Ukraine deal more than Zelensky" (GDELT, headline-only, published 09:32). It is an opinion about peace-deal
willingness, not a report of the ceasefire or the strikes. At that moment D398 had 7 members.

- 8908 linked to exactly one of them: 8331, at cosine 0.5606 and headline cosine 0.598, 12.2 h apart, sharing only
  Russia and Ukraine. Every condition was met.
- Its headline matches none of the analysis patterns, so the analysis guard did not apply.
- It should be DIFFERENT: no shared action, and it is commentary on a different matter.

**First clearly wrong attachment that exists only through chaining: item 8329, 10-13 11:43.** "Russia's offensive
ability is broken, Kyiv's former top general tells BBC". Its **only** accepted link is to 8908 (cosine 0.5464,
headline cosine 0.514). Both are just above the two thresholds (0.53 and 0.50), and the item links to no seed item.
Without 8908 already being a member, nothing in D398 would have admitted it.

**First attachments that materially expanded the scope.**

1. **8908 opened the largest sub-story.** S4 has 81 members, 10-13 to 10-24: peace-deal politics, Trump–Zelensky
   relations, envoy talks and opinion.
2. **9175, 10-13 13:14: a new attack occurrence.** "Ukraine had no warning from partners on incoming Kyiv missile
   strike" linked to 8331 (0.542) and 9046 (0.580). The Kyiv strikes of 10-13 then accumulated as sub-stories S7, S9
   and S12 (50 items).
3. **10242, 10-14 07:24: the Starlink storyline.** "Ukraine's Starlink access restricted without warning, Zelensky
   adviser says" had one link to 10038 ("Zelensky defies Trump's warnings with Ukraine drone strike on Russian oil
   depot", 0.582, headline 0.537, sharing only Russia and Ukraine). The Starlink sub-stories S10, S11, S14 and S48
   (83 items) followed. "Starlink India launch: Why Elon Musk is still waiting" (8431) joined at 09:34 through a single
   link to another Starlink item (0.541, headline 0.528). The place guard could not fire: 8431 names India, and its
   partner names no place.
4. **Later scope.** The EU summit (11590, 14323, 14348, 10-15/16), the Norway peace talks with Witkoff (S88, S89,
   from 10-20), Ukrainian drone strikes on Russia (S77) and the diesel deal (S30) each entered the same way: a link to
   some member of the moving storyline, never to the original occurrence.

## 3. The gravity-well test

| Day (stored) | Attached | Size | Actors | Places | Outlets | Sub-stories | Span (d) | Members within 72 h of a new item (mean) | Links per new item (mean) | Single-link share | All partners in other sub-stories | New item vs current centroid | vs seed centroid | Centroid vs seed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10-13 | 25 | 25 | 13 | 8 | 6 | 8 | 2.3 | 15 | 4.8 | 0.33 | 0.39 | 0.71 | 0.66 | 0.96 |
| 10-14 | 73 | 98 | 74 | 36 | 13 | 29 | 3.4 | 61 | 6.5 | 0.26 | 0.40 | 0.60 | 0.43 | 0.85 |
| 10-15 | 88 | 186 | 125 | 48 | 14 | 51 | 4.3 | 139 | 8.8 | 0.21 | 0.44 | 0.63 | 0.46 | 0.77 |
| 10-16 | 90 | 276 | 182 | 68 | 15 | 69 | 5.4 | 213 | 11.7 | 0.12 | 0.35 | 0.61 | 0.45 | 0.75 |
| 10-17 | 12 | 288 | 187 | 70 | 15 | 73 | 5.7 | 249 | 5.6 | 0.25 | 0.50 | 0.57 | 0.47 | 0.75 |
| 10-18 | 50 | 338 | 211 | 81 | 15 | 81 | 7.3 | 164 | 10.1 | 0.14 | 0.28 | 0.63 | 0.47 | 0.75 |
| 10-19 | 42 | 380 | 232 | 88 | 16 | 85 | 8.4 | 111 | 6.8 | 0.02 | 0.37 | 0.62 | 0.48 | 0.76 |
| 10-20 | 50 | 430 | 251 | 97 | 17 | 96 | 9.3 | 113 | 8.5 | 0.23 | 0.38 | 0.60 | 0.47 | 0.76 |
| 10-21 | 62 | 492 | 283 | 109 | 17 | 104 | 10.3 | 154 | 10.8 | 0.21 | 0.28 | 0.61 | 0.48 | 0.76 |
| 10-22 | 43 | 535 | 306 | 120 | 17 | 110 | 11.2 | 160 | 7.5 | 0.19 | 0.31 | 0.63 | 0.48 | 0.76 |
| 10-23 | 23 | 558 | 340 | 129 | 17 | 114 | 12.3 | 139 | 8.9 | 0.22 | 0.48 | 0.61 | 0.49 | 0.76 |
| 10-24 | 12 | 570 | 344 | 130 | 17 | 114 | 13.3 | 103 | 10.1 | 0.08 | 0.42 | 0.65 | 0.52 | 0.77 |
| 10-25 | 6 | 576 | 347 | 131 | 17 | 114 | 14.1 | 54 | 4.3 | 0.17 | 0.00 | 0.58 | 0.43 | 0.77 |
| 10-26 | 5 | 581 | 351 | 134 | 17 | 114 | 14.9 | 35 | 1.6 | 0.60 | 0.60 | 0.62 | 0.50 | 0.77 |
| 10-27 | 12 | 593 | 358 | 138 | 17 | 114 | 15.9 | 24 | 3.2 | 0.27 | 0.36 | 0.60 | 0.54 | 0.77 |

Languages were 1 on day one and 3 from 10-14. "All partners in other sub-stories" is the share of new items whose
every accepted link went to a member of a different descriptive sub-story.

> **Did D398 become a semantic gravity well? Yes.**

- **The number of members a new item could land on grew 16-fold in four days** (mean 15 on 10-13, 249 on 10-17). The
  rule needs a link to *any one* of them, and the mean number of links per new item rose with it (4.8 to 11.7).
- **What it took to join drifted away from the original occurrence.** 68% of all continuations are below cosine 0.53
  to the seed's centroid, but only 19% are below it to the Development's centroid at the time they joined. By 10-16
  the centroid itself had moved to cosine 0.75 from the seed. The Development's "meaning" was whatever its members
  had become.
- **Every day, 28–50% of new items joined only through members of other sub-stories.** The scope widened continuously.
- **The pull weakened only when the storyline cooled.** Members within 72 h fell from 249 to 24 as older members aged
  out of the link window. The well is bounded by the storyline's activity, not by any property of the Development.

## 4. Attachment graph

`attachment-graph.json`: 593 nodes, 5,198 edges. Each edge carries cosine, headline cosine, hours, shared places,
actors and anchors, guard, P7, override, the rule, and its class flags. `attachment-tree.svg` draws each member at its
storage time and hop distance from the seed, joined to its best partner.

- **Chaining.** Only 64 members link directly to a seed item. Hop distance from the seed over attach-time links:
  1 hop 57, 2 hops 119, **3 hops 214**, 4 hops 126, 5 hops 44, 6–10 hops 24, 2 unreached.
- **Earliest wrong edge.** 8908 → 8331 (cosine 0.5606). Earliest chain-only wrong edge: 8329 → 8908 (0.5464).
- **Bridges and hubs.** There is no small bridge set. The graph is a dense mesh: removing the earliest wrong edge or the
  Starlink entry edge leaves it in one piece (`counterfactual-cuts.md`, cuts 1, 1b, 1c). High-degree nodes are the
  storyline's central reports and live blogs. The seed report 8331 alone is the best partner of many early items.
- **Edges across sub-stories.** 3,301 of 5,198 edges (64%) connect different descriptive sub-stories.

## 5. Counterfactual cuts (summary; details in `counterfactual-cuts.md`)

- **Cutting the earliest clearly wrong link, or the Starlink entry link, changes nothing:** still 593 in one component.
- **Cutting commentary and analysis bridges detaches 53 items;** 540 stay connected. Commentary is not the bridge.
- **Cutting state-only or country-only links shatters the graph,** but also cuts the seed's genuine same-occurrence
  links (8440 ↔ 8561, cosine 0.81, share only states). Broad anchors describe the storyline's vocabulary, not a
  separable failure.
- **Direct-to-seed only (no chaining) leaves 64 members,** themselves already spanning 13 sub-stories.
- **The mesh does not depend on the seed:** cutting at the first occurrence boundary still leaves 586 later members
  connected.
- **GDELT headline-only items amplify but do not cause it:** without them, 277 members remain connected. Links within
  24 h only still connect 532 members. Only combinations start to split it (24 h and no GDELT: 119 + 100).
- **Pair thresholds:** the giant survives up to cosine 0.65 (341 members). Splitting it needs about 0.70, inside the
  0.55–0.67 band where genuine same-occurrence pairs lie.

## 6. The seven other giant Developments

Details: `../giant-developments/COMPARISON.md`, `failure-families.md`, `giant-development-summary.csv`.

- **The same assembly mechanism appears in all eight.**
  - Every one was multi-occurrence at creation.
  - Every one grew by chaining (max hop 4–10) for 5–16 days.
  - The first clearly wrong continuation is always a near-threshold single link.
  - Joiners resemble the current members, not the seed.
- **The link source differs, giving four families:**
  - **F1** storyline relay with topic drift: D398, D514, D397;
  - **F2** non-English text through the English-only embedding: D449, D639, D399;
  - **F3** event wave via live-blog and commentary bridges: D626;
  - **F4** theme or anniversary aggregation: D182.

## 7. Blast radius

Details: `../giant-developments/COMPARISON.md` and `blast-radius.csv`.

- **The full D398 signature** (long + chain + drift): 6 Developments, 912 items.
- **Storyline relay without the drift flag:** 18 more, 1,944 items.
- **Together:** 24 of 992 corroborated Developments (2.4%) hold 32% of their items.
- **Manual inspection:** 33 Developments deserve it. "Suspicious" is kept separate from "wrong"; no verdict is
  implied.

## 8. Relation to existing Phase 2 findings

- **Already-known failure mode?** Partly. The ingredients are known:
  - "whole-storyline" overmerge: 17 of the Phase 2 development split failures, and French protests G07;
  - "chains across a guard": the follow-up results tried forbidding them, and it cost as many correct merges as it
    gained;
  - cross-day creep: T24 and E1;
  - the overlap-merge of a later cluster: 5 defect cases.

  **New is the scale mechanism.** Continuation by one link to any member, repeated over hundreds of runs with no
  bound on the Development's age or size and no reference to what it originally was, turns those local errors into
  a Development of hundreds of items.
- **Did previous evaluations fail to cover this scale? Yes, by construction.**
  - Identity replay windows are 48 h (four 12 h ticks), and the largest Development in the frozen defect set had
    56 items.
  - Phase 2 and T24 could only see one to three ticks of growth. The D398 failure needs days of relaying.
  - The live soak checks counted Developments (explosion of count), not the growth of one.
- **T24** (a Development spans at most 24 h) is the one tested rule that bounds the Development as a whole. It fixed 8
  overmerges and was rejected for losing two holdout pairs 32–34 h apart. D398 shows why a bound on the Development,
  not on the pair, was the right kind of lever: cut 13 shows that a 24 h limit on *pairs* still leaves 532 members
  connected.
- **E1** failed because each accepted pair inside such a chain is locally plausible, with similar actions and similar
  wording. The divergence exists between the ends of the chain, not between neighbours. A pair-level signal cannot
  see it.
- **Blocked-by-identity relations** (22 scored cases in 11 Developments). D398 contains the action → reaction chains
  Phase 3 wants (announcement → violation → statements → retaliation) as members of one Development. Giant
  Developments are the extreme form of that blocker.
- **Coverage diagnosis.** Giant Developments absorb items that would otherwise be unsurfaced, so "in a Development"
  overstates coverage for storyline topics.
- **UI diagnostics.** Case UI-1 is this Development.

**Owning stage.** Primarily **attachment policy** (continuation by any single linked member, with no Development-level
representation or bound). Next is **cluster assembly** (single-link connectivity, which formed a multi-occurrence seed).
**Pair acceptance** is weak for headline-only items and the storyline's shared vocabulary, but it is not
sufficient as an explanation: the mesh survives every pair-level cut that keeps genuine links.

## 9. ROOT CAUSE VS SYMPTOMS

**Symptoms, which are not causes:**
- 593 members; 15.9-day span; 17 outlets; 358 actors and 138 places;
- 114 descriptive sub-stories; centroid drift;
- evidence heterogeneity (Starlink/India next to ceasefire reports);
- many near-threshold links; the GDELT share.

**Mechanisms that allowed the bad membership decisions:**

1. **Transitive single-link membership (CHAINING + CLUSTER_REPRESENTATION_EFFECT).**
   - A new item continues a Development when it links to *any one* member. The Development has no representation of
     its occurrence: no core, no centroid test, no reference to the seed.
   - So membership is the transitive closure of locally plausible links. 529 of 593 members are not directly linked
     to the seed, at up to 10 hops.
2. **No bound on growth (TIME_WINDOW_CREEP, by relay).**
   - The 72 h limit applies to pairs, not to the Development. Members keep being renewed, so the window slides with
     the storyline and the Development never closes.
   - Every member stored becomes a new attachment point.
3. **Locally plausible links within a storyline (DIRECT_BAD_LINKS, BROAD_ACTOR_ANCHOR, BROAD_PLACE_ANCHOR).**
   - Within the Russia–Ukraine–US storyline, distinct occurrences score 0.53–0.65 on the full-text embedding: same
     states, same vocabulary.
   - The guards do not separate them: places are compatible (all inside Russia and Ukraine), headlines are similar
     enough (≥ 0.5), and the actor sets are the same states.
   - 41% of accepted links are within 0.05 of the threshold.
4. **Formation at birth (SEGMENTATION_FAILURE of a cross-day seed).** The first cluster already merged an announcement,
   statements and subsequent strikes over 36 h with strong links and no applicable guard.
5. **Amplifiers, which are not root causes:**
   - **SOURCE_ORIGIN_EFFECT:** GDELT headline-only items carry 72% of the links and half of the single-link joins.
   - **LIVEBLOG_OR_ROUNDUP_BRIDGE and ANALYSIS_BRIDGE:** analysis items attach only through other analysis items or
     live blogs, which the analysis guard does not cover.
   - **P7/override:** 14 attachments.
   - **Missing places bypass the place guard:** 50 attachments.

   Removing any one amplifier leaves a giant (cuts 2, 10, 13).

## Findings

- **First incorrect attachment.** Questionable at creation (7 items, 10-13 07:47: announcement, statements and strikes
  joined over 36 h). The first clearly wrong continuation is **8908** ("Putin wants Ukraine deal more than Zelensky",
  10-13 09:45, single link to 8331 at cosine 0.5606). The first wrong attachment possible only through chaining is
  **8329** (10-13 11:43, its only link is to 8908).
- **Dominant mechanism.** **Transitive single-link continuation with no Development-level representation or bound**
  (CHAINING + CLUSTER_REPRESENTATION_EFFECT + relay TIME_WINDOW_CREEP), fed by locally plausible storyline links
  (DIRECT_BAD_LINKS through BROAD_ACTOR/PLACE anchors). The amplifiers are headline-only GDELT items, live-blog and
  analysis bridges, and guard bypasses.
- **Chaining amplified it: yes.** 89% of members are two or more hops from the seed. Direct-to-seed connectivity
  would hold 64 members.
- **Gravity well: yes.** Members a new item could land on grew from 15 to 249 in four days. Joiners resemble the
  current members, not the original occurrence (68% vs 19% below 0.53). The pull ended only when the storyline
  cooled.
- **Giant Developments sharing the mechanism.** All 8 giants share the assembly mechanism: a multi-occurrence seed,
  then transitive any-member continuation. 3 share D398's full profile, family F1 (D398, D514, D397). Corpus-wide,
  6 Developments carry the full D398 signature and 24 the storyline-relay signature, holding 32% of the items in
  corroborated Developments.
- **Owning stage.** Attachment policy (continuation) first, cluster assembly second; pair acceptance contributes but
  does not explain it.

## Unknowns

`NOT RECOVERABLE FROM CURRENT PROVENANCE`:

- **The narrative cluster each decision saw.** Clusters, HDBSCAN labels, refinement and segmentation splits are not
  persisted. Reconstruction shows which earlier members an item *could* continue; whether a given member was in the
  cluster that touched D398 at that moment is not stored. Where several Developments qualified, which ones competed
  is unknown.
- **Decision boundaries within a run** (2 continuation members link only to members stored in the same run).
- **The dedup partner of the 19 dedup-path members** (only the similarity is stored).
- **Per-item domain and event type** (classification is stored per Development).
- **Item language as the pipeline decided it** (recomputed here with the same function, not stored).
- **The headline embeddings at decision time.** They were recomputed with the same model; equality holds only if the
  model files are unchanged.
- **Entity rows at decision time.** Entities are stored per item at ingest, but canonical names can be renamed later by
  resolution; differences would change the shared-entity and guard reconstruction.

**Deferred to after Candidate A's C2:** an exact replay of the clustering ticks (to recover the clusters). It is a
full replay over 15 days of data, which is CPU-heavy on the live host.

## Next decision

Proposal work should cover these architectural intervention points, in this order:

1. **Attachment policy / Development representation.** What a new item must match for a Development to continue (any
   member today).
2. **Development-level bound.** Temporal or occurrence boundary on the Development, not on the pair (cf. T24).
3. **Cluster assembly.** Single-link chaining at formation, which produced a multi-occurrence seed.

Pair acceptance (thresholds, guards for headline-only items and missing places) is a secondary point. The forensics
show it cannot carry the fix alone.

FORENSIC IDENTITY INVESTIGATION COMPLETE — NO FIX IMPLEMENTED
