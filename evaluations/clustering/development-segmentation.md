# Development segmentation: benchmark results

Implementation: `osint_monitor/processors/development_segmentation.py`. Commits 23a54d2 (the
segmentation step) and 183b195 (benchmark evaluation mode). Configuration:
`development_segmentation` in config/event_grouping.yaml. It is off in production and forced on
for evaluation. Guards:

- `analysis_headlines: true`
- `min_headline_similarity: 0.5`
- `disjoint_locations: true`

Rationale: development-identity-diagnosis.md. Command:
`python main.py inspect clustering-benchmark --development --segmentation`.

## Development windows (written before the hold-out run)

Development windows are 2026-07-21, 08-07, 08-15, 08-21 (blind) and 2026-09-25 (not blind).

| | before | after |
|---|---|---|
| **blind: multi-source developments recovered** | 29/30 | **29/30** |
| **blind: cross-source SAME pairs linked** | 54/55 | **54/55** |
| all dev: multi-source recovered (2 sources / 3+) | 33/37 (28/32, 5/5) | 32/37 (27/32, 5/5) |
| all dev: cross-source SAME pairs linked | 58/64 | 57/64 |
| RELATED_BUT_DISTINCT pairs linked | 131 | **77** (-41%) |
| UNRELATED pairs linked | 25 | **3** (-88%) |
| mixed clusters | 32/54 | 24/48 |
| singletons wrongly clustered | 70 | 44 |
| multi-item developments fully recovered (incl. single-outlet) | 36/55 | 32/55 |
| analysis items kept as commentary | - | 8 |

Per window, related/unrelated wrong links fall 57/10 -> 40/0, 46/5 -> 25/3, 11/4 -> 6/0 and
16/6 -> 5/0 on the blind windows. Cross-source SAME links are unchanged in every blind window.

Recall cost:

- one cross-source pair on 2026-09-25 (CASI: two outlets' headlines at cosine 0.43, one framed as
  the think tank "will continue");
- three same-outlet pairs whose only connection ran through a split-off item (night-11 strikes,
  Moscow drone attack, Ervebo doses). Same-outlet items link only on near-identical headlines, so
  losing the bridge separates them.

Acceptance criterion: precision improves with no degradation of the blind cross-source recall
baseline. Met on development windows.

## Frozen for the hold-out

The code at 183b195 and the configuration above are frozen. The hold-out is run once, next, and is
read mainly for false joins: it holds 7 multi-source developments and 8 cross-source SAME pairs.

## Hold-out (run once, 2026-09-28, logged in holdout_runs.jsonl)

Windows 2026-08-31 and 2026-09-10 (blind). Code and configuration as frozen above.

| | before | after |
|---|---|---|
| multi-source developments recovered (all 2-source) | 6/7 (1 partial) | 5/7 (1 partial, 1 missed) |
| cross-source SAME pairs linked | 7/8 | 6/8 |
| RELATED_BUT_DISTINCT pairs linked | 52 | **9** (-83%) |
| UNRELATED pairs linked | 3 | **0** |
| mixed clusters | 8/14 | 5/13 |
| singletons wrongly clustered | 24 | 11 |
| analysis items kept as commentary | - | 3 |

Precision improves on independent data more than on development windows. One cross-source SAME pair
is lost: the Northern Cyprus ferry sinking. Al Jazeera ran "Rescuers search for 18 missing after boat
capsizes off Northern Cyprus" and BBC ran "'She slipped out of my hand' - children missing after ferry
sinks off northern Cyprus". Both are report headlines, with headline cosine 0.58, so the
disjoint-locations guard cut the link. The extracted place names do not overlap, though both name the
same place ("Northern Cyprus" / "Cyprus"). **Failure mode: location granularity.** A sub-region and
its country, or two spellings of one place, count as disjoint. Not fixed here: the hold-out is not
used for tuning. A containment-aware location match is the obvious remedy. It must be designed on
development windows and checked on the live window.

Read with the thin hold-out recall support (8 SAME pairs): the recall change is 1 pair, and it has
an identified, specific cause. It is not a general drop.

## Live out-of-sample window (run once, 2026-09-28)

Window `2026-09-27-live` covers 2026-09-27 00:00 to 09-28 12:00, drawn from the daemon's eval DB. It
has 173 items and 6 sources, including Defense News and Breaking Defense. Labels are blind and were
frozen before replay.

| | before | after |
|---|---|---|
| multi-source developments recovered (2 sources / 3+) | 12/13 (8/9, 4/4) | 11/13 (7/9, 4/4) |
| cross-source SAME pairs linked | 24/25 | 23/25 |
| RELATED_BUT_DISTINCT pairs linked | 38 | **18** (-53%) |
| UNRELATED pairs linked | 7 | 7 |
| mixed clusters | 8/16 | 6/14 |
| singletons wrongly clustered | 19 | 13 |

- **Lost SAME pair:** the nor'easter. Al Jazeera ran "Powerful storm floods US Northeast, causes power
  outages" and BBC ran "One dead as nor'easter storm pummels New York and New Jersey". Headline cosine
  is 0.35, so the headline-similarity guard cut the link: one outlet framed the story by region, the
  other by states.
- **Unrelated links left:** all 7 are two Nepal disasters, the floods and the Himlung avalanche. They
  share the country, so the location guard cannot see them as different places. This is the same
  template failure within one country.
- **Baseline recall:** the current clusterer links 24/25 cross-source SAME pairs on the current source
  mix, so the 2026-09-25 recall gap does not reproduce.

The frozen link rule was also run once on this window, the planned day-2 recall check. It adds 1
SAME join and 2 related joins, and completes 13/13 multi-source developments. Summed over the
independent windows (4 blind dev, 2 hold-out, live), the rule adds 1 true join against 15 false joins.
The KEEP recommendation for the link rule stands.

## Assessment

Precision improves on every evaluation set:

| set | related links | unrelated links |
|---|---|---|
| dev | 131 -> 77 | 25 -> 3 |
| hold-out | 52 -> 9 | 3 -> 0 |
| live | 38 -> 18 | 7 -> 7 |

Cross-source recall is unchanged on the blind development windows. It drops by **one pair** on the
hold-out (7 -> 6 of 8) and one on the live window (24 -> 23 of 25), each costing one 2-source
development. Out-of-sample, the guards removed 63 wrong links (related 43+20, unrelated 3+0) for 2
lost true links.

The acceptance criterion was precision gains with no recall degradation. It holds on development and
misses by one pair on each out-of-sample set. Both misses have specific causes:

- location granularity ("northern cyprus" vs "cyprus");
- headline framing (region vs states).

So segmentation stays **off by default**. Enabling it is a product decision, which the evidence
supports if Development purity is worth about 1 lost 2-source story in 30. The next increment, which
needs its own prompt, is a containment-aware location match (country contains region). It is expected
to recover the Cyprus-type case, and must be designed on development windows and checked on the next
live window.

## Remaining failure modes

1. Report vs report within one storyline: reactions, different actions by the same actors, follow-ups.
   77 / 9 / 18 related links remain on dev / hold-out / live.
2. Repeated actions in the same place on nearby days (strike nights). They need an explicit event
   date, and RSS descriptions rarely carry one. Pinned by a strict xfail test.
3. Different disasters in the same country (Nepal floods vs avalanche).
4. Location granularity: a sub-region vs its country, or name variants.
5. Headline framing: two outlets headline one event very differently (headline guard).
6. Incremental daemon behaviour, where later ticks extend existing events, is not replayed by the
   benchmark.
