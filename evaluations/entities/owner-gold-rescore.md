# Entity benchmark rescored on the owner-reviewed gold (revision 2)

Gold revision 2 (`gold/manifest.yaml`, commit bf39b7a) applies the owner-reviewed evaluation sheet
(`owner-review-2026-09-30.md`) to the principal and role labels. This note rescored the **saved predictions** of
every stage (`runs/*.json` -> `runs/r2/*.json`, `inspect entity-benchmark --rescore`) with no implementation
change, so every difference from `entity-resolution.md` comes from the labels alone. Rescoring the saved
revision-1 runs against revision-1 gold reproduces their stored summaries exactly (checked before the change).

## Gold corrections (revision 1 -> 2)

| Dev | Change |
|---|---|
| D05 | principals `Saudi Arabia, France\|Macron, Pakistan\|Sharif, Turkey, Houthis` -> `Saudi Arabia` (lead); France/Pakistan/Turkey secondary actors (role actor, not principals); Houthis role `actor` -> `actor\|target` |
| D07 | principals `United States\|U.S. Navy, United Kingdom` -> `United States, United Kingdom` (co-principals); U.S. Navy subordinate participant |
| D10 | principal `Argentina\|Javier Milei` -> `Argentina`; Milei role added: `representative` (represents Argentina); Falkland Islands `location` -> `location\|subject` |
| D13 | principal `Italy\|Giorgia Meloni` -> `Italy\|Italian government`; Meloni role added: `representative`; identity "Italian government" added to accepted names |
| D15 | Putin role `actor` -> `actor\|representative` (represents Russia) |
| D21 | roundup item 396 recorded (`roundup_items`); Malaysia kept, established by item 150 |
| D23 | `represents: {Donald Trump: United States}` documents the owner-accepted `Trump\|United States` alternative (US role stays institutional_context) |
| D24 | principal `United States\|Donald Trump` -> `United States` (the sheet's principal column is "Iran; United States"); Trump role `subject` -> `subject\|representative` |
| D25 | unchanged principals, now annotated: Commission lead, Council co-principal |

Benchmark-only schema: role alternatives `a|b`; gold-only role `representative`; bookkeeping fields
`principal_roles` (lead / co_principal / secondary / subordinate), `represents`, `roundup_items`. These are not
scored and nothing in the runtime reads them. Scoring rule unchanged: a predicted principal that is not a gold
principal (a secondary actor, a representative whose alternative was dropped) is a false positive.

Consistency audit (`scripts/gold_audit.py`, 10 checks, all pass): each principal has an actor role, or is the
entity its actor alternative represents; no duplicate role keys; every representative has `represents`;
accepted names of distinct identities do not overlap; no target or location is a principal; actors that are
also publishers (D25 Council, Commission) are named in the item text; each principal is named in a
non-roundup item; secondary actors act and are not principals; principals equal the owner sheet's column.
A seeded-error copy (secondary promoted, location promoted) fails checks 1, 6, 9 and 10 as expected.

Items the runtime treats as roundups by headline but the owner did not list: D05 #660, D08 #161, D14 #926,
D15 #282, D18 #1008. Every gold principal in those Developments is also named in a non-roundup item.

## Corrected results (same predictions, revision-2 gold)

| Metric | baseline (main) | current branch | en | it | es | es+it |
|---|---:|---:|---:|---:|---:|---:|
| NER detection precision | 86% (370/431) | 96% (378/392) | 98% (356/365) | 77% (10/13) | 86% (12/14) | |
| NER detection recall | 94% (370/392) | 96% (378/392) | 96% (356/369) | 100% (10/10) | 92% (12/13) | |
| Entity typing accuracy | 92% (341/370) | 95% (359/378) | 95% (339/356) | 90% (9/10) | 92% (11/12) | |
| Canonical resolution accuracy | 92% (340/370) | 97% (367/378) | 99% (352/356) | 80% (8/10) | 58% (7/12) | |
| Canonical-name hygiene | 96% (354/370) | 99% (373/378) | 99% (351/356) | 100% (10/10) | 100% (12/12) | |
| Principal-actor precision | 31% (17/55) | 78% (18/23) | 75% (15/20) | - | 100% (2/2) | 100% (1/1) |
| Principal-actor recall | 65% (17/26) | 69% (18/26) | 65% (15/23) | - | 100% (2/2) | 100% (1/1) |
| Actor-role accuracy | 15% (18/119) | 56% (67/119) | 57% (64/112) | - | 67% (2/3) | 25% (1/4) |

Principal and role metrics are per Development. Spanish rests on one Development (D24: 2 principals, 3 roles)
and the mixed it/es column on one (D23: 1 principal, 4 roles); Italian-only Developments have none. Those
columns are anecdotes, not rates.

### Difference from the revision-1 report (labels only)

NER, typing, resolution and hygiene are unchanged: revision 2 touched no mention label (the added "Italian
government" identity is not a mention's canonical name).

| Metric | rev-1 gold | rev-2 gold | cause |
|---|---:|---:|---|
| Principal precision | 91% (20/22) | 78% (18/23) | D05 Houthis and Pakistan are no longer principals (2 hits become false positives); D10 Milei was a skipped duplicate alternative and is now a false positive (+1 unit) |
| Principal recall | 67% (20/30) | 69% (18/26) | D05 loses 4 gold principals (France, Turkey were misses; Pakistan, Houthis were hits) |
| Actor-role accuracy | 57% (67/117) | 56% (67/119) | two new representative units (D10 Milei, D13 Meloni), both predicted `actor`; D05 Houthis, D10 Falklands, D15 Putin were already correct under the alternatives; D24 Trump wrong under both |

Baseline under revision 2: principal precision 31% (was 35%), recall 65% (was 63%), roles unchanged at 15%.

## Remaining principal errors (13)

| Dev | Gold | Predicted | Error | Root cause | Runtime change? |
|---|---|---|---|---|---|
| D05 | Saudi Arabia (lead) | + houthis | opposing actor promoted | Principals are all holders whose dominant role is actor with enough support; there is no lead-principal selection. "Houthi attacks" makes the Houthis agent of an action noun in 7 headlines (actor weight 7.0) | yes: lead vs secondary model |
| D05 | Saudi Arabia (lead) | + pakistan | secondary actor promoted | Same; Pakistan actor weight 3.0 reaches the support threshold exactly (12 non-roundup items -> 3.0; stage 7's roundup exclusion lowered it from 3.25) | yes: same |
| D10 | Argentina | + javier milei | representative promoted | "Argentina's Milei threatens" makes Milei a headline subject; the runtime has no representative role, so a leader and the state it speaks for are both principals | yes: representative role |
| D22 | D.C. Circuit | + united states | state substituted for a court | "US court upholds": "court" is not an entity, so "US" climbs to the subject and the state takes the court's role | yes: generic-body phrases |
| D22 | D.C. Circuit | + us department of defense | agent of the object action promoted | "upholds Pentagon's blacklisting": the genitive agent of the object noun is marked actor (3 headlines) | yes |
| D22 | D.C. Circuit | missed | support | Only "DC Circuit panel upholds" names it (actor 1.0 < 1.5 for 3 items); the other headlines say "US (appeals) court" | yes: generic-body phrases |
| D03 | U.S. Navy | missed | support + title-case misparse | "Department of War and U.S. Navy Award Contract for F/A-XX Program": NER span "U.S. Navy Award Contract" swallows the verb, both bodies are headline fragments; Navy actor 1.0, DoD 0.5 < 1.5 | yes: title-case headline parse |
| D03 | US Department of Defense | missed | same | same | yes |
| D07 | United States | missed | misparse; **regression vs main** | "US, UK test SM-6 ...": "test" tagged NOUN, US/UK a fallback `nmod`; "sent to the bottom of the Atlantic in joint US-UK SINKEX": co-agents of a joint exercise read as location of `in`. No headline actor remains | yes: joint co-agents |
| D07 | United Kingdom | missed | same | same | yes |
| D16 | U.S. Customs and Border Protection | missed | implicit issuer | Federal Register notice headline "Accreditation and Approval of Intertek USA ..." has no agent; CBP appears only as "pursuant to CBP regulations" (subject) | yes: document-type rule |
| D25 | European Commission | missed | upstream NER miss | en_core_web_lg misses headline-initial bare "Commission"; the lead mention alone gives 0.5 < 1.0 | yes: institutional NER in headlines |
| D25 | Council of the European Union | missed | same | same for "Council strengthens ..." | yes |

## Remaining actor-role failures (52 of 119), by root cause

| Root cause | n | Units |
|---|---:|---|
| Upstream: entity missing from the role path (NER miss, span, name form, unresolved generic, media exclusion) | 12 | D01 Abascal (typed PRODUCT), D07 USS Klakring, D22 Anthropic, D19 UN (title case): NER miss; D11 NATO ("European Nato"), D23 White House (it: "Pranzo alla Casa Bianca"): span; D16 Chelsea ("Chelsea, MA"), D22 Emil Michael ("CTO Emil Michael"): name form; D07 Navy (US and UK both in context), D08 Ukrainian Air Force ("The Air Force"): generic unresolved; D09 NYT: media outlet excluded although not the publisher; D08 Kyiv: a capital as target folds into Ukraine |
| Participant / target / affected boundary | 8 | D04 Fat Bear Week, D09 McKinsey (possessor takes "in-laws face charges"), D12 Milrem, D12 Ukraine, D18 Iran, D18 Iraq, D19 Iran ("disrupt" is not coercive), D20 Myanmar |
| Place role (location vs affected / subject) | 7 | D01 Madrid, D05 Yemen, D05 Yanbu, D07 Atlantic, D15 Ukraine, D19 China, D19 Pakistan |
| Malformed dependency parse | 7 | D07 US, D07 UK (headline), D05 US, D18 Trump ("was set to" as passive), D25 Brussels (dateline), D16 CBP, D16 Intertek (nominal notice headline) |
| Institution vs institutional context | 6 | D03 US, D17 Palestinian Authority, D21 UN, D11 Milrem Robotics, D22 US ("US court"), D23 US (es: "presidente de Estados Unidos") |
| Quoted speaker / official treated as actor | 4 | D02 DoD ("Pentagon official says"), D11 Rutte, D12 Rutte, D12 NATO |
| Representative vs state | 3 | D10 Milei, D13 Meloni, D24 Trump (runtime has no representative role) |
| Actor vs participant (grammatical subject or genitive agent that does not own the Development's action) | 2 | D03 Boeing ("Boeing wins"), D22 DoD ("Pentagon's blacklisting") |
| Broad / mixed Development (item-level role differs from the Development's) | 2 | D05 Iran, D23 US Supreme Court |
| Roundup exclusion (owner rule; entity only in a roundup) | 1 | D14 Ramaphosa |

The owner's roundup rule also accounts for two stage-7 role changes that the revision-1 report counted as
fixes or neutral: D18 Trump's actor evidence came only from the roundup #1008 and D08 Kyiv's location only from
#161. No role error comes from roundup contamination: roundup items contribute nothing.

## Canonical resolution errors (11 of 378)

| Lang | Dev | Mention -> resolved | Cause |
|---|---|---|---|
| es | D23 x3, D24 | Donald Trump -> "Donald J. Trump" (fuzzy, provisional, not stored) | Same person. The multilingual entity table's canonical is "Donald J. Trump" and the gold's accepted names omit that form. Gold omission, not a resolver error: accepting it would make Spanish 11/12. **Not applied**: the owner review covered principals and roles only |
| it | D23 | Donald Trump -> "Donald J. Trump" | same (Italian would be 9/10) |
| es | D24 | "Gobierno de Irán" -> new entity | "Government of X" is mapped to X in the role path (`_GOVERNMENT_OF`) but not in the resolver |
| it | D23 | "Pranzo alla Casa Bianca" -> new entity | Italian NER span ("lunch at the White House") |
| en | D03 | "U.S. Navy Award Contract" -> itself | title-case NER span swallows the verb |
| en | D07 | "Navy" -> "navy" | generic label, ambiguous (US and UK in context) falls through to a legacy bare "navy" entity in the frozen table |
| en | D08 | "The Air Force" -> itself | generic label unresolved (context Russia, Ukraine) falls through to a legacy entity |
| en | D16 | "Chelsea, MA" -> itself | city with state suffix not reduced |

No learned-alias / lookalike substitution, state-vs-capital, nationality-to-state or person-to-state error
remains among the scored units. The alias-pollution probe (`runs/07-alias-pollution.json`) still has 10/72 (en)
and 12/56 (ml) suspect learned aliases resolving to their lookalike: those surfaces do not occur in the gold items.

## Decision

**One focused fix before merge: D07, co-agents of a joint action.**

- Defect: "joint US-UK SINKEX" names the co-agents of the Development's action, but when the action noun is
  unknown and heads a prepositional phrase ("in joint ..."), `clause_role` reads the states as its location.
  With the headline-1 misparse this leaves D07 with no headline actor, so neither state is a principal.
- Evidence: D07 is the only Development where the branch is worse than main on the corrected gold (main
  predicted US and UK principals and actor roles; the branch predicts none). Stage 5 introduced the role change,
  and stage 6 made principals depend on it. The owner names D07 as the US-UK Military Coordination example.
- Upside: principal recall +2 (D07 US, UK) and roles +2 (D07 US, UK actor) if the second headline resolves.
- Risk: "joint" also modifies bases, statements and ventures. The fix only upgrades a place or fallback role
  (never a target or affected role), so "strike on joint US-Iraqi base" keeps the US as target.

Not chosen (each needs a larger semantic change or rests on less evidence):
- a lead-principal model (D05);
- a representative role (D10, D13, D24);
- headline institutional NER (D25);
- a nominal-notice issuer rule (D16);
- a generic-body phrase rule (D22).
