# Clustering benchmark, Phase C: development results

Written 2026-09-28, **before** the hold-out run. Command:
`python main.py inspect clustering-benchmark --development`. Windows: 2026-07-21, 2026-08-07,
2026-08-15, 2026-08-21 (Wayback, blind labels) and 2026-09-25 (local DB, labels not blind: this
window was seen with similarity scores during the day-1 recall review). A small labelled benchmark,
not an estimate for all news.

## Current clusterer

| | all dev | 4 blind windows | 2026-09-25 |
|---|---|---|---|
| multi-source developments recovered | 33/37 (1 partial, 3 missed) | 29/30 (1 partial) | 4/7 (3 missed) |
| 2-source / 3+-source recovered | 28/32 / 5/5 | | |
| cross-source SAME pairs linked | 58/64 | 54/55 | 4/9 |
| mixed clusters | 32/54 | 31/49 | 1/5 |
| wrong links (pairs): related / unrelated | 131 / 25 | | |

Recall is high on the blind windows: the only unlinked cross-source SAME pair there is an Al Jazeera
live blog headline ("Iran war live: Trilateral Mecca defence pact signed ...", sim 0.43, 9.3 h) against
the BBC report of the signing. The day-1 finding that recall is the main bottleneck reproduces only on
2026-09-25.

## The failure that dominates: storyline-level merging

Of the 32 mixed clusters, 26 merge developments of **one storyline** (US strikes night 10/11/12 plus
Trump threats and analysis; the Thailand shooting plus survivor account, "what we know" and the PM's
gun-law pledge; the Mecca pact signing plus three analysis pieces; Lebanon "pilot zone" deployment plus
reactions). 6 merge different storylines or unrelated items, mostly by template ("N dead after ...":
Guyana ferry + Afghanistan floods + Mauritania boat; Indonesia quake + Croatia wildfire; unrelated
China/AI pieces). The 25 unrelated wrong links come from those 6 clusters.

So the clusterer's Events are closer to storyline-sized than development-sized under these labels. The
labels are strict (a follow-up or analysis is a separate development), which is the contract
(Situation -> Development -> Evidence), so this is a real precision gap for the Development layer, but
much of it is a granularity mismatch rather than nonsense merges.

## Candidate secondary link rules (0.45-0.53 band, cross-source)

| rule | blind windows: +SAME / +RELATED / +UNRELATED | 2026-09-25: +SAME / +RELATED / +UNCERTAIN |
|---|---|---|
| proposed: <=6h, >=2 shared actors | 0 / 7 / 0 | 3 / 4 / 1 |
| <=4h, >=2 shared actors | 0 / 4 / 0 | 3 / 4 / 1 |
| <=8h / <=12h, >=2 shared actors | 0 / more / 0 | 3 / more |
| <=6h, >=1 shared actor | 0 / 10 / 3 | 3 / 6 / 1 |
| <=6h, actor coverage >= 0.5 | 0 / 9 / 1 | 3 / 4 / 1 |
| >=2 shared principals / same type / shared location | fewer joins, fewer or no SAME | |

Every variant's true joins come from 2026-09-25, the window the rule was derived from. On independent
windows no variant adds a true join; every variant adds related-but-distinct false joins (e.g. "Can
mediators broker a truce between the US and Iran?" with War on the Rocks' Iran relations essay; the
Mecca pact "What's in it?" explainer with the signing report; two different days of Russian strikes).
Development recovery by source count moves by one 2-source development (28 -> 29/32); 3+-source
developments are already 5/5.

## Actor-first retrieval (probe, not implemented)

Only 3 cross-source SAME misses lie below 0.45, all on 2026-09-25. `>=2 shared actors` within 24 h
would find 2 of them among 180 candidates (80 related, 98 unrelated); `>=1 shared principal` finds 1
among 885. Multi-source developments split across low-similarity angles barely exist in the blind
windows. No support for building actor-first candidate generation.

## Frozen for the hold-out

The pre-registered rule, unchanged: **0.45-0.53, <=6 h, >=2 shared actors**. Not re-tuned on these
results (the 4 h variant has fewer false joins here, but choosing it would be fitting to development
windows). The hold-out has little recall support (7 multi-source developments, 8 cross-source SAME
pairs) and is read mainly as a false-join check.

Development-level leaning before the hold-out: KEEP the current clusterer (no secondary link rule, no
actor-first). The open problem is over-merging within storylines, which none of the four options
addresses.
