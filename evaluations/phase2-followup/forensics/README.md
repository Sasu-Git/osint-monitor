# Giant-Development forensics (2026-10-27)

Read-only investigation of how the largest Developments formed. **No fix implemented**; no runtime code, rule,
threshold, Situation, production data or holdout was changed.

- `d398/FORENSIC-REPORT.md`: the deep dive (start here).
- `d398/counterfactual-cuts.md`, `d398/attachment-history.csv`, `d398/attachment-graph.json`,
  `d398/attachment-tree.svg`, `d398/analysis.json`, `d398/gravity.json`.
- `giant-developments/COMPARISON.md`, `failure-families.md`, `giant-development-summary.csv`, `blast-radius.csv`,
  `cases/` (per-case analysis and drift for D397, D449, D639, D399, D626, D514, D182).

## Inputs

- **Database.** A working copy of the 2026-10-27 live snapshot: SQLite backup API from a `mode=ro` source; the
  snapshot's sha256 is `3c0b2cd9c9a6e2347a055c62b1f88b7800f9d7b82228370983d48203ad0b4a39`. Scripts open the copy, never
  the live database.
- **Code.** The production modules at `adacb83` (worktree `../osint-monitor-timing`), imported unchanged. The identity,
  clustering, segmentation, dedup and lexical code and `config/event_grouping.yaml` are identical in `5f046b3`,
  `3eda6d0` and `adacb83`.

## Reproduce

All steps are lightweight (no clustering replay): a few minutes per Development, at below-normal priority.

```
python reconstruct.py --code-wt ../../../../osint-monitor-timing --db COPY.db --event 398 --out SCRATCH/d398-raw.json
FIRST_WRONG=8908 ENTRY_POINTS=10242 BOUNDARY="2026-10-13 09:45" \
  python analyze.py --full --raw SCRATCH/d398-raw.json --db COPY.db --code-wt ../../../../osint-monitor-timing --out d398
python gravity.py --svg --raw SCRATCH/d398-raw.json --analysis d398/analysis.json --db COPY.db --code-wt ... --out d398
python extra_cuts.py SCRATCH/d398-raw.json d398/attachment-graph.json
python blast.py --db COPY.db --code-wt ... --out giant-developments/blast-radius.csv
python compare.py --dir SCRATCH --events 398 397 449 639 399 626 514 182 --blast giant-developments/blast-radius.csv \
  --csv giant-developments/giant-development-summary.csv
```

The `*-raw.json` reconstructions (all reconstructed links) are not committed; rerun `reconstruct.py` to regenerate
them.

**Deferred until after Candidate A's C2:** an exact replay of the clustering ticks, to recover the cluster each
membership decision saw (CPU-heavy).
