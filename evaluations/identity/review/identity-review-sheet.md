# Development identity: owner review sheet

Draft labels were written blind: the labeller saw only the item text, outlet, publication time, language and the Development definition. It did not see the current grouping, similarity scores or the rule that proposed a case. The current-system columns are here for your review only.

Fill in `owner-verdicts.yaml` (or the verdict line under each case): `ACCEPT`, or the corrected label `SAME_DEVELOPMENT` / `DIFFERENT_DEVELOPMENT` / `AMBIGUOUS`, with an optional note. Nothing is frozen or hashed until your verdicts are applied.

## Structural cases (computed from the draft label)

| Flag | Meaning | Cases |
|---|---|---|
| `grows_same_id` | cluster grows over time and should keep the same ID | 18: A012, H002, H003, H010, H014, H017, B003, C006, C021, C038, C049, C052, C072, C085, C089, C093, C109, C114 |
| `should_split` | one Development should split into two | 35: A002, A013, A021, A022, A023, A028, H021, H024, B008, B011, C001, C002, C003, C007, C012, C017, C022, C026, C029, C033, C035, C037, C042, C046, C062, C063, C073, C079, C080, C084, C094, C105, C106, C112, C115 |
| `should_merge` | two candidate Developments (or an unattached item) should merge | 15: H001, H009, H018, B002, B004, B007, C036, C043, C051, C066, C077, C092, C096, C104, C113 |
| `same_story_new_action` | same story, materially new action | 5: A021, A022, B011, C003, C094 |
| `roundup_contamination` | roundup contaminating identity | 2: C029, C080 |
| `single_source_below_development` | single-source evidence that must stay below the Development layer | 1: C003 |
| `late_attach` | item attached late to an existing Development | 8: H003, H014, C036, C049, C077, C085, C096, C109 |

## Totals

| Window | Split | Cases | SAME | DIFFERENT | AMBIGUOUS |
|---|---|---:|---:|---:|---:|
| 2026-08-21 | development | 33 | 6 | 25 | 2 |
| 2026-08-31 | holdout | 30 | 10 | 18 | 2 |
| 2026-09-25 | development | 11 | 5 | 6 | 0 |
| 2026-09-30-multilingual | development | 115 | 38 | 74 | 3 |

## Window 2026-08-21 (development)

### A001

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-85e1f8c5197d` · t1 | `b-d21109ba71d7` · t2 |
| published | 2026-08-21T02:28:28 | 2026-08-21T12:54:44 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Hong Kong Tiananmen vigil organiser, former leaders guilty of inciting subversion | Why are Hong Kong’s Tiananmen vigil organisers facing prison? |
| current Development | D1 | - |
| places | China, Hong Kong, Hong Kong Tiananmen, Tiananmen Square | Hong Kong, Tiananmen |

- D1: "Hong Kong Tiananmen vigil organiser, former leaders guilty of inciting subversion" · 3 items · sources Al Jazeera, BBC World, South China Morning Post · principals -
- current system: one item not in any Development; cosine 0.63; not in any Development; closest member (cosine 0.63) is in D1; tick 3: link cut by segmentation guard 'analysis_headline'; ticks 1 and 2, cosine 0.63: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · SCMP reports the Hong Kong Alliance guilty verdict; Al Jazeera's 'Why are ... facing prison?' is an explainer about it.
- **owner verdict:** ____

### A002  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-ed25155d038d` · t4 | `b-320f20d36f00` · t1 |
| published | 2026-08-22T18:20:36 | 2026-08-21T03:12:49 |
| source · lang | BBC World · en | South China Morning Post · en |
| headline | Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse | Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud |
| current Development | D5 | D5 |
| places | Canada, US | Canada, Manitoba, US, Washington |

- D5: "Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud" · 2 items · sources BBC World, South China Morning Post · principals Canada, Carney, Donald Trump, Mark Carney, Trump
- current system: same Development D5; cosine 0.53; D5: grouped together at tick 4
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Carney announcing retaliatory tariffs after talks collapsed (22 Aug) is a different statement from Manitoba premier Kinew's attack on Trump (Thursday 20 Aug).
- **owner verdict:** ____

### A003

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-e095d21a704d` · t2 | `b-b3d4b7966b1a` · t1 |
| published | 2026-08-21T12:25:04 | 2026-08-21T01:30:06 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Humanoid crashes during speed test as China’s robotics industry grows | In the embodied AI race, China can opt to look beyond bigger models |
| current Development | - | - |
| places | China | China |

- current system: neither in a Development; cosine 0.56; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · A humanoid crashing in a speed test is an incident; the SCMP piece is an opinion on China's embodied-AI strategy.
- **owner verdict:** ____

### A004

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-3a527f407cc4` · t1 | `b-1a0f6855a3bf` · t2 |
| published | 2026-08-21T01:38:37 | 2026-08-21T13:30:10 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Brazil launches AI supercomputer push while balancing US and Chinese tech | China’s telecoms giants bet on ‘token factories’ as AI drives revenue growth |
| current Development | - | - |
| places | Brazil, China, US | China |

- current system: neither in a Development; cosine 0.56; tick 3: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Brazil's AI supercomputer investment and Chinese telecoms' token-factory strategy are unrelated occurrences.
- **owner verdict:** ____

### A005

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-b34bb8cdf0bb` · t2 | `b-f21800253bff` · t3 |
| published | 2026-08-21T13:29:28 | 2026-08-22T10:09:11 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Liverpool preview: Five key questions heading into 2026-27 season | Manchester City preview: Five key questions heading into 2026-27 season |
| current Development | - | - |
| places | Spain | Manchester City |

- current system: neither in a Development; cosine 0.66; ticks 2 and 3, cosine 0.66: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Separate season previews for Liverpool and Manchester City.
- **owner verdict:** ____

### A006

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-47221c4faf92` · t2 | `b-dfc16b535283` · t1 |
| published | 2026-08-21T12:08:50 | 2026-08-21T01:00:07 |
| source · lang | South China Morning Post · en | South China Morning Post · en |
| headline | Singapore’s carrots for fund managers set to sharpen competition with Hong Kong | Hong Kong financiers press for tax breaks after Singapore unveils rival scheme |
| current Development | - | - |
| places | Hong Kong, Lee Kuan Yew School, Singapore | Hong Kong, Singapore |

- current system: neither in a Development; cosine 0.64; ticks 1 and 2, cosine 0.64: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (reaction) · confidence medium · Analysts assessing Singapore's fund-manager package differs from Hong Kong financiers pressing for their own carried-interest tax break in response.
- **owner verdict:** ____

### A007

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-53dc89e53904` · t2 | `b-312853eceb17` · t2 |
| published | 2026-08-21T21:03:24 | 2026-08-21T14:49:33 |
| source · lang | BBC World · en | South China Morning Post · en |
| headline | One killed in sword attack at Swedish school | Man armed with sword injures several at Swedish high school |
| current Development | D2 | D2 |
| places | Sweden | Fagersta, Sweden |

- D2: "Several people injured in sword attack at school in Sweden" · 3 items · sources Al Jazeera, BBC World, South China Morning Post · principals -
- current system: same Development D2; cosine 0.76; D2: least similar members of a 3-item Development (cosine 0.76)
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Both report the Friday sword attack at a Swedish high school (Fagersta); BBC updates with one death and a suspect arrested.
- **owner verdict:** ____

### A008

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-bbcb00eae268` · t2 | `b-f55f349f9898` · t1 |
| published | 2026-08-21T15:00:05 | 2026-08-21T11:57:39 |
| source · lang | South China Morning Post · en | South China Morning Post · en |
| headline | China and US push Southeast Asia over their AI blocs. Will it test region’s non-alignment? | Will other Southeast Asian countries follow Indonesia’s example with joint China drill? |
| current Development | - | - |
| places | Beijing, China, Southeast Asia, US, Washington | China, Indonesia, Taiwan |

- current system: neither in a Development; cosine 0.61; ticks 1 and 2, cosine 0.61: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · US-China AI bloc analysis versus analysis of the China-Indonesia naval drill; different subjects, both commentary.
- **owner verdict:** ____

### A009

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-8b0980fba97b` · t4 | `b-34d06bf06e8c` · t4 |
| published | 2026-08-22T14:37:40 | 2026-08-22T21:42:42 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Israeli drone strike on ‘civilian vehicle’ injures several in Syria | Syria says Israeli strike near Damascus violation of international law |
| current Development | D7 | D7 |
| places | Israel, Syria | Damascus, Israel, Syria, Turkey |

- D7: "Israeli drone strike on ‘civilian vehicle’ injures several in Syria" · 2 items · sources Al Jazeera, BBC World · principals Israel, Syria
- current system: same Development D7; cosine 0.73; D7: grouped together at tick 4
- **proposed:** `AMBIGUOUS` · confidence low · Both report an Israeli strike in Syria on 22 Aug condemned by Syria as violating international law, but 'civilian vehicle in the southwest' and 'near Damascus' may or may not be the same strike.
- **owner verdict:** ____

### A010

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-e736db6a6335` · t1 | `b-9259fb4b9124` · t3 |
| published | 2026-08-21T09:54:38 | 2026-08-22T10:01:18 |
| source · lang | South China Morning Post · en | BBC World · en |
| headline | Embrace AI to boost competitiveness, Paul Chan says at tech festival opening | Robot horse and rider steal the spotlight at Chinese conference |
| current Development | - | - |
| places | Hong Kong | Beijing, China |

- current system: neither in a Development; cosine 0.59; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Paul Chan opening Hong Kong's tech exhibition and a robotics conference in Beijing are different events in different cities.
- **owner verdict:** ____

### A011

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-342d8d2a178d` · t2 | `b-bbcb00eae268` · t2 |
| published | 2026-08-21T12:58:20 | 2026-08-21T15:00:05 |
| source · lang | Breaking Defense · en | South China Morning Post · en |
| headline | ‘Hot competition’: NSA deputy sounds alarm on China threat, AI race | China and US push Southeast Asia over their AI blocs. Will it test region’s non-alignment? |
| current Development | - | - |
| places | Beijing, China, Iran | Beijing, China, Southeast Asia, US, Washington |

- current system: neither in a Development; cosine 0.47; same tick, different outlets, cosine 0.47: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · NSA deputy Kosiba's remarks on China versus an SCMP analysis of US-China AI blocs in Southeast Asia.
- **owner verdict:** ____

### A012  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-e5e62052515e` · t4 | `b-38f9f084379c` · t3 |
| published | 2026-08-22T17:02:06 | 2026-08-22T11:30:51 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | Watch: Moment humanoid robot beats Usain Bolt's 100m record | Usain Bolt’s 100m record broken at World Humanoid Robot Games |
| current Development | D4 | D4 |
| places | Beijing, World Humanoid Robot Games | Beijing, China, World Humanoid Robot Games |

- D4: "Usain Bolt’s 100m record broken at World Humanoid Robot Games" · 2 items · sources Al Jazeera, BBC World · principals -
- current system: same Development D4; cosine 0.82; D4: grouped together at tick 4; ticks 3 and 4, cosine 0.82: same Development
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report a humanoid robot beating Bolt's 100m record at the World Humanoid Robot Games in Beijing.
- **owner verdict:** ____

### A013  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-9d435faf259d` · t4 | `b-e65cd1bb15f4` · t4 |
| published | 2026-08-22T15:45:40 | 2026-08-22T12:51:55 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Settlers target Palestinian homes in Occupied West Bank’s Area B | Jewish activists push back against Israeli settlers |
| current Development | D6 | D6 |
| places | Israel, Occupied West Bank, Palestine, Qaryut | Israel, Occupied West Bank |

- D6: "Israel re-establishes closed West Bank settlement, defying growing international protests" · 3 items · sources Al Jazeera, BBC World · principals Israel
- current system: same Development D6; cosine 0.63; D6: least similar members of a 3-item Development (cosine 0.63)
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Settlers forcing families from homes in Qaryut is a different occurrence from Jewish activists providing a protective presence in the West Bank.
- **owner verdict:** ____

### A014

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-8a8e0d395f60` · t1 | `b-7d87768d2f82` · t1 |
| published | 2026-08-21T03:50:15 | 2026-08-21T05:47:32 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Hong Kong Tiananmen activists found guilty of national security charges | Hong Kong's Tiananmen activists guilty in national security trial |
| current Development | D1 | D1 |
| places | Hong Kong, Hong Kong Tiananmen | China, Hong Kong, Tiananmen |

- D1: "Hong Kong Tiananmen vigil organiser, former leaders guilty of inciting subversion" · 3 items · sources Al Jazeera, BBC World, South China Morning Post · principals -
- current system: same Development D1; cosine 0.81; D1: grouped together at tick 1
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report the guilty verdict against Hong Kong Tiananmen activists in the national security trial.
- **owner verdict:** ____

### A015

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-b63dd0b0fd76` · t2 | `b-8608173935c4` · t1 |
| published | 2026-08-21T13:59:28 | 2026-08-21T00:00:00 |
| source · lang | Al Jazeera · en | Al Jazeera · en · ROUNDUP |
| headline | War on Iran: The US could focus on economically isolating Iran | Iran war live: US vows toughest Iran sanctions, urges China support |
| current Development | - | - |
| places | Iran, US | China, Iran, US |

- current system: neither in a Development; cosine 0.61; ticks 1 and 2, cosine 0.61: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · 'The US could focus on economically isolating Iran' is analysis of the strategy shift; the live blog reports Bessent vowing toughest sanctions.
- **owner verdict:** ____

### A016

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-3a527f407cc4` · t1 | `b-b3d4b7966b1a` · t1 |
| published | 2026-08-21T01:38:37 | 2026-08-21T01:30:06 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Brazil launches AI supercomputer push while balancing US and Chinese tech | In the embodied AI race, China can opt to look beyond bigger models |
| current Development | - | - |
| places | Brazil, China, US | China |

- current system: neither in a Development; cosine 0.40; same tick, different outlets, cosine 0.40: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Brazil's AI investment report versus an SCMP opinion on China's embodied AI.
- **owner verdict:** ____

### A017

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-6a2e684a65d2` · t2 | `b-2e0da6b7e7eb` · t2 |
| published | 2026-08-21T13:30:36 | 2026-08-21T13:44:43 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll passes 2,500: UN | Ebola vaccine trial to start in DR Congo as warning issued over speed of infections |
| current Development | - | D3 |
| places | Congo, DR | DR Congo |

- D3: "Ebola vaccine trial to start in DR Congo as warning issued over speed of infections" · 3 items · sources Al Jazeera, BBC World · principals -
- current system: one item not in any Development; cosine 0.67; tick 3: link cut by segmentation guard 'disjoint_locations'
- **proposed:** `AMBIGUOUS` · confidence low · Both carry the same-day UN/WHO warning on Ebola's speed with 2,500 deaths, but the BBC headline leads with a vaccine trial announcement, so it is unclear whether they share one occurrence.
- **owner verdict:** ____

### A018

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-312853eceb17` · t2 | `b-25760921e54e` · t2 |
| published | 2026-08-21T14:49:33 | 2026-08-21T13:48:09 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Man armed with sword injures several at Swedish high school | Several people injured in sword attack at school in Sweden |
| current Development | D2 | D2 |
| places | Fagersta, Sweden | Fagersta, Sweden |

- D2: "Several people injured in sword attack at school in Sweden" · 3 items · sources Al Jazeera, BBC World, South China Morning Post · principals -
- current system: same Development D2; cosine 0.81; D2: grouped together at tick 2
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report the sword attack at a high school in Fagersta, Sweden, with one person detained.
- **owner verdict:** ____

### A019

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-e090e68e5085` · t4 | `b-71e9862bc0c3` · t4 |
| published | 2026-08-22T12:09:09 | 2026-08-22T13:13:16 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Russian strikes kill 6 people in Ukraine, day after shopping complex attack | Rescuers dig through Ukraine mall wreckage as Zelensky condemns 'despicable' Russian strike |
| current Development | - | - |
| places | Russia, Ukraine | Russia, Ukraine |

- current system: neither in a Development; cosine 0.51; same tick, different outlets, cosine 0.51: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence high · Al Jazeera reports new Russian strikes killing 6 on the day after the mall attack; BBC covers rescue at Friday's mall strike that killed 16.
- **owner verdict:** ____

### A020

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-25760921e54e` · t2 | `b-36b77b6ef894` · t2 |
| published | 2026-08-21T13:48:09 | 2026-08-21T22:45:01 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Several people injured in sword attack at school in Sweden | Two injured in stabbing attack at Canada Sikh temple |
| current Development | D2 | - |
| places | Fagersta, Sweden | Canada |

- D2: "Several people injured in sword attack at school in Sweden" · 3 items · sources Al Jazeera, BBC World, South China Morning Post · principals -
- current system: one item not in any Development; cosine 0.48; same tick, different outlets, cosine 0.48: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · A Swedish school sword attack and a stabbing at a Canadian Sikh temple are separate incidents.
- **owner verdict:** ____

### A021  · flags: should_split, same_story_new_action

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-2e0da6b7e7eb` · t2 | `b-8826249c972c` · t3 |
| published | 2026-08-21T13:44:43 | 2026-08-22T10:13:56 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | Ebola vaccine trial to start in DR Congo as warning issued over speed of infections | More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo |
| current Development | D3 | D3 |
| places | DR Congo | Congo, Kinshasa |

- D3: "Ebola vaccine trial to start in DR Congo as warning issued over speed of infections" · 3 items · sources Al Jazeera, BBC World · principals -
- current system: same Development D3; cosine 0.69; D3: grouped together at tick 3; ticks 2 and 3, cosine 0.69: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence medium · The announced vaccine trial and WHO warning (21 Aug) differ from the arrival of 16,000 Ervebo doses in Kinshasa (22 Aug).
- **owner verdict:** ____

### A022  · flags: should_split, same_story_new_action

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-422186e87411` · t3 | `b-2e0da6b7e7eb` · t2 |
| published | 2026-08-22T11:15:39 | 2026-08-21T13:44:43 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Ebola continues to spread in the DRC as 16,000 vaccine doses arrive | Ebola vaccine trial to start in DR Congo as warning issued over speed of infections |
| current Development | D3 | D3 |
| places | - | DR Congo |

- D3: "Ebola vaccine trial to start in DR Congo as warning issued over speed of infections" · 3 items · sources Al Jazeera, BBC World · principals -
- current system: same Development D3; cosine 0.68; D3: grouped together at tick 3; D3: least similar members of a 3-item Development (cosine 0.68); ticks 2 and 3, cosine 0.68: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence medium · Arrival of 16,000 vaccine doses on 22 Aug is a later occurrence than the vaccine-trial announcement and WHO warning of 21 Aug.
- **owner verdict:** ____

### A023  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-52e7176bac0a` · t1 | `b-e65cd1bb15f4` · t4 |
| published | 2026-08-21T05:00:57 | 2026-08-22T12:51:55 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | Israel re-establishes closed West Bank settlement, defying growing international protests | Jewish activists push back against Israeli settlers |
| current Development | D6 | D6 |
| places | Israel, Palestine, West Bank | Israel, Occupied West Bank |

- D6: "Israel re-establishes closed West Bank settlement, defying growing international protests" · 3 items · sources Al Jazeera, BBC World · principals Israel
- current system: same Development D6; cosine 0.67; D6: grouped together at tick 4; ticks 1 and 4, cosine 0.67: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Israel re-establishing a closed settlement differs from Jewish activists' protective presence against settlers.
- **owner verdict:** ____

### A024

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-25760921e54e` · t2 | `b-53dc89e53904` · t2 |
| published | 2026-08-21T13:48:09 | 2026-08-21T21:03:24 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Several people injured in sword attack at school in Sweden | One killed in sword attack at Swedish school |
| current Development | D2 | D2 |
| places | Fagersta, Sweden | Sweden |

- D2: "Several people injured in sword attack at school in Sweden" · 3 items · sources Al Jazeera, BBC World, South China Morning Post · principals -
- current system: same Development D2; cosine 0.78; D2: grouped together at tick 2
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Same Fagersta school sword attack; BBC later adds one killed and an 18-year-old suspect shot and arrested.
- **owner verdict:** ____

### A025

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-9d435faf259d` · t4 | `b-38eba7dee8c5` · t2 |
| published | 2026-08-22T15:45:40 | 2026-08-21T19:31:47 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Settlers target Palestinian homes in Occupied West Bank’s Area B | How Israel is expanding settlements in drive to reshape West Bank |
| current Development | D6 | - |
| places | Israel, Occupied West Bank, Palestine, Qaryut | Israel, Palestine, West Bank |

- D6: "Israel re-establishes closed West Bank settlement, defying growing international protests" · 3 items · sources Al Jazeera, BBC World · principals Israel
- current system: one item not in any Development; cosine 0.53; tick 4: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · A report of settlers targeting homes in Qaryut versus a BBC explainer on settlement expansion.
- **owner verdict:** ____

### A026

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-c349800cdff6` · t2 | `b-bbcb00eae268` · t2 |
| published | 2026-08-21T12:32:03 | 2026-08-21T15:00:05 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | US allies in Asia wary as Trump moves military assets for Iran war | China and US push Southeast Asia over their AI blocs. Will it test region’s non-alignment? |
| current Development | - | - |
| places | Asia, China, US | Beijing, China, Southeast Asia, US, Washington |

- current system: neither in a Development; cosine 0.57; tick 4: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Asian allies' wariness over US asset moves for the Iran war versus an analysis of US-China AI blocs; different subjects.
- **owner verdict:** ____

### A027

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-7d87768d2f82` · t1 | `b-85e1f8c5197d` · t1 |
| published | 2026-08-21T05:47:32 | 2026-08-21T02:28:28 |
| source · lang | BBC World · en | South China Morning Post · en |
| headline | Hong Kong's Tiananmen activists guilty in national security trial | Hong Kong Tiananmen vigil organiser, former leaders guilty of inciting subversion |
| current Development | D1 | D1 |
| places | China, Hong Kong, Tiananmen | China, Hong Kong, Hong Kong Tiananmen, Tiananmen Square |

- D1: "Hong Kong Tiananmen vigil organiser, former leaders guilty of inciting subversion" · 3 items · sources Al Jazeera, BBC World, South China Morning Post · principals -
- current system: same Development D1; cosine 0.66; D1: grouped together at tick 1; D1: least similar members of a 3-item Development (cosine 0.66)
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report the guilty verdict against the Tiananmen vigil organisers under the national security law.
- **owner verdict:** ____

### A028  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-52e7176bac0a` · t1 | `b-9d435faf259d` · t4 |
| published | 2026-08-21T05:00:57 | 2026-08-22T15:45:40 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | Israel re-establishes closed West Bank settlement, defying growing international protests | Settlers target Palestinian homes in Occupied West Bank’s Area B |
| current Development | D6 | D6 |
| places | Israel, Palestine, West Bank | Israel, Occupied West Bank, Palestine, Qaryut |

- D6: "Israel re-establishes closed West Bank settlement, defying growing international protests" · 3 items · sources Al Jazeera, BBC World · principals Israel
- current system: same Development D6; cosine 0.65; D6: grouped together at tick 4; ticks 1 and 4, cosine 0.65: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Re-establishment of a closed settlement by 30 families is a different occurrence from settlers forcing families out in Qaryut.
- **owner verdict:** ____

### A029

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-6a2e684a65d2` · t2 | `b-422186e87411` · t3 |
| published | 2026-08-21T13:30:36 | 2026-08-22T11:15:39 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll passes 2,500: UN | Ebola continues to spread in the DRC as 16,000 vaccine doses arrive |
| current Development | - | D3 |
| places | Congo, DR | - |

- D3: "Ebola vaccine trial to start in DR Congo as warning issued over speed of infections" · 3 items · sources Al Jazeera, BBC World · principals -
- current system: one item not in any Development; cosine 0.76; not in any Development; closest member (cosine 0.76) is in D3; ticks 2 and 3, cosine 0.76: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence medium · The UN warning with the toll passing 2,500 (21 Aug) versus the vaccine dose arrival next day; the second headline's occurrence is the doses.
- **owner verdict:** ____

### A030

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-b3d4b7966b1a` · t1 | `b-9259fb4b9124` · t3 |
| published | 2026-08-21T01:30:06 | 2026-08-22T10:01:18 |
| source · lang | South China Morning Post · en | BBC World · en |
| headline | In the embodied AI race, China can opt to look beyond bigger models | Robot horse and rider steal the spotlight at Chinese conference |
| current Development | - | - |
| places | China | Beijing, China |

- current system: neither in a Development; cosine 0.57; tick 3: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · An opinion on China's embodied AI versus a report on the robot horse at a Beijing robotics conference.
- **owner verdict:** ____

### A031

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-52e7176bac0a` · t1 | `b-38eba7dee8c5` · t2 |
| published | 2026-08-21T05:00:57 | 2026-08-21T19:31:47 |
| source · lang | BBC World · en | BBC World · en |
| headline | Israel re-establishes closed West Bank settlement, defying growing international protests | How Israel is expanding settlements in drive to reshape West Bank |
| current Development | D6 | - |
| places | Israel, Palestine, West Bank | Israel, Palestine, West Bank |

- D6: "Israel re-establishes closed West Bank settlement, defying growing international protests" · 3 items · sources Al Jazeera, BBC World · principals Israel
- current system: one item not in any Development; cosine 0.69; not in any Development; closest member (cosine 0.69) is in D6; ticks 1 and 2, cosine 0.69: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · A report of one settlement being re-established versus a BBC explainer on how Israel is expanding settlements.
- **owner verdict:** ____

### A032

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-6a2e684a65d2` · t2 | `b-8826249c972c` · t3 |
| published | 2026-08-21T13:30:36 | 2026-08-22T10:13:56 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Ebola outbreak ‘growing faster, ⁠⁠wider’ as DRC death toll passes 2,500: UN | More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo |
| current Development | - | D3 |
| places | Congo, DR | Congo, Kinshasa |

- D3: "Ebola vaccine trial to start in DR Congo as warning issued over speed of infections" · 3 items · sources Al Jazeera, BBC World · principals -
- current system: one item not in any Development; cosine 0.67; ticks 2 and 3, cosine 0.67: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence high · The UN warning on outbreak spread (21 Aug) versus the arrival of 16,000 Ervebo doses (22 Aug).
- **owner verdict:** ____

### A033

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-3a527f407cc4` · t1 | `b-e736db6a6335` · t1 |
| published | 2026-08-21T01:38:37 | 2026-08-21T09:54:38 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Brazil launches AI supercomputer push while balancing US and Chinese tech | Embrace AI to boost competitiveness, Paul Chan says at tech festival opening |
| current Development | - | - |
| places | Brazil, China, US | Hong Kong |

- current system: neither in a Development; cosine 0.40; same tick, different outlets, cosine 0.40: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Brazil's AI investment versus Paul Chan opening Hong Kong's tech festival.
- **owner verdict:** ____


## Window 2026-08-31 (holdout)

### H001  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-627e1276af35` · t4 | `b-80b4e4856474` · t3 |
| published | 2026-09-01T18:26:12 | 2026-09-01T02:30:45 |
| source · lang | BBC World · en | BBC World · en |
| headline | Ex-gang boss guilty of orchestrating 1996 murder of rapper Tupac Shakur | What it was like inside court for Tupac Shakur’s murder trial verdict |
| current Development | - | - |
| places | - | - |

- current system: neither in a Development; cosine 0.71; ticks 3 and 4, cosine 0.71: not grouped together
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence medium · Both concern the guilty verdict against Duane 'Keffe D' Davis; the second is a courtroom eyewitness account of that verdict, not analysis.
- **owner verdict:** ____

### H002  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-341fac703447` · t2 | `b-8e5ef74bd47d` · t1 |
| published | 2026-08-31T13:43:32 | 2026-08-31T07:22:10 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | South Korea court gives church leader two years in jail for bribery | South Korea’s Unification Church leader Han Hak-ja jailed 2 years for bribing officials |
| current Development | D5 | D5 |
| places | South Korea | South Korea |

- D5: "South Korea’s Unification Church leader Han Hak-ja jailed 2 years for bribing officials" · 2 items · sources Al Jazeera, South China Morning Post · principals Han Hak-ja, South Korea, Unification Church
- current system: same Development D5; cosine 0.64; D5: grouped together at tick 2; ticks 1 and 2, cosine 0.64: same Development
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report a South Korean court jailing Unification Church leader Han Hak-ja for two years for bribery.
- **owner verdict:** ____

### H003  · flags: grows_same_id, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-f24f0531bb39` · t4 | `b-40456da07df1` · t1 |
| published | 2026-09-01T16:11:18 | 2026-08-31T06:05:26 |
| source · lang | BBC World · en | South China Morning Post · en |
| headline | River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC | Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000 |
| current Development | D2 | D2 |
| places | Nepal | China, Gyirong Port, Nepal |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: same Development D2; cosine 0.56; D2: attached at tick 4 to a Development created at tick 1; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both cover the Nepal-China border flood rescue, with the toll rising from ~903 to over 1,000; the BBC piece is a survivor account within continuing rescue coverage.
- **owner verdict:** ____

### H004

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-a5d8ac56e6a0` · t1 | `b-8c3f1988382e` · t1 |
| published | 2026-08-31T10:17:22 | 2026-08-31T00:31:51 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Nepal tunnel traps hinder flood rescue: How many are dead or missing? | One dead and about 15 people missing after flash flood in Grand Canyon |
| current Development | D1 | - |
| places | Nepal, Tibet | Bright Angel Canyon, Grand Canyon Dozens, US |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.60; not in any Development; closest member (cosine 0.60) is in D1
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · The Nepal-Tibet border floods and the Grand Canyon flash flood are separate disasters.
- **owner verdict:** ____

### H005

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-0db307cfbf6e` · t2 | `b-c011c687ae36` · t2 |
| published | 2026-08-31T22:07:19 | 2026-08-31T12:00:06 |
| source · lang | BBC World · en | South China Morning Post · en |
| headline | Japan Inc is betting big on India as China risks deepen | Why Japan’s hypersonic and underwater weapon plans might worry China |
| current Development | - | - |
| places | China, India, Japan | Australia, China, Japan, Taiwan, Tokyo |

- current system: neither in a Development; cosine 0.44; same tick, different outlets, cosine 0.44: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Japanese corporate investment in India versus Japan's weapons plans; unrelated, both analytical.
- **owner verdict:** ____

### H006

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-a5d8ac56e6a0` · t1 | `b-40456da07df1` · t1 |
| published | 2026-08-31T10:17:22 | 2026-08-31T06:05:26 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Nepal tunnel traps hinder flood rescue: How many are dead or missing? | Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000 |
| current Development | D1 | D2 |
| places | Nepal, Tibet | China, Gyirong Port, Nepal |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: different Developments; cosine 0.58; tick 3: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence low · The Al Jazeera 'How many are dead or missing?' piece is framed as an explainer/tally on the Nepal floods, versus SCMP's rescue report; same disaster.
- **owner verdict:** ____

### H007

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-04b8dd1b7e59` · t1 | `b-a5d8ac56e6a0` · t1 |
| published | 2026-08-31T00:19:04 | 2026-08-31T10:17:22 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Flash flooding in Grand Canyon leaves more than 20 people missing | Nepal tunnel traps hinder flood rescue: How many are dead or missing? |
| current Development | - | D1 |
| places | Arizona, Grand Canyon | Nepal, Tibet |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.59; not in any Development; closest member (cosine 0.59) is in D1
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · The Grand Canyon flash flood and the Nepal-Tibet floods are separate disasters.
- **owner verdict:** ____

### H008

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-40456da07df1` · t1 | `b-757c54159001` · t1 |
| published | 2026-08-31T06:05:26 | 2026-08-31T06:05:26 |
| source · lang | South China Morning Post · en | South China Morning Post · en |
| headline | Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000 | China warns of ‘major risk’ of glacier collapse as Tibet-Nepal death toll nears 1,000 |
| current Development | D2 | - |
| places | China, Gyirong Port, Nepal | China, Cuojian River, Nepal, Purepuqiang River, Tibet |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.61; not in any Development; closest member (cosine 0.61) is in D2
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence medium · China's Ministry of Water Resources warning of further glacier collapse is a distinct statement from the rescue-operations report, though both carry the same death toll.
- **owner verdict:** ____

### H009  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-8c136bee2610` · t2 | `b-2e80a96f5651` · t1 |
| published | 2026-08-31T14:50:36 | 2026-08-31T11:59:37 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | 'She slipped out of my hand' - children missing after ferry sinks off northern Cyprus | Rescuers search for 18 missing after boat capsizes off Northern Cyprus |
| current Development | - | - |
| places | Cyprus Ayten | Northern Cyprus |

- current system: neither in a Development; cosine 0.53; tick 2: link cut by segmentation guard 'disjoint_locations'
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Both report the ferry that capsized off Northern Cyprus with around 18-20 missing, with added details (8 dead, crew arrested).
- **owner verdict:** ____

### H010  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-eb0ab8f69ba6` · t2 | `b-b378591e2234` · t1 |
| published | 2026-08-31T13:39:12 | 2026-08-31T09:56:34 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Spain PM blames Russia, Israel for Ceuta migrant crisis’ disinformation | Spain’s Sanchez says Russia, Israel spread disinformation on Ceuta crisis |
| current Development | D6 | D6 |
| places | Africa, Ceuta, Israel, Morocco, Russia | Ceuta, Israel, Russia, Spain |

- D6: "Spain’s Sanchez says Russia, Israel spread disinformation on Ceuta crisis" · 2 items · sources Al Jazeera, South China Morning Post · principals Israel, Pedro Sanchez, Sanchez, Spain
- current system: same Development D6; cosine 0.71; D6: grouped together at tick 2; ticks 1 and 2, cosine 0.71: same Development
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Sanchez saying on Monday that Russia and Israel spread disinformation on the Ceuta crisis.
- **owner verdict:** ____

### H011

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-98df932ec432` · t1 | `b-e1d69e6c7217` · t1 |
| published | 2026-08-31T02:45:21 | 2026-08-31T10:12:38 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Nepal floods: could foreign rescue teams have been brought in earlier? | After the flash flood disaster, here is what Nepal really needs |
| current Development | D1 | - |
| places | China, Kathmandu, Nepal | Nepal |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.54; tick 2: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · An SCMP analysis on the timing of foreign rescue teams and an Al Jazeera opinion on Nepal's needs are both commentary, not one occurrence.
- **owner verdict:** ____

### H012

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-4320f84c3536` · t2 | `b-bf8b8b7b2085` · t1 |
| published | 2026-08-31T12:57:49 | 2026-08-31T11:49:03 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Pakistan, Saudi Arabia, Turkiye meet: What’s next for their defence pact? | Turkiye, Saudi Arabia, Pakistan hold first Mecca defence pact meeting |
| current Development | - | - |
| places | Iran, Pakistan, Saudi Arabia, Turkiye, US | Pakistan, Saudi Arabia, Turkiye |

- current system: neither in a Development; cosine 0.64; ticks 1 and 2, cosine 0.64: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · 'What's next for their defence pact?' is analysis; the other reports the first Mecca defence pact meeting.
- **owner verdict:** ____

### H013

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-a6b62e9f30e0` · t2 | `b-fc10bd046cfa` · t2 |
| published | 2026-08-31T14:57:56 | 2026-08-31T12:26:28 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Why has Greece signed a $3.5bn missile deal with Israel? | Israel and Greece sign US$3.5 billion defence deal, largest ever between the 2 |
| current Development | - | D3 |
| places | Greece, Iran, Israel, Turkiye, US | Greece, Israel, Mediterranean |

- D3: "Israel and Greece sign US$3.5 billion defence deal, largest ever between the 2" · 2 items · sources Al Jazeera, South China Morning Post · principals Greece, Israel
- current system: one item not in any Development; cosine 0.79; not in any Development; closest member (cosine 0.79) is in D3; tick 4: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · 'Why has Greece signed...' is an explainer; SCMP reports the $3.5bn Israel-Greece deal signing.
- **owner verdict:** ____

### H014  · flags: grows_same_id, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-40456da07df1` · t1 | `b-898d1b9dc809` · t3 |
| published | 2026-08-31T06:05:26 | 2026-09-01T06:02:27 |
| source · lang | South China Morning Post · en | BBC World · en |
| headline | Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000 | The final minutes before floodwater crashed through Nepal-China border |
| current Development | D2 | D2 |
| places | China, Gyirong Port, Nepal | China, India, Nepal |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: same Development D2; cosine 0.54; D2: attached at tick 3 to a Development created at tick 1; D2: least similar members of a 4-item Development (cosine 0.54)
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence low · The BBC reconstruction of the floodwater hitting the Nepal-China border crossing covers the same flood incident as SCMP's rescue update, but it is a narrative feature.
- **owner verdict:** ____

### H015

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-98df932ec432` · t1 | `b-b18d96e6fc10` · t1 |
| published | 2026-08-31T02:45:21 | 2026-08-31T07:34:14 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Nepal floods: could foreign rescue teams have been brought in earlier? | Nepal races to rescue trapped workers, as flood death toll surpasses 900 |
| current Development | D1 | D2 |
| places | China, Kathmandu, Nepal | Nepal |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: different Developments; cosine 0.66; tick 1: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · SCMP's question-headline analysis on whether foreign rescue teams should have come earlier versus Al Jazeera's rescue report with the toll past 900.
- **owner verdict:** ____

### H016

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-a5d8ac56e6a0` · t1 | `b-f24f0531bb39` · t4 |
| published | 2026-08-31T10:17:22 | 2026-09-01T16:11:18 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Nepal tunnel traps hinder flood rescue: How many are dead or missing? | River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC |
| current Development | D1 | D2 |
| places | Nepal, Tibet | Nepal |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: different Developments; cosine 0.65; tick 4: link cut by segmentation guard 'analysis_headline'; ticks 1 and 4, cosine 0.65: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence low · Al Jazeera's 'How many are dead or missing?' explainer versus the BBC survivor account within rescue coverage of the same flood.
- **owner verdict:** ____

### H017  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-b18d96e6fc10` · t1 | `b-f24f0531bb39` · t4 |
| published | 2026-08-31T07:34:14 | 2026-09-01T16:11:18 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Nepal races to rescue trapped workers, as flood death toll surpasses 900 | River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC |
| current Development | D2 | D2 |
| places | Nepal | Nepal |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: same Development D2; cosine 0.69; ticks 1 and 4, cosine 0.69: same Development
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both cover the rescue of trapped hydropower workers in the Nepal flood; the toll rises from over 900 to over 1,000.
- **owner verdict:** ____

### H018  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-627e1276af35` · t4 | `b-74a7d55cfb9b` · t3 |
| published | 2026-09-01T18:26:12 | 2026-09-01T00:31:20 |
| source · lang | BBC World · en | BBC World · en |
| headline | Ex-gang boss guilty of orchestrating 1996 murder of rapper Tupac Shakur | Watch: Moment Duane 'Keffe D' Davis is found guilty of Tupac Shakur's murder |
| current Development | - | - |
| places | - | - |

- current system: neither in a Development; cosine 0.84; ticks 3 and 4, cosine 0.84: not grouped together
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Duane 'Keffe D' Davis being found guilty of Tupac Shakur's murder.
- **owner verdict:** ____

### H019

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-bf8b8b7b2085` · t1 | `b-4987459dba37` · t1 |
| published | 2026-08-31T11:49:03 | 2026-08-31T04:30:00 |
| source · lang | Al Jazeera · en | Breaking Defense · en |
| headline | Turkiye, Saudi Arabia, Pakistan hold first Mecca defence pact meeting | The Mecca pact explained, tankers for Qatar, and CENTCOM’s new drone force |
| current Development | - | - |
| places | Pakistan, Saudi Arabia, Turkiye | Dubai, Middle East Bureau, Qatar |

- current system: neither in a Development; cosine 0.60; tick 1: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · A report of the first Mecca pact meeting versus a Breaking Defense 'explained' recap/podcast.
- **owner verdict:** ____

### H020

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-98df932ec432` · t1 | `b-f24f0531bb39` · t4 |
| published | 2026-08-31T02:45:21 | 2026-09-01T16:11:18 |
| source · lang | South China Morning Post · en | BBC World · en |
| headline | Nepal floods: could foreign rescue teams have been brought in earlier? | River water smashed into tunnel and chased me for 20 minutes, Nepal worker tells BBC |
| current Development | D1 | D2 |
| places | China, Kathmandu, Nepal | Nepal |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: different Developments; cosine 0.60; tick 4: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · SCMP analysis on foreign rescue teams versus the BBC survivor account and rescue update.
- **owner verdict:** ____

### H021  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-df14f0a7ac2b` · t2 | `b-d71f2886d120` · t1 |
| published | 2026-08-31T22:05:43 | 2026-08-31T07:10:04 |
| source · lang | BBC World · en | South China Morning Post · en |
| headline | Orangutans in danger as wildfires blaze through Borneo | Malaysia’s air quality turns hazardous as Indonesian wildfires burn |
| current Development | D4 | D4 |
| places | Borneo, Indonesia | Indonesia, Kuching, Malaysia, Samarahan, Sarawak |

- D4: "Malaysia’s air quality turns hazardous as Indonesian wildfires burn" · 2 items · sources BBC World, South China Morning Post · principals Indonesia, Malaysia
- current system: same Development D4; cosine 0.56; D4: grouped together at tick 2
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · Same Indonesian wildfires, but orangutan habitat loss in Borneo and hazardous haze in Sarawak are different reported occurrences, neither a rewrite of the other.
- **owner verdict:** ____

### H022

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-2d14afc54339` · t2 | `b-fc10bd046cfa` · t2 |
| published | 2026-08-31T13:52:40 | 2026-08-31T12:26:28 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Greece signs $3.5bn air defence deal with Israel | Israel and Greece sign US$3.5 billion defence deal, largest ever between the 2 |
| current Development | D3 | D3 |
| places | Greece, Israel | Greece, Israel, Mediterranean |

- D3: "Israel and Greece sign US$3.5 billion defence deal, largest ever between the 2" · 2 items · sources Al Jazeera, South China Morning Post · principals Greece, Israel
- current system: same Development D3; cosine 0.75; D3: grouped together at tick 2
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Greece and Israel signing the $3.5bn air-defence deal on Monday.
- **owner verdict:** ____

### H023

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-193b898b20bc` · t1 | `b-40456da07df1` · t1 |
| published | 2026-08-31T04:19:22 | 2026-08-31T06:05:26 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | People return to their flood-ravaged homes in Nepal | Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000 |
| current Development | - | D2 |
| places | Nepal, Nuwakot | China, Gyirong Port, Nepal |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.49; same tick, different outlets, cosine 0.49: below the link threshold, never grouped
- **proposed:** `AMBIGUOUS` · confidence low · Survivors returning home in Nuwakot may be aftermath of the same border flood covered by SCMP's rescue report, or a distinct recovery occurrence; the text cannot decide.
- **owner verdict:** ____

### H024  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-a5d8ac56e6a0` · t1 | `b-98df932ec432` · t1 |
| published | 2026-08-31T10:17:22 | 2026-08-31T02:45:21 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | Nepal tunnel traps hinder flood rescue: How many are dead or missing? | Nepal floods: could foreign rescue teams have been brought in earlier? |
| current Development | D1 | D1 |
| places | Nepal, Tibet | China, Kathmandu, Nepal |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- current system: same Development D1; cosine 0.64; D1: grouped together at tick 1
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · Both are explainer/analysis pieces on the Nepal floods (a tally and a question on foreign rescue help), not one occurrence.
- **owner verdict:** ____

### H025

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-a5d8ac56e6a0` · t1 | `b-adea0d13d447` · t1 |
| published | 2026-08-31T10:17:22 | 2026-08-31T00:31:51 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | Nepal tunnel traps hinder flood rescue: How many are dead or missing? | Dozens evacuated and about 15 missing after Grand Canyon flash flood |
| current Development | D1 | - |
| places | Nepal, Tibet | Colorado River, Grand Canyon |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.56; not in any Development; closest member (cosine 0.56) is in D1
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · The Nepal floods and the Grand Canyon flash flood are separate disasters.
- **owner verdict:** ____

### H026

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-898d1b9dc809` · t3 | `b-a5d8ac56e6a0` · t1 |
| published | 2026-09-01T06:02:27 | 2026-08-31T10:17:22 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | The final minutes before floodwater crashed through Nepal-China border | Nepal tunnel traps hinder flood rescue: How many are dead or missing? |
| current Development | D2 | D1 |
| places | China, India, Nepal | Nepal, Tibet |

- D1: "Nepal floods: could foreign rescue teams have been brought in earlier?" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: different Developments; cosine 0.70; separate Developments D1 and D2 (closest items cosine 0.70; shared principals ['Nepal']); tick 3: link cut by segmentation guard 'analysis_headline'; ticks 1 and 3, cosine 0.70: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence low · The BBC reconstruction of the flood at the border crossing versus Al Jazeera's 'How many are dead or missing?' explainer.
- **owner verdict:** ____

### H027

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-40456da07df1` · t1 | `b-b18d96e6fc10` · t1 |
| published | 2026-08-31T06:05:26 | 2026-08-31T07:34:14 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000 | Nepal races to rescue trapped workers, as flood death toll surpasses 900 |
| current Development | D2 | D2 |
| places | China, Gyirong Port, Nepal | Nepal |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: same Development D2; cosine 0.65; D2: grouped together at tick 1
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Both report the intensifying rescue in the Nepal-China flood zone with the toll around 900-1,000.
- **owner verdict:** ____

### H028

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-e1d69e6c7217` · t1 | `b-40456da07df1` · t1 |
| published | 2026-08-31T10:12:38 | 2026-08-31T06:05:26 |
| source · lang | Al Jazeera · en | South China Morning Post · en |
| headline | After the flash flood disaster, here is what Nepal really needs | Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000 |
| current Development | - | D2 |
| places | Nepal | China, Gyirong Port, Nepal |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.52; same tick, different outlets, cosine 0.52: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · An Al Jazeera opinion on what Nepal needs versus SCMP's rescue report.
- **owner verdict:** ____

### H029

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-193b898b20bc` · t1 | `b-b18d96e6fc10` · t1 |
| published | 2026-08-31T04:19:22 | 2026-08-31T07:34:14 |
| source · lang | Al Jazeera · en | Al Jazeera · en |
| headline | People return to their flood-ravaged homes in Nepal | Nepal races to rescue trapped workers, as flood death toll surpasses 900 |
| current Development | - | D2 |
| places | Nepal, Nuwakot | Nepal |

- D2: "Rescue work intensifies as death toll in China-Nepal disaster approaches 1,000" · 4 items · sources Al Jazeera, BBC World, South China Morning Post · principals Nepal
- current system: one item not in any Development; cosine 0.60; not in any Development; closest member (cosine 0.60) is in D2
- **proposed:** `AMBIGUOUS` · confidence low · Nuwakot residents returning home could be aftermath of the same flood as the tunnel rescue report, or a separate recovery occurrence.
- **owner verdict:** ____

### H030

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-fc10bd046cfa` · t2 | `b-4320f84c3536` · t2 |
| published | 2026-08-31T12:26:28 | 2026-08-31T12:57:49 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Israel and Greece sign US$3.5 billion defence deal, largest ever between the 2 | Pakistan, Saudi Arabia, Turkiye meet: What’s next for their defence pact? |
| current Development | D3 | - |
| places | Greece, Israel, Mediterranean | Iran, Pakistan, Saudi Arabia, Turkiye, US |

- D3: "Israel and Greece sign US$3.5 billion defence deal, largest ever between the 2" · 2 items · sources Al Jazeera, South China Morning Post · principals Greece, Israel
- current system: one item not in any Development; cosine 0.48; same tick, different outlets, cosine 0.48: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · The Israel-Greece arms deal versus analysis of the Pakistan-Saudi-Turkiye defence pact.
- **owner verdict:** ____


## Window 2026-09-25 (development)

### B001

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-17f8645e6056` · t4 | `b-d4cad9c5fd6c` · t4 |
| published | 2026-09-25T07:02:44 | 2026-09-25T06:56:51 |
| source · lang | South China Morning Post · en | Al Jazeera · en |
| headline | Flood-ravaged Nepal pushes for climate deal with India, China | Nepal’s leader labels devastating flood a ‘warning to the world’ |
| current Development | D4 | D4 |
| places | China, Himalaya, India, Nepal, New York | Nepal |

- D4: "Nepal’s leader labels devastating flood a ‘warning to the world’" · 2 items · sources Al Jazeera, South China Morning Post · principals Nepal
- current system: same Development D4; cosine 0.63; D4: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Nepal PM Balendra Shah's UN address calling for climate action after the floods.
- **owner verdict:** ____

### B002  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-5d1ba8e525da` · t3 | `b-d72e5f6a5e01` · t3 |
| published | 2026-09-24T18:03:00 | 2026-09-24T16:33:41 |
| source · lang | Breaking Defense · en | Defense News · en |
| headline | OCCAR awards $4.2B DDX destroyer contract to Fincantieri, Leonardo joint venture | Italy taps state-owned firms to build two naval destroyers in $4.2 billion deal |
| current Development | - | - |
| places | Italy | Italy, ROME |

- current system: neither in a Development; cosine 0.52; same tick, different outlets, cosine 0.52: below the link threshold, never grouped
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report the OCCAR-brokered $4.2bn DDX destroyer contract for Italy with Fincantieri/Leonardo.
- **owner verdict:** ____

### B003  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-8a758a84c401` · t4 | `b-256c7087fa4e` · t3 |
| published | 2026-09-25T02:07:29 | 2026-09-24T19:32:59 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Meloni government bans burqas, caps foreign students in Italian schools | Italy ministers agree to ban burqa and niqab in school and cap foreigners in class |
| current Development | D3 | D3 |
| places | Italy | Italy |

- D3: "Italy ministers agree to ban burqa and niqab in school and cap foreigners in class" · 2 items · sources Al Jazeera, BBC World · principals Giorgia Meloni, Italy, Meloni
- current system: same Development D3; cosine 0.73; D3: grouped together at tick 4; ticks 3 and 4, cosine 0.73: same Development
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Meloni's ministers agreeing to ban burqas/niqabs in schools and cap foreign students.
- **owner verdict:** ____

### B004  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-63cb0d4f2400` · t4 | `b-9796005bb46b` · t4 |
| published | 2026-09-25T08:09:26 | 2026-09-25T05:48:05 |
| source · lang | BBC World · en | South China Morning Post · en |
| headline | Trump and Xi exchange warm words at state dinner but little progress on key issues | From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism |
| current Development | - | - |
| places | - | China, East Room, United States |

- current system: neither in a Development; cosine 0.49; same tick, different outlets, cosine 0.49: below the link threshold, never grouped
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence medium · Both report the Trump-Xi White House state dinner; BBC adds an assessment of little progress, SCMP details its symbolism.
- **owner verdict:** ____

### B005

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-9796005bb46b` · t4 | `b-683038d2cd37` · t4 |
| published | 2026-09-25T05:48:05 | 2026-09-25T08:05:54 |
| source · lang | South China Morning Post · en | South China Morning Post · en |
| headline | From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism | Trump gives Xi a tour of his pet White House building projects, including the ballroom |
| current Development | - | D1 |
| places | China, East Room, United States | Beijing, China, Great Hall of the People, Oval Office, South Lawn |

- D1: "Xi got Trump's red carpet welcome - but not everything he wanted" · 2 items · sources BBC World, South China Morning Post · principals Donald Trump, Trump, Xi Jinping
- current system: one item not in any Development; cosine 0.56; not in any Development; closest member (cosine 0.56) is in D1
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · The state dinner and Trump's tour of White House building works for Xi are separate occurrences in the same visit.
- **owner verdict:** ____

### B006

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-fee27e429610` · t4 | `b-3d9601881311` · t4 |
| published | 2026-09-25T00:44:04 | 2026-09-25T03:49:43 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | Netanyahu defends Israeli military action as delegates walk out before UN speech | Jewish protestors join Free Palestine march to denounce Netanyahu |
| current Development | - | - |
| places | Israel | Palestine |

- current system: neither in a Development; cosine 0.50; same tick, different outlets, cosine 0.50: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (reaction) · confidence medium · Netanyahu's UN speech and the walkout differ from a Free Palestine street march denouncing him.
- **owner verdict:** ____

### B007  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-6e3eb47c7f66` · t3 | `b-aa291f31d75e` · t1 |
| published | 2026-09-24T15:56:32 | 2026-09-23T15:38:14 |
| source · lang | Breaking Defense · en | Defense News · en |
| headline | The Air Force says its China think tank will continue. Its director says it’s basically dead. | Air Force, civilian staff dispute status of China Aerospace Studies Institute |
| current Development | - | - |
| places | China | - |

- current system: neither in a Development; cosine 0.58; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both report the dispute between the Air Force and CASI's director over eliminating the institute's civilian staff.
- **owner verdict:** ____

### B008  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-683038d2cd37` · t4 | `b-97cb65d1a469` · t4 |
| published | 2026-09-25T08:05:54 | 2026-09-25T03:57:09 |
| source · lang | South China Morning Post · en | BBC World · en |
| headline | Trump gives Xi a tour of his pet White House building projects, including the ballroom | Xi got Trump's red carpet welcome - but not everything he wanted |
| current Development | D1 | D1 |
| places | Beijing, China, Great Hall of the People, Oval Office, South Lawn | China, Taiwan |

- D1: "Xi got Trump's red carpet welcome - but not everything he wanted" · 2 items · sources BBC World, South China Morning Post · principals Donald Trump, Trump, Xi Jinping
- current system: same Development D1; cosine 0.54; D1: grouped together at tick 4
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · A report of Trump's building tour for Xi versus BBC analysis of what Xi did and did not get from the visit.
- **owner verdict:** ____

### B009

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-453ee4cac113` · t3 | `b-361a029728da` · t3 |
| published | 2026-09-24T15:49:22 | 2026-09-24T12:34:00 |
| source · lang | Defense News · en | Breaking Defense · en |
| headline | Why the last tactical mile is crucial to acquisition reform | Navy wants more offensive, ‘expeditionary’ cyber capabilities |
| current Development | - | - |
| places | - | - |

- current system: neither in a Development; cosine 0.44; same tick, different outlets, cosine 0.44: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · An acquisition-reform opinion piece versus the Navy's cyber advisor seeking expeditionary cyber; unrelated.
- **owner verdict:** ____

### B010

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-683038d2cd37` · t4 | `b-f2fe2e86b26c` · t4 |
| published | 2026-09-25T08:05:54 | 2026-09-25T07:00:17 |
| source · lang | South China Morning Post · en | South China Morning Post · en |
| headline | Trump gives Xi a tour of his pet White House building projects, including the ballroom | Xi-Trump dinner puts US tech titans in spotlight – what does it mean for China ties? |
| current Development | D1 | - |
| places | Beijing, China, Great Hall of the People, Oval Office, South Lawn | Beijing, China, United States, Washington |

- D1: "Xi got Trump's red carpet welcome - but not everything he wanted" · 2 items · sources BBC World, South China Morning Post · principals Donald Trump, Trump, Xi Jinping
- current system: one item not in any Development; cosine 0.58; not in any Development; closest member (cosine 0.58) is in D1
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · A report of the White House building tour versus analysis of tech titans' seating at the state dinner.
- **owner verdict:** ____

### B011  · flags: should_split, same_story_new_action

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `b-38730424bfbc` · t4 | `b-14aae9d37ebe` · t3 |
| published | 2026-09-25T04:22:10 | 2026-09-24T19:02:36 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Pakistani forces kill Afghan Taliban fighters in border escalation | Four civilians killed in Pakistani strikes in Afghanistan, Taliban says |
| current Development | D2 | D2 |
| places | Afghanistan, Pakistan | Afghanistan, Pakistan |

- D2: "Four civilians killed in Pakistani strikes in Afghanistan, Taliban says" · 2 items · sources Al Jazeera, BBC World · principals Pakistan, Taliban
- current system: same Development D2; cosine 0.61; D2: grouped together at tick 4; ticks 3 and 4, cosine 0.61: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence medium · Pakistani strikes on 10 targets in Afghanistan killing four civilians (24 Sep) differ from later cross-border fire killing Taliban fighters (25 Sep).
- **owner verdict:** ____


## Window 2026-09-30-multilingual (development)

### C001  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-129` · t3 | `sx-133` · t3 |
| published | 2026-09-29 23:05:00.000000 | 2026-09-29 19:21:00.000000 |
| source · lang | Rai News Esteri · it | Rai News Esteri · it |
| headline | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" | Gli Usa prestano alle aziende energetiche 40 milioni di barili di petrolio delle riserve strategiche |
| current Development | D6 | D6 |
| places | - | Paesi, U.S. |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.47; D6: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Experts criticising Big Tech AI self-regulation vs US lending 40m barrels from strategic reserves: unrelated occurrences.
- **owner verdict:** ____

### C002  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-48` · t4 | `sx-129` · t3 |
| published | 2026-09-30 01:10:48.000000 | 2026-09-29 23:05:00.000000 |
| source · lang | ANSA Mondo · it | Rai News Esteri · it |
| headline | Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza' | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.65; D6: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Trump signing the Super Intelligence executive order vs an experts' critique piece on Big Tech self-regulation.
- **owner verdict:** ____

### C003  · flags: should_split, same_story_new_action, single_source_below_development

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-553` · t2 | `sx-554` · t2 |
| published | 2026-09-29 00:00:00.000000 | 2026-09-29 00:00:00.000000 |
| source · lang | Federal Register · en | Federal Register · en |
| headline | Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory | Accreditation and Approval of Intertek USA, Inc. (Carteret, NJ), as a Commercial Gauger and Laboratory |
| current Development | D1 | D1 |
| places | - | Carteret, NJ |

- D1: "Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and" · 2 items · sources Federal Register · principals -
- current system: same Development D1; cosine 0.85; D1: grouped together at tick 2
- **proposed:** `DIFFERENT_DEVELOPMENT` (repeat) · confidence high · Two separate CBP accreditation notices for different Intertek sites (Chelsea MA vs Carteret NJ) with different dates.
- **owner verdict:** ____

### C004

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-105` · t3 | `sx-256` · t3 |
| published | 2026-09-29 23:23:58.000000 | 2026-09-29 15:00:18.000000 |
| source · lang | BBC Mundo · es | El País Internacional · es |
| headline | "Tom Cruise asume el mayor riesgo de su carrera": la crítica de la BBC de Digger, la nueva película de González Iñárritu | Andy Burnham coloca la crisis de la vivienda como prioridad de su programa de Gobierno |
| current Development | - | D12 |
| places | - | Gobierno, Liverpool |

- D12: "«Hope again», l’appello di Burnham agli inglesi tra stop alle privatizzazioni e riforma de" · 2 items · sources El País Internacional, Il Sole 24 Ore Mondo · principals Andy Burnham, Burnham
- current system: one item not in any Development; cosine 0.41; same tick, different outlets, cosine 0.41: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · BBC film review of Inarritu's Digger vs Andy Burnham's housing programme at Labour conference.
- **owner verdict:** ____

### C005

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-421` · t3 | `sx-424` · t1 |
| published | 2026-09-29 16:41:05.000000 | 2026-09-28 23:02:52.000000 |
| source · lang | UN Press · en | UN Press · en |
| headline | At ‘Most Dangerous Nuclear Moment’ Since Cold War Ended, Secretary-General Observance Message Urges Changing Course, Replacing Threats with Dialogue | International Security Rapidly Deteriorates; General Assembly Urges Nations to Address Weaker Global Arms Treaties and Heightened Nuclear Risks |
| current Development | - | - |
| places | New York | Middle East |

- current system: neither in a Development; cosine 0.64; ticks 3 and 1, cosine 0.64: not grouped together
- **proposed:** `AMBIGUOUS` · confidence low · Guterres' remarks at the plenary for the International Day for Total Elimination of Nuclear Weapons may be part of the GA high-level meeting summarised in item 2, but publication dates (28 vs 29 Sep 'today') leave it unclear whether it is the same meeting.
- **owner verdict:** ____

### C006  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-264` · t3 | `sx-536` · t4 |
| published | 2026-09-29 22:45:03.000000 | 2026-09-30 01:15:00.000000 |
| source · lang | Clarín Mundo · es | GDELT · en |
| headline | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico | Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability |
| current Development | D20 | D20 |
| places | Estados Unidos, Irán | Iran, Syria |

- D20: "Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuer" · 3 items · sources Clarín Mundo, Europa Press Internacional, GDELT · principals Iran, Irán
- current system: same Development D20; cosine 0.55; D20: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report the Iranian currency hitting a record low amid war, within hours of each other.
- **owner verdict:** ____

### C007  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-131` · t3 | `sx-129` · t3 |
| published | 2026-09-29 23:32:00.000000 | 2026-09-29 23:05:00.000000 |
| source · lang | Rai News Esteri · it | Rai News Esteri · it |
| headline | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.53; D6: grouped together at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Trump's White House lunch with tech leaders vs an experts' critique piece on AI self-regulation.
- **owner verdict:** ____

### C008

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-257` · t2 | `sx-109` · t2 |
| published | 2026-09-29 03:40:00.000000 | 2026-09-29 00:41:14.000000 |
| source · lang | El País Internacional · es | BBC Mundo · es |
| headline | El monte Athos, el feudo de monjes de Europa que prohíbe la entrada de mujeres | Una niña prodigio británica de 11 años se convierte en la gran maestra más joven de la historia del ajedrez |
| current Development | - | - |
| places | Athos, Europa, San Gregorio | Inglaterra |

- current system: neither in a Development; cosine 0.48; same tick, different outlets, cosine 0.48: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Feature on Mount Athos vs 11-year-old British chess grandmaster record.
- **owner verdict:** ____

### C009

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-232` · t4 | `sx-122` · t4 |
| published | 2026-09-30 09:25:00.000000 | 2026-09-30 07:58:00.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | Rai News Esteri · it |
| headline | Allarme su volo FlyDubai dirottato, copilota accoltella comandante. Tentativo di far schiantare l’aereo | Volo Flydubai, l'aereo diretto a Tel Aviv viene deviato in Arabia Saudita |
| current Development | D21 | D21 |
| places | Dubai, Israele | Tel Aviv |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: same Development D21; cosine 0.73; D21: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Same FlyDubai Dubai-Israel flight diverted to Saudi Arabia after a cockpit fight; item 1 adds later details (stabbing, crash attempt).
- **owner verdict:** ____

### C010

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-85` · t4 | `sx-154` · t4 |
| published | 2026-09-30 05:24:52.000000 | 2026-09-30 09:14:47.000000 |
| source · lang | BBC World · en | France 24 · en |
| headline | South Korea demands apology from Pyongyang for landmine blasts that injured three | Tensions mount as South Korea demands apology from North over mine blast |
| current Development | D17 | D17 |
| places | Pyongyang, South Korea | North, South Korea |

- D17: "South Korea demands apology from Pyongyang for landmine blasts that injured three" · 3 items · sources Al Jazeera, BBC World, France 24 · principals South Korea
- current system: same Development D17; cosine 0.73; D17: grouped together at tick 4; D17: least similar members of a 3-item Development (cosine 0.73)
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both headline South Korea's demand for an apology over the DMZ mine blasts injuring three; France 24 adds North Korea's rejection.
- **owner verdict:** ____

### C011

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-1` · t4 | `sx-164` · t4 |
| published | 2026-09-30 07:00:24.000000 | 2026-09-30 01:04:01.000000 |
| source · lang | Defense.gov · en | France 24 · en |
| headline | Statement by Chief Pentagon Spokesman Sean Parnell on the Conclusion of the U.S. Military Mission in Iraq | US forces leave Iraq, raising fears of Iran-backed militias amid power vacuum |
| current Development | D9 | D9 |
| places | Iraq, U.S. | Iran, Iraq, U.S. |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: same Development D9; cosine 0.30; D9: least similar members of a 5-item Development (cosine 0.30)
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Pentagon statement on formally concluding Operation Inherent Resolve and France 24 report of US forces leaving remaining Iraqi bases on Wednesday describe the same withdrawal/conclusion.
- **owner verdict:** ____

### C012  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-131` · t3 | `sx-263` · t3 |
| published | 2026-09-29 23:32:00.000000 | 2026-09-29 18:24:27.000000 |
| source · lang | Rai News Esteri · it | El País Internacional · es |
| headline | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia | Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.59; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Trump's Big Tech lunch summit vs the separate launch of the America.gov website.
- **owner verdict:** ____

### C013

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-275` · t4 | `sx-161` · t4 |
| published | 2026-09-30 08:14:48.000000 | 2026-09-30 05:35:15.000000 |
| source · lang | Kyiv Independent · en | France 24 · en · ROUNDUP |
| headline | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack | Live: Several people killed as Russia launches new round of strikes on Kyiv |
| current Development | D15 | D15 |
| places | Kyiv, Russia, Ukraine | Kyiv, Poland, Russia, Ukraine |

- D15: "Live: Several people killed as Russia launches new round of strikes on Kyiv" · 3 items · sources France 24, Kyiv Independent · principals Russia
- current system: same Development D15; cosine 0.62; D15: grouped together at tick 4; D15: least similar members of a 3-item Development (cosine 0.62)
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Same overnight 29-30 Sep Russian missile and drone attack on Kyiv/Ukraine; later report has higher toll.
- **owner verdict:** ____

### C014

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-238` · t3 | `sx-131` · t3 |
| published | 2026-09-29 19:04:00.000000 | 2026-09-29 23:32:00.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | Rai News Esteri · it |
| headline | Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence | Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.56; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence medium · Both report Trump's White House lunch/summit with AI and tech leaders on 29 Sep inaugurating the 'Super Intelligence' era.
- **owner verdict:** ____

### C015

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-126` · t4 | `sx-179` · t4 |
| published | 2026-09-30 04:08:00.000000 | 2026-09-30 02:50:18.000000 |
| source · lang | Rai News Esteri · it | France 24 Español · es |
| headline | Marocco, il re Mohammed VI incontra la nuova premier El Mansouri | Informe desde Caracas: Delcy Rodríguez solicita una reforma de la "Ley contra el Odio" |
| current Development | D18 | - |
| places | Marocco | Caracas, Venezuela |

- D18: "Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno" · 3 items · sources Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: one item not in any Development; cosine 0.42; same tick, different outlets, cosine 0.42: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Moroccan king meets new PM vs Delcy Rodriguez asks to reform Venezuela's hate law.
- **owner verdict:** ____

### C016

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-168` · t3 | `sx-209` · t4 |
| published | 2026-09-29 21:05:00.000000 | 2026-09-30 03:00:59.000000 |
| source · lang | France 24 · en | Al Jazeera · en |
| headline | Trump says he doesn't want to work with China on AI safety | Trump backs AI self-regulation at tech summit but is it enough? |
| current Development | - | - |
| places | China, South Korea, U.S. | U.S. |

- current system: neither in a Development; cosine 0.66; ticks 3 and 4, cosine 0.66: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · Trump's statement refusing AI safety cooperation with China vs an Al Jazeera 'is it enough?' assessment of the self-regulation deal.
- **owner verdict:** ____

### C017  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-238` · t3 | `sx-129` · t3 |
| published | 2026-09-29 19:04:00.000000 | 2026-09-29 23:05:00.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | Rai News Esteri · it |
| headline | Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.69; D6: grouped together at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Report of Trump's order and AI lunch vs experts' critique piece on self-regulation.
- **owner verdict:** ____

### C018

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-239` · t3 | `sx-126` · t4 |
| published | 2026-09-29 18:07:00.000000 | 2026-09-30 04:08:00.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | Rai News Esteri · it |
| headline | Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno | Marocco, il re Mohammed VI incontra la nuova premier El Mansouri |
| current Development | D18 | D18 |
| places | Marocco, Marrakech, Regno | Marocco |

- D18: "Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno" · 3 items · sources Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: same Development D18; cosine 0.65; D18: grouped together at tick 4; ticks 4 and 3, cosine 0.65: same Development
- **proposed:** `AMBIGUOUS` · confidence low · El Mansouri's selection as PM vs the king's official palace meeting with her 'after the appointment'; unclear whether the audience is the appointment act itself or a subsequent meeting.
- **owner verdict:** ____

### C019

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-510` · t3 | `sx-488` · t3 |
| published | 2026-09-29 16:59:08.000000 | 2026-09-29 16:18:42.000000 |
| source · lang | Breaking Defense · en | Defense News · en |
| headline | Raytheon nets potential $20.7 billion AMRAAM deal | Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production |
| current Development | D2 | D2 |
| places | - | - |

- D2: "Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production" · 2 items · sources Breaking Defense, Defense News · principals Raytheon, US Department of Defense
- current system: same Development D2; cosine 0.76; D2: grouped together at tick 3
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report the Pentagon's up-to-$20.7bn AMRAAM contract award to Raytheon.
- **owner verdict:** ____

### C020

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-126` · t4 | `sx-56` · t3 |
| published | 2026-09-30 04:08:00.000000 | 2026-09-29 20:36:05.000000 |
| source · lang | Rai News Esteri · it | ANSA Mondo · it |
| headline | Marocco, il re Mohammed VI incontra la nuova premier El Mansouri | Haiti, l'Onu proroga di sei mesi la missione contro le bande armate |
| current Development | D18 | - |
| places | Marocco | Haiti |

- D18: "Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno" · 3 items · sources Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: one item not in any Development; cosine 0.57; not in any Development; closest member (cosine 0.57) is in D18
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Morocco king meets new PM vs UN extends Haiti mission by six months.
- **owner verdict:** ____

### C021  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-208` · t4 | `sx-88` · t3 |
| published | 2026-09-30 03:53:39.000000 | 2026-09-29 21:55:13.000000 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Public workers in France strike over pay as student protests turn violent | More than 400 detained as France student protests escalate |
| current Development | D24 | D24 |
| places | France | France |

- D24: "More than 400 detained as France student protests escalate" · 2 items · sources Al Jazeera, BBC World · principals -
- current system: same Development D24; cosine 0.66; D24: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both report the same 29 Sep French student protest clashes with 400-440 arrests; Al Jazeera also covers the concurrent public-worker strike.
- **owner verdict:** ____

### C022  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-71` · t3 | `sx-176` · t4 |
| published | 2026-09-29 23:02:47.000000 | 2026-09-30 03:29:14.000000 |
| source · lang | Europa Press Internacional · es | France 24 Español · es |
| headline | Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" |
| current Development | D6 | D6 |
| places | Estados Unidos, Gobierno, Gobierno de EEUU | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.67; ticks 3 and 4, cosine 0.67: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · Executive order renaming AI 'superintelligence' in agencies vs the separate 'morally binding' self-regulation accord with tech leaders, both on the same day.
- **owner verdict:** ____

### C023

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-273` · t3 | `sx-267` · t3 |
| published | 2026-09-29 16:03:03.000000 | 2026-09-29 20:42:05.000000 |
| source · lang | Clarín Mundo · es | Clarín Mundo · es |
| headline | "Jamás frenaré el crecimiento" de la IA, dice Trump antes de reunirse con los mayores ejecutivos del sector | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA |
| current Development | - | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.59; not in any Development; closest member (cosine 0.59) is in D6
- **proposed:** `DIFFERENT_DEVELOPMENT` (preview) · confidence medium · Trump's 'never curb growth' remark at the America.gov launch before the meeting vs his announcement after the meeting that tech leaders signed an accord.
- **owner verdict:** ____

### C024

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-128` · t4 | `sx-133` · t3 |
| published | 2026-09-30 01:54:00.000000 | 2026-09-29 19:21:00.000000 |
| source · lang | Rai News Esteri · it | Rai News Esteri · it |
| headline | USA, stretta finale su Cuba. Stangata bancaria, stop ai viaggi e blocco finanziario | Gli Usa prestano alle aziende energetiche 40 milioni di barili di petrolio delle riserve strategiche |
| current Development | - | D6 |
| places | Cancellate, Cuba, U.S. | Paesi, U.S. |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.60; not in any Development; closest member (cosine 0.60) is in D6
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · US financial/travel squeeze on Cuba vs US loan of strategic petroleum reserve barrels to energy firms.
- **owner verdict:** ____

### C025

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-127` · t4 | `sx-42` · t4 |
| published | 2026-09-30 04:06:00.000000 | 2026-09-30 08:28:59.000000 |
| source · lang | Rai News Esteri · it | ANSA Mondo · it |
| headline | Marocco, Fatima Zahara Mansouri è la prima donna premier della storia del Paese | Fonti Ue, 'boom nelle spesa in difesa, fino a 547 miliardi entro il 2029' |
| current Development | D18 | - |
| places | Marocco, Marrakech, Paese Avvocata, Regno | Fonti Ue |

- D18: "Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno" · 3 items · sources Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: one item not in any Development; cosine 0.56; not in any Development; closest member (cosine 0.56) is in D18
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Morocco's first woman PM vs EDA estimate of EU defence spending.
- **owner verdict:** ____

### C026  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-264` · t3 | `sx-75` · t4 |
| published | 2026-09-29 22:45:03.000000 | 2026-09-30 08:42:46.000000 |
| source · lang | Clarín Mundo · es | Europa Press Internacional · es |
| headline | Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz |
| current Development | D20 | D20 |
| places | Estados Unidos, Irán | EE.UU., Estados Unidos, Irán, Teheran |

- D20: "Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuer" · 3 items · sources Clarín Mundo, Europa Press Internacional, GDELT · principals Iran, Irán
- current system: same Development D20; cosine 0.60; D20: grouped together at tick 4; ticks 4 and 3, cosine 0.60: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Iranian currency record low vs Iran confirming receipt of the US response to its peace proposal.
- **owner verdict:** ____

### C027

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-175` · t4 | `sx-263` · t3 |
| published | 2026-09-30 03:31:43.000000 | 2026-09-29 18:24:27.000000 |
| source · lang | France 24 Español · es | El País Internacional · es |
| headline | ¿Está amparada por el derecho internacional la deportación a terceros países promovida por Trump? | Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente |
| current Development | - | D6 |
| places | Estados Unidos, Gobierno | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.62; not in any Development; closest member (cosine 0.62) is in D6
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Explainer on legality of third-country deportations vs launch of America.gov.
- **owner verdict:** ____

### C028

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-81` · t4 | `sx-195` · t4 |
| published | 2026-09-30 09:02:59.000000 | 2026-09-30 08:00:10.000000 |
| source · lang | BBC World · en | Al Jazeera · en |
| headline | Israel-bound flight diverted after fight between pilots | Flydubai flight to Israel diverted to Saudi Arabia after emergency alert |
| current Development | D23 | D23 |
| places | Israel | Dubai, Flydubai, Israel, Saudi Arabia, Tel Aviv |

- D23: "Israel-bound flight diverted after fight between pilots" · 4 items · sources Al Jazeera, BBC World, France 24, South China Morning Post · principals -
- current system: same Development D23; cosine 0.68; D23: least similar members of a 4-item Development (cosine 0.68)
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Same FlyDubai Dubai-Tel Aviv flight diverted to Saudi Arabia after an emergency alert/pilot fight on 30 Sep.
- **owner verdict:** ____

### C029  · flags: should_split, roundup_contamination

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-285` · t3 | `sx-282` · t3 |
| published | 2026-09-29 16:45:31.000000 | 2026-09-29 17:43:27.000000 |
| source · lang | Kyiv Independent · en | Kyiv Independent · en · ROUNDUP |
| headline | Putin signs latest decree increasing Russian military staff in wake of monster military budget, looming mobilization | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war |
| current Development | D4 | D4 |
| places | Russia | Oleshky, Russia, Ukraine |

- D4: "Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending" · 3 items · sources Defense News, Kyiv Independent · principals Russia, Vladimir Putin
- current system: same Development D4; cosine 0.53; D4: grouped together at tick 3; D4: least similar members of a 3-item Development (cosine 0.53)
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Putin's decree raising military staff vs a daily roundup headlined on the record 2027 military budget.
- **owner verdict:** ____

### C030

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-507` · t3 | `sx-2` · t3 |
| published | 2026-09-29 21:26:24.000000 | 2026-09-29 21:30:53.000000 |
| source · lang | Breaking Defense · en | Defense.gov · en |
| headline | Boeing wins Navy next-gen fighter F/A-XX competition | Department of War and U.S. Navy Award Contract for F/A-XX Program |
| current Development | D5 | D5 |
| places | U.S. | - |

- D5: "Department of War and U.S. Navy Award Contract for F/A-XX Program" · 3 items · sources Breaking Defense, Defense News, Defense.gov · principals -
- current system: same Development D5; cosine 0.67; D5: grouped together at tick 3; D5: least similar members of a 3-item Development (cosine 0.67)
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Report and official release of the same Navy F/A-XX contract award to Boeing.
- **owner verdict:** ____

### C031

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-256` · t3 | `sx-244` · t4 |
| published | 2026-09-29 15:00:18.000000 | 2026-09-30 08:02:57.000000 |
| source · lang | El País Internacional · es | El País Internacional · es |
| headline | Andy Burnham coloca la crisis de la vivienda como prioridad de su programa de Gobierno | Andy Burnham no descarta estudiar un futuro reingreso del Reino Unido en la UE |
| current Development | D12 | - |
| places | Gobierno, Liverpool | Liverpool, Reino Unido |

- D12: "«Hope again», l’appello di Burnham agli inglesi tra stop alle privatizzazioni e riforma de" · 2 items · sources El País Internacional, Il Sole 24 Ore Mondo · principals Andy Burnham, Burnham
- current system: one item not in any Development; cosine 0.72; not in any Development; closest member (cosine 0.72) is in D12; ticks 4 and 3, cosine 0.72: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · Burnham's Tuesday conference programme on housing vs his Wednesday remark not ruling out rejoining the EU: different statements on different days.
- **owner verdict:** ____

### C032

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-353` · t3 | `sx-360` · t3 |
| published | 2026-09-29 22:00:00.000000 | 2026-09-29 16:02:00.000000 |
| source · lang | European Commission Press · en | Council of the EU Press · en |
| headline | Commission report finds devastating shifts in the Arctic and record-breaking marine heatwaves | MFF 2028-2034: Council agrees negotiating position on future EU support for the fisheries sector |
| current Development | - | - |
| places | Arctic, Brussels | - |

- current system: neither in a Development; cosine 0.57; tick 3: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Commission state-of-the-ocean report vs Council position on fisheries funding in the MFF.
- **owner verdict:** ____

### C033  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-75` · t4 | `sx-536` · t4 |
| published | 2026-09-30 08:42:46.000000 | 2026-09-30 01:15:00.000000 |
| source · lang | Europa Press Internacional · es | GDELT · en |
| headline | Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz | Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability |
| current Development | D20 | D20 |
| places | EE.UU., Estados Unidos, Irán, Teheran | Iran, Syria |

- D20: "Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuer" · 3 items · sources Clarín Mundo, Europa Press Internacional, GDELT · principals Iran, Irán
- current system: same Development D20; cosine 0.41; D20: least similar members of a 3-item Development (cosine 0.41)
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Iran receiving US response to peace proposal vs Iranian currency record low.
- **owner verdict:** ____

### C034

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-352` · t3 | `sx-351` · t3 |
| published | 2026-09-29 22:00:00.000000 | 2026-09-29 22:00:00.000000 |
| source · lang | European Commission Press · en | European Commission Press · en |
| headline | Commission proposes a new EU Critical Communication System for first responders | Questions and answers on the European Union Critical Communication System |
| current Development | D3 | - |
| places | Brussels, Europe | Brussels |

- D3: "Council strengthens EU space threat response architecture" · 2 items · sources Council of the EU Press, European Commission Press · principals -
- current system: one item not in any Development; cosine 0.76; not in any Development; closest member (cosine 0.76) is in D3
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · The Commission's proposal of the EU Critical Communication System vs the accompanying Q&A explainer.
- **owner verdict:** ____

### C035  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-186` · t4 | `sx-111` · t3 |
| published | 2026-09-30 02:20:53.000000 | 2026-09-29 15:04:21.000000 |
| source · lang | France 24 Español · es | BBC Mundo · es |
| headline | Informe desde París: más de 200 manifestaciones de empleados públicos, pide aumento de sueldo | La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisis de vivienda en España |
| current Development | D7 | D7 |
| places | Francia, PARIS | España |

- D7: "La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisi" · 7 items · sources BBC Mundo, Clarín Mundo, Europa Press Internacional, France 24 Español · principals -
- current system: same Development D7; cosine 0.36; D7: least similar members of a 7-item Development (cosine 0.36); D7: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · French public sector pay protests vs Spanish pensioner Maricarmen returning home after eviction.
- **owner verdict:** ____

### C036  · flags: should_merge, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-240` · t3 | `sx-145` · t3 |
| published | 2026-09-29 15:48:00.000000 | 2026-09-29 13:38:00.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | DW World · en |
| headline | «Hope again», l’appello di Burnham agli inglesi tra stop alle privatizzazioni e riforma del welfare | UK PM Burnham seeks 'hope again' at Labour Party conference |
| current Development | D12 | - |
| places | Regno Unito | - |

- D12: "«Hope again», l’appello di Burnham agli inglesi tra stop alle privatizzazioni e riforma de" · 2 items · sources El País Internacional, Il Sole 24 Ore Mondo · principals Andy Burnham, Burnham
- current system: one item not in any Development; cosine 0.55; not in any Development; closest member (cosine 0.55) is in D12; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Burnham's 'hope again' leader's speech at the Labour conference on 29 Sep.
- **owner verdict:** ____

### C037  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-181` · t4 | `sx-111` · t3 |
| published | 2026-09-30 02:47:34.000000 | 2026-09-29 15:04:21.000000 |
| source · lang | France 24 Español · es | BBC Mundo · es |
| headline | Trabajadores públicos franceses se movilizan para exigir aumentos de salarios | La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisis de vivienda en España |
| current Development | D7 | D7 |
| places | Francia | España |

- D7: "La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisi" · 7 items · sources BBC Mundo, Clarín Mundo, Europa Press Internacional, France 24 Español · principals -
- current system: same Development D7; cosine 0.46; D7: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · French public workers' pay demonstrations vs Spanish eviction case.
- **owner verdict:** ____

### C038  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-494` · t1 | `sx-282` · t3 |
| published | 2026-09-28 18:07:08.000000 | 2026-09-29 17:43:27.000000 |
| source · lang | Defense News · en | Kyiv Independent · en · ROUNDUP |
| headline | Russia raises 2027 military spending by 27%, budget documents show | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war |
| current Development | D4 | D4 |
| places | Russia, Ukraine | Oleshky, Russia, Ukraine |

- D4: "Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending" · 3 items · sources Defense News, Kyiv Independent · principals Russia, Vladimir Putin
- current system: same Development D4; cosine 0.70; ticks 3 and 1, cosine 0.70: same Development
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · The daily roundup's headline is the record 27% rise in Russia's 2027 military budget, the same budget-document occurrence Defense News reports.
- **owner verdict:** ____

### C039

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-400` · t3 | `sx-423` · t1 |
| published | 2026-09-29 12:00:00.000000 | 2026-09-28 23:02:53.000000 |
| source · lang | UN News · en · ROUNDUP | UN Press · en |
| headline | Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis | Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO |
| current Development | - | - |
| places | Congo, DRC, Democratic Republic, New York, Rwanda | Congo, Democratic Republic, Democratic Republic of the Congo, Haiti |

- current system: neither in a Development; cosine 0.59; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (preview) · confidence medium · Item 2 is the pre-meeting programme ('will convene', 'anticipated briefers') for the DRC Security Council meeting that item 1 covers live.
- **owner verdict:** ____

### C040

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-169` · t3 | `sx-209` · t4 |
| published | 2026-09-29 21:00:26.000000 | 2026-09-30 03:00:59.000000 |
| source · lang | France 24 · en | Al Jazeera · en |
| headline | Safeguards 'build a moat' around US AI firms, prevent open-source models from advancing, expert says | Trump backs AI self-regulation at tech summit but is it enough? |
| current Development | - | - |
| places | France, U.S. | U.S. |

- current system: neither in a Development; cosine 0.68; ticks 3 and 4, cosine 0.68: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Both are analysis/expert commentary pieces on the AI accord, not reports of an occurrence.
- **owner verdict:** ____

### C041

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-115` · t2 | `sx-87` · t3 |
| published | 2026-09-29 02:31:07.000000 | 2026-09-29 23:39:58.000000 |
| source · lang | BBC Mundo · es | BBC World · en |
| headline | Quién es y qué crimen cometió Christa Pike, la primera mujer que será ejecutada en Tennessee en 200 años | US Supreme Court denies Christa Pike's last-ditch bid to halt execution |
| current Development | - | - |
| places | Tennessee | Tennessee |

- current system: neither in a Development; cosine 0.49; es vs en, shared ['Christa Pike', 'Tennessee']: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Profile/explainer of Christa Pike vs the Supreme Court's denial of her bid to halt execution.
- **owner verdict:** ____

### C042  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-130` · t3 | `sx-129` · t3 |
| published | 2026-09-29 23:35:00.000000 | 2026-09-29 23:05:00.000000 |
| source · lang | Rai News Esteri · it | Rai News Esteri · it |
| headline | Tradurre il potere, l'arduo mestiere dell'interprete | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.47; D6: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Feature on interpreters of power vs experts' critique of Big Tech self-regulation.
- **owner verdict:** ____

### C043  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-4` · t1 | `sx-510` · t3 |
| published | 2026-09-28 21:00:22.000000 | 2026-09-29 16:59:08.000000 |
| source · lang | Defense.gov · en | Breaking Defense · en |
| headline | Department of War and RTX Accelerate Advanced Medium-Range Air-to-Air Missile Production Through $20.7B Award | Raytheon nets potential $20.7 billion AMRAAM deal |
| current Development | - | D2 |
| places | U.S. | - |

- D2: "Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production" · 2 items · sources Breaking Defense, Defense News · principals Raytheon, US Department of Defense
- current system: one item not in any Development; cosine 0.63; tick 3: link cut by segmentation guard 'headline_similarity'
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Official release and report of the same $20.7bn AMRAAM award to Raytheon.
- **owner verdict:** ____

### C044

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-198` · t4 | `sx-160` · t4 |
| published | 2026-09-30 07:21:26.000000 | 2026-09-30 06:15:59.000000 |
| source · lang | Al Jazeera · en | France 24 · en |
| headline | Nigeria and Ghana suffer huge AFCON 2027 qualifying shocks | 2027 AFCON qualifiers: First win for Patrick Vieira and Senegal |
| current Development | - | - |
| places | Gambia, Ghana, Guinea Bissau, Nigeria | Ethiopia, Senegal |

- current system: neither in a Development; cosine 0.64; tick 4: link cut by segmentation guard 'disjoint_locations'
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Different AFCON 2027 qualifying matches (Ghana/Nigeria upsets vs Senegal win in Ethiopia).
- **owner verdict:** ____

### C045

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-47` · t4 | `sx-237` · t4 |
| published | 2026-09-30 02:30:01.000000 | 2026-09-30 05:33:00.000000 |
| source · lang | ANSA Mondo · it | Il Sole 24 Ore Mondo · it |
| headline | Missili e droni su regione di Kiev, ucciso un bambino | Ucraina: missili balistici russi su Kiev, 2 morti. La Polonia chiude due aeroporti |
| current Development | D22 | D22 |
| places | Kiev, Vyshgorod | Kiev, Polonia, Ucraina |

- D22: "Missili e droni su regione di Kiev, ucciso un bambino" · 3 items · sources ANSA Mondo, Il Sole 24 Ore Mondo · principals -
- current system: same Development D22; cosine 0.63; D22: grouped together at tick 4; D22: least similar members of a 3-item Development (cosine 0.63)
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Same overnight Russian missile/drone attack on Kyiv and its region on 30 Sep; tolls and details updated.
- **owner verdict:** ____

### C046  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-76` · t4 | `sx-111` · t3 |
| published | 2026-09-30 03:45:08.000000 | 2026-09-29 15:04:21.000000 |
| source · lang | Europa Press Internacional · es | BBC Mundo · es |
| headline | Al menos 440 detenidos en Francia en protestas estudiantiles unidas a la huelga de cientos de miles en el sector público | La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisis de vivienda en España |
| current Development | D7 | D7 |
| places | Francia, Gobierno | España |

- D7: "La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisi" · 7 items · sources BBC Mundo, Clarín Mundo, Europa Press Internacional, France 24 Español · principals -
- current system: same Development D7; cosine 0.43; D7: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · French student protest arrests vs Spanish eviction case.
- **owner verdict:** ____

### C047

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-14` · t2 | `sx-12` · t3 |
| published | 2026-09-29 03:43:06.000000 | 2026-09-29 17:38:13.000000 |
| source · lang | State Department · en | State Department · en |
| headline | Secretary of State Marco Rubio With Sean Hannity of Fox News | Secretary of State Marco Rubio At President Trump’s America.gov Event |
| current Development | - | - |
| places | D.C., Washington | D.C., U.S., Washington |

- current system: neither in a Development; cosine 0.72; ticks 3 and 2, cosine 0.72: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Rubio's 28 Sep Fox News interview vs his 29 Sep remarks at the America.gov event.
- **owner verdict:** ____

### C048

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-347` · t4 | `sx-352` · t3 |
| published | 2026-09-30 09:06:33.000000 | 2026-09-29 22:00:00.000000 |
| source · lang | European Commission Press · en | European Commission Press · en |
| headline | Daily News 30 / 09 / 2026 | Commission proposes a new EU Critical Communication System for first responders |
| current Development | - | D3 |
| places | Brussels | Brussels, Europe |

- D3: "Council strengthens EU space threat response architecture" · 2 items · sources Council of the EU Press, European Commission Press · principals -
- current system: one item not in any Development; cosine 0.59; not in any Development; closest member (cosine 0.59) is in D3
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Daily news roundup headlined on the Democratic Resilience Centre vs the EUCCS proposal.
- **owner verdict:** ____

### C049  · flags: grows_same_id, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-149` · t2 | `sx-1` · t4 |
| published | 2026-09-29 11:08:00.000000 | 2026-09-30 07:00:24.000000 |
| source · lang | DW World · en | Defense.gov · en |
| headline | Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission against ISIS after 12 years | Statement by Chief Pentagon Spokesman Sean Parnell on the Conclusion of the U.S. Military Mission in Iraq |
| current Development | D9 | D9 |
| places | Baghdad, Iraq, U.S. | Iraq, U.S. |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: same Development D9; cosine 0.57; D9: attached at tick 4 to a Development created at tick 3
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · DW report of US troops completing withdrawal ending Operation Inherent Resolve and the Pentagon statement formally concluding it describe the same act.
- **owner verdict:** ____

### C050

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-51` · t4 | `sx-266` · t3 |
| published | 2026-09-30 00:00:58.000000 | 2026-09-29 21:26:52.000000 |
| source · lang | ANSA Mondo · it | Clarín Mundo · es |
| headline | Ecuador, 'una cella per Correa' se tornerà a Quito | El argentino Rafael Grossi recupera terreno en la carrera para dirigir la ONU |
| current Development | - | D8 |
| places | Ecuador, Quito | China, Costa Rica, Estados Unidos |

- D8: "Qué se sabe del Corredor Andes-Atlántico, el ambicioso proyecto con el que EE.UU. busca ac" · 2 items · sources BBC Mundo, Clarín Mundo · principals EE.UU., Estados Unidos, Rafael Grossi, Washington
- current system: one item not in any Development; cosine 0.57; not in any Development; closest member (cosine 0.57) is in D8; tick 4: link cut by segmentation guard 'disjoint_locations'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Ecuador minister on a cell for Correa vs Grossi in the UN Secretary-General race.
- **owner verdict:** ____

### C051  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-400` · t3 | `sx-416` · t3 |
| published | 2026-09-29 12:00:00.000000 | 2026-09-29 21:52:33.000000 |
| source · lang | UN News · en · ROUNDUP | UN Press · en |
| headline | Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis | Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council |
| current Development | - | - |
| places | Congo, DRC, Democratic Republic, New York, Rwanda | Democratic Republic of Congo, Democratic Republic of the Congo |

- current system: neither in a Development; cosine 0.55; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence medium · UN News live coverage and UN Press summary of the same 29 Sep Security Council meeting on the DRC.
- **owner verdict:** ____

### C052  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-157` · t4 | `sx-491` · t3 |
| published | 2026-09-30 08:34:22.000000 | 2026-09-29 14:40:57.000000 |
| source · lang | France 24 · en | Defense News · en |
| headline | ‘The country has become a battlefield’: Last US troops exit Iraq | US forces exiting Iraq after 2 decades, leaving opening for Iran |
| current Development | D9 | D9 |
| places | Baghdad, Iraq, U.S., Washington | Iran, Iraq, Tehran, U.S. |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: same Development D9; cosine 0.74; ticks 4 and 3, cosine 0.74: same Development
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both describe the final US withdrawal from Iraqi bases by Wednesday; the later France 24 piece reports the exit itself.
- **owner verdict:** ____

### C053

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-487` · t3 | `sx-2` · t3 |
| published | 2026-09-29 22:20:07.000000 | 2026-09-29 21:30:53.000000 |
| source · lang | Defense News · en | Defense.gov · en |
| headline | US Navy selects Boeing to build next-generation F/A-XX fighter | Department of War and U.S. Navy Award Contract for F/A-XX Program |
| current Development | D5 | D5 |
| places | - | - |

- D5: "Department of War and U.S. Navy Award Contract for F/A-XX Program" · 3 items · sources Breaking Defense, Defense News, Defense.gov · principals -
- current system: same Development D5; cosine 0.73; D5: grouped together at tick 3
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Report and official release of the Navy's F/A-XX award to Boeing.
- **owner verdict:** ____

### C054

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-257` · t2 | `sx-271` · t3 |
| published | 2026-09-29 03:40:00.000000 | 2026-09-29 18:08:20.000000 |
| source · lang | El País Internacional · es | Clarín Mundo · es |
| headline | El monte Athos, el feudo de monjes de Europa que prohíbe la entrada de mujeres | Los reyes de España despliegan todo el protocolo para recibir a Emmanuel y Brigitte Macron en visita oficial |
| current Development | - | D7 |
| places | Athos, Europa, San Gregorio | España, Francia, Palacio Real de Madrid |

- D7: "La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisi" · 7 items · sources BBC Mundo, Clarín Mundo, Europa Press Internacional, France 24 Español · principals -
- current system: one item not in any Development; cosine 0.58; not in any Development; closest member (cosine 0.58) is in D7; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Mount Athos feature vs Spanish royals receiving the Macrons.
- **owner verdict:** ____

### C055

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-158` · t4 | `sx-222` · t4 |
| published | 2026-09-30 08:25:17.000000 | 2026-09-30 07:54:04.000000 |
| source · lang | France 24 · en | South China Morning Post · en |
| headline | Israel-bound flight diverted to Saudi Arabia after brawl between pilots | FlyDubai flight to Israel diverted to Saudi Arabia after incident in cockpit |
| current Development | D23 | D23 |
| places | Flydubai, Israel, Saudi Arabia | Dubai, Flydubai, Israel, Saudi Arabia, United Arab Emirates |

- D23: "Israel-bound flight diverted after fight between pilots" · 4 items · sources Al Jazeera, BBC World, France 24, South China Morning Post · principals -
- current system: same Development D23; cosine 0.90; D23: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Same FlyDubai flight to Israel diverted to Saudi Arabia after a cockpit incident on 30 Sep.
- **owner verdict:** ____

### C056

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-278` · t4 | `sx-282` · t3 |
| published | 2026-09-30 06:40:21.000000 | 2026-09-29 17:43:27.000000 |
| source · lang | Kyiv Independent · en | Kyiv Independent · en · ROUNDUP |
| headline | General Staff: Russia has lost 1,533,970 troops in Ukraine since Feb. 24, 2022 | Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war |
| current Development | - | D4 |
| places | Russia, Ukraine | Oleshky, Russia, Ukraine |

- D4: "Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending" · 3 items · sources Defense News, Kyiv Independent · principals Russia, Vladimir Putin
- current system: one item not in any Development; cosine 0.60; not in any Development; closest member (cosine 0.60) is in D4
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Daily General Staff Russian casualty figure vs roundup headlined on the 2027 military budget.
- **owner verdict:** ____

### C057

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-272` · t3 | `sx-113` · t3 |
| published | 2026-09-29 17:52:12.000000 | 2026-09-29 18:49:14.000000 |
| source · lang | Clarín Mundo · es | BBC Mundo · es |
| headline | Barcelona inundada por lluvias torrenciales: hay operativos de emergencia y caos en el transporte público | El huracán Polo toca tierra dos veces en México con intensas lluvias que no han causado víctimas |
| current Development | - | - |
| places | Barcelona | Baja California, Mar de Cortés, México, Sonora |

- current system: neither in a Development; cosine 0.53; tick 3: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Barcelona torrential flooding vs Hurricane Polo landfall in Mexico.
- **owner verdict:** ____

### C058

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-246` · t4 | `sx-40` · t4 |
| published | 2026-09-30 09:14:30.000000 | 2026-09-30 08:40:14.000000 |
| source · lang | El País Internacional · es | ANSA Mondo · it |
| headline | Una pelea entre los pilotos de un avión con destino Israel activa una alerta de emergencia y su aterrizaje en Arabia Saudí | 'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino' |
| current Development | D21 | D21 |
| places | Arabia Saudí, Dubai, Israel | - |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: same Development D21; cosine 0.51; D21: least similar members of a 6-item Development (cosine 0.51)
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Same FlyDubai emergency caused by a fight between pilots, landing in Saudi Arabia.
- **owner verdict:** ____

### C059

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-237` · t4 | `sx-49` · t4 |
| published | 2026-09-30 05:33:00.000000 | 2026-09-30 01:04:54.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | ANSA Mondo · it |
| headline | Ucraina: missili balistici russi su Kiev, 2 morti. La Polonia chiude due aeroporti | Missili balistici lanciati su Kiev, esplosioni in città |
| current Development | D22 | D22 |
| places | Kiev, Polonia, Ucraina | Kiev |

- D22: "Missili e droni su regione di Kiev, ucciso un bambino" · 3 items · sources ANSA Mondo, Il Sole 24 Ore Mondo · principals -
- current system: same Development D22; cosine 0.67; D22: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Same overnight ballistic missile attack on Kyiv; later item adds deaths and Polish airport closures.
- **owner verdict:** ____

### C060

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-410` · t1 | `sx-424` · t1 |
| published | 2026-09-28 12:00:00.000000 | 2026-09-28 23:02:52.000000 |
| source · lang | UN News · en · ROUNDUP | UN Press · en |
| headline | Security Council LIVE: Ambassadors meet as West Bank tensions rise, Gaza plan stalls | International Security Rapidly Deteriorates; General Assembly Urges Nations to Address Weaker Global Arms Treaties and Heightened Nuclear Risks |
| current Development | - | - |
| places | Gaza, Israel, Middle East, West Bank | Middle East |

- current system: neither in a Development; cosine 0.42; same tick, different outlets, cosine 0.42: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Security Council meeting on the Middle East vs General Assembly high-level meeting on nuclear risks.
- **owner verdict:** ____

### C061

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-48` · t4 | `sx-234` · t4 |
| published | 2026-09-30 01:10:48.000000 | 2026-09-30 08:21:00.000000 |
| source · lang | ANSA Mondo · it | Il Sole 24 Ore Mondo · it |
| headline | Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza' | Nasce a Milano il Polish Italian business council |
| current Development | D6 | - |
| places | - | Gran Bretagna, Italia, Milano |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.56; not in any Development; closest member (cosine 0.56) is in D6
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Trump AI executive order vs Polish-Italian business council in Milan.
- **owner verdict:** ____

### C062  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-76` · t4 | `sx-270` · t3 |
| published | 2026-09-30 03:45:08.000000 | 2026-09-29 18:43:43.000000 |
| source · lang | Europa Press Internacional · es | Clarín Mundo · es |
| headline | Al menos 440 detenidos en Francia en protestas estudiantiles unidas a la huelga de cientos de miles en el sector público | Presionado por las protestas, Pedro Sánchez anuncia decretos clave para enfrentar la crisis de la vivienda en España |
| current Development | D7 | D7 |
| places | Francia, Gobierno | España |

- D7: "La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisi" · 7 items · sources BBC Mundo, Clarín Mundo, Europa Press Internacional, France 24 Español · principals -
- current system: same Development D7; cosine 0.63; tick 4: link cut by segmentation guard 'disjoint_locations'; ticks 4 and 3, cosine 0.63: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · French protest arrests vs Sanchez housing decrees in Spain.
- **owner verdict:** ____

### C063  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-263` · t3 | `sx-133` · t3 |
| published | 2026-09-29 18:24:27.000000 | 2026-09-29 19:21:00.000000 |
| source · lang | El País Internacional · es | Rai News Esteri · it |
| headline | Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente | Gli Usa prestano alle aziende energetiche 40 milioni di barili di petrolio delle riserve strategiche |
| current Development | D6 | D6 |
| places | - | Paesi, U.S. |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.25; D6: least similar members of a 15-item Development (cosine 0.25)
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · America.gov launch vs US strategic oil reserve loan.
- **owner verdict:** ____

### C064

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-423` · t1 | `sx-416` · t3 |
| published | 2026-09-28 23:02:53.000000 | 2026-09-29 21:52:33.000000 |
| source · lang | UN Press · en | UN Press · en |
| headline | Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO | Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council |
| current Development | - | - |
| places | Congo, Democratic Republic, Democratic Republic of the Congo, Haiti | Democratic Republic of Congo, Democratic Republic of the Congo |

- current system: neither in a Development; cosine 0.65; ticks 3 and 1, cosine 0.65: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (preview) · confidence medium · Pre-meeting programme of the DRC Security Council meeting vs the report of what the Special Representative told the Council.
- **owner verdict:** ____

### C065

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-507` · t3 | `sx-505` · t4 |
| published | 2026-09-29 21:26:24.000000 | 2026-09-30 01:55:49.000000 |
| source · lang | Breaking Defense · en | Breaking Defense · en |
| headline | Boeing wins Navy next-gen fighter F/A-XX competition | What Boeing’s F/A-XX win means for the company, and what challenges come next |
| current Development | D5 | - |
| places | U.S. | - |

- D5: "Department of War and U.S. Navy Award Contract for F/A-XX Program" · 3 items · sources Breaking Defense, Defense News, Defense.gov · principals -
- current system: one item not in any Development; cosine 0.68; not in any Development; closest member (cosine 0.68) is in D5
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Report of Boeing's F/A-XX win vs an analysis of what the win means.
- **owner verdict:** ____

### C066  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-122` · t4 | `sx-39` · t4 |
| published | 2026-09-30 07:58:00.000000 | 2026-09-30 09:27:04.000000 |
| source · lang | Rai News Esteri · it | ANSA Mondo · it |
| headline | Volo Flydubai, l'aereo diretto a Tel Aviv viene deviato in Arabia Saudita | Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino |
| current Development | D21 | - |
| places | Tel Aviv | Oman |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: one item not in any Development; cosine 0.55; tick 4: link cut by segmentation guard 'disjoint_locations'
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Later detail (pilots' nationalities) on the same FlyDubai diversion incident.
- **owner verdict:** ____

### C067

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-12` · t3 | `sx-55` · t3 |
| published | 2026-09-29 17:38:13.000000 | 2026-09-29 21:20:34.000000 |
| source · lang | State Department · en | ANSA Mondo · it |
| headline | Secretary of State Marco Rubio At President Trump’s America.gov Event | Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA' |
| current Development | - | D6 |
| places | D.C., U.S., Washington | U.S. |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.21; it vs en, shared ['Trump', 'U.S.']: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · Rubio's remarks at the America.gov event vs Trump's statement on a 10-person AI oversight committee.
- **owner verdict:** ____

### C068

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-175` · t4 | `sx-267` · t3 |
| published | 2026-09-30 03:31:43.000000 | 2026-09-29 20:42:05.000000 |
| source · lang | France 24 Español · es | Clarín Mundo · es |
| headline | ¿Está amparada por el derecho internacional la deportación a terceros países promovida por Trump? | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA |
| current Development | - | D6 |
| places | Estados Unidos, Gobierno | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.61; ticks 4 and 3, cosine 0.61: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Deportation legality explainer vs AI accord announcement.
- **owner verdict:** ____

### C069

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-266` · t3 | `sx-117` · t1 |
| published | 2026-09-29 21:26:52.000000 | 2026-09-28 13:29:19.000000 |
| source · lang | Clarín Mundo · es | BBC Mundo · es |
| headline | El argentino Rafael Grossi recupera terreno en la carrera para dirigir la ONU | "El ganado se está muriendo de sed y hambre": el devastador impacto de El Niño que ya se siente en el Corredor Seco de Centroamérica |
| current Development | D8 | - |
| places | China, Costa Rica, Estados Unidos | Corredor Seco de Centroamérica, El Niño |

- D8: "Qué se sabe del Corredor Andes-Atlántico, el ambicioso proyecto con el que EE.UU. busca ac" · 2 items · sources BBC Mundo, Clarín Mundo · principals EE.UU., Estados Unidos, Rafael Grossi, Washington
- current system: one item not in any Development; cosine 0.53; tick 3: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · UN leadership race vs El Nino drought in Central America.
- **owner verdict:** ____

### C070

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-241` · t3 | `sx-57` · t3 |
| published | 2026-09-29 14:59:00.000000 | 2026-09-29 20:36:13.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | ANSA Mondo · it |
| headline | Spagna, Sánchez vara nuove misure contro la crisi abitativa: cosa cambia per affitti e sfratti | Trump, 'da vertici big tech impegno moralmente vincolante su sicurezza IA' |
| current Development | - | D6 |
| places | Puerta del Sol, Spagna | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.41; same tick, different outlets, cosine 0.41: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Spanish housing decrees vs Trump AI accord.
- **owner verdict:** ____

### C071

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-43` · t4 | `sx-128` · t4 |
| published | 2026-09-30 07:31:58.000000 | 2026-09-30 01:54:00.000000 |
| source · lang | ANSA Mondo · it | Rai News Esteri · it |
| headline | Ft, colloqui tra Trump e consiglieri per valutare uno stop all'export di gasolio | USA, stretta finale su Cuba. Stangata bancaria, stop ai viaggi e blocco finanziario |
| current Development | D6 | - |
| places | - | Cancellate, Cuba, U.S. |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.57; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Trump weighing a diesel export ban vs Cuba sanctions tightening.
- **owner verdict:** ____

### C072  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-491` · t3 | `sx-164` · t4 |
| published | 2026-09-29 14:40:57.000000 | 2026-09-30 01:04:01.000000 |
| source · lang | Defense News · en | France 24 · en |
| headline | US forces exiting Iraq after 2 decades, leaving opening for Iran | US forces leave Iraq, raising fears of Iran-backed militias amid power vacuum |
| current Development | D9 | D9 |
| places | Iran, Iraq, Tehran, U.S. | Iran, Iraq, U.S. |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: same Development D9; cosine 0.76; ticks 4 and 3, cosine 0.76: same Development
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both report US forces leaving their last Iraqi bases by/on Wednesday under the 2024 agreement.
- **owner verdict:** ____

### C073  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-235` · t4 | `sx-129` · t3 |
| published | 2026-09-30 08:09:14.000000 | 2026-09-29 23:05:00.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | Rai News Esteri · it |
| headline | Ft: Trump valuta il divieto di export del gasolio per contenere la crisi dei prezzi | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.34; D6: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Trump weighing diesel export ban vs experts' critique of AI self-regulation.
- **owner verdict:** ____

### C074

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-488` · t3 | `sx-486` · t4 |
| published | 2026-09-29 16:18:42.000000 | 2026-09-30 00:03:53.000000 |
| source · lang | Defense News · en | Defense News · en |
| headline | Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production | Why the Pentagon just dropped $450M on tungsten mining |
| current Development | D2 | - |
| places | - | China, Iran, Russia, U.S. |

- D2: "Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production" · 2 items · sources Breaking Defense, Defense News · principals Raytheon, US Department of Defense
- current system: one item not in any Development; cosine 0.56; not in any Development; closest member (cosine 0.56) is in D2
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · AMRAAM contract award vs a separate $450m tungsten mining investment.
- **owner verdict:** ____

### C075

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-45` · t4 | `sx-47` · t4 |
| published | 2026-09-30 04:50:02.000000 | 2026-09-30 02:30:01.000000 |
| source · lang | ANSA Mondo · it | ANSA Mondo · it |
| headline | Ministro Kiev, 'ogni allarme missilistico costa 45 milioni dollari all'ora' | Missili e droni su regione di Kiev, ucciso un bambino |
| current Development | - | D22 |
| places | - | Kiev, Vyshgorod |

- D22: "Missili e droni su regione di Kiev, ucciso un bambino" · 3 items · sources ANSA Mondo, Il Sole 24 Ore Mondo · principals -
- current system: one item not in any Development; cosine 0.56; not in any Development; closest member (cosine 0.56) is in D22
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Ukrainian minister's statement on the economic cost of missile alerts vs the attack on Kyiv region killing a child.
- **owner verdict:** ____

### C076

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-277` · t4 | `sx-275` · t4 |
| published | 2026-09-30 07:03:10.000000 | 2026-09-30 08:14:48.000000 |
| source · lang | Kyiv Independent · en | Kyiv Independent · en |
| headline | Drone crashes in Moldova amid Russian mass attack on Ukraine | Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack |
| current Development | - | D15 |
| places | Moldova, Russia, Ukraine, Ukraine Russia | Kyiv, Russia, Ukraine |

- D15: "Live: Several people killed as Russia launches new round of strikes on Kyiv" · 3 items · sources France 24, Kyiv Independent · principals Russia
- current system: one item not in any Development; cosine 0.67; not in any Development; closest member (cosine 0.67) is in D15
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · A drone crashing in Moldova is a distinct incident from the casualties of the same overnight attack on Ukraine.
- **owner verdict:** ____

### C077  · flags: should_merge, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-4` · t1 | `sx-488` · t3 |
| published | 2026-09-28 21:00:22.000000 | 2026-09-29 16:18:42.000000 |
| source · lang | Defense.gov · en | Defense News · en |
| headline | Department of War and RTX Accelerate Advanced Medium-Range Air-to-Air Missile Production Through $20.7B Award | Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production |
| current Development | - | D2 |
| places | U.S. | - |

- D2: "Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production" · 2 items · sources Breaking Defense, Defense News · principals Raytheon, US Department of Defense
- current system: one item not in any Development; cosine 0.70; not in any Development; closest member (cosine 0.70) is in D2
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Official release and report of the same $20.7bn AMRAAM award.
- **owner verdict:** ____

### C078

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-87` · t3 | `sx-124` · t4 |
| published | 2026-09-29 23:39:58.000000 | 2026-09-30 06:27:00.000000 |
| source · lang | BBC World · en | Rai News Esteri · it |
| headline | US Supreme Court denies Christa Pike's last-ditch bid to halt execution | Christa Pike a un passo dall'esecuzione: "Non ho paura di morire" |
| current Development | - | - |
| places | Tennessee | Tennessee |

- current system: neither in a Development; cosine 0.38; it vs en, shared ['Christa Pike', 'Tennessee']: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (preview) · confidence medium · Supreme Court denial of Pike's bid vs a piece on her imminent execution and her 'not afraid to die' quote.
- **owner verdict:** ____

### C079  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-245` · t3 | `sx-80` · t4 |
| published | 2026-09-29 15:14:14.000000 | 2026-09-30 09:11:22.000000 |
| source · lang | El País Internacional · es | Europa Press Internacional · es |
| headline | Tres soldados israelíes sobre Gaza: “Llegó un momento en que ya no parecía tan grave matar a decenas de personas” | Muere una palestina en un nuevo ataque de Israel contra la ciudad de Gaza a pesar del alto el fuego |
| current Development | D26 | D26 |
| places | Gaza, Yabalia | Estados Unidos, Franja de Gaza, Gaza, Hamás, Israel |

- D26: "Muere una palestina en un nuevo ataque de Israel contra la ciudad de Gaza a pesar del alto" · 2 items · sources El País Internacional, Europa Press Internacional · principals Ejército de Israel, Israel
- current system: same Development D26; cosine 0.63; D26: grouped together at tick 4
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Feature with Israeli soldiers' testimonies vs a specific Israeli strike killing a Palestinian in Gaza City.
- **owner verdict:** ____

### C080  · flags: should_split, roundup_contamination

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-150` · t2 | `sx-396` · t3 |
| published | 2026-09-29 10:26:00.000000 | 2026-09-29 12:00:00.000000 |
| source · lang | DW World · en | UN News · en · ROUNDUP |
| headline | Malaysia repatriates Myanmar migrants despite UN warnings | World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update |
| current Development | D10 | D10 |
| places | Malaysia, Myanmar | Gaza, Malaysia, Myanmar, West Bank |

- D10: "World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency" · 2 items · sources DW World, UN News · principals Malaysia
- current system: same Development D10; cosine 0.62; D10: grouped together at tick 3; ticks 2 and 3, cosine 0.62: same Development
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · A multi-item UN news-in-brief roundup whose headline is not solely the Malaysian repatriation vs the DW report on that repatriation.
- **owner verdict:** ____

### C081

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-102` · t3 | `sx-175` · t4 |
| published | 2026-09-29 13:55:29.000000 | 2026-09-30 03:31:43.000000 |
| source · lang | BBC Mundo · es | France 24 Español · es |
| headline | "Temo por mi vida si me devuelven": las audiencias masivas en Miami que aceleran las deportaciones sin dar tiempo a los migrantes para defender sus casos | ¿Está amparada por el derecho internacional la deportación a terceros países promovida por Trump? |
| current Development | - | - |
| places | Estados Unidos, Miami | Estados Unidos, Gobierno |

- current system: neither in a Development; cosine 0.64; ticks 3 and 4, cosine 0.64: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Feature on Miami mass immigration hearings vs explainer on third-country deportations.
- **owner verdict:** ____

### C082

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-127` · t4 | `sx-126` · t4 |
| published | 2026-09-30 04:06:00.000000 | 2026-09-30 04:08:00.000000 |
| source · lang | Rai News Esteri · it | Rai News Esteri · it |
| headline | Marocco, Fatima Zahara Mansouri è la prima donna premier della storia del Paese | Marocco, il re Mohammed VI incontra la nuova premier El Mansouri |
| current Development | D18 | D18 |
| places | Marocco, Marrakech, Paese Avvocata, Regno | Marocco |

- D18: "Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno" · 3 items · sources Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: same Development D18; cosine 0.64; D18: grouped together at tick 4; D18: least similar members of a 3-item Development (cosine 0.64)
- **proposed:** `AMBIGUOUS` · confidence low · Mansouri becoming Morocco's first woman PM vs the king's palace meeting with her after the appointment; unclear if the audience is the appointment itself.
- **owner verdict:** ____

### C083

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-428` · t3 | `sx-5` · t1 |
| published | 2026-09-29 16:00:11.000000 | 2026-09-28 20:30:00.000000 |
| source · lang | War on the Rocks · en | Defense.gov · en |
| headline | What Will Hegseth’s “State of the Force” Reprise Reveal? | Secretary of War Pete Hegseth Signs Directive to Defend 2026 Elections From Foreign Threats |
| current Development | - | - |
| places | U.S. | - |

- current system: neither in a Development; cosine 0.61; tick 4: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (preview) · confidence high · Preview of Hegseth's upcoming 'State of the Force' address vs his signing of an election-defence directive.
- **owner verdict:** ____

### C084  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-43` · t4 | `sx-129` · t3 |
| published | 2026-09-30 07:31:58.000000 | 2026-09-29 23:05:00.000000 |
| source · lang | ANSA Mondo · it | Rai News Esteri · it |
| headline | Ft, colloqui tra Trump e consiglieri per valutare uno stop all'export di gasolio | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.38; D6: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Diesel export ban talks vs experts' AI self-regulation critique.
- **owner verdict:** ____

### C085  · flags: grows_same_id, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-157` · t4 | `sx-149` · t2 |
| published | 2026-09-30 08:34:22.000000 | 2026-09-29 11:08:00.000000 |
| source · lang | France 24 · en | DW World · en |
| headline | ‘The country has become a battlefield’: Last US troops exit Iraq | Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission against ISIS after 12 years |
| current Development | D9 | D9 |
| places | Baghdad, Iraq, U.S., Washington | Baghdad, Iraq, U.S. |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: same Development D9; cosine 0.75; D9: attached at tick 4 to a Development created at tick 3
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both report the completion of the US troop withdrawal from Iraq ending the anti-ISIS coalition mission.
- **owner verdict:** ____

### C086

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-5` · t1 | `sx-3` · t3 |
| published | 2026-09-28 20:30:00.000000 | 2026-09-29 18:10:35.000000 |
| source · lang | Defense.gov · en | Defense.gov · en |
| headline | Secretary of War Pete Hegseth Signs Directive to Defend 2026 Elections From Foreign Threats | Secretary of War Pete Hegseth Signs Directive Halting Tenured Civilian Positions at U.S. Military Service Academies |
| current Development | - | - |
| places | - | U.S. |

- current system: neither in a Development; cosine 0.63; ticks 3 and 1, cosine 0.63: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (repeat) · confidence high · Two different Hegseth directives on different days (election defence vs academy tenure).
- **owner verdict:** ____

### C087

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-122` · t4 | `sx-246` · t4 |
| published | 2026-09-30 07:58:00.000000 | 2026-09-30 09:14:30.000000 |
| source · lang | Rai News Esteri · it | El País Internacional · es |
| headline | Volo Flydubai, l'aereo diretto a Tel Aviv viene deviato in Arabia Saudita | Una pelea entre los pilotos de un avión con destino Israel activa una alerta de emergencia y su aterrizaje en Arabia Saudí |
| current Development | D21 | D21 |
| places | Tel Aviv | Arabia Saudí, Dubai, Israel |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: same Development D21; cosine 0.61; D21: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Same FlyDubai flight to Tel Aviv diverted to Saudi Arabia after a pilots' fight.
- **owner verdict:** ____

### C088

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-239` · t3 | `sx-77` · t4 |
| published | 2026-09-29 18:07:00.000000 | 2026-09-30 07:40:40.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | Europa Press Internacional · es |
| headline | Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno | La primera ministra designada de Marruecos iniciará hoy una ronda de contactos para ensamblar el nuevo Gobierno |
| current Development | D18 | D19 |
| places | Marocco, Marrakech, Regno | Gobierno, Marruecos |

- D18: "Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno" · 3 items · sources Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- D19: "La primera ministra designada de Marruecos iniciará hoy una ronda de contactos para ensamb" · 2 items · sources BBC Mundo, Europa Press Internacional · principals -
- current system: different Developments; cosine 0.55; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence high · El Mansouri's selection as PM vs her starting coalition consultations the next day.
- **owner verdict:** ____

### C089  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-491` · t3 | `sx-149` · t2 |
| published | 2026-09-29 14:40:57.000000 | 2026-09-29 11:08:00.000000 |
| source · lang | Defense News · en | DW World · en |
| headline | US forces exiting Iraq after 2 decades, leaving opening for Iran | Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission against ISIS after 12 years |
| current Development | D9 | D9 |
| places | Iran, Iraq, Tehran, U.S. | Baghdad, Iraq, U.S. |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: same Development D9; cosine 0.71; D9: grouped together at tick 3; ticks 2 and 3, cosine 0.71: same Development
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both report the US completing its military withdrawal from Iraqi bases.
- **owner verdict:** ____

### C090

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-64` · t4 | `sx-138` · t3 |
| published | 2026-09-30 07:50:50.000000 | 2026-09-29 18:02:00.000000 |
| source · lang | ANSA English · en | Rai News Esteri · it |
| headline | Cutting ties with Egypt won't bring truth for Giulio Regeni says Meloni | Prosegue la distensione tra Roma e Il Cairo dopo il gelo sul caso Regeni |
| current Development | - | - |
| places | Cairo, Egypt, Italy, Regeni, Rome | Il Cairo, Italia, Regeni, Roma, Stati |

- current system: neither in a Development; cosine 0.47; it vs en, shared ['Meloni', 'Regeni']: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · Meloni's 30 Sep statement refusing to cut ties with Egypt vs a background piece on the Rome-Cairo thaw.
- **owner verdict:** ____

### C091

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-210` · t4 | `sx-93` · t4 |
| published | 2026-09-30 02:39:06.000000 | 2026-09-30 06:41:35.000000 |
| source · lang | Al Jazeera · en | BBC World · en |
| headline | Somali pirates killed five crew members on hijacked tanker, officials say | Somali pirates killed oil tanker crew before rescue, official tells BBC |
| current Development | D28 | D28 |
| places | Somalia | Somalia |

- D28: "Somali pirates killed oil tanker crew before rescue, official tells BBC" · 2 items · sources Al Jazeera, BBC World · principals Somalia
- current system: same Development D28; cosine 0.76; D28: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Somali pirates killed crew on the hijacked tanker before the rescue.
- **owner verdict:** ____

### C092  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-39` · t4 | `sx-123` · t4 |
| published | 2026-09-30 09:27:04.000000 | 2026-09-30 07:00:00.000000 |
| source · lang | ANSA Mondo · it | Rai News Esteri · it |
| headline | Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino | Volo FlyDubai, la ricostruzione di Tel Aviv: "Pilota ha cercato di far schiantare l'aereo" |
| current Development | - | D21 |
| places | Oman | Dubai, Pilota, Tel Aviv |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: one item not in any Development; cosine 0.55; tick 4: link cut by segmentation guard 'disjoint_locations'
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both concern the same FlyDubai cockpit incident; one gives the reconstruction, the other revised pilot nationalities.
- **owner verdict:** ____

### C093  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-243` · t2 | `sx-185` · t4 |
| published | 2026-09-29 06:12:00.000000 | 2026-09-30 02:23:10.000000 |
| source · lang | Il Sole 24 Ore Mondo · it | France 24 Español · es |
| headline | Cisgiordania, raid di coloni israeliani contro famiglia palestinese a Jalud. Condanna Usa | Cisjordania: más de 100 colonos israelíes irrumpen en aldea; Netanyahu condena los hechos |
| current Development | D16 | D16 |
| places | Cisgiordania, Condanna Usa | Cisjordania |

- D16: "El Senado de EEUU rechaza votar una resolución acerca de la violencia en Cisjordania tras " · 3 items · sources Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo · principals -
- current system: same Development D16; cosine 0.61; D16: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both report the Israeli settler raid on the Palestinian village of Jalud, with US and later Netanyahu condemnation.
- **owner verdict:** ____

### C094  · flags: should_split, same_story_new_action

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-79` · t4 | `sx-243` · t2 |
| published | 2026-09-30 05:02:20.000000 | 2026-09-29 06:12:00.000000 |
| source · lang | Europa Press Internacional · es | Il Sole 24 Ore Mondo · it |
| headline | El Senado de EEUU rechaza votar una resolución acerca de la violencia en Cisjordania tras el último ataque de colonos | Cisgiordania, raid di coloni israeliani contro famiglia palestinese a Jalud. Condanna Usa |
| current Development | D16 | D16 |
| places | Cisjordania, Senado de EEUU | Cisgiordania, Condanna Usa |

- D16: "El Senado de EEUU rechaza votar una resolución acerca de la violencia en Cisjordania tras " · 3 items · sources Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo · principals -
- current system: same Development D16; cosine 0.50; D16: least similar members of a 3-item Development (cosine 0.50)
- **proposed:** `DIFFERENT_DEVELOPMENT` (reaction) · confidence high · US Senate refusing to vote on a West Bank resolution after the attack vs the settler raid on Jalud itself.
- **owner verdict:** ____

### C095

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-158` · t4 | `sx-81` · t4 |
| published | 2026-09-30 08:25:17.000000 | 2026-09-30 09:02:59.000000 |
| source · lang | France 24 · en | BBC World · en |
| headline | Israel-bound flight diverted to Saudi Arabia after brawl between pilots | Israel-bound flight diverted after fight between pilots |
| current Development | D23 | D23 |
| places | Flydubai, Israel, Saudi Arabia | Israel |

- D23: "Israel-bound flight diverted after fight between pilots" · 4 items · sources Al Jazeera, BBC World, France 24, South China Morning Post · principals -
- current system: same Development D23; cosine 0.85; D23: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Same Israel-bound FlyDubai diversion after a fight between pilots.
- **owner verdict:** ____

### C096  · flags: should_merge, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-39` · t4 | `sx-40` · t4 |
| published | 2026-09-30 09:27:04.000000 | 2026-09-30 08:40:14.000000 |
| source · lang | ANSA Mondo · it | ANSA Mondo · it |
| headline | Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino | 'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino' |
| current Development | - | D21 |
| places | Oman | - |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: one item not in any Development; cosine 0.71; not in any Development; closest member (cosine 0.71) is in D21
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Same FlyDubai incident; later item corrects the pilots' nationalities.
- **owner verdict:** ____

### C097

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-123` · t4 | `sx-122` · t4 |
| published | 2026-09-30 07:00:00.000000 | 2026-09-30 07:58:00.000000 |
| source · lang | Rai News Esteri · it | Rai News Esteri · it |
| headline | Volo FlyDubai, la ricostruzione di Tel Aviv: "Pilota ha cercato di far schiantare l'aereo" | Volo Flydubai, l'aereo diretto a Tel Aviv viene deviato in Arabia Saudita |
| current Development | D21 | D21 |
| places | Dubai, Pilota, Tel Aviv | Tel Aviv |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: same Development D21; cosine 0.77; D21: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence high · Same FlyDubai flight emergency and diversion to Saudi Arabia.
- **owner verdict:** ____

### C098

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-512` · t3 | `sx-490` · t3 |
| published | 2026-09-29 14:42:16.000000 | 2026-09-29 14:52:40.000000 |
| source · lang | Breaking Defense · en | Defense News · en |
| headline | Estonia accuses Russia of ordering August arson attack on Milrem | Estonia blames Russia in arson attack on military robotics firm Milrem |
| current Development | D13 | D13 |
| places | Estonia, Russia, Ukraine | Estonia, Milrem GLASGOW, Russia, Scotland, Tallinn |

- D13: "Estonia blames Russia in arson attack on military robotics firm Milrem" · 2 items · sources Breaking Defense, Defense News · principals Estonia, Tallinn
- current system: same Development D13; cosine 0.76; D13: grouped together at tick 3
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Both report Estonia's 29 Sep attribution of the August Milrem arson to Russia.
- **owner verdict:** ____

### C099

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-419` · t3 | `sx-353` · t3 |
| published | 2026-09-29 19:39:26.000000 | 2026-09-29 22:00:00.000000 |
| source · lang | UN Press · en | European Commission Press · en |
| headline | 2026 Climate Summit | Commission report finds devastating shifts in the Arctic and record-breaking marine heatwaves |
| current Development | - | - |
| places | - | Arctic, Brussels |

- current system: neither in a Development; cosine 0.57; tick 3: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · UN climate summit coverage page vs Commission state-of-the-ocean report.
- **owner verdict:** ____

### C100

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-167` · t3 | `sx-209` · t4 |
| published | 2026-09-29 22:48:07.000000 | 2026-09-30 03:00:59.000000 |
| source · lang | France 24 · en | Al Jazeera · en |
| headline | AI companies sign voluntary accord on safety with Trump | Trump backs AI self-regulation at tech summit but is it enough? |
| current Development | - | - |
| places | - | U.S. |

- current system: neither in a Development; cosine 0.67; tick 4: link cut by segmentation guard 'analysis_headline'
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · Report of the voluntary AI safety accord vs Al Jazeera's 'is it enough?' assessment of it.
- **owner verdict:** ____

### C101

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-487` · t3 | `sx-505` · t4 |
| published | 2026-09-29 22:20:07.000000 | 2026-09-30 01:55:49.000000 |
| source · lang | Defense News · en | Breaking Defense · en |
| headline | US Navy selects Boeing to build next-generation F/A-XX fighter | What Boeing’s F/A-XX win means for the company, and what challenges come next |
| current Development | D5 | - |
| places | - | - |

- D5: "Department of War and U.S. Navy Award Contract for F/A-XX Program" · 3 items · sources Breaking Defense, Defense News, Defense.gov · principals -
- current system: one item not in any Development; cosine 0.63; tick 4: link cut by segmentation guard 'analysis_headline'; ticks 3 and 4, cosine 0.63: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Report of the F/A-XX selection vs analysis of what it means for Boeing.
- **owner verdict:** ____

### C102

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-139` · t3 | `sx-137` · t3 |
| published | 2026-09-29 15:22:00.000000 | 2026-09-29 17:15:00.000000 |
| source · lang | Rai News Esteri · it | Rai News Esteri · it |
| headline | Burnham: "Londra per troppo tempo sulla strada sbagliata, miglioreremo i rapporti con l'UE" | Bruxelles intitola un edificio a Sassoli: il ricordo delle istituzioni europee |
| current Development | D25 | - |
| places | Bruxelles, Londra, Regno Unito | Bruxelles, Metsola, Sassoli |

- D25: "Burnham su Brexit, 'tutte le opzioni sul tavolo, inclusa riadesione a Ue'" · 2 items · sources ANSA Mondo, Rai News Esteri · principals Burnham
- current system: one item not in any Development; cosine 0.66; not in any Development; closest member (cosine 0.66) is in D25
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Burnham's conference speech vs naming of an EU Parliament building after Sassoli.
- **owner verdict:** ____

### C103

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-352` · t3 | `sx-350` · t3 |
| published | 2026-09-29 22:00:00.000000 | 2026-09-29 22:00:00.000000 |
| source · lang | European Commission Press · en | European Commission Press · en |
| headline | Commission proposes a new EU Critical Communication System for first responders | Factsheet: EU Critical Communication System |
| current Development | D3 | - |
| places | Brussels, Europe | - |

- D3: "Council strengthens EU space threat response architecture" · 2 items · sources Council of the EU Press, European Commission Press · principals -
- current system: one item not in any Development; cosine 0.77; not in any Development; closest member (cosine 0.77) is in D3
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · The EUCCS proposal press release vs its accompanying factsheet explainer.
- **owner verdict:** ____

### C104  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-1` · t4 | `sx-121` · t4 |
| published | 2026-09-30 07:00:24.000000 | 2026-09-30 08:36:00.000000 |
| source · lang | Defense.gov · en | Rai News Esteri · it |
| headline | Statement by Chief Pentagon Spokesman Sean Parnell on the Conclusion of the U.S. Military Mission in Iraq | Gli Stati Uniti annunciano la fine ufficiale della missione in Iraq |
| current Development | D9 | - |
| places | Iraq, U.S. | Iraq, Stati Uniti |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: one item not in any Development; cosine 0.39; it vs en, shared ['Iraq', 'Sean Parnell']: not grouped together
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence high · Pentagon spokesman Parnell's statement and Rai's report of it on the official end of the Iraq mission.
- **owner verdict:** ____

### C105  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-139` · t3 | `sx-41` · t4 |
| published | 2026-09-29 15:22:00.000000 | 2026-09-30 08:35:42.000000 |
| source · lang | Rai News Esteri · it | ANSA Mondo · it |
| headline | Burnham: "Londra per troppo tempo sulla strada sbagliata, miglioreremo i rapporti con l'UE" | Burnham su Brexit, 'tutte le opzioni sul tavolo, inclusa riadesione a Ue' |
| current Development | D25 | D25 |
| places | Bruxelles, Londra, Regno Unito | - |

- D25: "Burnham su Brexit, 'tutte le opzioni sul tavolo, inclusa riadesione a Ue'" · 2 items · sources ANSA Mondo, Rai News Esteri · principals Burnham
- current system: same Development D25; cosine 0.56; D25: grouped together at tick 4
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · Burnham's 29 Sep conference speech vs his 30 Sep BBC Radio remarks on EU rejoining.
- **owner verdict:** ____

### C106  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-176` · t4 | `sx-129` · t3 |
| published | 2026-09-30 03:29:14.000000 | 2026-09-29 23:05:00.000000 |
| source · lang | France 24 Español · es | Rai News Esteri · it |
| headline | Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante" | Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa" |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.51; D6: attached at tick 4 to a Development created at tick 3
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence high · Report of the 'morally binding' AI accord vs experts' critique piece.
- **owner verdict:** ____

### C107

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-408` · t1 | `sx-424` · t1 |
| published | 2026-09-28 12:00:00.000000 | 2026-09-28 23:02:52.000000 |
| source · lang | UN News · en | UN Press · en |
| headline | From energy crisis to energy transition: How renewables are reshaping energy security | International Security Rapidly Deteriorates; General Assembly Urges Nations to Address Weaker Global Arms Treaties and Heightened Nuclear Risks |
| current Development | - | - |
| places | Middle East | Middle East |

- current system: neither in a Development; cosine 0.45; same tick, different outlets, cosine 0.45: below the link threshold, never grouped
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Renewables/energy security feature vs GA nuclear risk meeting.
- **owner verdict:** ____

### C108

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-74` · t4 | `sx-263` · t3 |
| published | 2026-09-30 08:37:41.000000 | 2026-09-29 18:24:27.000000 |
| source · lang | Europa Press Internacional · es | El País Internacional · es |
| headline | Trump anuncia una gira de 32 días por todo EEUU para hacer campaña de cara a las elecciones de noviembre | Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente |
| current Development | - | D6 |
| places | EE.UU. | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: one item not in any Development; cosine 0.55; not in any Development; closest member (cosine 0.55) is in D6
- **proposed:** `DIFFERENT_DEVELOPMENT` (unrelated) · confidence high · Trump's 32-day midterm campaign tour announcement vs America.gov launch.
- **owner verdict:** ____

### C109  · flags: grows_same_id, late_attach

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-164` · t4 | `sx-149` · t2 |
| published | 2026-09-30 01:04:01.000000 | 2026-09-29 11:08:00.000000 |
| source · lang | France 24 · en | DW World · en |
| headline | US forces leave Iraq, raising fears of Iran-backed militias amid power vacuum | Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission against ISIS after 12 years |
| current Development | D9 | D9 |
| places | Iran, Iraq, U.S. | Baghdad, Iraq, U.S. |

- D9: "Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission agains" · 5 items · sources DW World, Defense News, Defense.gov, France 24 · principals U.S., Washington
- current system: same Development D9; cosine 0.70; D9: attached at tick 4 to a Development created at tick 3
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Both report the US completing its troop withdrawal from Iraq.
- **owner verdict:** ____

### C110

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-127` · t4 | `sx-77` · t4 |
| published | 2026-09-30 04:06:00.000000 | 2026-09-30 07:40:40.000000 |
| source · lang | Rai News Esteri · it | Europa Press Internacional · es |
| headline | Marocco, Fatima Zahara Mansouri è la prima donna premier della storia del Paese | La primera ministra designada de Marruecos iniciará hoy una ronda de contactos para ensamblar el nuevo Gobierno |
| current Development | D18 | D19 |
| places | Marocco, Marrakech, Paese Avvocata, Regno | Gobierno, Marruecos |

- D18: "Marocco, Fatima Ezzahra El Mansouri sarà la prima premier donna del Regno" · 3 items · sources Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- D19: "La primera ministra designada de Marruecos iniciará hoy una ronda de contactos para ensamb" · 2 items · sources BBC Mundo, Europa Press Internacional · principals -
- current system: different Developments; cosine 0.56; separate Developments D18 and D19 (closest items cosine 0.56; shared principals [])
- **proposed:** `DIFFERENT_DEVELOPMENT` (follow-up) · confidence high · Mansouri becoming PM vs her subsequent round of coalition consultations starting Wednesday.
- **owner verdict:** ____

### C111

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-156` · t4 | `sx-168` · t3 |
| published | 2026-09-30 08:42:08.000000 | 2026-09-29 21:05:00.000000 |
| source · lang | France 24 · en | France 24 · en |
| headline | Trump puts trust in AI bosses to 'police themselves' | Trump says he doesn't want to work with China on AI safety |
| current Development | - | - |
| places | U.S. | China, South Korea, U.S. |

- current system: neither in a Development; cosine 0.66; ticks 4 and 3, cosine 0.66: not grouped together
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence medium · Trump announcing the self-regulation commitment at the luncheon vs his earlier statement refusing AI safety cooperation with China.
- **owner verdict:** ____

### C112  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-267` · t3 | `sx-263` · t3 |
| published | 2026-09-29 20:42:05.000000 | 2026-09-29 18:24:27.000000 |
| source · lang | Clarín Mundo · es | El País Internacional · es |
| headline | Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA | Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente |
| current Development | D6 | D6 |
| places | - | - |

- D6: "Trump, 'Usa valutano comitato di 10 persone per vigilare sull'IA'" · 15 items · sources ANSA Mondo, Clarín Mundo, El País Internacional, Europa Press Internacional, France 24 Español, Il Sole 24 Ore Mondo, Rai News Esteri · principals Donald Trump, Trump
- current system: same Development D6; cosine 0.54; tick 4: link cut by segmentation guard 'headline_similarity'
- **proposed:** `DIFFERENT_DEVELOPMENT` · confidence high · AI accord announcement after the meeting vs America.gov launch.
- **owner verdict:** ____

### C113  · flags: should_merge

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-39` · t4 | `sx-232` · t4 |
| published | 2026-09-30 09:27:04.000000 | 2026-09-30 09:25:00.000000 |
| source · lang | ANSA Mondo · it | Il Sole 24 Ore Mondo · it |
| headline | Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino | Allarme su volo FlyDubai dirottato, copilota accoltella comandante. Tentativo di far schiantare l’aereo |
| current Development | - | D21 |
| places | Oman | Dubai, Israele |

- D21: "'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'" · 6 items · sources ANSA Mondo, El País Internacional, Il Sole 24 Ore Mondo, Rai News Esteri · principals -
- current system: one item not in any Development; cosine 0.65; tick 4: link cut by segmentation guard 'disjoint_locations'
- **proposed:** `SAME_DEVELOPMENT` (update) · confidence medium · Same FlyDubai incident; one reports the stabbing/crash attempt, the other the revised pilot nationalities.
- **owner verdict:** ____

### C114  · flags: grows_same_id

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-279` · t4 | `sx-13` · t3 |
| published | 2026-09-30 02:28:13.000000 | 2026-09-29 17:32:58.000000 |
| source · lang | Kyiv Independent · en | State Department · en |
| headline | US imposes sanctions against Russian companies tied to Iran weapons procurement | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet |
| current Development | D14 | D14 |
| places | China, Hong Kong, Iran, Pakistan, Russia | Iran, Russia, Sheet, U.S. |

- D14: "United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restriction" · 3 items · sources DW World, Kyiv Independent, State Department · principals U.S.
- current system: same Development D14; cosine 0.55; D14: grouped together at tick 4
- **proposed:** `SAME_DEVELOPMENT` (rewrite) · confidence medium · Kyiv Independent's report of US sanctions on 13 entities tied to Iran weapons procurement likely describes the 29 Sep State Department fact sheet on disrupting Iran's proliferation efforts.
- **owner verdict:** ____

### C115  · flags: should_split

| | Item 1 | Item 2 |
|---|---|---|
| id · tick | `sx-152` · t2 | `sx-13` · t3 |
| published | 2026-09-29 00:01:00.000000 | 2026-09-29 17:32:58.000000 |
| source · lang | DW World · en | State Department · en |
| headline | US sanctions on Iran's aviation industry make travel less predictable as countries cancel flights | United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet |
| current Development | D14 | D14 |
| places | Iran, U.S. | Iran, Russia, Sheet, U.S. |

- D14: "United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restriction" · 3 items · sources DW World, Kyiv Independent, State Department · principals U.S.
- current system: same Development D14; cosine 0.50; D14: grouped together at tick 4; D14: least similar members of a 3-item Development (cosine 0.50)
- **proposed:** `DIFFERENT_DEVELOPMENT` (commentary) · confidence medium · Analysis of effects of US aviation sanctions on Iran vs the State Department's 29 Sep proliferation-sanctions fact sheet.
- **owner verdict:** ____

