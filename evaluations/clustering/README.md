# Clustering benchmark

This folder holds frozen historical windows with blind gold labels. They are used to measure narrative clustering before any change to it. The code is in `osint_monitor/benchmark/`, and the file format is described in `format.py`.

## Protocol

1. **Import a window.** Imports are read-only on their input and record each item's provenance.
   ```
   python main.py benchmark import-wayback --id 2026-08-15 --start 2026-08-15 --end 2026-08-17 --split development
   python main.py benchmark import-db --id 2026-09-25 --db data/eval/<copy>.db --start ... --end ... --split development
   ```
2. **Freeze the items before looking at anything else:**
   `python main.py benchmark freeze --window <id> --items-only`
3. **Label blind.** Work from `python main.py benchmark label-sheet --window <id>`, which lists items in publication order with no similarity or clustering information. Edit `labels/<id>.labels.yaml` and set `labelled_by`.
4. **Freeze the labels** in their own commit, before any evaluation:
   `python main.py benchmark freeze --window <id>`
5. **Development:** `python main.py inspect clustering-benchmark --development`
   This reports current metrics, a small sweep of rule variants and the actor-first probe.
6. **Freeze one candidate rule:**
   `python main.py benchmark freeze-rule --variant "<name>" --rationale "..."`
7. **Hold-out, once:** `python main.py inspect clustering-benchmark --holdout`
   This evaluates the frozen rule only. Each run is appended to `holdout_runs.jsonl`.

Evaluation refuses windows whose files no longer match the hashes in `manifest.yaml`. Changing a frozen file requires `--refreeze`, and the change is visible in Git.

## Caveats

- **Replay** runs the current pipeline on a temporary database and measures one-shot clustering. The daemon's incremental behaviour is not replayed.
- **Unreviewed pairs:** pairs that are neither in one gold development nor labelled related are treated as unrelated.
- **Scope:** results are benchmark results on a few windows, not estimates for all news.
