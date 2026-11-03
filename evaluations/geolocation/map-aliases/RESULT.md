# Map-only place aliases: result (2026-11-02)

**Change.**
- **Table:** `osint_monitor/api/data/place_aliases.json`, 33 entries: es/it exonyms, cities the gazetteer lacks, Hong
  Kong / Macau / Vatican as their own outlines, DR Congo forms.
- **Lookup:** `CountryIndex.of_place` consults the table before the gazetteer.
- **Isolation:** the table is read by the map's placement check only. The shared gazetteer (`config/geography.yaml`)
  and every pipeline stage are unchanged, and a test asserts that no alias reaches the gazetteer.
- **No stored data changes.** It only decides which stored points the map may show.

**Check** (`check_aliases.py`, 2026-11-02 snapshot, the frozen audit's 208 hand-labelled cases):
- **Faithful baseline:** with the table emptied, the code reproduces the audit's recorded `shown` flag for **208/208**
  cases.

| Flip with the table | Count |
|---|---|
| C (right point) hidden → shown | **21** |
| W (wrong point) hidden → shown | **2**: D360 (ICE shooting in Minneapolis, stored point New York; the report names "Nueva York"), D941 (West Bank story, stored point Marseille; the report names "Marsiglia") |
| P hidden → shown | 0 |
| anything shown → hidden | **0** |

**Western Sahara entries removed during this check.** Their first version hid a correct point (D1149): the
gazetteer's Western Sahara → Morocco mapping matches the Natural Earth outline the point lies in. That was a table
error, and the entries were removed, not tuned.

**Pipeline neutrality.** Neutral: no pipeline input or stored location changes.

**Display.** Not strictly neutral: the table shows 21 more correct points and 2 more wrong ones. The 2 wrong ones are
stored geocodes that were already wrong, which a correct exonym now "confirms". Under the location contract they are
fixed at the source (re-derivation, U6 repair), not by the map.

**Owner decision.**
- (a) Ship the table as is: net +19 correct markers.
- (b) Drop "nueva york" and "marsiglia": 0 wrong markers, losing D146 and D442.

Recommended: (a). The two wrong markers come from wrong stored points, which the map's check can't know about.

**Remaining hidden correct points (25)** need things this table can't provide:
- an attacker-country top mention (D124, D170, D1086, …);
- containment by outline (Ceuta D438);
- the "Congo" ambiguity (D425, D468, D689, D1150).

These belong to the location contract, not to the map.

**Tests:** full suite 762 passed, 3 xfailed in 150.14s (0:02:30); workspace and page tests 22 passed (the Altoona assertion updated: now confirmed by design; an unknown town
keeps the unconfirmed case).

## Owner decision (2026-11-03): option (b)

"nueva york" and "marsiglia" dropped; the other 31 entries kept. Re-check (`result-b.json`, same snapshot and cases):
baseline 208/208; C hidden → shown **19** (D146, D442 stay hidden); W hidden → shown **0**; P 0; shown → hidden **0**.
Neutral by the check's rule. Tests: frontend (workspace, pages, UI, read-only web, geography, geocoding) 78 passed;
full suite 762 passed, 3 xfailed. Not deployed (pair-matcher soak in progress).
