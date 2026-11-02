# Frozen 2026-11-02: geolocation defect set

| Input | Value |
|---|---|
| Snapshot | backup-API copy of the live DB `data/eval/window-2026-09-25.db` (source opened `mode=ro`), taken 2026-11-02 12:55Z; 1,198 Developments (max D1198); last run finished 12:40:29Z; sha256 `b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40` (kept outside the repository) |
| Code | `deploy-web-20261102` = `d06af11` (the map's placement check, `osint_monitor/api/geo.py`); geocoder `osint_monitor/processors/geocoding.py` unchanged on `main` `44e0357` |
| Source languages | `config/sources.yaml` at `d06af11` |
| Shown sample | `random.sample(shown, 40)`, seed 20261102 |

| File | sha256 |
|---|---|
| `audit-all.json` (every Development; kept with the snapshot, not committed) | `f52061b718a897fe2faa7f455e1e7719f32503a1fe2a710fa25d1656d9cfdd09` |
| `cases.json` | `cab20c4ad5519f2b21b918b4758923ef2139213960c0eae931df76b289c330ef` |
| `labels.py` | `ae935830fb0408ebd3b1da49d911e10eee256eb4ac702dfd9948eaf77c2a42fc` |
| `audit.py` | `359fab29aec07e6154fecba6e8567314effbbda5b36bbb75a54178f23f69919b` |
| `build_cases.py` | `701362165aaaf406bda36575a6946cc29ddd53f9d3f9788fac3b9b8de435a94a` |
| `stats.json` | `7b262243ab4cfa73ecac2b9a2a8328783dc9e5d1dee8a9846eed44a391ded4af` |

Labels are a first pass by the assistant, not owner-reviewed. A fix must be judged on these cases unchanged; new
labels go into a new revision, not into this one.

Reproduce: `PYTHONPATH=<d06af11 checkout> python audit.py --db <snapshot> --sources <d06af11>/config/sources.yaml --out audit-all.json`,
then `python build_cases.py audit-all.json`.
