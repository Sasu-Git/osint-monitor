# Location contract, iteration 3 on the fresh blind sample (2026-11-11): NOT READY

**Run.** Scored once, on the inputs frozen in `LOOKUP-FREEZE.md` (`88d9d97`) and `FREEZE-SCORING.md` (`ab77878`).
No label, sample, rule, gazetteer, extension or lookup change after the run. Gates are iteration 1's, **PROPOSED and
not approved**: every verdict below is report-only. Full tables: `RESULTS-TABLES.md`; per-case outputs: `outputs/`.

**Checks before reading the numbers.**
- `audit.py` re-run with `d06af11` reproduced the frozen baseline audit byte for byte (`07442444…`), so the `B1`
  method is valid.
- `decide(rules=())` on the iteration-3 code equals iteration 2 (`a73b9f3`) on all 100 cases.
- Modules run: iteration 1 `72506285…` (CRLF of `afbd4baf…`), iteration 2 `a0b365b7…`, iteration 3 `985afbcd…`
  (CRLF of `145a1a1e…`).

## Primary basis (blind first answers) and secondary (final labels)

| System | Agrees with gold (primary / secondary) | W removed (both) | C preserved (primary / secondary) | Verdict vs PROPOSED gates (W ≥ 80%, C ≥ 90%) |
|---|---|---|---|---|
| `B0` map `d06af11` (baseline) | 54 / 55 | — | — | baseline |
| `B1` map + aliases `346456f` | 54 / 57 | — | — | baseline |
| `I1` iteration 1 | 50 / 52 | 17/24 (70.8%) | 37/50 (74%) / 37/50 | fails on both bases |
| `I2` iteration 2 | 50 / 52 | 17/24 (70.8%) | 37/50 / 37/50 | fails on both bases |
| `I3-2a` | 50 / 52 | 17/24 | 37/50 / 37/50 | fails on both bases |
| `I3-3a` | 47 / 48 | 17/24 / 18/24 | 34/50 (68%) / 35/50 (70%) | fails on both bases |
| `I3-4a` | 51 / 53 | 17/24 | 37/50 / 37/50 | fails on both bases |
| `I3-5a` | 49 / 53 | 17/24 | 37/50 / 37/50 | fails on both bases |
| `I3-all` | 47 / 50 | 17/24 / 18/24 | 34/50 / 35/50 | fails on both bases |

W and C sets come from the baseline map against gold: the map shows 74 of the 100; 50 of those are right (C) and 24
wrong (W) on both bases. **No system's verdict differs between the bases: nothing is inconclusive.**

## What each rule did (relative to iteration 2, per case)

- **2a (containment collapse):** no case changed.
- **4a (Congo cues):** 1 case, D1212 COG → COD, correct on both bases.
- **5a (Hong Kong / Macau):** 1 case, D1330 CHN → HKG: wrong on the blind basis (first answer CHN), right on the final
  basis (owner ruling 2026-11-10). D1322 did not change.
- **3a (locative-only countries):** 11 cases changed.
  - Gains: D1227 (both bases), D1218 (blind only), D1232 (final only).
  - Losses: D1302 and D1332 (a right country dropped to NONE), D1287 and D1289 (a country where gold is NONE), both
    bases; D1210 (blind only); D1218 and D1319 (final only).
  - Neutral (wrong before and after): D1234, D1312.
  - Net −3 on the blind basis, −4 on the final basis.

## Reading

- **No iteration beats the deployed map on the fresh sample.** The map agrees with the owner on 54–55 of 100 (57 with
  aliases); iterations 1–3 agree on 47–53. The map's errors (24 wrong points, 22 missed) are real, and the contract
  removes 17–18 of the 24 wrong points, but it loses 13–16 of the 50 points the map already has right.
- **The fresh sample confirms the audit-set result of iterations 1 and 2:** good wrong-point removal, poor
  preservation (74% here, 44% on the audit set for iteration 2), far from the PROPOSED 90%.
- **The low-risk rules are nearly inert** on fresh data (2a: 0 cases, 4a and 5a: 1 each). **3a is net negative.**
- **The aliases branch (`346456f`) is the only change that helps on the final basis** (2 Hong Kong cases), and it is a
  display change, not a location-contract change.
- **Not ready** for runtime wiring or backfill. Any next step is an owner decision (for example, keep the map's stored
  point where the contract has no stronger evidence, instead of replacing it).

Continuity re-scores of iterations 1 and 2 on their own audit set: `CONTINUITY.md`.
