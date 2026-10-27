# Giant Developments: comparison and blast radius

Read-only forensics, same method as `../d398/FORENSIC-REPORT.md`:

- **Reconstruction:** `../reconstruct.py`, which re-applies the unchanged production link and guard code to the
  stored data.
- **Analysis and drift:** `../analyze.py` and `../gravity.py`.
- **Summary table:** `../compare.py`, which writes `giant-development-summary.csv`.
- **Blast-radius scan:** `../blast.py`, which writes `blast-radius.csv`.

Per-case outputs are in `cases/`. No fix is proposed.

## The eight giant Developments

| D | Size | Span (d) | Outlets | Languages (items) | Actors | Places | Continuations reproduced | Links per member | Single-link joins | Near-threshold links | P7 / override links | Commentary-bridge links | Max hop | Linked directly to seed | Largest at cosine ≥ 0.65 | Drift (vs seed / vs current, share < 0.53) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **398** | 593 | 15.9 | 17 | en 572, es 18, it 3 | 358 | 138 | 565/567 | 8.8 | 19% | 41% | 291 | 11% | 10 | 64 | 341 | 0.68 / 0.19 |
| 397 | 319 | 15.7 | 16 | en 293, es 14, it 12 | 159 | 92 | 302/305 | 7.4 | 20% | 36% | 104 | 11% | 7 | 88 | 159 | 0.34 / 0.13 |
| 449 | 294 | 14.4 | 15 | es 156, en 70, it 68 | 186 | 96 | 284/284 | 15.1 | 13% | 30% | **658** | 4% | 9 | 20 | 233 | 0.21 / 0.06 |
| 639 | 256 | 11.1 | 12 | es 199, it 31, en 26 | 196 | 129 | 249/249 | 6.9 | 29% | 31% | 155 | 6% | 8 | 23 | 142 | 0.41 / 0.21 |
| 399 | 255 | 15.5 | 9 | es 184, it 70, ru 1 | 181 | 139 | 244/244 | 3.6 | 31% | 41% | 43 | 2% | 8 | 45 | 76 | 0.28 / 0.17 |
| 626 | 216 | 12.1 | 9 | en 209, es 7 | 185 | 65 | 210/210 | 7.5 | 21% | 44% | 43 | **26%** | 7 | 2 | 136 | 0.37 / 0.14 |
| 514 | 154 | 14.3 | 14 | es 70, en 55, it 29 | 92 | 62 | 146/146 | 5.3 | 25% | 35% | 27 | 1% | 8 | 1 | 86 | **0.68** / 0.23 |
| 182 | 148 | 4.8 | 15 | en 103, es 33, it 12 | 108 | 63 | 139/140 | 5.9 | 34% | 46% | 50 | 14% | 4 | 46 | 61 | 0.59 / 0.15 |

Column notes:

- **Languages** are recomputed with the pipeline's `item_language`.
- **Linked directly to seed** is the size of the component under the "direct-to-seed only" cut, seed included.
- **Drift** is the share of continuations whose cosine is below 0.53 to the seed centroid, and to the centroid of the
  members stored before them.

## First split, mechanism, chaining

| D | Topic | First questionable | First clearly wrong | Dominant mechanism | Chaining | Like D398? |
|---|---|---|---|---|---|---|
| 398 | Russia–Ukraine energy ceasefire → whole war and US politics | creation: ceasefire announcement + statements + strikes over 36 h | 8908 "Putin wants Ukraine deal more than Zelensky" (single link 0.5606) | any-member continuation, storyline vocabulary, GDELT headline-only amplifier | yes, max 10 hops | (reference) |
| 397 | Houthi strikes on Saudi airports → Houthi–Saudi war | creation: Guterres condemnation + fact checks + Houthi warning + third-day attack | 8851 "The escalation in Yemen is a turning point" (analysis, 0.5404); 8884 desert battle (0.5303) | as D398, narrower topic | yes, 7 | yes |
| 449 | Flávio Bolsonaro / Brazil election campaign (Spanish/Italian) | creation: visit to his father + labour-reform stance + marches + live campaign | 10723 a British youth killed by a tiger (0.5464) | English-only embedding on es/it text; names dominate; 658 links rely on P7/override | yes, 9 | partly |
| 639 | French protests (Spanish/Italian coverage) | creation: stun-grenade decision + protest live blog | 14960 Albanian PM refuses to resign (0.5898); 15144 Venezuelan opposition (0.5489) | English-only embedding on es/it text | yes, 8 | partly |
| 399 | Russia–Ukraine / Trump (Spanish/Italian) | creation already includes 8407 "Trump rules out Russia and China helping Iran" beside Kyiv casualties | 8462 Europe's hydrocarbon purchases (0.5654); later Greenland, US inflation, Taiwan gas | English-only embedding on es/it text | yes, 8 | partly |
| 626 | French protest wave (English) | creation: a GDELT opinion column + a protest preview | 14983 "Macron to address the nation" (a distinct action); later a football tangent (PSG) | event wave chained through live blogs and commentary | yes, 7 | yes (a wave, not drift) |
| 514 | Netanyahu / Israeli election | creation: Trump hedging (analysis) + "may endorse" | 11414 former Shin Bet chief sues Netanyahu (single link 0.5656) | any-member continuation with topic drift (68%) | yes, 8; only 1 member links directly to the seed | yes |
| 182 | October 7 anniversary | creation: writer interview + anniversary threat + Israeli kill claim + Gaza death toll | 3507 Gaza book enthusiasts (0.5383) | theme aggregation around a date; commentary-heavy | yes, 4 | partly (bounded by the date) |

## Findings across the eight

- **All eight were already multi-occurrence at creation.** The first questionable point is the cluster that created
  each Development (single-link connectivity within one narrative cluster), not a later attachment.
- **The first clearly wrong continuation is always a near-threshold single link** (cosine 0.53–0.59) to one existing
  member, never to the seed's core.
- **All eight grow by chaining** (max hop 4–10). In all but D182 (5 days), they grow for 11–16 days. In every case a
  "direct-to-seed only" restriction would keep a small fraction (1–88 members).
- **No pair-level cut breaks them.** Keeping only links at cosine 0.65 or more still leaves a largest component of
  61–341 members. Removing commentary-bridge links leaves 130–540 connected.
- **Representation drift is universal.** Joiners resemble the current members far more than the seed: below 0.53 to
  the current centroid 6–23%, to the seed centroid 21–68%.
- **The link source differs, and that defines the families** (`failure-families.md`):
  - English storyline vocabulary (398, 397, 514);
  - non-English text through an English-only embedding (449, 639, 399);
  - live-blog and commentary bridges (626);
  - a date theme (182).

## Blast radius (all 992 corroborated Developments, `blast-radius.csv`)

Signatures, computed from stored data only:

- **large:** at least 30 members;
- **long:** at least 4 growth days, or a span of at least 4 days;
- **drift:** at least half of the later members are below 0.53 to the first run's centroid, at size 10 or more;
- **chain:** max hop ≥ 4 over the base link rule. Guards are not applied here, so this over-approximates links;
- **actor-diverse:** at least 40 distinct actors.

"Suspicious" is not "wrong". None of these counts is a review verdict.

| Category | Developments | Items | Share of items in corroborated Developments (8,835) | Examples |
|---|---|---|---|---|
| **A. D398-like** (long + chain + drift) | **6** | 912 | 10% | 398, 514, 812 (Brad Lander / West Bank, 76), 439 (Pope at Gemelli, 36), 448 (Netanyahu–Trump, 33), 132 (Iran–US, 20) |
| **B. Storyline relay** (long + chain, drift not flagged) | **18** | 1,944 | 22% | 397, 449, 639, 399, 626, 147 (Bolsonaro first round, 108), 416, 441 (hurricane Simon, 74), 630, 805, 493, … |
| **C. Large or long, no chain** | 56 | 2,019 | 23% | 182, 119 (Yemen, 137), 124 (Kyiv bridge, 105), 67, 162, … |
| D. One signature | 38 | 413 | 5% | |
| E. None | 874 | 3,547 | 40% | |

- **Count vs impact.** A + B are **24 Developments (2.4%) holding 2,856 items (32%)** of everything in corroborated
  Developments: the problem is concentrated, but its share of evidence is large.
- **Likely legitimate large occurrences.** These cannot be certified from signatures. A low drift value does not mean
  coherent: D449 and D399 have low drift and are clearly mixed. Candidates for genuinely large single occurrences are
  in category C with short spans, for example D386 (37 items, 0.4 days). Some of B may also be legitimate long-running
  single occurrences, for example hurricane D441 (74 items over 10.7 days); that needs review.
- **Deserve manual inspection:** all of A and B (24), and the 9 category-C Developments above 50 members: 33 Developments.
- **Languages.** Non-English sources are the majority in 33% of large Developments (14 of 42), against 19% of all
  Developments.
- **GDELT.** At least 30% GDELT items in 20 of the 42 large Developments.

## Deferred

An exact replay of the clustering ticks for any of these Developments, to recover which cluster each decision saw, is
a full multi-day replay. It is CPU-heavy on the live host and is deferred until after Candidate A's C2.
