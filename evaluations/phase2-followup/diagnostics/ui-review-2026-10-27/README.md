# Diagnostic cases from the workspace UI review (2026-10-27)

Evaluation evidence only. Phase 2 is parked; nothing here is a fix or a decision, and nothing was changed in the
UI to hide it. Source: the owner's review of the situational-awareness workspace screenshots
(`docs/frontend/screenshots/04-development-detail.png`, `05-situation-view.png` on `feat/sa-workspace`).

> The UI has exposed clear mixed-occurrence evidence inside some Developments and overly broad Situation
> membership. Capture the shown ceasefire Development and Russia–Ukraine Situation as concrete Phase 2/identity
> diagnostic cases. (owner, 2026-10-27)

Data: `cases.json`, extracted read-only from a SQLite backup-API copy of the live database
(`data/eval/window-2026-09-25.db`, copied 2026-10-27 about 13:00 UTC from a `mode=ro` source; copy sha256
`3c0b2cd9c9a6e2347a055c62b1f88b7800f9d7b82228370983d48203ad0b4a39`). Code at the time: `adacb83` (Candidate A),
whose identity behaviour is the Phase 2 baseline.

## Case UI-1: Development 398, mixed occurrences (overmerge)

"Six Ukrainian energy sites hit by Russia since Trump announced ceasefire, Zelensky says" (ceasefire / security,
confirmed, Situation `russia-united-states`).

- **593 member items over 17 publication days** (2026-10-11 to 2026-10-27), 17 outlets.
- Corroborated Developments in the snapshot: median 3 items, p90 16, p99 108. Development 398 is the largest.
- Its evidence includes items that are not reports of the stated occurrence. The screenshot shows, for example, DW
  World "Starlink India launch: Why Elon Musk is still waiting", "Starlink: How Elon Musk's company influences
  geopolitics", and an EU-summit story, beside the energy-ceasefire reports. All 593 items are listed in `cases.json`.
- Class: OVERMERGE. It looks like whole-storyline absorption over many ticks (cross-day and same-day), the class the
  frozen defect set marks as the largest residual and that E1 could not address (most overmerge links are within 24 h).
- Other Developments of the same shape in the snapshot, for context and not reviewed: 397 (319 items, Guterres),
  449 (294, Bolsonaro), 639 (256, French stun grenades), 399 (255, Zelensky / Kyiv attacks), 626 (216, French
  protests), 514 (154), 182 (148).

## Case UI-2: Situation `russia-ukraine-war`, broad membership

"Russia–Ukraine war", active, primary actors Russia and Ukraine: **22 Developments** (2026-09-25 to 2026-10-26),
listed with their principal actors in `cases.json`.

- Members include occurrences the owner flagged as outside the war storyline: 959 "Russia to host first Olympic
  federation world event since Ukraine invasion"; 880 "Russian disinformation campaign targets pro-Ukraine
  candidates ahead of midterms"; also, for review, 242 "The price of doing business in Russia" and 214 "Russia's
  military spending masks a longer-term strategy" (analysis headlines).
- Their principal actors resolve to Russia and Ukraine, so they meet the current Situation rule (actor overlap).
  The breadth is a property of that rule, not a single wrong assignment: a Situation keyed on a state pair takes
  every Development whose principals are that pair.
- Class: Situation membership breadth (actor-overlap rule), distinct from Development identity. Situations are
  sticky; any change needs its own evaluation and repair procedure.

## What to do with these

- Use them as concrete cases when Development identity or Situation membership work resumes (Phase 2 is parked).
- Do not fix them in the UI. The workspace shows evidence as stored; an analyst-facing "mixed evidence" warning
  should come from future semantic work, not a frontend heuristic (owner, 2026-10-27).
