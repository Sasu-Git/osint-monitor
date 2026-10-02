# Entity Resolution — Owner-Reviewed Evaluation Sheet

Received 2026-09-30 as `entity-resolution-evaluation-sheet-owner-reviewed.md`; source of gold revision 2
(`gold/manifest.yaml`). Copied verbatim below.

Purpose: freeze the human semantics for principal actors and actor roles before rescoring the existing predictions. Do not tune code from this document until the corrected gold is re-hashed and rescored.

## Core owner semantics

1. **Lead principal vs secondary actors.** A Development may have one lead principal plus secondary actors/participants. Participation does not automatically make every actor a co-principal.
2. **State-level principals can be correct.** For interstate military coordination, prefer the states when the meaningful Development/Situation is bilateral or multilateral coordination, even if service-level bodies execute the action.
3. **Official state remarks.** Prefer the state/government as principal; the named leader can be stored as representative/speaker.
4. **Government policy actions.** Prefer the government/state over a leader-only principal.
5. **Roundups.** Roundup items contribute no actor/principal evidence by themselves.
6. **Multilateral institutions.** Formal bodies such as the European Commission, Council of the EU, UN Security Council, NATO, G7/G20 forums, WTO, OECD, OPEC, etc. may be principals when they themselves own the action.

## 25-Development owner review

| ID | Ref | Development | Approved principal(s) | Approved role summary | Decision | Notes |
|---|---|---|---|---|---|---|
| D01 | `en#69` | Evicted Spanish pensioner can move back home, lawyer says | Spain | Spain=actor; Maricarmen Abascal=affected; Madrid=location | **ACCEPT** | — |
| D02 | `en#78` | Hegseth to cut number of US general and admiral positions by 20% | Pete Hegseth | Pete Hegseth=actor; DoD=institutional_context; US=subject; Virginia=location | **ACCEPT** | — |
| D03 | `ml#2` | Department of War and U.S. Navy Award Contract for F/A-XX Program | U.S. Navy; US Department of Defense | U.S. Navy=actor; DoD=actor; Boeing=participant; Northrop Grumman=subject; US=institutional_context | **ACCEPT** | — |
| D04 | `ml#20` | 'Backpack' declared Alaska's Fat Bear Week winner | None | Fat Bear Week=subject; Alaska/Alaska Peninsula=location | **ACCEPT** | — |
| D05 | `en#4` | Saudi Arabia allies line up support as Houthi attacks mount | Saudi Arabia | Saudi Arabia=lead actor; France/Pakistan/Turkey=secondary actors/allies; Houthis=opposing actor/target by framing | **OWNER REVISED** | One lead principal plus secondary actors; do not promote all allies to co-principal |
| D06 | `en#65` | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack | Israel | Israel=actor; Hamas + Izz al-Din al-Beik=targets; Gaza/Gaza City=locations | **ACCEPT** | — |
| D07 | `en#70` | US, UK test SM-6, other missiles on SINKEX target frigate | United States; United Kingdom | US=actor; UK=actor; service-level bodies=subordinate participants; USS Klakring=target; Atlantic=location | **OWNER REVISED** | State-level principals fit the Situation: US–UK Military Coordination |
| D08 | `ml#12` | Live: Several people killed as Russia launches new round of strikes on Kyiv | Russia | Russia=actor; Ukraine=target; Kyiv=location; Ukrainian Air Force=subject | **ACCEPT** | — |
| D09 | `en#55` | New York Times executive fatally shot by elderly in-laws, police say | None | Jonathan McKinsey=affected; NYT=institutional_context; California=location | **OWNER ACCEPTED** | Should generally not surface unless the story develops into a materially broader/global story |
| D10 | `en#59` | Argentina threatens legal action against UK over Falkland Islands oil exploration | Argentina | Argentina=actor; United Kingdom=target; Javier Milei=representative/speaker; Falklands=location/subject | **OWNER REVISED** | State is the principal; UK is target of the remarks |
| D11 | `en#64` | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine | Estonia | Estonia=actor; Russia=target; Milrem=affected; Ukraine/NATO/Rutte=subject | **ACCEPT** | — |
| D12 | `ml#25` | Estonia blames Russia in arson attack on military robotics firm Milrem | Estonia | Estonia=actor; Russia=target; Milrem=affected; Ukraine/NATO/Rutte=subject | **ACCEPT** | — |
| D13 | `en#7` | Italy ministers agree to ban burqa and niqab in school and cap foreigners in class | Italian government / Italy | Italian government=actor; Giorgia Meloni=representative/speaker where relevant; Rome=location | **OWNER REVISED** | Government-level identity preferred over leader-only principal for cabinet/government policy |
| D14 | `en#32` | Two mass shootings in South Africa leave 27 dead | None | South Africa=location; Cyril Ramaphosa=subject | **ACCEPT** | — |
| D15 | `ml#13` | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war | Russia / Vladimir Putin | Russia=actor; Putin=actor/representative; Ukraine=subject; Reuters=subject | **OWNER ACCEPTED** | Should contribute to the broader Russia–Ukraine War Situation |
| D16 | `ml#17` | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory | U.S. Customs and Border Protection | CBP=actor; Intertek=participant; Chelsea/Carteret=locations | **ACCEPT** | — |
| D17 | `en#35` | Israel revokes Dutch diplomats’ status over sanctions on settlements | Israel | Israel=actor; Netherlands=target; Palestinian Authority=institutional_context; West Bank/Ramallah=locations | **ACCEPT** | — |
| D18 | `en#45` | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says | United States / Donald Trump | US/Trump=actor; Iran/Iraq=affected; Najaf=location; UN=institutional_context | **OWNER ACCEPTED** | Future research trigger: senior leader singles out a specific place → investigate why there and, if possible, why now |
| D19 | `ml#4` | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet | United States | US=actor; Iran/Russia=targets; UN=institutional_context; China/Pakistan=subject; Hong Kong=location | **ACCEPT** | — |
| D20 | `en#56` | Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland | Malaysia | Malaysia=actor; Myanmar/Rohingya=affected | **ACCEPT** | — |
| D21 | `ml#15` | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update | Malaysia | Malaysia=actor; Myanmar=affected; UN=subject | **OWNER ACCEPTED** | Roundup items contribute zero actor/principal evidence; Malaysia survives from the coherent non-roundup item |
| D22 | `en#16` | US court upholds Pentagon’s blacklisting of Anthropic | U.S. Court of Appeals for the D.C. Circuit | D.C. Circuit=actor; DoD=participant; Anthropic=target; US=institutional_context; Trump/Hegseth/Emil Michael=subject | **OWNER ACCEPTED** | Court cases involving major companies should surface; expand court/legal source endpoints separately |
| D23 | `ml#8` | Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza' | Donald Trump / United States | Trump=actor; US=institutional_context; White House=location; US Supreme Court=subject | **ACCEPT** | — |
| D24 | `ml#16` | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz | Iran; United States | Iran=actor; United States=actor; Donald Trump=subject/representative | **ACCEPT** | — |
| D25 | `ml#23` | Commission proposes a new EU Critical Communication System for first responders | European Commission; Council of the European Union | European Commission=principal actor; Council of EU=co-principal when its adopted action is part of the Development; EU=institutional_context; Brussels=location | **OWNER REVISED** | Do not skip; formal multilateral bodies can be principals/co-principals |

## Benchmark label changes to apply

- **D05:** principal → `Saudi Arabia`; France/Pakistan/Turkey become secondary actors/allies rather than co-principals.
- **D07:** principals → `United States`, `United Kingdom`; retain military service bodies as subordinate participants where detected.
- **D10:** principal → `Argentina`; UK = target; Milei = representative/speaker.
- **D13:** principal → `Italian government / Italy`; Meloni = representative/speaker.
- **D21:** keep Malaysia principal; roundup item contributes zero actor/principal evidence.
- **D25:** keep in role/principal scoring; European Commission principal, Council of the EU may be co-principal.

## Product notes — NOT gold-label rules

- **D09 surfacing:** local/private-crime type stories should normally stay low prominence unless they develop into a materially broader/global story.
- **D15 Situation routing:** this Development should roll into the broader `Russia–Ukraine War` Situation.
- **D18 senior-leader/location research trigger:** when a head of state/government or equivalently senior actor explicitly targets or singles out a specific location, consider a mini-research task answering `Why there?` and, when evidence supports it, `Why now?`.
- **D22 legal-source expansion:** court developments involving major companies should be eligible to surface; add/expand court, appellate, regulatory and legal-proceeding endpoints in a separate source-expansion task.

## Rescore procedure

1. Update only the gold labels/roles above.
2. Add or retain `development_quality` / scoring flags only where needed for benchmark bookkeeping; do not use them as downstream runtime blacklists.
3. Re-hash the gold set.
4. Rescore the existing saved predictions **without changing implementation**.
5. Report new principal precision/recall and actor-role accuracy, including which Development-level errors remain.
6. Only then decide whether another code iteration is justified.
