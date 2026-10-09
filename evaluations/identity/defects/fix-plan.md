# Identity follow-up: proposed generalizable fixes (pre-registered, 2026-10-09)

Written before any identity code changed. Baseline: identity code `0eff3ea` (cross-language stage disabled), frozen
defect set `manifest.yaml` (128 cases: 105 wrong, 23 correct controls).

## Diagnosis (offline features of every failing case and every gold pair; `defect-review.md`)

| mechanism | defect cases | finding |
|---|---|---|
| storyline creep across days | Christa Pike (T012-T014, T040), Ebola trial vs doses (A021/A022), Carney (A002), West Bank (A023), French protests (G07), Hormuz (R014 ...) | distinct occurrences 14-41 h apart linked one report at a time; no guard fires (cosine 0.53-0.82) |
| chains across a guard | C012, C037, C073, C094, C112, C115 | a headline guard fires between the pair, yet a chain of other links joins them |
| English-only model on es/it text | C002, C007, C017, C022, C026, C079, C105, C106 | in Spanish and Italian, SAME and DIFFERENT pairs have the same cosine distribution (median 0.44 vs 0.47): similarity carries no identity signal |
| same-day distinct actions | Pope (R046), Netanyahu (R100), Malaysia (T009), Xi visit (B008) | distinct actions hours apart; nothing in the text separates them |
| same-outlet release package | C034, C103 | a proposal and its own Q&A / factsheet from the same outlet in the same minute never link (same-outlet links need near-identical headlines) |
| place guard on one occurrence | C066, C092, C113, C005 | `disjoint_locations` cuts one occurrence that names two places (a diverted flight); owner rule P7: a place conflict is never outweighed |
| below the link threshold / not clustered | B002, B004, C013, C064, G01 (0.52), G08/G09 (GDELT headline-only, accepted cost) | no generalizable signal beyond lowering the threshold |
| two Developments for one occurrence | U110, U131 | formed in different ticks; reconcile never merges existing Developments (ID stability) |

## Rules considered

| rule | gold effect (offline estimate) | decision |
|---|---|---|
| **T24: one occurrence spans at most 24 h.** A report joins an existing Development only if published within 24 h of its earliest report; a new Development's items are split into 24 h spans before the link and origin checks. | gains A002, A023 and the Pike/Hormuz pairs over 24 h; gold SAME pairs over 24 h apart: 1 (B007, already apart); 9 SAME pairs 12-24 h apart are kept | **implement** |
| **P1: supporting documents of one release.** Two items from the same outlet published within 1 h link when one headline names a supporting-document form (Questions and answers, Q&A, Factsheet / Fact sheet) and their cosine passes the link threshold. The contract: "official supporting documents; a Q&A, factsheet or release package" are the same Development. | gains C034, C103; the only same-outlet DIFFERENT pair at that time and similarity (C003, two Federal Register accreditations) names no document form | **implement** |
| R1: no chain across a guard-incompatible pair | gains 6 (C012 ... C115) but 7 SAME pairs currently together also carry a headline guard (C011, C014, C030, C036, C043, C058, C077): guard strength does not separate them | rejected: recall cost equals the gain |
| T12: 12 h span | would also split 9 correct SAME merges 12-24 h apart | rejected |
| higher link threshold for es/it text | SAME and DIFFERENT es/it pairs are not separable by cosine (11 SAME together vs 14 DIFFERENT together) | rejected: the fix is a multilingual clustering model, outside this follow-up |
| outweigh the place guard with P7 anchors | would fix the FlyDubai cases | not implemented: contradicts owner rule P7 (a place conflict is never outweighed); owner decision |
| merge existing Developments | would fix U110, U131 | not implemented: breaks Development ID stability |

## Expected wins and risks

- T24: removes cross-day storyline creep beyond 24 h (about 6-8 defect cases: Pike T012/T013/T014, R014, A002 = R013,
  A023 = R029). Risk: a Development whose reports legitimately span more than 24 h is cut; items after 24 h start a
  new Development only if they qualify on their own (two independent origins), otherwise they stay below the layer.
  This is stricter identity, never looser: no standard is lowered, single-source holdback unchanged.
- P1: links release packages (C034, C103). Risk: same-outlet supporting documents of a different release within the
  hour, limited by the link threshold.
- Not addressed (remaining blockers): same-day distinct actions, es/it overmerges and splits (English-only model),
  place-guard splits (P7), sub-threshold recall, Developments formed twice.

## Gates after implementation

Frozen defect set; identity gold revision 4 (development); Phase 2 identity holdout (regression check of the one-time
scored holdout); clustering benchmark; segmentation benchmark; entity benchmark; Situation dry-run; duplicate
membership and single-source invariants. Every changed gold case is explained. Stop if the gains need broad precision
regressions.

## Amendment 1 (after the first scoring run `t24p1`, before any other change)

Run `t24p1` (`score-t24p1.json`): defect set 23 -> 30 correct (8 overmerges fixed, 1 control broken), gold 157 -> 160.
P1 had no effect in the data: the release-package items now link, but they come from one outlet, so the
single-source holdback (unchanged) keeps them below the Development layer.

The one regression (C114, SAME) is an artifact of how T24 split new items: chronological chunks anchored at the
earliest item. In C114's cluster an unrelated earlier report (DW, C115 DIFFERENT) opened the first chunk and pushed
the later of the two same-occurrence reports (9 h apart) into a second chunk. The rule stays the same (a Development's
reports span at most 24 h); its implementation for new Developments changes: linked new items merge in descending
similarity order, and a merge is refused when the merged group would span more than 24 h. No threshold or
parameter changes. Run label `t24p1-v2`.
