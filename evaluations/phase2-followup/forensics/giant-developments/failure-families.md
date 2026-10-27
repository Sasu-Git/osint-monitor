# Failure families of the giant Developments

All eight share one **assembly mechanism**:

1. **Formation.** A multi-occurrence seed is formed by single-link connectivity within one narrative cluster.
2. **Growth.** It then grows by **continuation through one link to any member**. There is no Development-level
   representation (core, centroid, seed) and no bound on age or size, so membership becomes the transitive closure
   of locally plausible links. It relays through members for days and drifts away from the seed.

What differs is **what supplies the plausible links**. The families below are grouped by that link source. They are
not forced into one explanation.

| Family | Developments | What supplies the links | Distinguishing evidence | Already known? |
|---|---|---|---|---|
| **F1. Storyline relay with topic drift** | D398, D514, D397 (narrower) | A storyline's shared vocabulary (the same states, leaders and verbs) in full-text embeddings; headline-only GDELT items amplify | Drift vs seed 0.34–0.68; 35–41% of links near the threshold; links mostly share only states. Scope widens daily through members of other sub-stories (D398: Starlink, EU summit, peace talks; D514: Shin Bet lawsuit → election → Iran → West Bank) | Partly: "whole storyline" overmerge, cross-day creep (T24, E1). The scale was not evaluated |
| **F2. Non-English text through an English-only embedding** | D449, D639, D399 | Spanish and Italian text embedded by the English model: similarity is dominated by shared names and surface tokens, not by the occurrence | 77–100% es/it items; absurd joins (a tiger attack, Albania's PM, Venezuela's opposition, Greenland, US inflation); D449 has 658 links passed only through the P7/headline override | Yes in kind: the follow-up results say the English-only model "carries no identity signal on Spanish and Italian text". The scale is new |
| **F3. Event wave via live-blog and commentary bridges** | D626 | One protest wave's reports, live blogs and analysis; analysis items link through live blogs and other analysis, which the analysis guard does not cover | 26% of links are commentary bridges; 25 live blogs, 21 analysis items; the seed is an opinion column and a preview; only 2 members link directly to the seed | Yes in kind: French protests G07 (whole storyline) |
| **F4. Theme or anniversary aggregation** | D182 | A date theme (the October 7 anniversary): memorial pieces, essays, casualty tallies and threats share framing, not an occurrence | 5-day span, ending when the date passed; 46% near-threshold links; 14% commentary bridges; mixed languages | No specific prior case |

## Mechanism tags per Development

| | DIRECT_BAD_LINKS | CHAINING | BROAD_ACTOR_ANCHOR | BROAD_PLACE_ANCHOR | COMMENTARY / ANALYSIS BRIDGE | LIVEBLOG / ROUNDUP BRIDGE | TIME_WINDOW_CREEP (relay) | P7_OVERRIDE | SEGMENTATION_FAILURE (seed) | SOURCE_ORIGIN_EFFECT | CLUSTER_REPRESENTATION_EFFECT | OTHER |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 398 | ● | ● | ● | ● | ○ | ○ | ● | ○ (14 joins) | ● | ● GDELT headline-only | ● | |
| 397 | ● | ● | ● | ● | ○ | ○ | ● | ○ | ● | ○ | ● | |
| 449 | ● | ● | ○ | ○ | | | ● | ● (658 links) | ● | | ● | ● English-only embedding on es/it |
| 639 | ● | ● | ○ | ○ | | | ● | ○ | ● | | ● | ● English-only embedding on es/it |
| 399 | ● | ● | ○ | ○ | | | ● | | ● | | ● | ● English-only embedding on es/it |
| 626 | ● | ● | ○ | ○ | ● | ● | ● | | ● | ○ | ● | |
| 514 | ● | ● | ● | ○ | | | ● | | ● | ○ | ● | |
| 182 | ● | ● | ○ | ○ | ● | ○ | ○ (bounded by the date) | ○ | ● | ○ | ● | ● date theme |

● = dominant or necessary in this case; ○ = present, contributing.

Evidence for each tag is in `../d398/FORENSIC-REPORT.md` for D398, and in `COMPARISON.md` plus
`cases/d<id>-analysis.json` for the others.
