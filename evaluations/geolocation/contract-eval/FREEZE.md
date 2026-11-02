# Frozen before the first evaluation run (2026-11-02)

| Input | sha256 |
|---|---|
| Snapshot `snap.db` (2026-11-02 12:55Z, outside the repo) | `b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40` |
| `*evaluations/geolocation/contract-eval/audit-cases.json` | `c11e52a5d0f1ec82bfac40f3d2814f9b421aa43e6f71ad68de534e459e48846f` |
| `*evaluations/geolocation/contract-eval/evaluate.py` | `f831dfb05e1adc5e902325291ee0fb05290d6e2f5b3d628dac90ea6de70bcf38` |
| `*evaluations/geolocation/acceptance-cases.yaml` | `d34df5f58bbd83dbf20f69e885cb6f86a32987dc7192b7578c2edd31e2ae0534` |
| `*osint_monitor/processors/event_location.py` | `afbd4bafbbcef14838775c9d76b5b19cc360ef2b43c2fbf804040a14e71fc945` |

Code: `feat/geolocation-contract` `62fe91d` (module), ISO lookup from the web code `ab45312` (`osint_monitor/api/geo.py`).
`audit-cases.json` is `evaluations/geolocation/2026-11-02/cases.json` from `eval/soak-safe-20261102` (`b794902`),
copied unchanged (its own FREEZE.md records sha `cab20c4a...`).
Gates in `evaluate.py` are PROPOSED (W removed >= 80%, C preserved >= 90%); they are not established until approved.

**Amendment (before any result was produced):** the first run failed at import (`osint_monitor.api.geo` is not importable
beside this branch's package). `evaluate.py` now loads the web code's `geo.py` by file path. Import mechanism only;
no metric, input or rule changed. New sha: `12926c7c9e4ac89841bf517fce6831f730aab36b3241bef22ef0ad4fdd41ba1e`. The audit copy differs from the original only in line endings
(same JSON content; CRLF-normalised hashes equal).
