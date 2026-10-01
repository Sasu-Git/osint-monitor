# Owner review of the identity gold: corrections, notes and feature proposals

The owner reviewed all 189 cases in the blind review page; the gold is frozen as revision 1
(`gold/manifest.yaml`).

**Labels.** Every label is the owner's verdict: 64 SAME, 124 DIFFERENT, 1 AMBIGUOUS, of which 9 corrected the
draft. The development split has 54 / 104 / 1 and the holdout 10 / 20.

**Notes.** The owner wrote 46 notes. They are stored verbatim in `gold/identity-gold.yaml`. No label was changed
to fit a note.

## 1. Corrections to the draft (9)

| Case | Draft → owner | Pattern |
|---|---|---|
| A009, C005 | AMBIGUOUS → SAME | same strike / same UN observance, reported with different detail |
| C018, C082 | AMBIGUOUS → SAME | appointment + the customary audience with the King = one institutional act |
| A017, H023, H029 | AMBIGUOUS → DIFFERENT | distinct actions inside one crisis (vaccine trial vs spread warning; return home vs rescue) |
| C029 | DIFFERENT → SAME | a roundup headline from the same outlet, an hour apart, carrying the same occurrence (record budget + decree) |
| A028 | DIFFERENT → AMBIGUOUS | depends on whether the settlement re-establishment displaced the same families |

**What the corrections show:**
- 7 of the 9 resolve draft AMBIGUOUS cases using domain knowledge the text alone did not give, for example
  institutional formality.
- The owner's Development boundary is **strict**: distinct actions within one crisis remain different
  Developments.

## 2. Verdicts whose notes read like "same Development" (confirm or keep)

These are frozen as labelled (DIFFERENT). The notes suggest the owner may mean a grouping *above* the
Development (section 3) rather than identity. Please confirm. If any should be SAME, that becomes gold
revision 2.

| Case | Verdict | Note (verbatim, shortened) |
|---|---|---|
| C064 | DIFFERENT | "basically same news, should bundle together and add to the development" |
| C034 | DIFFERENT | "should be bundled together, it's literally the accompanying Q&A" |
| C103 | DIFFERENT | "different but should be bundled together into one piece of news" |
| C076 | DIFFERENT | "same attack though, should be clustered" |

## 3. The main finding: a grouping layer between Development and Situation

About 30 notes say, in different words, "different Developments, but they belong together". That middle layer
does not exist today: a Development is one occurrence, and a Situation is a broad actor-set bucket (audit S2).
The notes describe **typed groupings with predictable internal structure**:

| Type | Owner cases | Structure the owner describes |
|---|---|---|
| **Natural calamity** | A021, A022, A032, H003, H006, H008, H015, H020, H021, H024, H026 | Geographically limited, with a "relatively predictable chain of events: warnings, evacuations if possible, the actual event, rescue and death toll, then cost assessment" (H006). It should be "bundled and update silently until rescue and death toll stabilise" (A032). |
| **Official act package** | C034, C103, C048 | A proposal plus its Q&A, factsheet and the day's "Daily News" mention: one piece of news from one institution |
| **Summit / visit** | B005, B008, C064 | One visit or meeting. Surface "only the juice" (the substantive outcome); colour pieces are background. Before/after reports matter only if the outcome contradicts the stated aim. |
| **Attack wave** | C076 | One overnight attack and its side effects (a drone crash in Moldova) |
| **Action → reaction / co-causation** | A006, A013, A023, C094 | One Development occurs "in response to or because of the other" |
| **Same situation, distinct aspect** | A017, H016, H029, C016, C032, C039, C105, C115 | The broader Situation level, e.g. "maritime policies" (C032) |

**Recommendation.** This is the most important input for **Phase 3 (Situation / state semantics)**, and it
should be designed there, not inside Development identity.
- The identity gold stays strict, as the owner labelled it. The Phase 2 contract stays "one Development = one
  occurrence".
- Phase 3 should model a typed **storyline** (or episode) between Development and Situation, with explicit
  membership records (S2) and its own owner-reviewed gold.
- The notes above, and the 64/124 identity labels, are a ready seed for that gold.

## 4. Feature proposals from the notes

**Placement rules.** Each proposal is placed on the agreed sequence (Phases 0 → 8). None is implemented here, and
none may change runtime behaviour before its phase.

| # | Proposal | Owner cases | What it needs | Phase | Notes and constraints |
|---|---|---|---|---|---|
| P1 | **Interest / relevance gating.** Sports and sports business never surface. Local or private stories surface only if internationally relevant. Opinion only when it adds new information about a specific Development. | A003, A005, C044, H002 (and entity review D09) | an owner interest profile; a relevance class per Development (the classifier already has `event_domain`) | ranking, after Phase 4 | Gating is about **surfacing**: evidence is still stored and counted. Needs a small ranking gold. |
| P2 | **Typed storyline layer** (section 3) | ~30 cases | storyline table, membership with reasons and time, type-specific templates | **Phase 3** | Core design input. Keep Development strict. |
| P3 | **Calamity lifecycle with quiet updates.** Bundle, then update silently until the death toll and rescue stabilise; then cost assessment. | A032, H006, H021 | storyline type "disaster" with phase states; change history to detect stabilisation | Phases 3-5 | Silent updates depend on Phase 4 change history and Phase 5 notification state. |
| P4 | **Official act packages and watch rules.** Group release + Q&A + factsheet + daily-news mention. Vet the EU Critical Communication System proposal "carefully". | C034, C103, C048 | same institutional publisher, same act title, same day; owner watchlist (topic or act) | package: Phase 3; watchlist: Phase 5 | Deterministic, provenance-friendly. The watchlist is user state (follow/mute family). |
| P5 | **Meeting / visit outcome extraction.** Surface the substantive outcome. Before/after only when the outcome contradicts the stated aim (e.g. a public altercation). | B005, B008, C064 | storyline type "meeting"; outcome vs stated-aim fields; summary generation | Phase 3 (grouping), Phase 8 (summaries) | Outcome text from an LLM must carry provenance and never become canonical (invariants 27-28). |
| P6 | **Action → reaction links and "weight of the news" inquiry.** Explain a Development's weight from reactions by media, institutions and known accounts on X and Instagram. | A006, A023, C094 | typed links between Developments (`reaction_to`, `response_to`, `caused_by`) with evidence; a reaction-collection task | links: Phase 4; inquiry: Phases 6-8 | **X and Instagram are not collected today.** Adding them is source expansion with terms-of-service, authentication and rate-limit constraints; it needs a separate decision. |
| P7 | **Identity verification for doubtful pairs.** When in doubt, check for a common cited source, location and actors before deciding. | A028 | evidence checks run on a candidate pair (cited sources, places, actors), recorded as reasons | **Phase 2** | Owner-provided rule. It fits the deterministic, explainable matching Phase 2 needs. The benchmark's AMBIGUOUS case (A028) is excluded from scoring. |
| P8 | **Testimony vs report.** Separate eyewitness testimony from event reporting, clearly labelled, especially in conflicts and disasters. | H020, C079 | an evidence-type class per item (report, testimony, commentary, official release) persisted with provenance | Phase 2 (provenance role), used in Phase 3 | Affects corroboration: testimony is evidence of experience, not independent confirmation of the whole event. Needs a small gold. |
| P9 | **Research triggers: "why / why now" and "what led here".** For leader announcements (C002, and D18 earlier), and for social conflicts: look for commentary from both sides on the contributing factors and policies (C035). | C002, C035 | deterministic trigger rules over Developments; research tasks with sourced output | Phases 6-8 | Output is an assessment with sources; persisted LLM output needs provenance. |
| P10 | **Framing / spin review.** Recurring review of how outlets frame a topic (e.g. Italy–Egypt "cold relations"). | C090 | framing labels per item; recurring report | after Phase 4 | Fits the existing narrative-tracking direction. Needs labelled examples before any automation. |
| P11 | **Roundup novelty.** From "in brief" items, surface only parts not already reported by other sources. | C080 | roundup segmentation (deferred earlier) plus a seen-before check against existing Developments | Phase 2 or 3 | Roundup splitting was explicitly deferred; this defines its acceptance criterion. |
| P12 | **Question vetting and generation.** Vet official Q&A questions and propose further questions to attach to threads. | C034 | LLM question generation attached to storylines | Phase 8 | Generated content is labelled, provenance-tracked and never canonical. |

## 5. Consequences for the plan

1. **The Phase 2 gate is unblocked.** The identity gold is owner-reviewed and frozen. Proposal P7 is an owner rule
   Phase 2 may use. The holdout (30 cases) stays untouched until Phase 2 development ends.
2. **Phase 3 needs a storyline / Situation gold** built from section 3. The same protocol applies: freeze windows,
   draft blind, owner review, freeze.
3. **Confirm section 2.** Confirm or correct the 4 cases. Only if any changes is a revision 2 of the identity gold
   needed.
4. **Decide separately on X and Instagram (P6).** They are new sources with legal and ToS implications, not part of
   any current phase.
