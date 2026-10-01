# Phase 2 baseline: current Development identity on gold revision 2

What the **current** runtime (Phase 1 branch, no change) does with Development identity before any Phase 2 code exists. Gold: revision 2 (`gold/manifest.yaml`, sha256 cc98765b7506...).

Method:
- the three **development** windows are replayed tick by tick (4 × 12 h) twice, each in a clean temporary DB, by `scripts/phase2_baseline.py`;
- the **holdout window is neither replayed nor scored**;
- a gold pair counts as *kept together* when, after the later item's tick, both items share a Development ID. The current code never deletes, splits or merges Developments, so final membership plus each membership's tick is the full history;
- AMBIGUOUS cases (1) are excluded.

**Scope caveat.** These are rates over the gold's candidate pairs (chosen by the candidate rules), not over every pair in the windows. They measure the decisions the gold covers.

## Baseline metrics

| Window | Pairs scored | Continuity precision | Continuity recall | Split failures (DIFFERENT kept together) | Merge failures (SAME kept apart) | ID stability (cross-tick SAME retained) |
|---|---:|---:|---:|---:|---:|---:|
| 2026-08-21 | 32 | 7/12 (58%) | 7/7 (100%) | 5/25 (20%) | 0/7 (0%) | 1/1 (100%) |
| 2026-09-25 | 11 | 2/4 (50%) | 2/5 (40%) | 2/6 (33%) | 3/5 (60%) | 1/2 (50%) |
| 2026-09-30-multilingual | 115 | 32/56 (57%) | 32/46 (70%) | 24/69 (35%) | 14/46 (30%) | 12/16 (75%) |
| **all development** | **158** | **41/72 (57%)** | **41/58 (71%)** | **31/100 (31%)** | **17/58 (29%)** | **14/19 (74%)** |

Definitions:
- **Continuity precision:** of the gold pairs the runtime keeps under one ID, the share that are SAME.
- **Continuity recall:** of the SAME pairs, the share kept under one ID.
- **Split failure rate:** over DIFFERENT pairs.
- **Merge failure rate:** over SAME pairs.
- **ID stability:** SAME pairs whose items arrive at different ticks and where the later item joined the earlier item's Development.

| Development-level | Result |
|---|---:|
| Mixed-Development rate (Developments containing a gold DIFFERENT pair / Developments containing any gold pair) | 14/33 (42%) |
| Mixed Developments / all multi-item Developments | 14/39 (36%) |
| Duplicate-membership rate (items in more than one Development / items in any Development) | 0/118 (0%) |
| Memberships added after their Development was created (overlap extensions) | 12 memberships in 3 Developments |

## Determinism result

- **2026-08-21**: run 1 vs run 2 identical; run 1 vs the committed review trace identical
- **2026-09-25**: run 1 vs run 2 identical; run 1 vs the committed review trace identical
- **2026-09-30-multilingual**: run 1 vs run 2 identical; run 1 vs the committed review trace identical

**Findings (this run and the investigation before it):**
- Development IDs, memberships and the tick of every membership were identical in every replay of every development window: 2026-08-21 was replayed 7 times, the others 4 times each.
- **One order difference was observed.** In an earlier baseline run, 2026-08-21's pre-segmentation cluster list and cut list at tick 2 came out in a different **order** in one of two runs. Contents (as sets) and the resulting Developments were the same.
- **Reproduced:** replaying the window as if 30 minutes more had passed between ticks gives the same tick-2 difference.
- **Exact source, part 1:** `clustering.recent_items` (`osint_monitor/processors/clustering.py:43-53`) selects items with `cutoff = datetime.utcnow() - 48 h`. Identical inputs processed at a different wall-clock moment can therefore drop an edge item from the candidate set, which renumbers HDBSCAN's labels and reorders the clusters.
- **Exact source, part 2:** `persist_clusters` is order-dependent. It walks clusters in list order, extends the first existing Development an overlapping cluster meets (`_find_overlapping_event`, unordered `.first()`, `clustering.py:548-557`), and allocates new Development IDs in that order.
- **Impact:** no identity difference was observed in these windows, but the mechanism can change which Development an overlapping cluster joins, and which ID a new Development gets, between runs of identical input.
- **This replay is not the daemon.** In the daemon the window cutoff is a real input, a time; the replay harness only makes it visible. Phase 2's identity rule must not depend on the order clusters are produced in, nor on `.first()`.

## Error ledger

48 failures: merge failure (SAME kept apart) 17, split failure (DIFFERENT kept together) 31.

| Error class | Split failures | Merge failures |
|---|---:|---:|
| whole-storyline overmerge | 17 | 0 |
| late attachment | 12 | 0 |
| segmentation interaction | 0 | 8 |
| missed continuation | 0 | 7 |
| other | 0 | 2 |
| single-source promotion | 1 | 0 |
| roundup contamination | 1 | 0 |

| Case | Gold | Current | Development IDs | Ticks | Items | Error class | Likely root cause |
|---|---|---|---|---|---|---|---|
| A002 | DIFFERENT | kept together | D5 / D5 | t4/t1 | `b-ed25155d038d` [BBC World, en] Carney calls Trump's fresh tariffs a 'miscalculation' after trade talk<br>`b-320f20d36f00` [South China Morning Post, en] Canadian premier says ‘erratic’ Trump ‘not to be trusted’ amid US trad | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them |
| A013 | DIFFERENT | kept together | D6 / D6 | t4/t4 | `b-9d435faf259d` [Al Jazeera, en] Settlers target Palestinian homes in Occupied West Bank’s Area B<br>`b-e65cd1bb15f4` [Al Jazeera, en] Jewish activists push back against Israeli settlers | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |
| A021 | DIFFERENT | kept together | D3 / D3 | t2/t3 | `b-2e0da6b7e7eb` [BBC World, en] Ebola vaccine trial to start in DR Congo as warning issued over speed <br>`b-8826249c972c` [Al Jazeera, en] More than 16,000 doses of Ervebo vaccine arrive in Ebola-hit DR Congo | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |
| A022 | DIFFERENT | kept together | D3 / D3 | t3/t2 | `b-422186e87411` [Al Jazeera, en] Ebola continues to spread in the DRC as 16,000 vaccine doses arrive<br>`b-2e0da6b7e7eb` [BBC World, en] Ebola vaccine trial to start in DR Congo as warning issued over speed  | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |
| A023 | DIFFERENT | kept together | D6 / D6 | t1/t4 | `b-52e7176bac0a` [BBC World, en] Israel re-establishes closed West Bank settlement, defying growing int<br>`b-e65cd1bb15f4` [Al Jazeera, en] Jewish activists push back against Israeli settlers | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |
| B002 | SAME | not grouped | – / – | t3/t3 | `b-5d1ba8e525da` [Breaking Defense, en] OCCAR awards $4.2B DDX destroyer contract to Fincantieri, Leonardo joi<br>`b-d72e5f6a5e01` [Defense News, en] Italy taps state-owned firms to build two naval destroyers in $4.2 bil | other | same-tick items of one occurrence not grouped (below the link threshold or left as noise) |
| B004 | SAME | not grouped | – / – | t4/t4 | `b-63cb0d4f2400` [BBC World, en] Trump and Xi exchange warm words at state dinner but little progress o<br>`b-9796005bb46b` [South China Morning Post, en] From wine to ping-pong, Trump and Xi’s state dinner is heavy on histor | other | same-tick items of one occurrence not grouped (below the link threshold or left as noise) |
| B007 | SAME | not grouped | – / – | t3/t1 | `b-6e3eb47c7f66` [Breaking Defense, en] The Air Force says its China think tank will continue. Its director sa<br>`b-aa291f31d75e` [Defense News, en] Air Force, civilian staff dispute status of China Aerospace Studies In | segmentation interaction | segmentation cut the link between them (guard: headline_similarity) |
| B008 | DIFFERENT | kept together | D1 / D1 | t4/t4 | `b-683038d2cd37` [South China Morning Post, en] Trump gives Xi a tour of his pet White House building projects, includ<br>`b-97cb65d1a469` [BBC World, en] Xi got Trump's red carpet welcome - but not everything he wanted | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them |
| B011 | DIFFERENT | kept together | D2 / D2 | t4/t3 | `b-38730424bfbc` [Al Jazeera, en] Pakistani forces kill Afghan Taliban fighters in border escalation<br>`b-14aae9d37ebe` [BBC World, en] Four civilians killed in Pakistani strikes in Afghanistan, Taliban say | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them |
| C001 | DIFFERENT | kept together | D6 / D6 | t3/t3 | `sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big<br>`sx-133` [Rai News Esteri, it] Gli Usa prestano alle aziende energetiche 40 milioni di barili di petr | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C002 | DIFFERENT | kept together | D6 / D6 | t4/t3 | `sx-48` [ANSA Mondo, it] Trump firma ordine esecutivo, 'inaugura l'era della Super Intelligenza<br>`sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C003 | DIFFERENT | kept together | D1 / D1 | t2/t2 | `sx-553` [Federal Register, en] Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a C<br>`sx-554` [Federal Register, en] Accreditation and Approval of Intertek USA, Inc. (Carteret, NJ), as a  | single-source promotion | one outlet's near-identical headlines form the Development on their own |
| C005 | SAME | not grouped | – / – | t3/t1 | `sx-421` [UN Press, en] At ‘Most Dangerous Nuclear Moment’ Since Cold War Ended, Secretary-Gen<br>`sx-424` [UN Press, en] International Security Rapidly Deteriorates; General Assembly Urges Na | missed continuation | the later item did not join the earlier item's Development (or neither was clustered) |
| C007 | DIFFERENT | kept together | D6 / D6 | t3/t3 | `sx-131` [Rai News Esteri, it] Donald Trump e la nuova "età dell'oro": vertice con i big della tecnol<br>`sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (15-item Development); segmentation did not cut them |
| C012 | DIFFERENT | kept together | D6 / D6 | t3/t3 | `sx-131` [Rai News Esteri, it] Donald Trump e la nuova "età dell'oro": vertice con i big della tecnol<br>`sx-263` [El País Internacional, es] Trump lanza una página oficial de información sobre el Gobierno de EE  | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (15-item Development); segmentation did not cut them |
| C017 | DIFFERENT | kept together | D6 / D6 | t3/t3 | `sx-238` [Il Sole 24 Ore Mondo, it] Trump, per Ai solo autoregolamentazione. Firmato l’ordine che cambia i<br>`sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (15-item Development); segmentation did not cut them |
| C022 | DIFFERENT | kept together | D6 / D6 | t3/t4 | `sx-71` [Europa Press Internacional, es] Trump ordena renombrar la 'Inteligencia Artificial' como 'Súper Inteli<br>`sx-176` [France 24 Español, es] Trump y los gigantes de la inteligencia artificial sellan un acuerdo " | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C026 | DIFFERENT | kept together | D20 / D20 | t3/t4 | `sx-264` [Clarín Mundo, es] Por la guerra y la incertidumbre económica, la moneda de Irán se hunde<br>`sx-75` [Europa Press Internacional, es] Irán confirma que recibió la respuesta oficial de EEUU a su última pro | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |
| C033 | DIFFERENT | kept together | D20 / D20 | t4/t4 | `sx-75` [Europa Press Internacional, es] Irán confirma que recibió la respuesta oficial de EEUU a su última pro<br>`sx-536` [GDELT, en] Iran Currency Hits a New Record Low as War Erodes the Country Economic | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |
| C034 | SAME | not grouped | D3 / – | t3/t3 | `sx-352` [European Commission Press, en] Commission proposes a new EU Critical Communication System for first r<br>`sx-351` [European Commission Press, en] Questions and answers on the European Union Critical Communication Sys | missed continuation | one item is in a Development, the other was left out of it |
| C035 | DIFFERENT | kept together | D7 / D7 | t4/t3 | `sx-186` [France 24 Español, es] Informe desde París: más de 200 manifestaciones de empleados públicos,<br>`sx-111` [BBC Mundo, es] La anciana Maricarmen podrá volver a su casa tras el desalojo que puso | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C036 | SAME | not grouped | D12 / – | t3/t3 | `sx-240` [Il Sole 24 Ore Mondo, it] «Hope again», l’appello di Burnham agli inglesi tra stop alle privatiz<br>`sx-145` [DW World, en] UK PM Burnham seeks 'hope again' at Labour Party conference | segmentation interaction | segmentation cut the link between them (guard: headline_similarity) (cross-language: the embedding model is English-only) |
| C037 | DIFFERENT | kept together | D7 / D7 | t4/t3 | `sx-181` [France 24 Español, es] Trabajadores públicos franceses se movilizan para exigir aumentos de s<br>`sx-111` [BBC Mundo, es] La anciana Maricarmen podrá volver a su casa tras el desalojo que puso | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C042 | DIFFERENT | kept together | D6 / D6 | t3/t3 | `sx-130` [Rai News Esteri, it] Tradurre il potere, l'arduo mestiere dell'interprete<br>`sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C043 | SAME | not grouped | – / D2 | t1/t3 | `sx-4` [Defense.gov, en] Department of War and RTX Accelerate Advanced Medium-Range Air-to-Air <br>`sx-510` [Breaking Defense, en] Raytheon nets potential $20.7 billion AMRAAM deal | segmentation interaction | segmentation cut the link between them (guard: headline_similarity) |
| C046 | DIFFERENT | kept together | D7 / D7 | t4/t3 | `sx-76` [Europa Press Internacional, es] Al menos 440 detenidos en Francia en protestas estudiantiles unidas a <br>`sx-111` [BBC Mundo, es] La anciana Maricarmen podrá volver a su casa tras el desalojo que puso | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C051 | SAME | not grouped | – / – | t3/t3 | `sx-400` [UN News, en] Security Council LIVE: DRC peace deals fail to halt fighting as Ebola <br>`sx-416` [UN Press, en] Commitments Must Yield Tangible Progress in Democratic Republic of Con | segmentation interaction | segmentation cut the link between them (guard: headline_similarity) |
| C062 | DIFFERENT | kept together | D7 / D7 | t4/t3 | `sx-76` [Europa Press Internacional, es] Al menos 440 detenidos en Francia en protestas estudiantiles unidas a <br>`sx-270` [Clarín Mundo, es] Presionado por las protestas, Pedro Sánchez anuncia decretos clave par | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C063 | DIFFERENT | kept together | D6 / D6 | t3/t3 | `sx-263` [El País Internacional, es] Trump lanza una página oficial de información sobre el Gobierno de EE <br>`sx-133` [Rai News Esteri, it] Gli Usa prestano alle aziende energetiche 40 milioni di barili di petr | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C064 | SAME | not grouped | – / – | t1/t3 | `sx-423` [UN Press, en] Security Council, 10232nd Meeting (AM) Democratic Republic of the Cong<br>`sx-416` [UN Press, en] Commitments Must Yield Tangible Progress in Democratic Republic of Con | missed continuation | the later item did not join the earlier item's Development (or neither was clustered) |
| C066 | SAME | not grouped | D21 / – | t4/t4 | `sx-122` [Rai News Esteri, it] Volo Flydubai, l'aereo diretto a Tel Aviv viene deviato in Arabia Saud<br>`sx-39` [ANSA Mondo, it] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emir | segmentation interaction | segmentation cut the link between them (guard: disjoint_locations) |
| C073 | DIFFERENT | kept together | D6 / D6 | t4/t3 | `sx-235` [Il Sole 24 Ore Mondo, it] Ft: Trump valuta il divieto di export del gasolio per contenere la cri<br>`sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C076 | SAME | not grouped | – / D15 | t4/t4 | `sx-277` [Kyiv Independent, en] Drone crashes in Moldova amid Russian mass attack on Ukraine<br>`sx-275` [Kyiv Independent, en] Russian attacks kill at least 6, injure 34 across Ukraine as Kyiv face | missed continuation | one item is in a Development, the other was left out of it |
| C077 | SAME | not grouped | – / D2 | t1/t3 | `sx-4` [Defense.gov, en] Department of War and RTX Accelerate Advanced Medium-Range Air-to-Air <br>`sx-488` [Defense News, en] Pentagon awards Raytheon up to $20.7 billion to nearly double AMRAAM p | segmentation interaction | segmentation cut the link between them (guard: headline_similarity) |
| C079 | DIFFERENT | kept together | D26 / D26 | t3/t4 | `sx-245` [El País Internacional, es] Tres soldados israelíes sobre Gaza: “Llegó un momento en que ya no par<br>`sx-80` [Europa Press Internacional, es] Muere una palestina en un nuevo ataque de Israel contra la ciudad de G | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them |
| C080 | DIFFERENT | kept together | D10 / D10 | t2/t3 | `sx-150` [DW World, en] Malaysia repatriates Myanmar migrants despite UN warnings<br>`sx-396` [UN News, en] World News in Brief: Deadly Myanmar strikes as Malaysia begins deporta | roundup contamination | a roundup item shares the Development, so its mixed headline links distinct occurrences |
| C084 | DIFFERENT | kept together | D6 / D6 | t4/t3 | `sx-43` [ANSA Mondo, it] Ft, colloqui tra Trump e consiglieri per valutare uno stop all'export <br>`sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C092 | SAME | not grouped | – / D21 | t4/t4 | `sx-39` [ANSA Mondo, it] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emir<br>`sx-123` [Rai News Esteri, it] Volo FlyDubai, la ricostruzione di Tel Aviv: "Pilota ha cercato di far | segmentation interaction | segmentation cut the link between them (guard: disjoint_locations) |
| C094 | DIFFERENT | kept together | D16 / D16 | t4/t2 | `sx-79` [Europa Press Internacional, es] El Senado de EEUU rechaza votar una resolución acerca de la violencia <br>`sx-243` [Il Sole 24 Ore Mondo, it] Cisgiordania, raid di coloni israeliani contro famiglia palestinese a  | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |
| C096 | SAME | not grouped | – / D21 | t4/t4 | `sx-39` [ANSA Mondo, it] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emir<br>`sx-40` [ANSA Mondo, it] 'Emergenza sul volo FlyDubai per una lite tra pilota russo e copilota  | missed continuation | one item is in a Development, the other was left out of it |
| C103 | SAME | not grouped | D3 / – | t3/t3 | `sx-352` [European Commission Press, en] Commission proposes a new EU Critical Communication System for first r<br>`sx-350` [European Commission Press, en] Factsheet: EU Critical Communication System | missed continuation | one item is in a Development, the other was left out of it |
| C104 | SAME | not grouped | D9 / – | t4/t4 | `sx-1` [Defense.gov, en] Statement by Chief Pentagon Spokesman Sean Parnell on the Conclusion o<br>`sx-121` [Rai News Esteri, it] Gli Stati Uniti annunciano la fine ufficiale della missione in Iraq | missed continuation | one item is in a Development, the other was left out of it (cross-language: the embedding model is English-only) |
| C105 | DIFFERENT | kept together | D25 / D25 | t3/t4 | `sx-139` [Rai News Esteri, it] Burnham: "Londra per troppo tempo sulla strada sbagliata, miglioreremo<br>`sx-41` [ANSA Mondo, it] Burnham su Brexit, 'tutte le opzioni sul tavolo, inclusa riadesione a  | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (2-item Development); segmentation did not cut them |
| C106 | DIFFERENT | kept together | D6 / D6 | t4/t3 | `sx-176` [France 24 Español, es] Trump y los gigantes de la inteligencia artificial sellan un acuerdo "<br>`sx-129` [Rai News Esteri, it] Politica e scienza divise, gli esperti: “L'autoregolamentazione di Big | late attachment | a later-tick cluster overlapping the Development extends it with a different occurrence (overlap-merge) |
| C112 | DIFFERENT | kept together | D6 / D6 | t3/t3 | `sx-267` [Clarín Mundo, es] Donald Trump anunció que los líderes del sector tecnológico firmaron u<br>`sx-263` [El País Internacional, es] Trump lanza una página oficial de información sobre el Gobierno de EE  | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (15-item Development); segmentation did not cut them |
| C113 | SAME | not grouped | – / D21 | t4/t4 | `sx-39` [ANSA Mondo, it] Media, piloti del volo FlyDubai sarebbero uno dell'Oman e l'altro emir<br>`sx-232` [Il Sole 24 Ore Mondo, it] Allarme su volo FlyDubai dirottato, copilota accoltella comandante. Te | segmentation interaction | segmentation cut the link between them (guard: disjoint_locations) |
| C115 | DIFFERENT | kept together | D14 / D14 | t2/t3 | `sx-152` [DW World, en] US sanctions on Iran's aviation industry make travel less predictable <br>`sx-13` [State Department, en] United States Disrupts Iran’s Proliferation-Sensitive Efforts in Suppo | whole-storyline overmerge | distinct occurrences of one storyline linked above the similarity threshold in one cluster (3-item Development); segmentation did not cut them |

## Duplicate membership findings

- **No item belongs to more than one Development** in any development window: 0 of 118 items in Developments.
- The mechanism that produced the 24 double memberships in the real snapshot (audit S1) needs a cluster that bridges two existing Developments across runs. These short replays did not trigger it.
- The schema now forbids a duplicate *pair*, UNIQUE(event, item) from Phase 1, but **not** one item in two Developments.

## Single-source findings

Product rule: *single-source evidence stays below the Development layer until independently corroborated.* Not implemented. Developments formed from one outlet only:

- 2026-09-30-multilingual D1: 2 items, all Federal Register: "Accreditation and Approval of Intertek USA, Inc. (Chelsea, MA), as a Commercial Gauger and Laboratory"

**1 single-source Development(s) in the development windows.** The runtime creates them (minimum cluster size 2, same-outlet links allowed when headlines are near-identical) and only flags them SINGLE_SOURCE. The real 2026-09-30 snapshot had more (INV E53, SX E17, audit section 6).

## Roundup findings

| Window / Development | Members | Roundup item | Sources with / without roundup | Corroboration | Summary is the roundup headline | Gold DIFFERENT pairs among the other members |
|---|---:|---|---:|---|---|---|
| 2026-09-30-multilingual D4 | 3 | sx-282 | 2 / 2 | PROBABLE | **yes** | none |
| 2026-09-30-multilingual D10 | 2 | sx-396 | 2 / 1 | PROBABLE | **yes** | none |
| 2026-09-30-multilingual D15 | 3 | sx-161 | 2 / 1 | PROBABLE | **yes** | none |

- **False corroboration:** 2 of 3 Developments with a roundup item would have one source fewer without it. The roundup is counted as an independent source (both are rated PROBABLE).
- **Roundup as summary:** in 3 of 3 the Development's summary is the roundup headline, although a normal report of the occurrence is a member.
- **Roundup forcing unrelated occurrences together:** no gold DIFFERENT pair among the non-roundup members of these Developments. The one roundup-driven split failure (C080) is the roundup item itself grouped with a report of one of its many stories.

## Main structural failure modes

1. **Whole-storyline overmerge (17) and late attachment (12) are the split failures.**
   - Distinct actions of one storyline are linked by similar language: the Ebola warning vs the vaccine trial vs the dose arrival; settlers vs activists; the Trump AI order vs the self-regulation accord vs the expert commentary.
   - Persisted Developments then absorb later clusters by overlap. D6 in the multilingual window holds the AI order, the self-regulation accord and the expert commentary at creation (tick 3). At tick 4 it absorbs an interpreter feature, the strategic oil loan and a diesel export ban.
   - Segmentation cuts only within a batch, and overlap-merge undoes its cuts at persistence.
2. **Segmentation interaction (8) is the main merge failure.**
   - Guards cut links between reports of one occurrence: the FlyDubai incident across Italian outlets; the Pentagon release vs the Raytheon contract report; the UN live coverage vs the UN press summary.
   - Most of these pairs differ in headline wording, language, or report vs official release.
3. **Missed continuation and grouping (7 + 2 other).**
   - SAME items stay outside the Development, or form a second one.
   - Examples: the Commission proposal vs its Q&A and factsheet (C034, C103); a Security Council meeting record vs its briefing (C064); the drone crash vs the same attack (C076); cross-language pairs.
   - Contributing factor: the embedding model is English-only.
4. **Single-source promotion (1) and roundup contamination (1).**
   - These are few in the ledger, but they are policy gaps rather than tuning issues:
     - a single-source Development exists;
     - roundups count as sources and become summaries.
5. **Order dependence.** Identity can depend on cluster order and on `.first()`; see *Determinism result*.

Nothing in this document proposes a change; Phase 2 design starts from these failure modes and the contract (`development-identity-contract.md`).

PHASE 2 BASELINE COMPLETE
