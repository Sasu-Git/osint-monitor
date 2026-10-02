# Entity review sample — 2026-09-30

Real Developments from a read-only copy of the daemon database (2026-09-25 → 09-30, English feeds) and the
source-expansion evaluation collection (2026-09-30, Italian/Spanish feeds). Classification and principal actors were
recomputed on working copies with current `main` (ee93a3e); NER was re-run with the pipeline's spaCy model on each item's
headline + first 600 characters. Entity logic was not changed.

**Selection** (made before any flag was read, except as noted): per domain, a seeded order (`sha1(seed:db:id)`), first an
item from the multilingual collection when the domain has one, then the Developments adding the most unseen sources; a
4th is taken from auto-flagged Developments only if none of the first three is flagged. No embedding scores, Situation
decisions or ranking were used. The rules classifier assigns no Development to **humanitarian** or **institutional** in
this data: those are sampled from domain `unknown` by source (UN / EU / central-bank feeds) or headline words, and marked
*fallback*. Only 2 humanitarian candidates exist; economic has 3 in total.

**Columns.** *Method* replays the resolver read-only: `new entity` = no existing match, the mention created the
entity; `exact alias` / `normalised alias` / `seeded` = matched a recorded name; `fuzzy` = rapidfuzz ratio above the
threshold (80 same type, 85 cross type); `unresolved` = detected by NER now but not linked to the item. *Downstream*:
principal → ranking, Situation matching, UI actors; places (GPE/LOC/FAC) → clustering (segmentation's place check);
provenance never uses entities; when a Development has no principal, Situation matching and the UI fall back to all
mentioned actors. ⚑ marks automatic flags (heuristics, for your review — not conclusions).

Review codes: `Y` / `N` / `?` (unsure).

## Contents

1. [diplomacy] Evicted Spanish pensioner can move back home, lawyer says — `en#69`
2. [diplomacy] Hegseth to cut number of US general and admiral positions by 20% — `en#78`
3. [diplomacy] Department of War and U.S. Navy Award Contract for F/A-XX Program — `ml#2`
4. [diplomacy] 'Backpack' declared Alaska's Fat Bear Week winner — `ml#20`
5. [military] Saudi Arabia allies line up support as Houthi attacks mount — `en#4`
6. [military] Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack — `en#65`
7. [military] US, UK test SM-6, other missiles on SINKEX target frigate — `en#70`
8. [military] Live: Several people killed as Russia launches new round of strikes on Kyiv — `ml#12`
9. [security] New York Times executive fatally shot by elderly in-laws, police say — `en#55`
10. [security] Argentina threatens legal action against UK over Falkland Islands oil exploration — `en#59`
11. [security] Estonia blames Russia for arson attack on company supplying vehicles to Ukraine — `en#64`
12. [security] Estonia blames Russia in arson attack on military robotics firm Milrem — `ml#25`
13. [political] Italy ministers agree to ban burqa and niqab in school and cap foreigners in class — `en#7`
14. [political] Two mass shootings in South Africa leave 27 dead — `en#32`
15. [political] Ukraine war latest: Record Russian military budget for 2027 confirms no interest in endin… — `ml#13`
16. [political] Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger an… — `ml#17`
17. [economic] Israel revokes Dutch diplomats’ status over sanctions on settlements — `en#35`
18. [economic] US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says — `en#45`
19. [economic] United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictio… — `ml#4`
20. [humanitarian] Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland — `en#56`
21. [humanitarian] World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergenc… — `ml#15`
22. [institutional] US court upholds Pentagon’s blacklisting of Anthropic — `en#16`
23. [institutional] Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza' — `ml#8`
24. [institutional] Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acue… — `ml#16`
25. [institutional] Commission proposes a new EU Critical Communication System for first responders — `ml#23`

---

# Diplomacy

## 1. Evicted Spanish pensioner can move back home, lawyer says

- **Development:** `en#69` (db `entity-review-en`)
- **Domain / type:** diplomacy / significant_statement
- **Items:** 6; **sources:** Al Jazeera, BBC World, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 1012 | BBC World | en | 2026-09-29 01:28 | Evicted Spanish pensioner can move back home, lawyer says | The eviction of Maricarmen Abascal, 87, prompted large-scale protests across Spain. |
| 1124 | BBC World | en | 2026-09-29 12:14 | Spain announces new housing measures after protests over 87-year-old woman's eviction | The measures include a proposed ban on evictions until 2030 and the automatic renewal of tenant contracts. |
| 1316 | BBC World | en | 2026-09-29 16:23 | Spain announces ban on evictions after protests over 87-year-old woman's removal from flat | The ban is part of a number of proposals that must be approved in parliament within 30 days. |
| 1200 | South China Morning Post | en | 2026-09-29 17:54 | 87-year-old woman whose eviction sparked protests in Spain is returning home | Spain’s coalition government said it had agreed on proposals including banning evictions until 2030 to address the country’s housing crisis, as the 87-year-old woman whose forced removal last week tr… |
| 1213 | Al Jazeera | en | 2026-09-29 18:57 | Madrid residents feel the impact of Spain’s housing crisis | Spain’s housing crisis is deepening as soaring rents and a shortage of homes put affordable housing out of reach. |
| 1233 | Al Jazeera | en | 2026-09-29 21:02 | Spain protests: Evicted 87-year-old woman to return to Madrid home | The real estate firm backs down and restores her old rent after mass protests over Spain&#039;s housing crisis. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Spanish | NORP | yes | 1 | Evicted Spanish pensioner can move back home, lawyer says The eviction of Maricarmen Abascal, 87, prompted large-scale protests across Spain. |
| Maricarmen Abascal | PRODUCT | yes | 2 | Evicted Spanish pensioner can move back home, lawyer says The eviction of Maricarmen Abascal, 87, prompted large-scale protests across Spain. |
| 87 | DATE | no (label not stored) | 1 | Evicted Spanish pensioner can move back home, lawyer says The eviction of Maricarmen Abascal, 87, prompted large-scale protests across Spain. |
| Spain | GPE | yes | 8 | Evicted Spanish pensioner can move back home, lawyer says The eviction of Maricarmen Abascal, 87, prompted large-scale protests across Spain. |
| 87-year-old | DATE | no (label not stored) | 5 | Spain announces new housing measures after protests over 87-year-old woman's eviction The measures include a proposed ban on evictions until 2030 and… |
| 2030 | DATE | no (label not stored) | 2 | Spain announces new housing measures after protests over 87-year-old woman's eviction The measures include a proposed ban on evictions until 2030 and… |
| 30 days | DATE | no (label not stored) | 1 | Spain announces ban on evictions after protests over 87-year-old woman's removal from flat The ban is part of a number of proposals that must be appr… |
| last week | DATE | no (label not stored) | 1 | 87-year-old woman whose eviction sparked protests in Spain is returning home Spain’s coalition government said it had agreed on proposals including b… |
| Hundreds | CARDINAL | no (label not stored) | 1 | Hundreds of ‌people remained camped in one of Madrid’s main squares on Tuesday to protest Maricarmen Abascal’s removal from her home on a stretcher l… |
| one | CARDINAL | no (label not stored) | 1 | Hundreds of ‌people remained camped in one of Madrid’s main squares on Tuesday to protest Maricarmen Abascal’s removal from her home on a stretcher l… |
| Madrid | GPE | yes | 3 | Hundreds of ‌people remained camped in one of Madrid’s main squares on Tuesday to protest Maricarmen Abascal’s removal from her home on a stretcher l… |
| Tuesday | DATE | no (label not stored) | 1 | Hundreds of ‌people remained camped in one of Madrid’s main squares on Tuesday to protest Maricarmen Abascal’s removal from her home on a stretcher l… |
| last Wednesday | DATE | no (label not stored) | 1 | Hundreds of ‌people remained camped in one of Madrid’s main squares on Tuesday to protest Maricarmen Abascal’s removal from her home on a stretcher l… |
| Spain&#039;s | NORP | yes | 1 | Spain protests: Evicted 87-year-old woman to return to Madrid home The real estate firm backs down and restores her old rent after mass protests over… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Madrid | GPE | Madrid | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Spain | GPE | Spain | new entity | no existing match: the mention created this entity | 6 | | | | | | |
| Spain&#039;s | NORP | Spain&#039;s | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Spanish | NORP | Spanish | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Maricarmen Abascal | PRODUCT | Maricarmen Abascal | new entity | no existing match: the mention created this entity | 2 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | Spanish | yes | — | spain → spain |
| lead ×1 | Spain | no | topic / not a participant | spain → spain |
| title ×4 | Spain | yes | — | spain → spain |
| title ×1 | Spain | no | topic / not a participant | spain → spain |
| lead ×2 | Spain | yes | — | spain → spain |
| title ×2 | Madrid | no | place | madrid → madrid |
| lead ×1 | Spain&#039;s | no | topic / not a participant | spain&#039;s → spain&#039;s |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): spain 6.0
- **Final principal actors:** spain
- **Entities flagged principal on the Development:** Spain, Spanish

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Spain | spain | country | — | yes |
| Madrid | madrid | sub-national | spain | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Spain | GPE | yes | yes | yes | yes | — | yes |
| Spanish | NORP | yes | — | yes | yes | — | yes |
| Madrid | GPE | — | yes | — | — | — | — |
| Spain&#039;s | NORP | — | — | — | — | — | — |
| Maricarmen Abascal | PRODUCT | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: malformed span 'Spain&#039;s' (NORP)

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 2. Hegseth to cut number of US general and admiral positions by 20%

- **Development:** `en#78` (db `entity-review-en`)
- **Domain / type:** diplomacy / bilateral_meeting
- **Items:** 2; **sources:** Al Jazeera, War on the Rocks; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 1181 | War on the Rocks | en | 2026-09-29 16:00 | What Will Hegseth’s “State of the Force” Reprise Reveal? | Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military personnel for a &#8220;State of the Force&#8221; address this week |
| 1247 | Al Jazeera | en | 2026-09-30 05:05 | Hegseth to cut number of US general and admiral positions by 20% | Pentagon official says the plan will be announced in the defence secretary&#039;s &#039;State of the Force&#039; address in Virginia. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Will Hegseth | PERSON | yes | 1 | What Will Hegseth’s “State of the Force” Reprise Reveal? Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military … |
| State of the Force | WORK_OF_ART | no (label not stored) | 1 | What Will Hegseth’s “State of the Force” Reprise Reveal? Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military … |
| Defense | ORG | yes | 1 | What Will Hegseth’s “State of the Force” Reprise Reveal? Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military … |
| Pete Hegseth | PERSON | yes | 1 | What Will Hegseth’s “State of the Force” Reprise Reveal? Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military … |
| this week | DATE | no (label not stored) | 1 | What Will Hegseth’s “State of the Force” Reprise Reveal? Secretary of Defense Pete Hegseth is expected to convene a high-profile meeting of military … |
| U.S. | GPE | yes | 2 | Will it show the U.S. armed forces as healthy? |
| Hegseth | PERSON | yes | 2 | The answer may depend on how the audience responds, regardless of what Hegseth says. |
| Donald | PERSON | yes | 1 | How the audience handles what could be one of the higher-visibility made-for-media events of the defense secretary&#8217;s tenure could tell us a lot… |
| second | ORDINAL | no (label not stored) | 1 | How the audience handles what could be one of the higher-visibility made-for-media events of the defense secretary&#8217;s tenure could tell us a lot… |
| US | GPE | yes | 1 | Hegseth to cut number of US general and admiral positions by 20% Pentagon official says the plan will be announced in the defence secretary&#039;s &#… |
| 20% | PERCENT | no (label not stored) | 1 | Hegseth to cut number of US general and admiral positions by 20% Pentagon official says the plan will be announced in the defence secretary&#039;s &#… |
| Pentagon | ORG | yes | 1 | Hegseth to cut number of US general and admiral positions by 20% Pentagon official says the plan will be announced in the defence secretary&#039;s &#… |
| secretary&#039;s &#039;State | ORG | yes | 1 | Hegseth to cut number of US general and admiral positions by 20% Pentagon official says the plan will be announced in the defence secretary&#039;s &#… |
| Virginia | GPE | yes | 1 | Hegseth to cut number of US general and admiral positions by 20% Pentagon official says the plan will be announced in the defence secretary&#039;s &#… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| U.S. | GPE | America | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| US | GPE | America | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Virginia | GPE | Virginia | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Defense | ORG | Defense | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Pentagon | ORG | the Department of Defense | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Pentagon&#8217;s | ORG | Pentagon&#8217;s | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| secretary&#039;s &#039;State | ORG | secretary&#039;s &#039;State | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Donald | PERSON | Donald | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Hegseth | PERSON | Hegseth | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Pete Hegseth | PERSON | Pete Hegseth | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Will Hegseth | PERSON | Will Hegseth | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | Will Hegseth | no | topic / not a participant | will hegseth → will hegseth |
| lead ×1 | Defense | yes | — | defense → defense |
| lead ×1 | Pete Hegseth | yes | — | pete hegseth → united states |
| title ×1 | Hegseth | yes | — | hegseth → united states |
| title ×1 | US | yes | — | united states → united states |
| lead ×1 | Pentagon | yes | — | department of defense → united states |
| lead ×1 | secretary&#039;s &#039;State | no | topic / not a participant | secretary&#039;s &#039;state → secretary&#039;s &#039;state |
| lead ×1 | Virginia | no | place | virginia → virginia |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): united states 2.0, defense 1.0
- **Final principal actors:** defense, united states
- **Entities flagged principal on the Development:** America, Defense, Hegseth

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| U.S. | united states | country | — | yes |
| US | united states | country | — | yes |
| Virginia | virginia | sub-national | mid-atlantic, united states | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| America | GPE | yes | yes | yes | yes | — | yes |
| Defense | ORG | yes | — | yes | yes | — | yes |
| Hegseth | PERSON | yes | — | yes | yes | — | yes |
| Virginia | GPE | — | yes | — | — | — | — |
| Pentagon&#8217;s | ORG | — | — | — | — | — | — |
| secretary&#039;s &#039;State | ORG | — | — | — | — | — | — |
| the Department of Defense | ORG | — | — | — | — | — | — |
| Donald | PERSON | — | — | — | — | — | — |
| Pete Hegseth | PERSON | — | — | — | — | — | — |
| Will Hegseth | PERSON | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: malformed span 'Pentagon&#8217;s' (ORG)
- **NER detection**: malformed span 'secretary&#039;s &#039;State' (ORG)
- **person -> state/institution mapping** (principal): principal 'defense' is a generic institution name, not mapped to its state

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 3. Department of War and U.S. Navy Award Contract for F/A-XX Program

- **Development:** `ml#2` (db `entity-review-ml`)
- **Domain / type:** diplomacy / negotiation
- **Items:** 3; **sources:** Breaking Defense, Defense News, Defense.gov; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 507 | Breaking Defense | en | 2026-09-29 21:26 | Boeing wins Navy next-gen fighter F/A-XX competition | Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 selection to build the F-47. |
| 2 | Defense.gov | en | 2026-09-29 21:30 | Department of War and U.S. Navy Award Contract for F/A-XX Program | The War Department announced a contract awarded by the U.S |
| 487 | Defense News | en | 2026-09-29 22:20 | US Navy selects Boeing to build next-generation F/A-XX fighter | Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fighter, dubbed F/A-XX, icing out what was considered to be its biggest competitor in late-stage negotiations, North… |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Boeing | ORG | yes | 4 | Boeing wins Navy next-gen fighter F/A-XX competition Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 select… |
| Navy | ORG | yes | 2 | Boeing wins Navy next-gen fighter F/A-XX competition Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 select… |
| F/A-XX | PRODUCT | yes | 3 | Boeing wins Navy next-gen fighter F/A-XX competition Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 select… |
| American | NORP | yes | 1 | Boeing wins Navy next-gen fighter F/A-XX competition Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 select… |
| sixth | ORDINAL | no (label not stored) | 2 | Boeing wins Navy next-gen fighter F/A-XX competition Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 select… |
| 2025 | CARDINAL | no (label not stored) | 1 | Boeing wins Navy next-gen fighter F/A-XX competition Boeing&#8217;s win gives it a monopoly on American sixth-gen fighters, following its 2025 select… |
| Department of War | ORG | yes | 1 | Department of War and U.S. Navy Award Contract for F/A-XX Program The War Department announced a contract awarded by the U.S. Navy to Boeing for the … |
| U.S. Navy Award Contract | ORG | yes | 1 | Department of War and U.S. Navy Award Contract for F/A-XX Program The War Department announced a contract awarded by the U.S. Navy to Boeing for the … |
| The War Department | ORG | yes | 1 | Department of War and U.S. Navy Award Contract for F/A-XX Program The War Department announced a contract awarded by the U.S. Navy to Boeing for the … |
| the U.S. Navy | ORG | yes | 1 | Department of War and U.S. Navy Award Contract for F/A-XX Program The War Department announced a contract awarded by the U.S. Navy to Boeing for the … |
| Sixth | ORDINAL | no (label not stored) | 1 | Department of War and U.S. Navy Award Contract for F/A-XX Program The War Department announced a contract awarded by the U.S. Navy to Boeing for the … |
| US Navy | ORG | yes | 1 | US Navy selects Boeing to build next-generation F/A-XX fighter Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fig… |
| F | PRODUCT | yes | 1 | US Navy selects Boeing to build next-generation F/A-XX fighter Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fig… |
| Northrop Grumman | ORG | yes | 1 | US Navy selects Boeing to build next-generation F/A-XX fighter Boeing has been selected to build the Navy’s sixth-generation carrier-based strike fig… |
| $20 billion | MONEY | no (label not stored) | 1 | Inked at $20 billion for the full-scale development phase, the contract, according to a Pentagon release, “procures multiple test aircraft for ground… |
| Pentagon | ORG | yes | 1 | Inked at $20 billion for the full-scale development phase, the contract, according to a Pentagon release, “procures multiple test aircraft for ground… |
| Michael P. Duffey | PERSON | yes | 1 | ”“The F/A-XX is a critical pillar in our commitment to maintaining peace through strength,” Michael P. Duffey, under secretary of defense for Acquisi… |
| defense for Acquisition | ORG | yes | 1 | ”“The F/A-XX is a critical pillar in our commitment to maintaining peace through strength,” Michael P. Duffey, under secretary of defense for Acquisi… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| U.S. | GPE | U.S. | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| American | NORP | Mexican | exact alias | 'American' is a recorded name of 'Mexican' | 1 | | | | | | |
| 2028.The Air Force | ORG | 2028.The Air Force | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Boeing | ORG | Boeing | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Boeing Defense, Space & | ORG | Boeing Defense, Space & | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Collaborative Combat Aircraft | ORG | Collaborative Combat Aircraft | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Department of War | ORG | Department of War | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| F/A-18E/ | ORG | F/A-18E/ | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Lockheed Martin | ORG | Lockheed Martin | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| NGAD | ORG | NGAD | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Navy | ORG | Navy | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Northrop Grumman | ORG | Northrop Grumman | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Pentagon | ORG | Pentagon | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Security | ORG | Security | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| The War Department | ORG | The War Department | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| U.S. Navy Award Contract | ORG | U.S. Navy Award Contract | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| US Navy | ORG | the U.S. Navy | fuzzy | best alias 'the U.S. Navy' scored 88 (threshold 80) | 1 | | | | | | |
| defense for Acquisition | ORG | defense for Acquisition | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the U.S. Air Force’s | ORG | the U.S. Armed Forces | exact alias | 'the U.S. Air Force’s' is a recorded name of 'the U.S. Armed Forces' | 1 | | | | | | |
| the U.S. Navy | ORG | the U.S. Navy | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| F-47 | PERSON | F-47 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Hung Cao | PERSON | Hung Cao | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Michael P. Duffey | PERSON | Michael P. Duffey | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Steve Parker | PERSON | Steve Parker | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| EA-18G Growlers | PRODUCT | EA-18G Growlers | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| F | PRODUCT | F | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| F-22 Raptor | PRODUCT | F-22 Raptors | exact alias | 'F-22 Raptor' is a recorded name of 'F-22 Raptors' | 1 | | | | | | |
| F/A-XX | PRODUCT | F/A-XX | new entity | no existing match: the mention created this entity | 2 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Boeing | yes | — | boeing → boeing |
| title ×1 | Navy | yes | — | navy → navy |
| lead ×1 | American | no | topic / not a participant | united states → united states |
| title ×1 | Department of War | yes | — | department of war → department of war |
| title ×1 | U.S. Navy Award Contract | yes | — | u.s. navy award contract → u.s. navy award contract |
| lead ×1 | The War Department | yes | — | war department → war department |
| lead ×1 | U.S | yes | — | united states → united states |
| title ×1 | US Navy | yes | — | us navy → united states |
| lead ×1 | Boeing | yes | — | boeing → boeing |
| lead ×1 | Navy | yes | — | navy → navy |
| lead ×1 | Northrop Grumman | no | topic / not a participant | northrop grumman → northrop grumman |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): boeing 2.0, navy 1.5, united states 1.5, department of war 1.0, u.s. navy award contract 1.0, war department 0.5
- **Final principal actors:** boeing, navy, united states
- **Entities flagged principal on the Development:** Boeing, Navy, U.S.

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| U.S. | united states | country | — | yes |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| U.S. | GPE | yes | yes | yes | yes | — | yes |
| Boeing | ORG | yes | — | yes | yes | — | yes |
| Navy | ORG | yes | — | yes | yes | — | yes |
| Mexican | NORP | — | — | — | — | — | — |
| 2028.The Air Force | ORG | — | — | — | — | — | — |
| Boeing Defense, Space & | ORG | — | — | — | — | — | — |
| Collaborative Combat Aircraft | ORG | — | — | — | — | — | — |
| Department of War | ORG | — | — | — | — | — | — |
| F/A-18E/ | ORG | — | — | — | — | — | — |
| Lockheed Martin | ORG | — | — | — | — | — | — |
| NGAD | ORG | — | — | — | — | — | — |
| Northrop Grumman | ORG | — | — | — | — | — | — |
| Pentagon | ORG | — | — | — | — | — | — |
| Security | ORG | — | — | — | — | — | — |
| The War Department | ORG | — | — | — | — | — | — |
| U.S. Navy Award Contract | ORG | — | — | — | — | — | — |
| defense for Acquisition | ORG | — | — | — | — | — | — |
| the U.S. Armed Forces | ORG | — | — | — | — | — | — |
| the U.S. Navy | ORG | — | — | — | — | — | — |
| F-47 | PERSON | — | — | — | — | — | — |
| Hung Cao | PERSON | — | — | — | — | — | — |
| Michael P. Duffey | PERSON | — | — | — | — | — | — |
| Steve Parker | PERSON | — | — | — | — | — | — |
| EA-18G Growlers | PRODUCT | — | — | — | — | — | — |
| F | PRODUCT | — | — | — | — | — | — |
| F-22 Raptors | PRODUCT | — | — | — | — | — | — |
| F/A-XX | PRODUCT | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: article/possessive kept in span: 'The War Department'
- **NER detection**: article/possessive kept in span: 'the U.S. Navy'
- **alias resolution**: fuzzy: 'US Navy' -> 'the U.S. Navy' (best alias 'the U.S. Navy' scored 88 (threshold 80))
- **NER detection**: article/possessive kept in span: 'the U.S. Air Force’s'
- **NER detection**: malformed span 'defense for Acquisition' (ORG)
- **person -> state/institution mapping** (principal): principal 'navy' is a generic institution name, not mapped to its state

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 4. 'Backpack' declared Alaska's Fat Bear Week winner

- **Development:** `ml#20` (db `entity-review-ml`)
- **Domain / type:** diplomacy / significant_statement
- **Items:** 2; **sources:** Al Jazeera, BBC World; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 92 | BBC World | en | 2026-09-30 05:01 | 'Backpack' declared Alaska's Fat Bear Week winner | "Backpack" defeated a bear known only as "910" in the final round of the annual competition. |
| 199 | Al Jazeera | en | 2026-09-30 06:57 | Gentle giant Backpack wins Alaska’s Fat Bear Week | The contest celebrates the resilience of the 2,200 brown bears that live in the preserve on the Alaska Peninsula. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Alaska | GPE | yes | 2 | 'Backpack' declared Alaska's Fat Bear Week winner "Backpack" defeated a bear known only as "910" in the final round of the annual competition. |
| Fat Bear Week | ORG | yes | 2 | 'Backpack' declared Alaska's Fat Bear Week winner "Backpack" defeated a bear known only as "910" in the final round of the annual competition. |
| Backpack | WORK_OF_ART | no (label not stored) | 1 | 'Backpack' declared Alaska's Fat Bear Week winner "Backpack" defeated a bear known only as "910" in the final round of the annual competition. |
| annual | DATE | no (label not stored) | 1 | 'Backpack' declared Alaska's Fat Bear Week winner "Backpack" defeated a bear known only as "910" in the final round of the annual competition. |
| 2,200 | CARDINAL | no (label not stored) | 1 | Gentle giant Backpack wins Alaska’s Fat Bear Week The contest celebrates the resilience of the 2,200 brown bears that live in the preserve on the Ala… |
| the Alaska Peninsula | LOC | yes | 1 | Gentle giant Backpack wins Alaska’s Fat Bear Week The contest celebrates the resilience of the 2,200 brown bears that live in the preserve on the Ala… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Alaska | GPE | Alaska | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| the Alaska Peninsula | LOC | the Alaska Peninsula | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Fat Bear Week | ORG | Fat Bear Week | new entity | no existing match: the mention created this entity | 2 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Alaska | no | place | alaska → alaska |
| title ×2 | Fat Bear Week | yes | — | fat bear week → fat bear week |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): fat bear week 2.0
- **Final principal actors:** fat bear week
- **Entities flagged principal on the Development:** Fat Bear Week

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Alaska | alaska | sub-national | united states | no |
| the Alaska Peninsula | alaska peninsula | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Fat Bear Week | ORG | yes | — | yes | yes | — | yes |
| Alaska | GPE | — | yes | — | — | — | — |
| the Alaska Peninsula | LOC | — | yes | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: article/possessive kept in span: 'the Alaska Peninsula'
- **principal-selection failure** (principal): no state among the principals (fat bear week); check they are actors

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

---

# Military

## 5. Saudi Arabia allies line up support as Houthi attacks mount

- **Development:** `en#4` (db `entity-review-en`)
- **Domain / type:** military / military_action
- **Items:** 13; **sources:** Al Jazeera, BBC World, Defense News, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 72 | Al Jazeera | en | 2026-09-25 03:35 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting | Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Houthi attacks and Yemen fighting intensify. |
| 110 | South China Morning Post | en | 2026-09-25 06:03 | France to protect key Saudi oil terminal as Houthis step up missile attacks | President Emmanuel Macron said France would send troops to defend an oil plant in Saudi Arabia as the Iran-backed Houthi militia took responsibility for new attacks on the kingdom. |
| 57 | Al Jazeera | en | 2026-09-25 08:32 | Saudi Arabia allies line up support as Houthi attacks mount | France is sending military to protect key Yanbu oil terminal; Pakistan and Turkiye to hold military talks with Riyadh. |
| 325 | Defense News | en | 2026-09-25 11:24 | France to send military to protect Saudi Arabia on Red Sea oil route, Macron says | PARIS, Sept 24 (Reuters) — France will send troops and defense systems to Saudi Arabia to help protect the Red Sea port city of Yanbu, which is key for energy transport, French President Emmanuel Mac… |
| 433 | Al Jazeera | en | 2026-09-25 19:38 | Pakistan PM calls Houthi threats to Saudi holy sites a ‘red line’ | Pakistan PM, a signatory to the Mecca Joint Defence Agreement, condemned Houthi attacks on Saudi Arabia at UNGA 81. |
| 441 | Al Jazeera | en | 2026-09-25 20:59 | Houthi attack on Mecca, Medina would cross ‘red line’, Pakistan PM tells UN | Shehbaz Sharif speaks as Islamabad, Riyadh and Ankara army chiefs meet to discuss Mecca pact, closer military ties. |
| 547 | South China Morning Post | en | 2026-09-26 10:00 | Houthi attacks on Saudi Arabia test limits of Mecca regional security pact | Just a month after Saudi Arabia signed a regional mutual defence deal with Pakistan and Turkey, attacks by Yemen’s Houthis against the kingdom’s energy infrastructure and military sites are testing t… |
| 575 | Al Jazeera | en | 2026-09-26 12:48 | Mecca defence alliance chiefs meet amid Houthi attacks | Defence chiefs from Saudi Arabia, Turkiye and Pakistan have been meeting in Riyadh to discuss support for Saudi Arabia. |
| 603 | Al Jazeera | en | 2026-09-26 19:43 | Saudi FM accuses Iran of ‘flagrant attacks’ and condemns Houthis at UNGA | At the UN, Saudi Arabia accused Iran of attacks across the region and called for action against the Houthis. |
| 660 | Al Jazeera | en | 2026-09-27 09:59 | Yemen government forces widen attacks against Houthis: What we know | Yemeni government forces claim multiple air and ground operations across Taiz in 24 hours. |
| 721 | BBC World | en | 2026-09-27 21:16 | Inside Yemen's front-line city as Houthis battle for control | In rare access to Yemen's conflict zone the BBC travels to the front line with pro-government soldiers. |
| 999 | Al Jazeera | en | 2026-09-29 04:46 | Rubio, Saudi Arabia’s foreign minister hold talks on Yemen, Hormuz Strait | Top US and Saudi diplomats discuss cooperation on security challenges, including hostilities with Yemen&#039;s Houthis. |
| 1150 | Al Jazeera | en | 2026-09-29 13:20 | Iran downplays possible role in Houthis’ recent Yemen victories | Iran has long been accused of links with the Houthis in Yemen, but how far do these links go? |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Saudi | NORP | yes | 6 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| Turkish | NORP | yes | 1 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| Pakistani | NORP | yes | 1 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| Yemen | GPE | yes | 9 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| Saudi Arabia | GPE | yes | 12 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| Turkiye | GPE | yes | 3 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| Pakistan | GPE | yes | 6 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| Houthi | ORG | yes | 8 | Saudi, Turkish, Pakistani chiefs plan urgent talks amid Yemen fighting Saudi Arabia, Turkiye and Pakistan move to deepen defence coordination as Hout… |
| France | GPE | yes | 6 | France to protect key Saudi oil terminal as Houthis step up missile attacks President Emmanuel Macron said France would send troops to defend an oil … |
| Houthis | ORG | yes | 9 | France to protect key Saudi oil terminal as Houthis step up missile attacks President Emmanuel Macron said France would send troops to defend an oil … |
| Emmanuel Macron | PERSON | yes | 2 | France to protect key Saudi oil terminal as Houthis step up missile attacks President Emmanuel Macron said France would send troops to defend an oil … |
| Iran | GPE | yes | 5 | France to protect key Saudi oil terminal as Houthis step up missile attacks President Emmanuel Macron said France would send troops to defend an oil … |
| Houthi militia | ORG | yes | 1 | France to protect key Saudi oil terminal as Houthis step up missile attacks President Emmanuel Macron said France would send troops to defend an oil … |
| Macron | ORG | yes | 3 | Macron said in a television interview Thursday with TF1 and France 2 that he would send soldiers and military support to help protect the Saudi port … |
| Thursday | DATE | no (label not stored) | 3 | Macron said in a television interview Thursday with TF1 and France 2 that he would send soldiers and military support to help protect the Saudi port … |
| TF1 | GPE | yes | 1 | Macron said in a television interview Thursday with TF1 and France 2 that he would send soldiers and military support to help protect the Saudi port … |
| Yanbu | GPE | yes | 4 | Macron said in a television interview Thursday with TF1 and France 2 that he would send soldiers and military support to help protect the Saudi port … |
| Red Sea | LOC | yes | 3 | Saudi Arabia came under attack from the Houthi militia on Thursday, with the kingdom saying it intercepted missiles fired towards the Red Sea port of… |
| Riyadh | GPE | yes | 4 | Saudi Arabia allies line up support as Houthi attacks mount France is sending military to protect key Yanbu oil terminal; Pakistan and Turkiye to hol… |
| PARIS | GPE | yes | 1 | France to send military to protect Saudi Arabia on Red Sea oil route, Macron says PARIS, Sept 24 (Reuters) — France will send troops and defense syst… |
| Sept 24 | DATE | no (label not stored) | 1 | France to send military to protect Saudi Arabia on Red Sea oil route, Macron says PARIS, Sept 24 (Reuters) — France will send troops and defense syst… |
| Reuters | ORG | yes | 1 | France to send military to protect Saudi Arabia on Red Sea oil route, Macron says PARIS, Sept 24 (Reuters) — France will send troops and defense syst… |
| French | NORP | yes | 2 | France to send military to protect Saudi Arabia on Red Sea oil route, Macron says PARIS, Sept 24 (Reuters) — France will send troops and defense syst… |
| U.S. | GPE | yes | 2 | Macron also said a U.S. ban on diesel exports, which the White House has denied is under consideration, would be “catastrophic,” both globally and fo… |
| the White House | ORG | yes | 1 | Macron also said a U.S. ban on diesel exports, which the White House has denied is under consideration, would be “catastrophic,” both globally and fo… |
| Macron | PERSON | yes | 1 | Macron was speaking in a wide-ranging primetime television interview on the international situation, in which he also warned about possible Russian a… |
| Russian | NORP | yes | 1 | Macron was speaking in a wide-ranging primetime television interview on the international situation, in which he also warned about possible Russian a… |
| Pakistan PM | TIME | no (label not stored) | 1 | Pakistan PM calls Houthi threats to Saudi holy sites a ‘red line’ Pakistan PM, a signatory to the Mecca Joint Defence Agreement, condemned Houthi att… |
| the Mecca Joint Defence Agreement | ORG | yes | 2 | Pakistan PM calls Houthi threats to Saudi holy sites a ‘red line’ Pakistan PM, a signatory to the Mecca Joint Defence Agreement, condemned Houthi att… |
| UNGA | ORG | yes | 2 | Pakistan PM calls Houthi threats to Saudi holy sites a ‘red line’ Pakistan PM, a signatory to the Mecca Joint Defence Agreement, condemned Houthi att… |
| 81 | CARDINAL | no (label not stored) | 1 | Pakistan PM calls Houthi threats to Saudi holy sites a ‘red line’ Pakistan PM, a signatory to the Mecca Joint Defence Agreement, condemned Houthi att… |
| Mecca | GPE | yes | 4 | Houthi attack on Mecca, Medina would cross ‘red line’, Pakistan PM tells UN Shehbaz Sharif speaks as Islamabad, Riyadh and Ankara army chiefs meet to… |
| Medina | GPE | yes | 1 | Houthi attack on Mecca, Medina would cross ‘red line’, Pakistan PM tells UN Shehbaz Sharif speaks as Islamabad, Riyadh and Ankara army chiefs meet to… |
| UN | ORG | yes | 2 | Houthi attack on Mecca, Medina would cross ‘red line’, Pakistan PM tells UN Shehbaz Sharif speaks as Islamabad, Riyadh and Ankara army chiefs meet to… |
| Shehbaz Sharif | PERSON | yes | 1 | Houthi attack on Mecca, Medina would cross ‘red line’, Pakistan PM tells UN Shehbaz Sharif speaks as Islamabad, Riyadh and Ankara army chiefs meet to… |
| Islamabad | GPE | yes | 1 | Houthi attack on Mecca, Medina would cross ‘red line’, Pakistan PM tells UN Shehbaz Sharif speaks as Islamabad, Riyadh and Ankara army chiefs meet to… |
| Ankara | GPE | yes | 1 | Houthi attack on Mecca, Medina would cross ‘red line’, Pakistan PM tells UN Shehbaz Sharif speaks as Islamabad, Riyadh and Ankara army chiefs meet to… |
| Just a month | DATE | no (label not stored) | 1 | Houthi attacks on Saudi Arabia test limits of Mecca regional security pact Just a month after Saudi Arabia signed a regional mutual defence deal with… |
| Turkey | GPE | yes | 1 | Houthi attacks on Saudi Arabia test limits of Mecca regional security pact Just a month after Saudi Arabia signed a regional mutual defence deal with… |
| Friday | DATE | no (label not stored) | 1 | At a hastily convened meeting of the Mecca Joint Defence Agreement in Riyadh on Friday, military chiefs of the three parties reaffirmed their commitm… |
| three | CARDINAL | no (label not stored) | 1 | At a hastily convened meeting of the Mecca Joint Defence Agreement in Riyadh on Friday, military chiefs of the three parties reaffirmed their commitm… |
| the Saudi Press Agency | ORG | yes | 1 | At a hastily convened meeting of the Mecca Joint Defence Agreement in Riyadh on Friday, military chiefs of the three parties reaffirmed their commitm… |
| Yemeni | NORP | yes | 1 | Yemen government forces widen attacks against Houthis: What we know Yemeni government forces claim multiple air and ground operations across Taiz in … |
| Taiz | ORG | yes | 1 | Yemen government forces widen attacks against Houthis: What we know Yemeni government forces claim multiple air and ground operations across Taiz in … |
| 24 hours | TIME | no (label not stored) | 1 | Yemen government forces widen attacks against Houthis: What we know Yemeni government forces claim multiple air and ground operations across Taiz in … |
| BBC | ORG | yes | 1 | Inside Yemen's front-line city as Houthis battle for control In rare access to Yemen's conflict zone the BBC travels to the front line with pro-gover… |
| Rubio | PERSON | yes | 1 | Rubio, Saudi Arabia’s foreign minister hold talks on Yemen, Hormuz Strait Top US and Saudi diplomats discuss cooperation on security challenges, incl… |
| Saudi Arabia’s | GPE | yes | 1 | Rubio, Saudi Arabia’s foreign minister hold talks on Yemen, Hormuz Strait Top US and Saudi diplomats discuss cooperation on security challenges, incl… |
| Hormuz Strait | LOC | yes | 1 | Rubio, Saudi Arabia’s foreign minister hold talks on Yemen, Hormuz Strait Top US and Saudi diplomats discuss cooperation on security challenges, incl… |
| US | GPE | yes | 1 | Rubio, Saudi Arabia’s foreign minister hold talks on Yemen, Hormuz Strait Top US and Saudi diplomats discuss cooperation on security challenges, incl… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Leipzig | FAC | Leipzig | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Ankara | GPE | Ankara | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Azerbaijan | GPE | Azerbaijan | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Elysee | GPE | Elysee | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| France | GPE | France | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Germany | GPE | Germany | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Iran | GPE | Iran | new entity | no existing match: the mention created this entity | 4 | | | | | | |
| Islamabad | GPE | Islamabad | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Mecca | GPE | Mecca | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Medina | GPE | Medina | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| PARIS | GPE | Paris | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Riyadh | GPE | Riyadh | new entity | no existing match: the mention created this entity | 4 | | | | | | |
| Saudi Arabia | GPE | Saudi Arabia | new entity | no existing match: the mention created this entity | 8 | | | | | | |
| Saudi Arabia’s | GPE | Saudi Arabia | exact alias | 'Saudi Arabia’s' is a recorded name of 'Saudi Arabia' | 1 | | | | | | |
| TF1 | GPE | TF1 | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Turkey | GPE | Turkey | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Turkiye | GPE | Turkiye | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| U.S. | GPE | America | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| US | GPE | America | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Ukraine | GPE | Ukraine | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Yanbu | GPE | Yanbu | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Yemen | GPE | Yemen | new entity | no existing match: the mention created this entity | 7 | | | | | | |
| Yemeni | GPE | Yemen | exact alias | 'Yemeni' is a recorded name of 'Yemen' | 1 | | | | | | |
| Europe | LOC | Europe | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| European | LOC | Europe | exact alias | 'European' is a recorded name of 'Europe' | 1 | | | | | | |
| Mediterranean | LOC | Mediterranean | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Red Sea | LOC | Red Sea | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| French | NORP | French | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Pakistan | NORP | Pakistani | exact alias | 'Pakistan' is a recorded name of 'Pakistani' | 6 | | | | | | |
| Pakistani | NORP | Pakistani | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Russia | NORP | Russian | exact alias | 'Russia' is a recorded name of 'Russian' | 1 | | | | | | |
| Russian | NORP | Russian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Russian-Uzbek | NORP | Russian-Uzbek | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Saudi | NORP | Saudi | new entity | no existing match: the mention created this entity | 6 | | | | | | |
| Spanish | NORP | Spanish | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Turkish | NORP | Turkish | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| anti-Russian | NORP | anti-Russian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| BBC | ORG | BBC | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| CIA | ORG | CIA | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Defence | ORG | Defense | exact alias | 'Defence' is a recorded name of 'Defense' | 1 | | | | | | |
| EU | ORG | EU | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| El Mundo | ORG | El Mundo | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Houthi | ORG | Houthis | fuzzy | best alias 'Houthis' scored 92 (threshold 80) | 6 | | | | | | |
| Houthi militia | ORG | Houthi militia | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Houthis | ORG | Houthis | seeded (entities.yaml) | 'Houthis' is a recorded name of 'Houthis' | 7 | | | | | | |
| Macron | ORG | Macron | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Reuters | ORG | Reuters | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Taiz | ORG | Taiz | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| UN | ORG | UN | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| UNGA | ORG | UNGA | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| the Mecca Joint Defence Agreement | ORG | the Mecca Joint Defence Agreement | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| the Saudi Press Agency | ORG | the Saudi Press Agency | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the U.S. Central Intelligence Agency | ORG | the U.S. Central Intelligence Agency | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the White House | ORG | White House | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Alisher Usmanov | PERSON | Alisher Usmanov | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Emmanuel Macron | PERSON | Emmanuel Macron | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Rubio | PERSON | Rubio | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Shehbaz Sharif | PERSON | Shehbaz Sharif | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Hormuz Strait | LOC | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| Houthi | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| Houthis | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×4 | Saudi | yes | — | saudi arabia → saudi arabia |
| title ×1 | Turkish | yes | — | turkey → turkey |
| title ×1 | Pakistani | yes | — | pakistan → pakistan |
| title ×3 | Yemen | no | topic / not a participant | yemen → yemen |
| lead ×4 | Saudi Arabia | yes | — | saudi arabia → saudi arabia |
| lead ×1 | Turkiye | yes | — | turkey → turkey |
| lead ×3 | Pakistan | yes | — | pakistan → pakistan |
| lead ×2 | Houthi | yes | — | houthi → houthi |
| lead ×3 | Yemen | no | topic / not a participant | yemen → yemen |
| title ×2 | France | yes | — | france → france |
| title ×3 | Houthis | yes | — | houthis → houthis |
| lead ×2 | Emmanuel Macron | yes | — | emmanuel macron → emmanuel macron |
| lead ×3 | France | yes | — | france → france |
| lead ×4 | Saudi Arabia | no | topic / not a participant | saudi arabia → saudi arabia |
| lead ×1 | Iran | no | topic / not a participant | iran → iran |
| lead ×1 | Houthi militia | yes | — | houthi militia → houthi militia |
| title ×3 | Saudi Arabia | yes | — | saudi arabia → saudi arabia |
| title ×3 | Houthi | no | topic / not a participant | houthi → houthi |
| lead ×2 | Yanbu | yes | — | yanbu → yanbu |
| lead ×2 | Pakistan | no | topic / not a participant | pakistan → pakistan |
| lead ×2 | Turkiye | no | topic / not a participant | turkey → turkey |
| lead ×3 | Riyadh | no | place | riyadh → riyadh |
| title ×1 | Macron | yes | — | macron → macron |
| lead ×1 | PARIS | no | place | paris → paris |
| lead ×1 | Reuters | no | topic / not a participant | reuters → reuters |
| lead ×1 | French | yes | — | france → france |
| lead ×1 | Macron | yes | — | macron → macron |
| lead ×1 | U.S | yes | — | united states → united states |
| title ×2 | Pakistan | yes | — | pakistan → pakistan |
| title ×2 | Houthi | yes | — | houthi → houthi |
| lead ×1 | the Mecca Joint Defence Agreement | no | topic / not a participant | mecca joint defence agreement → mecca joint defence agreement |
| lead ×1 | UNGA | no | topic / not a participant | unga → unga |
| title ×3 | Mecca | no | place | mecca → mecca |
| title ×1 | Medina | yes | — | medina → medina |
| title ×1 | UN | yes | — | un → un |
| lead ×1 | Shehbaz Sharif | yes | — | shehbaz sharif → shehbaz sharif |
| lead ×1 | Islamabad | no | topic / not a participant | pakistan → pakistan |
| lead ×1 | Ankara | no | place | ankara → ankara |
| lead ×1 | Mecca | no | place | mecca → mecca |
| lead ×1 | Turkey | yes | — | turkey → turkey |
| lead ×1 | Yemen | yes | — | yemen → yemen |
| lead ×4 | Houthis | yes | — | houthis → houthis |
| title ×2 | Iran | yes | — | iran → iran |
| title ×1 | UNGA | no | topic / not a participant | unga → unga |
| lead ×1 | UN | no | topic / not a participant | un → un |
| lead ×2 | Iran | yes | — | iran → iran |
| title ×2 | Yemen | yes | — | yemen → yemen |
| lead ×1 | Yemeni | yes | — | yemen → yemen |
| lead ×1 | Taiz | no | topic / not a participant | taiz → taiz |
| title ×2 | Houthis | no | topic / not a participant | houthis → houthis |
| lead ×1 | BBC | yes | — | bbc → bbc |
| title ×1 | Rubio | yes | — | rubio → united states |
| title ×1 | Saudi Arabia’s | yes | — | saudi arabia → saudi arabia |
| lead ×1 | US | yes | — | united states → united states |
| lead ×1 | Saudi | yes | — | saudi arabia → saudi arabia |

- **Support per actor** (headline 1.0, lead 0.5; needed 3.25): saudi arabia 8.0, houthis 4.5, pakistan 3.5, houthi 2.5, france 2.5, yemen 2.5, iran 2.0, turkey 1.5, united states 1.5, emmanuel macron 1.0, yanbu 1.0, macron 1.0, un 1.0, medina 1.0, bbc 1.0, houthi militia 0.5, shehbaz sharif 0.5
- **Final principal actors:** houthis, pakistan, saudi arabia
- **Entities flagged principal on the Development:** Houthis, Islamabad, Pakistani, Saudi, Saudi Arabia

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Saudi Arabia | saudi arabia | country | — | yes |
| Turkiye | turkiye | country | — | yes |
| Yemen | yemen | country | — | yes |
| Iran | iran | country | — | yes |
| France | france | country | — | yes |
| Yanbu | yanbu | not in gazetteer | — | yes |
| TF1 | tf1 | not in gazetteer | — | no |
| Red Sea | red sea | not in gazetteer | — | no |
| Riyadh | riyadh | sub-national | saudi arabia | no |
| PARIS | paris | sub-national | france | no |
| Ukraine | ukraine | country | — | no |
| Germany | germany | country | — | no |
| U.S. | united states | country | — | yes |
| Europe | europe | not in gazetteer | — | no |
| European | european | not in gazetteer | — | no |
| Mediterranean | mediterranean | not in gazetteer | — | no |
| Leipzig | leipzig | not in gazetteer | — | no |
| Elysee | elysee | not in gazetteer | — | no |
| Azerbaijan | azerbaijan | country | — | no |
| Ankara | ankara | sub-national | turkiye | no |
| Mecca | mecca | sub-national | saudi arabia | no |
| Medina | medina | sub-national | saudi arabia | yes |
| Islamabad | islamabad | sub-national | pakistan | yes |
| Turkey | turkiye | country | — | yes |
| Yemeni | yemeni | not in gazetteer | — | yes |
| US | united states | country | — | yes |
| Saudi Arabia’s | saudi arabia | country | — | yes |
| Hormuz Strait | hormuz strait | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Islamabad | GPE | yes | yes | yes | yes | — | yes |
| Saudi Arabia | GPE | yes | yes | yes | yes | — | yes |
| Pakistani | NORP | yes | — | yes | yes | — | yes |
| Saudi | NORP | yes | — | yes | yes | — | yes |
| Houthis | ORG | yes | — | yes | yes | — | yes |
| Leipzig | FAC | — | yes | — | — | — | — |
| America | GPE | — | yes | — | — | — | — |
| Ankara | GPE | — | yes | — | — | — | — |
| Azerbaijan | GPE | — | yes | — | — | — | — |
| Elysee | GPE | — | yes | — | — | — | — |
| France | GPE | — | yes | — | — | — | — |
| Germany | GPE | — | yes | — | — | — | — |
| Iran | GPE | — | yes | — | — | — | — |
| Mecca | GPE | — | yes | — | — | — | — |
| Medina | GPE | — | yes | — | — | — | — |
| Paris | GPE | — | yes | — | — | — | — |
| Riyadh | GPE | — | yes | — | — | — | — |
| TF1 | GPE | — | yes | — | — | — | — |
| Turkey | GPE | — | yes | — | — | — | — |
| Turkiye | GPE | — | yes | — | — | — | — |
| Ukraine | GPE | — | yes | — | — | — | — |
| Yanbu | GPE | — | yes | — | — | — | — |
| Yemen | GPE | — | yes | — | — | — | — |
| Europe | LOC | — | yes | — | — | — | — |
| Mediterranean | LOC | — | yes | — | — | — | — |
| Red Sea | LOC | — | yes | — | — | — | — |
| French | NORP | — | — | — | — | — | — |
| Russian | NORP | — | — | — | — | — | — |
| Russian-Uzbek | NORP | — | — | — | — | — | — |
| Spanish | NORP | — | — | — | — | — | — |
| Turkish | NORP | — | — | — | — | — | — |
| anti-Russian | NORP | — | — | — | — | — | — |
| BBC | ORG | — | — | — | — | — | — |
| CIA | ORG | — | — | — | — | — | — |
| Defense | ORG | — | — | — | — | — | — |
| EU | ORG | — | — | — | — | — | — |
| El Mundo | ORG | — | — | — | — | — | — |
| Houthi militia | ORG | — | — | — | — | — | — |
| Macron | ORG | — | — | — | — | — | — |
| Reuters | ORG | — | — | — | — | — | — |
| Taiz | ORG | — | — | — | — | — | — |
| UN | ORG | — | — | — | — | — | — |
| UNGA | ORG | — | — | — | — | — | — |
| White House | ORG | — | — | — | — | — | — |
| the Mecca Joint Defence Agreement | ORG | — | — | — | — | — | — |
| the Saudi Press Agency | ORG | — | — | — | — | — | — |
| the U.S. Central Intelligence Agency | ORG | — | — | — | — | — | — |
| Alisher Usmanov | PERSON | — | — | — | — | — | — |
| Emmanuel Macron | PERSON | — | — | — | — | — | — |
| Rubio | PERSON | — | — | — | — | — | — |
| Shehbaz Sharif | PERSON | — | — | — | — | — | — |

### ⚑ Automatic flags

- **alias resolution**: fuzzy: 'Houthi' -> 'Houthis' (best alias 'Houthis' scored 92 (threshold 80))
- **NER detection**: article/possessive kept in span: 'the White House'
- **NER detection**: article/possessive kept in span: 'the U.S. Central Intelligence Agency'
- **NER detection**: article/possessive kept in span: 'the Mecca Joint Defence Agreement'
- **NER detection**: article/possessive kept in span: 'the Saudi Press Agency'
- **NER detection**: article/possessive kept in span: 'Saudi Arabia’s'

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 6. Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack

- **Development:** `en#65` (db `entity-review-en`)
- **Domain / type:** military / military_action
- **Items:** 2; **sources:** Al Jazeera, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 1061 | Al Jazeera | en | 2026-09-29 07:34 | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack | Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike on an apartment building in Gaza City. |
| 1171 | South China Morning Post | en | 2026-09-29 14:40 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack | An Israeli air strike killed the head of Hamas’ armed wing in north Gaza on Tuesday, officials on both sides said, with the militant group describing him as a leader of the October 7, 2023 attack tha… |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Israeli | NORP | yes | 4 | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike o… |
| Hamas | ORG | yes | 4 | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike o… |
| Izz al-Din al-Beik | PERSON | yes | 1 | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike o… |
| Gaza | GPE | yes | 3 | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike o… |
| Hamas&#039;s | NORP | yes | 1 | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike o… |
| Gaza City | GPE | yes | 1 | Israeli forces kill Hamas commander Izz al-Din al-Beik in Gaza attack Head of Hamas&#039;s armed wing in northern Gaza killed in ⁠an Israeli strike o… |
| Israel | GPE | yes | 2 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack An Israeli air strike killed the head of Hamas’ armed wing in north Gaza… |
| October 7 | DATE | no (label not stored) | 1 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack An Israeli air strike killed the head of Hamas’ armed wing in north Gaza… |
| 2023 | CARDINAL | no (label not stored) | 2 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack An Israeli air strike killed the head of Hamas’ armed wing in north Gaza… |
| north Gaza | GPE | yes | 1 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack An Israeli air strike killed the head of Hamas’ armed wing in north Gaza… |
| Tuesday | DATE | no (label not stored) | 1 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack An Israeli air strike killed the head of Hamas’ armed wing in north Gaza… |
| the October 7 | EVENT | yes | 1 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack An Israeli air strike killed the head of Hamas’ armed wing in north Gaza… |
| Palestinian | NORP | yes | 1 | Israel’s Gaza air strike kills Hamas commander behind October 7, 2023 attack An Israeli air strike killed the head of Hamas’ armed wing in north Gaza… |
| Izz al-Din Al-Beik | PERSON | yes | 1 | Israel’s government said its military had targeted and killed Izz al-Din Al-Beik, ‌who they said was involved in planning attacks and recruiting. |
| Medics | ORG | yes | 1 | Medics said the Israeli strike hit a building in Gaza City’s Nasr neighbourhood... |
| Gaza City’s | GPE | yes | 1 | Medics said the Israeli strike hit a building in Gaza City’s Nasr neighbourhood... |
| Nasr | PERSON | yes | 1 | Medics said the Israeli strike hit a building in Gaza City’s Nasr neighbourhood... |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| the October 7 | EVENT | the October 7 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Gaza | GPE | Gaza | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Gaza City | GPE | Gaza City | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Gaza City’s | GPE | Gaza City | exact alias | 'Gaza City’s' is a recorded name of 'Gaza City' | 1 | | | | | | |
| north Gaza | GPE | north Gaza | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Hamas&#039;s | NORP | Hamas&#039;s | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Israel | NORP | Israeli | exact alias | 'Israel' is a recorded name of 'Israeli' | 1 | | | | | | |
| Israeli | NORP | Israeli | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Palestinian | NORP | Palestinians | exact alias | 'Palestinian' is a recorded name of 'Palestinians' | 1 | | | | | | |
| Hamas | ORG | Hamas | seeded (entities.yaml) | 'Hamas' is a recorded name of 'Hamas' | 2 | | | | | | |
| Medics | ORG | Medics | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Izz al-Din Al-Beik | PERSON | Izz al-Din al-Beik | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Izz al-Din al-Beik | PERSON | Izz al-Din al-Beik | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Nasr | PERSON | Nasr | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | Israeli | yes | — | israel → israel |
| title ×2 | Hamas | yes | — | hamas → hamas |
| title ×1 | Izz al-Din al-Beik | yes | — | izz al-din al-beik → izz al-din al-beik |
| title ×1 | Gaza | no | topic / not a participant | gaza → gaza |
| lead ×1 | Hamas&#039;s | no | common_noun | hamas&#039;s → hamas&#039;s |
| lead ×1 | Gaza | no | topic / not a participant | gaza → gaza |
| lead ×1 | Israeli | no | topic / not a participant | israel → israel |
| lead ×1 | Gaza City | no | place | gaza city → gaza city |
| title ×1 | Israel | yes | — | israel → israel |
| title ×1 | Gaza | yes | — | gaza → gaza |
| lead ×1 | Israeli | yes | — | israel → israel |
| lead ×1 | Hamas | yes | — | hamas → hamas |
| lead ×1 | north Gaza | no | place | north gaza → north gaza |
| lead ×1 | Palestinian | no | topic / not a participant | palestine → palestine |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): hamas 2.0, israel 2.0, izz al-din al-beik 1.0, gaza 1.0
- **Final principal actors:** gaza, hamas, israel, izz al-din al-beik
- **Entities flagged principal on the Development:** Gaza, Hamas, Israeli, Izz al-Din al-Beik

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Gaza | gaza | sub-national | palestine | yes |
| Gaza City | gaza city | sub-national | gaza, palestine | no |
| Gaza City’s | gaza city | sub-national | gaza, palestine | no |
| north Gaza | gaza | sub-national | palestine | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Gaza | GPE | yes | yes | yes | yes | — | yes |
| Israeli | NORP | yes | — | yes | yes | — | yes |
| Hamas | ORG | yes | — | yes | yes | — | yes |
| Izz al-Din al-Beik | PERSON | yes | — | yes | yes | — | yes |
| the October 7 | EVENT | — | — | — | — | — | — |
| Gaza City | GPE | — | yes | — | — | — | — |
| north Gaza | GPE | — | yes | — | — | — | — |
| Hamas&#039;s | NORP | — | — | — | — | — | — |
| Palestinians | NORP | — | — | — | — | — | — |
| Medics | ORG | — | — | — | — | — | — |
| Nasr | PERSON | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: malformed span 'Hamas&#039;s' (NORP)
- **NER detection**: article/possessive kept in span: 'Gaza City’s'
- **NER detection**: article/possessive kept in span: 'the October 7'
- **location/actor confusion** (principal): principal 'gaza' comes from place mentions (GPE)
- **person -> state/institution mapping** (principal): principal person 'izz al-din al-beik' has no state/body mapping (fine for private persons)

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 7. US, UK test SM-6, other missiles on SINKEX target frigate

- **Development:** `en#70` (db `entity-review-en`)
- **Domain / type:** military / military_exercise
- **Items:** 2; **sources:** Breaking Defense, Defense News; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 984 | Breaking Defense | en | 2026-09-28 22:00 | US, UK test SM-6, other missiles on SINKEX target frigate | The joint exercise saw the test of several muntions but the final blow was delivered by an Mk 48 Advanced Capability Torpedo, a Navy official said. |
| 1203 | Defense News | en | 2026-09-29 16:11 | USS Klakring sent to the bottom of the Atlantic in joint US-UK SINKEX | A decommissioned U.S |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| US | GPE | yes | 2 | US, UK test SM-6, other missiles on SINKEX target frigate The joint exercise saw the test of several muntions but the final blow was delivered by an … |
| UK | GPE | yes | 2 | US, UK test SM-6, other missiles on SINKEX target frigate The joint exercise saw the test of several muntions but the final blow was delivered by an … |
| SM-6 | PERSON | yes | 1 | US, UK test SM-6, other missiles on SINKEX target frigate The joint exercise saw the test of several muntions but the final blow was delivered by an … |
| SINKEX | LAW | no (label not stored) | 2 | US, UK test SM-6, other missiles on SINKEX target frigate The joint exercise saw the test of several muntions but the final blow was delivered by an … |
| 48 | CARDINAL | no (label not stored) | 1 | US, UK test SM-6, other missiles on SINKEX target frigate The joint exercise saw the test of several muntions but the final blow was delivered by an … |
| Navy | ORG | yes | 2 | US, UK test SM-6, other missiles on SINKEX target frigate The joint exercise saw the test of several muntions but the final blow was delivered by an … |
| Atlantic | LOC | yes | 1 | USS Klakring sent to the bottom of the Atlantic in joint US-UK SINKEX A decommissioned U.S. guided-missile frigate was sent below the seas on Sept. 2… |
| U.S. | GPE | yes | 1 | USS Klakring sent to the bottom of the Atlantic in joint US-UK SINKEX A decommissioned U.S. guided-missile frigate was sent below the seas on Sept. 2… |
| Sept. 25 | DATE | no (label not stored) | 1 | USS Klakring sent to the bottom of the Atlantic in joint US-UK SINKEX A decommissioned U.S. guided-missile frigate was sent below the seas on Sept. 2… |
| the U.S. Navy | ORG | yes | 1 | USS Klakring sent to the bottom of the Atlantic in joint US-UK SINKEX A decommissioned U.S. guided-missile frigate was sent below the seas on Sept. 2… |
| U.S. Task Force 65 | ORG | yes | 1 | The recent SINKEX blended the firepower of U.S. Task Force 65, Task Force 67, Task Force 68, Task Force 69 and Task Force 1060 alongside the Royal Na… |
| Task Force 67 | PRODUCT | yes | 1 | The recent SINKEX blended the firepower of U.S. Task Force 65, Task Force 67, Task Force 68, Task Force 69 and Task Force 1060 alongside the Royal Na… |
| Task Force 68 | PRODUCT | yes | 1 | The recent SINKEX blended the firepower of U.S. Task Force 65, Task Force 67, Task Force 68, Task Force 69 and Task Force 1060 alongside the Royal Na… |
| Task Force 69 | PRODUCT | yes | 1 | The recent SINKEX blended the firepower of U.S. Task Force 65, Task Force 67, Task Force 68, Task Force 69 and Task Force 1060 alongside the Royal Na… |
| Task Force 1060 | PRODUCT | yes | 1 | The recent SINKEX blended the firepower of U.S. Task Force 65, Task Force 67, Task Force 68, Task Force 69 and Task Force 1060 alongside the Royal Na… |
| the Royal Navy | ORG | yes | 1 | The recent SINKEX blended the firepower of U.S. Task Force 65, Task Force 67, Task Force 68, Task Force 69 and Task Force 1060 alongside the Royal Na… |
| the U.S. Air Force | ORG | yes | 1 | The recent SINKEX blended the firepower of U.S. Task Force 65, Task Force 67, Task Force 68, Task Force 69 and Task Force 1060 alongside the Royal Na… |
| The USS Klakring | PRODUCT | yes | 1 | The USS Klakring, an Oliver Hazard Perry-class frigate — laid up in Philadelphia, Pennsylvania, since its decommissioning on March 22, 2013 — served … |
| Oliver Hazard Perry | PERSON | yes | 1 | The USS Klakring, an Oliver Hazard Perry-class frigate — laid up in Philadelphia, Pennsylvania, since its decommissioning on March 22, 2013 — served … |
| Philadelphia | GPE | yes | 1 | The USS Klakring, an Oliver Hazard Perry-class frigate — laid up in Philadelphia, Pennsylvania, since its decommissioning on March 22, 2013 — served … |
| Pennsylvania | GPE | yes | 1 | The USS Klakring, an Oliver Hazard Perry-class frigate — laid up in Philadelphia, Pennsylvania, since its decommissioning on March 22, 2013 — served … |
| March 22, 2013 | DATE | no (label not stored) | 1 | The USS Klakring, an Oliver Hazard Perry-class frigate — laid up in Philadelphia, Pennsylvania, since its decommissioning on March 22, 2013 — served … |
| Rear Adm. | ORG | yes | 1 | Named for Rear Adm. Thomas B. Klakring, who was awarded three Navy Crosses as the commander |
| Thomas B. Klakring | PERSON | yes | 1 | Named for Rear Adm. Thomas B. Klakring, who was awarded three Navy Crosses as the commander |
| three | CARDINAL | no (label not stored) | 1 | Named for Rear Adm. Thomas B. Klakring, who was awarded three Navy Crosses as the commander |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| World War II | EVENT | World War II | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the Iran-Iraq War | EVENT | the Iran-Iraq War | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the Standard Missile 6 | FAC | the Standard Missile 6 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Kuwaiti | GPE | Kuwait | exact alias | 'Kuwaiti' is a recorded name of 'Kuwait' | 1 | | | | | | |
| Pennsylvania | GPE | Pennsylvania | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Philadelphia | GPE | Philadelphia | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| U.K. | GPE | U.K. | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| UK | GPE | UK | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| US | GPE | America | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| United Kingdom | GPE | UK | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Atlantic | LOC | Atlantic | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the North Atlantic | LOC | the North Atlantic | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| British | NORP | British | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Iranian | NORP | Iranian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Atlantic Thunder | ORG | Atlantic Thunder | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Excalibur | ORG | Excalibur | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Navy | ORG | navy | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Rear Adm. | ORG | Rear Adm. | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| U.S. Task Force 65 | ORG | U.S. Task Force 65 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| USS Massachusetts | ORG | USS Massachusetts | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| UUV | ORG | UUV | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the Royal Navy | ORG | Royal Navy | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the U.S. 6th Fleet | ORG | U.S. 5th Fleet’s | fuzzy | best alias 'the U.S. Fifth Fleet' scored 87 (threshold 80) | 1 | | | | | | |
| the U.S. Air Force | ORG | the U.S. Armed Forces | normalised alias | normalised 'u.s. air force' matches 'the U.S. Armed Forces' | 1 | | | | | | |
| the U.S. Navy | ORG | U.S. Navy | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Kelechi Ndukwe | PERSON | Kelechi Ndukwe | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Mk | PERSON | Mk | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Oliver Hazard Perry | PERSON | Oliver Hazard Perry | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| SM-6 | PERSON | SM-6 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Thomas B. Klakring | PERSON | Thomas B. Klakring | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Block IV | PRODUCT | Block IV | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Operation Earnest | PRODUCT | Operation Earnest | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Task Force 67 | PRODUCT | Task Force 59 | exact alias | 'Task Force 67' is a recorded name of 'Task Force 59' | 1 | | | | | | |
| The USS Klakring | PRODUCT | The USS Klakring | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| USS Guardfish | PRODUCT | USS Guardfish | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| USS Paul Ignatius | PRODUCT | USS Paul Ignatius | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Task Force 1060 | PRODUCT | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| Task Force 68 | PRODUCT | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| Task Force 69 | PRODUCT | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | US | yes | — | united states → united states |
| title ×1 | UK | yes | — | united kingdom → united kingdom |
| title ×1 | SM-6 | no | common_noun | sm-6 → sm-6 |
| lead ×1 | Navy | yes | — | navy → navy |
| title ×1 | US | no | topic / not a participant | united states → united states |
| title ×1 | UK | no | topic / not a participant | united kingdom → united kingdom |
| lead ×1 | U.S | yes | — | united states → united states |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): united states 2.0, united kingdom 1.0, navy 0.5
- **Final principal actors:** united kingdom, united states
- **Entities flagged principal on the Development:** America, British, UK

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| UK | united kingdom | country | — | yes |
| US | united states | country | — | yes |
| United Kingdom | united kingdom | country | — | yes |
| Kuwaiti | kuwaiti | not in gazetteer | — | no |
| U.K. | u.k | not in gazetteer | — | no |
| Atlantic | atlantic | not in gazetteer | — | no |
| the North Atlantic | north atlantic | not in gazetteer | — | no |
| Philadelphia | philadelphia | sub-national | mid-atlantic, pennsylvania, united states, us northeast | no |
| Pennsylvania | pennsylvania | sub-national | mid-atlantic, united states, us northeast | no |
| the Standard Missile 6 | standard missile 6 | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| America | GPE | yes | yes | yes | yes | — | yes |
| UK | GPE | yes | yes | yes | yes | — | yes |
| British | NORP | yes | — | yes | yes | — | yes |
| World War II | EVENT | — | — | — | — | — | — |
| the Iran-Iraq War | EVENT | — | — | — | — | — | — |
| the Standard Missile 6 | FAC | — | yes | — | — | — | — |
| Kuwait | GPE | — | yes | — | — | — | — |
| Pennsylvania | GPE | — | yes | — | — | — | — |
| Philadelphia | GPE | — | yes | — | — | — | — |
| U.K. | GPE | — | yes | — | — | — | — |
| Atlantic | LOC | — | yes | — | — | — | — |
| the North Atlantic | LOC | — | yes | — | — | — | — |
| Iranian | NORP | — | — | — | — | — | — |
| Atlantic Thunder | ORG | — | — | — | — | — | — |
| Excalibur | ORG | — | — | — | — | — | — |
| Rear Adm. | ORG | — | — | — | — | — | — |
| Royal Navy | ORG | — | — | — | — | — | — |
| U.S. 5th Fleet’s | ORG | — | — | — | — | — | — |
| U.S. Navy | ORG | — | — | — | — | — | — |
| U.S. Task Force 65 | ORG | — | — | — | — | — | — |
| USS Massachusetts | ORG | — | — | — | — | — | — |
| UUV | ORG | — | — | — | — | — | — |
| navy | ORG | — | — | — | — | — | — |
| the U.S. Armed Forces | ORG | — | — | — | — | — | — |
| Kelechi Ndukwe | PERSON | — | — | — | — | — | — |
| Mk | PERSON | — | — | — | — | — | — |
| Oliver Hazard Perry | PERSON | — | — | — | — | — | — |
| SM-6 | PERSON | — | — | — | — | — | — |
| Thomas B. Klakring | PERSON | — | — | — | — | — | — |
| Block IV | PRODUCT | — | — | — | — | — | — |
| Operation Earnest | PRODUCT | — | — | — | — | — | — |
| Task Force 59 | PRODUCT | — | — | — | — | — | — |
| The USS Klakring | PRODUCT | — | — | — | — | — | — |
| USS Guardfish | PRODUCT | — | — | — | — | — | — |
| USS Paul Ignatius | PRODUCT | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: article/possessive kept in span: 'the U.S. Navy'
- **NER detection**: article/possessive kept in span: 'the U.S. Air Force'
- **NER detection**: article/possessive kept in span: 'the Royal Navy'
- **NER detection**: article/possessive kept in span: 'the U.S. 6th Fleet'
- **alias resolution**: fuzzy: 'the U.S. 6th Fleet' -> 'U.S. 5th Fleet’s' (best alias 'the U.S. Fifth Fleet' scored 87 (threshold 80))
- **NER detection**: article/possessive kept in span: 'the North Atlantic'
- **NER detection**: article/possessive kept in span: 'The USS Klakring'
- **NER detection**: article/possessive kept in span: 'the Iran-Iraq War'
- **NER detection**: article/possessive kept in span: 'the Standard Missile 6'

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 8. Live: Several people killed as Russia launches new round of strikes on Kyiv

- **Development:** `ml#12` (db `entity-review-ml`)
- **Domain / type:** military / military_action
- **Items:** 3; **sources:** France 24, Kyiv Independent; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 274 | Kyiv Independent | en | 2026-09-30 00:28 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital | The latest strikes came as Russia intensifies its attacks on Kyiv since August, relentlessly launching drone attacks, even in daytime, to exhaust the Ukrainian air defense. |
| 161 | France 24 | en | 2026-09-30 05:35 | Live: Several people killed as Russia launches new round of strikes on Kyiv | At least four people, including a 14-year old child, have died after Russia launched another round of strikes on Kyiv and its surrounding regions overnight to Wednesday, officials said |
| 275 | Kyiv Independent | en | 2026-09-30 08:14 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack | The Air Force said Russia attacked Ukraine overnight with Zircon and Onyx anti-ship missiles, Iskander-M and S-400 ballistic missiles, and 188 attack drones of various types. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Russia | GPE | yes | 5 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| Kyiv | GPE | yes | 5 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| 3 | CARDINAL | no (label not stored) | 1 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| 5 | CARDINAL | no (label not stored) | 1 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| Ukraine | GPE | yes | 4 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| August | DATE | no (label not stored) | 1 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| daytime | TIME | no (label not stored) | 1 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| Ukrainian | NORP | yes | 1 | Russia strikes Kyiv energy infrastructure, kills 3, injures 5 in overnight attack on Ukraine's capital The latest strikes came as Russia intensifies … |
| At least four | CARDINAL | no (label not stored) | 1 | Several people killed as Russia launches new round of strikes on Kyiv At least four people, including a 14-year old child, have died after Russia lau… |
| 14-year old | DATE | no (label not stored) | 1 | Several people killed as Russia launches new round of strikes on Kyiv At least four people, including a 14-year old child, have died after Russia lau… |
| Wednesday | DATE | no (label not stored) | 1 | Several people killed as Russia launches new round of strikes on Kyiv At least four people, including a 14-year old child, have died after Russia lau… |
| Poland | GPE | yes | 1 | In Poland, two airports, in Lublin and Rzeszow, were briefly shut over “military aviation activity” during Russian attacks on Ukraine. |
| two | CARDINAL | no (label not stored) | 1 | In Poland, two airports, in Lublin and Rzeszow, were briefly shut over “military aviation activity” during Russian attacks on Ukraine. |
| Lublin | ORG | yes | 1 | In Poland, two airports, in Lublin and Rzeszow, were briefly shut over “military aviation activity” during Russian attacks on Ukraine. |
| Rzeszow | ORG | yes | 1 | In Poland, two airports, in Lublin and Rzeszow, were briefly shut over “military aviation activity” during Russian attacks on Ukraine. |
| Russian | NORP | yes | 2 | In Poland, two airports, in Lublin and Rzeszow, were briefly shut over “military aviation activity” during Russian attacks on Ukraine. |
| at least 6 | CARDINAL | no (label not stored) | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |
| 34 | CARDINAL | no (label not stored) | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |
| The Air Force | ORG | yes | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |
| Zircon | ORG | yes | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |
| Onyx | ORG | yes | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |
| Iskander-M | ORG | yes | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |
| S-400 | WEAPON_SYSTEM | no (label not stored) | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |
| 188 | CARDINAL | no (label not stored) | 1 | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack The Air Force said Russia attacked Uk… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Kyiv | GPE | Ukraine | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Poland | GPE | Poland | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Russia | GPE | Russia | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Russian | GPE | Russia | exact alias | 'Russian' is a recorded name of 'Russia' | 2 | | | | | | |
| Ukraine | GPE | Ukraine | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Ukrainian | NORP | Ukrainian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Iskander-M | ORG | Iskander-M | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Lublin | ORG | Lublin | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Onyx | ORG | Onyx | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Rzeszow | ORG | Rzeszow | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| The Air Force | ORG | The Air Force | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Zircon | ORG | Zircon | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Russia | yes | — | russia → russia |
| title ×2 | Kyiv | yes | — | ukraine → ukraine |
| title ×1 | Ukraine | yes | — | ukraine → ukraine |
| lead ×3 | Russia | yes | — | russia → russia |
| lead ×1 | Kyiv | yes | — | ukraine → ukraine |
| lead ×1 | Ukrainian | yes | — | ukraine → ukraine |
| title ×1 | Kyiv | no | topic / not a participant | ukraine → ukraine |
| lead ×1 | Kyiv | no | topic / not a participant | ukraine → ukraine |
| title ×1 | Russian | yes | — | russia → russia |
| title ×1 | Ukraine | no | topic / not a participant | ukraine → ukraine |
| lead ×1 | The Air Force | yes | — | air force → air force |
| lead ×1 | Ukraine | yes | — | ukraine → ukraine |
| lead ×1 | Zircon | yes | — | zircon → zircon |
| lead ×1 | Onyx | yes | — | onyx → onyx |
| lead ×1 | Iskander-M | yes | — | iskander-m → iskander-m |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): russia 3.0, ukraine 2.0, onyx 0.5, zircon 0.5, air force 0.5, iskander-m 0.5
- **Final principal actors:** russia, ukraine
- **Entities flagged principal on the Development:** Russia, Ukraine, Ukrainian

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Russia | russia | country | — | yes |
| Kyiv | kyiv | sub-national | ukraine | yes |
| Russian | russian | not in gazetteer | — | yes |
| Poland | poland | country | — | no |
| Ukraine | ukraine | country | — | yes |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Russia | GPE | yes | yes | yes | yes | — | yes |
| Ukraine | GPE | yes | yes | yes | yes | — | yes |
| Ukrainian | NORP | yes | — | yes | yes | — | yes |
| Poland | GPE | — | yes | — | — | — | — |
| Iskander-M | ORG | — | — | — | — | — | — |
| Lublin | ORG | — | — | — | — | — | — |
| Onyx | ORG | — | — | — | — | — | — |
| Rzeszow | ORG | — | — | — | — | — | — |
| The Air Force | ORG | — | — | — | — | — | — |
| Zircon | ORG | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: article/possessive kept in span: 'The Air Force'

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

---

# Security

## 9. New York Times executive fatally shot by elderly in-laws, police say

- **Development:** `en#55` (db `entity-review-en`)
- **Domain / type:** security / security_incident
- **Items:** 2; **sources:** BBC World, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 1031 | South China Morning Post | en | 2026-09-29 03:14 | Elderly in-laws arrested in California shooting death of New York Times employee | A couple in their late 70s gunned down their son-in-law in a California city park over the weekend, authorities said, and court documents showed the victim had been in a bitter custody dispute with t… |
| 1014 | BBC World | en | 2026-09-29 04:06 | New York Times executive fatally shot by elderly in-laws, police say | Jonathan McKinsey's in-laws, who are both 77 years old, face multiple charges including first-degree murder. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| California | GPE | yes | 2 | Elderly in-laws arrested in California shooting death of New York Times employee A couple in their late 70s gunned down their son-in-law in a Califor… |
| New York Times | ORG | yes | 2 | Elderly in-laws arrested in California shooting death of New York Times employee A couple in their late 70s gunned down their son-in-law in a Califor… |
| late 70s | DATE | no (label not stored) | 1 | Elderly in-laws arrested in California shooting death of New York Times employee A couple in their late 70s gunned down their son-in-law in a Califor… |
| the weekend | DATE | no (label not stored) | 1 | Elderly in-laws arrested in California shooting death of New York Times employee A couple in their late 70s gunned down their son-in-law in a Califor… |
| Jonathan McKinsey | PERSON | yes | 1 | Jonathan McKinsey, a 40-year-old gaming engineer for The New York Times, was shot to death Saturday afternoon in the car park of a sports complex in … |
| 40-year-old | DATE | no (label not stored) | 1 | Jonathan McKinsey, a 40-year-old gaming engineer for The New York Times, was shot to death Saturday afternoon in the car park of a sports complex in … |
| The New York Times | ORG | yes | 1 | Jonathan McKinsey, a 40-year-old gaming engineer for The New York Times, was shot to death Saturday afternoon in the car park of a sports complex in … |
| Saturday | DATE | no (label not stored) | 1 | Jonathan McKinsey, a 40-year-old gaming engineer for The New York Times, was shot to death Saturday afternoon in the car park of a sports complex in … |
| afternoon | TIME | no (label not stored) | 1 | Jonathan McKinsey, a 40-year-old gaming engineer for The New York Times, was shot to death Saturday afternoon in the car park of a sports complex in … |
| Dublin | GPE | yes | 1 | Jonathan McKinsey, a 40-year-old gaming engineer for The New York Times, was shot to death Saturday afternoon in the car park of a sports complex in … |
| San Francisco | GPE | yes | 1 | Jonathan McKinsey, a 40-year-old gaming engineer for The New York Times, was shot to death Saturday afternoon in the car park of a sports complex in … |
| 911 | CARDINAL | no (label not stored) | 1 | A police sergeant was driving nearby and saw him on the ground as witnesses began calling 911 and pointing... |
| Jonathan McKinsey's | PERSON | yes | 1 | New York Times executive fatally shot by elderly in-laws, police say Jonathan McKinsey's in-laws, who are both 77 years old, face multiple charges in… |
| 77 years old | DATE | no (label not stored) | 1 | New York Times executive fatally shot by elderly in-laws, police say Jonathan McKinsey's in-laws, who are both 77 years old, face multiple charges in… |
| first | ORDINAL | no (label not stored) | 1 | New York Times executive fatally shot by elderly in-laws, police say Jonathan McKinsey's in-laws, who are both 77 years old, face multiple charges in… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| California | GPE | California | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Dublin | GPE | Dublin | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| San Francisco | GPE | San Francisco | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| New York Times | ORG | New York Times | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Jonathan McKinsey | PERSON | Jonathan McKinsey's | exact alias | 'Jonathan McKinsey' is a recorded name of 'Jonathan McKinsey's' | 1 | | | | | | |
| Jonathan McKinsey's | PERSON | Jonathan McKinsey's | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | California | no | place | california → california |
| title ×2 | New York Times | no | affiliation | new york times → new york times |
| lead ×1 | California | no | place | california → california |
| lead ×1 | Jonathan McKinsey's | yes | — | jonathan mckinsey → jonathan mckinsey |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): jonathan mckinsey 1.0
- **Final principal actors:** jonathan mckinsey
- **Entities flagged principal on the Development:** Jonathan McKinsey's

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Dublin | dublin | sub-national | ireland | no |
| San Francisco | san francisco | sub-national | california, united states | no |
| California | california | sub-national | united states | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Jonathan McKinsey's | PERSON | yes | — | yes | yes | — | yes |
| California | GPE | — | yes | — | — | — | — |
| Dublin | GPE | — | yes | — | — | — | — |
| San Francisco | GPE | — | yes | — | — | — | — |
| New York Times | ORG | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: malformed span 'Jonathan McKinsey' (PERSON)
- **NER detection**: article/possessive kept in span: 'Jonathan McKinsey's'
- **person -> state/institution mapping** (principal): principal person 'jonathan mckinsey' has no state/body mapping (fine for private persons)
- **principal-selection failure** (principal): no state among the principals (jonathan mckinsey); check they are actors

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 10. Argentina threatens legal action against UK over Falkland Islands oil exploration

- **Development:** `en#59` (db `entity-review-en`)
- **Domain / type:** security / threat
- **Items:** 2; **sources:** Al Jazeera, BBC World; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 1013 | BBC World | en | 2026-09-29 03:50 | Argentina threatens legal action against UK over Falkland Islands oil exploration | President Javier Milei set a two-week deadline for the Sea Lion oilfield project to be scrapped. |
| 1092 | Al Jazeera | en | 2026-09-29 09:17 | Argentina’s Milei threatens legal action over Falklands oil project | Argentina gives UK two weeks to cease operations or face maritime court action. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Argentina | GPE | yes | 3 | Argentina threatens legal action against UK over Falkland Islands oil exploration President Javier Milei set a two-week deadline for the Sea Lion oil… |
| UK | GPE | yes | 2 | Argentina threatens legal action against UK over Falkland Islands oil exploration President Javier Milei set a two-week deadline for the Sea Lion oil… |
| Falkland Islands | LOC | yes | 1 | Argentina threatens legal action against UK over Falkland Islands oil exploration President Javier Milei set a two-week deadline for the Sea Lion oil… |
| Javier Milei | PERSON | yes | 1 | Argentina threatens legal action against UK over Falkland Islands oil exploration President Javier Milei set a two-week deadline for the Sea Lion oil… |
| two-week | DATE | no (label not stored) | 1 | Argentina threatens legal action against UK over Falkland Islands oil exploration President Javier Milei set a two-week deadline for the Sea Lion oil… |
| Sea Lion | ORG | yes | 1 | Argentina threatens legal action against UK over Falkland Islands oil exploration President Javier Milei set a two-week deadline for the Sea Lion oil… |
| Milei | NORP | yes | 1 | Argentina’s Milei threatens legal action over Falklands oil project Argentina gives UK two weeks to cease operations or face maritime court action. |
| Falklands | GPE | yes | 1 | Argentina’s Milei threatens legal action over Falklands oil project Argentina gives UK two weeks to cease operations or face maritime court action. |
| two weeks | DATE | no (label not stored) | 1 | Argentina’s Milei threatens legal action over Falklands oil project Argentina gives UK two weeks to cease operations or face maritime court action. |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Argentina | GPE | Argentina | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Falklands | GPE | Falklands | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| UK | GPE | UK | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Falkland Islands | LOC | Falkland Islands | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Milei | NORP | Milei | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Sea Lion | ORG | Sea Lion | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Javier Milei | PERSON | Javier Milei | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Argentina | yes | — | argentina → argentina |
| title ×1 | UK | yes | — | united kingdom → united kingdom |
| lead ×1 | Javier Milei | yes | — | javier milei → javier milei |
| lead ×1 | Sea Lion | yes | — | sea lion → sea lion |
| title ×1 | Milei | yes | — | milei → milei |
| title ×1 | Falklands | no | topic / not a participant | falklands → falklands |
| lead ×1 | Argentina | yes | — | argentina → argentina |
| lead ×1 | UK | yes | — | united kingdom → united kingdom |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): argentina 2.0, united kingdom 1.5, milei 1.0, sea lion 0.5, javier milei 0.5
- **Final principal actors:** argentina, milei, united kingdom
- **Entities flagged principal on the Development:** Argentina, Milei, UK

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| UK | united kingdom | country | — | yes |
| Argentina | argentina | country | — | yes |
| Falkland Islands | falkland islands | not in gazetteer | — | no |
| Falklands | falklands | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Argentina | GPE | yes | yes | yes | yes | — | yes |
| UK | GPE | yes | yes | yes | yes | — | yes |
| Milei | NORP | yes | — | yes | yes | — | yes |
| Falklands | GPE | — | yes | — | — | — | — |
| Falkland Islands | LOC | — | yes | — | — | — | — |
| Sea Lion | ORG | — | — | — | — | — | — |
| Javier Milei | PERSON | — | — | — | — | — | — |

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 11. Estonia blames Russia for arson attack on company supplying vehicles to Ukraine

- **Development:** `en#64` (db `entity-review-en`)
- **Domain / type:** security / security_incident
- **Items:** 5; **sources:** Al Jazeera, BBC World, Breaking Defense, Defense News, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 1123 | South China Morning Post | en | 2026-09-29 12:07 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine | Estonian authorities said on Tuesday they had concluded that an arson attack in mid-August on a defence company that provides military vehicles to Ukraine was an act of sabotage commissioned by Russi… |
| 1143 | BBC World | en | 2026-09-29 13:15 | Estonia blames Russia for arson at defence company supplying Ukraine | Russia has been accused of launching sabotage attacks across a number of European Nato countries which have been helping Ukraine. |
| 1153 | Al Jazeera | en | 2026-09-29 13:26 | Estonia says Russia ordered August arson attack on defence company | Tallinn accuses Moscow of responsibility for the fire at Estonian company Milrem Robotics, a supplier of unmanned ground vehicles to Ukraine. |
| 1175 | Breaking Defense | en | 2026-09-29 14:42 | Estonia accuses Russia of ordering August arson attack on Milrem | Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to undermine our unity and support for Ukraine,” NATO Secretary General Mark Rutte said today. |
| 1172 | Defense News | en | 2026-09-29 14:52 | Estonia blames Russia in arson attack on military robotics firm Milrem | GLASGOW, Scotland — Russian special services were behind the fire at a building used by an Estonian military robotics company last month, the government in Tallinn said on Tuesday |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Estonia | GPE | yes | 6 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine Estonian authorities said on Tuesday they had concluded that an arson… |
| Russia | GPE | yes | 8 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine Estonian authorities said on Tuesday they had concluded that an arson… |
| Ukraine | GPE | yes | 6 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine Estonian authorities said on Tuesday they had concluded that an arson… |
| Estonian | NORP | yes | 3 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine Estonian authorities said on Tuesday they had concluded that an arson… |
| Tuesday | DATE | no (label not stored) | 2 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine Estonian authorities said on Tuesday they had concluded that an arson… |
| mid-August | DATE | no (label not stored) | 1 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine Estonian authorities said on Tuesday they had concluded that an arson… |
| Russian | NORP | yes | 2 | Estonia blames Russia for arson attack on company supplying vehicles to Ukraine Estonian authorities said on Tuesday they had concluded that an arson… |
| Margus Tsahkna | PERSON | yes | 1 | Foreign Minister Margus Tsahkna said that “such actions are absolutely unacceptable” and that Russia’s charge d’affaires in Tallinn was being summone… |
| Tallinn | GPE | yes | 3 | Foreign Minister Margus Tsahkna said that “such actions are absolutely unacceptable” and that Russia’s charge d’affaires in Tallinn was being summone… |
| overnight | TIME | no (label not stored) | 1 | A fire broke out overnight on August 15 at a building in Estonia’s capital used by Milrem Robotics, but was... |
| August 15 | DATE | no (label not stored) | 1 | A fire broke out overnight on August 15 at a building in Estonia’s capital used by Milrem Robotics, but was... |
| Milrem Robotics | ORG | yes | 2 | A fire broke out overnight on August 15 at a building in Estonia’s capital used by Milrem Robotics, but was... |
| European Nato | ORG | yes | 1 | Estonia blames Russia for arson at defence company supplying Ukraine Russia has been accused of launching sabotage attacks across a number of Europea… |
| August | DATE | no (label not stored) | 2 | Estonia says Russia ordered August arson attack on defence company Tallinn accuses Moscow of responsibility for the fire at Estonian company Milrem R… |
| Moscow | GPE | yes | 1 | Estonia says Russia ordered August arson attack on defence company Tallinn accuses Moscow of responsibility for the fire at Estonian company Milrem R… |
| Milrem | PERSON | yes | 3 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| NATO | ORG | yes | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| Mark Rutte | PERSON | yes | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| today | DATE | no (label not stored) | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| Milrem GLASGOW | ORG | yes | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| Scotland | GPE | yes | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| last month | DATE | no (label not stored) | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| six-week | DATE | no (label not stored) | 1 | The finding comes after a six-week investigation by the Estonian Internal Security Service. |
| the Estonian Internal Security Service | ORG | yes | 1 | The finding comes after a six-week investigation by the Estonian Internal Security Service. |
| the Russian Federation | GPE | yes | 1 | In a press statement, the government said it could say “with full confidence that the arson attack on the building of defence industry company Milrem… |
| ”A | ORG | yes | 1 | ”A fire was spotted by residents in a Lasnamäe neighborhood building used by Milrem in th |
| Lasnamäe | ORG | yes | 1 | ”A fire was spotted by residents in a Lasnamäe neighborhood building used by Milrem in th |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Leipzig/Halle Airport | FAC | Leipzig/Halle Airport | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Bulgarian | GPE | Bulgaria | exact alias | 'Bulgarian' is a recorded name of 'Bulgaria' | 1 | | | | | | |
| Chargé | GPE | Chargé | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Estonia | GPE | Estonia | new entity | no existing match: the mention created this entity | 5 | | | | | | |
| Estonian | GPE | Estonia | exact alias | 'Estonian' is a recorded name of 'Estonia' | 2 | | | | | | |
| German | GPE | Germany | exact alias | 'German' is a recorded name of 'Germany' | 1 | | | | | | |
| Germany | GPE | Germany | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Milrem GLASGOW | GPE | Milrem GLASGOW | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Munich | GPE | Munich | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Schwarz | GPE | Schwarz | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Scotland | GPE | Scotland | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Tallinn | GPE | Tallinn | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| The United Arab Emirates’ | GPE | the United Arab Emirates | fuzzy | best alias 'the United Arab Emirates' scored 98 (threshold 80) | 1 | | | | | | |
| Ukraine | GPE | Ukraine | new entity | no existing match: the mention created this entity | 5 | | | | | | |
| Ukraine Russia | GPE | Ukraine Russia | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Europe | LOC | Europe | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| European | LOC | Europe | exact alias | 'European' is a recorded name of 'Europe' | 1 | | | | | | |
| Dutch | NORP | Dutch | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Latvia | NORP | Latvian | exact alias | 'Latvia' is a recorded name of 'Latvian' | 1 | | | | | | |
| Latvian | NORP | Latvian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Russia | NORP | Russian | exact alias | 'Russia' is a recorded name of 'Russian' | 5 | | | | | | |
| Russian | NORP | Russian | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Ukraine Estonian | NORP | Ukraine Estonian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Ukrainian | NORP | Ukrainian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Western | NORP | Western | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Boeing | ORG | Boeing | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| EDGE | ORG | EDGE | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| European Nato | ORG | EU | fuzzy | best alias 'the European Union' scored 81 (threshold 80) | 1 | | | | | | |
| ISS | ORG | ISS | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Kremlin | ORG | Kremlin | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Lasnamäe | ORG | Lasnamäe | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Milrem Robotics | ORG | Milrem Robotics | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| NATO | ORG | NATO | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Rohde & | ORG | Rohde & | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Tsahkna | ORG | Tsahkna | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the Estonian Internal Security Service | ORG | the Estonian Internal Security Service | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| ”A | ORG | ”A | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Dimitry Peskov | PERSON | Dimitry Peskov | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Helsing | PERSON | Helsing | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Kristen Michal | PERSON | Kristen Michal | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Margo Palloson | PERSON | Margo Palloson | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Margus Tsahkna | PERSON | Margus Tsahkna | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Mark Rutte | PERSON | Mark Rutte | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Milrem | PERSON | Milrem | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Palloson | PERSON | Palloson | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Peskov | PERSON | Peskov | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| 757 | PRODUCT | 757 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| THeMIS | PRODUCT | THeMIS | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Estonian | NORP | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| Milrem GLASGOW | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×5 | Estonia | yes | — | estonia → estonia |
| title ×5 | Russia | yes | — | russia → russia |
| title ×1 | Ukraine | no | topic / not a participant | ukraine → ukraine |
| lead ×2 | Estonian | yes | — | estonia → estonia |
| lead ×3 | Ukraine | no | topic / not a participant | ukraine → ukraine |
| lead ×2 | Russian | yes | — | russia → russia |
| title ×1 | Ukraine | yes | — | ukraine → ukraine |
| lead ×1 | Russia | yes | — | russia → russia |
| lead ×1 | European Nato | no | topic / not a participant | european nato → european nato |
| lead ×1 | Ukraine | yes | — | ukraine → ukraine |
| lead ×1 | Tallinn | yes | — | tallinn → tallinn |
| lead ×1 | Moscow | yes | — | russia → russia |
| lead ×1 | Estonian | no | topic / not a participant | estonia → estonia |
| lead ×1 | Milrem Robotics | no | topic / not a participant | milrem robotics → milrem robotics |
| title ×2 | Milrem | yes | — | milrem → milrem |
| lead ×1 | Russia | no | topic / not a participant | russia → russia |
| lead ×1 | NATO | yes | — | nato → nato |
| lead ×1 | Mark Rutte | yes | — | mark rutte → mark rutte |
| lead ×1 | GLASGOW | yes | — | glasgow → glasgow |
| lead ×1 | Scotland | no | place | scotland → scotland |
| lead ×1 | Tallinn | no | topic / not a participant | tallinn → tallinn |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): russia 5.0, estonia 5.0, milrem 2.0, ukraine 1.0, tallinn 0.5, mark rutte 0.5, nato 0.5, glasgow 0.5
- **Final principal actors:** estonia, milrem, russia
- **Entities flagged principal on the Development:** Estonia, Milrem, Russian

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Ukraine | ukraine | country | — | yes |
| Estonia | estonia | country | — | yes |
| Tallinn | tallinn | not in gazetteer | — | yes |
| Ukraine Russia | ukraine russia | not in gazetteer | — | no |
| Estonian | estonian | not in gazetteer | — | yes |
| Germany | germany | country | — | no |
| German | german | not in gazetteer | — | no |
| Europe | europe | not in gazetteer | — | no |
| European | european | not in gazetteer | — | no |
| Leipzig/Halle Airport | leipzig/halle airport | not in gazetteer | — | no |
| Bulgarian | bulgarian | not in gazetteer | — | no |
| Scotland | scotland | sub-national | united kingdom | no |
| The United Arab Emirates’ | united arab emirates | country | — | no |
| Munich | munich | sub-national | germany | no |
| Milrem GLASGOW | milrem glasgow | not in gazetteer | — | no |
| Chargé | chargé | not in gazetteer | — | no |
| Schwarz | schwarz | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Estonia | GPE | yes | yes | yes | yes | — | yes |
| Russian | NORP | yes | — | yes | yes | — | yes |
| Milrem | PERSON | yes | — | yes | yes | — | yes |
| Leipzig/Halle Airport | FAC | — | yes | — | — | — | — |
| Bulgaria | GPE | — | yes | — | — | — | — |
| Chargé | GPE | — | yes | — | — | — | — |
| Germany | GPE | — | yes | — | — | — | — |
| Milrem GLASGOW | GPE | — | yes | — | — | — | — |
| Munich | GPE | — | yes | — | — | — | — |
| Schwarz | GPE | — | yes | — | — | — | — |
| Scotland | GPE | — | yes | — | — | — | — |
| Tallinn | GPE | — | yes | — | — | — | — |
| Ukraine | GPE | — | yes | — | — | — | — |
| Ukraine Russia | GPE | — | yes | — | — | — | — |
| the United Arab Emirates | GPE | — | yes | — | — | — | — |
| Europe | LOC | — | yes | — | — | — | — |
| Dutch | NORP | — | — | — | — | — | — |
| Latvian | NORP | — | — | — | — | — | — |
| Ukraine Estonian | NORP | — | — | — | — | — | — |
| Ukrainian | NORP | — | — | — | — | — | — |
| Western | NORP | — | — | — | — | — | — |
| Boeing | ORG | — | — | — | — | — | — |
| EDGE | ORG | — | — | — | — | — | — |
| EU | ORG | — | — | — | — | — | — |
| ISS | ORG | — | — | — | — | — | — |
| Kremlin | ORG | — | — | — | — | — | — |
| Lasnamäe | ORG | — | — | — | — | — | — |
| Milrem Robotics | ORG | — | — | — | — | — | — |
| NATO | ORG | — | — | — | — | — | — |
| Rohde & | ORG | — | — | — | — | — | — |
| Tsahkna | ORG | — | — | — | — | — | — |
| the Estonian Internal Security Service | ORG | — | — | — | — | — | — |
| ”A | ORG | — | — | — | — | — | — |
| Dimitry Peskov | PERSON | — | — | — | — | — | — |
| Helsing | PERSON | — | — | — | — | — | — |
| Kristen Michal | PERSON | — | — | — | — | — | — |
| Margo Palloson | PERSON | — | — | — | — | — | — |
| Margus Tsahkna | PERSON | — | — | — | — | — | — |
| Mark Rutte | PERSON | — | — | — | — | — | — |
| Palloson | PERSON | — | — | — | — | — | — |
| Peskov | PERSON | — | — | — | — | — | — |
| 757 | PRODUCT | — | — | — | — | — | — |
| THeMIS | PRODUCT | — | — | — | — | — | — |

### ⚑ Automatic flags

- **alias resolution**: fuzzy: 'European Nato' -> 'EU' (best alias 'the European Union' scored 81 (threshold 80))
- **NER detection**: article/possessive kept in span: 'The United Arab Emirates’'
- **alias resolution**: fuzzy: 'The United Arab Emirates’' -> 'the United Arab Emirates' (best alias 'the United Arab Emirates' scored 98 (threshold 80))
- **NER detection**: article/possessive kept in span: 'the Estonian Internal Security Service'
- **NER detection**: malformed span 'THeMIS' (PRODUCT)
- **NER detection**: malformed span 'Milrem GLASGOW' (ORG)
- **person -> state/institution mapping** (principal): principal person 'milrem' has no state/body mapping (fine for private persons)

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 12. Estonia blames Russia in arson attack on military robotics firm Milrem

- **Development:** `ml#25` (db `entity-review-ml`)
- **Domain / type:** security / security_incident
- **Items:** 2; **sources:** Breaking Defense, Defense News; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 512 | Breaking Defense | en | 2026-09-29 14:42 | Estonia accuses Russia of ordering August arson attack on Milrem | Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to undermine our unity and support for Ukraine,” NATO Secretary General Mark Rutte said today. |
| 490 | Defense News | en | 2026-09-29 14:52 | Estonia blames Russia in arson attack on military robotics firm Milrem | GLASGOW, Scotland — Russian special services were behind the fire at a building used by an Estonian military robotics company last month, the government in Tallinn said on Tuesday |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Estonia | GPE | yes | 2 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| Russia | GPE | yes | 3 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| August | DATE | no (label not stored) | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| Milrem | PERSON | yes | 3 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| Ukraine | GPE | yes | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| NATO | ORG | yes | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| Mark Rutte | PERSON | yes | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| today | DATE | no (label not stored) | 1 | Estonia accuses Russia of ordering August arson attack on Milrem Despite Russia’s ongoing “reckless campaign of hostile actions,” it is “failing to u… |
| Milrem GLASGOW | ORG | yes | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| Scotland | GPE | yes | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| Russian | NORP | yes | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| Estonian | NORP | yes | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| last month | DATE | no (label not stored) | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| Tallinn | GPE | yes | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| Tuesday | DATE | no (label not stored) | 1 | Estonia blames Russia in arson attack on military robotics firm Milrem GLASGOW, Scotland — Russian special services were behind the fire at a buildin… |
| six-week | DATE | no (label not stored) | 1 | The finding comes after a six-week investigation by the Estonian Internal Security Service. |
| the Estonian Internal Security Service | ORG | yes | 1 | The finding comes after a six-week investigation by the Estonian Internal Security Service. |
| the Russian Federation | GPE | yes | 1 | In a press statement, the government said it could say “with full confidence that the arson attack on the building of defence industry company Milrem… |
| ”A | ORG | yes | 1 | ”A fire was spotted by residents in a Lasnamäe neighborhood building used by Milrem in th |
| Lasnamäe | ORG | yes | 1 | ”A fire was spotted by residents in a Lasnamäe neighborhood building used by Milrem in th |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Leipzig/Halle Airport | FAC | Leipzig/Halle Airport | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Chargé | GPE | Chargé | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Estonia | GPE | Estonia | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Estonian | GPE | Estonia | exact alias | 'Estonian' is a recorded name of 'Estonia' | 1 | | | | | | |
| Milrem GLASGOW | GPE | Milrem GLASGOW | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Munich | GPE | Munich | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Russia | GPE | Russia | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Russian | GPE | Russia | exact alias | 'Russian' is a recorded name of 'Russia' | 1 | | | | | | |
| Schwarz | GPE | Schwarz | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Scotland | GPE | Scotland | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Tallinn | GPE | Tallinn | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| The United Arab Emirates’ | GPE | the United Arab Emirates | exact alias | 'The United Arab Emirates’' is a recorded name of 'the United Arab Emirates' | 1 | | | | | | |
| Ukraine | GPE | Ukraine | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Europe | LOC | Europe | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| European | LOC | Europe | fuzzy | best alias 'Europe' scored 86 (threshold 80) | 1 | | | | | | |
| Bulgarian | NORP | Bulgarian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Dutch | NORP | Dutch | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| German | NORP | the German | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Germany | NORP | the German | fuzzy | best alias 'the German' scored 92 (threshold 80) | 1 | | | | | | |
| Latvia | NORP | Latvian | exact alias | 'Latvia' is a recorded name of 'Latvian' | 1 | | | | | | |
| Latvian | NORP | Latvian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Ukrainian | NORP | Ukrainian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Western | NORP | Western | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Boeing | ORG | Boeing | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| EDGE | ORG | EDGE | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| ISS | ORG | ISIS | exact alias | 'ISS' is a recorded name of 'ISIS' | 1 | | | | | | |
| Kremlin | ORG | Kremlin | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Lasnamäe | ORG | Lasnamäe | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| NATO | ORG | NATO | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Rohde & | ORG | Rohde & | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Tsahkna | ORG | Tsahkna | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the Estonian Internal Security Service | ORG | the Estonian Internal Security Service | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| ”A | ORG | ”A | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Dimitry Peskov | PERSON | Dimitry Peskov | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Helsing | PERSON | Helsing | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Kristen Michal | PERSON | Kristen Michal | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Margo Palloson | PERSON | Margo Palloson | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Margus Tsahkna | PERSON | Margus Tsahkna | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Mark Rutte | PERSON | Mark Rutte | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Milrem | PERSON | Milrem | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Palloson | PERSON | Palloson | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Peskov | PERSON | Peskov | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| 757 | PRODUCT | 757 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| THeMIS | PRODUCT | THeMIS | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Milrem GLASGOW | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Estonia | yes | — | estonia → estonia |
| title ×2 | Russia | yes | — | russia → russia |
| title ×2 | Milrem | yes | — | milrem → milrem |
| lead ×1 | Russia | no | topic / not a participant | russia → russia |
| lead ×1 | Ukraine | no | topic / not a participant | ukraine → ukraine |
| lead ×1 | NATO | yes | — | nato → nato |
| lead ×1 | Mark Rutte | yes | — | mark rutte → mark rutte |
| lead ×1 | GLASGOW | yes | — | glasgow → glasgow |
| lead ×1 | Scotland | no | place | scotland → scotland |
| lead ×1 | Russian | yes | — | russia → russia |
| lead ×1 | Estonian | yes | — | estonia → estonia |
| lead ×1 | Tallinn | no | topic / not a participant | tallinn → tallinn |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): russia 2.0, estonia 2.0, milrem 2.0, mark rutte 0.5, nato 0.5, glasgow 0.5
- **Final principal actors:** estonia, milrem, russia
- **Entities flagged principal on the Development:** Estonia, Kremlin, Milrem, Russia

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Russia | russia | country | — | yes |
| Ukraine | ukraine | country | — | no |
| Estonia | estonia | country | — | yes |
| Russian | russian | not in gazetteer | — | yes |
| Europe | europe | not in gazetteer | — | no |
| European | european | not in gazetteer | — | no |
| Munich | munich | sub-national | germany | no |
| The United Arab Emirates’ | united arab emirates | country | — | no |
| Estonian | estonian | not in gazetteer | — | yes |
| Milrem GLASGOW | milrem glasgow | not in gazetteer | — | no |
| Scotland | scotland | sub-national | united kingdom | no |
| Tallinn | tallinn | not in gazetteer | — | no |
| Leipzig/Halle Airport | leipzig/halle airport | not in gazetteer | — | no |
| Chargé | chargé | not in gazetteer | — | no |
| Schwarz | schwarz | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Estonia | GPE | yes | yes | yes | yes | — | yes |
| Russia | GPE | yes | yes | yes | yes | — | yes |
| Kremlin | ORG | yes | — | yes | yes | — | yes |
| Milrem | PERSON | yes | — | yes | yes | — | yes |
| Leipzig/Halle Airport | FAC | — | yes | — | — | — | — |
| Chargé | GPE | — | yes | — | — | — | — |
| Milrem GLASGOW | GPE | — | yes | — | — | — | — |
| Munich | GPE | — | yes | — | — | — | — |
| Schwarz | GPE | — | yes | — | — | — | — |
| Scotland | GPE | — | yes | — | — | — | — |
| Tallinn | GPE | — | yes | — | — | — | — |
| Ukraine | GPE | — | yes | — | — | — | — |
| the United Arab Emirates | GPE | — | yes | — | — | — | — |
| Europe | LOC | — | yes | — | — | — | — |
| Bulgarian | NORP | — | — | — | — | — | — |
| Dutch | NORP | — | — | — | — | — | — |
| Latvian | NORP | — | — | — | — | — | — |
| Ukrainian | NORP | — | — | — | — | — | — |
| Western | NORP | — | — | — | — | — | — |
| the German | NORP | — | — | — | — | — | — |
| Boeing | ORG | — | — | — | — | — | — |
| EDGE | ORG | — | — | — | — | — | — |
| ISIS | ORG | — | — | — | — | — | — |
| Lasnamäe | ORG | — | — | — | — | — | — |
| NATO | ORG | — | — | — | — | — | — |
| Rohde & | ORG | — | — | — | — | — | — |
| Tsahkna | ORG | — | — | — | — | — | — |
| the Estonian Internal Security Service | ORG | — | — | — | — | — | — |
| ”A | ORG | — | — | — | — | — | — |
| Dimitry Peskov | PERSON | — | — | — | — | — | — |
| Helsing | PERSON | — | — | — | — | — | — |
| Kristen Michal | PERSON | — | — | — | — | — | — |
| Margo Palloson | PERSON | — | — | — | — | — | — |
| Margus Tsahkna | PERSON | — | — | — | — | — | — |
| Mark Rutte | PERSON | — | — | — | — | — | — |
| Palloson | PERSON | — | — | — | — | — | — |
| Peskov | PERSON | — | — | — | — | — | — |
| 757 | PRODUCT | — | — | — | — | — | — |
| THeMIS | PRODUCT | — | — | — | — | — | — |

### ⚑ Automatic flags

- **alias resolution**: fuzzy: 'European' -> 'Europe' (best alias 'Europe' scored 86 (threshold 80))
- **alias resolution**: fuzzy: 'Germany' -> 'the German' (best alias 'the German' scored 92 (threshold 80))
- **NER detection**: article/possessive kept in span: 'The United Arab Emirates’'
- **NER detection**: article/possessive kept in span: 'the Estonian Internal Security Service'
- **NER detection**: malformed span 'THeMIS' (PRODUCT)
- **NER detection**: malformed span 'Milrem GLASGOW' (ORG)
- **person -> state/institution mapping** (principal): principal person 'milrem' has no state/body mapping (fine for private persons)

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

---

# Political

## 13. Italy ministers agree to ban burqa and niqab in school and cap foreigners in class

- **Development:** `en#7` (db `entity-review-en`)
- **Domain / type:** political / policy_change
- **Items:** 2; **sources:** BBC World, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 44 | BBC World | en | 2026-09-24 19:32 | Italy ministers agree to ban burqa and niqab in school and cap foreigners in class | Prime Minister Giorgia Meloni described the measures as "common-sense tools that do not divide but really help to integrate". |
| 320 | South China Morning Post | en | 2026-09-25 11:20 | Italy to ban burkas in schools, with 30% cap on pupils with poor Italian | Italy has passed a decree banning face coverings in all schools and capping the proportion of newly arrived foreign pupils with insufficient Italian at 30 per cent per class from the next school year… |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Italy | GPE | yes | 4 | Italy ministers agree to ban burqa and niqab in school and cap foreigners in class Prime Minister Giorgia Meloni described the measures as "common-se… |
| Giorgia Meloni | PERSON | yes | 1 | Italy ministers agree to ban burqa and niqab in school and cap foreigners in class Prime Minister Giorgia Meloni described the measures as "common-se… |
| 30% | PERCENT | no (label not stored) | 1 | Italy to ban burkas in schools, with 30% cap on pupils with poor Italian Italy has passed a decree banning face coverings in all schools and capping … |
| Italian | NORP | yes | 4 | Italy to ban burkas in schools, with 30% cap on pupils with poor Italian Italy has passed a decree banning face coverings in all schools and capping … |
| 30 per cent | MONEY | no (label not stored) | 2 | Italy to ban burkas in schools, with 30% cap on pupils with poor Italian Italy has passed a decree banning face coverings in all schools and capping … |
| the next school year | DATE | no (label not stored) | 1 | Italy to ban burkas in schools, with 30% cap on pupils with poor Italian Italy has passed a decree banning face coverings in all schools and capping … |
| Rome | GPE | yes | 1 | Italy to ban burkas in schools, with 30% cap on pupils with poor Italian Italy has passed a decree banning face coverings in all schools and capping … |
| Friday | DATE | no (label not stored) | 1 | Italy to ban burkas in schools, with 30% cap on pupils with poor Italian Italy has passed a decree banning face coverings in all schools and capping … |
| at least two years | DATE | no (label not stored) | 1 | The government said the 30 per cent quota applies in primary school to children who do not hold Italian citizenship, were not born in Italy and have … |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Italy | GPE | Italy | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Rome | GPE | ROME | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Italian | ORG | Taliban | exact alias | 'Italian' is a recorded name of 'Taliban' | 1 | | | | | | |
| Giorgia Meloni | PERSON | Giorgia Meloni | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Italy | yes | — | italy → italy |
| lead ×1 | Giorgia Meloni | yes | — | giorgia meloni → giorgia meloni |
| title ×1 | Italian | yes | — | italy → italy |
| lead ×1 | Italy | yes | — | italy → italy |
| lead ×1 | Italian | yes | — | italy → italy |
| lead ×1 | Rome | no | place | rome → rome |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): italy 2.0, giorgia meloni 0.5
- **Final principal actors:** italy
- **Entities flagged principal on the Development:** Italy

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Italy | italy | country | — | yes |
| Rome | rome | sub-national | italy | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Italy | GPE | yes | yes | yes | yes | — | yes |
| ROME | GPE | — | yes | — | — | — | — |
| Taliban | ORG | — | — | — | — | — | — |
| Giorgia Meloni | PERSON | — | — | — | — | — | — |

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 14. Two mass shootings in South Africa leave 27 dead

- **Development:** `en#32` (db `entity-review-en`)
- **Domain / type:** political / election
- **Items:** 4; **sources:** Al Jazeera, BBC World, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 667 | South China Morning Post | en | 2026-09-27 12:07 | South African police probe mining feud shooting, 27 dead as elections near | South African police on Sunday were hunting the perpetrators of two separate shootings that killed 27 people within hours of each other, in stark reminders of the country’s problem with gun violence. |
| 632 | BBC World | en | 2026-09-27 14:09 | Two mass shootings in South Africa leave 27 dead | The two attacks hours apart come as the country struggles to stop high levels of gang-related armed violence. |
| 687 | Al Jazeera | en | 2026-09-27 16:58 | Dozens killed in two mass shootings in South Africa | At least 27 people have been killed in two mass shootings across South Africa. |
| 926 | BBC World | en | 2026-09-28 17:26 | Twelve women have been killed in one part of South Africa since July. Here's what we know so far | South African President Cyril Ramaphosa says the murders are a "stain on our national conscience". |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| South African | NORP | yes | 3 | South African police probe mining feud shooting, 27 dead as elections near South African police on Sunday were hunting the perpetrators of two separa… |
| 27 | CARDINAL | no (label not stored) | 3 | South African police probe mining feud shooting, 27 dead as elections near South African police on Sunday were hunting the perpetrators of two separa… |
| Sunday | DATE | no (label not stored) | 1 | South African police probe mining feud shooting, 27 dead as elections near South African police on Sunday were hunting the perpetrators of two separa… |
| two | CARDINAL | no (label not stored) | 3 | South African police probe mining feud shooting, 27 dead as elections near South African police on Sunday were hunting the perpetrators of two separa… |
| hours | TIME | no (label not stored) | 1 | South African police probe mining feud shooting, 27 dead as elections near South African police on Sunday were hunting the perpetrators of two separa… |
| Johannesburg | GPE | yes | 1 | Officials were still establishing the motives for the shootings near Johannesburg and Cape Town, but initial investigations suggested one could be a … |
| Cape Town | LOC | yes | 1 | Officials were still establishing the motives for the shootings near Johannesburg and Cape Town, but initial investigations suggested one could be a … |
| South Africa | GPE | yes | 5 | Violent crime remains rife in South Africa, despite government efforts to curb one of... |
| one | CARDINAL | no (label not stored) | 2 | Violent crime remains rife in South Africa, despite government efforts to curb one of... |
| Two | CARDINAL | no (label not stored) | 1 | Two mass shootings in South Africa leave 27 dead The two attacks hours apart come as the country struggles to stop high levels of gang-related armed … |
| two attacks hours | TIME | no (label not stored) | 1 | Two mass shootings in South Africa leave 27 dead The two attacks hours apart come as the country struggles to stop high levels of gang-related armed … |
| Dozens | CARDINAL | no (label not stored) | 1 | Dozens killed in two mass shootings in South Africa At least 27 people have been killed in two mass shootings across South Africa. |
| At least 27 | CARDINAL | no (label not stored) | 1 | Dozens killed in two mass shootings in South Africa At least 27 people have been killed in two mass shootings across South Africa. |
| Twelve | CARDINAL | no (label not stored) | 1 | Twelve women have been killed in one part of South Africa since July. |
| July | DATE | no (label not stored) | 1 | Twelve women have been killed in one part of South Africa since July. |
| Cyril Ramaphosa | PERSON | yes | 1 | Here's what we know so far South African President Cyril Ramaphosa says the murders are a "stain on our national conscience". |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Johannesburg | GPE | Johannesburg | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Cape Town | LOC | Cape Town | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| South Africa | NORP | South African | exact alias | 'South Africa' is a recorded name of 'South African' | 4 | | | | | | |
| South African | NORP | South African | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Cyril Ramaphosa | PERSON | Cyril Ramaphosa | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | South African | yes | — | south africa → south africa |
| lead ×2 | South African | yes | — | south africa → south africa |
| title ×3 | South Africa | no | topic / not a participant | south africa → south africa |
| lead ×1 | South Africa | no | topic / not a participant | south africa → south africa |
| lead ×1 | Cyril Ramaphosa | yes | — | cyril ramaphosa → cyril ramaphosa |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): south africa 2.0, cyril ramaphosa 1.0
- **Final principal actors:** south africa
- **Entities flagged principal on the Development:** South African

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Johannesburg | johannesburg | sub-national | south africa | no |
| Cape Town | cape town | sub-national | south africa | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| South African | NORP | yes | — | yes | yes | — | yes |
| Johannesburg | GPE | — | yes | — | — | — | — |
| Cape Town | LOC | — | yes | — | — | — | — |
| Cyril Ramaphosa | PERSON | — | — | — | — | — | — |

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 15. Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war

- **Development:** `ml#13` (db `entity-review-ml`)
- **Domain / type:** political / policy_change
- **Items:** 3; **sources:** Defense News, Kyiv Independent; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 494 | Defense News | en | 2026-09-28 18:07 | Russia raises 2027 military spending by 27%, budget documents show | Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027, around 27% more than the 13.5 trillion roubles, or $159.8 billion, originally budgeted and the highest figure since… |
| 285 | Kyiv Independent | en | 2026-09-29 16:45 | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization | Compared to the most recent figure from July 2026, the decree increases total staff by only around 15,500, is the fourth such incremental raise announced this year. |
| 282 | Kyiv Independent | en | 2026-09-29 17:43 | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war | Key developments on Sept |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Russia | GPE | yes | 3 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| 2027 | CARDINAL | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| 27% | PERCENT | no (label not stored) | 2 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| 17.1 trillion roubles | MONEY | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| $202.6 billion | MONEY | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| 2027 | DATE | no (label not stored) | 3 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| around 27% | PERCENT | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| 13.5 trillion roubles | MONEY | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| $159.8 billion | MONEY | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| Ukraine | GPE | yes | 2 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| 2022 | DATE | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| Reuters | ORG | yes | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| Monday | DATE | no (label not stored) | 1 | Russia raises 2027 military spending by 27%, budget documents show Russia plans to spend 17.1 trillion roubles, or $202.6 billion, on defense in 2027… |
| 50 trillion roubles | MONEY | no (label not stored) | 1 | Total defense spending will amount to 50 trillion roubles, or $591.7 billion, in the next three years, according to the documents. |
| $591.7 billion | MONEY | no (label not stored) | 1 | Total defense spending will amount to 50 trillion roubles, or $591.7 billion, in the next three years, according to the documents. |
| the next three years | DATE | no (label not stored) | 1 | Total defense spending will amount to 50 trillion roubles, or $591.7 billion, in the next three years, according to the documents. |
| 2026 | DATE | no (label not stored) | 1 | In 2026, the government planned to spend 12.1 trillion roubles on defense, but the actual amount is classified and will not be disclosed. |
| 12.1 trillion roubles | MONEY | no (label not stored) | 1 | In 2026, the government planned to spend 12.1 trillion roubles on defense, but the actual amount is classified and will not be disclosed. |
| Putin | PERSON | yes | 1 | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization Compared to the most recent figu… |
| Russian | NORP | yes | 3 | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization Compared to the most recent figu… |
| July 2026 | DATE | no (label not stored) | 1 | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization Compared to the most recent figu… |
| only around 15,500 | CARDINAL | no (label not stored) | 1 | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization Compared to the most recent figu… |
| fourth | ORDINAL | no (label not stored) | 1 | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization Compared to the most recent figu… |
| this year | DATE | no (label not stored) | 1 | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization Compared to the most recent figu… |
| Sept. 29 | DATE | no (label not stored) | 1 | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war Key developments on Sept. 29:Russia to raise military … |
| Oleshky | GPE | yes | 1 | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war Key developments on Sept. 29:Russia to raise military … |
| Ukrainian | NORP | yes | 1 | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war Key developments on Sept. 29:Russia to raise military … |
| strikesRussian | NORP | yes | 1 | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war Key developments on Sept. 29:Russia to raise military … |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Oleshky | GPE | Oleshky | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Russia | GPE | Russia | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Russian | GPE | Russia | exact alias | 'Russian' is a recorded name of 'Russia' | 2 | | | | | | |
| Ukraine | GPE | Ukraine | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Ukrainian | NORP | Ukrainian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| strikesRussian | NORP | strikesRussian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| National Wealth Fund | ORG | National Wealth Fund | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Reuters | ORG | Reuters | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Putin | PERSON | Vladimir Putin | seeded (entities.yaml) | 'Putin' is a recorded name of 'Vladimir Putin' | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | Russia | yes | — | russia → russia |
| lead ×1 | Russia | yes | — | russia → russia |
| lead ×1 | Ukraine | no | topic / not a participant | ukraine → ukraine |
| lead ×1 | Reuters | yes | — | reuters → reuters |
| title ×1 | Putin | yes | — | putin → russia |
| title ×2 | Russian | yes | — | russia → russia |
| title ×1 | Ukraine | yes | — | ukraine → ukraine |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): russia 3.0, ukraine 1.0, reuters 0.5
- **Final principal actors:** russia
- **Entities flagged principal on the Development:** Russia, Vladimir Putin

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Russia | russia | country | — | yes |
| Ukraine | ukraine | country | — | yes |
| Russian | russian | not in gazetteer | — | yes |
| Oleshky | oleshky | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Russia | GPE | yes | yes | yes | yes | — | yes |
| Vladimir Putin | PERSON | yes | — | yes | yes | — | yes |
| Oleshky | GPE | — | yes | — | — | — | — |
| Ukraine | GPE | — | yes | — | — | — | — |
| Ukrainian | NORP | — | — | — | — | — | — |
| strikesRussian | NORP | — | — | — | — | — | — |
| National Wealth Fund | ORG | — | — | — | — | — | — |
| Reuters | ORG | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: malformed span 'strikesRussian' (NORP)

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 16. Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory

- **Development:** `ml#17` (db `entity-review-ml`)
- **Domain / type:** political / policy_change
- **Items:** 2; **sources:** Federal Register; **languages:** en (assumed)

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 553 | Federal Register | en (assumed) | 2026-09-29 00:00 | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory | Notice is hereby given, pursuant to CBP regulations, that Intertek USA, Inc |
| 554 | Federal Register | en (assumed) | 2026-09-29 00:00 | Accreditation and Approval of Intertek USA, Inc. (Carteret, NJ), as a Commercial Gauger and Laboratory | Notice is hereby given, pursuant to CBP regulations, that Intertek USA, Inc |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Intertek USA, Inc. | ORG | yes | 4 | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regulat… |
| Chelsea, MA | ORG | yes | 2 | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regulat… |
| Commercial Gauger | ORG | yes | 2 | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regulat… |
| CBP | ORG | yes | 2 | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regulat… |
| the next three years | DATE | no (label not stored) | 2 | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regulat… |
| August 28, 2024 | DATE | no (label not stored) | 1 | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regulat… |
| Carteret | GPE | yes | 2 | Accreditation and Approval of Intertek USA, Inc. (Carteret, NJ), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regula… |
| NJ | GPE | yes | 2 | Accreditation and Approval of Intertek USA, Inc. (Carteret, NJ), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regula… |
| August 28, 2025 | DATE | no (label not stored) | 1 | Accreditation and Approval of Intertek USA, Inc. (Carteret, NJ), as a Commercial Gauger and Laboratory Notice is hereby given, pursuant to CBP regula… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Carteret | GPE | Carteret | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| NJ | GPE | NJ | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| CBP | ORG | CBP | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Chelsea, MA | ORG | Chelsea, MA | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Commercial Gauger and Laboratory | ORG | Commercial Gauger and Laboratory | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Intertek USA, Inc. | ORG | Intertek USA, Inc. | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Commercial Gauger | ORG | — | unresolved | detected now but no stored entity link for this item | 2 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Intertek USA, Inc. | yes | — | intertek usa, inc → intertek usa, inc |
| title ×1 | Chelsea, MA | yes | — | chelsea, ma → chelsea, ma |
| title ×2 | Commercial Gauger and Laboratory | no | topic / not a participant | commercial gauger and laboratory → commercial gauger and laboratory |
| lead ×2 | CBP | no | topic / not a participant | cbp → cbp |
| lead ×2 | Intertek USA | no | topic / not a participant | intertek usa → intertek usa |
| title ×1 | Carteret | yes | — | carteret → carteret |
| title ×1 | NJ | no | topic / not a participant | nj → nj |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): intertek usa, inc 2.0, chelsea, ma 1.0, carteret 1.0
- **Final principal actors:** carteret, chelsea, ma, intertek usa, inc
- **Entities flagged principal on the Development:** Carteret, Chelsea, MA, Intertek USA, Inc.

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Carteret | carteret | not in gazetteer | — | yes |
| NJ | nj | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Carteret | GPE | yes | yes | yes | yes | — | yes |
| Chelsea, MA | ORG | yes | — | yes | yes | — | yes |
| Intertek USA, Inc. | ORG | yes | — | yes | yes | — | yes |
| NJ | GPE | — | yes | — | — | — | — |
| CBP | ORG | — | — | — | — | — | — |
| Commercial Gauger and Laboratory | ORG | — | — | — | — | — | — |

### ⚑ Automatic flags

- **location/actor confusion** (principal): principal 'carteret' comes from place mentions (GPE)
- **location/actor confusion** (principal): principal 'chelsea, ma' is a 'Place, ST' address typed ORG
- **contextual organisation** (principal): principal 'chelsea, ma' is a company in an administrative notice
- **contextual organisation** (principal): principal 'intertek usa, inc' is a company in an administrative notice
- **principal-selection failure** (principal): no state among the principals (carteret, chelsea, ma, intertek usa, inc); check they are actors

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

---

# Economic

## 17. Israel revokes Dutch diplomats’ status over sanctions on settlements

- **Development:** `en#35` (db `entity-review-en`)
- **Domain / type:** economic / sanctions
- **Items:** 2; **sources:** Al Jazeera, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 710 | Al Jazeera | en | 2026-09-27 20:21 | Israel revokes Dutch diplomats’ status over sanctions on settlements | Israel escalates retaliatory measures as Western sanctions target illegal West Bank settlements. |
| 711 | South China Morning Post | en | 2026-09-27 20:23 | Israel revokes diplomatic status of Dutch diplomats in Ramallah | Israel said on Sunday ⁠it was revoking the ⁠diplomatic status of Dutch ⁠diplomats who represent the Netherlands at the Ramallah-based Palestinian Authority, in response to Dutch sanctions targeting I… |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Israel | GPE | yes | 5 | Israel revokes Dutch diplomats’ status over sanctions on settlements Israel escalates retaliatory measures as Western sanctions target illegal West B… |
| Dutch | NORP | yes | 4 | Israel revokes Dutch diplomats’ status over sanctions on settlements Israel escalates retaliatory measures as Western sanctions target illegal West B… |
| West Bank | GPE | yes | 2 | Israel revokes Dutch diplomats’ status over sanctions on settlements Israel escalates retaliatory measures as Western sanctions target illegal West B… |
| Ramallah | GPE | yes | 2 | Israel revokes diplomatic status of Dutch diplomats in Ramallah Israel said on Sunday ⁠it was revoking the ⁠diplomatic status of Dutch ⁠diplomats who… |
| Sunday | DATE | no (label not stored) | 1 | Israel revokes diplomatic status of Dutch diplomats in Ramallah Israel said on Sunday ⁠it was revoking the ⁠diplomatic status of Dutch ⁠diplomats who… |
| Netherlands | GPE | yes | 1 | Israel revokes diplomatic status of Dutch diplomats in Ramallah Israel said on Sunday ⁠it was revoking the ⁠diplomatic status of Dutch ⁠diplomats who… |
| Palestinian Authority | ORG | yes | 1 | Israel revokes diplomatic status of Dutch diplomats in Ramallah Israel said on Sunday ⁠it was revoking the ⁠diplomatic status of Dutch ⁠diplomats who… |
| Israeli | NORP | yes | 2 | Israel revokes diplomatic status of Dutch diplomats in Ramallah Israel said on Sunday ⁠it was revoking the ⁠diplomatic status of Dutch ⁠diplomats who… |
| earlier this month | DATE | no (label not stored) | 1 | Israel earlier this month ordered the closure of the British consulate in East ‌Jerusalem, which is Britain’s representative with the Palestinian Aut… |
| British | NORP | yes | 1 | Israel earlier this month ordered the closure of the British consulate in East ‌Jerusalem, which is Britain’s representative with the Palestinian Aut… |
| East | LOC | yes | 1 | Israel earlier this month ordered the closure of the British consulate in East ‌Jerusalem, which is Britain’s representative with the Palestinian Aut… |
| Britain | GPE | yes | 1 | Israel earlier this month ordered the closure of the British consulate in East ‌Jerusalem, which is Britain’s representative with the Palestinian Aut… |
| the Palestinian Authority | ORG | yes | 1 | Israel earlier this month ordered the closure of the British consulate in East ‌Jerusalem, which is Britain’s representative with the Palestinian Aut… |
| London | GPE | yes | 1 | Israel earlier this month ordered the closure of the British consulate in East ‌Jerusalem, which is Britain’s representative with the Palestinian Aut… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Britain | GPE | Britain | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| London | GPE | London | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Netherlands | GPE | Netherlands | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Ramallah | GPE | Ramallah | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| West Bank | GPE | West Bank | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| East | LOC | East | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| British | NORP | British | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Dutch | NORP | Dutch | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Israel | NORP | Israeli | exact alias | 'Israel' is a recorded name of 'Israeli' | 2 | | | | | | |
| Israeli | NORP | Israeli | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Palestinian Authority | ORG | Palestinian Authority | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Israel | yes | — | israel → israel |
| title ×2 | Dutch | yes | — | netherlands → netherlands |
| lead ×2 | Israel | yes | — | israel → israel |
| lead ×2 | West Bank | no | place | west bank → west bank |
| title ×1 | Ramallah | no | place | ramallah → ramallah |
| lead ×1 | Dutch | yes | — | netherlands → netherlands |
| lead ×1 | Netherlands | yes | — | netherlands → netherlands |
| lead ×1 | Ramallah | no | place | ramallah → ramallah |
| lead ×1 | Palestinian Authority | no | topic / not a participant | palestinian authority → palestinian authority |
| lead ×1 | Dutch | no | topic / not a participant | netherlands → netherlands |
| lead ×1 | Israeli | yes | — | israel → israel |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): netherlands 2.0, israel 2.0
- **Final principal actors:** israel, netherlands
- **Entities flagged principal on the Development:** Dutch, Israeli, Netherlands

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| West Bank | west bank | sub-national | palestine | no |
| Netherlands | netherlands | country | — | yes |
| Britain | united kingdom | country | — | no |
| London | london | sub-national | england, united kingdom | no |
| Ramallah | ramallah | sub-national | palestine, west bank | no |
| East | east | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Netherlands | GPE | yes | yes | yes | yes | — | yes |
| Dutch | NORP | yes | — | yes | yes | — | yes |
| Israeli | NORP | yes | — | yes | yes | — | yes |
| Britain | GPE | — | yes | — | — | — | — |
| London | GPE | — | yes | — | — | — | — |
| Ramallah | GPE | — | yes | — | — | — | — |
| West Bank | GPE | — | yes | — | — | — | — |
| East | LOC | — | yes | — | — | — | — |
| British | NORP | — | — | — | — | — | — |
| Palestinian Authority | ORG | — | — | — | — | — | — |

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 18. US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says

- **Development:** `en#45` (db `entity-review-en`)
- **Domain / type:** economic / sanctions
- **Items:** 3; **sources:** Al Jazeera, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 932 | South China Morning Post | en | 2026-09-28 18:28 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says | US President Donald Trump’s administration was set to grant a limited waiver to its Iran sanctions programme on Monday to allow for flights carrying Shiite Muslim religious pilgrims between Iran and … |
| 952 | Al Jazeera | en | 2026-09-28 18:50 | Flights between Iraq’s Najaf and Iran resumed as Tehran protests US curbs | Tehran filed a UN complaint against US sanctions forcing regional cancellations of Iran flights. |
| 1008 | Al Jazeera | en | 2026-09-29 00:00 | Iran war live: Trump says he did not offer Tehran sanctions relief | US President Trump rejects a news report claiming his administration offered Iran sanctions relief and frozen funds. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| US | GPE | yes | 5 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says US President Donald Trump’s administration was set to grant a lim… |
| Iran | GPE | yes | 8 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says US President Donald Trump’s administration was set to grant a lim… |
| Iraq | GPE | yes | 4 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says US President Donald Trump’s administration was set to grant a lim… |
| Najaf | GPE | yes | 3 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says US President Donald Trump’s administration was set to grant a lim… |
| Donald Trump | PERSON | yes | 1 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says US President Donald Trump’s administration was set to grant a lim… |
| Monday | DATE | no (label not stored) | 1 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says US President Donald Trump’s administration was set to grant a lim… |
| Shiite Muslim | NORP | yes | 1 | US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says US President Donald Trump’s administration was set to grant a lim… |
| the US Treasury Department | ORG | yes | 1 | The source, who is involved ‌in the deliberations, said the US Treasury Department waiver would allow Iraqi Airways to fly back and forth between Ira… |
| Iraqi Airways | ORG | yes | 1 | The source, who is involved ‌in the deliberations, said the US Treasury Department waiver would allow Iraqi Airways to fly back and forth between Ira… |
| Shiite | NORP | yes | 1 | The source, who is involved ‌in the deliberations, said the US Treasury Department waiver would allow Iraqi Airways to fly back and forth between Ira… |
| one month | DATE | no (label not stored) | 1 | The source, who is involved ‌in the deliberations, said the US Treasury Department waiver would allow Iraqi Airways to fly back and forth between Ira… |
| Tehran | GPE | yes | 3 | Flights between Iraq’s Najaf and Iran resumed as Tehran protests US curbs Tehran filed a UN complaint against US sanctions forcing regional cancellat… |
| UN | ORG | yes | 1 | Flights between Iraq’s Najaf and Iran resumed as Tehran protests US curbs Tehran filed a UN complaint against US sanctions forcing regional cancellat… |
| Trump | PERSON | yes | 2 | Trump says he did not offer Tehran sanctions relief US President Trump rejects a news report claiming his administration offered Iran sanctions relie… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Iran | GPE | Iran | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Iraq | GPE | Iraq | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Najaf | GPE | Najaf | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| US | GPE | America | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Shiite | NORP | Shiite | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Shiite Muslim | NORP | Shiite Muslim | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Iraqi Airways | ORG | Iraqi Airways | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| UN | ORG | UN | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the US Treasury Department | ORG | the US Treasury Department | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Donald Trump | PERSON | Donald Trump | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Trump | PERSON | Trump | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | US | yes | — | united states → united states |
| title ×2 | Iran | yes | — | iran → iran |
| title ×2 | Iraq | yes | — | iraq → iraq |
| title ×2 | Najaf | no | place | najaf → najaf |
| lead ×3 | US | yes | — | united states → united states |
| lead ×1 | Donald Trump | yes | — | donald trump → united states |
| lead ×1 | Iran | no | topic / not a participant | iran → iran |
| lead ×1 | Shiite Muslim | no | common_noun | shiite muslim → shiite muslim |
| lead ×3 | Iran | yes | — | iran → iran |
| lead ×1 | Iraq | yes | — | iraq → iraq |
| title ×2 | Tehran | yes | — | iran → iran |
| lead ×1 | Tehran | yes | — | iran → iran |
| lead ×1 | UN | yes | — | un → un |
| title ×1 | Iran | no | topic / not a participant | iran → iran |
| title ×1 | Trump | yes | — | trump → united states |
| lead ×1 | Trump | yes | — | trump → united states |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): united states 3.0, iran 3.0, iraq 2.0, un 0.5
- **Final principal actors:** iran, iraq, united states
- **Entities flagged principal on the Development:** America, Iran, Iraq, Trump

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Iran | iran | country | — | yes |
| US | united states | country | — | yes |
| Iraq | iraq | country | — | yes |
| Najaf | najaf | sub-national | iraq | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| America | GPE | yes | yes | yes | yes | — | yes |
| Iran | GPE | yes | yes | yes | yes | — | yes |
| Iraq | GPE | yes | yes | yes | yes | — | yes |
| Trump | PERSON | yes | — | yes | yes | — | yes |
| Najaf | GPE | — | yes | — | — | — | — |
| Shiite | NORP | — | — | — | — | — | — |
| Shiite Muslim | NORP | — | — | — | — | — | — |
| Iraqi Airways | ORG | — | — | — | — | — | — |
| UN | ORG | — | — | — | — | — | — |
| the US Treasury Department | ORG | — | — | — | — | — | — |
| Donald Trump | PERSON | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: article/possessive kept in span: 'the US Treasury Department'

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 19. United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet

- **Development:** `ml#4` (db `entity-review-ml`)
- **Domain / type:** economic / sanctions
- **Items:** 3; **sources:** DW World, Kyiv Independent, State Department; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 152 | DW World | en | 2026-09-29 00:01 | US sanctions on Iran's aviation industry make travel less predictable as countries cancel flights | The threat of secondary US sanctions is putting pressure on airports, fuel suppliers and aviation companies that service Iranian airlines |
| 13 | State Department | en | 2026-09-29 17:32 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet | Office of the Spokesman |
| 279 | Kyiv Independent | en | 2026-09-30 02:28 | US imposes sanctions against Russian companies tied to Iran weapons procurement | The measures target 13 individuals and entities in Russia, Hong Kong, China, and Pakistan as the United States continues to exert economic pressure on Tehran under "Operation Economic Outcast" amid i… |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| US | GPE | yes | 3 | US sanctions on Iran's aviation industry make travel less predictable as countries cancel flights The threat of secondary US sanctions is putting pre… |
| Iran | GPE | yes | 8 | US sanctions on Iran's aviation industry make travel less predictable as countries cancel flights The threat of secondary US sanctions is putting pre… |
| Iranian | NORP | yes | 1 | US sanctions on Iran's aviation industry make travel less predictable as countries cancel flights The threat of secondary US sanctions is putting pre… |
| United States | ORG | yes | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| September 29 | DATE | no (label not stored) | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| Today | DATE | no (label not stored) | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| one-year | DATE | no (label not stored) | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| UN | ORG | yes | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| the Department of State | ORG | yes | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| one | CARDINAL | no (label not stored) | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| two | CARDINAL | no (label not stored) | 1 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| Russia | GPE | yes | 2 | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet Office of the Spokesman United States Disrupts… |
| Russian | NORP | yes | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |
| 13 | CARDINAL | no (label not stored) | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |
| Hong Kong | GPE | yes | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |
| China | GPE | yes | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |
| Pakistan | GPE | yes | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |
| the United States | GPE | yes | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |
| Tehran | GPE | yes | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |
| months-long war | DATE | no (label not stored) | 1 | US imposes sanctions against Russian companies tied to Iran weapons procurement The measures target 13 individuals and entities in Russia, Hong Kong,… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| China | GPE | China | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| E.O. | GPE | E.O. | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Hong Kong | GPE | Hong Kong | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Iran | GPE | Iran | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| Irkutsk | GPE | Irkutsk | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Pakistan | GPE | Pakistan | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Russia | GPE | Russia | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Russian | GPE | Russia | exact alias | 'Russian' is a recorded name of 'Russia' | 2 | | | | | | |
| US | GPE | U.S. | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| United States | GPE | U.S. | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the United States | GPE | U.S. | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Iranian | NORP | Iranian | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| E.O. 13949 | ORG | E.O. 13949 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Executive Order | ORG | Executive Order | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Islamic Revolutionary Guard Corps | ORG | IRGC | seeded (entities.yaml) | 'Islamic Revolutionary Guard Corps' is a recorded name of 'IRGC' | 1 | | | | | | |
| Justice | ORG | Justice | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| LLC | ORG | LLC | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Ministry of Defense and Armed Forces Logistics | ORG | Ministry of Defense and Armed Forces Logistics | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| The Department of the Treasury | ORG | The Department of the Treasury | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| The U.S. Department of State’s Rewards | ORG | The U.S. Department of State’s Rewards | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| U.S.-designated Foreign Terrorist Organization | ORG | U.S.-designated Foreign Terrorist Organization | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| UN | ORG | UN | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| YAKOVLEV | ORG | YAKOVLEV | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Yak-130 | ORG | Yak-130 | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the Department of State | ORG | Department of War | exact alias | 'the Department of State' is a recorded name of 'Department of War' | 1 | | | | | | |
| the Government of Iran | ORG | the Government of Iran | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| A.S. YAKOVLEV | PERSON | A.S. YAKOVLEV | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Kompozitor Rakhmaninov | PERSON | Kompozitor Rakhmaninov | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| MG-FLOT LIMITED LIABILITY COMPANY | PRODUCT | MG-FLOT LIMITED LIABILITY COMPANY | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | US | yes | — | united states → united states |
| title ×2 | Iran | yes | — | iran → iran |
| lead ×1 | US | yes | — | united states → united states |
| lead ×1 | Iranian | yes | — | iran → iran |
| title ×1 | United States | yes | — | united states → united states |
| lead ×1 | Office of the Spokesman | yes | — | office of the spokesman → office of the spokesman |
| title ×1 | Russian | yes | — | russia → russia |
| title ×1 | Iran | no | topic / not a participant | iran → iran |
| lead ×1 | Russia | no | topic / not a participant | russia → russia |
| lead ×1 | Hong Kong | no | place | hong kong → hong kong |
| lead ×1 | China | no | topic / not a participant | china → china |
| lead ×1 | Pakistan | no | topic / not a participant | pakistan → pakistan |
| lead ×1 | the United States | yes | — | united states → united states |
| lead ×1 | Tehran | yes | — | iran → iran |
| lead ×1 | Iran | yes | — | iran → iran |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): united states 3.0, iran 2.5, russia 1.0, office of the spokesman 0.5
- **Final principal actors:** iran, united states
- **Entities flagged principal on the Development:** Iran, Iranian, U.S.

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| US | united states | country | — | yes |
| Iran | iran | country | — | yes |
| the United States | united states | country | — | yes |
| United States | united states | country | — | yes |
| E.O. | e.o | not in gazetteer | — | no |
| Russia | russia | country | — | yes |
| Russian | russian | not in gazetteer | — | yes |
| Irkutsk | irkutsk | not in gazetteer | — | no |
| China | china | country | — | no |
| Hong Kong | hong kong | sub-national | china | no |
| Pakistan | pakistan | country | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Iran | GPE | yes | yes | yes | yes | — | yes |
| U.S. | GPE | yes | yes | yes | yes | — | yes |
| Iranian | NORP | yes | — | yes | yes | — | yes |
| China | GPE | — | yes | — | — | — | — |
| E.O. | GPE | — | yes | — | — | — | — |
| Hong Kong | GPE | — | yes | — | — | — | — |
| Irkutsk | GPE | — | yes | — | — | — | — |
| Pakistan | GPE | — | yes | — | — | — | — |
| Russia | GPE | — | yes | — | — | — | — |
| Department of War | ORG | — | — | — | — | — | — |
| E.O. 13949 | ORG | — | — | — | — | — | — |
| Executive Order | ORG | — | — | — | — | — | — |
| IRGC | ORG | — | — | — | — | — | — |
| Justice | ORG | — | — | — | — | — | — |
| LLC | ORG | — | — | — | — | — | — |
| Ministry of Defense and Armed Forces Logistics | ORG | — | — | — | — | — | — |
| The Department of the Treasury | ORG | — | — | — | — | — | — |
| The U.S. Department of State’s Rewards | ORG | — | — | — | — | — | — |
| U.S.-designated Foreign Terrorist Organization | ORG | — | — | — | — | — | — |
| UN | ORG | — | — | — | — | — | — |
| YAKOVLEV | ORG | — | — | — | — | — | — |
| Yak-130 | ORG | — | — | — | — | — | — |
| the Government of Iran | ORG | — | — | — | — | — | — |
| A.S. YAKOVLEV | PERSON | — | — | — | — | — | — |
| Kompozitor Rakhmaninov | PERSON | — | — | — | — | — | — |
| MG-FLOT LIMITED LIABILITY COMPANY | PRODUCT | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: article/possessive kept in span: 'the United States'
- **NER detection**: article/possessive kept in span: 'the Department of State'
- **NER detection**: article/possessive kept in span: 'The U.S. Department of State’s Rewards'
- **NER detection**: article/possessive kept in span: 'The Department of the Treasury'
- **NER detection**: article/possessive kept in span: 'the Government of Iran'

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

---

# Humanitarian

## 20. Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland

- **Development:** `en#56` (db `entity-review-en`)
- **Domain / type:** unknown / unknown — sampled as **humanitarian** (fallback)
- **Items:** 5; **sources:** Al Jazeera, BBC World, South China Morning Post; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 1066 | BBC World | en | 2026-09-29 06:06 | Malaysia begins controversial repatriation of asylum seekers to Myanmar | Human rights groups say some 5,000 returnees could face violence, persecution and forced conscription. |
| 1045 | South China Morning Post | en | 2026-09-29 07:00 | Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland | Malaysia began an operation to send nearly 1,500 Myanmar nationals back to their war-torn homeland on Tuesday, pressing ahead with a government-to-government repatriation deal despite warnings that r… |
| 1094 | Al Jazeera | en | 2026-09-29 09:27 | Malaysia begins sending back Rohingya refugees despite safety warnings | About 1,500 refugees are to be sent back in the first phase, despite criticism from rights groups. |
| 1116 | Al Jazeera | en | 2026-09-29 11:22 | Malaysia gave refuge to Rohingya; now it wants them to go | Malaysia welcomed persecuted Muslim minority but now plans to send them back to Myanmar amid rising hate against them. |
| 1125 | Al Jazeera | en | 2026-09-29 12:08 | Malaysia sends Rohingya back to Myanmar despite safety warnings | Malaysia sends Rohingya back to Myanmar despite safety warnings |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Malaysia | GPE | yes | 8 | Malaysia begins controversial repatriation of asylum seekers to Myanmar Human rights groups say some 5,000 returnees could face violence, persecution… |
| Myanmar | GPE | yes | 6 | Malaysia begins controversial repatriation of asylum seekers to Myanmar Human rights groups say some 5,000 returnees could face violence, persecution… |
| some 5,000 | CARDINAL | no (label not stored) | 1 | Malaysia begins controversial repatriation of asylum seekers to Myanmar Human rights groups say some 5,000 returnees could face violence, persecution… |
| thousands | CARDINAL | no (label not stored) | 1 | Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland Malaysia began an operation to send nearly 1,500 Myanmar nationals b… |
| nearly 1,500 | CARDINAL | no (label not stored) | 1 | Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland Malaysia began an operation to send nearly 1,500 Myanmar nationals b… |
| Tuesday | DATE | no (label not stored) | 1 | Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland Malaysia began an operation to send nearly 1,500 Myanmar nationals b… |
| first | ORDINAL | no (label not stored) | 2 | The first group of 1,476 is part of an agreement to return 5,000 people held in Malaysian immigration facilities under a programme Kuala Lumpur descr… |
| 1,476 | CARDINAL | no (label not stored) | 1 | The first group of 1,476 is part of an agreement to return 5,000 people held in Malaysian immigration facilities under a programme Kuala Lumpur descr… |
| 5,000 | CARDINAL | no (label not stored) | 1 | The first group of 1,476 is part of an agreement to return 5,000 people held in Malaysian immigration facilities under a programme Kuala Lumpur descr… |
| Malaysian | NORP | yes | 1 | The first group of 1,476 is part of an agreement to return 5,000 people held in Malaysian immigration facilities under a programme Kuala Lumpur descr… |
| Kuala Lumpur | GPE | yes | 1 | The first group of 1,476 is part of an agreement to return 5,000 people held in Malaysian immigration facilities under a programme Kuala Lumpur descr… |
| About 1,500 | CARDINAL | no (label not stored) | 1 | Malaysia begins sending back Rohingya refugees despite safety warnings About 1,500 refugees are to be sent back in the first phase, despite criticism… |
| Rohingya | ORG | yes | 3 | Malaysia gave refuge to Rohingya; now it wants them to go Malaysia welcomed persecuted Muslim minority but now plans to send them back to Myanmar ami… |
| Muslim | NORP | yes | 1 | Malaysia gave refuge to Rohingya; now it wants them to go Malaysia welcomed persecuted Muslim minority but now plans to send them back to Myanmar ami… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Kuala Lumpur | GPE | Kuala Lumpur | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Malaysia | GPE | Malaysia | new entity | no existing match: the mention created this entity | 5 | | | | | | |
| Malaysian | GPE | Malaysia | exact alias | 'Malaysian' is a recorded name of 'Malaysia' | 1 | | | | | | |
| Myanmar | GPE | Myanmar | new entity | no existing match: the mention created this entity | 4 | | | | | | |
| Muslim | NORP | Muslims | exact alias | 'Muslim' is a recorded name of 'Muslims' | 1 | | | | | | |
| Rohingya | ORG | Rohingya | new entity | no existing match: the mention created this entity | 2 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×5 | Malaysia | yes | — | malaysia → malaysia |
| title ×2 | Myanmar | no | topic / not a participant | myanmar → myanmar |
| title ×1 | Myanmar | yes | — | myanmar → myanmar |
| lead ×3 | Malaysia | yes | — | malaysia → malaysia |
| lead ×1 | Myanmar | yes | — | myanmar → myanmar |
| title ×1 | Rohingya | no | topic / not a participant | rohingya → rohingya |
| lead ×1 | Muslim | no | common_noun | muslim → muslim |
| lead ×2 | Myanmar | no | topic / not a participant | myanmar → myanmar |
| title ×1 | Rohingya | yes | — | rohingya → rohingya |
| lead ×1 | Rohingya | yes | — | rohingya → rohingya |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): malaysia 5.0, myanmar 1.0, rohingya 1.0
- **Final principal actors:** malaysia
- **Entities flagged principal on the Development:** Malaysia

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Malaysia | malaysia | country | — | yes |
| Myanmar | myanmar | country | — | yes |
| Malaysian | malaysian | not in gazetteer | — | yes |
| Kuala Lumpur | kuala lumpur | sub-national | malaysia | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Malaysia | GPE | yes | yes | yes | yes | — | yes |
| Kuala Lumpur | GPE | — | yes | — | — | — | — |
| Myanmar | GPE | — | yes | — | — | — | — |
| Muslims | NORP | — | — | — | — | — | — |
| Rohingya | ORG | — | — | — | — | — | — |

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 21. World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update

- **Development:** `ml#15` (db `entity-review-ml`)
- **Domain / type:** unknown / unknown — sampled as **humanitarian** (fallback)
- **Items:** 2; **sources:** DW World, UN News; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 150 | DW World | en | 2026-09-29 10:26 | Malaysia repatriates Myanmar migrants despite UN warnings | Malaysia has started repatriating about 1,500 Myanmar nationals, defying warnings from the UN and rights groups |
| 396 | UN News | en | 2026-09-29 12:00 | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update | The UN chief on Tuesday strongly condemned an airstrike that reportedly killed at least 50 people at a market in Myanmar’s Rakhine state and called for those responsible to be held to account. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Malaysia | GPE | yes | 4 | Malaysia repatriates Myanmar migrants despite UN warnings Malaysia has started repatriating about 1,500 Myanmar nationals, defying warnings from the … |
| Myanmar | GPE | yes | 4 | Malaysia repatriates Myanmar migrants despite UN warnings Malaysia has started repatriating about 1,500 Myanmar nationals, defying warnings from the … |
| UN | ORG | yes | 3 | Malaysia repatriates Myanmar migrants despite UN warnings Malaysia has started repatriating about 1,500 Myanmar nationals, defying warnings from the … |
| about 1,500 | CARDINAL | no (label not stored) | 1 | Malaysia repatriates Myanmar migrants despite UN warnings Malaysia has started repatriating about 1,500 Myanmar nationals, defying warnings from the … |
| World News | ORG | yes | 1 | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update The UN chief o… |
| Gaza | GPE | yes | 1 | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update The UN chief o… |
| West Bank | GPE | yes | 1 | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update The UN chief o… |
| Tuesday | DATE | no (label not stored) | 1 | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update The UN chief o… |
| at least 50 | CARDINAL | no (label not stored) | 1 | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update The UN chief o… |
| Rakhine | NORP | yes | 1 | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update The UN chief o… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Gaza | GPE | Gaza | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Malaysia | GPE | Malaysia | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Myanmar | GPE | Myanmar | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| West Bank | GPE | West Bank | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Rakhine | NORP | Rakhine | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| UN | ORG | UN | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| World News | ORG | World News | new entity | no existing match: the mention created this entity | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | Malaysia | yes | — | malaysia → malaysia |
| title ×2 | Myanmar | yes | — | myanmar → myanmar |
| title ×1 | UN | no | topic / not a participant | un → un |
| lead ×1 | Malaysia | yes | — | malaysia → malaysia |
| lead ×1 | Myanmar | yes | — | myanmar → myanmar |
| lead ×1 | UN | no | topic / not a participant | un → un |
| title ×1 | World News | yes | — | world news → world news |
| title ×1 | Gaza | yes | — | gaza → gaza |
| title ×1 | West Bank | no | place | west bank → west bank |
| lead ×1 | UN | yes | — | un → un |
| lead ×1 | Myanmar | no | topic / not a participant | myanmar → myanmar |
| lead ×1 | Rakhine | no | topic / not a participant | rakhine → rakhine |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): myanmar 2.0, malaysia 2.0, gaza 1.0, world news 1.0, un 0.5
- **Final principal actors:** gaza, malaysia, myanmar, world news
- **Entities flagged principal on the Development:** Gaza, Malaysia, Myanmar, World News

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Malaysia | malaysia | country | — | yes |
| Myanmar | myanmar | country | — | yes |
| Gaza | gaza | sub-national | palestine | yes |
| West Bank | west bank | sub-national | palestine | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Gaza | GPE | yes | yes | yes | yes | — | yes |
| Malaysia | GPE | yes | yes | yes | yes | — | yes |
| Myanmar | GPE | yes | yes | yes | yes | — | yes |
| World News | ORG | yes | — | yes | yes | — | yes |
| West Bank | GPE | — | yes | — | — | — | — |
| Rakhine | NORP | — | — | — | — | — | — |
| UN | ORG | — | — | — | — | — | — |

### ⚑ Automatic flags

- **location/actor confusion** (principal): principal 'gaza' comes from place mentions (GPE)
- **contextual organisation** (principal): principal 'world news' is a media outlet / programme name

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

---

# Institutional

## 22. US court upholds Pentagon’s blacklisting of Anthropic

- **Development:** `en#16` (db `entity-review-en`)
- **Domain / type:** unknown / unknown — sampled as **institutional** (fallback)
- **Items:** 3; **sources:** Al Jazeera, Breaking Defense, Defense News; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 390 | Al Jazeera | en | 2026-09-25 17:03 | US court upholds Pentagon’s blacklisting of Anthropic | Conflict began in February when Anthropic refused to remove restrictions on use of Claude for fully autonomous weapons. |
| 421 | Defense News | en | 2026-09-25 19:19 | US appeals court upholds Pentagon’s blacklisting of Anthropic | A federal appeals court on Friday upheld the Pentagon’s blacklisting of Anthropic from military contracts, handing a victory to President Donald Trump and Defense Secretary Pete Hegseth in their batt… |
| 429 | Breaking Defense | en | 2026-09-25 19:50 | DC Circuit panel upholds Pentagon’s ban on Anthropic – so what comes next? | Pentagon CTO Emil Michael crowed “The hammer of justice has smashed AnthropicAI[’s] arguments.” The AI titan hinted at an appeal — but they may not be allowed one. |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| US | GPE | yes | 2 | US court upholds Pentagon’s blacklisting of Anthropic Conflict began in February when Anthropic refused to remove restrictions on use of Claude for f… |
| Pentagon | ORG | yes | 6 | US court upholds Pentagon’s blacklisting of Anthropic Conflict began in February when Anthropic refused to remove restrictions on use of Claude for f… |
| Anthropic Conflict | ORG | yes | 1 | US court upholds Pentagon’s blacklisting of Anthropic Conflict began in February when Anthropic refused to remove restrictions on use of Claude for f… |
| February | DATE | no (label not stored) | 1 | US court upholds Pentagon’s blacklisting of Anthropic Conflict began in February when Anthropic refused to remove restrictions on use of Claude for f… |
| Claude | PERSON | yes | 1 | US court upholds Pentagon’s blacklisting of Anthropic Conflict began in February when Anthropic refused to remove restrictions on use of Claude for f… |
| Friday | DATE | no (label not stored) | 1 | US appeals court upholds Pentagon’s blacklisting of Anthropic A federal appeals court on Friday upheld the Pentagon’s blacklisting of Anthropic from … |
| Donald Trump | PERSON | yes | 1 | US appeals court upholds Pentagon’s blacklisting of Anthropic A federal appeals court on Friday upheld the Pentagon’s blacklisting of Anthropic from … |
| Defense | ORG | yes | 1 | US appeals court upholds Pentagon’s blacklisting of Anthropic A federal appeals court on Friday upheld the Pentagon’s blacklisting of Anthropic from … |
| Pete Hegseth | PERSON | yes | 1 | US appeals court upholds Pentagon’s blacklisting of Anthropic A federal appeals court on Friday upheld the Pentagon’s blacklisting of Anthropic from … |
| AI | ORG | yes | 2 | US appeals court upholds Pentagon’s blacklisting of Anthropic A federal appeals court on Friday upheld the Pentagon’s blacklisting of Anthropic from … |
| 2 | CARDINAL | no (label not stored) | 1 | The 2-1 decision by the U.S. Court of Appeals in Washington came in a lawsuit by Anthropic challenging its March designation by the Pentagon as a nat… |
| the U.S. Court of Appeals | ORG | yes | 1 | The 2-1 decision by the U.S. Court of Appeals in Washington came in a lawsuit by Anthropic challenging its March designation by the Pentagon as a nat… |
| Washington | GPE | yes | 1 | The 2-1 decision by the U.S. Court of Appeals in Washington came in a lawsuit by Anthropic challenging its March designation by the Pentagon as a nat… |
| March | DATE | no (label not stored) | 1 | The 2-1 decision by the U.S. Court of Appeals in Washington came in a lawsuit by Anthropic challenging its March designation by the Pentagon as a nat… |
| billions of dollars | MONEY | no (label not stored) | 1 | The 2-1 decision by the U.S. Court of Appeals in Washington came in a lawsuit by Anthropic challenging its March designation by the Pentagon as a nat… |
| DC Circuit | ORG | yes | 1 | DC Circuit panel upholds Pentagon’s ban on Anthropic – so what comes next? Pentagon CTO Emil Michael crowed “The hammer of justice has smashed Anthro… |
| Emil Michael | PERSON | yes | 1 | DC Circuit panel upholds Pentagon’s ban on Anthropic – so what comes next? Pentagon CTO Emil Michael crowed “The hammer of justice has smashed Anthro… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| San Francisco | GPE | San Francisco | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| US | GPE | America | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| American | NORP | American | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| AI | ORG | AI | new entity | no existing match: the mention created this entity | 2 | | | | | | |
| Anthropic | ORG | Anthropic | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Anthropic Conflict | ORG | Anthropic Conflict | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| DC Circuit | ORG | DC Circuit | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Defense | ORG | Defense | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Pentagon | ORG | the Department of Defense | new entity | no existing match: the mention created this entity | 3 | | | | | | |
| The White House | ORG | White House | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the U.S. Court of Appeals | ORG | the U.S. Court of Appeals | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Claude | PERSON | Claude | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Donald Trump | PERSON | Donald Trump | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Emil Michael | PERSON | Emil Michael | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Gregory Katsas | PERSON | Gregory Katsas | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Hegseth | PERSON | Hegseth | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Pete Hegseth | PERSON | Pete Hegseth | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Rita Lin | PERSON | Rita Lin | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Trump | PERSON | Trump | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Anthropic Conflict | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×2 | US | yes | — | united states → united states |
| title ×3 | Pentagon | yes | — | department of defense → united states |
| lead ×1 | Claude | yes | — | claude → claude |
| lead ×2 | Pentagon | yes | — | department of defense → united states |
| lead ×1 | Donald Trump | no | topic / not a participant | donald trump → united states |
| lead ×1 | Defense | no | topic / not a participant | defense → defense |
| lead ×1 | Pete Hegseth | no | topic / not a participant | pete hegseth → united states |
| lead ×2 | AI | yes | — | non-actor (dropped) |
| lead ×1 | U.S | yes | — | united states → united states |
| title ×1 | DC Circuit | yes | — | dc circuit → dc circuit |
| lead ×1 | CTO Emil Michael | yes | — | cto emil michael → cto emil michael |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.5): united states 3.0, dc circuit 1.0, claude 0.5, cto emil michael 0.5
- **Final principal actors:** united states
- **Entities flagged principal on the Development:** America, American, the Department of Defense

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| US | united states | country | — | yes |
| San Francisco | san francisco | sub-national | california, united states | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| America | GPE | yes | yes | yes | yes | — | yes |
| American | NORP | yes | — | yes | yes | — | yes |
| the Department of Defense | ORG | yes | — | yes | yes | — | yes |
| San Francisco | GPE | — | yes | — | — | — | — |
| AI | ORG | — | — | — | — | — | — |
| Anthropic | ORG | — | — | — | — | — | — |
| Anthropic Conflict | ORG | — | — | — | — | — | — |
| DC Circuit | ORG | — | — | — | — | — | — |
| Defense | ORG | — | — | — | — | — | — |
| White House | ORG | — | — | — | — | — | — |
| the U.S. Court of Appeals | ORG | — | — | — | — | — | — |
| Claude | PERSON | — | — | — | — | — | — |
| Donald Trump | PERSON | — | — | — | — | — | — |
| Emil Michael | PERSON | — | — | — | — | — | — |
| Gregory Katsas | PERSON | — | — | — | — | — | — |
| Hegseth | PERSON | — | — | — | — | — | — |
| Pete Hegseth | PERSON | — | — | — | — | — | — |
| Rita Lin | PERSON | — | — | — | — | — | — |
| Trump | PERSON | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: malformed span 'Anthropic Conflict' (ORG)
- **NER detection**: article/possessive kept in span: 'The White House'
- **NER detection**: article/possessive kept in span: 'the U.S. Court of Appeals'

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 23. Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza'

- **Development:** `ml#8` (db `entity-review-ml`)
- **Domain / type:** unknown / unknown — sampled as **institutional** (fallback)
- **Items:** 10; **sources:** ANSA Mondo, Clarín Mundo, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri; **languages:** es, it

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 238 | Il Sole 24 Ore Mondo | it | 2026-09-29 19:04 | Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence | Pranzo alla Casa Bianca con decine di protagonisti dell’intelligenza artificiale americana per inaugurare la nuova era della Super Intelligenza |
| 132 | Rai News Esteri | it | 2026-09-29 20:36 | Trump incontra i vertici Big Tech sulla sicurezza AI: "Autoregolazione e nessun controllo federale" | Un impegno "moralmente vincolante" a predisporre misure di salvaguardia |
| 57 | ANSA Mondo | it | 2026-09-29 20:36 | Trump, 'da vertici big tech impegno moralmente vincolante su sicurezza IA' | 'Si autoregoleranno' |
| 267 | Clarín Mundo | es | 2026-09-29 20:42 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA | • "Van a autorregularse", declaró al término de la reunión llevada a cabo este martes. |
| 55 | ANSA Mondo | it | 2026-09-29 21:20 | Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA' | 'Se i modelli di IA non verranno usati a fin di bene, li bloccheremo' |
| 71 | Europa Press Internacional | es | 2026-09-29 23:02 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU | El presidente de Estados Unidos, Donald Trump, ha firmado este martes una orden ejecutiva por la que insta a todos los organismos del Gobierno federal sustituir el término "inteligencia artificial" y… |
| 129 | Rai News Esteri | it | 2026-09-29 23:05 | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" | “Controlli volontari finti, a rischio lavoro, concorrenza e sicurezza” |
| 131 | Rai News Esteri | it | 2026-09-29 23:32 | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia | Trump pranza con i leader del Big Tech tra progetti sull'AI, mentre la Corte Suprema sblocca i piani di deportazione dei migranti |
| 48 | ANSA Mondo | it | 2026-09-30 01:10 | Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza' | 'Sistemi di frontiera odierni vanno ben oltre singoli aspetti dell'intelligenza umana' |
| 176 | France 24 Español | es | 2026-09-30 03:29 | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" | El presidente Donald Trump anunció un acuerdo que calificó como “moralmente vinculante” junto a algunos de los principales líderes de la industria tecnológica |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Trump | ORG | yes | 4 | Trump, per Ai solo autoregolamentazione. |
| Super Intelligence | ORG | yes | 1 | Firmato l’ordine che cambia il nome in Super Intelligence Pranzo alla Casa Bianca con decine di protagonisti dell’intelligenza artificiale americana … |
| artificiale americana | ORG | yes | 1 | Firmato l’ordine che cambia il nome in Super Intelligence Pranzo alla Casa Bianca con decine di protagonisti dell’intelligenza artificiale americana … |
| la nuova | ORG | yes | 1 | Firmato l’ordine che cambia il nome in Super Intelligence Pranzo alla Casa Bianca con decine di protagonisti dell’intelligenza artificiale americana … |
| della Super Intelligenza | ORG | yes | 1 | Firmato l’ordine che cambia il nome in Super Intelligence Pranzo alla Casa Bianca con decine di protagonisti dell’intelligenza artificiale americana … |
| Nessuna menzione di rischi | PERSON | yes | 1 | Nessuna menzione di rischi, crisi, e incidenti anche se forse nascerà un comitato consultivo di supervisione. |
| crisi | ORG | yes | 1 | Nessuna menzione di rischi, crisi, e incidenti anche se forse nascerà un comitato consultivo di supervisione. |
| forse nascerà un comitato consultivo di supervisione | ORG | yes | 1 | Nessuna menzione di rischi, crisi, e incidenti anche se forse nascerà un comitato consultivo di supervisione. |
| Big Tech | ORG | yes | 1 | Trump incontra i vertici Big Tech sulla sicurezza AI: "Autoregolazione e nessun controllo federale" Un impegno "moralmente vincolante" a predisporre … |
| Autoregolazione e nessun controllo | ORG | yes | 1 | Trump incontra i vertici Big Tech sulla sicurezza AI: "Autoregolazione e nessun controllo federale" Un impegno "moralmente vincolante" a predisporre … |
| Un | ORG | yes | 1 | Trump incontra i vertici Big Tech sulla sicurezza AI: "Autoregolazione e nessun controllo federale" Un impegno "moralmente vincolante" a predisporre … |
| Zuckerberg | PERSON | yes | 1 | Zuckerberg: "Controlli interni robusti". |
| Controlli interni robusti | ORG | yes | 1 | Zuckerberg: "Controlli interni robusti". |
| Un futuro di abbondanza | ORG | yes | 1 | Un futuro di abbondanza" |
| impegno moralmente vincolante su sicurezza IA' | PERSON | yes | 1 | Trump, 'da vertici big tech impegno moralmente vincolante su sicurezza IA' 'Si autoregoleranno' |
| Donald Trump | PERSON | yes | 3 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA • "Van a autorregularse", … |
| que los | ORG | yes | 1 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA • "Van a autorregularse", … |
| tecnológico firmaron un acuerdo | ORG | yes | 1 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA • "Van a autorregularse", … |
| la IA | GPE | yes | 1 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA • "Van a autorregularse", … |
| declaró al término de la | PERSON | yes | 1 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA • "Van a autorregularse", … |
| cabo este martes | GPE | yes | 1 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA • "Van a autorregularse", … |
| en la | ORG | yes | 1 | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA • "Van a autorregularse", … |
| Usa | GPE | yes | 1 | Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA' 'Se |
| 10 | CARDINAL | no (label not stored) | 1 | Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA' 'Se |
| li bloccheremo' | PERSON | yes | 1 | i modelli di IA non verranno usati a fin di bene, li bloccheremo' |
| Trump ordena | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| la ' | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| Inteligencia Artificial' | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| Súper Inteligencia' | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| El presidente de Estados Unidos | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| firmado este martes una orden | PERSON | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| por la que insta | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| del Gobierno | GPE | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| sustituir el término | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| por | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| oficial | ORG | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| documentos públicos | GPE | yes | 1 | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU El presidente de Estados Uni… |
| La medida | PERSON | yes | 1 | La medida, que no afecta a normas o contratos ya vigentes, otorga un plazo de 60 días al asesor presidencial para Ciencia y Tecnología para presentar… |
| que no afecta | ORG | yes | 1 | La medida, que no afecta a normas o contratos ya vigentes, otorga un plazo de 60 días al asesor presidencial para Ciencia y Tecnología para presentar… |
| un plazo de 60 días | ORG | yes | 1 | La medida, que no afecta a normas o contratos ya vigentes, otorga un plazo de 60 días al asesor presidencial para Ciencia y Tecnología para presentar… |
| presidencial para Ciencia | ORG | yes | 1 | La medida, que no afecta a normas o contratos ya vigentes, otorga un plazo de 60 días al asesor presidencial para Ciencia y Tecnología para presentar… |
| Tecnología para presentar una propuesta legislativa que est… | ORG | yes | 1 | La medida, que no afecta a normas o contratos ya vigentes, otorga un plazo de 60 días al asesor presidencial para Ciencia y Tecnología para presentar… |
| del nuevo término | ORG | yes | 1 | La medida, que no afecta a normas o contratos ya vigentes, otorga un plazo de 60 días al asesor presidencial para Ciencia y Tecnología para presentar… |
| di Big Tech | ORG | yes | 1 | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" “Controlli volontari finti, a rischio lavoro, concorrenza e … |
| Controlli | ORG | yes | 1 | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" “Controlli volontari finti, a rischio lavoro, concorrenza e … |
| concorrenza e sicurezza | ORG | yes | 1 | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" “Controlli volontari finti, a rischio lavoro, concorrenza e … |
| Da Sam Altman di | PERSON | yes | 1 | Da Sam Altman di OpenAI a Stanford, dal MIT ai sindacati ai pionieri dell'Intelligenza |
| Stanford | GPE | yes | 1 | Da Sam Altman di OpenAI a Stanford, dal MIT ai sindacati ai pionieri dell'Intelligenza |
| Artificiale, il coro dei no non è | ORG | yes | 1 | Artificiale, il coro dei no non è residuale |
| Donald Trump e la nuova | PERSON | yes | 1 | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia Trump pranza con i leader del Big Tech tra progetti sull'AI, mentre la Cor… |
| età | ORG | yes | 1 | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia Trump pranza con i leader del Big Tech tra progetti sull'AI, mentre la Cor… |
| del Big Tech tra progetti sull'AI | ORG | yes | 1 | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia Trump pranza con i leader del Big Tech tra progetti sull'AI, mentre la Cor… |
| Suprema | ORG | yes | 1 | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia Trump pranza con i leader del Big Tech tra progetti sull'AI, mentre la Cor… |
| piani di deportazione dei migranti | PERSON | yes | 1 | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia Trump pranza con i leader del Big Tech tra progetti sull'AI, mentre la Cor… |
| Trump firma | ORG | yes | 1 | Trump firma ordine esecutivo, 'inaugura l'era della |
| l'era della | ORG | yes | 1 | Trump firma ordine esecutivo, 'inaugura l'era della |
| ben oltre | PERSON | yes | 1 | Super Intelligenza' 'Sistemi di frontiera odierni vanno ben oltre singoli aspetti dell'intelligenza umana' |
| singoli aspetti | PERSON | yes | 1 | Super Intelligenza' 'Sistemi di frontiera odierni vanno ben oltre singoli aspetti dell'intelligenza umana' |
| umana | ORG | yes | 1 | Super Intelligenza' 'Sistemi di frontiera odierni vanno ben oltre singoli aspetti dell'intelligenza umana' |
| Trump y los gigantes de la | ORG | yes | 1 | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" El presidente Donald Trump anunció un acuerdo que califi… |
| sellan un acuerdo | ORG | yes | 1 | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" El presidente Donald Trump anunció un acuerdo que califi… |
| El presidente | GPE | yes | 1 | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" El presidente Donald Trump anunció un acuerdo que califi… |
| un acuerdo que calificó como | ORG | yes | 1 | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" El presidente Donald Trump anunció un acuerdo que califi… |
| algunos de los | ORG | yes | 1 | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" El presidente Donald Trump anunció un acuerdo que califi… |
| Los representantes de las compañías se | ORG | yes | 1 | Los representantes de las compañías se comprometieron a autorregularse en un momento de creciente preocupación por los riesgos asociados al rápido de… |
| en un momento de creciente | ORG | yes | 1 | Los representantes de las compañías se comprometieron a autorregularse en un momento de creciente preocupación por los riesgos asociados al rápido de… |
| por los riesgos asociados | ORG | yes | 1 | Los representantes de las compañías se comprometieron a autorregularse en un momento de creciente preocupación por los riesgos asociados al rápido de… |
| al rápido desarrollo de la | ORG | yes | 1 | Los representantes de las compañías se comprometieron a autorregularse en un momento de creciente preocupación por los riesgos asociados al rápido de… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Stanford | GPE | Stanford | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Usa | GPE | U.S. | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| cabo este martes | GPE | cabo este martes | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| del Gobierno | GPE | del governo | exact alias | 'del Gobierno' is a recorded name of 'del governo' | 1 | | | | | | |
| documentos públicos | GPE | documentos públicos | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| en la | GPE | en la | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Artificiale, il coro dei no non è | ORG | Artificiale, il coro dei no non è | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Autoregolazione e nessun controllo | ORG | Autoregolazione e nessun controllo | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Big Tech | ORG | di Big Tech | exact alias | 'Big Tech' is a recorded name of 'di Big Tech' | 1 | | | | | | |
| Controlli | ORG | Controlli | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Controlli interni robusti | ORG | Controlli interni robusti | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Inteligencia Artificial' | ORG | Inteligencia Artificial' | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Los representantes de las compañías se | ORG | Los representantes de las compañías se | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Super Intelligence Pranzo | ORG | Super Intelligence | fuzzy | best alias 'Super Intelligence' scored 84 (threshold 80) | 1 | | | | | | |
| Suprema | ORG | Suprema | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Súper Inteligencia' | ORG | Super Intelligence | exact alias | 'Súper Inteligencia'' is a recorded name of 'Super Intelligence' | 1 | | | | | | |
| Tecnología para presentar una propuesta legislativa que est… | ORG | Tecnología para presentar una propuesta legislativa que est… | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Trump firma | ORG | Trump firma | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Trump ordena | ORG | Trump ordena | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Trump y los gigantes de la | ORG | Trump y los gigantes de la | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Un | ORG | UN | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Un futuro di abbondanza | ORG | Un futuro di abbondanza | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| al rápido desarrollo de la | ORG | al rápido desarrollo de la | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| algunos de los | ORG | uno de los | exact alias | 'algunos de los' is a recorded name of 'uno de los' | 1 | | | | | | |
| artificiale americana | ORG | artificiale americana | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| concorrenza e sicurezza | ORG | concorrenza e sicurezza | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| crisi | ORG | crisi | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| del Big Tech tra progetti sull'AI | ORG | del Big Tech tra progetti sull'AI | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| del nuevo término | ORG | del nuevo término | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| della Super Intelligenza | ORG | l'era della Super Intelligenza' ' | exact alias | 'della Super Intelligenza' is a recorded name of 'l'era della Super Intelligenza' '' | 1 | | | | | | |
| di Big Tech | ORG | di Big Tech | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| en un momento de creciente | ORG | en un momento de creciente | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| età | ORG | età | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| forse nascerà un comitato consultivo di supervisione | ORG | forse nascerà un comitato consultivo di supervisione | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| l'era della Super Intelligenza' ' | ORG | l'era della Super Intelligenza' ' | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| la ' | ORG | la ' | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| la IA | ORG | la IA | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| la nuova | ORG | la nuova | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| oficial | ORG | oficial | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| por | ORG | por | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| por la que insta | ORG | por la que insta | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| por los riesgos asociados | ORG | por los riesgos asociados | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| presidencial para Ciencia | ORG | presidencial para Ciencia | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| que los | ORG | que los | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| que no afecta | ORG | que no afecta | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| sellan un acuerdo | ORG | sellan un acuerdo | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| sustituir el término | ORG | sustituir el término | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| tecnológico firmaron un acuerdo | ORG | tecnológico firmaron un acuerdo | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| umana | ORG | umana | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| un acuerdo que calificó como | ORG | un acuerdo que calificó como | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| un plazo de 60 días | ORG | un plazo de 60 días | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Da Sam Altman di | PERSON | Da Sam Altman di | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Donald Trump | PERSON | Donald J. Trump | exact alias | 'Donald Trump' is a recorded name of 'Donald J. Trump' | 2 | | | | | | |
| Donald Trump e la nuova | PERSON | Donald Trump e la nuova | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| El presidente Donald Trump | PERSON | El presidente Donald Trump | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| La medida | PERSON | La medida | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Nessuna menzione di rischi | PERSON | Nessuna menzione di rischi | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Sistemi di frontiera | PERSON | Sistemi di frontiera | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Trump | PERSON | Trump | new entity | no existing match: the mention created this entity | 5 | | | | | | |
| Zuckerberg | PERSON | Zuckerberg | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| ben oltre | PERSON | ben oltre | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| declaró al término de la | PERSON | declaró al término de la | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| firmado este martes una orden | PERSON | firmado este martes una orden | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| impegno moralmente vincolante su sicurezza IA' ' | PERSON | impegno moralmente vincolante su sicurezza IA' ' | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| li bloccheremo' | PERSON | li bloccheremo' | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| piani di deportazione dei migranti | PERSON | piani di deportazione dei migranti | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| singoli aspetti | PERSON | singoli aspetti | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| El presidente | GPE | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| El presidente de Estados Unidos | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| Super Intelligence | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| l'era della | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| Donald Trump | PERSON | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| impegno moralmente vincolante su sicurezza IA' | PERSON | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×3 | Trump | yes | — | trump → united states |
| title ×1 | Super Intelligence | no | topic / not a participant | super intelligence → super intelligence |
| lead ×1 | Pranzo alla Casa | yes | — | pranzo alla casa → pranzo alla casa |
| lead ×1 | artificiale americana | no | common_noun | artificiale americana → artificiale americana |
| lead ×1 | la nuova | no | topic / not a participant | la nuova → la nuova |
| lead ×1 | della Super Intelligenza | yes | — | della super intelligenza → della super intelligenza |
| title ×1 | Trump | no | topic / not a participant | trump → united states |
| title ×1 | Big Tech | yes | — | big tech → big tech |
| title ×1 | Autoregolazione e nessun controllo | yes | — | autoregolazione e nessun controllo → autoregolazione e nessun control… |
| lead ×1 | Un | yes | — | un → un |
| title ×1 | impegno moralmente vincolante su sicurezza IA' | yes | — | impegno moralmente vincolante su sicurezza ia → impegno moralmente vi… |
| title ×1 | Donald Trump | yes | — | donald trump → united states |
| title ×1 | que los | yes | — | que los → que los |
| title ×1 | tecnológico firmaron un acuerdo | yes | — | tecnológico firmaron un acuerdo → tecnológico firmaron un acuerdo |
| title ×1 | la IA | no | topic / not a participant | la ia → la ia |
| lead ×1 | declaró al término de la | yes | — | declaró al término de la → declaró al término de la |
| lead ×1 | cabo este martes | yes | — | cabo este martes → cabo este martes |
| title ×1 | Usa | yes | — | united states → united states |
| lead ×1 | li bloccheremo' | yes | — | li bloccheremo → li bloccheremo |
| title ×1 | Trump ordena | yes | — | trump ordena → trump ordena |
| title ×1 | la ' | yes | — | la → la |
| title ×1 | Inteligencia Artificial' | yes | — | inteligencia artificial → inteligencia artificial |
| title ×1 | Súper Inteligencia' | yes | — | súper inteligencia → súper inteligencia |
| lead ×1 | El presidente de Estados Unidos | yes | — | el presidente de estados unidos → el presidente de estados unidos |
| lead ×1 | Donald Trump | yes | — | donald trump → united states |
| lead ×1 | firmado este martes una orden | yes | — | firmado este martes una orden → firmado este martes una orden |
| lead ×1 | por la que insta | yes | — | por la que insta → por la que insta |
| lead ×1 | del Gobierno | yes | — | del gobierno → del gobierno |
| lead ×1 | sustituir el término | yes | — | sustituir el término → sustituir el término |
| lead ×1 | por | no | common_noun | por → por |
| lead ×1 | oficial | yes | — | oficial → oficial |
| lead ×1 | documentos públicos | no | common_noun | documentos públicos → documentos públicos |
| title ×1 | di Big Tech | yes | — | di big tech → di big tech |
| lead ×1 | Controlli | yes | — | controlli → controlli |
| lead ×1 | concorrenza e sicurezza | yes | — | concorrenza e sicurezza → concorrenza e sicurezza |
| title ×1 | Donald Trump e la nuova | yes | — | donald trump e la nuova → donald trump e la nuova |
| title ×1 | età | yes | — | età → età |
| lead ×1 | Trump | yes | — | trump → united states |
| lead ×1 | del Big Tech tra progetti sull'AI | yes | — | del big tech tra progetti sull'ai → del big tech tra progetti sull'ai |
| lead ×1 | Suprema | yes | — | suprema → suprema |
| lead ×1 | piani di deportazione dei migranti | yes | — | piani di deportazione dei migranti → piani di deportazione dei migran… |
| title ×1 | Trump firma | yes | — | trump firma → trump firma |
| title ×1 | l'era della | yes | — | l'era della → l'era della |
| lead ×1 | Sistemi di frontiera | no | topic / not a participant | sistemi di frontiera → sistemi di frontiera |
| lead ×1 | ben oltre | no | topic / not a participant | ben oltre → ben oltre |
| lead ×1 | singoli aspetti | no | topic / not a participant | singoli aspetti → singoli aspetti |
| lead ×1 | umana | yes | — | umana → umana |
| title ×1 | Trump y los gigantes de la | yes | — | trump y los gigantes de la → trump y los gigantes de la |
| title ×1 | sellan un acuerdo | no | topic / not a participant | sellan un acuerdo → sellan un acuerdo |
| lead ×1 | El presidente Donald Trump | yes | — | el presidente donald trump → el presidente donald trump |
| lead ×1 | un acuerdo que calificó como | yes | — | un acuerdo que calificó como → un acuerdo que calificó como |
| lead ×1 | algunos de los | yes | — | algunos de los → algunos de los |
| lead ×1 | tecnológica | yes | — | tecnológica → tecnológica |

- **Support per actor** (headline 1.0, lead 0.5; needed 2.5): united states 5.0, big tech 1.0, autoregolazione e nessun controllo 1.0, impegno moralmente vincolante su sicurezza ia 1.0, tecnológico firmaron un acuerdo 1.0, que los 1.0, inteligencia artificial 1.0, trump ordena 1.0, la 1.0, súper inteligencia 1.0, di big tech 1.0, donald trump e la nuova 1.0, età 1.0, trump firma 1.0, l'era della 1.0, trump y los gigantes de la 1.0, della super intelligenza 0.5, pranzo alla casa 0.5, un 0.5, declaró al término de la 0.5, cabo este martes 0.5, li bloccheremo 0.5, del gobierno 0.5, firmado este martes una orden 0.5, por la que insta 0.5, sustituir el término 0.5, oficial 0.5, el presidente de estados unidos 0.5, concorrenza e sicurezza 0.5, controlli 0.5, del big tech tra progetti sull'ai 0.5, piani di deportazione dei migranti 0.5, suprema 0.5, umana 0.5, el presidente donald trump 0.5, un acuerdo que calificó como 0.5, algunos de los 0.5, tecnológica 0.5
- **Final principal actors:** united states
- **Entities flagged principal on the Development:** Trump, U.S.

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| en la | en la | not in gazetteer | — | no |
| cabo este martes | cabo este martes | not in gazetteer | — | yes |
| Usa | united states | country | — | yes |
| del Gobierno | del gobierno | not in gazetteer | — | yes |
| documentos públicos | documentos públicos | not in gazetteer | — | no |
| Stanford | stanford | not in gazetteer | — | no |
| El presidente | el presidente | not in gazetteer | — | no |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| U.S. | GPE | yes | yes | yes | yes | — | yes |
| Trump | PERSON | yes | — | yes | yes | — | yes |
| Stanford | GPE | — | yes | — | — | — | — |
| cabo este martes | GPE | — | yes | — | — | — | — |
| del governo | GPE | — | yes | — | — | — | — |
| documentos públicos | GPE | — | yes | — | — | — | — |
| en la | GPE | — | yes | — | — | — | — |
| Artificiale, il coro dei no non è | ORG | — | — | — | — | — | — |
| Autoregolazione e nessun controllo | ORG | — | — | — | — | — | — |
| Controlli | ORG | — | — | — | — | — | — |
| Controlli interni robusti | ORG | — | — | — | — | — | — |
| Inteligencia Artificial' | ORG | — | — | — | — | — | — |
| Los representantes de las compañías se | ORG | — | — | — | — | — | — |
| Super Intelligence | ORG | — | — | — | — | — | — |
| Suprema | ORG | — | — | — | — | — | — |
| Tecnología para presentar una propuesta legislativa que est… | ORG | — | — | — | — | — | — |
| Trump firma | ORG | — | — | — | — | — | — |
| Trump ordena | ORG | — | — | — | — | — | — |
| Trump y los gigantes de la | ORG | — | — | — | — | — | — |
| UN | ORG | — | — | — | — | — | — |
| Un futuro di abbondanza | ORG | — | — | — | — | — | — |
| al rápido desarrollo de la | ORG | — | — | — | — | — | — |
| artificiale americana | ORG | — | — | — | — | — | — |
| concorrenza e sicurezza | ORG | — | — | — | — | — | — |
| crisi | ORG | — | — | — | — | — | — |
| del Big Tech tra progetti sull'AI | ORG | — | — | — | — | — | — |
| del nuevo término | ORG | — | — | — | — | — | — |
| di Big Tech | ORG | — | — | — | — | — | — |
| en un momento de creciente | ORG | — | — | — | — | — | — |
| età | ORG | — | — | — | — | — | — |
| forse nascerà un comitato consultivo di supervisione | ORG | — | — | — | — | — | — |
| l'era della Super Intelligenza' ' | ORG | — | — | — | — | — | — |
| la ' | ORG | — | — | — | — | — | — |
| la IA | ORG | — | — | — | — | — | — |
| la nuova | ORG | — | — | — | — | — | — |
| oficial | ORG | — | — | — | — | — | — |
| por | ORG | — | — | — | — | — | — |
| por la que insta | ORG | — | — | — | — | — | — |
| por los riesgos asociados | ORG | — | — | — | — | — | — |
| presidencial para Ciencia | ORG | — | — | — | — | — | — |
| que los | ORG | — | — | — | — | — | — |
| que no afecta | ORG | — | — | — | — | — | — |
| sellan un acuerdo | ORG | — | — | — | — | — | — |
| sustituir el término | ORG | — | — | — | — | — | — |
| tecnológico firmaron un acuerdo | ORG | — | — | — | — | — | — |
| umana | ORG | — | — | — | — | — | — |
| un acuerdo que calificó como | ORG | — | — | — | — | — | — |
| un plazo de 60 días | ORG | — | — | — | — | — | — |
| uno de los | ORG | — | — | — | — | — | — |
| Da Sam Altman di | PERSON | — | — | — | — | — | — |
| Donald J. Trump | PERSON | — | — | — | — | — | — |
| Donald Trump e la nuova | PERSON | — | — | — | — | — | — |
| El presidente Donald Trump | PERSON | — | — | — | — | — | — |
| La medida | PERSON | — | — | — | — | — | — |
| Nessuna menzione di rischi | PERSON | — | — | — | — | — | — |
| Sistemi di frontiera | PERSON | — | — | — | — | — | — |
| Zuckerberg | PERSON | — | — | — | — | — | — |
| ben oltre | PERSON | — | — | — | — | — | — |
| declaró al término de la | PERSON | — | — | — | — | — | — |
| firmado este martes una orden | PERSON | — | — | — | — | — | — |
| impegno moralmente vincolante su sicurezza IA' ' | PERSON | — | — | — | — | — | — |
| li bloccheremo' | PERSON | — | — | — | — | — | — |
| piani di deportazione dei migranti | PERSON | — | — | — | — | — | — |
| singoli aspetti | PERSON | — | — | — | — | — | — |

### ⚑ Automatic flags

- **alias resolution**: fuzzy: 'Super Intelligence Pranzo' -> 'Super Intelligence' (best alias 'Super Intelligence' scored 84 (threshold 80))
- **NER detection**: malformed span 'della Super Intelligenza' (ORG)
- **NER detection**: malformed span 'artificiale americana' (ORG)
- **NER detection**: malformed span 'crisi' (ORG)
- **NER detection**: malformed span 'forse nascerà un comitato consultivo di supervisione' (ORG)
- **NER detection**: article/possessive kept in span: 'impegno moralmente vincolante su sicurezza IA' ''
- **NER detection**: article/possessive kept in span: 'impegno moralmente vincolante su sicurezza IA''
- **NER detection**: malformed span 'en la' (GPE)
- **NER detection**: malformed span 'que los' (ORG)
- **NER detection**: malformed span 'tecnológico firmaron un acuerdo' (ORG)
- **NER detection**: malformed span 'declaró al término de la' (PERSON)
- **NER detection**: malformed span 'cabo este martes' (GPE)
- **NER detection**: article/possessive kept in span: 'li bloccheremo''
- **NER detection**: article/possessive kept in span: 'Súper Inteligencia''
- **NER detection**: malformed span 'del Gobierno' (GPE)
- **NER detection**: article/possessive kept in span: 'la ''
- **NER detection**: article/possessive kept in span: 'Inteligencia Artificial''
- **NER detection**: malformed span 'firmado este martes una orden' (PERSON)
- **NER detection**: malformed span 'por la que insta' (ORG)
- **NER detection**: malformed span 'sustituir el término' (ORG)
- **NER detection**: malformed span 'por' (ORG)
- **NER detection**: malformed span 'oficial' (ORG)
- **NER detection**: malformed span 'documentos públicos' (GPE)
- **NER detection**: malformed span 'que no afecta' (ORG)
- **NER detection**: malformed span 'un plazo de 60 días' (ORG)
- **NER detection**: malformed span 'presidencial para Ciencia' (ORG)
- **NER detection**: malformed span 'Tecnología para presentar una propuesta legislativa que establezca un…' (ORG)
- **NER detection**: malformed span 'del nuevo término' (ORG)
- **NER detection**: malformed span 'di Big Tech' (ORG)
- **NER detection**: malformed span 'concorrenza e sicurezza' (ORG)
- **NER detection**: malformed span 'età' (ORG)
- **NER detection**: malformed span 'del Big Tech tra progetti sull'AI' (ORG)
- **NER detection**: malformed span 'piani di deportazione dei migranti' (PERSON)
- **NER detection**: article/possessive kept in span: 'l'era della Super Intelligenza' ''
- **NER detection**: malformed span 'ben oltre' (PERSON)
- **NER detection**: malformed span 'singoli aspetti' (PERSON)
- **NER detection**: malformed span 'umana' (ORG)
- **NER detection**: malformed span 'l'era della' (ORG)
- **NER detection**: malformed span 'algunos de los' (ORG)
- **NER detection**: malformed span 'sellan un acuerdo' (ORG)
- **NER detection**: malformed span 'un acuerdo que calificó como' (ORG)
- **NER detection**: malformed span 'en un momento de creciente' (ORG)
- **NER detection**: malformed span 'por los riesgos asociados' (ORG)
- **multilingual failure**: es/it text parsed by the English NER model; 8 clause-length spans

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 24. Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz

- **Development:** `ml#16` (db `entity-review-ml`)
- **Domain / type:** unknown / unknown — sampled as **institutional** (fallback)
- **Items:** 2; **sources:** Clarín Mundo, Europa Press Internacional; **languages:** es

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 264 | Clarín Mundo | es | 2026-09-29 22:45 | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico | Las sanciones internacionales presionan a las finanzas de la república islámica |
| 75 | Europa Press Internacional | es | 2026-09-30 08:42 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz | El Gobierno de Irán ha confirmado este miércoles que ha recibido la respuesta oficial de Estados Unidos a su propuesta para reactivar el proceso de conversaciones para un acuerdo de paz, días después… |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| Por la guerra y la incertidumbre económica | GPE | yes | 1 | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico Las sanciones internacionales presionan a las finanzas … |
| la moneda de Irán se hunde en un | ORG | yes | 1 | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico Las sanciones internacionales presionan a las finanzas … |
| Las | GPE | yes | 1 | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico Las sanciones internacionales presionan a las finanzas … |
| internacionales presionan | ORG | yes | 1 | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico Las sanciones internacionales presionan a las finanzas … |
| las finanzas de la república | FAC | yes | 1 | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico Las sanciones internacionales presionan a las finanzas … |
| El régimen | ORG | yes | 1 | El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto. |
| abre la puerta | ORG | yes | 1 | El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto. |
| Estados Unidos | ORG | yes | 1 | El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto. |
| el conflicto | GPE | yes | 1 | El régimen abre la puerta a nuevas negociaciones con Estados Unidos para terminar con el conflicto. |
| que recibió la respuesta | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| oficial de EEUU | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| su última propuesta para un acuerdo de paz | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| El Gobierno de Irán ha confirmado este miércoles que ha rec… | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| oficial de Estados Unidos | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| su propuesta para reactivar | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| el proceso de conversaciones para un acuerdo de paz | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| días después de que el presidente | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| Donald Trump | PERSON | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| expresara su rechazo al | PERSON | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |
| por Teherán | ORG | yes | 1 | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz El Gobierno de Irán ha confirmado este miércoles … |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| las finanzas de la república | FAC | las finanzas de la república | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Por la guerra y la incertidumbre económica | GPE | Por la guerra y la incertidumbre económica | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| el conflicto | GPE | el conflicto | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| El régimen | ORG | El régimen | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Estados Unidos | ORG | por Estados Unidos | exact alias | 'Estados Unidos' is a recorded name of 'por Estados Unidos' | 1 | | | | | | |
| abre la puerta | ORG | abre la puerta | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| días después de que el presidente | ORG | días después de que el presidente | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| el proceso de conversaciones para un acuerdo de paz | ORG | el proceso de conversaciones para un acuerdo de paz | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| internacionales presionan | ORG | internacionales presionan | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| la moneda de Irán se hunde | ORG | la moneda de Irán se hunde | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| oficial de EEUU | ORG | oficial de EEUU | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| oficial de Estados Unidos | ORG | oficial de Estados Unidos | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| por Teherán | ORG | por Teherán | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| que recibió la respuesta | ORG | que recibió la respuesta | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| su propuesta para reactivar | ORG | su propuesta para reactivar | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| su última propuesta para un acuerdo de paz El Gobierno de I… | ORG | su última propuesta para un acuerdo de paz El Gobierno de I… | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Donald Trump | PERSON | Donald J. Trump | exact alias | 'Donald Trump' is a recorded name of 'Donald J. Trump' | 1 | | | | | | |
| expresara su rechazo al | PERSON | expresara su rechazo al | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Las | GPE | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| El Gobierno de Irán ha confirmado este miércoles que ha rec… | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| la moneda de Irán se hunde en un | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |
| su última propuesta para un acuerdo de paz | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | Por la guerra y la incertidumbre económica | yes | — | por la guerra y la incertidumbre económica → por la guerra y la incer… |
| title ×1 | la moneda de Irán se hunde en un | yes | — | la moneda de irán se hunde en un → la moneda de irán se hunde en un |
| lead ×1 | Las | yes | — | las → las |
| lead ×1 | internacionales presionan | no | common_noun | internacionales presionan → internacionales presionan |
| title ×1 | que recibió la respuesta | yes | — | que recibió la respuesta → que recibió la respuesta |
| title ×1 | oficial de EEUU | yes | — | oficial de eeuu → oficial de eeuu |
| title ×1 | su última propuesta para un acuerdo de paz | yes | — | su última propuesta para un acuerdo de paz → su última propuesta para… |
| lead ×1 | El Gobierno de Irán ha | yes | — | el gobierno de irán ha → el gobierno de irán ha |
| lead ×1 | oficial de Estados Unidos | yes | — | oficial de estados unidos → oficial de estados unidos |
| lead ×1 | su propuesta para reactivar | yes | — | su propuesta para reactivar → su propuesta para reactivar |
| lead ×1 | el proceso de conversaciones para un acuerdo de paz | yes | — | el proceso de conversaciones para un acuerdo de paz → el proceso de c… |
| lead ×1 | días después de que el presidente | yes | — | días después de que el presidente → días después de que el presidente |
| lead ×1 | Donald Trump | yes | — | donald trump → united states |
| lead ×1 | expresara su rechazo al plan presentado | yes | — | expresara su rechazo al plan presentado → expresara su rechazo al pla… |
| lead ×1 | por Teher | yes | — | por teher → por teher |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): por la guerra y la incertidumbre económica 1.0, la moneda de irán se hunde en un 1.0, su última propuesta para un acuerdo de paz 1.0, que recibió la respuesta 1.0, oficial de eeuu 1.0, las 0.5, united states 0.5, su propuesta para reactivar 0.5, el gobierno de irán ha 0.5, días después de que el presidente 0.5, expresara su rechazo al plan presentado 0.5, oficial de estados unidos 0.5, el proceso de conversaciones para un acuerdo de paz 0.5, por teher 0.5
- **Final principal actors:** la moneda de irán se hunde en un, oficial de eeuu, por la guerra y la incertidumbre económica, que recibió la respuesta, su última propuesta para un acuerdo de paz
- **Entities flagged principal on the Development:** Por la guerra y la incertidumbre económica, oficial de EEUU, que recibió la respuesta

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Por la guerra y la incertidumbre económica | por la guerra y la incertidumbre económ… | not in gazetteer | — | yes |
| las finanzas de la república | las finanzas de la república | not in gazetteer | — | no |
| el conflicto | el conflicto | not in gazetteer | — | no |
| Las | las | not in gazetteer | — | yes |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Por la guerra y la incertidumbre económica | GPE | yes | yes | yes | yes | — | yes |
| oficial de EEUU | ORG | yes | — | yes | yes | — | yes |
| que recibió la respuesta | ORG | yes | — | yes | yes | — | yes |
| las finanzas de la república | FAC | — | yes | — | — | — | — |
| el conflicto | GPE | — | yes | — | — | — | — |
| El régimen | ORG | — | — | — | — | — | — |
| abre la puerta | ORG | — | — | — | — | — | — |
| días después de que el presidente | ORG | — | — | — | — | — | — |
| el proceso de conversaciones para un acuerdo de paz | ORG | — | — | — | — | — | — |
| internacionales presionan | ORG | — | — | — | — | — | — |
| la moneda de Irán se hunde | ORG | — | — | — | — | — | — |
| oficial de Estados Unidos | ORG | — | — | — | — | — | — |
| por Estados Unidos | ORG | — | — | — | — | — | — |
| por Teherán | ORG | — | — | — | — | — | — |
| su propuesta para reactivar | ORG | — | — | — | — | — | — |
| su última propuesta para un acuerdo de paz El Gobierno de I… | ORG | — | — | — | — | — | — |
| Donald J. Trump | PERSON | — | — | — | — | — | — |
| expresara su rechazo al | PERSON | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: malformed span 'internacionales presionan' (ORG)
- **NER detection**: malformed span 'las finanzas de la república' (FAC)
- **NER detection**: malformed span 'abre la puerta' (ORG)
- **NER detection**: malformed span 'la moneda de Irán se hunde en un' (ORG)
- **NER detection**: malformed span 'que recibió la respuesta' (ORG)
- **NER detection**: malformed span 'oficial de EEUU' (ORG)
- **NER detection**: malformed span 'su última propuesta para un acuerdo de paz El Gobierno de Irán ha con…' (ORG)
- **NER detection**: malformed span 'oficial de Estados Unidos' (ORG)
- **NER detection**: malformed span 'su propuesta para reactivar' (ORG)
- **NER detection**: malformed span 'el proceso de conversaciones para un acuerdo de paz' (ORG)
- **NER detection**: malformed span 'días después de que el presidente' (ORG)
- **NER detection**: malformed span 'expresara su rechazo al' (PERSON)
- **NER detection**: malformed span 'por Teherán' (ORG)
- **NER detection**: malformed span 'su última propuesta para un acuerdo de paz' (ORG)
- **NER detection**: malformed span 'El Gobierno de Irán ha confirmado este miércoles que ha recibido la' (ORG)
- **multilingual failure** (principal): principal 'la moneda de irán se hunde en un' is a clause, not a name
- **location/actor confusion** (principal): principal 'por la guerra y la incertidumbre económica' comes from place mentions (GPE)
- **multilingual failure** (principal): principal 'por la guerra y la incertidumbre económica' is a clause, not a name
- **multilingual failure** (principal): principal 'que recibió la respuesta' is a clause, not a name
- **multilingual failure** (principal): principal 'su última propuesta para un acuerdo de paz' is a clause, not a name
- **multilingual failure**: es text parsed by the English NER model; 8 clause-length spans
- **principal-selection failure** (principal): no state among the principals (la moneda de irán se hunde en un, oficial de eeuu, por la guerra y la incertidumbre económica, que recibió la respuesta, su última propuesta para un acuerdo de paz); check they are actors

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

## 25. Commission proposes a new EU Critical Communication System for first responders

- **Development:** `ml#23` (db `entity-review-ml`)
- **Domain / type:** unknown / unknown — sampled as **institutional** (fallback)
- **Items:** 2; **sources:** Council of the EU Press, European Commission Press; **languages:** en

### Source text

| Item | Source | Lang | Published (UTC) | Headline | Lead |
|---|---|---|---|---|---|
| 361 | Council of the EU Press | en | 2026-09-28 16:05 | Council strengthens EU space threat response architecture | The Council has adopted a decision strengthening the EU Space Threat Response Architecture to respond to increased irresponsible and hostile behaviour in the space domain. |
| 352 | European Commission Press | en | 2026-09-29 22:00 | Commission proposes a new EU Critical Communication System for first responders | European Commission Press release Brussels, 30 Sep 2026 Today, the European Commission proposed to establish a new EU Critical Communication System to provide Europe's first responders with secure an… |

### Raw NER output

| Text span | NER type | Kept by pipeline | × | Source sentence (first) |
|---|---|---|---:|---|
| EU | ORG | yes | 1 | Council strengthens EU space threat response architecture The Council has adopted a decision strengthening the EU Space Threat Response Architecture … |
| Council | ORG | yes | 1 | Council strengthens EU space threat response architecture The Council has adopted a decision strengthening the EU Space Threat Response Architecture … |
| the EU Space Threat Response Architecture | ORG | yes | 1 | Council strengthens EU space threat response architecture The Council has adopted a decision strengthening the EU Space Threat Response Architecture … |
| EU Critical Communication System | ORG | yes | 2 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |
| first | ORDINAL | no (label not stored) | 2 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |
| European Commission Press | ORG | yes | 1 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |
| Brussels | GPE | yes | 1 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |
| 30 Sep 2026 | DATE | no (label not stored) | 1 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |
| Today | DATE | no (label not stored) | 1 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |
| the European Commission | ORG | yes | 1 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |
| Europe | LOC | yes | 1 | Commission proposes a new EU Critical Communication System for first responders European Commission Press release Brussels, 30 Sep 2026 Today, the Eu… |

### Resolution output + review

| Mention | Detected type | Canonical entity | Method | Reason | × | Entity correct? | Canonical resolution? | Principal actor? | Correct type | Correct canonical form | Comment |
|---|---|---|---|---|---:|---|---|---|---|---|---|
| Brussels | GPE | Brussels | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| Europe | LOC | Europe | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| EU | ORG | the European Union | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| EU Critical Communication System | ORG | the European Union Critical Communication System European C… | fuzzy | best alias 'the European Union Critical Communication System' scored 84 (threshold 80) | 1 | | | | | | |
| European Commission Press | ORG | the European Commission | fuzzy | best alias 'the European Commission' scored 86 (threshold 80) | 1 | | | | | | |
| The Council | ORG | Council | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the EU Space Threat Response Architecture | ORG | the EU Space Threat Response Architecture | new entity | no existing match: the mention created this entity | 1 | | | | | | |
| the European Commission | ORG | — | unresolved | detected now but no stored entity link for this item | 1 | | | | | | |

### Principal actors

| Item field | Candidate span | Participant | Rejected because | Normalised → actor key |
|---|---|---|---|---|
| title ×1 | EU | yes | — | european union → european union |
| lead ×1 | Council | yes | — | council → council |
| lead ×1 | the EU Space Threat Response Architecture | yes | — | eu space threat response architecture → eu space threat response arch… |
| title ×1 | EU Critical Communication System | yes | — | eu critical communication system → eu critical communication system |
| lead ×1 | European Commission Press | no | topic / not a participant | european commission press → european commission press |
| lead ×1 | Brussels | yes | — | european union → european union |
| lead ×1 | the European Commission | yes | — | european union → european union |
| lead ×1 | EU Critical Communication System | yes | — | eu critical communication system → eu critical communication system |

- **Support per actor** (headline 1.0, lead 0.5; needed 1.0): european union 1.5, eu critical communication system 1.0, council 0.5, eu space threat response architecture 0.5
- **Final principal actors:** eu critical communication system, european union
- **Entities flagged principal on the Development:** Brussels, the European Commission, the European Union

### Geography

| Place mention | Canonical place | Level | Contained in | Treated as actor? |
|---|---|---|---|---|
| Europe | europe | not in gazetteer | — | no |
| Brussels | brussels | sub-national | belgium | yes |

### Current downstream effect

| Entity | Type | Principal | Clustering | Situation matching | Ranking | Provenance | UI display |
|---|---|---|---|---|---|---|---|
| Brussels | GPE | yes | yes | yes | yes | — | yes |
| the European Commission | ORG | yes | — | yes | yes | — | yes |
| the European Union | ORG | yes | — | yes | yes | — | yes |
| Europe | LOC | — | yes | — | — | — | — |
| Council | ORG | — | — | — | — | — | — |
| the EU Space Threat Response Architecture | ORG | — | — | — | — | — | — |
| the European Union Critical Communication System European C… | ORG | — | — | — | — | — | — |

### ⚑ Automatic flags

- **NER detection**: article/possessive kept in span: 'The Council'
- **NER detection**: article/possessive kept in span: 'the EU Space Threat Response Architecture'
- **alias resolution**: fuzzy: 'European Commission Press' -> 'the European Commission' (best alias 'the European Commission' scored 86 (threshold 80))
- **alias resolution**: fuzzy: 'EU Critical Communication System' -> 'the European Union Critical Communication System …' (best alias 'the European Union Critical Communication System' scored 84 (threshold 80))
- **NER detection**: article/possessive kept in span: 'the European Commission'
- **principal-selection failure** (principal): no state among the principals (eu critical communication system, european union); check they are actors

### Development review

```text
Overall actors correct? YES / NO / PARTIAL
Missing important actor:
Spurious actor:
Notes:
```

---

# Summary

| Domain | Examples | Entity mentions | Suspect entities | Suspect principals | Unresolved |
|---|---:|---:|---:|---:|---:|
| diplomacy | 4 | 62 | 9 | 3 | 0 |
| military | 4 | 190 | 19 | 2 | 6 |
| security | 4 | 134 | 14 | 4 | 3 |
| political | 4 | 37 | 1 | 5 | 2 |
| economic | 3 | 66 | 6 | 0 | 0 |
| humanitarian | 2 | 24 | 0 | 2 | 0 |
| institutional | 4 | 132 | 66 | 7 | 12 |
| **total** | **25** | **645** | **115** | **23** | **23** |

Suspect counts are automatic flags (deduplicated per Development), not confirmed errors.

## Suspected failures by class

| Class | Flags |
|---|---:|
| NER detection | 105 |
| entity typing | 0 |
| alias resolution | 10 |
| person -> state/institution mapping | 6 |
| location/actor confusion | 5 |
| contextual organisation | 3 |
| duplicate canonical identity | 0 |
| multilingual failure | 6 |
| principal-selection failure | 5 |


## Observations the heuristics do not count

Seen while assembling the sample (for your review; not fixed):

- **Entity typing:** `Milrem` (Estonian robotics company) typed PERSON and selected as a principal; `Chelsea, MA`
  typed ORG; `Fat Bear Week` typed ORG and selected as the only principal of a Development classified *diplomacy*;
  `Standard Missile 6` typed FAC.
- **Wrong fuzzy links (alias resolution):** `the U.S. 6th Fleet` → `U.S. 5th Fleet’s` (87); `European Nato` → `EU` (81);
  `Germany` → `the German` (92); `European` → `Europe` (86). Correct fuzzy links also exist (`Houthi` → `Houthis`,
  `US Navy` → `the U.S. Navy`), so the 80/85 thresholds admit both.
- **Alias pollution (alias resolution):** a fuzzy match registers the mention as a permanent alias, so later mentions
  resolve by *exact alias* to the wrong entity. In this sample `American` → `Mexican` (Development 3). Across the
  working copies' entity tables, 66 of 364 learned aliases (English data) and 52 of 275 (multilingual collection) are
  unlike their entity (rapidfuzz < 90, not seeded, not a substring), e.g. `England` → `Nagaland`, `Tejas` → `Texas`,
  `Canada` → `Cada`, `Auckland` → `Oakland`, `Nation` → `NATO`, `UNSCR` → `UNHCR`, `Americans` → `Mexican`,
  `the United States Marine Corps` → `the United States Armed Forces` (GPE).
- **Canonical names keep articles and possessives:** 273 of 2,653 canonical names start with "the" and 41 end in a
  possessive (`U.S. 5th Fleet’s`, `Saudi Arabia’s`). Normalisation folds these for matching, so no duplicate pair exists;
  it affects display and fuzzy scores. The only same-type duplicate found is `UK` / `U.K.`.
- **Unmapped institutions:** `Navy`, `Defense` become principals of their own instead of the United States.
- **Multilingual:** Spanish and Italian headlines produce clause-length "entities" (`la moneda de Irán se hunde en un`,
  `Por la guerra y la incertidumbre económica` typed GPE) that become principals; `strikesRussian` shows feed text
  glued without a space.
- **Classification (context, outside entity logic):** no Development is ever classified *humanitarian* or
  *institutional*; a Federal Register lab-accreditation notice is *political* with three place/company principals.

## Recommendation (most common failure classes)

0. **Alias pollution from fuzzy resolution** is the highest-impact English failure: one wrong fuzzy match becomes a
   permanent alias (≈18% of learned aliases look wrong), and nationality/country actors (`American` → `Mexican`)
   feed principal selection, Situation matching and ranking. Review these first.
1. **NER span quality** is the most frequent problem by count (articles, possessives, glued text, HTML entities,
   clause-length spans); most of it is cosmetic for English but decisive for Spanish/Italian, where the English spaCy
   model turns clauses into principals.
2. **Multilingual failure** has the highest impact per case: every Spanish/Italian Development with a non-trivial
   headline produced a spurious principal. A language-appropriate NER model (or skipping actor extraction for
   unsupported languages) matters more than any rule change.
3. **Fuzzy thresholds (80 / 85)** also admit direct wrong links (fleet numbers, `European Nato` → `EU`); see item 0
   for how they persist.
4. **Principal selection on non-news items** (administrative notices, event names) and **unmapped institutions**
   (`Navy`, `Defense`) are the main principal-level errors in English.
5. Location/actor confusion is rarer than expected in English (Gaza cases are arguable); it appears mostly through
   mistyped addresses and Spanish clauses.

Stopping here for your annotations.
