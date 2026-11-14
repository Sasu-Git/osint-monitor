# Upstream blocker map (2026-11-14)

Evidence:
- the 2026-11-02 snapshot (1,198 Developments);
- the v2 chronological replay on the 126 diagnostic cases (`feat/situation-membership-v2-candidate` `4f4f85d`);
- the three upstream tracks of 2026-11-11;
- a fresh VM snapshot of 2026-11-14 (repair dry run).

Defect kinds: **missing data** (the signal is not produced), **wrong classification** (produced, wrong), **wrong
threshold** (a cutoff decides it), **wrong ontology** (the categories or conventions don't fit).

| # | Layer | Feeds | Current failure share | Kind |
|---|---|---|---|---|
| 1 | **Actor / entity normalisation** (deployed `03841eb`) | principals → Development topic keys → Situation keys | New malformed Situations prevented. **10** old ones still open (repair track). 93 place aliases parked: they feed actor and entity resolution | ontology (mostly fixed); missing data (aliases) |
| 2 | **Role assignment / principal actors** | Development identity (topic keys), Situation creation and E1 coverage | **25%** of Developments have no principal (302/1198). 1,636 headline-named states or orgs are not principal: threshold 458, a place standing for a state (Gaza → Palestine) 339, topic or counterpart 330, noise from merged Developments 297, coercion target 61, multilateral framing 44, support split across names of one actor 43 | threshold; ontology; wrong aggregation |
| 3 | **Topic / event classification** | v2 topic families (creation keys, OD5 scope signal), ranking | **45.7%** `unknown` (English 36.5%, Spanish 79%, Italian 91%). In v2, 21 of 36 missed members have no Situation, largely for want of a family. Some wrong types (Olympics → `military_action`) | missing data (English-only rules); ontology (no legal or disaster type; intent not modelled); wrong classification |
| 4 | **Event location / place roles** | v2 single-party and hazard keys, place scope signals, the map | **58%** of Developments have no event country. The deployed map agrees with the gold on 54/100. The iteration-3 rule family is closed (negative) | missing data (no place roles); ontology (role conventions) |
| 5 | **Mixed-Development detection** | v2 E5 / `PENDING_MIXED`, membership precision, identity diagnostics | Not stored on `main`. 2 of 4 v2 wrong admissions are merged Developments. Identity: "whole-storyline overmerge" 17 cases, the largest identity error class | missing data |
| 6 | **Development identity / grouping** | everything above | Phase 2 identity (development windows): continuity precision 43/65, recall 43/58, split 22/100, merge 15/58, ID stability 16/19, mixed 12/31. Unchanged by every 11-11 change that passed | wrong threshold / missing signals (the Development-identity follow-up is blocked on new signals) |
| 7 | **Situation creation / membership** (v2 contract frozen `bf57ed7` + amendment 1) | the product | Replay: precision 20/24, recall **20/56** vs runtime 48/56. v2 creates 12 Situations against 23 at runtime. Bounded by layers 2–5 | downstream; **paused** |

**Order the dependencies impose:**
1. Layer 2 roles and layer 3 topic: one model; principals become a consequence of roles.
2. Layer 4 location.
3. Layer 5 mixed flag: independent, small.
4. Layer 6 re-measured.
5. Layer 7 re-replayed.
