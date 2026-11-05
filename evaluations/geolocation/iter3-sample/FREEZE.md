# Iteration 3: fresh blind sample, frozen before any rule is implemented (2026-11-05)

**Owner rulings (2026-11-05).**
- 100 Developments created after the 2026-11-02 snapshot, window frozen at D1341.
- Stratified by map status and language, option (b): all unmapped, plus 75 shown, proportional by language.
- Owner gold labels are frozen before any scoring. The fresh sample decides; the 2026-11-02 audit cases are continuity
  evidence only.

## Inputs

| Input | Value |
|---|---|
| Snapshot | backup API from the live DB opened `mode=ro`, 2026-11-05 13:55:46Z; max D1341. Kept outside the repo at `osint-monitor/data/eval/geolocation-iter3/snap-20261105.db`, sha256 `d85cbac412968468fbc1c189bccdd7c48b28dd60d34462309e4cb017388d0f47` |
| Map status | frozen `audit.py` (`eval/soak-safe-20261102`, sha256 `359fab29aec07e6154fecba6e8567314effbbda5b36bbb75a54178f23f69919b`) with `PYTHONPATH` = `d06af11` (`deploy-web-20261102`, the map baseline) and `d06af11` `config/sources.yaml` |
| Audit output | `osint-monitor/data/eval/geolocation-iter3/audit-all-20261105.json` (outside the repo), sha256 `074424440728b6d577ee33818bc3dbab735e56a561d04ed30193e056859f0797` |
| `draw_sample.py` | sha256 `645d0d220723c23221c093d48abbfe5b2d01dab502256bf324d0e1734b3268a4`, seed 20261105 |
| `manifest.json` | sha256 `f238d6404c4df60524f68224fec0abd96c2045b0c49d5781f08bcd464184f33b` (reproduced byte-identical on a second run) |

## Frame and allocation

| Stratum | Frame | Sample |
|---|---|---|
| Unmapped (hidden 21, no stored point 4) | 25 | 25 (all) |
| Shown, English | 79 | 50 |
| Shown, Spanish | 19 | 12 |
| Shown, undeclared language (`?`) | 14 | 9 |
| Shown, Italian | 6 | 4 |
| **Total** | **143** | **100** |

The dominant language is the one with the most member items. A tie goes to a declared language over `?`, then
alphabetically.

## Gold label schema (owner, blind)

The labeller sees each Development's headline, its member items and their text. They do **not** see the stored point,
the map decision, the stratum or any rule output.

| Field | Value |
|---|---|
| `event_country` | ISO 3166-1 alpha-3 of the country where the reported event takes place; `NONE` when there is no single event country (several countries equally, at sea, global, or not determinable from the items) |
| `event_place` | optional: a more specific place, as written |
| `note` | optional |

## Order from here (no step skipped)

1. Implement rules 2a, 4a, 5a and 3a on iteration 2 with the frozen extension unchanged. Each rule is switchable so
   they can be scored separately. **Not scored.**
2. The owner labels the 100 cases, and the labels are frozen (hash recorded).
3. Lookup audit over every gold label: fix every equivalent gap, then freeze the lookup.
4. Freeze the scoring rule and the rule code. Baseline = `d06af11` map behaviour; aliases `346456f` = secondary.
5. Score once. Re-score iterations 1 and 2 under the same lookup.
