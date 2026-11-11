# Iteration 3, step 4: scoring rule and rule code frozen (2026-11-11, before any system output)

The scoring rule is `SCORING.md`. Gates are iteration 1's and remain **PROPOSED, not approved**: results are
report-only against them. Nothing below is changed after the run.

## Scoring files (sha256, LF bytes)

| File | sha256 |
|---|---|
| `SCORING.md` | `53a1baa750c9939c97b49f74c3bd3eba6f9b67741272dae5d386d39b3304583f` |
| `locate.py` | `b8af3c5308aaa8f4bf1174631ec8f7d677bbcbd93d7963dd2b6263a30518a1d9` |
| `baseline_outputs.py` | `0db7b11859c00d8a1ad73c9c6cd1f856d2540ad02560d670b376cc7d7bf95e94` |
| `score.py` | `32ad5058d139127987c4fd9b5ac72f5d737c2dbbfc72c2cfb9161032244aa98d` |
| `rescore_iter12.py` | `0badfc7c4a77aab30fbdba77c1276ed65ec886ef467a3ad004350cc0d7600dae` |
| lookup (`LOOKUP-FREEZE.md`) | `lookup-overrides.json` `6a30949d…`, `lookup_audit.py` `b220df37…` |

## Rule code per system

| System | Commit | `event_location.py` |
|---|---|---|
| `I1` | `d842feb68db13ede232d453af46aab67bde74c14` | git blob (LF) `afbd4baf…` = iteration 1 FREEZE.md; exported with CRLF `72506285…` |
| `I2` | `a73b9f3e03e5d997abe05d78045b5453fde254ba` | CRLF `a0b365b7…` = iteration 2 FREEZE.md |
| `I3-*` | `c5e45f41c019c2780a50fd5284ac091c8414faa2` (unchanged at this branch's HEAD) | git blob (LF) `145a1a1e…`; this worktree's CRLF bytes `985afbcd…` |
| `B0` | `d06af1140fe9cdea489164b1697c443df10ed60b` (map) | frozen output `audit-all-20261105.json` `07442444…` |
| `B1` | `346456fe52cba73466386eabc8d848e0f51981ec` (map with aliases) | `audit.py` at `b7949028` (`359fab29…`), `d06af11` `config/sources.yaml` (`9f372d81…`) |

Shared: `config/geography.yaml` `21e0eb38…` is identical in all five trees; `place_extension.json` `5924ddf2…`
(iterations 2 and 3).

**B1 method check (run before B1 is used):** `audit.py` re-run with `PYTHONPATH` = `d06af11` on the same snapshot
must reproduce the frozen audit's `shown` and `point_country` on all 100 sample cases. If it does not, `B1` is
reported as not reproducible and left out of the verdicts.

## Rule switches for `I3-*`

`locate.py --rules`: `2a`, `3a`, `4a`, `5a` alone, and `2a,3a,4a,5a`. Consistency check: `--rules ""` on the
iteration-3 code must equal `I2` on every case.
