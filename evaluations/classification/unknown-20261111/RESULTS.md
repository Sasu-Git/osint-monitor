# Spanish/Italian classifier fallback: gate results (2026-11-11)

**Code.** `fix/v2-upstream-topic` `8049788` against `b695aa0`, on the same snapshot copy (`snap-20261102.db`,
sha `b5bb5728…`). Diagnosis frozen first (`2a6d27a`). **Nothing was changed after these results.**

## Gates

| Gate | Result |
|---|---|
| (a) `unknown` rate | **45.7% → 35.8%** overall (547 → 429). English 353 → 347 of 968; **Spanish 108 → 40 of 136; Italian 86 → 42 of 94** |
| (b) already-typed Developments changed | **0** (the fallback runs only when no English rule matched anything) |
| (c) precision of newly typed (seeded spot check, 30 of 118) | **11 right / 19 wrong = 37%**: **FAIL** |
| (d) pytest | full suite passed (exit 0; 12 new tests in `tests/test_classification_multilingual.py`) |

Newly typed (118): military_action 35, election 19, significant_statement 14, security_incident 12, and 38 others.

## Spot check (judged by reading headlines; not owner labels). Sample in `spot-check-sample.txt`

| Verdict | Developments |
|---|---|
| right (11) | D159 statement, D177 espionage, D325 commentary, D423 primaries, D615 summit, D656 sanctions, D802 negotiation, D840 tanker attack, D886 mines deployed, D902 church shooting, D1107 announcement |
| wrong (19) | D209 anniversary ("invasion" in a lead), D232 Nobel prize ("sanzioni"), D265 mixed with Messi, D275 knife attack typed as military, D409 not a summit (lead), D439 truce talk inside a mixed Development, D460 *calls for* resignation, D515 embassy opening, D543 sabotage trial, D636 settler violence typed as military, D648 orcas attacking sharks, D719 arrest warrant, D777 decree powers, D952 *possible* meeting, D1047 royal tour (one stray headline), D1126 protests, D1137 protests, D1158 "cualquier ataque" (hypothetical), D1173 "a semanas de las elecciones" (time anchor) |

## Why it fails

1. **One headline decides a mixed Development.** In most es/it Developments only one headline matches, and the vote
   has no majority requirement (the same is true of the English vote, but English Developments are less mixed).
2. **Lead-sentence votes** (D209, D265, D409) pull in incidental words.
3. **"ataque/atacan" is too broad** without the English rule order's security-first phrasings (knife attack, sabotage).
4. **Guards incomplete:** hypothetical ("cualquier ataque"), time anchor ("a semanas de las elecciones"), calls for
   ("pide la dimisión").
5. Legal stories (arrest warrants, trials) have no es/it legal guard.

## Verdict

**Do not merge.** The fallback lowers `unknown` a lot (es 79% → 29%, it 91% → 45%) and changes no typed Development,
but about 6 in 10 new types are wrong. That broadens false classifications, which the brief forbids.

**Proposal for the next cycle** (not implemented, so nothing is tuned to these results):
- headlines only;
- a type only when at least half of the Development's es/it headlines agree;
- security-first and legal guards mirroring the English order;
- the missing hypothetical, time-anchor and calls-for guards.

Re-measure on a **fresh** spot-check sample.
