# Frozen 2026-11-02 14:08Z: pair-matcher equivalence benchmark (before any variant was run)

| Input | sha256 |
|---|---|
| Snapshot `snap.db` (backup-API copy of the live DB, 2026-11-02 12:55Z; kept outside the repo) | `b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40` |
| `harness.py` (variants P0/P1/P2/impl pre-registered in its docstring) | `1a0df6fc6c8e3ff729fcde7e5ff796ff833260b672c74a37ce82c2e692d3b738` |
| `benchmark.json` (32 Developments, their item ids, groups; seed 20261102) | `51b17b4083e275fc2d21e0f598da9a834dbe3aef4e0a63e5e895caff63f69552` |
| `p0_pairs.csv` (every pair P0 decided: event, item_i, item_j, accept/reject, ratio; 226,218 rows; outside the repo) | `e02857b9b9ebfa1a4205fbe4297cbcb8034063494518e3c98b9b6464ebbfaaf2` |
| `p0_outputs.json` (serialized provenance assessment + corroboration score per Development; outside the repo) | `d704dba1c1ce4f591e6a486b0a0716da0464d30c05bf0826038cff670d1ba476` |

Code: `main` `44e0357` (`osint_monitor/processors/provenance/resolve.py` unchanged since). Groups: largest 5 (D398, D449,
D397, D399, D514), named D398/D449/D514, two 151–300, six 51–150, eight 11–50, twelve 2–10.

Gate (fixed before testing): a variant qualifies only with **0** differences against `p0_outputs.json` (every
Development's provenance and corroboration output, byte-identical serialisation) and identical accepted pair ids;
every pair it skips must be a P0 reject.
