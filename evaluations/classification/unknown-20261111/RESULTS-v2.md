# Stricter Spanish/Italian fallback: gate results (2026-11-11)

**Code.** `fix/v2-upstream-topic` `da8033d`: the stricter design recorded in `RESULTS.md`, built on `ef1f0e7` as one
commit. It is measured on the same snapshot copy (`snap-20261102.db`, sha `b5bb5728…`) against the baseline
`diagnosis-base.json` (code `b695aa0`). **Nothing was changed after these results.**

## Design (as specified)

- Headlines only.
- A type only when at least half of the Development's Spanish/Italian headlines agree.
- Security-first and legal guards mirroring the English rules.
- Hypothetical, time-anchor and calls-for guards.
- Military action only with a military means or object (never a bare "ataque").

## Gates

| Gate | Result |
|---|---|
| Already-typed Developments that change type | **0** |
| `unknown` rate, all | 45.7% → **42.5%** (547 → 509) |
| English | 36.5% → 36.4% (353 → 352 of 968) |
| Spanish | 79.4% → **62.5%** (108 → 85 of 136) |
| Italian | 91.5% → **76.6%** (86 → 72 of 94) |
| Newly typed | 38 |
| **Precision on a fresh sample** (≥ 90% required) | **23 / 30 = 76.7%: FAIL** |
| pytest | **781 passed, 3 xfailed** (17 tests in `tests/test_classification_multilingual.py`) |

**Fresh sample.** Seed **20261112**. Drawn from the 38 newly typed Developments after excluding the 30 reviewed in
`RESULTS.md` (8 overlapped), leaving a pool of exactly 30, so the sample is the whole pool. Judged by reading the
headlines, not by owner labels. Listing: `spot-check-v2-sample.txt`.

| Verdict | Developments |
|---|---|
| right (23) | D146, D148, D213, D226, D230, D238, D271, D560, D561, D570, D584, D606, D609, D645, D661, D673, D915, D967, D984, D1071, D1079, D1131, D1157 |
| wrong (7) | D391 election *postponed* typed as an election; D434 "wants a truce" typed as a ceasefire; D807 the Pope's "let there be a truce" (a calls-for phrasing the guard does not cover); D764 NATO *reinforces presence* after drone attacks (a deployment, typed as military action); D814 and D895 celebrity remarks typed as significant statements; D1070 a celebrity's compensation claim in a mixed Development |

## Verdict

**Do not merge.** The stricter version removes the gross errors of the first fallback. Bare "ataque", lead votes and
single stray headlines no longer type a Development. Precision rose from 37% to 77%. It is still below the 90% gate,
and it now recovers only 38 Developments (`unknown` 45.7% → 42.5%).

The remaining errors are not lexicon gaps that more words would fix:
- **intent versus act:** "wants a truce", "postpones the elections", "let there be a truce";
- **statements by non-political figures:** the `significant_statement` type has no notion of who is speaking.

Closing those needs either the actor-role layer (is the speaker a political principal?) or a modal/intent parser.
Both are upstream of keyword rules and out of scope here.

Side observation, out of scope: the existing English rules already match some Spanish words (for example
`bombard\w*` matches "bombardeo"), so a Spanish legal headline can still be typed military action by the English
pass.
