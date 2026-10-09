# Development identity defect set (2026-10-09)

Owner request: a frozen review set of the identity failures that block or distort Phase 3 relations
(`../../relations/PHASE3-STATUS.md`). No identity logic has changed; the rejected cross-language stage stays disabled.

| file | what |
|---|---|
| `defect-review.md` | **reviewer-facing sheet**, grouped by class |
| `defect-cases.json` | the same cases, machine-readable |
| `owner-verdicts.yaml` | owner verdicts per case (class / expected: ACCEPT or a correction; note) |
| `manifest.yaml` | frozen candidate manifest: counts, SHA-256 of outputs and every input |
| `build_defect_set.py` | builder (the class rules are in its docstring) |

Baseline: identity code `0eff3ea` (Phase 2 identity, GDELT headline-only rule), replayed with the fixed replay clock.
Current Developments come from the existing deterministic replays (`relations/runs-rev2/`,
`relations/runtime/runs/`). The identity gold's holdout split and both sealed holdouts were not read.

## Integrity check note

`scripts/gold_check.py` passes on the gold files (identity gold, revision 3/4 additions, checks 2-7) but reports a
hash mismatch on `review-rev3/draft-labels.json` and `review-rev3/labeller-input.md` in any fresh checkout. Cause:
the two files were written with CRLF line endings and hashed as such; Git stores them with LF. Converting the
checked-out files back to CRLF reproduces the frozen hashes exactly (`bd999456...`, `03f5e21e...`), and the check
passes in the worktree that holds the original bytes (`osint-monitor-xlang`). The content is unchanged. Making the
check line-ending-neutral (or pinning `eol=lf` for evaluation files) is a tooling decision left to the owner.
