# Phase 2 holdout: one-time score and merge decision

Phase 2 (stable Development identity) was implemented against the frozen identity gold revision 2 and iterated on
the development windows only. The implementation was then frozen and the sealed holdout scored once
(`scripts/score_holdout.py`). No code changed after scoring began.

## Frozen implementation

| | |
|---|---|
| Branch | `feat/phase2-development-identity` |
| HEAD at freeze | `1f7748075379fdf091f11e16feb17c3ec287e7e7` (freeze record committed as `1ca37b5`) |
| Runtime vs the gated commit | identical (`git diff 5ed4b03 1f77480 -- osint_monitor config` is empty) |
| Config hash | `40645c947f673b180276170f8407b24a8a7563f609306eeb3d6c60cbe3785d81` |
| Models | en_core_web_lg, it_core_news_md, es_core_news_md (all available); embedding all-MiniLM-L6-v2 |
| Clustering benchmark manifest | `e667fad8f23d…` |
| Entity gold manifest | `4c7af75a7e03…` |
| Identity windows manifest | `9be66ed8b7aa…` |
| Identity gold | revision 2, `identity-gold.yaml` `cc98765b7506…`, manifest `87293792fba5…` |

Full record: `runs/phase2-holdout-freeze.json`. Result: `runs/phase2-holdout.json`. Trace:
`runs/phase2-holdout-traces/`.

**What Phase 2 changed:**

| Commit | Change |
|---|---|
| 34300c6 | Deterministic, order-independent persistence; one Development per item; continuation only through a compatible link to an existing member; single-source hold; report headlines as summaries |
| cd78d97 | Live blogs, roundups and analysis headlines are commentary, not corroboration |
| 5ed4b03 | Owner rule P7 (explicit and testable): within 24 h, no place conflict, and a specific shared anchor or the same cited source |

## Holdout metrics (2026-08-31, 30 cases, scored once)

| Metric | Result |
|---|---:|
| Continuity precision (kept together and SAME / kept together) | 7/8 (88%) |
| Continuity recall (kept together and SAME / SAME) | 7/10 (70%) |
| Split correctness (DIFFERENT pairs kept apart) | 19/20 (95%); 1 split failure |
| Merge correctness (SAME pairs kept together) | 7/10 (70%); 3 merge failures |
| ID stability (cross-tick SAME pairs retained) | 5/8 (63%) |
| Mixed-Development rate | 1/5 (20%) |
| Duplicate-membership rate | 0/12 (0%) |
| Single-source Developments | 0 |
| Roundup Developments / roundup source inflation / roundup summaries | 0 / 0 / 0 |
| Determinism (two replays) | identical |

## Development vs holdout

| Metric | Development set | Holdout set | Difference |
|---|---:|---:|---:|
| Continuity precision | 43/65 (66%) | 7/8 (88%) | +22 pp |
| Continuity recall | 43/58 (74%) | 7/10 (70%) | −4 pp |
| Split failures (of DIFFERENT) | 22/100 (22%) | 1/20 (5%) | −17 pp (better) |
| Merge failures (of SAME) | 15/58 (26%) | 3/10 (30%) | +4 pp |
| ID stability | 16/19 (84%) | 5/8 (63%) | −21 pp |
| Mixed Developments | 12/31 (39%) | 1/5 (20%) | −19 pp (better) |
| Duplicate membership | 0/110 | 0/12 | 0 |
| Single-source / roundup policy failures | 0 / 0 | 0 / 0 | 0 |

**Overfitting check:**
- **Continuity:** no drop. Holdout precision is higher, and recall is within one pair of the development rate.
- **Split / merge:** splits are better. Merges are 3 failures where the development rate predicts about 2.6, so
  no degradation.
- **ID stability:** lower, 5/8. The 3 failures are pairs whose items never formed a Development at all (H001,
  H018), or were cut by segmentation (H009). These are clustering-recall misses. **No retained identity broke.**
  With n = 8 the difference is not evidence of overfitting.
- **Mixed Developments:** 1 (H021), a whole-storyline overmerge, the largest remaining development-set class.
- **Policies:** no single-source Development, no roundup inflation, no duplicate membership.
- **Holdout size:** 30 cases, so every holdout rate has wide uncertainty. Nothing here is outside what the
  development set predicts.

## Case-level holdout failures

| Case | Gold | Current behaviour | Development IDs | Ticks | Items | Error class | Likely root cause |
|---|---|---|---|---|---|---|---|
| H001 | SAME | not grouped | – / – | t4 / t3 | "Ex-gang boss guilty of orchestrating 1996 murder of rapper…" / "What it was like inside court for Tupac Shakur's murder…" | missed continuation | courtroom account vs verdict report: below the link threshold, never clustered |
| H018 | SAME | not grouped | – / – | t4 / t3 | "Ex-gang boss guilty…" / "Watch: Moment Duane 'Keffe D' Davis is found guilty…" | missed continuation | same verdict, different framing; no Development formed |
| H009 | SAME | not grouped | – / – | t2 / t1 | "'She slipped out of my hand' – children missing after…" / "Rescuers search for 18 missing after boat capsizes off…" | segmentation interaction | survivor testimony vs report: headline guard cut; no specific anchor for P7 |
| H021 | DIFFERENT | kept together | D2 / D2 | t2 / t1 | "Orangutans in danger as wildfires blaze through Borneo" / "Malaysia's air quality turns hazardous as Indonesian wildfires burn" | whole-storyline overmerge | one wildfire storyline, distinct occurrences linked by similar language |

The owner marked H021 "same situation, natural calamity" and H009 / H020 as testimony vs report. Both point to
Phase 3 (storyline layer) and P8 (testimony as an evidence type), not to a Phase 2 defect.

## Regression results

| Gate | Result |
|---|---|
| `pytest -q` | 572 passed, 3 xfailed (Phase 2 tests: order independence, one Development per item, continuation needs a link, single-source hold, roundup does not corroborate, report summary, P7 conditions and anchors) |
| smoke | passed (NER OK, 3 events, migrations OK) |
| entity benchmark / gold audit | no unit changed / passed |
| frozen clustering benchmark (`--development`) | identical to main (except `generated_at`) |
| development segmentation benchmark | identical to main in every window after the P7 anchor-length rule (the first P7 version added one unrelated link; fixed on development data before the freeze) |
| Phase 1 replay | 2026-07-21 and 2026-08-07 PASS, membership facts unchanged |
| identity benchmark (development) | all metrics no worse than baseline; see the table above |
| duplicate-membership check | 0 in development and holdout; structurally prevented (an existing member never joins a second Development) |
| identity gold check / hashes | passed (checks 1-6); freeze hashes recorded |
| single-source first-class Developments | 0 (development and holdout; the snapshot's BBC `url#0/#1` pair is now held) |
| roundup false corroboration | 0 (development and holdout) |
| split lineage integrity | Phase 2 performs no split or merge. No Development is deleted, renamed or re-membered (no delete or reassignment path in clustering or identity), so there is no lineage to break. |
| deterministic replay | identical across two runs in all three development windows and the holdout |

## Downstream Situation impact

The read-only copy of the 2026-09-30 inventory snapshot (1,335 items) was replayed in 12 h ticks through the
pre-Phase-2 code (worktree at `4ad3def`, imports pinned to it) and through the frozen code
(`runs/phase2-situation-impact/`).

| | Before | After |
|---|---:|---:|
| Developments | 37 | 37 |
| Unchanged identity (same member set) | 36 | 36 |
| Situation memberships | 2 | 2 (identical: us-iran, gaza-ceasefire) |
| Situations and actor sets | 5 seeds | 5 seeds, actor sets unchanged |

**Developments whose identity changed: 1 removed and 1 new.** Situation memberships affected: none.
- **Removed:** "Stand-up comic released after being convicted of insulting Erdoğan" (BBC World twice, the
  `url#0/#1` pair). Single-source, now held below the Development layer.
- **New:** "SpaceX's Starship rocket reaches orbit for first time" (Al Jazeera + SCMP). Formed only with Phase 2
  code; the two headlines differ but share specific anchors (SpaceX, Starship). Consistent with P7.

No Situation meaning changed. Both changes are direct consequences of the Phase 2 rules.

## Merge recommendation

**PHASE 2 MERGE READY**

Every criterion holds:
- **The holdout generalizes:** precision and split behaviour are better than on the development set; recall
  and merges are within noise; the ID-stability gap is clustering recall, not broken identity.
- **No critical regression:** clustering, segmentation, entity, Phase 1, smoke and pytest gates are unchanged or
  green.
- **Development IDs are deterministic:** order-independent by construction, and identical across replays.
- **Duplicate membership is eliminated structurally.**
- **The single-source and roundup policies hold** on development and holdout.

**Known limits** (documented, not blockers):
- whole-storyline overmerge, 17 on the development set and 1 on the holdout;
- clustering-recall misses, where items never form a Development;
- cross-language recall, because the embedding model is English-only.

The first two are Phase 3 (storyline layer) and P8 (testimony) inputs. None is an identity-stability defect.

**Merge note:** Phase 2 sits on a branch stack (Phase 0 fixes → Phase 1 run ledger → identity gold → Phase 2).
Merging it brings migrations 4-5 to the next deployment. The live daemon (worktree at `a9edd18`) is untouched
until the planned redeploy after the Situation holdout report.
