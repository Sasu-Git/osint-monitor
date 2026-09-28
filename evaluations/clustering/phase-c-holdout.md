# Clustering benchmark, Phase C: hold-out result and recommendation

Hold-out run once on 2026-09-28 (`inspect clustering-benchmark --holdout`, logged in
`holdout_runs.jsonl`), after `frozen_rule.yaml` and `phase-c-development.md` were committed.
Windows 2026-08-31 and 2026-09-10 (Wayback, blind labels). A small labelled benchmark, not an
estimate for all news.

**Limitation, stated up front:** the hold-out has 7 multi-source developments (all 2-source, none
3+) and 8 cross-source SAME pairs. It can say little about recall; it is read mainly as a false-join
check.

## Current clusterer

- Multi-source developments: 6/7 recovered, 1 partial, 0 missed (2 sources 6/7; 3+ none present).
- Cross-source SAME pairs linked: 7/8.
- Mixed clusters 8/14; wrong links 52 related-but-distinct, 3 unrelated. Same pattern as development:
  storyline-level clusters (SCO summit previews + analysis; the Nepal-Tibet flood rescue, updates and
  explainers; the 9/11 anniversary ceremonies and roundups; the Houthi advance milestones).

## Frozen rule: 0.45-0.53, <=6 h, >=2 shared actors

- Adds 0 SAME, 5 related-but-distinct, 1 unrelated. The one remaining SAME miss is in the band but
  outside the rule's time/actor conditions.
- False joins: two SCO summit previews with SCMP's SCO strategy analysis (shared: China, SCO); a
  Serena Williams biopic feature with Venus Williams' US Open exit; two Nepal flood pieces; two
  Russia-Ukraine drone analyses; a Breaking Defense Europe op-ed with an Al Jazeera Ukraine diplomacy
  piece (unrelated).
- Development recovery by source count: unchanged (6/7).

This replicates the development result on the four blind windows: no true joins, only false joins
of exactly the hard-negative class (related developments sharing actors and timing).

## Recommendation: KEEP the current clusterer

- **Do not add the secondary link rule.** Across six blind windows it adds 0 true joins and 13
  false joins (7 dev + 6 hold-out). Its only gains were on 2026-09-25, the non-blind window it was
  derived from.
- **Do not build actor-first candidate generation.** Low-similarity (<0.45) cross-source SAME misses
  exist only on 2026-09-25 (3 pairs); actor-first retrieval finds 2 of them among 180 candidates.
- **Not "need more data" for these two questions:** both answers are negative on independent data
  and consistent between development and hold-out. They could be reopened if the live 2026-09-27+
  window shows a 2026-09-25-like recall gap (see below).

## What the benchmark points at instead (not implemented, needs its own prompt)

1. **Storyline-level over-merging is the main error** (33 of 46 mixed clusters in dev + hold-out
   merge developments of one storyline; a handful merge unrelated items by template, e.g. "N dead
   after ..." disasters). For the Situation -> Development -> Evidence hierarchy this matters more than
   recall: an Event currently often spans several developments. Candidate directions to evaluate on
   this same benchmark: a within-cluster development split (e.g. on event-type/time/principal-action
   differences), or accept clusters as storylines and add the development split below them.
2. **Why 2026-09-25 differs.** It is the one window with recall misses (4/9 cross-source SAME pairs
   linked vs 61/63 elsewhere). Differences: local-DB items rather than RSS archive descriptions,
   6 sources including defence-trade press (Defense News is absent from all Wayback windows), and one
   dominant many-angle story (the Xi state visit). The live 2026-09-27+ window, which has the same
   source mix, is the right test of whether this is a real recall gap or a window artefact.

Benchmark source coverage caveat: Wayback windows are mostly Al Jazeera, SCMP and BBC; Defense News
and CSIS are unavailable in the archive.
