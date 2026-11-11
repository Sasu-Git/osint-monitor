# Situation v2 candidate: chronological replay after the upstream hardening cycle (2026-11-11)

**Development evidence on the 126-case diagnostic set, not acceptance.** No rule changed after any result. The v2
contract (`bf57ed7`) is unchanged except amendment 1 (seeded scope metadata, `bbc9bba`).

## What is in the candidate (`feat/situation-membership-v2-candidate`)

| Upstream change | Gate | In the primary replay |
|---|---|---|
| Actor normalisation `b695aa0` | passed (2 documented deviations) | yes |
| Seeded scope metadata v1 (track 5) | curated, contract amendment 1 | yes |
| Place containment, 86 parent entries (`fix/v2-upstream-places` `aa1d5a2`/`1735756`) | passed every gate | yes |
| Place aliases (93) | **failed** identity (aliases also feed actor and entity resolution) | no, parked |
| Principal support per actor (`fix/v2-upstream-principals` `5bb210e`) | **failed** the frozen gate (benchmark precision 20/25 → 22/28; 4 unlisted changes) | sensitivity branch only |
| Spanish/Italian topic rules (`fix/v2-upstream-topic` `39bb7d0`) | **failed** precision (37%, then 77% vs ≥ 90%) | no |
| Single-party creation (OD1) and full chronological creation (track 6, 7) | 10 unit tests | yes |

## Result (frozen metric code; blind / final labels)

| | Runtime | Founder-only replay | Chronological, interim | **Chronological, final** |
|---|---|---|---|---|
| MEMBER recall | 47/58 · 48/56 | 9/58 · 10/56 | 15/58 · 17/56 | **18/58 · 20/56** |
| MEMBER precision | 47/69 · 48/69 | 9/12 · 10/12 | 15/21 · 17/21 | **18/24 · 20/24** |
| NOT_MEMBER rejected | 0.75 · 0.71 | 1.0 · 1.0 | 0.96 · 1.0 | **0.96 · 1.0** |
| positive seeds lost | 0 | 6 | 4 | **2** |

The sensitivity branch (`exp/situation-v2-sensitivity-principals`, with the principals fix) gives identical case
outcomes.

## Remaining failures (final labels: 36 missed members, 4 wrong admissions)

| Class | Cases | Root cause |
|---|---|---|
| No v2 counterpart Situation was ever created | 21 | Creation starves. Across 1,198 Developments, v2 creates 12 Situations against 23 automatic Situations at runtime. Topic `unknown` on 544 (45%) blocks the actor and single-party keys (OD4). No event country on 696 (58%) blocks single-party and hazard keys. No principals on 302 (25%) |
| Widely shared actor only | 6 (4 seeded) | the OD6 strong match needs family plus an in-scope place not in the generic party's country; those Developments have neither (unknown family or no place) |
| Other rule rejections | 9 | no shared actors (2), no scope signal (2), off-scope family (2), low coverage (1), assigned elsewhere (1), pending on a hedge word (1) |
| Wrong admissions | 4 | S166 merged Development (no `mixed` flag on `main`); S307 and S377 commentary with report-style headlines; S320 Olympics typed `military_action` (classifier) |

## Verdict

**Not credible enough to freeze for the fresh holdout.** The membership rules are precise: 20 of 24 admitted are
owner members, and 2 of the 4 wrong admissions come from upstream classifiers. But recall is 36% against 86% for
today's runtime. That would fail the OD8 recall gate (≥ 0.90) and the no-worse-than-baseline veto by a wide margin.

The binding constraint is no longer membership logic. It is upstream inputs that v2's identity rules depend on:
- **Topic family:** 45% unknown. Keyword rules can't fix it at acceptable precision; it needs intent and speaker-role
  modelling.
- **Event country:** 58% missing. It needs the upstream event-location / place-role track that geolocation iteration 3
  pointed to.
- **Principals:** 25% without any.
