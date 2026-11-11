# Track: multilingual event / topic modelling (opened 2026-11-11)

**Why.** Situation v2 cannot form Situations without a topic family. On the 2026-11-02 snapshot, 45.7% of all
Developments are `unknown`: English 36.5%, Spanish 79%, Italian 91%. Keyword rules cannot close this at acceptable
precision. Spanish/Italian lists reached 37%, then 77%, against a 90% bar
(`fix/v2-upstream-topic`, `evaluations/classification/unknown-20261111/`). The residual errors need **intent** (act
vs. call / threat / plan / hypothetical) and **speaker and action roles** (who acts, whether they are a political
actor), not more words.

**Owner constraints.**
- No more multilingual keyword lists.
- Structured extraction at the Development level.
- No Situation-membership tuning while this runs.

## Goal

Produce, per Development, a structured event representation that the v2 contract consumes:
- **event type** in the existing taxonomy, mapped to v2 topic families;
- **intent / modality:** occurred · announced / planned · called-for · threatened · hypothetical · denied;
- **actor roles:** agent, target or counterpart, speaker, and whether the speaker is a political or state actor;
- **confidence:** abstain (`unknown`) when the evidence is weak. A wrong type is worse than `unknown`.

## Constraints that shape the design

- **No API keys on the VM** (security rule). The existing `llm_classifier.py` / `hybrid.py` path needs a key, so it is
  out unless the owner decides otherwise. Any key must be coordinated with the Data & AI Team first.
- Candidates are therefore local and offline:
  - dependency-parse role extraction with the spaCy models already installed (en / es / it);
  - multilingual sentence-embedding or NLI zero-shot classification over the taxonomy;
  - optionally a small local model (Ollama, noted 11-09 as a later option), subject to VM RAM (8 GB, daemon ≈ 3 GB).
- Deterministic and replayable on snapshots. The stage cost must fit the warm tier.

## Evaluation (before any model choice is accepted)

1. **New gold set (owner-labelled, blind):** about 150 Developments from a recent VM snapshot, stratified by language
   (en / es / it) and by today's type (`unknown` oversampled). Labels: type, intent, agent / target / speaker. The
   126 Situation cases and the geolocation sample are excluded.
2. **Frozen before scoring:** the sample, the labels, the metrics:
   - type precision ≥ 0.90 on typed outputs (the bar already used in this cycle);
   - `unknown` rate per language;
   - intent accuracy;
   - role F1.
3. Candidates are compared on the same set. The winner then goes through the normal gates (entity benchmark, identity
   gold check, Phase 2 identity, pytest) and the v2 chronological replay as development evidence.

## First steps

1. Spec the representation (fields, enums, abstain rule) as `SPEC.md`; owner review.
2. Build the gold sample from a VM snapshot (backup API); labelling page reused from the Situation review.
3. Prototype 2–3 local candidates on a development split only.

Not started beyond this charter.
