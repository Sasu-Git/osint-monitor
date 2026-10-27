# D398 counterfactual cuts

Diagnosis, not tuning. **No cut here is a proposed production fix**, and none was run against any pipeline.

**Graph.** The 593 stored members of Development 398. The edges are the 5,198 attach-time links: links the
production rule accepts between a member and the members stored in earlier runs. They were reconstructed with the
unchanged `clustering._linked` and `development_segmentation.incompatibility` code (`../reconstruct.py`) on a
read-only snapshot. Each cut removes a class of edges and recomputes connected components (`../analyze.py`).

**Sub-stories.** "Sub-story" is the descriptive grouping in `FORENSIC-REPORT.md`: average-linkage clustering of
headline embeddings at distance 0.45. It is an analyst's aid, not gold. A cut "splits same-occurrence evidence" when a
sub-story of 5 or more items ends up in two or more non-trivial components; sub-story labels are themselves
approximate.

| # | Cut | Components | Largest | Seed component | Sub-stories left in the seed component | Same-occurrence evidence split? |
|---|---|---|---|---|---|---|
| 0 | none (baseline) | 1 | 593 | 593 | 114 | n/a |
| 1 | remove the attach-time link of the earliest clearly wrong attachment (8908 → 8331) | 1 | 593 | 593 | 114 | no |
| 1b | remove 8908 entirely (as if never attached) | 2 | 592 | 592 | 114 | no |
| 1c | remove the attach-time link of the Starlink entry item (10242 → 10038) | 1 | 593 | 593 | 114 | no |
| 2 | remove commentary / analysis / roundup bridge links (555 edges) | 54 | 540 | 540 | 111 | no |
| 2b | remove live-blog links | 17 | 548 (+29) | 548 | 112 | yes: S2, S4, S10, S30, S41, S45, S48 |
| 3 | remove links whose only shared entities are states (broad actor anchor; 3,853 edges) | 309 | 270 | **1** | 1 | yes: S2, S4. The seed's own same-occurrence links (Trump's claim, 8440 ↔ 8561, cosine 0.81) share only states |
| 4 | remove links whose only shared places are countries or regions (broad place anchor; 3,458 edges) | 232 | 359 | 359 | 74 | no, but 228 singletons |
| 5 | remove links with no shared entity at all (92 edges) | 16 | 578 | 578 | 110 | no |
| 6 | remove near-threshold links (cosine < 0.58; 2,121 edges) | 85 | 504 | 504 | 76 | no |
| 7 | remove links crossing the first occurrence boundary (before vs after the first wrong attachment, 2026-10-13 09:45) | 8 | **586** (without the seed) | **1** | 1 | the 7 seed items fall apart into singletons |
| 8 | direct-to-seed only (no chaining): keep only links that touch a seed item | 530 | **64** | 64 | 13 | n/a: 529 members become unattached |
| 9 | remove links crossing descriptive sub-stories (circular, for scale only) | 184 | 77 | 46 | 1 | yes, by construction |
| 10 | remove links touching GDELT items (275 of 284 are headline-only; 72% of all edges, 77% of near-threshold edges) | 315 | **277** | 277 | 69 | not measured (GDELT items drop out) |
| 11 | non-GDELT, no live-blog and no commentary links | 344 | 250 | 250 | 65 | not measured |
| 12 | non-GDELT links with cosine ≥ 0.58 | 355 | 229 | 229 | 51 | not measured |
| 13 | keep only links within 24 h (time delta of the pair) | 51 | **532** | 532 | 102 | no |
| 14 | links within 24 h and non-GDELT | 360 | 119 (+100) | 119 | 37 | not measured |

Cuts 10–14: `../extra_cuts.py` on the same graph.

Cosine sweep (`gravity.json`): if only links at or above t were kept, the largest component would be

| t | 0.53 | 0.55 | 0.58 | 0.60 | 0.62 | 0.65 | 0.70 | 0.75 |
|---|---|---|---|---|---|---|---|---|
| Largest component | 593 | 560 | 504 | 461 | 423 | 341 | 170 | 33 |

Live calibration places same-Development cross-source pairs at cosine 0.55–0.67 (`clustering.py`). A pair threshold
high enough to break D398 (0.70 or more) would cut most genuine same-occurrence links.

## What the cuts show

1. **No single bridge.** Removing the earliest clearly wrong attachment (cut 1, 1b) or the attachment that brought
   in the Starlink storyline (cut 1c) leaves D398 whole. On average a member has about 9 accepted links to earlier
   members, so every sub-story reaches the rest through many alternative edges. Removing "one or a few edges" cannot
   split the graph cleanly.
2. **The mesh does not depend on the seed.** Cut 7 isolates the 7 seed items, and the 586 later members still form one
   component. Without the first Development, the same storyline would have meshed into one giant group of its own
   under the same link rule.
3. **Commentary is not the bridge.** Cut 2 detaches 53 commentary items, and the remaining 540 stay connected.
4. **Broad anchors are everywhere, including in true links.** Most accepted links share only states (Russia, Ukraine,
   United States) and country-level places. Removing them (cuts 3, 4) shatters the graph, but cut 3 also severs the
   seed's genuine same-occurrence links. "Shares only states" describes the storyline's vocabulary; it does not
   separate occurrences.
5. **Chaining is what carries the size.** Only 64 members link directly to a seed item (cut 8), and even those span 13
   sub-stories. The other 529 joined through intermediate members, up to 10 hops from the seed
   (`attachment-history.csv`, column `hop_from_seed`).
6. **Headline-only items amplify but do not cause it.** Without the GDELT items, the 309 other members still form a
   277-member component spanning 69 sub-stories (cut 10).
7. **Short links chain across days.** Keeping only pairs within 24 h still leaves 532 members connected (cut 13): a
   storyline relays itself day to day through short links, so the 72 h window is not what made D398 span 16 days.
   A pair-level time limit alone would not have stopped it. Only combinations of cuts (14) start to split the mesh.
8. **Pair thresholds are the wrong lever.** The sweep needs about 0.70 before the giant splits into several large
   parts, well inside the range where genuine same-occurrence pairs lie.
