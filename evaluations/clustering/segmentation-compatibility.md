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

## Fresh live validation: pre-registration (written 2026-09-29 before the window closes)

- **Segmentation code under test:** frozen commit `936d05c`. The file blob
  `osint_monitor/processors/development_segmentation.py` is `fb58483`. Its SHA-256 over LF bytes equals
  the `code_sha256` logged by the previous hold-out run. The CRLF working copy on Windows hashes
  differently. `9a6aaed` is a documentation-only follow-up.
- **Window:** `2026-09-29-live`, 2026-09-28 12:00 to 2026-09-29 12:00 UTC (end exclusive), hold-out split.
  The source is a SQLite backup-API snapshot of the daemon eval DB, taken after about 13:00 UTC. The
  daemon DB is only read or copied, never written.
- **Default:** `development_segmentation.enabled: false`. It is not changed by this validation.
- **Procedure:** freeze items -> commit -> blind labels from the label sheet only -> freeze -> commit
  separately -> verify hashes -> one `inspect clustering-benchmark --holdout --segmentation --window
  2026-09-29-live` run. That run yields the baseline and segmentation from one replay. Pair-level
  diagnostics come from a deterministic re-replay, asserted identical to that run.
- **Decision criteria, fixed now:**
  - **ENABLE** only if all of these hold:
    - cross-source SAME recall stays within one pair of baseline;
    - multi-source development recovery stays similarly close;
    - most of the precision gain remains;
    - no new systematic false-split pattern appears;
    - the compatibility layer does not substantially reintroduce storyline-level over-merging.
  - **KEEP OFF** if any of these hold:
    - false splits are material;
    - the override causes significant false joins;
    - the precision gain is too small for the recall loss;
    - a new systematic failure mode appears.
  - **NEED MORE DATA** only if the window is too sparse, the result is genuinely borderline, or there
    are too few multi-source developments.

### Collection conditions in the window (operational metadata, checked 07:45 UTC)

- **Process:** the daemon (PID 42048, worktree at `a9edd18`) ran continuously. Its only scheduler
  start is 2026-09-25. It has no pause flag, no tracked changes, and no config file modified since the
  window start. DB `quick_check: ok`.
- **Host standby:** the machine went into standby (Windows Kernel-Power 506/507), so every tier
  missed its ticks during:
  - 14:27-18:47 UTC on 09-28;
  - 23:23-02:02 UTC and 02:05-05:59 UTC on 09-29.

  After each resume the RSS feeds were read in full. Narrative items by *published* hour during the
  gaps are in line with the same hours the day before (e.g. 15-17 UTC: 6/10/10 vs 5/10/7), which is
  consistent with the feed depth covering the gaps. Items published and rolled off a feed inside a gap
  would be missing, which biases the window toward lower-volume completeness, not toward any story.
- **Lock burst on resume:** at 06:02 UTC on 09-29, 29 items failed processing with `database is
  locked`. This happened right after resume, when all tiers ran at once. No other lock errors occurred
  in the window. Items that failed before storage are re-read on the next warm tick while still in
  the feed.
- **Other:** 3 timeouts in the government collector, which is structured and outside the narrative
  window.
- **Evaluator exposure:** while characterising the lock errors, the evaluator saw 8 truncated
  headlines from inside the window (the error message embeds the item title). The segmentation code
  and config are frozen and the labeller is a separate blind agent, so this cannot influence the rules
  or the labels. It is recorded for completeness.
