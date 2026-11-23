# D398 identity diagnostic (read-only, facts only, 2026-11-23)

**Input.** VM snapshot 2026-11-23, sha256 `7463859a…964c3c`, backup-API copy, `query_only=ON`. Numbers in
`results.json` / `followup.json`; per-item attach rows in `d398_attach_rows.json`. No repair, no verdict.

| Fact | Value |
|---|---|
| Items | **2,344** (705 by 2026-11-02; 1,639 since); none shared with another Development |
| Stored | summary "Six Ukrainian energy sites hit by Russia since Trump announced ceasefire, Zelensky says"; type `ceasefire`; Situation 14 (`russia-united-states`) |
| Span | published 2026-10-11 → 2026-11-23; added 2026-10-13 → 2026-11-23; peak 2026-11-19 (272 items); W47 alone 977 |
| Runs | 1,358 distinct runs (1,284 warm); 8 code versions (03841eb 1,332 items, 3eda6d0 580) |
| Sources | 25; GDELT 1,216, Kyiv Independent 339, France 24 186, Al Jazeera 142, SCMP 111 |
| Language | en 2,165 · es 136 · it 43 |
| Per-item rule type | unknown 803, military_action 463, negotiation 219, summit 179, bilateral_meeting 176, significant_statement 137, ceasefire 82, … |
| Actor keys (items) | russia 1,675, ukraine 1,431, united states 1,007, china 524, shenzhen 183, … ; stored principals are only Russia variants (Ukraine not stored) |
| Places (items) | shenzhen 183, apec 152, europe 120, abu dhabi 86, oleshky 70, crimea 46, …; 1,332 items carry no specific place |
| Components | all 2,745,996 pairs checked: **1 compatible component of 2,344** (degree median 12, max 168; diameter 25; 146 articulation points) |

**Attachment mechanism.**
- **Rule:** `clustering.persist_clusters` → `development_identity.reconcile`. A new item joins the existing
  Development it is directly `compatible_link`ed to: cosine ≥ 0.53 across sources, within 72 h, no segmentation
  guard against it. It is tested against **any member**, not the centroid. There is **no size and no age cap**.
  59 items came via the hot-tier near-duplicate path.
- **Chaining:** recomputed from stored embeddings, 2,333 of the 2,337 items after the first run link to an earlier
  member (best-link cosine median 0.66), but their median cosine to the first run is **0.40**. No item after W42 links
  to a seed item. The parent-chain depth median is 31 (max 51).
- **Drift:** the first-chunk centroid drifts from 1.0 to about 0.6–0.8. All-pairs cosine median is 0.30.
- **Finding (factual):** single-linkage growth by chaining. Late items (APEC / Shenzhen, Libya warship) share
  nothing direct with the founding ceasefire story.

**Gold sets.** D398 is in neither (both cover ids > 1341).

**Not reproduced:** 4 items (8560, 12595, 37404, 43002) have no compatible link to an earlier member under the current
rule; they possibly attached through a same-run link or older code (untested).
