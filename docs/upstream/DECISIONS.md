# Upstream owner decisions (2026-11-14; owner rulings recorded 2026-11-23)

Every semantic choice in the upstream track is listed here before any code. Each is marked
**`OWNER DECISION REQUIRED`** or **`ALREADY FROZEN`**. Nothing marked "required" is implemented until approved.

Fields per decision: (1) function / rule, (2) current behaviour, (3) alternatives, (4) examples, (5) precision /
recall trade-off, (6) downstream, (7) recommendation, (8) reversible?, (9) needs a new frozen evaluation?

**Already frozen, not reopened here:**
- the v2 topic families and event-type mapping (contract §1.1, `bf57ed7`);
- `generic_parties` v1;
- `create_window_days` 7, single-party separation 24 h, `pending_days` 7;
- the hazard and hedge lexicons v1;
- seeded scope metadata v1 (amendment 1, `bbc9bba`);
- the owner ruling that a strike is located at its impact (2026-11-10, geolocation gold);
- Hong Kong / Macau as their own entities (rule 5a, kept 2026-11-10).

---

## A. Principal actors (as a consequence of roles)

### P1. Support threshold: fixed or size-dependent — **APPROVED 2026-11-23: keep current size-dependent rule, provisional until the role model is evaluated**
1. `principals.required_support(n)`; weights `HEADLINE=1.0`, `LEAD=0.5` (`principals.py`).
2. Already size-dependent: 1.0 for 1–2 items, else `max(1.5, 0.25·n)`.
3. (a) keep; (b) fixed 1.5 (a 12-item Development needs 1.5, not 3); (c) role-based: a principal needs an *agent*
   or *target* role (§B) in at least one headline, with no count threshold; (d) (a) for agents, plus (c) for targets.
4. 458 headline-named actors miss today because they act in only one headline of a 3+-item Development. Examples: a
   Russian strike story with 8 items where "Ukraine" is the agent in one headline.
5. (b) and (c) raise recall on large Developments; (c) can admit incidental agents. Precision then depends on role
   quality, not counts.
6. More principals change Development topic keys (identity) and Situation coverage.
7. **(a) until the role model exists, then decide between (c) and (d) on the role gold.** No new threshold now.
8. Reversible (config and code).
9. Yes: entity gold rev 3 plus the role gold (§B).

### P2. Representative → state aggregation — **APPROVED 2026-11-23: representative and state stay separate; the state is principal only with institutional evidence**
1. `config/actors.yaml` `represents`; support aggregation per holder in `mark_principal_actors`.
2. A representative's mention keys to the state (Trump → United States), but principal flags and support are counted
   per surface holder. Support for "Russia" and "Kremlin" doesn't add up (43 cases). The rejected fix `5bb210e`
   summed them; precision fell on France/Macron, where the gold has France as secondary.
3. (a) keep per-holder counting; (b) sum per state (`5bb210e`, rejected); (c) keep **both** layers:
   - the representative stays a principal in its own right (Macron);
   - the state is principal only when it is also named or acted for **as an institution** (government, army,
     ministry), not merely through its leader;
   (d) count a representative for the state only for specified roles (head of state or government, foreign minister,
   armed forces) and only for the agent role.
4. Russia + Kremlin (D270), Ukraine + Zelensky + Zelenskyy, United States + Rubio; France next to Macron (gold D05).
5. (b) recall +2 / precision −1 on the gold; (c) protects the France convention; (d) is in between.
6. It decides whether Situation keys see "France" or "Macron". It interacts with OD6 (France is generic).
7. **(c), decided inside the topic/role spec (`SPEC.md` §4).** Keep both entities; the state needs institutional
   evidence.
8. Reversible.
9. Yes: role gold plus entity gold rev 3.

### P3. Does Gaza imply Palestine for actor purposes? — **APPROVED 2026-11-23: Gaza is a target/event location, never an actor standing for Palestine**
1. Normalisation, `represents` / aliases; place-vs-actor rejection (`principals.rejection`, `place`).
2. "Gaza" is a place: never an actor, never Palestine (339 misses of states named via a place, Gaza 33 of them).
3. (a) keep (Gaza is a place); (b) "Gaza" as an actor stands for Palestine (like "Kremlin" → Russia); (c) Gaza stands
   for Hamas when Hamas acts; (d) neither: the role model gives Gaza a *target location*, and Palestine is never
   inferred.
4. "Israeli strikes on Gaza", "Gaza ceasefire talks", "Gaza health ministry says".
5. (b) raises recall for `israel-palestine` and conflates territory with polity; (c) is politically loaded and often
   wrong; (d) is precise and keeps recall in the location layer.
6. `gaza-ceasefire` (Israel, Hamas) and `israel-palestine` membership; seeded scope already lists Palestine as a
   place.
7. **(d).** Gaza is a target or event location, not an actor. "Gaza health ministry" is an institution whose
   represented polity is a separate owner question (P3b).
8. Reversible.
9. Yes: location gold plus role gold.

### P4. Do targets count as principals? — **APPROVED 2026-11-23: target is a separate role; principal only where being targeted is structural (coercive or military action)**
1. `principals.TARGET_HEADS` / `TARGET_PREPS` and the entity gold convention.
2. Coercion targets ("sanctions on Russia", "strike on Iran") already count as parties in principal extraction (code
   comment line 62). The gold excludes some targets on purpose ("Russia warns NATO": NATO not principal); 61 such
   misses.
3. (a) targets are principals, as for coercion today; (b) targets are a separate role, never principal; (c) targets
   are principal only for coercive and military actions, not for statements or warnings.
4. "US sanctions on Iran" (Iran principal today), "Russia warns NATO" (NATO not), "Israel strikes Gaza" (place, P3).
5. (a) has the best Situation coverage, with noisier statements; (c) matches the gold's spirit.
6. Situation coverage: a sanctions target is half the actor pair.
7. **(c)**, stated in the role spec: agent and target are separate roles, and "principal" is derived.
8. Reversible.
9. Yes: role gold.

### P5. Support from merged Developments — **APPROVED 2026-11-23: largest compatible component only, once component evidence exists**
1. `aggregate` over all member items.
2. All members vote, including items from a merged-in different occurrence (297 noise misses, D49 Pope + summit).
3. (a) keep; (b) count only the largest compatible component when the Development is mixed (needs M1); (c) count
   only items compatible with the headline item.
4. D49, D542, D439, D447, D810 (126-case review).
5. (b) and (c) raise precision on merged Developments; they lose minority-component actors (correct, since those
   belong elsewhere).
6. Depends on M1. It changes principals only on mixed Developments.
7. **(b), after M1 is decided.**
8. Reversible.
9. Yes, with M1.

---

## B. Topic / event model with roles (`design/event-topic-model`, `SPEC.md`)

### T1. Topic families beyond the frozen v2 set — **APPROVED 2026-11-23: add out_of_scope; keep unknown for unresolved in-scope material; legal_justice deferred to a later amendment**
1. Taxonomy `config/development_types.yaml`; v2 family map (frozen).
2. No legal / justice, disaster, sport, health or markets type; those stories are `unknown`, which is the right call
   today.
3. (a) keep the taxonomy and abstain; (b) add `legal_justice` and `hazard` as event types (v2 would need an
   amendment); (c) add an explicit `out_of_scope` class (sport, markets, culture) distinct from `unknown`.
4. Christa Pike execution (legal), hurricanes (hazard), Olympics (sport, today mis-typed military).
5. (c) raises measured precision (fewer forced types) and separates "can't tell" from "not geopolitical".
6. v2 creation keys: `out_of_scope` never founds; `legal_justice` would need a contract amendment.
7. **(c) now; (b) `legal_justice` as a later contract amendment** if the owner wants legal storylines.
8. Reversible; (b) needs a v2 amendment before the window.
9. Yes: topic gold.

### T2. Intent: which intents yield an event type — **APPROVED 2026-11-23: intent always stored; threatened -> threat; called for -> significant_statement**
1. New `intent` field (spec §3).
2. Not modelled: "wants a truce" typed as ceasefire; "postpones election" as election.
3. (a) type only `occurred`; announced, threatened and called-for get type plus intent but count as non-occurrence;
   (b) all intents get the type, intent informational; (c) `threatened` maps to a separate `threat` type (exists),
   called-for to `significant_statement`.
4. The Pope calls for a truce; "elections postponed"; "Iran threatens to close Hormuz".
5. (a) gives the highest precision for occurrence-dependent uses; (c) keeps coverage.
6. v2 E3 (occurrence) and creation keys; ranking.
7. **(c) for type, plus the intent field always stored.** v2 creation uses occurrence intents only, as the contract
   already demands occurrence-led Developments.
8. Reversible.
9. Yes.

### T3. Abstention and confidence classes — **APPROVED 2026-11-23: downstream uses high and medium only; numeric boundaries calibrated on the frozen gold, not now**
1. Spec §6 (`confidence`, `abstain_reason`).
2. Rules output a type or `unknown`; no confidence.
3. Classes: `high` / `medium` / `low` / `abstain`. Alternatives for what downstream may use: (a) high only; (b) high +
   medium; (c) all except abstain.
4. A mixed-language Development with one typed headline (the 37%-precision failure mode).
5. (a) is precise with low coverage; (b) is the balanced default; (c) repeats the keyword failure.
6. What counts as "family known" in v2.
7. **(b)**, with the class boundaries set on the topic gold, never after seeing acceptance results.
8. Reversible.
9. Yes: boundaries frozen on the gold's development split.

### T4. Multilingual method — **APPROVED 2026-11-23: spaCy role parsing + multilingual embedding classifier first; local LLM only if that fails the bar; no API keys**
1. The model backend.
2. English-only rules; the LLM path needs an API key, which is banned on the VM.
3. (a) dependency-parse role extraction (spaCy en / es / it) plus multilingual embedding zero-shot for type; (b)
   (a) plus a small local LLM (Ollama) for intent, if VM RAM allows; (c) translate es/it → en, then English rules (no
   offline translator installed).
4. —
5. (b) gives the best intent quality, at the cost of RAM and latency; (a) is cheapest.
6. Warm-tier latency (about 5 min today), VM RAM (8 GB, daemon about 3 GB).
7. **(a) first, measured; (b) only if (a) misses the gold bar.** No API keys (Data & AI Team rule).
8. Reversible.
9. Yes.

### T5. Item → Development aggregation — **APPROVED 2026-11-23: confidence-weighted vote over report items only; derived Development text never votes back**
1. Spec §5.
2. Rules use every headline, and leads vote.
3. (a) headline-majority among compatible report items; (b) the headline of the earliest report item; (c) the
   confidence-weighted vote of report items, analysis items excluded.
4. Mixed Spanish/English Developments; roundups.
5. (c) is the most robust; (b) is brittle.
6. Interacts with M1 (mixed).
7. **(c).**
8. Reversible.
9. Yes.

---

## C. Event location and place roles (`design/event-location-model`, `SPEC.md`)

### L1. Several valid locations — **APPROVED 2026-11-23: one Development-level location; MULTI when supported locations span countries**
2. The map picks one point; v2 needs one event country or `NONE`.
3. (a) one event location, plus the others kept as role-tagged places; (b) multiple event locations, all in scope;
   (c) `NONE` when they disagree.
4. A strike on two cities in two countries; talks in Geneva about Ukraine.
5. (a) is precise and auditable.
6. v2 single-party and hazard keys (one country).
7. **(a), with `MULTI` as an explicit abstain reason when occurrence places span countries.**
8. Reversible. 9. Yes.

### L2. Target vs origin for attacks — `ALREADY FROZEN` (owner 2026-11-10: impact or target)
Kept. Origin is stored as `origin_location`. The only open sub-point is an attack with no stated target (launch
reported only); recommended `abstain_reason=NO_TARGET`.

### L3. Country-only events — **APPROVED 2026-11-23: country-only only for explicitly country-wide occurrences, never as a fallback**
3. (a) a country-level event location is valid ("sanctions on Iran" → Iran?); (b) only when the text states a
   country-wide occurrence (the iteration-2 `_COUNTRY_WIDE` lexicon); (c) never: `NONE`.
4. "Iran imposes curfew nationwide" vs "US sanctions Iran" (no occurrence place).
7. **(b) for occurrences. Coercive measures get `NONE` for location; their target is a role, not a place.**
8. Reversible. 9. Yes.

### L4. Disputed territories — **APPROVED 2026-11-23: disputed territories are first-class entities marked disputed**
3. (a) an own entity code (as for Hong Kong); (b) the de-facto administrator; (c) `NONE` with `DISPUTED`.
4. Jerusalem / East Jerusalem, Western Sahara, Falklands, Crimea, Dongsha (left unmapped on 11-11).
7. **(a): own entity with an explicit `disputed: true`, never silently assigned to a state.**
8. Reversible. 9. Yes.

### L5. Seas and regions — **APPROVED 2026-11-23: seas and regions are valid event locations, possibly without a country**
3. (a) a region or sea is a valid event location without a country; (b) map it to the nearest or most-mentioned
   coastal state; (c) `NONE`.
4. Black Sea, Strait of Hormuz, Red Sea attacks, "Middle East".
7. **(a)**: a sea or region location with `country=null`. v2 scopes may list seas (seeded metadata could add
   `black sea` to the war). Never mapped to a state.
8. Reversible. 9. Yes.

### L6. Containment source — **APPROVED 2026-11-23: containment-only place-alias table, never entering actor/entity resolution**
2. Containment comes from `geography.yaml`. Its aliases also feed actor and entity resolution, so the 93 parked
   aliases broke identity.
3. (a) a containment-only alias table, read only by location and scope; (b) keep one table and accept identity
   changes.
7. **(a).**
8. Reversible. 9. Identity gates only.

### L7. Evidence scope: headline / lead vs full text — **APPROVED 2026-11-23: headline and lead primary; body may support or disambiguate but never silently overrides them**
3. (a) headline + lead only; (b) + full text when fetched; (c) full text with dateline stripping.
4. Datelines ("KYIV, Nov 3 –") are reporting locations, not occurrences.
7. **(a) first; (c) as a measured variant.** Full text is uneven across sources.
8. Reversible. 9. Yes.

### L8. Minimum evidence for an event location — **APPROVED 2026-11-23: single-item: one clear headline-level item; multi-item: support from at least two items**
3. (a) one occurrence or target role in one report headline; (b) the same place (or a contained one) in at least two
   items; (c) (a) for single-item Developments, (b) otherwise.
5. (b) is precise, with lower coverage.
7. **(c)**, set on the location gold.
8. Reversible. 9. Yes.

---

## D. Mixed-Development flag

### M1. Definition — `OWNER DECISION REQUIRED` (measured; samples returned 2026-11-23; field name and definition not chosen)
1. A new read-only computation over stored Developments using the existing `development_segmentation.compatible_link`.
2. Not computed after cluster formation; late attachments are never re-checked.
3. Variants:
   - V1: at least 2 compatible components of any size;
   - V2: at least 2 components of at least 2 items each;
   - V3: V1 on report items only;
   - V4: V2 on report items only.
4. Counts on the 11-02 snapshot (all 1,198 Developments; `eval/mixed-flag-diagnostic` `e304a21`, read-only;
   identity hash unchanged before and after):

   | | V1 | V2 | V3 | V4 |
   |---|---|---|---|---|
   | all | 76 (6.3%) | 16 (1.3%) | 59 (4.9%) | 10 (0.8%) |
   | size 6+ | 47 (14.5%) | 15 (4.6%) | 40 (12.3%) | 9 (2.8%) |

   Known merged Developments (check only):
   - D49: flagged by all four variants;
   - D439: flagged by V3 and V4;
   - **D447, D542, D810: flagged by none.** Their items are linked as compatible pairwise even though the stories
     differ.

   Samples with headlines are in that branch's `REPORT.md`.
6. v2 E5 (`PENDING_MIXED`), P5 support, identity diagnostics. The flag never mutates a Development.
7. **The existing pairwise compatibility signal has low recall on known merges (1–2 of 5).** Options:
   - (a) store V4 now as a conservative `segmentation_split` evidence flag (0.8%), explicitly not "mixed";
   - (b) store nothing until the topic/role model gives a per-item action frame, then define "mixed" as report items
     with incompatible frames (different `action_type` + agent sets) inside one Development;
   - (c) both: (a) now as evidence, (b) as the real definition later.

   **Recommendation: (c).** Owner to read the V4 sample in `REPORT.md` before approving (a).
8. Reversible (a stored flag). 9. Identity gates must stay identical; the definition is checked against the known
   merged cases only as evidence.

---

## E. Malformed-Situation repair (dry run done, 2026-11-14; no writes)

### R1. Approve the five retirements found by the existing check — **APPROVED 2026-11-23 for 76 Developments; ON HOLD: the same five now hold 130 (re-approval needed)**
Fresh VM snapshot (sha256 `541029e7…`, code `03841eb`), `scripts/repair_situations.py` dry run:

| Situation | Reason | Developments detached |
|---|---|---|
| `donald-j-trump-united-states` (16) | actors collapse to `united states` | 7: 202, 351, 354, 754, 866, 918, 985 |
| `bukele-el-salvador-nayib-bukele` (24) | actors collapse to `bukele`, `el salvador` | 5: 501, 837, 1023, 1454, 1585 |
| `china-chinas-long-march` (25) | `Chinas Long March` no longer an actor | 18: 678, 845, 1278, 1417, 1456, 1458, 1497, 1565, 1592, 1599, 1602, 1603, 1613, 1646, 1666, 1708, 1710, 1761 |
| `emmanuel-macron-france-macron` (28) | actors collapse to `france`, `macron` | 20: 708, 973, 1199, 1249, 1333, 1334, 1452, 1499, 1512, 1519, 1554, 1561, 1580, 1604, 1615, 1628, 1677, 1685, 1762, 1764 |
| `democrat-united-states` (31) | `Democrat` no longer an actor | 26: 1084, 1174, 1189, 1228, 1268, 1269, 1282, 1283, 1285, 1288, 1296, 1300, 1352, 1357, 1381, 1460, 1462, 1477, 1482, 1520, 1524, 1544, 1571, 1581, 1607, 1725 |

**Mutation per Situation:**
- `status=closed`;
- slug renamed `<slug>--retired-<date>`;
- a note in `short_description`;
- its Developments set `situation_id=NULL`.

That's 76 Developments detached in total.

### R2. Detection gaps — **PARTIAL 2026-11-23: detector switched to the canonicaliser (dry run only); rachel-simon, russell-brand, china-iran returned for review**
- **Name-variant pairs aren't caught:** `elon-musk-musk` (17, active, 6), `christa-pike-pike` (12, 3),
  `javier-milei-milei` (22, 2), `machado-maria-corina-machado` (27, 2). The script validates with the plain
  normaliser, and the set-level variant collapse lives only in the Situation canonicaliser.
  - Alternatives: (a) make the script use `ActorCanonicalizer.keys` (a code change, dry run again); (b) an explicit
    owner list.
- **`rachel-simon` (18)** is never caught: single names stay actors by design. Only an explicit owner list retires it.
- **New since 11-02, for review:**
  - `russell-brand-united-kingdom` (33): a person plus his country, but not a state representative. Valid by current
    rules.
  - `china-iran-united-states` (32): plausible.
- **Recommendation:** (a) for the four name-variant pairs, and an explicit owner line for `rachel-simon`. Both via a
  second dry run.

### R3. Detach only, or detach + regroup — **APPROVED 2026-11-23: detach only, no regroup**
- (a) detach only: the Developments stay without a Situation;
- (b) `--regroup`: the normal grouping stage re-places those updated within the creation window. Most of these are
  older, so they would mostly stay unassigned anyway.

Today's grouper is the v1 rule known to over-admit. **Recommendation: (a) detach only.** Re-placement waits for v2.
Reversible from the verified backup that `--apply` writes first. No new evaluation needed; post-repair integrity
checks apply.
