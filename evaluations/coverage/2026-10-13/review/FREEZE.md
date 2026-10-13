# Coverage-recoverability sample: freeze record

Frozen 2026-10-13, before any owner review. Do not regenerate or edit the files below; labels go only to
`owner-labels.yaml` (written by `review_server.py`). `key.json` holds the bucket and reason per case: do not open it
before review ends (the review page reveals each case's key only after its label is saved).

- seed: 20261013 (sample), 20261014 (case order); 30 per stratum; up to 3 partners
- code: `df33560cfe96abd2b4284fafe6433ba39e997f15` (eval/coverage-diagnosis-20261013; `osint_monitor/` and `config/` identical to deploy-candidate-20261013 `3eda6d0`)
- snapshot: `data/deploy/20261013-1246/backup-final-20261013-105028.db` sha256 `37be8e6dbcbc74a80f57aa30d14cc7acae83e0b0ef05e72dba43b0472b2e3f32`
- coverage.json sha256 `3336c29c0cfd7ab94395cef2ea5684a978c4f277e0945881b88c36ece28abc6e`
- pools: below_threshold 1028, segmentation_es 69, segmentation_it 92, cross_language 190
- labels: SHOULD_JOIN (with the partner ids it should join), SHOULD_NOT_JOIN, AMBIGUOUS

| file | sha256 |
|---|---|
| build_sample.py | `b82381950e51c85c8c0e0189f68c358b5149745cf28088a97105a5b4fa54bd1e` |
| sample-manifest.json | `f2189d75b0cc8793db0903e611df7726524e968a898780ed7592faae0180711e` |
| review-cases.json | `4ad21683e460d9cbfec4925923abac25bd542df70ced32876325799c1734a541` |
| key.json | `356c3ec75338c03c5e6c703f7295aefc50d3325da101ffce3fedd98f09c57f0c` |

Review: `python review_server.py` then open http://127.0.0.1:8766/ . Score: `python score.py`.
