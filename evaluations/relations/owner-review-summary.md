# Phase 3 relation gold: owner review summary (2026-10-07)

**What was reviewed.** All 142 development cases. The owner's verdicts and notes are authoritative. They are
frozen verbatim in `gold/owner-verdicts.snapshot.yaml`, with SHA-256 in `gold/manifest.yaml`.

**Holdout.** The sealed holdout was not opened (`check_sealed.py`: seal intact).

**The gold is not frozen yet.**
- 122 cases are settled.
- 16 cases carry an owner question, a conditional verdict, or a contradiction between label and note.
- 4 identity suspects need routing or discussion.
- Four taxonomy-policy questions (§6) decide how several of those cases read.

`gold/relation-gold.candidate.yaml` holds every case with its status. Only `settled` cases count below.

## 1. Counts

### By owner verdict

| Owner verdict | Cases |
|---|---:|
| `NO_RELATION` | 96 |
| `same_calamity_lifecycle` | 13 |
| `same_visit_or_summit` | 10 |
| `AMBIGUOUS` | 5 |
| `SAME_DEVELOPMENT_SUSPECTED` | 4 |
| `reaction_to` | 4 |
| `co_caused_with` | 4 |
| `caused_by` | 3 |
| `follow_up_to` | 2 |
| `same_attack_wave` | 1 |

### By status

| Status | Cases |
|---|---:|
| settled | 122 |
| pending owner discussion | 16 |
| identity suspect | 4 |

### Agreement with the blind draft

The owner changed the draft on 26 cases. 21 of them were draft `NO_RELATION` → a relation, `AMBIGUOUS` or an identity suspect. That direction matters: the
draft applied the taxonomy's explicit-evidence rule, and the owner's verdicts are often looser (§6, D3).

## 2. Confirmed positives per relation type

| Relation | Settled positives | Incl. pending | Distinct episodes (settled) |
|---|---:|---:|---|
| `same_calamity_lifecycle` | **13** | 13 | 3: Nepal/Tibet flood (7 pairs), DRC Ebola (5), Borneo wildfires/haze (1) |
| `same_visit_or_summit` | **8** | 10 | 7: Xi state visit, Trump's AI tech luncheon, Pope Leo in France (2 pairs), UK Labour conference, Macron in Spain, SCO summit, Netanyahu in the UAE |
| `same_attack_wave` | 1 | 1 | 1: Kyiv, Academy of Sciences strike |
| `reaction_to` | **1** | 4 | 1: R014, Araghchi's "doomsday war" after Trump rejects the Hormuz plan |
| `follow_up_to` | 0 | 2 | none |
| `caused_by` | 0 | 3 | none |
| `co_caused_with` | 0 | 4 | none |

## 3. Owner questions and answers

These cases are **not settled** until the owner confirms each one. Notes are quoted verbatim.

| Case | Owner verdict and note | Answer from the evidence | Needs owner |
|---|---|---|---|
| **R115** | `co_caused_with`. "I think this should be co_caused with: they're both commentary pieces on a broader topic which 'caused' both (prompt me if you disagree/agree and why)" | **Partly disagree.** A ("Tehran awaits official response as Trump rejects Hormuz plan", a live blog) names the cause; B ("Strait of Hormuz tensions linger as Iran and US move further from a deal") does not name a single event. `co_caused_with` needs both texts to name one identifiable cause. Here one text names a decision and the other names a state of affairs. Both are commentary on the same occurrence, Trump's rejection, so they are better expressed as two `commentary_on` links to that Development (D2) than as a relation between each other. | yes (D2) |
| **R132** | `co_caused_with`. "B does not respond to A but they are both caused by the rejection (ping me with your take on this as well)" | **Agree.** A ("…only negotiation can end conflict *after Trump rejects Hormuz deal*") and B ("Trump expects new Iran talks *despite rejecting deal offer*") both name the rejection explicitly, and neither responds to the other. This meets the taxonomy definition exactly. A is also a `reaction_to` the rejection, but that is a link to a third Development. | confirm |
| **R134** | `SAME_DEVELOPMENT_SUSPECTED`. "'only' the topic? it's literally HongKong retail, how are they not part of the same development? (let's dig on this, ping me for futher clarification or follow-up)" | **Two occurrences, one topic.** A is the government's monthly statistics release (retail sales +4.5% in July, a 15th month of growth). B is a property-agent feature on leasing (HSBC, fashion brands taking prime space at lower rents). The identity contract says the same topic is not the same Development. Both are SCMP-only, hence not surfaced (§5). Your wish to see them together fits a topic or storyline layer ("Hong Kong retail"), not identity. | yes |
| **R098** | `SAME_DEVELOPMENT_SUSPECTED`. "the DPRK made statements regarding its nuclear position, but specifically during its main UN General Assembly (UNGA) address." | **The evidence points to two different meetings.** A (UN News): the DPRK "told the UN General Assembly on Monday", i.e. its general-debate address. B (UN Press, two items) covers the General Assembly's **high-level meeting for the International Day for the Total Elimination of Nuclear Weapons**, with the Secretary-General's message. That is a separate plenary. Under the C064 precedent (a meeting record and the briefing in it = SAME), they would be one Development only if the DPRK spoke at B's meeting. B's text does not show that. | yes |
| **R008** | `caused_by` B->A. "Hong Kong tax break is a reaction to --> Singapore rival tax scheme" | **Your note describes `reaction_to`.** A's text: "should press ahead … *after Singapore unveiled a rival tax-exemption scheme*". Hong Kong financiers respond to Singapore's scheme, and B is about that scheme. Taxonomy precedence: a different actor responding → `reaction_to`. Proposed: `reaction_to`, A responds to B (A->B under the sheet's convention). | yes |
| **R127** | `caused_by` A->B. "different days but the rescue cited in B is directly caused by A" | **The text points elsewhere.** A is *new* Russian strikes that killed 6 people (22 Aug), "day after shopping complex attack". B is the rescue at the **mall** wreckage from "Friday's attack which killed 16". B's rescue follows the mall attack, which A only mentions as background. So the cause is a third occurrence. A and B are linked through that mall attack, not to each other. | yes |
| **R059** | `caused_by` A->B. "caused by the object of A's analysis. The analysis talks about the rejection, it is the rejection causing the spikes, not the analysis itself of course. This is obvious" | **Agree on the causality** ("Oil prices surge *after Trump rejects* Iran's plan"). But the cause is the rejection, a Development that is not in the pair. A is an analysis piece *about* it. The correct gold is `caused_by(oil-price surge → rejection)` plus `commentary_on(A → rejection)`. | yes (D2) |
| **R087** | `NO_RELATION`. "are we sure we want to flag this kind of things under no relation? if the remarks follow the summit, then it should be a followup, especially because it's about a very hot topic inside US-China relationship" | **Your note argues the opposite of your verdict.** B ("US, China list goods recommended for tariff cuts following Trump-Xi summit") is a concrete summit deliverable. Under the taxonomy it is `follow_up_to` the summit, or `same_visit_or_summit` if outcomes count as part of the bounded event (D4). A (Trump brushing off questions about Taiwan talk at the summit) is another summit thread. A↔B share only the summit. | yes |
| **R055** | `NO_RELATION`. "no relation although the reaction originated from Trump's remarks made at the visit, so I would also linger towards 'reaction_to'" | A (Southeast Asia's relief after the summit) is a regional reaction to the **summit**. B is Trump's Taiwan remarks. Your lean is `reaction_to` the summit, not to B. | yes |
| **R060** | `co_caused_with`. "No relation but the shared 'west bank' topic is a pretty hot one … Without settlers presence there would not be a need to deter violence" | Label and note disagree ("No relation"). The note describes a common background cause (settler presence) that is not one identifiable event. | yes |
| **R123** | `co_caused_with`. "okay yes separate acts but same development … I would put follow up or co_caused_with" | **Two acts:** the 2027 budget documents (+27% military spending) and Putin's decree adding 15,500 troops. Under the identity contract they are different Developments. Neither text names the other or a common cause, so `co_caused_with` lacks its explicit cause. Your reading: one policy of military expansion → storyline (D2/D3). | yes |
| **R029, R076** | `reaction_to` B->A. Notes: "…one would assume that activists were there precisely because of the old settlement re-establishment…" and "…It's not important that the reaction be to the exact event to create a causal link…" | **This is a policy question (D3).** B (Jewish activists' "protective presence") does not name A (the settlement re-establishment; soldiers throwing belongings). These are inferred reactions to settler activity in general. The taxonomy as written needs explicit reference. | yes (D3) |
| **R036, R105** | `reaction_to` / `same_visit_or_summit`. Notes: "without the speech there is no commentary" and "both are commentaries referred to the same address/event" | **Commentary policy (D2).** Elsewhere you marked commentary as no relation: R028 "commentary on what happened"; R026 `AMBIGUOUS`. | yes (D2) |
| **R002** | `follow_up_to` A->B. "Judge asks jurors to keep trying --> what are the jury's options; I think it is a follow-up or commentary on the empasse the jury is facing" | B is an explainer of the impasse in A. Under D2 this is `commentary_on(B → A)`. | yes (D1, D2) |
| **R056** | `follow_up_to` A->B. "not specifically linked as one thing, but it is pretty clear that the main objective is to hit Iran/ secure Israel" | Two US Treasury actions on the same day, with a shared objective and no textual link. Your reading is a shared policy aim → storyline/Situation, not a pairwise follow-up. | yes |
| **R005** | `same_visit_or_summit`. "If they are both analysis pieces then there is a relation, they're broadly referring to the same meeting or summit" | **Conditional.** A (BBC, "Xi got Trump's red carpet welcome – but not everything he wanted") is an analytical report. B (SCMP "answers your questions") is a reader Q&A. Both are analysis, so your condition is met. The verdict then stands if commentary counts (D2). | yes (D2) |

### Settled with an annotation

| Case | Owner note | Resolution |
|---|---|---|
| R045 | "even if same development, one lifecycle is fine. We can insert checkpoints for the most newsworthy events" | Settles the identity conflict raised earlier (H006/H016/H026). The relation stands. |
| R114 | "... if they share the DRC crisis then there is a link. It's the same lifecycle" | Condition met: B's coverage includes "Security Council LIVE: DRC peace deals fail to halt fighting *as Ebola deepens crisis*". |
| R124 | "yes, they were" | Confirms the Pope's AI remarks were made during the France tour. |
| R064 | "only 2 articles are about Macron in A … Rest should not be part of the development (should be part of 'housing crisis' on the 'Spain' area)" | **Confirmed.** System Development D9 mixes the Macron state visit (Clarín, France 24 Español) with Spain's housing crisis (BBC Mundo, Clarín). It is a mixed Development, a clustering error in the Spanish window. The relation holds for the Macron items. D9 is routed to identity review. |
| R066 | "I cannot see the body, I marked no relation" | **A source-coverage limit.** The Commission's Daily News feed item stores only its opening item; the body is truncated in the feed. The owner verdict is recorded as given on limited evidence. |

## 4. Identity-suspect cases

| Case | Owner | Evidence | Route |
|---|---|---|---|
| R012 | SAME suspected | BBC "Are Trump's US government funded ads illegal?" and France 24 "Public service announcement or Donald Trump propaganda?": one matter, two outlets | **Agree** → identity review. This is a clustering-recall miss: two independent outlets that should have formed one Development. |
| R138 | SAME suspected | System D10 (es/it: the White House AI luncheon and the America.gov launch) and France 24 (en) on the same luncheon | **Agree** → identity review. A cross-language split, because the embeddings are English-only. Post-soak fix 1 found the same pattern founding Situations. |
| R098 | SAME suspected | Two different General Assembly meetings (§3) | owner discussion |
| R134 | SAME suspected | A statistics release and a leasing feature (§3) | owner discussion |

## 5. Why sides were "not surfaced"

The 142 cases have 223 distinct sides. **181 were not surfaced as system Developments.**

- **178 are single-source.** The Phase 2 policy holds single-source items below the Development layer until
  independent evidence arrives. This is by design, not a failure.
  - Applies to R134 (SCMP only on both sides) and R098 A (UN News only).
- **3 are multi-source but not surfaced:**
  - `sx-423` (R114 B): UN News + UN Press are one institutional origin (the UN), so they count as one independent
    origin. The policy holds it back.
  - `us-china-state-dinner` (BBC + SCMP, R133 B) and `summit-trade-deliverables` (Al Jazeera + SCMP): two
    independent outlets that the clusterer did not join. These are **clustering-recall misses**, the known
    Phase 2 limitation (H001/H018 family).
- **R012 is an identity suspect, not an unsurfaced Development.** Its two outlets were never clustered. That is
  the same recall issue: the review sheet shows each side as single-source because the clusterer kept them apart.

## 6. Taxonomy-policy questions (decide before freezing)

| # | Question | Evidence in the verdicts | Recommendation |
|---|---|---|---|
| **D1** | **Direction convention.** The sheet defined `source -> target` (the follow-up/effect points to the original/cause). | `reaction_to` verdicts follow that (all four B->A). But every `follow_up_to` and `caused_by` arrow reads as **cause → effect**: R002, R056, R059 and R127 are A->B, where A causes or precedes B; R008 is B->A, with Singapore's scheme in B causing Hong Kong's response in A. | Store directed relations as named roles (`effect`, `cause`; `follower`, `original`; `reacting`, `stimulus`), not arrows. With that, the owner's intent is unambiguous in every directed case, and I can rewrite the five arrows mechanically after you confirm. |
| **D2** | **Is commentary or analysis a relation?** | Yes: R036, R105, R005 (conditional), R002, R115, R059. No: R028 ("commentary on what happened"); R026 `AMBIGUOUS`. | Add one explicit type, **`commentary_on`** (analysis → the occurrence it analyses). Don't overload `reaction_to`, `same_visit_or_summit` or `co_caused_with`. It also fits your earlier rule: "opinion only when it adds new information about a specific Development". |
| **D3** | **Explicit or inferred evidence** for `reaction_to` and `caused_by`. | R029 and R076 are inferred reactions; R060 and R123 are inferred common causes. The Phase 3 rule says "causal relations require explicit evidence". | Keep runtime relations explicit-only. Record inferred links as **storyline/Situation context** (settler violence, military expansion), not pairwise causal relations. Otherwise the explosion and false-causality risks return. |
| **D4** | **What `same_visit_or_summit` covers.** | The owner accepted a party conference (R048), a UN General Assembly day (R105) and a White House tech luncheon (R023). R087 and R034 raise summit outcomes. | Rename to **`same_convened_event`**: one bounded, scheduled gathering (visit, summit, conference, assembly session), with its announcement, sessions, side events and **stated outcomes**. Later implementation or policy is `follow_up_to`. |

## 7. Proposed Phase 3 runtime taxonomy (provisional until §6 is decided)

| Type | Decision | Rationale |
|---|---|---|
| `same_calamity_lifecycle` | **KEEP, implement** | 13 settled positives over 3 episodes. The owner sees this as the core grouping (calamity checkpoints: R045, R037). |
| `same_visit_or_summit` → `same_convened_event` | **KEEP, implement** (renamed, scope D4) | 8 settled positives over 7 distinct events; the clearest bounded-episode type. |
| `same_attack_wave` | **DEFER**; candidate merge into `same_calamity_lifecycle`'s episode model as a hostile-event episode | 1 positive. It overlaps the identity rule (C076: one overnight attack plus its side effects is one Development). |
| `reaction_to` | **DEFER until D2/D3**, then likely keep | 1 settled. After D2 (commentary out) and D1 (R008 relabelled), it could reach 2–3 explicit positives, which is still thin. A small targeted gold batch is needed, development windows only. |
| `commentary_on` | **ADD** (if D2 is accepted) | It absorbs about 6–8 owner positives currently spread across four types. It is directed and evidence-light, and suited to "surface commentary only when it adds information". |
| `follow_up_to` | **DEFER** | 0 settled, 2 contested. |
| `caused_by` | **DROP for runtime** | 0 settled. All three are either a reaction (R008), a link through a third Development (R059, R127), or contradicted by the text. False-causality risk outweighs value. |
| `co_caused_with` | **DROP for runtime** | 0 settled. 1 clean case (R132); the rest are inferred background causes (D3). |

**Net, if §6 is accepted:**
- implement now: `same_calamity_lifecycle`, `same_convened_event` and `commentary_on`;
- implement after a targeted gold batch: `reaction_to`;
- deferred or dropped: everything else.

## 8. Owner notes that are product requirements, not relation verdicts

Recorded for the backlog. They do not change any relation label.

| Area | Owner notes |
|---|---|
| **Suppress** | sports (R119); royal/celebrity gossip unless political (R032, R130) |
| **Digest handling** | "reading digest" articles aggregated weekly per macro-area (R011, R025); a drill-down research trigger on each story in a digest (R047); an EU-institutions bundle modelled on the Commission Daily News (R061) |
| **Research triggers** | IPO "clears hearing" over ~20M → company background brief (R051); Japan exiting versus investors entering China → "why" research (R121) |
| **Watch / surface** | lawsuits against Mag7 / big pharma (R070); **critical-minerals investments by G20 states should surface and found their own Situation, "prompt me to address after review" (R101): owner-requested follow-up** |
| **Birds-eye topics** | applied robotics, the AI race, semiconductors, critical raw materials (R126) |
| **Thematic umbrellas** | irregular migration (Greece, Morocco, Italy, Spain, Portugal, France, UK, Libya, Egypt; EU responses) (R057); policy "approaches" compared across macro-areas (R093); armed-force conduct scrutiny in conflicts (R040); maritime/climate policy (R035); China foreign policy (R003); US–China Taiwan (R007); summit "threads" (R016) |
| **Calamity lifecycle** | distinguish major events; checkpoints for the most newsworthy (R037, R045) |

## 9. Files

| File | Content |
|---|---|
| `gold/owner-verdicts.snapshot.yaml` | the owner's verdicts and notes, verbatim, frozen |
| `gold/relation-gold.candidate.yaml` | every case with owner label, owner direction, note, draft, status, open question, annotation |
| `gold/manifest.yaml` | counts, positives, SHA-256 of the snapshot, candidate and review inputs |
| `scripts/apply_owner_verdicts.py` | regenerates the candidate and manifest; the pending, identity and annotation lists live in it |

**Next step.** After the owner answers §3 and §6:

1. apply the answers as a candidate revision;
2. rewrite the directed arrows to named roles;
3. freeze `gold/relation-gold.yaml` with hashes;
4. only then implement the runtime types.

---

## 10. Resolution and freeze (2026-10-07, owner decisions)

### Locked taxonomy decisions

- **Named semantic roles, not arrows:**
  - `reaction_to`: reaction → trigger;
  - `follow_up_to`: follow-up → original;
  - `caused_by`: effect → cause;
  - `commentary_on`: commentary → subject.
- **`commentary_on`** joins the gold taxonomy. Its runtime is deferred: it is a content relation, not a
  world-state relation.
- **Evidence.** Runtime canonical relations are explicit-only. Inferred links are kept in the gold with
  `evidence: inferred` and `canonical: false`, for later Situation/assessment logic.
- **Rename.** `same_visit_or_summit` → **`same_convened_event`**: a bounded scheduled gathering and its distinct
  actions/outcomes.

### Case resolutions

| Case | Final | How |
|---|---|---|
| R132 | `co_caused_with` (explicit; common cause: Trump's rejection) | owner agrees |
| R115 | `NO_RELATION`; both sides `commentary_on` the rejection (external link) | owner agrees |
| R134 | `NO_RELATION` (different events, same topic) | owner agrees |
| R098 | `AMBIGUOUS`, not scored | owner: two events. Their relation was not assessed; candidate `same_convened_event` (same day, UN General Assembly) |
| R008 | `reaction_to`: reaction = A (HK financiers), trigger = B (Singapore scheme) | owner agrees |
| R127 | `NO_RELATION`; B `follow_up_to` the Friday mall attack (external) | owner: link to the third event |
| R059 | `NO_RELATION`; A `commentary_on`, B `caused_by` the rejection (external) | owner: link to the third event |
| R087 | `NO_RELATION`; B an outcome of the summit, A a later remark about it (external) | owner: link to the summit |
| R060 | `NO_RELATION` | owner: the note was a West Bank watchpoint |
| R123 | `follow_up_to` (follow-up = troop decree, original = budget), **inferred** | owner: follow-up or co-cause both fine |
| R029, R076 | `reaction_to`, **inferred** (non-canonical) | D3 |
| R056 | `follow_up_to`, **inferred** (non-canonical) | D3 |
| R002, R036 | `commentary_on` (commentary = B) | D2 |
| R005 | `commentary_on` (commentary = B, the Q&A; subject = A, the summit) | owner condition met; D2 |
| R105 | `commentary_on` (commentary = A; subject = B, UNGA Day Three) | D2 |
| R012, R138 | `SAME_DEVELOPMENT_SUSPECTED`, routed to identity review, not scored | evidence and owner agree |
| **R055** | **deferred for debate, excluded from the frozen gold** | owner leans `reaction_to`. Disputed: A was published at 08:06, before B's Taiwan remarks (09:43, "on Saturday"), and A reacts to the summit as a whole, so it cannot react to B. |

### Frozen gold (`gold/relation-gold.yaml`, revision 1)

141 cases (142 minus R055); **133 scored**.

| Label | Cases | Canonical (explicit) | Inferred |
|---|---:|---:|---:|
| `NO_RELATION` | 100 | – | – |
| `same_calamity_lifecycle` | 13 | 13 | 0 |
| `same_convened_event` | 8 | 8 | 0 |
| `commentary_on` | 4 | 4 | 0 |
| `reaction_to` | 4 | **2** (R008, R014) | 2 (R029, R076) |
| `follow_up_to` | 2 | 0 | 2 (R056, R123) |
| `same_attack_wave` | 1 | 1 | 0 |
| `co_caused_with` | 1 | 1 | 0 |
| `caused_by` | 0 | 0 | 0 |
| `AMBIGUOUS` | 6 (not scored) | – | – |
| `SAME_DEVELOPMENT_SUSPECTED` | 2 (not scored) | – | – |

Third-event links are recorded per case under `external_links` (not scored): R059, R087, R115, R127, R132.
SHA-256 of the gold, the verdict snapshot and the inputs are in `gold/manifest.yaml`. The sealed holdout is
untouched.

### Final Phase 3 runtime taxonomy

| Plan | Types |
|---|---|
| **Implement** | `same_calamity_lifecycle` (13 canonical positives, 3 episodes); `same_convened_event` (8 canonical, 7 events) |
| **Targeted batch first** | `reaction_to`: only 2 canonical positives |
| **Defer** | `same_attack_wave`, `follow_up_to`, `commentary_on` |
| **Drop from Phase 3 runtime** | `caused_by`, `co_caused_with` |
