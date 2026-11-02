# Development-admission owner labels: frozen 2026-11-02 (summary only)

**Labels only.** No admission variant, DA1 compatibility test or H3 feasibility check has been applied; H3 needs a
separate approval. The plan and its amendments are unchanged (hashes in `FREEZE-LABELLING.json`, all re-verified).

| | |
|---|---|
| Label file | `owner-labels.yaml`, sha256 `1a66ec001afc3fb31548c9271f56e44ed9dcf9183ec1b4e248d187df0ed0110b` |
| Freeze record | `LABELS-FREEZE.json` (frozen 2026-11-02 15:01:36Z, written by `labels_tool.py freeze`) |
| Reviewer | owner (217 of 217) |
| Labelling period | 2026-10-27 17:09Z to 2026-11-02 14:51Z (completion) |
| Validation | `labels_tool.py validate`: 217 of 217 labelled, 0 problems. One final verdict per case, valid values only, reviewer recorded, no label for an unknown case. All 12 frozen inputs re-hashed and unchanged: plan, scripts, cases, key, dataset inputs |
| Revised verdicts | 10 cases changed their verdict before the final one. Every earlier verdict is kept in that case's `history`, same reviewer; nothing was overwritten silently |
| Notes | 2 cases carry an owner note |

## Counts

| Set | Cases | SAME_OCCURRENCE | DIFFERENT_OCCURRENCE | AMBIGUOUS |
|---|---|---|---|---|
| L1 (giant founders) | 30 | 2 | 26 | 2 |
| L2 (giant sampled members, Q1–Q4) | 128 | 9 | 117 | 2 |
| L2b (giant set-level, reported, not gated) | 8 | 1 | 7 | 0 |
| L3a (large-occurrence members) | 45 | 4 | 41 | 0 |
| L3b (large-occurrence set-level) | 6 | 0 | 6 | 0 |
| **Total** | **217** | **16** | **197** | **4** |

**L2 by quartile.**

| Quartile | SAME | DIFFERENT | AMBIGUOUS |
|---|---|---|---|
| Q1 | 2 | 30 | 0 |
| Q2 | 3 | 28 | 1 |
| Q3 | 0 | 32 | 0 |
| Q4 | 4 | 27 | 1 |

## Control classes

- **G11 (large-occurrence controls) is not applicable.** All six L3b set-level cases are DIFFERENT_OCCURRENCE: the
  owner labelled no large-occurrence candidate as one occurrence. The acceptance gate provides for exactly this case
  ("If no candidate is labelled one occurrence, G11 is not applicable and is reported so").
- **Classes that are not empty:** SAME members exist in L1 (2), L2 (9) and L3a (4). The H3 F2 denominator (owner
  SAME members) is therefore small, 16 in total. That is stated now, before any scoring.
- **Not part of this label set:**
  - the small controls (G14) are an H2 stability metric;
  - the defect-set SAME controls (G8) are a frozen H1 set.
