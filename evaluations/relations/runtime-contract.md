# Phase 3 runtime relation contract (locked 2026-10-09)

Locks the runtime subset of `taxonomy.md` (revision 1) for implementation. The code form is
`osint_monitor/processors/development_relations.py`; `tests/test_development_relations.py` checks the code against
this taxonomy and against the gold manifest's `runtime_taxonomy`. Changing either needs an owner decision and a new
revision of this file.

## Types

| Type | Kind | Stored as | Canonical evidence |
|---|---|---|---|
| `same_calamity_lifecycle` | symmetric | lower Development ID → higher | the same hazard event (storm, quake, flood episode, outbreak) and an overlapping area, stated in both |
| `same_convened_event` | symmetric | lower → higher | the same bounded gathering (visit, summit, conference, session): participants, dates, venue |
| `reaction_to` | directed | **reaction → trigger** | the reaction names the trigger occurrence or refers to it unambiguously |

Not stored at runtime: `follow_up_to`, `commentary_on`, `same_attack_wave` (deferred); `caused_by`,
`co_caused_with` (dropped from the Phase 3 runtime). They remain gold labels.

## Rules

1. **Endpoints are Development IDs.** Both ends of a relation are `events.id`. No free-text endpoint exists in the
   schema. A link whose other end has no Development (for example, a reaction to an occurrence the system never
   surfaced) is not stored.
2. **Explicit-only.** `status = accepted` requires `evidence_kind = explicit` and cited evidence: member items of
   each side and the text span. `inferred` links are never accepted at runtime.
3. **Candidates are not relations.** `status = candidate` records a proposal for the classifier; it carries no
   claim, is never shown as a relation, and is not counted as one.
4. **Two distinct Developments.** A relation between one Development and itself is refused; a suspected identity
   goes to identity review.
5. **No side effects.** A relation never merges or splits Developments and never changes Situation membership.
6. **Never sufficient alone:** shared actors (including broad bilateral pairs), a shared place, temporal proximity,
   the same storyline or Situation, the same topic, high text similarity. These may propose a candidate; they
   never accept one.
7. **One primary label per pair**, by the taxonomy's precedence: episode types, then `reaction_to`.

## Schema (migration 7)

`development_relations`: `relation_type`, `source_event_id`, `target_event_id` (both `events.id`, distinct),
`status` (candidate | accepted | rejected), `evidence_kind` (explicit | inferred | none), `evidence` (JSON list of
`{item_id, side, cue, text}`, items must be members of that side), `method` (rule or model and version),
`created_at` / `created_run_id`, `updated_at` / `updated_run_id`. Unique per (type, source, target); index on
target.

## Scoring (gold revision 2)

Per type: precision and recall on canonical positives; direction accuracy for `reaction_to`; false-positive rate per
hard-negative family; unsupported relation count. `AMBIGUOUS` and `SAME_DEVELOPMENT_SUSPECTED` are reported
separately. `BLOCKED_BY_IDENTITY` pairs (both sides in one system Development) count against end-to-end coverage,
not against classifier precision or recall. Development and Situation regression must be zero.
