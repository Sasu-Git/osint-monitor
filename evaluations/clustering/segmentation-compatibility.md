# Segmentation compatibility: geographic containment and headline override

Branch `feat/segmentation-compatibility`, from main after merging `feat/clustering-benchmark` and
`feat/development-identity`. Code and config are frozen at 3923f64:

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
