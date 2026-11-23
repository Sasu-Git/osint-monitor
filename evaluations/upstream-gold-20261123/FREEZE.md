# Gold samples: freeze (owner ruling 2026-11-23)

Frozen before any labelling. Sizes fixed by the owner; the pool was **not** widened to reach 150.

| Set | Size | Notes |
|---|---|---|
| topic | **130** | es/typed (13 of 20) and it/typed (7 of 20) strata exhausted: every eligible Development in them is included |
| location | **133** | es/strike (10 of 14) and it/strike (1 of 14) strata exhausted (only 18 es and 9 it Developments in the whole frame carry a strike word) |
| location role subset | **50** | seed 20261125 |

- Frame: Developments with id > 1341 on the post-freeze VM snapshot (sha256 `7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c`), 839 eligible; none seen by an earlier evaluation. D398 (the 682-item Development) is not in either set.
- Type convention (owner): stored `other` counts as an existing classification; only NULL, empty or `unknown` is untyped.
- Scoring bar (owner): topic precision ≥ 0.90 for downstream eligibility; metrics per `../event-topic-model/SPEC.md` §8 and the owner's 2026-11-23 list.
- The first saved answer per case is the blind primary basis; the label servers refuse edits after `--freeze`.

```sha256
cba3bcc4ac06b618c3155532be6ba68912c605c59871402d95cec844c160f99b  sample.py
53311616f72ada6ff40e3ae981c55492599156c5162edad773960baa37425dfd  topic/manifest.json
d779d9c82c5f20a6548883ec57a02c75de942fe742764dc1f2c5e6df6d519e24  topic/cases.json
8c3d188622a09fb82f5c43aaf9fd6642a84e67fac155973c0b6fe72520e214b4  topic/label_server.py
03e2bde4b3309dee62721e29aa7f1774a21e53678c26ea80a607eeb241cfef2b  location/manifest.json
52d33cdc7a3dc12a6aa2b6b6d07f6d969e55963ba2788b24de3f8179f5227ed6  location/cases.json
87f59ca890a7e671f50940481a75174e8622c1a1e352e1085fceabfa0218e93f  location/label_server.py
```

## Amendment 1 (2026-11-23, 0 labels saved): development / acceptance split

Owner ruling: 40 / 60, fixed seed, stratified, frozen before any label exists (both `labels.yaml` empty, no history).
`split.py` (seed 20261126; stratified by sampling stratum, and for location also by role-subset membership; 40%
per stratum, rounded). Development = confidence-band calibration only; acceptance = scored once.

| Set | Development | Acceptance |
|---|---|---|
| topic | 52 | 78 |
| location | 53 | 80 |

```sha256
c3a9d6147e2e01cc4d5b15223b75234be4fa6fc7b1c10b562ab16f14911505eb  split.py
c299c015e0ea95357b804ef895d1b91d6c5334cdc9a0697bab4fbcd8d02afec3  topic/split.json
bfc2c157e866807650f28bedb93ea0d935106b1a2a352c11202c5126727fdc43  location/split.json
```
