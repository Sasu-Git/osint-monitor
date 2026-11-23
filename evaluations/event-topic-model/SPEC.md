# SPEC (FROZEN 2026-11-23, owner rulings applied): Development event representation — topic, action, intent and roles

**Status.** Frozen 2026-11-23 with the owner's P/T/L rulings (`docs/upstream/DECISIONS.md`). Nothing implemented yet. Changes after this point are dated amendments; amendments after the acceptance gold is frozen void that gold. Items marked APPROVED 2026-11-23 refer to
`docs/upstream/DECISIONS.md` on `design/upstream-representation` (`b3ed3ef`); none is chosen silently. No new
keyword rules are the primary answer to `unknown` (owner, 2026-11-11).

## 1. Output per Development

| Field | Type | Meaning |
|---|---|---|
| `topic_family` | enum: v2 families (`armed_conflict`, `security`, `diplomacy`, `economic`, `politics`, `hazard`) + `out_of_scope` (T1) + null | `ALREADY FROZEN` mapping from `action_type` (contract §1.1); `out_of_scope` pending T1 |
| `action_type` | enum: existing taxonomy (`config/development_types.yaml`), unchanged | What happened, e.g. `military_action`, `sanctions`, `summit` |
| `intent` | enum: `occurred` · `announced_planned` · `threatened` · `called_for` · `hypothetical` · `denied` · `reported_allegation` | Modality of the action (T2) |
| `agent` | list of actors (canonical key + surface + entity id) | Who performs the action |
| `target` | list of actors | Whom the action is directed at / affects as object |
| `speaker` | actor or null | Who says it (statements, claims); the speaker is not the agent unless they also act |
| `speaker_is_political` | bool or null | Speaker is a state, government, party, IGO or armed actor (vs celebrity, company, analyst) |
| `affected_party` | list of actors | Parties affected without being targeted (civilians of X, a third country's shipping) |
| `institutional_context` | list | The institution an actor acts through (UN Security Council, EU Council, NATO summit) |
| `confidence` | `high` · `medium` · `low` · `abstain` | Class boundaries set on the gold's development split (T3) |
| `abstain_reason` | enum: `NO_ACTION` · `OUT_OF_TAXONOMY` · `MIXED` · `CONFLICTING_ITEMS` · `LOW_EVIDENCE` · `LANGUAGE_UNSUPPORTED` | Why no type was given |

Per item, the same fields are produced first; §5 aggregates them to the Development.

## 2. Roles

- **Agent:** grammatical or semantic doer of the main action in the headline clause (subject of an active verb;
  `by`-agent of a passive; possessor of an action noun: "Russia's strike").
- **Target:** object of a coercive/military/legal action (direct object; `on/against` + action noun:
  "sanctions on Iran"). Whether targets count as principals: P4 (APPROVED 2026-11-23).
- **Speaker:** subject of a reporting or statement verb (says, warns, claims, denies, dice, afferma, advierte).
  A warning is speech; the speaker is not an agent of the warned action.
- **Counterpart:** the other party of a symmetric action (meeting, talks, agreement) — recorded as a second agent.
- **Place names are never agents.** A place in agent position ("Gaza says", "Kyiv strikes") resolves through the
  existing `represents` table only where already configured (Kyiv → Ukraine, `ALREADY FROZEN`); new place-for-polity
  readings (Gaza) are P3 (APPROVED 2026-11-23): never.

## 3. Intent

Intent comes from the clause's verb and modality markers (future, modal, conditional, "calls for", "threatens to",
"plans to", "denies", "accused of"), in all three languages, from the dependency parse — not from topic keywords.
Which intents yield an `action_type`: T2 (APPROVED 2026-11-23: type always, intent stored,
`threatened` → `threat`, `called_for` → `significant_statement`).

## 4. Representatives and represented entities

- A **representative** is a person or body configured in `actors.yaml` `represents` (head of state/government,
  foreign/defence minister, ministries, armed forces), plus the institution registry (`config/institutions.yaml`).
- A representative **acts for** its state when it is the agent or speaker of an action in an official capacity —
  determined by role (agent/speaker) and the configured mapping; never inferred for unconfigured persons.
- **Both are retained:** the record keeps the representative (Macron) and the represented entity (France) with the
  link `acts_for`.
- **Support aggregation** across aliases and representatives: P2 (APPROVED 2026-11-23). Approved (c):
  the representative counts as itself; the state counts as a principal only with institutional evidence (named as
  state/government/army, or an institution acting) — so France next to Macron stays secondary, as the entity gold
  encodes. Name variants of one person always aggregate (already deployed, set-level).
- **No new support threshold** is chosen here (P1 APPROVED 2026-11-23).

## 5. Item → Development aggregation

T5 (APPROVED 2026-11-23: confidence-weighted vote over report items only, analysis/rolling
excluded, within the largest compatible component when the Development is mixed — M1/P5).
`CONFLICTING_ITEMS` abstains when report items disagree on `action_type` with no majority.

## 6. Abstention and confidence

- Abstain rather than guess; a wrong type is worse than `unknown`.
- `out_of_scope` (sport, markets, culture, crime, health, obituaries) is a positive class, not an abstention (T1).
- Confidence classes and what downstream may consume: T3 (APPROVED 2026-11-23: high + medium).

## 7. Multilingual behaviour

- English, Spanish, Italian handled by the same role logic over each language's spaCy parse (`en_core_web_lg`,
  `es_core_news_md`, `it_core_news_md`, already deployed); verb and modality lexicons per language are small closed
  sets (reporting verbs, modal markers), not topic keyword lists.
- `action_type` from the role frame + a multilingual sentence-embedding classifier over the taxonomy (T4); no
  translation step; no API keys on the VM.
- Item language from the source's configured language first, detector second (short Spanish headlines are
  mis-detected as English).
- Other languages: `abstain_reason=LANGUAGE_UNSUPPORTED`.

## 8. Evaluation (before any implementation is accepted)

1. Spec approved, decisions T1–T5, P1–P5 taken.
2. New owner-labelled gold, blind: ~150 Developments from a fresh VM snapshot, stratified en/es/it, `unknown`
   oversampled; excludes the 126 Situation cases and the geolocation samples. Labels: `action_type`, `intent`, agent,
   target, speaker. Split: development (for confidence boundaries) / acceptance (scored once).
3. Frozen before scoring: sample, labels, metrics — type precision on typed outputs (bar from this cycle: ≥ 0.90,
   **OPEN: owner to confirm the bar before scoring**), `unknown` rate per language, intent accuracy, role F1.
4. Then normal gates (entity benchmark, identity gold check, Phase 2 identity, pytest) and the v2 chronological
   replay as development evidence. Evaluation runs via `eval-worker`.
