# Freeze record: long-horizon Development identity v1

**Frozen 2026-11-23** on owner approval of O1-O11 (recorded in `SPEC.md` section 12). From here the spec, sample, case
files, split and scoring rules change only by a dated amendment appended below. Labels: 0 at freeze.

| | |
|---|---|
| Owner definition | "A Development is one occurrence or tightly bounded event episode. Longer-running storylines belong at the Situation layer." |
| Snapshot | `7463859a4f3537eb29447a755f252dbebc80cc01a1d855739c57b10489964c3c` (VM, 2026-11-23 09:43Z) |
| Seed | `20261124` |
| Sample | 157 cases, 104 Developments; split 74 development / 83 acceptance (by Development) |
| Primary scoring basis | first answer per case in `label-history.jsonl` (blind); final answers secondary |
| Binary projection | *same* = `SAME_EPISODE`; sensitivity run: *same* = `SAME_EPISODE` + `FOLLOW_UP_SAME_STORYLINE` |
| Guard thresholds | none; owner sets them before the first guard is scored (O5) |

## Frozen files (sha256 of LF content)

Text files are hashed with CRLF folded to LF (`.gitattributes` pins these paths to LF on checkout).

| File | sha256 |
|---|---|
| `SPEC.md` | `3c1e00fb118b0274f9261292270acec86240d44bb07676326edee5e1a7488778` |
| `SAMPLE.md` | `37cd7ae551117b1b7b7152121123f0ab6284362795a55251506f16f5a9fef272` |
| `build_sample.py` | `e6c686ec0cf1b9660e15d8ed643ad218066f8e436c61e0ee33c60396faea0eb9` |
| `label_server.py` | `250d87632692dcdd951dcfd0b690780e614c8d7ac014b22bba460ff64afcd968` |
| `cases.json` | `c1d41fe7fc2361817b460bb1172d154803ed9788f5dbaf0367b1c1c43cf338fb` |
| `key.json` | `ba1f0bc4c444b588c417bf3608f2e387b6e5068a2c2be9a89610e1cb84980981` |
| `split.json` | `20d34a6da64b012428f6b92bf8a5e16c9ff09678741d8402021e104f87fa8710` |
| `manifest.json` | `c29a2023b4a9d0107ca0cb28fe45ba2d73cff9e10cae88855060625637959c07` |

`manifest.json` output hashes (`cases.json`, `key.json`, `split.json`) and `script_sha256` (`build_sample.py`) were
re-verified against these files at freeze.

## Labelling

`label_server.py --port 8795` (127.0.0.1 only). After the last case: `--validate`, then `--freeze` (writes
`labels-freeze.json`; edits refused afterwards).

## Amendments

(none)
