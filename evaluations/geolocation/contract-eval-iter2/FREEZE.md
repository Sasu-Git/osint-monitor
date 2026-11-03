# Iteration 2: frozen before scoring (2026-11-03)

**Rule changes:** `RULES.md`. There are three, and nothing else changed. The diff of `event_location.py` against
iteration 1 (`d842feb`) contains only:
- the extension loader;
- the two lexicons and the filter;
- the extension's L2 resolution;
- the actor-country hold and its fallback block.

**Evaluation:** the same `evaluate.py`, byte-identical to iteration 1 (sha below), on the same snapshot, audit cases
and acceptance cases. `decide()` loads the extension by default. Gates are **PROPOSED**: iteration 1's `FREEZE.md`
and `evaluate.py` mark them "PROPOSED … not established until approved", so they are not binding. A failed gate is
reported as measured, with no tuning after scoring.

| Input | sha256 | Same as iteration 1 |
|---|---|---|
| Snapshot `snap.db` (2026-11-02 12:55Z, outside the repo) | `b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40` | yes |
| `*evaluations/geolocation/contract-eval/audit-cases.json` | `c11e52a5d0f1ec82bfac40f3d2814f9b421aa43e6f71ad68de534e459e48846f` | yes |
| `*evaluations/geolocation/acceptance-cases.yaml` | `92a30dd268239b2c9e5ce8c0878ccdf35e33a5f598d73efd112d74a4ecca3898` | yes (amendment 2 version) |
| `*evaluations/geolocation/contract-eval/evaluate.py` | `a922554753c951701e75b27c9879a9549a79269f8f4905fc53296ce3f0fb5712` | yes |
| `*config/geography.yaml` (shared gazetteer) | `21e0eb38ee9ae4e04a99ad7d27328ae581770ee02308822f369e21ac3072c2cb` | unchanged since `d842feb` |
| `*osint_monitor/processors/event_location.py` | `a0b365b76965646020bbdf43f6a69eb30da96c41fd06436fdf457ac8baf4d669` | new (iteration 2) |
| `*osint_monitor/processors/data/place_extension.json` | `5924ddf2668243aa19ec570d07d6fdb1121010c7a0db1523c1021a98c600ba12` | new |
| `*evaluations/geolocation/gazetteer-extension/build_extension.py` | `432954ee1b927b1c156bfd131007ec87a0981f8d72ba5933a018ad59aefcc017` | new |
| `*evaluations/geolocation/contract-eval-iter2/RULES.md` | `9077d58357e1ce89bb496ba53562fd5874d784428513973380211772395d6229` | new |

**Country lookup for ISO mapping:** the web code's `osint_monitor/api/geo.py` at `ab45312`, as in iteration 1.

**Command** (run once, after this file is committed):

```
PYTHONPATH=<this branch> python evaluations/geolocation/contract-eval/evaluate.py --db <snap.db> \
  --audit evaluations/geolocation/contract-eval/audit-cases.json --acceptance evaluations/geolocation/acceptance-cases.yaml \
  --countries <ab45312 checkout> --out evaluations/geolocation/contract-eval-iter2/results.json
```

**Not done:** no backfill, no database write, no pipeline wiring.
