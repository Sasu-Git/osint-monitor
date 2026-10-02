# Development identity contract (Phase 2)

The semantic contract Phase 2 implements and is scored against. It is fixed by the owner-reviewed identity gold,
revision 2 (`gold/manifest.yaml`), and was recorded before any Phase 2 runtime code exists.

## Definition

A **Development** represents one coherent real-world action, occurrence, decision or materially unified update.

## Labels

### SAME_DEVELOPMENT

Two items are the same Development when they are about the **same underlying occurrence or action**, even when
they differ by:
- outlet;
- language;
- framing;
- detail;
- casualty count;
- follow-up factual updates;
- official supporting documents;
- a Q&A, factsheet or release package;
- a roundup headline that carries the same occurrence.

Different reporting artifacts are not automatically different Developments.

Owner-confirmed examples (gold):
- **C034, C103:** the Commission's proposal and its own Q&A and factsheet.
- **C064:** a Security Council meeting record and the briefing in it.
- **C076:** a drone crash in Moldova during the overnight attack on Ukraine, and the attack's casualties.
- **C018, C082:** the Moroccan PM's appointment and the customary audience with the King.
- **C029:** a same-outlet roundup headline carrying the record budget and decree reported an hour apart.
- **A009, C005:** one strike or one UN observance reported with different detail.

### DIFFERENT_DEVELOPMENT

Two items are different Developments when there is a **distinct action or occurrence**, even inside the same:
- crisis;
- conflict;
- summit;
- visit;
- disaster;
- policy process;
- military campaign.

Examples of distinct actions:
- warning vs evacuation vs rescue vs damage assessment;
- meeting vs later agreement;
- attack vs retaliation;
- policy proposal vs later adoption;
- summit arrival vs substantive outcome, where these are distinct actions.

Owner examples (gold):
- **A017, A021, A022:** an Ebola spread warning vs the vaccine trial vs the arrival of doses.
- **H023, H029:** people returning home vs the rescue operation after the Nepal flood.
- **H008:** China's glacier warning vs the rescue report.
- **C094:** the US Senate declining to vote vs the settler raid itself.

### AMBIGUOUS

Use AMBIGUOUS **only** when the available evidence is insufficient to decide whether two items refer to the same
underlying occurrence. Do not use it merely because the story is complex.

The only gold case is A028: whether a settlement re-establishment displaced the same families reported in a
second article. AMBIGUOUS cases are excluded from scoring and reported separately.

## The higher level is out of scope for Phase 2

The owner's notes describe typed relationships and groupings *above* the Development:
- official act packages, beyond the cases already labelled SAME;
- calamity lifecycles;
- visits and summits;
- attack waves;
- action → reaction;
- co-causation.

They are recorded in `owner-notes-proposals.md` as Phase 3 design input. **They are not part of Phase 2.** Phase 2
keeps Development identity strict, adds no grouping layer, and does not use them to merge Developments.

## What Phase 2 is scored on

Phase 2 is scored on revision 2 of the gold, development split only. The holdout (30 cases) stays sealed until
Phase 2 development is complete. Metrics are defined in `README.md`: continuity precision and recall,
split/merge correctness, ID stability, mixed-Development rate and duplicate membership.
