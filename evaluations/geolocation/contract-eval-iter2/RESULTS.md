# Location contract, iteration 2 (2026-11-03): NOT READY

**Run.** Scored once, on the inputs frozen in `FREEZE.md` (commit `a2ef830`): the same snapshot, audit cases,
acceptance cases and `evaluate.py` as iteration 1. No rule was changed after scoring. Gates are `PROPOSED`.

| Measure | Iteration 1 | **Iteration 2** | PROPOSED gate |
|---|---|---|---|
| Audit W (wrong stored point) removed | 91 / 94 (96.8%) | **88 / 94 (93.6%)** | ≥ 80%: met |
| Audit C (right stored point) preserved | 24 / 81 (29.6%) | **36 / 81 (44.4%)** | ≥ 90%: **not met** |
| C lost to NONE / C moved to another country | 36 / 21 | 23 / 22 | — |
| Audit P (partly right) | EC 9, EP 9, NONE 15 | EC 10, EP 10, NONE 13 | — |
| Acceptance cases passed | 4 / 16 | **4 / 16** (G02, G03, G04, G06; same as iteration 1) | — |

## What changed, case by case

**C gained (12; 11 from NONE, 1 from another country):**
- **Extension (10):** Kaliningrad (D92), Altoona (D127), Nueva York (D146), Marsiglia (D442), Riad (D465),
  Yerevan (D643), Estambul (D681), Nancy (D796), Karak (D902), Kidal (D249).
- **Extension, Bosnia now named (1):** D1092 (previously another country).
- **L1 revision (1):** Venezuela (D691).

**L1 revision fired correctly but is scored CHANGED (1):** South Sudan (D286). The evaluation's ISO lookup (web
`geo.py` at `ab45312`, frozen) cannot map "south sudan". It is a harness limitation, not counted as a pass.

**W regressions (4):**

| Case | Location given | Cause |
|---|---|---|
| D360 | New York | "Nueva York" is a real New York, but this story's stored point was judged wrong |
| D420 | Djibouti | "Gibuti" in the lead of a story about Cuban prisons |
| D734 | Spain | "Pacífico": a Spanish-language region word missing from the U3 region list |
| D941 | Marsiglia | Marseille, in a West Bank story |

**W gained (1):** D1160, Antigua resolved to Guatemala.

## Why C is still lost (45)

| Cause | C cases | Fixed by these three changes? |
|---|---|---|
| Place only outside the headline/lead window (L1 window) | 13 | no (window unchanged) |
| Country named as the place but not the stored one (e.g. "Brasile" → USA, D148; Bosnia election → Ukraine, D154; Ceuta → Spain, D438) | 8 + 9 single-place | partly: an actor/subject country is often the wrong one, and the L4 choice of country is unchanged |
| L5 ties: several places or countries, none dominant | 10 | no (L5 unchanged) |
| "Congo" ambiguity (COD vs COG) | 3 | no (gazetteer) |
| Hong Kong as actor: the gazetteer files it as a city in China, so the L1 revision (countries only) does not apply (D96, D1081, G08) | 3 | no |
| Disputed / territory ISO mapping (Vatican, Western Sahara) | 2 | no (harness and U4) |

**Acceptance failures that the three changes target:**
- **G10 (La Liga):** now returns Madrid. "La Liga" is filtered, but "Madrid" (from "Real Madrid") is typed as a place
  by NER.
- **G11 (Man City):** now returns Liverpool (another mention in the reports).

In both, the non-place filter works on the mention it targets. The expected NONE is lost to a *different* mention that
the gazetteer knows.

## Reading

- **Iteration 2 moves preservation from 29.6% to 44.4%** at a cost of 3.2 points of removal. That is far from the
  proposed 90%.
- **The remaining loss is mostly outside the three approved changes:** the headline/lead window, the choice of country
  under L4/L5, and gazetteer identity (Congo, Hong Kong).
- **Not ready** for runtime wiring or backfill.

**Any next iteration would need new owner decisions**, for example:
- widen the L1 evidence window;
- a rule for choosing between subject and place countries;
- Hong Kong / Macau as their own entities, like U4;
- a multilingual region list.

Each would be a contract change. None is applied here.
