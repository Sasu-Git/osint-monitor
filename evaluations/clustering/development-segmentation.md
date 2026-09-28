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
