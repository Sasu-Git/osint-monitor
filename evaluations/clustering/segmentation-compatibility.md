# Segmentation compatibility: geographic containment and headline override

Branch `feat/segmentation-compatibility`, from main after merging `feat/clustering-benchmark` and
`feat/development-identity`. Code and config are frozen at 936d05c (3923f64 before the rebase onto the reconciled main; same tree):

- `osint_monitor/processors/geography.py` and `config/geography.yaml`;
- `development_segmentation` in config/event_grouping.yaml, with
  `location_match: containment`, `use_regions: false` and
  `headline_override: {max_hours: 6, require_shared_place: true, min_shared_actors: 0}`.

The override applies only when both headlines are reports.

## Design

- **Geographic compatibility.** Two place sets are compatible when some pair is the same place, or
  one contains the other. Containment comes from aliases, a place-to-parent map (cities and regions
  to countries), US region membership and directional prefixes ("northern X" is part of X). Places
  that only share a country are not compatible: Kyiv vs Odesa, New York vs Virginia. Supra-national
  regions ("middle east") are opt-in and off: on development windows they changed nothing. Names
  missing from the gazetteer match only themselves.
- **Headline override.** The headline-similarity guard does not cut a link between two report
  headlines published within 6 h of each other that name compatible places. Live blogs, roundups and
  analysis are never rescued: with them included, the 6 h override brought back 4 rolling-coverage
  links on development windows. An actor-overlap requirement (1 or 2 shared actors) changed nothing
  on development windows, so it is not required. 6 h is the time bound already used for close pairs;
  3 h gave identical development results and 12 h brought back unrelated links.

## Development windows (before the hold-out)

| | no segmentation | segmentation v1 (exact places) | v2 (this) |
|---|---|---|---|
| blind: multi-source recovered | 29/30 | 29/30 | 29/30 |
| blind: cross-source SAME linked | 54/55 | 54/55 | 54/55 |
| all dev: SAME pairs linked (incl. same outlet) | 76/114 | 72/114 | 74/114 |
| RELATED linked | 131 | 77 | 78 |
| UNRELATED linked | 25 | 3 | 3 |
| mixed clusters | 32/54 | 24/48 | 24/48 |

v2 compared with v1:

- **False splits fixed:** 2, both same-outlet. The Ervebo doses pair ("DR Congo" vs "DRC") and the
  Moscow mass drone attack pair.
- **Wrong links reintroduced:** 1 related (Ebola vaccine trial vs doses arriving), plus 1 uncertain.
- **New false splits:** none.

The development windows contain no cross-source false split caused by places or headline framing,
so development evidence for v2 is thin: it is a small positive. The design targets the two named
out-of-sample failures. Those windows (2026-08-31 and 2026-09-27-live) are therefore not blind to
this change. A fresh live window is the real test.

## Hold-out (run once, 2026-09-28; logged in holdout_runs.jsonl)

The hold-out split now holds 2026-08-31, 2026-09-10 and 2026-09-27-live. v1 figures are from the
earlier single runs; v2 has not been re-tuned.

| window | cross-source SAME: none / v1 / v2 | RELATED linked: none / v1 / v2 | UNRELATED: none / v1 / v2 |
|---|---|---|---|
| 2026-08-31 | 4/4 / 3/4 / 3/4 | 24 / 7 / 7 | 0 / 0 / 0 |
| 2026-09-10 | 3/4 / 3/4 / 3/4 | 28 / 2 / **6** | 3 / 0 / 0 |
| 2026-09-27-live | 24/25 / 23/25 / **24/25** | 38 / 18 / 18 | 7 / 7 / 7 |
| total | 31/33 / 29/33 / **30/33** | 90 / 27 / **31** | 10 / 7 / 7 |

Multi-source developments across the three windows: no segmentation 18/20, v2 17/20 (all 3+-source
developments are kept, 4/4).

- **False split fixed:** the nor'easter (region vs states). The headline override kept it:
  report/report, 0.8 h apart, compatible places.
- **False split not fixed:** Northern Cyprus. NER gave the BBC item the single place "cyprus ayten",
  a place name fused with a following person name, so no gazetteer entry can match it. The failure
  is NER noise, not geography. It was not patched after seeing it.
- **Wrong links reintroduced:** 4 related, all on 2026-09-10 and all from the headline override. They
  are same-day report headlines about one storyline: different 9/11 anniversary ceremonies ("Four
  former US presidents mark 25th anniversary in NYC" vs "Trump pays tribute ... at Pentagon ceremony"),
  and a Houthi advance vs a battles piece. This is the storyline merging the override was meant to
  avoid: close in time, compatible places, different occurrences.

2026-08-31 and 2026-09-27-live are not blind to v2: their failures motivated it. The fresh live window
required by the protocol cannot be built yet. Since 2026-09-28 12:00 UTC the daemon has collected
22 narrative-window items. A 24 h window closes at 2026-09-29 12:00 UTC.

## Recommendation: NEED ANOTHER LIVE WINDOW

Evidence so far:

- **Precision:** out-of-sample, related links fall 90 -> 31 and unrelated 10 -> 7.
- **Development recall:** blind development recall is untouched (54/55, 29/30).
- **Out-of-sample recall:** 30/33 vs a 31/33 baseline, so it is close to baseline. v1 was 29/33.
- **Against:** the gain over v1 is one fixed pair for four reintroduced related links. The windows
  that show the fix are not blind to the design.

That is borderline-positive, not decisive. Next step: build `2026-09-29-live` from 2026-09-28 12:00
to 2026-09-29 12:00 UTC, label it blind, freeze it, and run
`inspect clustering-benchmark --holdout --segmentation --window 2026-09-29-live` once. Enable
segmentation by default only if that window keeps cross-source SAME recall within one pair of the
baseline and keeps most of the precision gain.

## Remaining limitations

- NER noise in place names ("cyprus ayten") defeats both exact and containment matching.
- The headline override can rejoin same-day, same-place developments of one storyline (anniversary
  ceremonies, battlefield reports).
- Same-country different disasters (Nepal floods vs avalanche) stay merged: containment treats the
  shared country as compatible.
- Reactions, follow-ups, different actions by the same actors, and repeated actions in the same place
  are unchanged. Both strict xfails are kept.
- The gazetteer is curated: places missing from it only match exactly.
- Incremental daemon behaviour is not replayed.
