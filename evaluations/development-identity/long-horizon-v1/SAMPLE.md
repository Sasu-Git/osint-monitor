# Long-horizon identity sample (DRAFT, built at the proposed size)

Governing spec: `SPEC.md` (DRAFT, not frozen). Nothing is labelled, scored or run through any model or guard. The sample is a
proposal until the owner resolves SPEC section 12 and starts labelling; after that, sample and case files change only by a dated amendment.

Snapshot: `data/eval/upstream-gold-20261123/gold-snap.db` (VM snapshot 2026-11-23 09:43Z), sha256
`7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c` (verified before use; opened read-only, backup-API copy in a temp dir,
chain depth from the exact runtime pair test `development_segmentation.compatible_link`). Seed `20261124`. Script `build_sample.py`
(sha256 in `manifest.json`). Run with the main `.venv` python, `HF_HUB_OFFLINE=1`, `PYTHONPATH=<worktree>`; about 12 minutes.

## Frame

| Step | Developments |
|---|---|
| In snapshot (>= 3 members with a publication time) | 1,274 |
| minus upstream topic/location gold Developments (all ids > 1341; 263 listed, 167 have >= 3 members here) | -167 |
| minus Developments containing an item of the existing identity gold | -14 |
| Eligible | 1,093 |

## Strata and counts

| Stratum | Pool | Developments drawn | Cases | Gap bands of the cases |
|---|---|---|---|---|
| A_SHORT (12 h <= span < 48 h) | 513 | 30 | 30 | G1 30 |
| B_CONTINUOUS_MULTIDAY | 94 | 30 | 30 | G2 30 |
| C_RECURRING_GAP | 75 | 15 | 28 | G2 26, G3 2 |
| D_DRIFT_MULTIDAY | 86 | 15 | 25 | G2 25 |
| E_CHAIN_FAILURE (span >= 7 d, depth >= 8; D398 pinned) | 32 | 14 | 44 | G2 20, G3 21, G4 3 |
| **Total** | 800 | **104** | **157** | G1 30, G2 101, G3 23, G4 3 |

Split (by Development, stratified, seed-fixed): development 74 cases, acceptance 83 cases (`split.json`).

Shortfalls against the plan (A 30, B 30, C 30, D 30, E 40 cases):
- **D** 25 of 30 and **C** 28 of 30: 15 Developments each, but some Developments (5 in D, 2 in C) had no second unused late segment to draw
  (B items are not reused within a Development), so they give 1 case.
- **E** 44 (above the 40 plan): D398 is pinned at 6 cases; the other 13 Developments give up to 3 each.
- **G4 (>= 21 d) has only 3 cases** (D398 twice, D449 once): the snapshot holds only 15 Developments (>= 3 members) longer than 14 d, 2 longer than
  30 d. The long-gap end cannot be filled more without repeating D398; the evidence there is D398-heavy. Reported, not padded.
- Only **16** of the 157 B sides are a single report (no companion within 24 h); **77** A sides hold a single report (only one report within
  6 h of the earliest member), 32 hold two, 48 hold three.
- Strata overlap: a Development belongs to the first matching stratum only (E, C, D, B, A order).

Cases per Development: 1 to 3, D398 6 (2 per long band). Cases from one Development are not independent; they stay on the same split
side and the scorer reports Development-level numbers too.

## Overlap

| Check | Count |
|---|---|
| Upstream gold Developments listed (topic + location `cases.json`) | 263 |
| of which present in the drawn Developments | **0** (excluded up front; 167 would have been in the frame) |
| Identity-gold case items (a/b ids, `identity-gold.yaml`) | 228 |
| of which matched to snapshot items (normalised URL or outlet+headline) | 33 |
| Developments excluded because they contain a matched gold item | 14 |
| matched gold items in the drawn Developments / in shown case items | **0 / 0** |
| All identity replay-window items (windows 2026-07 .. 2026-09-30) | 810 |
| of which matched to snapshot items | 61 |
| matched window items in drawn Developments / in shown case items | 3 / 3 (reported, not excluded: windows are context, the gold cases are what was labelled) |

Most identity-gold items predate the snapshot's live window (wayback windows), so few can match. The matching is by URL or
exact outlet+headline; an item re-published under a different URL and headline would not be caught.

## Method notes

- Item time = `published_at`, else `fetched_at`. Founders = members within 6 h of the earliest member; late = more than 48 h after it;
  burst gap = 24 h; chain depth, parent = the most cosine-similar earlier compatible member (feature definitions in the `build_sample.py` header).
  Chain depth is computed for Developments with span >= 48 h and >= 4 members only (other strata need none).
- Side A: up to 3 earliest founders. Side B: a seeded random anchor in the band plus its 2 nearest (cosine) non-founder members published
  within 24 h; items already used as B in an earlier case of the same Development are not reused.
- Case order is a seeded shuffle and case ids are opaque; `cases.json` has no Development id, item id, cosine, stratum or band.
- Stratum thresholds are PROPOSED (owner decision O6); the strata are sampling aids and do not label anything.
- First build attempt: the recurring stratum used a 48 h silent-gap rule and found no Development (the clusterer links within 72 h, so
  silences of 48 h or more hardly occur); the gap was changed to 24 h and the sample rebuilt, **before any label or score existed**. Only
  the committed final build is in the manifest.

## Files

`cases.json` (blind label input), `key.json` (case to Development, item ids, stratum, band, gap, features, pool size; not for labellers),
`split.json`, `manifest.json` (snapshot sha, seed, script hash, parameters, counts, overlap, output hashes), `build_sample.py`,
`label_server.py`, `SPEC.md`.

## Labelling

`python label_server.py` (127.0.0.1:8795), `--validate`, `--freeze` (writes `labels-freeze.json` with label and history sha256; edits refused afterwards).
Every save is appended to `label-history.jsonl`; the first answer per case is the blind primary basis. Fields: label, confidence (optional), note.
