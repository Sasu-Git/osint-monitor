# Actor normalisation (Situation-v2 prerequisite): deploy readiness note

Prepared 2026-11-11. **Not deployed, not tagged, not merged.** The owner treats `b695aa0` as a successful
prerequisite candidate; deploy only on separate owner approval, through the normal VM runbook.

| | |
|---|---|
| Branch / SHA | `feat/actor-normalization-v2pre` at `b695aa0` (code `2f23f59`), pushed |
| Base | `main` `0d3382d` = `production-stable-20261111` (`484dcc8`) + ops-only files; fast-forward mergeable |
| Schema | **no change**, no migration |
| Gates (`RESULTS.md`) | entity benchmark byte-identical; identity gold check passed; Phase 2 identity identical; 764 pytest passed; 9/10 defect expectations (1 mis-specified, documented); 2 correct same-class merges outside the list (documented) |

## Code changed against `0d3382d`

| File | Change |
|---|---|
| `config/actors.yaml` | non-actors (party words, English, Long March); alias `Donald J. Trump`; represents for three full names |
| `osint_monitor/processors/actors.py` | `collapse_variants` (set-level, gazetteer-guarded) |
| `osint_monitor/processors/situations/canonical.py` | `ActorCanonicalizer.keys` uses it |
| `tests/test_actor_normalization_v2pre.py` | 25 tests |

## Expected live effects (new decisions only)

- **New** Situations can no longer be founded on one person counted twice, a person and their own state, a party
  word, the language "English" or a rocket. Existing Situations are sticky: the deploy changes no stored Situation.
- Situation keys collapse for the defect patterns; Development identity (topic keys) changes only where a B or C
  name is present (17 of 1198 Developments on the 11-02 snapshot).
- About 11 more PERSON principals per 1,200 Developments (the three full names are now configured actors).

## Gates for the deploy itself (normal VM runbook)

1. Pre-deploy check with `PYTHONPATH` = the target worktree (the venv is an editable install of the main repo).
2. VM: pause, backup-API copy of the VM DB, rehearsal on that copy with the target code, migrate expecting no delta,
   POST-DEPLOY OK, re-pin `/etc/osint/pinned_commit`, restart `osint-daemon`.
3. C1 (after 3 warm runs) / about 2 h / C2 (24 h), using absolute UTC deadlines (timed-check learning 2026-11-11).
4. At C2, additionally:
   - no Situation created from a name-variant pair, a person and their own state, or a listed non-actor word;
   - principal-flag churn on Developments updated during the soak, limited to listed names;
   - Development-creation rate within the usual bound.

## Separately gated afterwards (never inside the deploy)

Retiring the existing defect Situations (`javier-milei-milei`, `elon-musk-musk`, `christa-pike-pike`,
`machado-maria-corina-machado`, `bukele-el-salvador-nayib-bukele`, `emmanuel-macron-france-macron`,
`donald-j-trump-united-states`, `democrat-united-states`, `china-chinas-long-march`, `rachel-simon`): a fresh VM
snapshot, `scripts/repair_situations.py` dry run, owner review of the exact list, backup, apply, verify.

## Open point for the owner

Ship this alone (smallest blast radius), or bundle it with the other upstream fixes (topic classification, principal
extraction, place containment) once they pass their own gates. Recommendation: **alone first**. It is gated, small and
independent, and the others are still in development.
