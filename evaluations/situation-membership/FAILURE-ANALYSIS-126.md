# Failure analysis of today's Situation membership on the 126-case diagnostic set (2026-11-10)

**Status.** Diagnosis only. The 126-case subsample is a development / diagnostic set from now on (`LEARNINGS.md`).
Nothing here is a candidate rule fitted to these cases, and no case outcome below is a target for v2.

**Inputs.** Frozen owner labels (`evalset/subsample/`, `57fef39`), the label history (first answer per case = blind),
`evalset/key.json` (opened after the freeze, as the preregistration allows): `current_member` and
`grouper_explain_today` per case. `scopes.json` for founders. Counts use the **adjudicated** labels. The blind basis
is given where it differs and leads to the same classes.

## 1. Error counts

| | Adjudicated | Blind |
|---|---|---|
| False negatives (owner `MEMBER`, system rejects) | 8 | 11 |
| False positives (owner `NOT_MEMBER` / `OTHER_SITUATION` / `CONTEXT` / `SPILLOVER`, system admits) | 21 | 22 |
| Owner `AMBIGUOUS` (excluded) | 11 | 10 |

Adjudicated false positives by owner label: `OTHER_SITUATION` 9, `NOT_MEMBER` 7, `CONTEXT` 4, `SPILLOVER` 1.

## 2. Failure classes

Root-cause columns: **M** membership logic, **C** Situation creation / scope, **A** actor normalisation or principal
extraction, **S** Development segmentation, **H** missing state / history, **U** another upstream defect (event-type
classifier, geocoding, commentary detector). Cases can fall in several classes.

| Class | Cases | What happens | Root cause |
|---|---|---|---|
| **False negatives** | 8 (S027, S066, S132, S150, S158, S292, S344, S372) | All 8 are near-misses at **half coverage** (0.5) scoring 0.45–0.57, under the 0.6 join threshold. None is at full coverage. In most, the Situation's second party is in the story but not among the principals (Iran in an Italian headline, Palestine only as "West Bank", the RSF / SAF side in Sudan, NATO). | **M** (a weighted score: at half coverage actor overlap contributes 0.25, and similarity cannot lift it; there is no rule-based half-coverage path) + **A** (second party not extracted) + **U** (geocoding: "Laos" stored as `lagos`) |
| **Commentary admitted** | 4 of 5 owner-`CONTEXT` (S037, S149, S307, S377); 2 analysis pieces labelled otherwise (S343, S379) | `is_routine_commentary` is false for all of them. Commentary joins at full coverage like any report. | **M** (no commentary exclusion) + **U** (the commentary detector does not flag analysis headlines) |
| **Other-Situation confusion** | 9 (S003, S006, S054, S157, S166, S169, S319, S320, S357) | Actor-pair overlap admits stories whose topic belongs elsewhere: Western Sahara, Rubio on Venezuela, Patriots for Ukraine (war, not US–Russia), German sabotage threat, the Olympics. There is no "better Situation" comparison beyond the score margin. | **M** (no scope requirement, no better-Situation rule) + **C** (the Situation has no scope) |
| **No principals** | 3 (S033, S275, S343) | Admitted on mentioned entities through the fallback path (coverage 1.0 of mentioned entities). | **M** (fallback path; already withdrawn by owner ruling D3, not implemented) + **S** (S275 is a 36-report Development) |
| **Half coverage admitted** | 5 (S022, S149, S300, S319, S357) | One shared actor, often the generic "United States" or "Russia", plus centroid similarity. | **M** (no scope / place requirement at half coverage; owner ruling D4 not implemented) + **A** (generic state actor) |
| **Malformed Situation identity / scope** | founders labelled non-members: S006 (`javier-milei-milei`), S157 (`elon-musk-musk`), S169 (`christa-pike-pike`), S302 (`emmanuel-macron-france-macron`); unclear identity: S033 (`eritrea-ethiopia`) | The Situation's own founder is not a member of what the owner understands the Situation to be. Of 23 automatic Situations, **10** have a malformed key: 6 person-name self-pairs, `rachel-simon` (storm names), `china-chinas-long-march` (a rocket as an actor), `democrat-united-states` (party word), `donald-j-trump-united-states` (a person variant not mapped to the state). | **C** (actor-set identity only, no topic split) + **A** (name variants, non-actor tokens) |
| **Upstream Development defects** | merged Developments: S166 (D49), S274 (D542), S275 (D439), S157 (D447), and S273 (D810, `AMBIGUOUS`); mis-typed Developments: S320 (Olympics as `military_action`), S357 (Patriots as `resignation`), many `unknown/unknown` | A Development whose headline is one story and whose reports are another is judged on its pooled actors. Wrong event types make domain-based scope unreliable. | **S** + **U**; membership logic cannot repair these |
| **Missing state** | S273 (`AMBIGUOUS`; pending on confirmation) | Membership is decided once, when the Development is first grouped. Nothing re-checks it, and there is no pending state. | **H** |

## 3. Upstream defect or membership defect

| Defect | Where it lives | Fixable in the membership contract? |
|---|---|---|
| No scope requirement; weighted score decides | membership | yes: rule-based eligibility (E1–E5) |
| Half coverage under- and over-admits | membership | yes: owner ruling D4 as a rule, not a score |
| Fallback on mentioned entities | membership | yes: owner ruling D3 (X1) |
| Commentary joins as a member | membership + commentary detector | the rule yes (D2 / X2); detection quality is upstream and needs its own check |
| No better-Situation comparison | membership | yes: X6 / `OTHER_SITUATION` outcome |
| No pending state, no re-evaluation | missing state | yes, as a contract outcome; needs storage (owner decision) |
| Actor-pair identity, no topic split, no hazard key | Situation creation | yes: Situation identity section of the contract |
| Name variants, party / language / storm tokens as actors, incomplete person-to-state map | actor normalisation | **no**: upstream (`fix/actor-hygiene` lineage); the contract states the precondition |
| Second party not extracted (non-English, place-only references) | principal extraction | **no**: upstream |
| Merged Developments | Development segmentation | **no**: upstream; the contract only refuses to grant `MEMBER` to a flagged Development |
| Event-type / domain errors, `unknown` | classifier | **no**: upstream; the contract must not let an unreliable type alone satisfy or veto scope |
| Junk places (`lagos` for Laos, `charge`, `ademas`) | geocoding / place extraction | **no**: upstream (geolocation contract) |

## 4. What this does and does not show

- Today's runtime has had **none** of the 2026-11-02 owner rulings (D2–D6) implemented. All 10 negative seeds of
  `CONTRACT-V2.md` are still members. Much of the false-positive mass was already diagnosed on 11-02.
- The 11-02 seed groups are **not reliable gold**. The owner's labels make 3 of the 10 negative seeds `MEMBER` (D880,
  D1138, D34) and 1 `AMBIGUOUS` (D387), and 2 boundary seeds `MEMBER` (D12, D188). Seeds must not be reused as
  fixed v2 acceptance cases.
- New since 11-02: half-coverage **false negatives** at the score threshold; the size of the **malformed-identity**
  problem (10 of 23 automatic Situations); commentary detection missing every analysis piece in the set; merged
  Developments as a membership contaminant.
- Not shown: how any v2 rule would score. That needs a frozen candidate on a fresh holdout (`PREREGISTRATION-V2-R2.md`).
