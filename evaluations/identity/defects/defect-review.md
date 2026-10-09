# Development identity defect set: owner review

Baseline: identity code `0eff3ea` (Phase 2 identity, GDELT headline-only rule; cross-language stage disabled). Nothing in identity logic has changed. Each case is a pair of item sets with the owner-approved expected identity, the Developments the baseline forms today, the class and the suspected root cause. Record verdicts in `owner-verdicts.yaml` (class / expected: ACCEPT or a correction; note).

| class | cases |
|---|---|
| OVERMERGE | 42 |
| CROSS_LANGUAGE_MISS | 43 |
| SPLIT | 2 |
| LATE_ATTACHMENT_MISS | 0 |
| SAME_LANGUAGE_RECALL_MISS | 17 |
| AMBIGUOUS | 1 |
| CORRECT_BEHAVIOR | 23 |

## OVERMERGE (42)

### D004 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 A002 (owner (agrees with draft)))
- **References:** IG A002
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them (shared Development [4], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct_action

**A** Developments D4 (2 items) · langs en
  actors: Canada, Carney, Donald Trump, Mark Carney, Trump · places: Canada, US
- `b-ed25155d038d` 2026-08-22T18:20 (tick 4) [BBC World, en] [D4] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse

**B** Developments D4 (2 items) · langs en
  actors: Canada, Carney, Donald Trump, Mark Carney, Trump · places: Canada, Manitoba, US, Washington
- `b-320f20d36f00` 2026-08-21T03:12 (tick 1) [South China Morning Post, en] [D4] Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud

---

### D005 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 A021 (owner (agrees with draft)))
- **References:** IG A021
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them (shared Development [3], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** same situation though, also natural calamity here (should trigger automatic aggregation/clustering)

**A** Developments D3 (3 items) · langs en
  actors: - · places: DR Congo
- `b-2e0da6b7e7eb` 2026-08-21T13:44 (tick 2) [BBC World, en] [D3] Ebola vaccine trial to start in DR Congo as warning issued over speed of infections

**B** Developments D3 (3 items) · langs en
  actors: - · places: Congo, Kinshasa
- `b-8826249c972c` 2026-08-22T10:13 (tick 3) [Al Jazeera, en] [D3] More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo

---

### D006 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 A022 (owner (agrees with draft)))
- **References:** IG A022
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them (shared Development [3], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** later occurrence but same situation, natural disaster

**A** Developments D3 (3 items) · langs en
  actors: - · places: -
- `b-422186e87411` 2026-08-22T11:15 (tick 3) [Al Jazeera, en] [D3] Ebola continues to spread in the DRC as 16,000 vaccine doses arrive

**B** Developments D3 (3 items) · langs en
  actors: - · places: DR Congo
- `b-2e0da6b7e7eb` 2026-08-21T13:44 (tick 2) [BBC World, en] [D3] Ebola vaccine trial to start in DR Congo as warning issued over speed of infections

---

### D008 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R013 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB R013 (NO_RELATION)
- **Root cause (suspected):** relation pair inside one Development (shared Development [4], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D4 (2 items) · langs en
  actors: Canada, Carney, Donald Trump, Mark Carney, Trump · places: Canada, Manitoba, US, Washington
- `b-320f20d36f00` 2026-08-21T03:12 (tick 1) [South China Morning Post, en] [D4] Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trade feud

**B** Developments D4 (2 items) · langs en
  actors: Canada, Carney, Donald Trump, Mark Carney, Trump · places: Canada, US
- `b-ed25155d038d` 2026-08-22T18:20 (tick 4) [BBC World, en] [D4] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse
- `b-f43c963adf42` 2026-08-22T20:10 (tick 4) [BBC World, en] [-] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talks collapse

---

### D009 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R029 = reaction_to (owner verdict: two distinct occurrences))
- **References:** RB R029 (reaction_to); IG A023
- **Root cause (suspected):** relation pair inside one Development (shared Development [5], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** different but same situation: action-reaction or co-causation mechanism, one likely occurs in response to or because of the other

**A** Developments D5 (3 items) · langs en
  actors: Israel · places: Israel, Palestine, West Bank
- `b-52e7176bac0a` 2026-08-21T05:00 (tick 1) [BBC World, en] [D5] Israel re-establishes closed West Bank settlement, defying growing international protests

**B** Developments D5 (3 items) · langs en
  actors: Israel · places: Israel, Occupied West Bank
- `b-e65cd1bb15f4` 2026-08-22T12:51 (tick 4) [Al Jazeera, en] [D5] Jewish activists push back against Israeli settlers

---

### D010 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R060 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB R060 (NO_RELATION); IG A013
- **Root cause (suspected):** relation pair inside one Development (shared Development [5], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct action / development but same situation, or rather an aspect of the situation between Israel and Palestine and neighboring nations

**A** Developments D5 (3 items) · langs en
  actors: Israel · places: Israel, Occupied West Bank
- `b-e65cd1bb15f4` 2026-08-22T12:51 (tick 4) [Al Jazeera, en] [D5] Jewish activists push back against Israeli settlers

**B** Developments D5 (3 items) · langs en
  actors: Israel · places: Israel, Occupied West Bank, Palestine, Qaryut
- `b-9d435faf259d` 2026-08-22T15:45 (tick 4) [Al Jazeera, en] [D5] Settlers target Palestinian homes in Occupied West Bank’s Area B

---

### D011 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R082 = same_calamity_lifecycle (owner verdict: two distinct occurrences))
- **References:** RB R082 (same_calamity_lifecycle)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (3 items) · langs en
  actors: - · places: DR Congo
- `b-2e0da6b7e7eb` 2026-08-21T13:44 (tick 2) [BBC World, en] [D3] Ebola vaccine trial to start in DR Congo as warning issued over speed of infections

**B** Developments D3 (3 items) · langs en
  actors: - · places: Congo, Kinshasa
- `b-422186e87411` 2026-08-22T11:15 (tick 3) [Al Jazeera, en] [D3] Ebola continues to spread in the DRC as 16,000 vaccine doses arrive
- `b-8826249c972c` 2026-08-22T10:13 (tick 3) [Al Jazeera, en] [D3] More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo

---

### D012 · 2026-08-31

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R030 = same_calamity_lifecycle (owner verdict: two distinct occurrences))
- **References:** RB R030 (same_calamity_lifecycle)
- **Root cause (suspected):** relation pair inside one Development (shared Development [2], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D2 (2 items) · langs en
  actors: Indonesia, Malaysia · places: Indonesia, Kuching, Malaysia, Samarahan, Sarawak, West Kalimantan
- `b-d71f2886d120` 2026-08-31T07:10 (tick 1) [South China Morning Post, en] [D2] Malaysia’s air quality turns hazardous as Indonesian wildfires burn

**B** Developments D2 (2 items) · langs en
  actors: Indonesia, Malaysia · places: Borneo, Indonesia
- `b-df14f0a7ac2b` 2026-08-31T22:05 (tick 2) [BBC World, en] [D2] Orangutans in danger as wildfires blaze through Borneo

---

### D017 · 2026-09-25

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 B008 (owner (agrees with draft)))
- **References:** IG B008
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them (shared Development [3], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** it's a distinct action but the area of interest is the same: of course Xi did not travel all the way there for a report of Trump's building tour, despite this being the headline. It's something that happened in the background of other important meetings

**A** Developments D3 (2 items) · langs en
  actors: Donald Trump, Trump, Xi Jinping · places: Beijing, China, Great Hall of the People, Oval Office, South Lawn, United States
- `b-683038d2cd37` 2026-09-25T08:05 (tick 4) [South China Morning Post, en] [D3] Trump gives Xi a tour of his pet White House building projects, including the ballroom

**B** Developments D3 (2 items) · langs en
  actors: Donald Trump, Trump, Xi Jinping · places: China, Taiwan
- `b-97cb65d1a469` 2026-09-25T03:57 (tick 4) [BBC World, en] [D3] Xi got Trump's red carpet welcome - but not everything he wanted

---

### D018 · 2026-09-25

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 B011 (owner (agrees with draft)))
- **References:** IG B011
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them (shared Development [1], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** follow_up_update

**A** Developments D1 (2 items) · langs en
  actors: Pakistan, Taliban · places: Afghanistan, Pakistan
- `b-38730424bfbc` 2026-09-25T04:22 (tick 4) [Al Jazeera, en] [D1] Pakistani forces kill Afghan Taliban fighters in border escalation

**B** Developments D1 (2 items) · langs en
  actors: Pakistan, Taliban · places: Afghanistan, Pakistan
- `b-14aae9d37ebe` 2026-09-24T19:02 (tick 3) [BBC World, en] [D1] Four civilians killed in Pakistani strikes in Afghanistan, Taliban says

---

### D019 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R014 = reaction_to (owner verdict: two distinct occurrences))
- **References:** RB R014 (reaction_to)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Strait of Hormuz, Tehran, US
- `b-03bf5d3fc39a` 2026-09-27T00:00 (tick 1) [Al Jazeera, en] [D3] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan

**B** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Strait, Tehran, Washington
- `b-11af3f1b218b` 2026-09-28T00:00 (tick 3) [Al Jazeera, en] [D3] Iran war live: Tehran open to ‘real diplomacy’, ready for ‘apocalyptic war’
- `b-c5f73c1eff91` 2026-09-27T17:46 (tick 2) [Al Jazeera, en] [-] ‘Iran ready for doomsday war’, FM Araghchi says

---

### D020 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R031 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB R031 (NO_RELATION)
- **Root cause (suspected):** relation pair inside one Development (shared Development [9], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D9 (5 items) · langs en
  actors: - · places: Nepal
- `b-004f547a2ee6` 2026-09-27T17:29 (tick 2) [Al Jazeera, en] [D9] One month after Nepal’s catastrophic floods, thousands remain missing

**B** Developments D9 (5 items) · langs en
  actors: - · places: Nepal
- `b-c2228010948d` 2026-09-28T04:44 (tick 3) [Al Jazeera, en] [D9] 14 killed, a dozen missing as Nepal is hit by more floods and landslides

---

### D021 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R046 = same_convened_event (owner verdict: two distinct occurrences))
- **References:** RB R046 (same_convened_event)
- **Root cause (suspected):** relation pair inside one Development (shared Development [2], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D2 (3 items) · langs en
  actors: Pope · places: France, Lourdes, US
- `b-4e5e0bc4c49b` 2026-09-27T23:14 (tick 2) [Al Jazeera, en] [D2] Pope pledges action on clergy child abuse in meeting with French survivors
- `b-7e163e96ca25` 2026-09-27T09:16 (tick 1) [South China Morning Post, en] [D2] Pope meets victims of sex abuse, urges ‘wise leaders’ as French election looms

**B** Developments D2 (3 items) · langs en
  actors: Pope · places: France, Lourdes
- `b-9f2fd2c29401` 2026-09-27T11:38 (tick 1) [BBC World, en] [D2] 'Scourge' of abuse must be rooted out, says Pope during Lourdes visit

---

### D022 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R115 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB R115 (NO_RELATION)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Strait of Hormuz, Tehran, US
- `b-03bf5d3fc39a` 2026-09-27T00:00 (tick 1) [Al Jazeera, en] [D3] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan

**B** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, US
- `b-f0d7399ed7a6` 2026-09-27T14:36 (tick 2) [Al Jazeera, en] [D3] Strait of Hormuz tensions linger as Iran and US move further from a deal

---

### D023 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R132 = co_caused_with (owner verdict: two distinct occurrences))
- **References:** RB R132 (co_caused_with)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Tehran, US
- `b-7dd9705dba63` 2026-09-27T07:44 (tick 1) [BBC World, en] [D3] Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal

**B** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Iran, New York, Strait of Hormuz, Tehran, US
- `b-6df939d5bb83` 2026-09-27T19:16 (tick 2) [South China Morning Post, en] [D3] Trump expects new Iran talks despite rejecting deal offer

---

### D024 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T018 = reaction_to (owner verdict: two distinct occurrences))
- **References:** RB T018 (reaction_to)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Strait of Hormuz, Tehran, US
- `b-03bf5d3fc39a` 2026-09-27T00:00 (tick 1) [Al Jazeera, en] [D3] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan

**B** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Tehran, US
- `b-7dd9705dba63` 2026-09-27T07:44 (tick 1) [BBC World, en] [D3] Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal

---

### D025 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T029 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB T029 (NO_RELATION)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, US
- `b-f0d7399ed7a6` 2026-09-27T14:36 (tick 2) [Al Jazeera, en] [D3] Strait of Hormuz tensions linger as Iran and US move further from a deal

**B** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Strait, Tehran, Washington
- `b-11af3f1b218b` 2026-09-28T00:00 (tick 3) [Al Jazeera, en] [D3] Iran war live: Tehran open to ‘real diplomacy’, ready for ‘apocalyptic war’
- `b-c5f73c1eff91` 2026-09-27T17:46 (tick 2) [Al Jazeera, en] [-] ‘Iran ready for doomsday war’, FM Araghchi says

---

### D026 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T037 = follow_up_to (owner verdict: two distinct occurrences))
- **References:** RB T037 (follow_up_to)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Strait of Hormuz, Tehran, US
- `b-03bf5d3fc39a` 2026-09-27T00:00 (tick 1) [Al Jazeera, en] [D3] Iran war live: Tehran awaits official response as Trump rejects Hormuz plan

**B** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Iran, New York, Strait of Hormuz, Tehran, US
- `b-6df939d5bb83` 2026-09-27T19:16 (tick 2) [South China Morning Post, en] [D3] Trump expects new Iran talks despite rejecting deal offer

---

### D027 · 2026-09-27-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T045 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB T045 (NO_RELATION)
- **Root cause (suspected):** relation pair inside one Development (shared Development [3], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, Tehran, US
- `b-7dd9705dba63` 2026-09-27T07:44 (tick 1) [BBC World, en] [D3] Iranian minister says only negotiation can end conflict after Trump rejects Hormuz deal

**B** Developments D3 (5 items) · langs en
  actors: Donald Trump, Iran, Tehran, Trump, US, Washington · places: Hormuz, Iran, US
- `b-f0d7399ed7a6` 2026-09-27T14:36 (tick 2) [Al Jazeera, en] [D3] Strait of Hormuz tensions linger as Iran and US move further from a deal

---

### D028 · 2026-09-29-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 R100 = same_convened_event (owner verdict: two distinct occurrences))
- **References:** RB R100 (same_convened_event)
- **Root cause (suspected):** relation pair inside one Development (shared Development [8], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D8 (2 items) · langs en
  actors: Benjamin Netanyahu, Israel, UAE · places: Abu Dhabi, Israel
- `b-0115154e4b8c` 2026-09-28T19:42 (tick 1) [Al Jazeera, en] [D8] UAE confirms Netanyahu visit to Abu Dhabi

**B** Developments D8 (2 items) · langs en
  actors: Benjamin Netanyahu, Israel, UAE · places: Israel, UAE
- `b-dfaa73241bf8` 2026-09-28T22:25 (tick 1) [South China Morning Post, en] [D8] Israel security agency files complaint over TV report that Netanyahu visited UAE

---

### D029 · 2026-09-29-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T009 = commentary_on (owner verdict: two distinct occurrences))
- **References:** RB T009 (commentary_on)
- **Root cause (suspected):** relation pair inside one Development (shared Development [16], 4 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D16 (4 items) · langs en
  actors: Malaysia · places: Kuala Lumpur, Malaysia, Myanmar
- `b-89d356fd2694` 2026-09-29T09:27 (tick 2) [Al Jazeera, en] [D16] Malaysia begins sending back Rohingya refugees despite safety warnings
- `b-9244faa26b60` 2026-09-29T07:00 (tick 2) [South China Morning Post, en] [D16] Malaysia begins sending thousands of Myanmar nationals back to war-torn homeland
- `b-b26c02100dbb` 2026-09-29T06:06 (tick 2) [BBC World, en] [D16] Malaysia begins controversial repatriation of asylum seekers to Myanmar

**B** Developments D16 (4 items) · langs en
  actors: Malaysia · places: Malaysia, Myanmar
- `b-faf3df1e7bae` 2026-09-29T11:22 (tick 2) [Al Jazeera, en] [D16] Malaysia gave refuge to Rohingya; now it wants them to go

---

### D030 · 2026-09-29-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T022 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB T022 (NO_RELATION)
- **Root cause (suspected):** relation pair inside one Development (shared Development [6], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D6 (3 items) · langs en
  actors: US · places: Iran, Iraq, Najaf, US
- `b-a6c5c12bf244` 2026-09-28T18:28 (tick 1) [South China Morning Post, en] [D6] US to grant sanctions waiver for flights between Iran and Iraq’s Najaf, source says

**B** Developments D6 (3 items) · langs en
  actors: US · places: Iran, Tehran, US
- `b-d93fa9820e25` 2026-09-29T00:00 (tick 2) [Al Jazeera, en] [D6] Iran war live: Trump says he did not offer Tehran sanctions relief

---

### D031 · 2026-09-29-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T023 = NO_RELATION (owner verdict: two distinct occurrences))
- **References:** RB T023 (NO_RELATION)
- **Root cause (suspected):** relation pair inside one Development (shared Development [6], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D6 (3 items) · langs en
  actors: US · places: Iran, Iraq, Najaf, Tehran, US
- `b-0d1e24ede095` 2026-09-28T18:50 (tick 1) [Al Jazeera, en] [D6] Flights between Iraq’s Najaf and Iran resumed as Tehran protests US curbs

**B** Developments D6 (3 items) · langs en
  actors: US · places: Iran, Tehran, US
- `b-d93fa9820e25` 2026-09-29T00:00 (tick 2) [Al Jazeera, en] [D6] Iran war live: Trump says he did not offer Tehran sanctions relief

---

### D048 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C002 (owner (agrees with draft)))
- **References:** IG C002
- **Root cause (suspected):** a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct action, one is an announcement coming from Trump regarding how AI should be called (should trigger a question: why/why now?) , the other is Big Tech regulation topic

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-48` 2026-09-30 01:10 (tick 4) [ANSA Mondo, it] [D9] Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza'

**B** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-129` 2026-09-29 23:05 (tick 3) [Rai News Esteri, it] [D9] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa"

---

### D051 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C007 (owner (agrees with draft)))
- **References:** IG C007
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (12-item Development); segmentation did not cut them (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct_action

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-131` 2026-09-29 23:32 (tick 3) [Rai News Esteri, it] [D9] Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia

**B** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-129` 2026-09-29 23:05 (tick 3) [Rai News Esteri, it] [D9] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa"

---

### D052 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C012 (owner (agrees with draft)))
- **References:** IG C012
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (12-item Development); segmentation did not cut them (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct_action

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-131` 2026-09-29 23:32 (tick 3) [Rai News Esteri, it] [D9] Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia

**B** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: -
- `sx-263` 2026-09-29 18:24 (tick 3) [El País Internacional, es] [D9] Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente

---

### D054 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C017 (owner (agrees with draft)))
- **References:** IG C017
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (12-item Development); segmentation did not cut them (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct action but one is a commentary on the other

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-238` 2026-09-29 19:04 (tick 3) [Il Sole 24 Ore Mondo, it] [D9] Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence

**B** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-129` 2026-09-29 23:05 (tick 3) [Rai News Esteri, it] [D9] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa"

---

### D055 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C022 (owner (agrees with draft)))
- **References:** IG C022
- **Root cause (suspected):** a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** commentary_or_analysis

**A** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: Estados Unidos, Gobierno, Gobierno de EEUU
- `sx-71` 2026-09-29 23:02 (tick 3) [Europa Press Internacional, es] [D9] Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteligencia' en todas las agencias del Gobierno de EEUU

**B** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: -
- `sx-176` 2026-09-30 03:29 (tick 4) [France 24 Español, es] [D9] Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante"

---

### D056 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C026 (owner (agrees with draft)))
- **References:** IG C026; IG G10
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them (shared Development [18], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct_action; owner, 2026-10-07: D19 split: rial low vs US response

**A** Developments D18 (2 items) · langs es
  actors: EE.UU., Estados Unidos, Irán, Teheran · places: Estados Unidos, Irán
- `sx-264` 2026-09-29 22:45 (tick 3) [Clarín Mundo, es] [D18] Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico

**B** Developments D18 (2 items) · langs es
  actors: EE.UU., Estados Unidos, Irán, Teheran · places: EE.UU., Estados Unidos, Irán, Teheran
- `sx-75` 2026-09-30 08:42 (tick 4) [Europa Press Internacional, es] [D18] Irán confirma que recibió la respuesta oficial de EEUU a su última propuesta para un acuerdo de paz

---

### D058 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C037 (owner (agrees with draft)))
- **References:** IG C037
- **Root cause (suspected):** a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) (shared Development [8], 5 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct_action

**A** Developments D8 (5 items) · langs es
  actors: Emmanuel Macron, Macron · places: Francia
- `sx-181` 2026-09-30 02:47 (tick 4) [France 24 Español, es] [D8] Trabajadores públicos franceses se movilizan para exigir aumentos de salarios

**B** Developments D8 (5 items) · langs es
  actors: Emmanuel Macron, Macron · places: España
- `sx-111` 2026-09-29 15:04 (tick 3) [BBC Mundo, es] [D8] La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisis de vivienda en España

---

### D062 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C073 (owner (agrees with draft)))
- **References:** IG C073
- **Root cause (suspected):** a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct_action

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-235` 2026-09-30 08:09 (tick 4) [Il Sole 24 Ore Mondo, it] [D9] Ft: Trump valuta il divieto di export del gasolio per contenere la crisi dei prezzi

**B** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-129` 2026-09-29 23:05 (tick 3) [Rai News Esteri, it] [D9] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa"

---

### D064 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C079 (owner (agrees with draft)))
- **References:** IG C079
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them (shared Development [14], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** for conflicts: we should be able to divide testimony from actual event reporting

**A** Developments D14 (2 items) · langs es
  actors: Ejército de Israel, Israel · places: Gaza, Yabalia
- `sx-245` 2026-09-29 15:14 (tick 3) [El País Internacional, es] [D14] Tres soldados israelíes sobre Gaza: “Llegó un momento en que ya no parecía tan grave matar a decenas de personas”

**B** Developments D14 (2 items) · langs es
  actors: Ejército de Israel, Israel · places: Estados Unidos, Franja de Gaza, Gaza, Hamás, Israel
- `sx-80` 2026-09-30 09:11 (tick 4) [Europa Press Internacional, es] [D14] Muere una palestina en un nuevo ataque de Israel contra la ciudad de Gaza a pesar del alto el fuego

---

### D066 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C094 (owner (agrees with draft)))
- **References:** IG C094
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them (shared Development [12], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** one is the commentary (spanish, US senate vote refusal) vs the raid itself

**A** Developments D12 (3 items) · langs es
  actors: - · places: Cisjordania, Senado de EEUU
- `sx-79` 2026-09-30 05:02 (tick 4) [Europa Press Internacional, es] [D12] El Senado de EEUU rechaza votar una resolución acerca de la violencia en Cisjordania tras el último ataque de colonos

**B** Developments D12 (3 items) · langs it
  actors: - · places: Cisgiordania, Condanna Usa
- `sx-243` 2026-09-29 06:12 (tick 2) [Il Sole 24 Ore Mondo, it] [D12] Cisgiordania, raid di coloni israeliani contro famiglia palestinese a Jalud. Condanna Usa

---

### D070 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C105 (owner (agrees with draft)))
- **References:** IG C105
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them (shared Development [15], 2 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct action but same situation

**A** Developments D15 (2 items) · langs it
  actors: Burnham · places: Bruxelles, Londra, Regno Unito
- `sx-139` 2026-09-29 15:22 (tick 3) [Rai News Esteri, it] [D15] Burnham: "Londra per troppo tempo sulla strada sbagliata, miglioreremo i rapporti con l'UE"

**B** Developments D15 (2 items) · langs it
  actors: Burnham · places: -
- `sx-41` 2026-09-30 08:35 (tick 4) [ANSA Mondo, it] [D15] Burnham su Brexit, 'tutte le opzioni sul tavolo, inclusa riadesione a Ue'

---

### D071 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C106 (owner (agrees with draft)))
- **References:** IG C106
- **Root cause (suspected):** a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** commentary_or_analysis

**A** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: -
- `sx-176` 2026-09-30 03:29 (tick 4) [France 24 Español, es] [D9] Trump y los gigantes de la inteligencia artificial sellan un acuerdo "moralmente vinculante"

**B** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-129` 2026-09-29 23:05 (tick 3) [Rai News Esteri, it] [D9] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big Tech è una farsa"

---

### D072 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C112 (owner (agrees with draft)))
- **References:** IG C112
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (12-item Development); segmentation did not cut them (shared Development [9], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct_action

**A** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: -
- `sx-267` 2026-09-29 20:42 (tick 3) [Clarín Mundo, es] [D9] Donald Trump anunció que los líderes del sector tecnológico firmaron un acuerdo "moralmente vinculante" para regular la IA

**B** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: -
- `sx-263` 2026-09-29 18:24 (tick 3) [El País Internacional, es] [D9] Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente

---

### D074 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C115 (owner (agrees with draft)))
- **References:** IG C115
- **Root cause (suspected):** distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them (shared Development [11], 3 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** distinct action but same situation

**A** Developments D11 (3 items) · langs en
  actors: U.S. · places: Iran, U.S.
- `sx-152` 2026-09-29 00:01 (tick 2) [DW World, en] [D11] US sanctions on Iran's aviation industry make travel less predictable as countries cancel flights

**B** Developments D11 (3 items) · langs en
  actors: U.S. · places: Iran, Russia, Sheet, U.S.
- `sx-13` 2026-09-29 17:32 (tick 3) [State Department, en] [D11] United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet

---

### D100 · 2026-10-03-live

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 4 G07 (owner-given (2026-10-07)))
- **References:** IG G07
- **Root cause (suspected):** whole-storyline overmerge (shared Development [5], 12 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints
- **Notes:** owner, 2026-10-07: T025: two days of the protest wave

**A** Developments D5 (12 items) · langs en
  actors: - · places: France
- `s-1228` 2026-09-29 21:32 (tick 1) [BBC World, en] [D5] More than 400 detained as France student protests escalate

**B** Developments D5 (12 items) · langs en
  actors: - · places: France
- `s-1380` 2026-09-30 13:18 (tick 3) [BBC World, en] [D5] Dozens hurt and hundreds arrested in wave of French school protests

---

### D101 · 2026-10-03-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T012 = follow_up_to (owner verdict: two distinct occurrences))
- **References:** RB T012 (follow_up_to)
- **Root cause (suspected):** relation pair inside one Development (shared Development [19], 14 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Tennessee
- `s-1245` 2026-09-29 23:39 (tick 1) [BBC World, en] [D19] US Supreme Court denies Christa Pike's last-ditch bid to halt execution

**B** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Nashville, Tennessee, US
- `s-1663` 2026-10-01 16:45 (tick 5) [BBC World, en] [D19] Tennessee halts executions after Christa Pike survives two lethal injection attempts
- `s-1790` 2026-10-02 03:02 (tick 6) [South China Morning Post, en] [D19] Christa Pike in ‘life-saving care’ after botched Tennessee execution
- `s-1834` 2026-10-02 07:58 (tick 6) [Al Jazeera, en] [D19] Lawyers for US inmate who survived lethal injections demand release
- `s-1921` 2026-10-02 20:57 (tick 7) [Al Jazeera, en] [D19] Christa Pike unconscious, on ventilator after botched execution: Lawyers
- `s-1935` 2026-10-02 20:32 (tick 7) [BBC World, en] [D19] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say

---

### D102 · 2026-10-03-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T013 = follow_up_to (owner verdict: two distinct occurrences))
- **References:** RB T013 (follow_up_to)
- **Root cause (suspected):** relation pair inside one Development (shared Development [19], 14 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Tennessee, US
- `s-1421` 2026-09-30 16:44 (tick 3) [Al Jazeera, en] [D19] US appeals court halts Tennessee execution of Christa Pike

**B** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Nashville, Tennessee, US
- `s-1663` 2026-10-01 16:45 (tick 5) [BBC World, en] [D19] Tennessee halts executions after Christa Pike survives two lethal injection attempts
- `s-1790` 2026-10-02 03:02 (tick 6) [South China Morning Post, en] [D19] Christa Pike in ‘life-saving care’ after botched Tennessee execution
- `s-1834` 2026-10-02 07:58 (tick 6) [Al Jazeera, en] [D19] Lawyers for US inmate who survived lethal injections demand release
- `s-1921` 2026-10-02 20:57 (tick 7) [Al Jazeera, en] [D19] Christa Pike unconscious, on ventilator after botched execution: Lawyers
- `s-1935` 2026-10-02 20:32 (tick 7) [BBC World, en] [D19] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say

---

### D103 · 2026-10-03-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T014 = follow_up_to (owner verdict: two distinct occurrences))
- **References:** RB T014 (follow_up_to)
- **Root cause (suspected):** relation pair inside one Development (shared Development [19], 14 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Tennessee, US
- `s-1404` 2026-09-30 16:00 (tick 3) [South China Morning Post, en] [D19] US Tennessee’s first execution of a woman in 200 years halted

**B** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Nashville, Tennessee, US
- `s-1663` 2026-10-01 16:45 (tick 5) [BBC World, en] [D19] Tennessee halts executions after Christa Pike survives two lethal injection attempts
- `s-1790` 2026-10-02 03:02 (tick 6) [South China Morning Post, en] [D19] Christa Pike in ‘life-saving care’ after botched Tennessee execution
- `s-1834` 2026-10-02 07:58 (tick 6) [Al Jazeera, en] [D19] Lawyers for US inmate who survived lethal injections demand release
- `s-1921` 2026-10-02 20:57 (tick 7) [Al Jazeera, en] [D19] Christa Pike unconscious, on ventilator after botched execution: Lawyers
- `s-1935` 2026-10-02 20:32 (tick 7) [BBC World, en] [D19] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say

---

### D104 · 2026-10-03-live

- **Expected:** DIFFERENT_DEVELOPMENT (relation gold rev 2 T040 = follow_up_to (owner verdict: two distinct occurrences))
- **References:** RB T040 (follow_up_to)
- **Root cause (suspected):** relation pair inside one Development (shared Development [19], 14 items)
- **Blocks a Phase 3 endpoint:** yes: the two occurrences have no distinct Development endpoints

**A** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Tennessee
- `s-1510` 2026-10-01 02:35 (tick 4) [Al Jazeera, en] [D19] Christa Pike’s execution by lethal injection fails in Tennessee

**B** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Nashville, Tennessee, US
- `s-1663` 2026-10-01 16:45 (tick 5) [BBC World, en] [D19] Tennessee halts executions after Christa Pike survives two lethal injection attempts
- `s-1790` 2026-10-02 03:02 (tick 6) [South China Morning Post, en] [D19] Christa Pike in ‘life-saving care’ after botched Tennessee execution
- `s-1834` 2026-10-02 07:58 (tick 6) [Al Jazeera, en] [D19] Lawyers for US inmate who survived lethal injections demand release
- `s-1921` 2026-10-02 20:57 (tick 7) [Al Jazeera, en] [D19] Christa Pike unconscious, on ventilator after botched execution: Lawyers
- `s-1935` 2026-10-02 20:32 (tick 7) [BBC World, en] [D19] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say

---

## CROSS_LANGUAGE_MISS (43)

### D050 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C006 (owner (agrees with draft)))
- **References:** IG C006
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D18 (2 items) · langs es
  actors: EE.UU., Estados Unidos, Irán, Teheran · places: Estados Unidos, Irán
- `sx-264` 2026-09-29 22:45 (tick 3) [Clarín Mundo, es] [D18] Por la guerra y la incertidumbre económica, la moneda de Irán se hunde en un mínimo histórico

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-536` 2026-09-30 01:15 (tick 4) [GDELT, en] [-] Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability

---

### D069 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C104 (owner (agrees with draft)))
- **References:** IG C104
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Iraq, U.S.
- `sx-1` 2026-09-30 07:00 (tick 4) [Defense.gov, en] [D5] Statement by Chief Pentagon Spokesman Sean Parnell on the Conclusion of the U.S. Military Mission in Iraq

**B** Developments none (not surfaced) · langs it
  actors: - · places: Iraq, Stati Uniti
- `sx-121` 2026-09-30 08:36 (tick 4) [Rai News Esteri, it] [-] Gli Stati Uniti annunciano la fine ufficiale della missione in Iraq

---

### D076 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G02 (owner-given (2026-10-07)))
- **References:** IG G02
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** owner, 2026-10-07: R138: White House AI luncheon, it / en

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-132` 2026-09-29 20:36 (tick 3) [Rai News Esteri, it] [D9] Trump incontra i vertici Big Tech sulla sicurezza AI: "Autoregolazione e nessun controllo federale"

**B** Developments none (not surfaced) · langs en
  actors: - · places: China, South Korea, U.S.
- `sx-168` 2026-09-29 21:05 (tick 3) [France 24, en] [-] Trump says he doesn't want to work with China on AI safety

---

### D077 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G03 (owner-given (2026-10-07)))
- **References:** IG G03
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** owner, 2026-10-07: R138: America.gov launch at the luncheon, es / en

**A** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: -
- `sx-263` 2026-09-29 18:24 (tick 3) [El País Internacional, es] [D9] Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente

**B** Developments none (not surfaced) · langs en
  actors: - · places: China, South Korea, U.S.
- `sx-168` 2026-09-29 21:05 (tick 3) [France 24, en] [-] Trump says he doesn't want to work with China on AI safety

---

### D080 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V001 (owner (agrees with draft)))
- **References:** IG V001
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-48` 2026-09-30 01:10 (tick 4) [ANSA Mondo, it] [D9] Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza'

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-22` 2026-09-29 21:21 (tick 3) [White House, en] [-] Fact Sheet: President Donald J. Trump Inaugurates The Era of Super Intelligence

---

### D081 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V003 (owner (agrees with draft)))
- **References:** IG V003
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Iran, Iraq, Tehran, U.S.
- `sx-491` 2026-09-29 14:40 (tick 3) [Defense News, en] [D5] US forces exiting Iraq after 2 decades, leaving opening for Iran

**B** Developments none (not surfaced) · langs es
  actors: - · places: EE.UU., Irak
- `sx-101` 2026-09-30 03:32 (tick 4) [BBC Mundo, es] [-] EE.UU. se retira completamente de Irak tras 20 años de presencia militar: cómo deja el país y qué ocurrirá ahora

---

### D082 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V010 (owner (agrees with draft)))
- **References:** IG V010
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs it
  actors: - · places: Haiti
- `sx-56` 2026-09-29 20:36 (tick 3) [ANSA Mondo, it] [-] Haiti, l'Onu proroga di sei mesi la missione contro le bande armate

**B** Developments none (not surfaced) · langs en
  actors: - · places: Haiti
- `sx-420` 2026-09-29 18:45 (tick 3) [UN Press, en] [-] Adopting Resolution 2829 (2026), Security Council Renews Haiti Gang Suppression Force for Six Months

---

### D083 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V011 (owner (agrees with draft)))
- **References:** IG V011
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D15 (2 items) · langs it
  actors: Burnham · places: -
- `sx-41` 2026-09-30 08:35 (tick 4) [ANSA Mondo, it] [D15] Burnham su Brexit, 'tutte le opzioni sul tavolo, inclusa riadesione a Ue'

**B** Developments none (not surfaced) · langs es
  actors: - · places: Liverpool, Reino Unido
- `sx-244` 2026-09-30 08:02 (tick 4) [El País Internacional, es] [-] Andy Burnham no descarta estudiar un futuro reingreso del Reino Unido en la UE

---

### D084 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V014 (owner corrected (2026-10-08)))
- **References:** IG V014
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** different developments, same attack wave

**A** Developments D20 (3 items) · langs it
  actors: - · places: Kiev, Vyshgorod
- `sx-47` 2026-09-30 02:30 (tick 4) [ANSA Mondo, it] [D20] Missili e droni su regione di Kiev, ucciso un bambino

**B** Developments none (not surfaced) · langs en
  actors: - · places: Moldova, Russia, Ukraine, Ukraine Russia
- `sx-277` 2026-09-30 07:03 (tick 4) [Kyiv Independent, en] [-] Drone crashes in Moldova amid Russian mass attack on Ukraine

---

### D085 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V020 (owner (agrees with draft)))
- **References:** IG V020
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D16 (3 items) · langs it
  actors: - · places: Marocco, Marrakech, Paese Avvocata, Regno
- `sx-127` 2026-09-30 04:06 (tick 4) [Rai News Esteri, it] [D16] Marocco, Fatima Zahara Mansouri è la prima donna premier della storia del Paese

**B** Developments D19 (2 items) · langs es
  actors: - · places: Marruecos
- `sx-108` 2026-09-30 00:03 (tick 4) [BBC Mundo, es] [D19] Fatima Zahra El Mansouri, la primera mujer elegida primera ministra de Marruecos

---

### D086 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V028 (owner (agrees with draft)))
- **References:** IG V028
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D12 (3 items) · langs es
  actors: - · places: Cisjordania, Senado de EEUU
- `sx-79` 2026-09-30 05:02 (tick 4) [Europa Press Internacional, es] [D12] El Senado de EEUU rechaza votar una resolución acerca de la violencia en Cisjordania tras el último ataque de colonos

**B** Developments none (not surfaced) · langs en
  actors: - · places: Israel, U.S., West Bank
- `sx-211` 2026-09-30 02:26 (tick 4) [Al Jazeera, en] [-] US Senate blocks resolution seeking report on Americans killed in West Bank

---

### D087 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V032 (owner (agrees with draft)))
- **References:** IG V032
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-238` 2026-09-29 19:04 (tick 3) [Il Sole 24 Ore Mondo, it] [D9] Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-22` 2026-09-29 21:21 (tick 3) [White House, en] [-] Fact Sheet: President Donald J. Trump Inaugurates The Era of Super Intelligence

---

### D088 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V034 (owner (agrees with draft)))
- **References:** IG V034
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs en
  actors: - · places: Gaza, Malaysia, Myanmar, West Bank
- `sx-396` 2026-09-29 12:00 (tick 3) [UN News, en] [-] World News in Brief: Deadly Myanmar strikes as Malaysia begins deportations, new emergency funding released, Gaza and West Bank update

**B** Developments none (not surfaced) · langs es
  actors: - · places: Ejército de Myanmar, Pobladores, Rakáin
- `sx-184` 2026-09-30 02:37 (tick 4) [France 24 Español, es] [-] Myanmar: ataque aéreo contra un mercado deja al menos 50 muertos

---

### D089 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V039 (owner (agrees with draft)))
- **References:** IG V039
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D9 (12 items) · langs es
  actors: Donald Trump, Trump · places: -
- `sx-263` 2026-09-29 18:24 (tick 3) [El País Internacional, es] [D9] Trump lanza una página oficial de información sobre el Gobierno de EE UU que le desmiente

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-26` 2026-09-29 14:45 (tick 3) [White House, en] [-] Fact Sheet: President Donald J. Trump Streamlines Access to Government Services Through America.gov

---

### D090 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V040 (owner (agrees with draft)))
- **References:** IG V040
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D13 (2 items) · langs es
  actors: - · places: Francia, Gobierno
- `sx-76` 2026-09-30 03:45 (tick 4) [Europa Press Internacional, es] [D13] Al menos 440 detenidos en Francia en protestas estudiantiles unidas a la huelga de cientos de miles en el sector público

**B** Developments D17 (2 items) · langs en
  actors: - · places: France
- `sx-88` 2026-09-29 21:55 (tick 3) [BBC World, en] [D17] More than 400 detained as France student protests escalate

---

### D091 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V043 (owner (agrees with draft)))
- **References:** IG V043
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Iran, Iraq, Tehran, U.S.
- `sx-491` 2026-09-29 14:40 (tick 3) [Defense News, en] [D5] US forces exiting Iraq after 2 decades, leaving opening for Iran

**B** Developments none (not surfaced) · langs it
  actors: - · places: Iraq
- `sx-140` 2026-09-29 15:20 (tick 3) [Rai News Esteri, it] [-] Iraq, gli ultimi soldati americani verso l’uscita: la lunga ombra di una guerra

---

### D092 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V046 (owner (agrees with draft)))
- **References:** IG V046
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs en
  actors: - · places: China, South Korea, U.S.
- `sx-168` 2026-09-29 21:05 (tick 3) [France 24, en] [-] Trump says he doesn't want to work with China on AI safety

**B** Developments none (not surfaced) · langs es
  actors: - · places: -
- `sx-273` 2026-09-29 16:03 (tick 3) [Clarín Mundo, es] [-] "Jamás frenaré el crecimiento" de la IA, dice Trump antes de reunirse con los mayores ejecutivos del sector

---

### D093 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V048 (owner (agrees with draft)))
- **References:** IG V048
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs en
  actors: - · places: Kyiv, Russia, Ukraine
- `sx-275` 2026-09-30 08:14 (tick 4) [Kyiv Independent, en] [-] Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack

**B** Developments D20 (3 items) · langs it
  actors: - · places: Kiev, Polonia, Ucraina
- `sx-237` 2026-09-30 05:33 (tick 4) [Il Sole 24 Ore Mondo, it] [D20] Ucraina: missili balistici russi su Kiev, 2 morti. La Polonia chiude due aeroporti

---

### D094 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V058 (owner (agrees with draft)))
- **References:** IG V058
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D7 (2 items) · langs en
  actors: Estonia, Tallinn · places: Estonia, Milrem GLASGOW, Russia, Scotland, Tallinn
- `sx-490` 2026-09-29 14:52 (tick 3) [Defense News, en] [D7] Estonia blames Russia in arson attack on military robotics firm Milrem

**B** Developments none (not surfaced) · langs es
  actors: - · places: Estonia, Londres, Rusia
- `sx-262` 2026-09-29 11:27 (tick 2) [El País Internacional, es] [-] Estonia acusa a Rusia del incendio en un fabricante de material militar

---

### D095 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V059 (owner (agrees with draft)))
- **References:** IG V059
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D19 (2 items) · langs es
  actors: - · places: Marruecos
- `sx-108` 2026-09-30 00:03 (tick 4) [BBC Mundo, es] [D19] Fatima Zahra El Mansouri, la primera mujer elegida primera ministra de Marruecos

**B** Developments none (not surfaced) · langs en
  actors: - · places: Morocco
- `sx-97` 2026-09-29 17:14 (tick 3) [BBC World, en] [-] First female prime minister named in Morocco after winning elections

---

### D096 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V060 (owner (agrees with draft)))
- **References:** IG V060
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D8 (5 items) · langs es
  actors: Emmanuel Macron, Macron · places: España
- `sx-270` 2026-09-29 18:43 (tick 3) [Clarín Mundo, es] [D8] Presionado por las protestas, Pedro Sánchez anuncia decretos clave para enfrentar la crisis de la vivienda en España

**B** Developments none (not surfaced) · langs it
  actors: - · places: Puerta del Sol, Spagna
- `sx-241` 2026-09-29 14:59 (tick 3) [Il Sole 24 Ore Mondo, it] [-] Spagna, Sánchez vara nuove misure contro la crisi abitativa: cosa cambia per affitti e sfratti

---

### D105 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G12 (owner-given (2026-10-07)))
- **References:** IG G12
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** owner, 2026-10-07: regression: RAF Fairford bombers, en / es

**A** Developments D17 (10 items) · langs en
  actors: Donald Trump, Trump, US · places: England, Iran, UK, US
- `s-2277` 2026-10-04 21:31 (tick 1) [South China Morning Post, en] [D17] US Air Force removes all bombers from UK airbase targeted by suspected terror attack

**B** Developments none (not surfaced) · langs es
  actors: - · places: Fairford
- `s-2623` 2026-10-05 07:42 (tick 2) [El País Internacional, es] [-] El Pentágono retira sus bombarderos de la base británica de Fairford tras el presunto intento de atentado

---

### D106 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G13 (owner-given (2026-10-07)))
- **References:** IG G13
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** owner, 2026-10-07: regression: RAF Fairford bombers, en / es

**A** Developments D17 (10 items) · langs en
  actors: Donald Trump, Trump, US · places: UK, US
- `s-2314` 2026-10-05 04:58 (tick 2) [BBC World, en] [D17] US air force removes all bombers from British military base RAF Fairford

**B** Developments none (not surfaced) · langs es
  actors: - · places: Estados Unidos, Londres, Reino Unido, Teherán
- `s-2639` 2026-10-04 22:24 (tick 1) [Clarín Mundo, es] [-] Estados Unidos retiró sus bombarderos de una base del Reino Unido tras descubrir un plan de atentado

---

### D107 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G14 (owner-given (2026-10-07)))
- **References:** IG G14
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** owner, 2026-10-07: regression: Siberian plague case, en / es

**A** Developments D40 (5 items) · langs en
  actors: Moscow, Russia, US, Washington · places: Russia, Siberia, US
- `s-2299` 2026-10-05 04:07 (tick 2) [Al Jazeera, en] [D40] Russian lab worker dies of suspected plague in Siberia; US monitoring case

**B** Developments D27 (5 items) · langs es
  actors: EE.UU., Moscú, Rusia · places: Irkutsk, Rusia, Shelejov
- `s-2432` 2026-10-05 06:53 (tick 2) [Europa Press Internacional, es] [D27] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio

---

### D108 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V005 (owner (agrees with draft)))
- **References:** IG V005
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** same_occurrence

**A** Developments D5 (14 items) · langs en
  actors: Bolsonaro, Brazil, Flavio Bolsonaro · places: Brazil, US
- `s-2246` 2026-10-04 17:48 (tick 1) [South China Morning Post, en] [D5] Brazilians head to polls in high-stakes, polarised election

**B** Developments D3 (56 items) · langs it
  actors: Bolsonaro, Flavio Bolsonaro, Partido Liberal de Bolsonaro · places: Brasile
- `s-2444` 2026-10-05 10:46 (tick 2) [ANSA Mondo, it] [D3] Astensione record in Brasile, il 21,08% non ha votato al primo turno

---

### D109 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V007 (owner (corrected draft)))
- **References:** IG V007
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** same_occurrence

**A** Developments none (not surfaced) · langs en
  actors: - · places: Brazil
- `s-2305` 2026-10-05 01:55 (tick 2) [Al Jazeera, en] [-] Brazil’s presidential race: Three key takeaways from the first round

**B** Developments none (not surfaced) · langs es
  actors: - · places: Brasil, Sciences Sociales de París
- `s-2593` 2026-10-05 03:11 (tick 2) [France 24 Español, es] [-] Lula y Bolsonaro se enfrentan en el balotaje en Brasil: ¿qué se puede concluir de la primera vuelta?

---

### D110 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V009 (owner (agrees with draft)))
- **References:** IG V009
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D22 (3 items) · langs it
  actors: Sanchez · places: Paese, Spagna
- `s-2562` 2026-10-05 12:08 (tick 3) [Rai News Esteri, it] [D22] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa

**B** Developments D18 (12 items) · langs es
  actors: Pedro Sanchez · places: España, Palacio de La Moncloa
- `s-2630` 2026-10-05 07:18 (tick 2) [Clarín Mundo, es] [D18] Pedro Sánchez adelantó las elecciones generales en España para el 29 de noviembre

---

### D111 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V019 (owner (agrees with draft)))
- **References:** IG V019
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs it
  actors: - · places: Kharkiv, Poltava
- `s-2454` 2026-10-05 10:07 (tick 2) [ANSA Mondo, it] [-] Doppio attacco russo su Kharkiv con missili Banderol, un morto

**B** Developments none (not surfaced) · langs en
  actors: - · places: Kharkiv, Russia, Ukraine
- `s-2651` 2026-10-05 08:05 (tick 2) [Kyiv Independent, en] [-] Kharkiv targeted in deadly Banderol strike as Russia kills 5, injures 61 across Ukraine over past day

---

### D112 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V024 (owner (agrees with draft)))
- **References:** IG V024
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D22 (3 items) · langs it
  actors: Sanchez · places: Paese, Spagna
- `s-2562` 2026-10-05 12:08 (tick 3) [Rai News Esteri, it] [D22] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa

**B** Developments D30 (6 items) · langs en
  actors: Pedro Sanchez, Sanchez, Spain · places: Spain
- `s-2397` 2026-10-05 10:18 (tick 2) [BBC World, en] [D30] Spanish PM Sánchez calls early election after housing protests

---

### D113 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V026 (owner (agrees with draft)))
- **References:** IG V026
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs en
  actors: - · places: Pakistan, Saudi Arabia, Turkiye
- `s-3339` 2026-10-05 20:17 (tick 3) [Al Jazeera, en] [-] Turkiye, Pakistan agree to military deployment to Saudi Arabia

**B** Developments none (not surfaced) · langs es
  actors: - · places: Arabia Saudita, Bab el Mandeb, Gobierno de Yemen, Pakistan, Turquía
- `s-3548` 2026-10-05 22:41 (tick 3) [France 24 Español, es] [-] Arabia Saudita, Turquía y Pakistán activan su alianza militar: ¿qué implica ante la amenaza hutí?

---

### D114 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V033 (owner (agrees with draft)))
- **References:** IG V033
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs en
  actors: - · places: Britain, France, UK, US
- `s-2545` 2026-10-05 13:00 (tick 3) [France 24, en] [-] US bombers leave UK air base amid 'new threats': What we know so far

**B** Developments none (not surfaced) · langs es
  actors: - · places: Fairford
- `s-2623` 2026-10-05 07:42 (tick 2) [El País Internacional, es] [-] El Pentágono retira sus bombarderos de la base británica de Fairford tras el presunto intento de atentado

---

### D115 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V045 (owner (agrees with draft)))
- **References:** IG V045
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D17 (10 items) · langs en
  actors: Donald Trump, Trump, US · places: Iran, UK, US
- `s-2553` 2026-10-05 09:49 (tick 2) [France 24, en] [D17] US withdraws all bombers from UK base at centre of suspected terror attack

**B** Developments none (not surfaced) · langs es
  actors: - · places: Estados Unidos, Londres, Reino Unido, Teherán
- `s-2639` 2026-10-04 22:24 (tick 1) [Clarín Mundo, es] [-] Estados Unidos retiró sus bombarderos de una base del Reino Unido tras descubrir un plan de atentado

---

### D116 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V051 (owner (agrees with draft)))
- **References:** IG V051
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments none (not surfaced) · langs it
  actors: - · places: Irkutsk, Russia, Siberia
- `s-2598` 2026-10-05 09:57 (tick 2) [Il Sole 24 Ore Mondo, it] [-] Russia, donna morta in Siberia per peste: in 200 sotto osservazione

**B** Developments none (not surfaced) · langs es
  actors: - · places: Europa, Irkutsk, Rusia, Siberia
- `s-2582` 2026-10-05 12:46 (tick 3) [France 24 Español, es] [-] ¿Peste pulmonar en Siberia? Europa sigue el caso mientras Rusia pide calma

---

### D117 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V054 (owner (agrees with draft)))
- **References:** IG V054
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D17 (10 items) · langs en
  actors: Donald Trump, Trump, US · places: UK, US
- `s-2314` 2026-10-05 04:58 (tick 2) [BBC World, en] [D17] US air force removes all bombers from British military base RAF Fairford

**B** Developments none (not surfaced) · langs es
  actors: - · places: Fairford
- `s-2623` 2026-10-05 07:42 (tick 2) [El País Internacional, es] [-] El Pentágono retira sus bombarderos de la base británica de Fairford tras el presunto intento de atentado

---

### D118 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 V056 (owner (agrees with draft)))
- **References:** IG V056
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)

**A** Developments D29 (3 items) · langs en
  actors: Donald Trump, Trump · places: France, US
- `s-2551` 2026-10-05 10:09 (tick 2) [France 24, en] [D29] Trump names Jay Clayton as AI czar to lead 'Super Intelligence Force'

**B** Developments none (not surfaced) · langs it
  actors: - · places: Pechino
- `s-2605` 2026-10-04 14:08 (tick 1) [Il Sole 24 Ore Mondo, it] [-] Trump affida l’IA al capo dei Servizi: Clayton nuovo «zar» della Super Intelligence

---

### D119 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (targeted batch P123: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT P123
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D18 (12 items) · langs es
  actors: Pedro Sanchez · places: Barcelona, España, Europa, Francia, Gobierno, Madrid, Palacio de La Moncloa
- `s-2468` 2026-10-03 17:24 (tick 1) [BBC Mundo, es] [D18] En fotos: las multitudinarias protestas en España contra la crisis de la vivienda
- `s-2630` 2026-10-05 07:18 (tick 2) [Clarín Mundo, es] [D18] Pedro Sánchez adelantó las elecciones generales en España para el 29 de noviembre
- `s-2590` 2026-10-05 08:54 (tick 2) [France 24 Español, es] [D18] Pedro Sánchez anuncia elecciones anticipadas en España para el 29 de noviembre
- `s-2589` 2026-10-05 10:09 (tick 2) [France 24 Español, es] [D18] Pedro Sánchez adelanta las elecciones en España al 29 de noviembre tras el revés parlamentario por la vivienda
- `s-2588` 2026-10-05 10:50 (tick 2) [France 24 Español, es] [D18] “Necesitamos una mayoría más amplia”: España adelanta las elecciones al 29 de noviembre
- `s-2587` 2026-10-05 10:54 (tick 2) [France 24 Español, es] [D18] Informe desde Barcelona: Pedro Sánchez convoca elecciones anticipadas en España
- `s-2456` 2026-10-05 12:31 (tick 3) [BBC Mundo, es] [D18] Pedro Sánchez convoca elecciones anticipadas tras el fracaso en el Congreso de sus decretos para enfrentar la crisis de la vivienda en España
- `s-2995` 2026-10-05 14:39 (tick 3) [France 24 Español, es] [D18] Ruth Forero:"La intención de Pedro Sánchez es aprovechar la movilización en las calles"
- `s-3168` 2026-10-05 19:00 (tick 3) [France 24 Español, es] [D18] La derecha celebra, la izquierda se organiza: así reacciona la política en España al adelanto electoral
- `s-3454` 2026-10-05 21:00 (tick 3) [Clarín Mundo, es] [D18] La sombra de la extrema derecha sobre Europa: de las presidenciales en Francia al adelantamiento electoral en España
- `s-3452` 2026-10-05 21:40 (tick 3) [BBC Mundo, es] [D18] Por qué Pedro Sánchez decidió convocar elecciones anticipadas en España ahora
- `s-3486` 2026-10-05 22:03 (tick 3) [France 24 Español, es] [D18] Directo a... Madrid y el adelanto de las elecciones en España en medio de la crisis de vivienda

**B** Developments D22 (3 items) · langs it
  actors: Sanchez · places: Madrid, Paese, Spagna, Valencia
- `s-2574` 2026-10-04 12:33 (tick 1) [Rai News Esteri, it] [D22] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
- `s-2451` 2026-10-05 07:29 (tick 2) [ANSA Mondo, it] [D22] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
- `s-2562` 2026-10-05 12:08 (tick 3) [Rai News Esteri, it] [D22] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa

---

### D120 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (runtime benchmark U001: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT U001
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D22 (3 items) · langs it
  actors: Sanchez · places: Madrid, Paese, Spagna, Valencia
- `s-2574` 2026-10-04 12:33 (tick 1) [Rai News Esteri, it] [D22] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
- `s-2451` 2026-10-05 07:29 (tick 2) [ANSA Mondo, it] [D22] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
- `s-2562` 2026-10-05 12:08 (tick 3) [Rai News Esteri, it] [D22] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa

**B** Developments D30 (6 items) · langs en
  actors: Pedro Sanchez, Sanchez, Spain · places: France, Madrid, Spain
- `s-2349` 2026-10-05 07:14 (tick 2) [Al Jazeera, en] [D30] Spanish Prime Minister Pedro Sanchez announces snap election
- `s-2357` 2026-10-05 08:04 (tick 2) [South China Morning Post, en] [D30] Spain’s prime minister calls early election as housing becomes national flashpoint
- `s-2397` 2026-10-05 10:18 (tick 2) [BBC World, en] [D30] Spanish PM Sánchez calls early election after housing protests
- `s-3079` 2026-10-05 17:27 (tick 3) [Al Jazeera, en] [D30] Spain calls snap election amid housing crisis
- `s-3251` 2026-10-05 19:30 (tick 3) [BBC World, en] [D30] Spain PM pins hopes on housing crisis to help win snap election
- `s-3253` 2026-10-05 19:31 (tick 3) [France 24, en] [D30] Sanchez chose 'best moment in a sea of troubles' to call for snap election, analyst says

---

### D121 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (runtime benchmark U116: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT U116
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D3 (56 items) · langs es, it
  actors: Bolsonaro, Flavio Bolsonaro, Partido Liberal de Bolsonaro · places: Además, América Latina, Argentina, Bolsa Familia, Brasil, Brasile, Brasilia, Bruselas, Distrito Federal, EE.UU., El Salvador, Estados Unidos
- `s-2626` 2026-10-04 03:30 (tick 1) [El País Internacional, es] [D3] Ni Bolsonaro, ni Lula: Trump se reserva (de momento) su apoyo en las elecciones de Brasil
- `s-2616` 2026-10-04 04:00 (tick 1) [El País Internacional, es] [D3] La disputa entre Lula y Trump marca las elecciones brasileñas
- `s-2576` 2026-10-04 11:20 (tick 1) [Rai News Esteri, it] [D3] Urne aperte in Brasile per le elezioni presidenziali e legislative, sfida Lula-Bolsonaro
- `s-2625` 2026-10-04 20:19 (tick 1) [El País Internacional, es] [D3] Brasil decide su futuro entre Lula y Bolsonaro, un estadista desgastado y el hijo de un ultra
- `s-2426` 2026-10-04 20:43 (tick 1) [Europa Press Internacional, es] [D3] Bolsonaro gana la primera vuelta en Brasil con el 47% de los votos y disputará contra Lula (45%) la segunda vuelta
- `s-2455` 2026-10-04 22:25 (tick 1) [ANSA Mondo, it] [D3] Media, Lula e Bolsonaro andranno al ballottaggio il 25 ottobre
- `s-2638` 2026-10-04 23:00 (tick 1) [Clarín Mundo, es] [D3] Los Bolsonaro amplían su presencia en el Congreso con las elecciones en Brasil: entran la esposa del ex presidente y dos hermanos de Flavio
- `s-2637` 2026-10-04 23:23 (tick 1) [Clarín Mundo, es] [D3] Elecciones en Brasil: Flávio Bolsonaro, un presidenciable a la sombra de su padre
- `s-2636` 2026-10-04 23:23 (tick 1) [Clarín Mundo, es] [D3] Lula da Silva busca su reelección en Brasil: entre el freno a la ultraderecha y la defensa de su legado social
- `s-2566` 2026-10-05 00:09 (tick 2) [Rai News Esteri, it] [D3] Il sorpasso di Bolsonaro, la crisi di Lula
- `s-2634` 2026-10-05 00:12 (tick 2) [Clarín Mundo, es] [D3] Elecciones en Brasil: un voto castigo que sorprendió a Lula da Silva y llegó desde su base tradicional de votantes
- `s-2632` 2026-10-05 01:03 (tick 2) [Clarín Mundo, es] [D3] Lula acepta el impacto del triunfo de Bolsonaro: fue "un resultado inesperado"
- `s-2631` 2026-10-05 01:08 (tick 2) [Clarín Mundo, es] [D3] Flavio Bolsonaro, tras ganar en primera vuelta ante Lula: "Brasil quiere un cambio"
- `s-2614` 2026-10-05 01:41 (tick 2) [El País Internacional, es] [D3] Arrasadora victoria de la derecha en Brasil
- `s-2427` 2026-10-05 02:13 (tick 2) [Europa Press Internacional, es] [D3] Bolsonaro proclama "fin de la era del PT" y Lula apela a combatir su "pasado tenebroso" en la segunda vuelta en Brasil
- `s-2613` 2026-10-05 02:28 (tick 2) [El País Internacional, es] [D3] El apellido Bolsonaro gana desde la cárcel
- `s-2457` 2026-10-05 02:39 (tick 2) [BBC Mundo, es] [D3] Cómo se compara Flávio Bolsonaro con su padre Jair y cuánto cambia el duelo con Lula por la presidencia de Brasil 4 años después
- `s-2597` 2026-10-05 02:46 (tick 2) [France 24 Español, es] [D3] Simone Pitta: "Con esta primera vuelta se puede ver una consolidación del bolsonarismo en Brasil"
- `s-2596` 2026-10-05 02:47 (tick 2) [France 24 Español, es] [D3] Juan Agulló: "A diferencia de otros países de Latinoamérica, Brasil es un competidor directo"
- `s-2612` 2026-10-05 02:54 (tick 2) [El País Internacional, es] [D3] Bolsonaro vence a Lula en primera vuelta de las elecciones y acaricia el retorno de la ultraderecha al poder en Brasil
- `s-2592` 2026-10-05 03:19 (tick 2) [France 24 Español, es] [D3] Brasil: la derecha de Bolsonaro se fortalece en las regiones, con un triunfo holgado en São Paulo
- `s-2621` 2026-10-05 03:36 (tick 2) [El País Internacional, es] [D3] Las claves de la primera vuelta en Brasil: de la fuerza ultra al día después de Lula con América Latina pendiente
- `s-2591` 2026-10-05 03:41 (tick 2) [France 24 Español, es] [D3] Flávio Bolsonaro tritura las encuestas: una ventaja pequeña, pero un escenario cuesta arriba para Lula
- `s-2629` 2026-10-05 04:08 (tick 2) [El País Internacional, es] [D3] Videoanálisis | Lula se enfrenta a una segunda vuelta electoral muy complicada
- `s-2565` 2026-10-05 04:33 (tick 2) [Rai News Esteri, it] [D3] Brasile, avanzata del clan Bolsonaro: quattro eletti in Parlamento, Flavio al ballottaggio con Lula
- `s-2604` 2026-10-05 05:14 (tick 2) [Il Sole 24 Ore Mondo, it] [D3] Brasile, Bolsonaro vince al primo turno con 47%, Lula al 45%: ballottaggio il 25 ottobre
- `s-2429` 2026-10-05 05:31 (tick 2) [Europa Press Internacional, es] [D3] Trump tacha de "corruptas" las elecciones de EEUU comparándolas con las de Brasil tras la victoria de Bolsonaro
- `s-2428` 2026-10-05 05:46 (tick 2) [Europa Press Internacional, es] [D3] Milei felicita a su "querido amigo" Flávio Bolsonaro por su "histórica elección" frente a Lula en Brasil
- `s-2452` 2026-10-05 06:44 (tick 2) [ANSA Mondo, it] [D3] Brasile, l'ex giudice che condannò Lula eletto governatore
- `s-2461` 2026-10-05 07:14 (tick 2) [BBC Mundo, es] [D3] Elecciones en Brasil: Flávio Bolsonaro y Lula da Silva van a una segunda vuelta en la que el presidente enfrenta una difícil remontada
- `s-2449` 2026-10-05 07:46 (tick 2) [ANSA Mondo, it] [D3] In Brasile un 30enne di destra è il deputato più votato della storia
- `s-2444` 2026-10-05 10:46 (tick 2) [ANSA Mondo, it] [D3] Astensione record in Brasile, il 21,08% non ha votato al primo turno
- `s-2585` 2026-10-05 11:42 (tick 2) [France 24 Español, es] [D3] Brasil irá a segunda vuelta: Flávio Bolsonaro lidera la primera ronda
- `s-2561` 2026-10-05 12:20 (tick 3) [Rai News Esteri, it] [D3] Il primo turno delle presidenziali in Brasile, avanti Bolsonaro: ribaltati i pronostici pro-Lula
- `s-2575` 2026-10-05 12:21 (tick 3) [Rai News Esteri, it] [D3] Presidenziali in Brasile, Flavio Bolsonaro a sorpresa supera Lula di 2 punti. Si va al ballottaggio
- `s-2933` 2026-10-05 12:29 (tick 3) [Clarín Mundo, es] [D3] Elecciones en Brasil 2026, EN VIVO: reacciones tras la victoria de Flávio Bolsonaro sobre Lula y últimas noticias del balotaje
- `s-2932` 2026-10-05 12:31 (tick 3) [Clarín Mundo, es] [D3] Quién es Flávio Bolsonaro, el hijo de Jair que sorprendió a Lula y va por la presidencia de Brasil
- `s-2581` 2026-10-05 13:05 (tick 3) [France 24 Español, es] [D3] Informe desde Río de Janeiro: el Partido Liberal de Bolsonaro se fortalece en el Senado
- `s-2998` 2026-10-05 13:16 (tick 3) [Clarín Mundo, es] [D3] Elecciones en Brasil: los mercados celebran la ventaja de Flávio Bolsonaro sobre Lula y el principal índice de la Bolsa marca un nuevo récord
- `s-2923` 2026-10-05 13:57 (tick 3) [BBC Mundo, es] [D3] Quiénes son Lucas Pavanato y Nikolas Ferreira, los jóvenes influencers de derecha que lograron las mayores votaciones en la historia de la Cámara de D
- `s-3098` 2026-10-05 14:50 (tick 3) [Clarín Mundo, es] [D3] Elecciones en Brasil: los resultados del domingo cambian por completo el diseño del país y ya asoma una amnistía para Jair Bolsonaro
- `s-3096` 2026-10-05 15:47 (tick 3) [Clarín Mundo, es] [D3] La reacción de los medios en Brasil tras la victoria de Bolsonaro: desde "el ciclo de Lula está terminado" hasta "el tsunami de lo peor de la derecha"
- `s-3076` 2026-10-05 15:59 (tick 3) [France 24 Español, es] [D3] Flávio Bolsonaro y Lula da Silva se preparan para el balotaje en Brasil
- `s-3091` 2026-10-05 16:02 (tick 3) [El País Internacional, es] [D3] El lulismo cruje ante la ofensiva ultra
- `s-3075` 2026-10-05 16:10 (tick 3) [France 24 Español, es] [D3] "Solo faltan días para el rescate Brasil": Bolsonaro celebra la victoria sobre Lula
- `s-3095` 2026-10-05 16:23 (tick 3) [Clarín Mundo, es] [D3] Elecciones en Brasil: a contrarreloj, Lula y el PT analizan cambios totales en la estrategia de campaña
- `s-3074` 2026-10-05 16:36 (tick 3) [France 24 Español, es] [D3] Paraguay, refugio fiscal y político para la extrema derecha brasileña
- `s-3060` 2026-10-05 17:02 (tick 3) [ANSA Mondo, it] [D3] Brasile, Erika Hilton è la donna più votata della storia alla Camera
- `s-3149` 2026-10-05 17:30 (tick 3) [Clarín Mundo, es] [D3] El fantasma de Bolsonaro reaparece en Europa: los temores de Bruselas ante un eventual cambio de gobierno en Brasil
- `s-3121` 2026-10-05 18:04 (tick 3) [France 24 Español, es] [D3] El mercado de valores de Brasil aplaude la ventaja de Bolsonaro en primera vuelta presidencial
- `s-3120` 2026-10-05 18:10 (tick 3) [France 24 Español, es] [D3] La dinastía Bolsonaro se fortalece: prensa brasileña sobre la primera vuelta electoral
- `s-3254` 2026-10-05 19:41 (tick 3) [El País Internacional, es] [D3] La ola conservadora de América Latina llega a Brasil
- `s-3294` 2026-10-05 19:42 (tick 3) [El País Internacional, es] [D3] La victoria en primera vuelta de Bolsonaro impulsa a la ola ultra de América Latina
- `s-3354` 2026-10-05 19:47 (tick 3) [Clarín Mundo, es] [D3] Elecciones en Brasil: las urnas de la sorpresa
- `s-3321` 2026-10-05 20:21 (tick 3) [ANSA Mondo, it] [D3] Trump, il risultato di Bolsonaro in Brasile una 'grande vittoria'
- `s-3485` 2026-10-05 22:09 (tick 3) [ANSA Mondo, it] [D3] Brasile, l'ex presidente Temer sostiene Bolsonaro al ballottaggio

**B** Developments D5 (14 items) · langs en
  actors: Bolsonaro, Brazil, Flavio Bolsonaro · places: Bolsonaro Close, Brazil, China, France, South America, US
- `s-2196` 2026-10-04 11:15 (tick 1) [Al Jazeera, en] [D5] Brazil votes in deeply polarised election pitting Lula against Bolsonaro
- `s-2246` 2026-10-04 17:48 (tick 1) [South China Morning Post, en] [D5] Brazilians head to polls in high-stakes, polarised election
- `s-2275` 2026-10-04 21:11 (tick 1) [BBC World, en] [D5] Polls close in Brazil as Lula and Flávio Bolsonaro remain neck and neck
- `s-2533` 2026-10-05 00:27 (tick 2) [DW World, en] [D5] Brazil election: Bolsonaro and Lula head to runoff
- `s-2857` 2026-10-05 03:16 (tick 2) [BBC World, en] [D5] Right-wing Flávio Bolsonaro wins first round of Brazil election
- `s-2315` 2026-10-05 04:51 (tick 2) [BBC World, en] [D5] Watch: How Brazil's dramatic election unfolded
- `s-2297` 2026-10-05 05:08 (tick 2) [Al Jazeera, en] [D5] Bolsonaro beats expectations in Brazil vote, faces Lula in runoff
- `s-2557` 2026-10-05 09:38 (tick 2) [France 24, en] [D5] Brazil heads to run-off as Bolsonaro pulls off shock first place finish in first round
- `s-2376` 2026-10-05 09:46 (tick 2) [South China Morning Post, en] [D5] Brazil-China ties in focus as Bolsonaro gets election edge over Lula
- `s-2420` 2026-10-05 12:34 (tick 3) [Al Jazeera, en] [D5] Bolsonaro favourite to win: What Brazil’s first round of elections tells us
- `s-2548` 2026-10-05 12:52 (tick 3) [France 24, en] [D5] Brazil presidential election: 'Bolsonaro being ahead is a surprise,' researcher says
- `s-2547` 2026-10-05 12:54 (tick 3) [France 24, en] [D5] 'Very bad result for Lula: Bolsonaro is far more effective at speaking to that growing middle class'
- `s-3421` 2026-10-05 20:37 (tick 3) [France 24, en] [D5] Concerns of US interference weigh on Brazil vote
- `s-3397` 2026-10-05 21:00 (tick 3) [Al Jazeera, en] [D5] Brazil’s presidential race head for a tough runoff

---

### D122 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (runtime benchmark U124: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT U124
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D27 (5 items) · langs es
  actors: EE.UU., Moscú, Rusia · places: EE.UU., Estado, Irkutsk, Moscú, Rusia, Shelejov, Siberia, Yaroslavsky
- `s-2635` 2026-10-04 23:23 (tick 1) [Clarín Mundo, es] [D27] Alerta en Rusia: murió una científica por un accidente con bacterias en un laboratorio y debieron aislar a 200 personas
- `s-2432` 2026-10-05 06:53 (tick 2) [Europa Press Internacional, es] [D27] Rusia asegura que la situación epidemiológica en Irkutsk es "estable" tras un supuesto accidente en un laboratorio
- `s-2618` 2026-10-05 10:17 (tick 2) [El País Internacional, es] [D27] Rusia pone bajo observación a cientos de personas tras morir una investigadora de un laboratorio contra la peste
- `s-2964` 2026-10-05 14:34 (tick 3) [Europa Press Internacional, es] [D27] EEUU pide a Rusia compartir información "de forma rápida y transparente" tras supuesto caso de peste en Irkutsk
- `s-3416` 2026-10-05 21:21 (tick 3) [BBC Mundo, es] [D27] EE.UU. "sigue de cerca" el caso de una científica rusa que falleció en un centro de investigación de la peste en Siberia

**B** Developments D40 (5 items) · langs en
  actors: Moscow, Russia, US, Washington · places: France, Irkutsk, Moscow, Russia, Siberia, Siberia Russian, US, Washington
- `s-2299` 2026-10-05 04:07 (tick 2) [Al Jazeera, en] [D40] Russian lab worker dies of suspected plague in Siberia; US monitoring case
- `s-3088` 2026-10-05 17:14 (tick 3) [South China Morning Post, en] [D40] After plague death reports at Siberia lab, Russia says situation under control
- `s-3206` 2026-10-05 19:19 (tick 3) [France 24, en] [D40] Russian officials say 'situation under control' after plague reports
- `s-3290` 2026-10-05 19:55 (tick 3) [BBC World, en] [D40] US 'watching closely' after plague researcher dies in Russia, Rubio says
- `s-3396` 2026-10-05 21:03 (tick 3) [Al Jazeera, en] [D40] Trump says US ready to aid Russia with plague outbreak in Siberia

---

### D124 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (runtime benchmark U151: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT U151
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D18 (12 items) · langs es
  actors: Pedro Sanchez · places: Barcelona, España, Europa, Francia, Gobierno, Madrid, Palacio de La Moncloa
- `s-2468` 2026-10-03 17:24 (tick 1) [BBC Mundo, es] [D18] En fotos: las multitudinarias protestas en España contra la crisis de la vivienda
- `s-2630` 2026-10-05 07:18 (tick 2) [Clarín Mundo, es] [D18] Pedro Sánchez adelantó las elecciones generales en España para el 29 de noviembre
- `s-2590` 2026-10-05 08:54 (tick 2) [France 24 Español, es] [D18] Pedro Sánchez anuncia elecciones anticipadas en España para el 29 de noviembre
- `s-2589` 2026-10-05 10:09 (tick 2) [France 24 Español, es] [D18] Pedro Sánchez adelanta las elecciones en España al 29 de noviembre tras el revés parlamentario por la vivienda
- `s-2588` 2026-10-05 10:50 (tick 2) [France 24 Español, es] [D18] “Necesitamos una mayoría más amplia”: España adelanta las elecciones al 29 de noviembre
- `s-2587` 2026-10-05 10:54 (tick 2) [France 24 Español, es] [D18] Informe desde Barcelona: Pedro Sánchez convoca elecciones anticipadas en España
- `s-2456` 2026-10-05 12:31 (tick 3) [BBC Mundo, es] [D18] Pedro Sánchez convoca elecciones anticipadas tras el fracaso en el Congreso de sus decretos para enfrentar la crisis de la vivienda en España
- `s-2995` 2026-10-05 14:39 (tick 3) [France 24 Español, es] [D18] Ruth Forero:"La intención de Pedro Sánchez es aprovechar la movilización en las calles"
- `s-3168` 2026-10-05 19:00 (tick 3) [France 24 Español, es] [D18] La derecha celebra, la izquierda se organiza: así reacciona la política en España al adelanto electoral
- `s-3454` 2026-10-05 21:00 (tick 3) [Clarín Mundo, es] [D18] La sombra de la extrema derecha sobre Europa: de las presidenciales en Francia al adelantamiento electoral en España
- `s-3452` 2026-10-05 21:40 (tick 3) [BBC Mundo, es] [D18] Por qué Pedro Sánchez decidió convocar elecciones anticipadas en España ahora
- `s-3486` 2026-10-05 22:03 (tick 3) [France 24 Español, es] [D18] Directo a... Madrid y el adelanto de las elecciones en España en medio de la crisis de vivienda

**B** Developments D30 (6 items) · langs en
  actors: Pedro Sanchez, Sanchez, Spain · places: France, Madrid, Spain
- `s-2349` 2026-10-05 07:14 (tick 2) [Al Jazeera, en] [D30] Spanish Prime Minister Pedro Sanchez announces snap election
- `s-2357` 2026-10-05 08:04 (tick 2) [South China Morning Post, en] [D30] Spain’s prime minister calls early election as housing becomes national flashpoint
- `s-2397` 2026-10-05 10:18 (tick 2) [BBC World, en] [D30] Spanish PM Sánchez calls early election after housing protests
- `s-3079` 2026-10-05 17:27 (tick 3) [Al Jazeera, en] [D30] Spain calls snap election amid housing crisis
- `s-3251` 2026-10-05 19:30 (tick 3) [BBC World, en] [D30] Spain PM pins hopes on housing crisis to help win snap election
- `s-3253` 2026-10-05 19:31 (tick 3) [France 24, en] [D30] Sanchez chose 'best moment in a sea of troubles' to call for snap election, analyst says

---

### D125 · 2026-10-08-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (targeted batch P118: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT P118
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D12 (12 items) · langs es, it
  actors: - · places: Estado, Francia, Irán, Parigi, Paris, Plaza de la Bastilla, Teherán
- `s-6358` 2026-10-07 23:32 (tick 1) [Rai News Esteri, it] [D12] La protesta degli studenti blocca licei e università in Francia
- `s-6462` 2026-10-07 23:45 (tick 1) [Europa Press Internacional, es] [D12] Lecornu defiende la actuación policial ante los disturbios en Francia y promete diálogo ante las protestas estudiantiles
- `s-6392` 2026-10-08 02:27 (tick 1) [France 24 Español, es] [D12] Francia: Ejecutivo anuncia que mantendrá fuerza policial contra manifestaciones estudiantiles
- `s-6466` 2026-10-08 06:10 (tick 1) [France 24 Español, es] [D12] En directo: nuevas marchas estudiantiles en Francia entre promesas oficiales y denuncias de violencia policial
- `s-6903` 2026-10-08 11:36 (tick 1) [El País Internacional, es] [D12] Los estudiantes de Francia presentan 10 reivindicaciones para detener sus protestas
- `s-7242` 2026-10-08 14:44 (tick 2) [Clarín Mundo, es] [D12] "¡A tomar la Bastilla!": sindicatos, el campo y las universidades se unen a las barricadas estudiantiles en una cuarta movilización en Francia
- `s-7185` 2026-10-08 14:45 (tick 2) [Rai News Esteri, it] [D12] Proteste studentesche in Francia, l'abbraccio tra Mélenchon e il giovane Elwan diventa virale
- `s-7228` 2026-10-08 14:52 (tick 2) [Rai News Esteri, it] [D12] Chi è Elwan, simbolo delle proteste studentesche in Francia: 17 anni e milioni di visualizzazioni
- `s-7286` 2026-10-08 16:16 (tick 2) [BBC Mundo, es] [D12] Cuáles son los reclamos de los estudiantes que están participando en las violentas protestas que sacuden a Francia
- `s-7321` 2026-10-08 16:39 (tick 2) [France 24 Español, es] [D12] Directo París y el cuarto día de manifestaciones de estudiantes en Francia
- `s-7320` 2026-10-08 17:31 (tick 2) [France 24 Español, es] [D12] Por qué Irán ataca a Francia aprovechando las protestas estudiantiles
- `s-7376` 2026-10-08 18:20 (tick 2) [Rai News Esteri, it] [D12] Francia, si allarga la protesta della scuola: "Basta repressione"

**B** Developments D20 (11 items) · langs en
  actors: France · places: France, Paris
- `s-6381` 2026-10-08 03:28 (tick 1) [France 24, en] [D20] Live: French high school, university students call for fresh protests as funding demands grow
- `s-6336` 2026-10-08 03:38 (tick 1) [BBC World, en] [D20] France's school protests: What lies behind the anger
- `s-6707` 2026-10-08 06:27 (tick 1) [France 24, en] [D20] French students prepare for more marches as hundreds of schools close
- `s-6820` 2026-10-08 10:45 (tick 1) [South China Morning Post, en] [D20] French school blockades continue despite PM’s pledge to act
- `s-6867` 2026-10-08 11:03 (tick 1) [Al Jazeera, en] [D20] School protests, blockades resume in France despite PM’s promise to act
- `s-7041` 2026-10-08 12:48 (tick 2) [France 24, en] [D20] French teens keep up school blockades despite prime minister's pledge to act
- `s-7160` 2026-10-08 13:45 (tick 2) [Al Jazeera, en] [D20] French PM vows changes as students keep up school protests
- `s-7158` 2026-10-08 14:01 (tick 2) [Al Jazeera, en] [D20] ‘This is a crisis of hope’: Echoes of 1968 as France’s students rise up
- `s-7230` 2026-10-08 15:23 (tick 2) [France 24, en] [D20] Student protesters 'showing no signs of backing down'
- `s-7378` 2026-10-08 20:17 (tick 2) [France 24, en] [D20] 'Fighting for our future': France high school students vow no let-up
- `s-7377` 2026-10-08 20:22 (tick 2) [France 24, en] [D20] ‘Nothing will stop us’: French student protests show few signs of ending

---

### D126 · 2026-10-08-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (targeted batch P125: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT P125
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D5 (7 items) · langs es
  actors: - · places: Aeropuerto Internacional Rey Jalid de Riad, Aeropuerto Internacional Rey Khalid, Arabia Saudita, Arabia Saudí, Dhubab, EUROPA, Ejército de Yemen, Esmail Baqaei, Francia, Hutíes de Yemen, Irán, Mascate
- `s-6398` 2026-10-07 22:15 (tick 1) [France 24 Español, es] [D5] Francia convoca al embajador iraní por la "desinformación" sobre las protestas estudiantiles
- `s-6537` 2026-10-08 03:30 (tick 1) [El País Internacional, es] [D5] La guerra en Irán reactiva el conficto civil en Yemen tras cuatro años de tregua
- `s-6456` 2026-10-08 04:34 (tick 1) [Europa Press Internacional, es] [D5] Irán asegura haber acordado con Omán rutas marítimas seguras en el estrecho de Ormuz
- `s-6591` 2026-10-08 07:27 (tick 1) [France 24 Español, es] [D5] En Yemen, los hutíes se muestran tranquilos ante la contraofensiva respaldada por Riad
- `s-6956` 2026-10-08 12:05 (tick 2) [El País Internacional, es] [D5] Los hutíes de Yemen amenazan a las compañías aéreas para que dejen de volar a Arabia Saudí
- `s-7294` 2026-10-08 16:08 (tick 2) [Europa Press Internacional, es] [D5] Los rebeldes yemeníes atacan de nuevo el aeropuerto de Riad, en Arabia Saudí
- `s-7379` 2026-10-08 20:24 (tick 2) [France 24 Español, es] [D5] Hutíes de Yemen atacan aeropuertos de Arabia Saudita

**B** Developments D14 (10 items) · langs en
  actors: Houthis, Riyadh, Saudi Arabia, Yemen · places: France, Iran, King Khalid International Airport, Riyadh, Saudi Arabia, Yemen
- `s-6376` 2026-10-08 00:00 (tick 1) [Al Jazeera, en] [D14] Yemen war live: Gov’t forces claim key heights, Houthi attacks continue
- `s-6375` 2026-10-08 00:16 (tick 1) [Al Jazeera, en] [D14] Saudi Arabia confirms three dead in Houthi strikes on its airports
- `s-6371` 2026-10-08 01:02 (tick 1) [Al Jazeera, en] [D14] Yemeni government forces claim 1,860 Houthis ‘neutralised’
- `s-6419` 2026-10-08 01:54 (tick 1) [South China Morning Post, en] [D14] Houthi strikes on Saudi airports leave 3 dead, dozens wounded
- `s-6382` 2026-10-08 03:02 (tick 1) [France 24, en] [D14] Saudi Arabia says it will retaliate after deadly Houthi attacks on airports
- `s-6340` 2026-10-08 03:32 (tick 1) [BBC World, en] [D14] Three people killed in Houthi attacks on Saudi Arabia airports, officials say
- `s-6512` 2026-10-08 06:50 (tick 1) [Al Jazeera, en] [D14] Yemen’s government needs tribes to defeat the Houthis. Will they join?
- `s-6760` 2026-10-08 09:55 (tick 1) [France 24, en] [D14] Houthis claim new attack on Riyadh airport as fighting continues in Yemen
- `s-7039` 2026-10-08 12:52 (tick 2) [France 24, en] [D14] Conflict in Yemen: What are the Houthis’ aims?
- `s-7187` 2026-10-08 14:43 (tick 2) [Al Jazeera, en] [D14] Saudi-led coalition says it intercepts three Houthi ballistic missiles

---

### D128 · 2026-10-08-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (runtime benchmark U143: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT U143
- **Root cause (suspected):** English-only clustering embeddings; the cross-language stage is disabled (rejected 2026-10-09)
- **Blocks a Phase 3 endpoint:** distorts: one occurrence has a Development per language (duplicate endpoints)
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D8 (6 items) · langs es, it
  actors: Abascal, Maricarmen Abascal · places: Assemblea di Madrid, España, Madrid, Mas Madrid, Mobilitazione, San Blas
- `s-6401` 2026-10-07 22:41 (tick 1) [Clarín Mundo, es] [D8] La muerte de Maricarmen, la mártir de los inquilinos que reclaman por una vivienda digna y puso en jaque al gobierno de Sánchez
- `s-6389` 2026-10-08 03:07 (tick 1) [France 24 Español, es] [D8] Falleció Maricarmen Abascal, mujer desahuciada que se convirtió en símbolo de lucha por la vivienda
- `s-6644` 2026-10-08 08:38 (tick 1) [ANSA Mondo, it] [D8] La morte di Maricarmen Abascal, un minuto di silenzio fuori dall'Assemblea di Madrid
- `s-7001` 2026-10-08 11:22 (tick 1) [Rai News Esteri, it] [D8] La storia di Maricarmen: sfrattata a 87 anni e diventata il simbolo della protesta per la casa
- `s-7146` 2026-10-08 13:59 (tick 2) [Rai News Esteri, it] [D8] Madrid, fanno scudo a una famiglia con tre figli e fermano lo sfratto: "Tamara non sei sola"
- `s-7209` 2026-10-08 15:19 (tick 2) [Il Sole 24 Ore Mondo, it] [D8] Polizia britannica riconosce l’illegalità delle perquisizioni a casa di Andrea nel caso Epstein

**B** Developments D16 (5 items) · langs en
  actors: - · places: France, Madrid, Spain
- `s-6370` 2026-10-08 01:15 (tick 1) [Al Jazeera, en] [D16] Death of 87-year old sparks furious Spain housing protests
- `s-6759` 2026-10-08 09:56 (tick 1) [France 24, en] [D16] Anger mounts in Spain as woman whose eviction ignited housing protests dies
- `s-6844` 2026-10-08 10:35 (tick 1) [France 24, en] [D16] Evicted pensioner Maricarmen, symbol of Spain's housing crisis, dies at 87
- `s-6869` 2026-10-08 10:48 (tick 1) [Al Jazeera, en] [D16] Photos: Protests erupt after 87-year-old evicted woman dies in Madrid
- `s-6932` 2026-10-08 11:54 (tick 1) [France 24, en] [D16] Maricarmen, the 87-year-old woman whose eviction shook Spain, dies

---

## SPLIT (2)

### D123 · 2026-10-05-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (runtime benchmark U131: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT U131
- **Root cause (suspected):** two same-language clusters not linked (below the link threshold or cut by segmentation)
- **Blocks a Phase 3 endpoint:** distorts: duplicate endpoints for one occurrence
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D19 (7 items) · langs it
  actors: Sanchez, Spagna · places: Barcellona, Centinaia, El Pais, Europa, Francia, Madrid, Spagna, Valencia
- `s-2579` 2026-10-03 23:35 (tick 1) [Rai News Esteri, it] [D19] Marea sociale contro il caro-affitti in Spagna: le piazze spingono Sánchez verso le urne
- `s-2568` 2026-10-04 17:28 (tick 1) [Rai News Esteri, it] [D19] Casa e scuola: il filo rosso che lega le proteste in Europa
- `s-2567` 2026-10-04 23:15 (tick 1) [Rai News Esteri, it] [D19] La Spagna in piazza per il diritto alla casa. E Sanchez pensa al voto anticipato
- `s-2601` 2026-10-05 06:21 (tick 2) [Il Sole 24 Ore Mondo, it] [D19] Caro casa, prezzi e affitti salgono nell’Ue. Il Governo studia le misure per giovani e locazioni
- `s-2563` 2026-10-05 10:27 (tick 2) [Rai News Esteri, it] [D19] La Spagna al voto: i sondaggi premiano le destre, l'area progressista frammentata
- `s-3187` 2026-10-05 19:05 (tick 3) [Il Sole 24 Ore Mondo, it] [D19] Sanchez sfida le destre: Spagna al voto anticipato
- `s-3467` 2026-10-05 21:04 (tick 3) [Rai News Esteri, it] [D19] Migliaia di persone a Barcellona in piazza per il diritto alla casa

**B** Developments D22 (3 items) · langs it
  actors: Sanchez · places: Madrid, Paese, Spagna, Valencia
- `s-2574` 2026-10-04 12:33 (tick 1) [Rai News Esteri, it] [D22] Spagna, il Psoe in pressing su Sanchez per il voto anticipato. La destra soffia sulle piazze
- `s-2451` 2026-10-05 07:29 (tick 2) [ANSA Mondo, it] [D22] Sanchez, 'ho deciso di convocare le elezioni il 29 novembre'
- `s-2562` 2026-10-05 12:08 (tick 3) [Rai News Esteri, it] [D22] Sanchez porta la Spagna al voto il 29 novembre sull'onda delle proteste per la crisi abitativa

---

### D127 · 2026-10-08-live

- **Expected:** SAME_DEVELOPMENT (owner verdict 2026-10-09 (runtime benchmark U110: SAME_DEVELOPMENT_SUSPECTED))
- **References:** RT U110
- **Root cause (suspected):** two same-language clusters not linked (below the link threshold or cut by segmentation)
- **Blocks a Phase 3 endpoint:** distorts: duplicate endpoints for one occurrence
- **Notes:** both sides are system Developments the owner judged one occurrence

**A** Developments D33 (6 items) · langs es
  actors: Cilia Flores, EE. UU., EEUU, Flores, Maduro, Nicolás Maduro · places: Caracas, EE UU, EE. UU., EEUU, Nueva York, Venezuela
- `s-6460` 2026-10-08 00:56 (tick 1) [Europa Press Internacional, es] [D33] Maduro y Flores podrían ser acusados este jueves de haber torturado a estadounidenses venezolanos
- `s-7241` 2026-10-08 14:52 (tick 2) [Clarín Mundo, es] [D33] Torturas: Estados Unidos suma una nueva acusación contra Nicolás Maduro
- `s-7206` 2026-10-08 15:13 (tick 2) [France 24 Español, es] [D33] EE. UU. suma a Maduro y Cilia Flores un cargo por conspiración para torturar a opositores
- `s-7266` 2026-10-08 15:20 (tick 2) [El País Internacional, es] [D33] Nicolás Maduro y Cilia Flores, acusados en EE UU de nuevos cargos de tortura y represión
- `s-7223` 2026-10-08 15:21 (tick 2) [BBC Mundo, es] [D33] Presentan nuevos cargos contra Maduro y su esposa por presuntas torturas a ciudadanos de estadounidenses ante un tribunal de Nueva York
- `s-7258` 2026-10-08 15:32 (tick 2) [Europa Press Internacional, es] [D33] EEUU imputa a Maduro y su esposa por liderar un sistema de represión y torturas en Venezuela

**B** Developments D17 (3 items) · langs es, it
  actors: Partido Socialista Unido de Venezuela · places: Estados Unidos, Lesotho, Roma, Venezuela
- `s-6461` 2026-10-08 01:15 (tick 1) [Europa Press Internacional, es] [D17] Diosdado Cabello llama a cerrar filas con Delcy Rodríguez y reta a la oposición a medirse en las urnas
- `s-6349` 2026-10-08 01:22 (tick 1) [ANSA Mondo, it] [D17] Venezuela, Delcy Rodríguez al Forum mondiale dell'alimentazione a Roma
- `s-7154` 2026-10-08 14:28 (tick 2) [France 24 Español, es] [D17] Estados Unidos presenta nuevos cargos contra Maduro y Cilia Flores por presuntas torturas a estadounidenses

---

## SAME_LANGUAGE_RECALL_MISS (17)

### D014 · 2026-09-25

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 B002 (owner (agrees with draft)))
- **References:** IG B002
- **Root cause (suspected):** same-tick items of one occurrence not grouped (below the link threshold or left as noise)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** same_occurrence

**A** Developments none (not surfaced) · langs en
  actors: - · places: Italy
- `b-5d1ba8e525da` 2026-09-24T18:03 (tick 3) [Breaking Defense, en] [-] OCCAR awards $4.2B DDX destroyer contract to Fincantieri, Leonardo joint venture

**B** Developments none (not surfaced) · langs en
  actors: - · places: Italy, ROME
- `b-d72e5f6a5e01` 2026-09-24T16:33 (tick 3) [Defense News, en] [-] Italy taps state-owned firms to build two naval destroyers in $4.2 billion deal

---

### D015 · 2026-09-25

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 B004 (owner (agrees with draft)))
- **References:** IG B004
- **Root cause (suspected):** same-tick items of one occurrence not grouped (below the link threshold or left as noise)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** same_occurrence

**A** Developments none (not surfaced) · langs en
  actors: - · places: -
- `b-63cb0d4f2400` 2026-09-25T08:09 (tick 4) [BBC World, en] [-] Trump and Xi exchange warm words at state dinner but little progress on key issues

**B** Developments none (not surfaced) · langs en
  actors: - · places: China, East Room, United States
- `b-9796005bb46b` 2026-09-25T05:48 (tick 4) [South China Morning Post, en] [-] From wine to ping-pong, Trump and Xi’s state dinner is heavy on historic symbolism

---

### D016 · 2026-09-25

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 B007 (owner (agrees with draft)))
- **References:** IG B007
- **Root cause (suspected):** segmentation cut the link between them (guard: headline_similarity)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** same_occurrence

**A** Developments none (not surfaced) · langs en
  actors: - · places: China
- `b-6e3eb47c7f66` 2026-09-24T15:56 (tick 3) [Breaking Defense, en] [-] The Air Force says its China think tank will continue. Its director says it’s basically dead.

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `b-aa291f31d75e` 2026-09-23T15:38 (tick 1) [Defense News, en] [-] Air Force, civilian staff dispute status of China Aerospace Studies Institute

---

### D049 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C005 (owner (corrected draft)))
- **References:** IG C005
- **Root cause (suspected):** the later item did not join the earlier item's Development (or neither was clustered)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** same_occurrence

**A** Developments none (not surfaced) · langs en
  actors: - · places: New York
- `sx-421` 2026-09-29 16:41 (tick 3) [UN Press, en] [-] At ‘Most Dangerous Nuclear Moment’ Since Cold War Ended, Secretary-General Observance Message Urges Changing Course, Replacing Threats with Dialogue

**B** Developments none (not surfaced) · langs en
  actors: - · places: Middle East
- `sx-424` 2026-09-28 23:02 (tick 1) [UN Press, en] [-] International Security Rapidly Deteriorates; General Assembly Urges Nations to Address Weaker Global Arms Treaties and Heightened Nuclear Risks

---

### D053 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C013 (owner (agrees with draft)))
- **References:** IG C013
- **Root cause (suspected):** same-tick items of one occurrence not grouped (below the link threshold or left as noise)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)

**A** Developments none (not surfaced) · langs en
  actors: - · places: Kyiv, Russia, Ukraine
- `sx-275` 2026-09-30 08:14 (tick 4) [Kyiv Independent, en] [-] Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack

**B** Developments none (not surfaced) · langs en
  actors: - · places: Kyiv, Poland, Russia, Ukraine
- `sx-161` 2026-09-30 05:35 (tick 4) [France 24, en] [-] Live: Several people killed as Russia launches new round of strikes on Kyiv

---

### D057 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C034 (owner (corrected draft)))
- **References:** IG C034
- **Root cause (suspected):** one item is in a Development, the other was left out of it
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** should be bundled together, it's literally the accompanying Q&A ( and btw we should vet the questions asked as well and possibly come up with other ones to launch /attach onto other threads)

**A** Developments D1 (2 items) · langs en
  actors: - · places: Brussels, Europe
- `sx-352` 2026-09-29 22:00 (tick 3) [European Commission Press, en] [D1] Commission proposes a new EU Critical Communication System for first responders

**B** Developments none (not surfaced) · langs en
  actors: - · places: Brussels
- `sx-351` 2026-09-29 22:00 (tick 3) [European Commission Press, en] [-] Questions and answers on the European Union Critical Communication System

---

### D059 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C051 (owner (agrees with draft)))
- **References:** IG C051
- **Root cause (suspected):** segmentation cut the link between them (guard: headline_similarity)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)

**A** Developments none (not surfaced) · langs en
  actors: - · places: Congo, DRC, Democratic Republic, New York, Rwanda
- `sx-400` 2026-09-29 12:00 (tick 3) [UN News, en] [-] Security Council LIVE: DRC peace deals fail to halt fighting as Ebola deepens crisis

**B** Developments none (not surfaced) · langs en
  actors: - · places: Democratic Republic of Congo, Democratic Republic of the Congo
- `sx-416` 2026-09-29 21:52 (tick 3) [UN Press, en] [-] Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council

---

### D060 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C064 (owner (corrected draft)))
- **References:** IG C064
- **Root cause (suspected):** the later item did not join the earlier item's Development (or neither was clustered)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** basically same news, should bundle together and add to the development, before-after meeting only matters if there's a big dissonance between intentions/proposed aim of the meeting and the actual turnout (e.g. Zelensky - Trump live altercations along with JD Vance).

**A** Developments none (not surfaced) · langs en
  actors: - · places: Congo, Democratic Republic, Democratic Republic of the Congo, Haiti
- `sx-423` 2026-09-28 23:02 (tick 1) [UN Press, en] [-] Security Council, 10232nd Meeting (AM) Democratic Republic of the Congo/MONUSCO

**B** Developments none (not surfaced) · langs en
  actors: - · places: Democratic Republic of Congo, Democratic Republic of the Congo
- `sx-416` 2026-09-29 21:52 (tick 3) [UN Press, en] [-] Commitments Must Yield Tangible Progress in Democratic Republic of Congo, Special Representative Tells Security Council

---

### D061 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C066 (owner (agrees with draft)))
- **References:** IG C066
- **Root cause (suspected):** segmentation cut the link between them (guard: disjoint_locations)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)

**A** Developments D24 (6 items) · langs it
  actors: - · places: Tel Aviv
- `sx-122` 2026-09-30 07:58 (tick 4) [Rai News Esteri, it] [D24] Volo Flydubai, l'aereo diretto a Tel Aviv viene deviato in Arabia Saudita

**B** Developments none (not surfaced) · langs it
  actors: - · places: Oman
- `sx-39` 2026-09-30 09:27 (tick 4) [ANSA Mondo, it] [-] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino

---

### D063 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C076 (owner (corrected draft)))
- **References:** IG C076
- **Root cause (suspected):** same-tick items of one occurrence not grouped (below the link threshold or left as noise)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** same attack though, should be clustered

**A** Developments none (not surfaced) · langs en
  actors: - · places: Moldova, Russia, Ukraine, Ukraine Russia
- `sx-277` 2026-09-30 07:03 (tick 4) [Kyiv Independent, en] [-] Drone crashes in Moldova amid Russian mass attack on Ukraine

**B** Developments none (not surfaced) · langs en
  actors: - · places: Kyiv, Russia, Ukraine
- `sx-275` 2026-09-30 08:14 (tick 4) [Kyiv Independent, en] [-] Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv faces another overnight missile, drone attack

---

### D065 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C092 (owner (agrees with draft)))
- **References:** IG C092
- **Root cause (suspected):** segmentation cut the link between them (guard: disjoint_locations)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)

**A** Developments none (not surfaced) · langs it
  actors: - · places: Oman
- `sx-39` 2026-09-30 09:27 (tick 4) [ANSA Mondo, it] [-] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino

**B** Developments D24 (6 items) · langs it
  actors: - · places: Dubai, Pilota, Tel Aviv
- `sx-123` 2026-09-30 07:00 (tick 4) [Rai News Esteri, it] [D24] Volo FlyDubai, la ricostruzione di Tel Aviv: "Pilota ha cercato di far schiantare l'aereo"

---

### D067 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C096 (owner (agrees with draft)))
- **References:** IG C096
- **Root cause (suspected):** one item is in a Development, the other was left out of it
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)

**A** Developments none (not surfaced) · langs it
  actors: - · places: Oman
- `sx-39` 2026-09-30 09:27 (tick 4) [ANSA Mondo, it] [-] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino

**B** Developments D24 (6 items) · langs it
  actors: - · places: -
- `sx-40` 2026-09-30 08:40 (tick 4) [ANSA Mondo, it] [D24] 'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota ucraino'

---

### D068 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C103 (owner (corrected draft)))
- **References:** IG C103
- **Root cause (suspected):** one item is in a Development, the other was left out of it
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** different but should be bundled together into one piece of news

**A** Developments D1 (2 items) · langs en
  actors: - · places: Brussels, Europe
- `sx-352` 2026-09-29 22:00 (tick 3) [European Commission Press, en] [D1] Commission proposes a new EU Critical Communication System for first responders

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-350` 2026-09-29 22:00 (tick 3) [European Commission Press, en] [-] Factsheet: EU Critical Communication System

---

### D073 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C113 (owner (agrees with draft)))
- **References:** IG C113
- **Root cause (suspected):** segmentation cut the link between them (guard: disjoint_locations)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)

**A** Developments none (not surfaced) · langs it
  actors: - · places: Oman
- `sx-39` 2026-09-30 09:27 (tick 4) [ANSA Mondo, it] [-] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emiratino

**B** Developments D24 (6 items) · langs it
  actors: - · places: Dubai, Israele
- `sx-232` 2026-09-30 09:25 (tick 4) [Il Sole 24 Ore Mondo, it] [D24] Allarme su volo FlyDubai dirottato, copilota accoltella comandante. Tentativo di far schiantare l’aereo

---

### D075 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G01 (owner-given (2026-10-07)))
- **References:** IG G01
- **Root cause (suspected):** a report not clustered (no Development)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** owner, 2026-10-07: R012: one matter, BBC / France 24

**A** Developments none (not surfaced) · langs en
  actors: - · places: U.S.
- `sx-100` 2026-09-29 01:12 (tick 2) [BBC World, en] [-] Are Trump's US government funded ads illegal?

**B** Developments none (not surfaced) · langs en
  actors: - · places: France
- `sx-170` 2026-09-29 20:56 (tick 3) [France 24, en] [-] Public service announcement or Donald Trump propaganda?

---

### D078 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G08 (owner-given (2026-10-07)))
- **References:** IG G08
- **Root cause (suspected):** a report not clustered (no Development)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** owner, 2026-10-07: T033: rial record low (GDELT)

**A** Developments none (not surfaced) · langs en
  actors: - · places: India, Iran
- `sx-535` 2026-09-29 14:45 (tick 3) [GDELT, en] [-] Iran rial crashes past 2 . 5 million per dollar : War , sanctions push currency to new low

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-536` 2026-09-30 01:15 (tick 4) [GDELT, en] [-] Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability

---

### D079 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 4 G09 (owner-given (2026-10-07)))
- **References:** IG G09
- **Root cause (suspected):** a report not clustered (no Development)
- **Blocks a Phase 3 endpoint:** yes: a side has no Development (NOT_SURFACED)
- **Notes:** owner, 2026-10-07: T039: rial record low (GDELT)

**A** Developments none (not surfaced) · langs en
  actors: - · places: Iran, U.S.
- `sx-540` 2026-09-29 16:30 (tick 3) [GDELT, en] [-]   This is how the war will end : Iran currency hits new record low

**B** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-536` 2026-09-30 01:15 (tick 4) [GDELT, en] [-] Iran Currency Hits a New Record Low as War Erodes the Country Economic Stability

---

## AMBIGUOUS (1)

### D007 · 2026-08-21

- **Expected:** AMBIGUOUS (identity gold rev 2 A028 (owner (corrected draft)))
- **References:** IG A028
- **Root cause (suspected):** expected identity is AMBIGUOUS
- **Blocks a Phase 3 endpoint:** unknown
- **Notes:** it is different only if the re-establishment didn't force families out in the same area. When in doubt we should trigger a sequence that makes sure we're talking about the same event: detecting perhaps a common source cited, common location etc..

**A** Developments D5 (3 items) · langs en
  actors: Israel · places: Israel, Palestine, West Bank
- `b-52e7176bac0a` 2026-08-21T05:00 (tick 1) [BBC World, en] [D5] Israel re-establishes closed West Bank settlement, defying growing international protests

**B** Developments D5 (3 items) · langs en
  actors: Israel · places: Israel, Occupied West Bank, Palestine, Qaryut
- `b-9d435faf259d` 2026-08-22T15:45 (tick 4) [Al Jazeera, en] [D5] Settlers target Palestinian homes in Occupied West Bank’s Area B

---

## CORRECT_BEHAVIOR (23)

### D001 · 2026-08-21

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 A006 (owner (agrees with draft)))
- **References:** CT A006 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments none (not surfaced) · langs en
  actors: - · places: Hong Kong, Lee Kuan Yew School, Singapore
- `b-47221c4faf92` 2026-08-21T12:08 (tick 2) [South China Morning Post, en] [-] Singapore’s carrots for fund managers set to sharpen competition with Hong Kong

**B** Developments none (not surfaced) · langs en
  actors: - · places: Hong Kong, Singapore
- `b-dfc16b535283` 2026-08-21T01:00 (tick 1) [South China Morning Post, en] [-] Hong Kong financiers press for tax breaks after Singapore unveils rival scheme

---

### D002 · 2026-08-21

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 A024 (owner (agrees with draft)))
- **References:** CT A024 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D2 (3 items) · langs en
  actors: - · places: Fagersta, Sweden
- `b-25760921e54e` 2026-08-21T13:48 (tick 2) [Al Jazeera, en] [D2] Several people injured in sword attack at school in Sweden

**B** Developments D2 (3 items) · langs en
  actors: - · places: Sweden
- `b-53dc89e53904` 2026-08-21T21:03 (tick 2) [BBC World, en] [D2] One killed in sword attack at Swedish school

---

### D003 · 2026-08-21

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 A027 (owner (agrees with draft)))
- **References:** CT A027 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D1 (3 items) · langs en
  actors: - · places: China, Hong Kong, Tiananmen
- `b-7d87768d2f82` 2026-08-21T05:47 (tick 1) [BBC World, en] [D1] Hong Kong's Tiananmen activists guilty in national security trial

**B** Developments D1 (3 items) · langs en
  actors: - · places: China, Hong Kong, Hong Kong Tiananmen, Tiananmen Square
- `b-85e1f8c5197d` 2026-08-21T02:28 (tick 1) [South China Morning Post, en] [D1] Hong Kong Tiananmen vigil organiser, former leaders guilty of inciting subversion

---

### D013 · 2026-09-25

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 B003 (owner (agrees with draft)))
- **References:** CT B003 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D2 (2 items) · langs en
  actors: Giorgia Meloni, Italy, Meloni · places: Italy
- `b-8a758a84c401` 2026-09-25T02:07 (tick 4) [Al Jazeera, en] [D2] Meloni government bans burqas, caps foreign students in Italian schools

**B** Developments D2 (2 items) · langs en
  actors: Giorgia Meloni, Italy, Meloni · places: Italy
- `b-256c7087fa4e` 2026-09-24T19:32 (tick 3) [BBC World, en] [D2] Italy ministers agree to ban burqa and niqab in school and cap foreigners in class

---

### D032 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C014 (owner (agrees with draft)))
- **References:** CT C014 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-238` 2026-09-29 19:04 (tick 3) [Il Sole 24 Ore Mondo, it] [D9] Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia il nome in Super Intelligence

**B** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-131` 2026-09-29 23:32 (tick 3) [Rai News Esteri, it] [D9] Donald Trump e la nuova "età dell'oro": vertice con i big della tecnologia

---

### D033 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C019 (owner (agrees with draft)))
- **References:** CT C019 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D3 (3 items) · langs en
  actors: Raytheon, US Department of Defense · places: -
- `sx-510` 2026-09-29 16:59 (tick 3) [Breaking Defense, en] [D3] Raytheon nets potential $20.7 billion AMRAAM deal

**B** Developments D3 (3 items) · langs en
  actors: Raytheon, US Department of Defense · places: -
- `sx-488` 2026-09-29 16:18 (tick 3) [Defense News, en] [D3] Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM production

---

### D034 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C025 (owner (agrees with draft)))
- **References:** CT C025 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D16 (3 items) · langs it
  actors: - · places: Marocco, Marrakech, Paese Avvocata, Regno
- `sx-127` 2026-09-30 04:06 (tick 4) [Rai News Esteri, it] [D16] Marocco, Fatima Zahara Mansouri è la prima donna premier della storia del Paese

**B** Developments none (not surfaced) · langs it
  actors: - · places: Fonti Ue
- `sx-42` 2026-09-30 08:28 (tick 4) [ANSA Mondo, it] [-] Fonti Ue, 'boom nelle spesa in difesa, fino a 547 miliardi entro il 2029'

---

### D035 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C035 (owner (agrees with draft)))
- **References:** CT C035 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D13 (2 items) · langs es
  actors: - · places: Francia, PARIS
- `sx-186` 2026-09-30 02:20 (tick 4) [France 24 Español, es] [D13] Informe desde París: más de 200 manifestaciones de empleados públicos, pide aumento de sueldo

**B** Developments D8 (5 items) · langs es
  actors: Emmanuel Macron, Macron · places: España
- `sx-111` 2026-09-29 15:04 (tick 3) [BBC Mundo, es] [D8] La anciana Maricarmen podrá volver a su casa tras el desalojo que puso el foco en la crisis de vivienda en España

---

### D036 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C043 (owner (agrees with draft)))
- **References:** CT C043 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D3 (3 items) · langs en
  actors: Raytheon, US Department of Defense · places: U.S.
- `sx-4` 2026-09-28 21:00 (tick 1) [Defense.gov, en] [D3] Department of War and RTX Accelerate Advanced Medium-Range Air-to-Air Missile Production Through $20.7B Award

**B** Developments D3 (3 items) · langs en
  actors: Raytheon, US Department of Defense · places: -
- `sx-510` 2026-09-29 16:59 (tick 3) [Breaking Defense, en] [D3] Raytheon nets potential $20.7 billion AMRAAM deal

---

### D037 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C044 (owner (agrees with draft)))
- **References:** CT C044 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments none (not surfaced) · langs en
  actors: - · places: Gambia, Ghana, Guinea Bissau, Nigeria
- `sx-198` 2026-09-30 07:21 (tick 4) [Al Jazeera, en] [-] Nigeria and Ghana suffer huge AFCON 2027 qualifying shocks

**B** Developments none (not surfaced) · langs en
  actors: - · places: Ethiopia, Senegal
- `sx-160` 2026-09-30 06:15 (tick 4) [France 24, en] [-] 2027 AFCON qualifiers: First win for Patrick Vieira and Senegal

---

### D038 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C056 (owner (agrees with draft)))
- **References:** CT C056 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments none (not surfaced) · langs en
  actors: - · places: Russia, Ukraine
- `sx-278` 2026-09-30 06:40 (tick 4) [Kyiv Independent, en] [-] General Staff: Russia has lost 1,533,970 troops in Ukraine since Feb. 24, 2022

**B** Developments D2 (3 items) · langs en
  actors: Russia, Vladimir Putin · places: Oleshky, Russia, Ukraine
- `sx-282` 2026-09-29 17:43 (tick 3) [Kyiv Independent, en] [D2] Ukraine war latest: Record Russian military budget for 2027 confirms no interest in ending war

---

### D039 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C070 (owner (agrees with draft)))
- **References:** CT C070 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments none (not surfaced) · langs it
  actors: - · places: Puerta del Sol, Spagna
- `sx-241` 2026-09-29 14:59 (tick 3) [Il Sole 24 Ore Mondo, it] [-] Spagna, Sánchez vara nuove misure contro la crisi abitativa: cosa cambia per affitti e sfratti

**B** Developments D9 (12 items) · langs it
  actors: Donald Trump, Trump · places: -
- `sx-57` 2026-09-29 20:36 (tick 3) [ANSA Mondo, it] [D9] Trump, 'da vertici big tech impegno moralmente vincolante su sicurezza IA'

---

### D040 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C071 (owner (agrees with draft)))
- **References:** CT C071 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments none (not surfaced) · langs it
  actors: - · places: -
- `sx-43` 2026-09-30 07:31 (tick 4) [ANSA Mondo, it] [-] Ft, colloqui tra Trump e consiglieri per valutare uno stop all'export di gasolio

**B** Developments none (not surfaced) · langs it
  actors: - · places: Cancellate, Cuba, U.S.
- `sx-128` 2026-09-30 01:54 (tick 4) [Rai News Esteri, it] [-] USA, stretta finale su Cuba. Stangata bancaria, stop ai viaggi e blocco finanziario

---

### D041 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C072 (owner (agrees with draft)))
- **References:** CT C072 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Iran, Iraq, Tehran, U.S.
- `sx-491` 2026-09-29 14:40 (tick 3) [Defense News, en] [D5] US forces exiting Iraq after 2 decades, leaving opening for Iran

**B** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Iran, Iraq, U.S.
- `sx-164` 2026-09-30 01:04 (tick 4) [France 24, en] [D5] US forces leave Iraq, raising fears of Iran-backed militias amid power vacuum

---

### D042 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C086 (owner (agrees with draft)))
- **References:** CT C086 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-5` 2026-09-28 20:30 (tick 1) [Defense.gov, en] [-] Secretary of War Pete Hegseth Signs Directive to Defend 2026 Elections From Foreign Threats

**B** Developments none (not surfaced) · langs en
  actors: - · places: U.S.
- `sx-3` 2026-09-29 18:10 (tick 3) [Defense.gov, en] [-] Secretary of War Pete Hegseth Signs Directive Halting Tenured Civilian Positions at U.S. Military Service Academies

---

### D043 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C089 (owner (agrees with draft)))
- **References:** CT C089 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Iran, Iraq, Tehran, U.S.
- `sx-491` 2026-09-29 14:40 (tick 3) [Defense News, en] [D5] US forces exiting Iraq after 2 decades, leaving opening for Iran

**B** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Baghdad, Iraq, U.S.
- `sx-149` 2026-09-29 11:08 (tick 2) [DW World, en] [D5] Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission against ISIS after 12 years

---

### D044 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C100 (owner (agrees with draft)))
- **References:** CT C100 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments none (not surfaced) · langs en
  actors: - · places: -
- `sx-167` 2026-09-29 22:48 (tick 3) [France 24, en] [-] AI companies sign voluntary accord on safety with Trump

**B** Developments none (not surfaced) · langs en
  actors: - · places: U.S.
- `sx-209` 2026-09-30 03:00 (tick 4) [Al Jazeera, en] [-] Trump backs AI self-regulation at tech summit but is it enough?

---

### D045 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C109 (owner (agrees with draft)))
- **References:** CT C109 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Iran, Iraq, U.S.
- `sx-164` 2026-09-30 01:04 (tick 4) [France 24, en] [D5] US forces leave Iraq, raising fears of Iran-backed militias amid power vacuum

**B** Developments D5 (5 items) · langs en
  actors: U.S., Washington · places: Baghdad, Iraq, U.S.
- `sx-149` 2026-09-29 11:08 (tick 2) [DW World, en] [D5] Iraq: US troops withdraw from their Iraqi US-led Operation Inherent Resolve mission against ISIS after 12 years

---

### D046 · 2026-09-30-multilingual

- **Expected:** DIFFERENT_DEVELOPMENT (identity gold rev 2 C110 (owner (agrees with draft)))
- **References:** CT C110 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D16 (3 items) · langs it
  actors: - · places: Marocco, Marrakech, Paese Avvocata, Regno
- `sx-127` 2026-09-30 04:06 (tick 4) [Rai News Esteri, it] [D16] Marocco, Fatima Zahara Mansouri è la prima donna premier della storia del Paese

**B** Developments D19 (2 items) · langs es
  actors: - · places: Gobierno, Marruecos
- `sx-77` 2026-09-30 07:40 (tick 4) [Europa Press Internacional, es] [D19] La primera ministra designada de Marruecos iniciará hoy una ronda de contactos para ensamblar el nuevo Gobierno

---

### D047 · 2026-09-30-multilingual

- **Expected:** SAME_DEVELOPMENT (identity gold rev 2 C114 (owner (agrees with draft)))
- **References:** CT C114 (control)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D11 (3 items) · langs en
  actors: U.S. · places: China, Hong Kong, Iran, Pakistan, Russia, Tehran, U.S.
- `sx-279` 2026-09-30 02:28 (tick 4) [Kyiv Independent, en] [D11] US imposes sanctions against Russian companies tied to Iran weapons procurement

**B** Developments D11 (3 items) · langs en
  actors: U.S. · places: Iran, Russia, Sheet, U.S.
- `sx-13` 2026-09-29 17:32 (tick 3) [State Department, en] [D11] United States Disrupts Iran’s Proliferation-Sensitive Efforts in Support of UN Restrictions Fact Sheet

---

### D097 · 2026-10-03-live

- **Expected:** SAME_DEVELOPMENT (owner identity verdict 2026-10-07b (T008))
- **References:** CT T008 (blocked relation pair, correct merge)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D3 (5 items) · langs en
  actors: Spain · places: Spain
- `s-1124` 2026-09-29 12:14 (tick 1) [BBC World, en] [D3] Spain announces new housing measures after protests over 87-year-old woman's eviction

**B** Developments D3 (5 items) · langs en
  actors: Spain · places: Spain
- `s-1316` 2026-09-29 16:23 (tick 1) [BBC World, en] [D3] Spain announces ban on evictions after protests over 87-year-old woman's removal from flat

---

### D098 · 2026-10-03-live

- **Expected:** SAME_DEVELOPMENT (owner identity verdict 2026-10-07b (T034))
- **References:** CT T034 (blocked relation pair, correct merge)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D3 (5 items) · langs en
  actors: Spain · places: Madrid, Spain
- `s-1200` 2026-09-29 17:54 (tick 1) [South China Morning Post, en] [D3] 87-year-old woman whose eviction sparked protests in Spain is returning home

**B** Developments D3 (5 items) · langs en
  actors: Spain · places: Madrid, Spain
- `s-1233` 2026-09-29 21:02 (tick 1) [Al Jazeera, en] [D3] Spain protests: Evicted 87-year-old woman to return to Madrid home

---

### D099 · 2026-10-03-live

- **Expected:** SAME_DEVELOPMENT (owner identity verdict 2026-10-07b (T041))
- **References:** CT T041 (blocked relation pair, correct merge)
- **Root cause (suspected):** -
- **Blocks a Phase 3 endpoint:** no

**A** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Tennessee
- `s-1525` 2026-10-01 04:14 (tick 4) [South China Morning Post, en] [D19] Tennessee halts executions after Christa Pike survives 2 doses of lethal drug

**B** Developments D19 (14 items) · langs en
  actors: Christa Pike, Pike, US · places: Nashville, Tennessee, US
- `s-1663` 2026-10-01 16:45 (tick 5) [BBC World, en] [D19] Tennessee halts executions after Christa Pike survives two lethal injection attempts
- `s-1790` 2026-10-02 03:02 (tick 6) [South China Morning Post, en] [D19] Christa Pike in ‘life-saving care’ after botched Tennessee execution
- `s-1834` 2026-10-02 07:58 (tick 6) [Al Jazeera, en] [D19] Lawyers for US inmate who survived lethal injections demand release
- `s-1921` 2026-10-02 20:57 (tick 7) [Al Jazeera, en] [D19] Christa Pike unconscious, on ventilator after botched execution: Lawyers
- `s-1935` 2026-10-02 20:32 (tick 7) [BBC World, en] [D19] US murderer Christa Pike unconscious and on ventilator after failed execution, lawyers say

---

