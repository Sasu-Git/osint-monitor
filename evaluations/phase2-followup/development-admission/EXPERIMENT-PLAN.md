# Development admission (DA): pre-registration

Status: **PRE-REGISTERED DRAFT, NOT APPROVED, NOTHING MEASURED** (2026-10-27). The name E1 is taken by the closed
action-divergence experiment, so these variants are DA0–DA4. Amendments are appended, never edited in.
Architecture: `ARCHITECTURE.md`. Data: `DATASET-MANIFEST.md`. Gate: `ACCEPTANCE-GATE.md`.

## Hypothesis

Requiring every new member to be compatible with a frozen occurrence core of its Development (in addition to the
existing local link) stops relay growth and topic drift, which drive the giant and relay-signature Developments,
without losing genuine same-occurrence corroboration or late evidence.

## Variants (fixed now; no variant is added after results)

| Variant | Formation | Later attachment |
|---|---|---|
| **DA0** | current (connected component + 2 origins) | current: one compatible link to any member |
| **DA1** | current; core = kernel of the founders (founder-set fallback) | link to any member **and** `core_compatible` (C-sem quorum, C-head, C-place) |
| **DA2** | **cohesive kernel**: promote only the complete-link cross-origin kernel; other founders must pass `core_compatible` | as DA1 |
| **DA3** | current | k-support: compatible links to ≥ 2 members from ≥ 2 provenance origins (no core) |
| **DA4** | current; representative = the founder medoid (the founder report with the highest mean cosine to the other founders) | link to any member **and** C-sem (cosine ≥ 0.53), C-head and C-place against the medoid alone |

Every variant uses the existing thresholds (0.53, 0.5, 72 h, the guards). The only new constants are core size ≤ 5,
the majority quorum (DA1, DA2) and k = 2 (DA3). They are fixed here. The variants sit behind an off-by-default
experiment flag in an evaluation branch; production stays DA0.

## Harnesses

| | What | Data | Cost | When |
|---|---|---|---|---|
| **H1** | Existing frozen-window replay (`evaluations/identity/scripts/phase2_baseline.py` / `replay_current.py`: 4 × 12 h ticks per window, temporary database), run per variant | Phase 2 development windows, identity rev 4 development windows, clustering out-of-sample windows | light (48 h windows, stored embeddings) | after implementation approval; may run during the soak at below-normal priority |
| **H2** | **New long replay**: the snapshot's narrative items from 2026-10-04 to 2026-10-27, replayed in 12 h ticks through clustering, segmentation and admission, in a temporary database, with the stored embeddings and entities (no NLP, no collectors) | `snapshot-20261027-forensic.db` (relay set, giant label sample, large-occurrence candidates, small controls) | **heavy** (about 46 ticks × 5 variants) | **only after Candidate A's C2**, off-hours, below-normal priority |
| **H3** | Offline sequence check, no replay: apply each variant's admission test to the reconstructed attachment sequences (`../forensics/reconstruct.py` output) | the 8 giants | trivial | feasibility gate only (step 3) |

**H2 validity check.** Before any variant is scored, DA0 under H2 must reproduce the failure: at least 6 of the 8
giants' founder items end up in a Development with ≥ 100 members, and ≥ 90% of the small controls are reproduced
with identical membership. If not, the harness is not faithful. **Stop** and report; do not score variants on it.

## Procedure

0. **Freeze.** The dataset selections are frozen (`dataset/FREEZE.json`), and this plan, the gate and the manifest
   are committed with their hashes, before any variant runs.
1. **Owner labels.**
   - **L1:** which of the 38 founder items of the 8 giants form the founding occurrence.
   - **L2:** the 128 sampled giant members, each as SAME_AS_FOUNDER_OCCURRENCE / DIFFERENT / AMBIGUOUS.
   - **L3:** the 6 large-occurrence candidates × 8 members, the same labels against each one's founders, plus "is
     this Development one occurrence?".

   Blind review page as for the coverage review: variant outcomes are hidden, and labels are written per case with
   reviewer provenance. The labels are frozen with their hash before step 3.
2. **Characterise formation, no variant.** For each relay-set founder set, count whether a cross-origin complete-link
   report kernel exists, its size, and the founder items outside it. Report only.
3. **Feasibility gate (H3, no implementation).** On the 8 giants' reconstructed sequences, apply DA1's test with the
   kernel from the actual founders.
   - **F1:** the share of L2-DIFFERENT sampled members DA1 would reject must be ≥ 60%.
   - **F2:** the share of L2-SAME sampled members DA1 would reject must be ≤ 10%.

   If either fails, **stop**: record "core compatibility does not separate founder occurrence from relay members"
   and implement nothing.
4. **Implement the variants** behind the experiment flag, in an evaluation branch, with unit tests per condition.
   This step needs a separate owner approval.
5. **H1 runs:** all variants on all frozen development windows; defect set and gold rescoring.
6. **H2 runs (after C2):** the validity check, then all variants.
7. **Development decision** against `ACCEPTANCE-GATE.md`. Among passing variants, pick by this order: DA1, then DA4,
   then DA2, then DA3 (fewest new mechanisms first), unless a later variant passes and an earlier one does not.
8. **One-time holdout veto:** the Phase 2 holdout (2026-08-31), scored once for the chosen variant only.
9. **Report:** Situation impact on a snapshot copy (report only), the size and span distributions, and the
   provenance samples.

## Metrics (reported separately; no composite score)

- **Overmerge control:**
  - giants correctly split (L2 labels, per giant);
  - relay-signature Developments and their items (H2);
  - defect-set OVERMERGE fixed;
  - Phase 2 development DIFFERENT pairs kept together;
  - relation BLOCKED_BY_IDENTITY pairs whose two sides end in different Developments.
- **SAME preservation:**
  - continuity recall;
  - SAME kept apart;
  - **late attachment** (cross-tick SAME retained, i.e. ID stability, and the owner-verified late cases);
  - defect-set SAME controls;
  - L2-SAME and L3-SAME members kept;
  - clustering out-of-sample cross-source SAME.
- **Stability:**
  - ID stability;
  - Developments created per 1,000 items;
  - **unnecessary splits** (L2/L3-SAME members outside the founder's Development);
  - membership churn on the small controls.
- **Shape:**
  - size and span distributions;
  - maximum cosine distance of a member to its core;
  - relay depth (max hop) and graph diameter (H2).
- **Precision:**
  - false attachments (L2/L3-DIFFERENT kept);
  - mixed-occurrence Developments remaining (Phase 2 mixed-Development rate);
  - single-source Developments;
  - duplicate memberships.

## Exact replay

**Not needed to evaluate the variants.** The question is counterfactual: what each admission rule does. That needs
the same harness for DA0 and every variant (H1, H2), not a reproduction of production history. H2's validity check
guards against an unfaithful harness. Production's exact 10-minute tick sequence is not reproduced; the 12 h ticks
are the established identity-replay convention.

**Needed only to explain historical decisions** (which cluster each D398 attachment saw). That is forensic, outside
this experiment; the provenance proposal makes it unnecessary in future.

**H2 itself is CPU-heavy, so it runs only after C2.**

## Stop conditions

- The feasibility gate fails (step 3).
- The H2 validity check fails.
- No variant passes the development gate. Record it. **No tuning**, no case exceptions, no new variant in this round.
  A new round needs a new pre-registration.
- The holdout veto fails: reject. The holdout is not reused.
- Any variant requires a Situation-rule change, the cross-language stage, or weakens the single-source policy:
  out of scope, so stop.

## Out of scope

Repairing existing Developments; Situation rules; cross-language identity; a multilingual embedding; core
promotion; secondary safeguards (size, age, source-specific rules); production deployment.
