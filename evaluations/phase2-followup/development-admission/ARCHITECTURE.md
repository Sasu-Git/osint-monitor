# Development admission: architecture proposal

Status: **PROPOSAL, NOT IMPLEMENTED** (2026-10-27). No runtime behaviour changes until the owner approves an
implementation. Evidence: `../forensics/` (start with `d398/FORENSIC-REPORT.md`).

Research question:

> Can a new item be required to match the Development **as an occurrence**, not merely any individual member, while
> preserving legitimate corroboration and late-arriving evidence?

## 1. The current admission contract (code at `adacb83`, identical in `5f046b3` and `3eda6d0`)

### 1a. Candidate generation, every tier run (`clustering.cluster_recent_items`)

1. **Window.** Narrative items fetched and published in the last 48 h (`recent_items`) that have an embedding.
   Existing members are included when they are inside the window.
2. **HDBSCAN** on the stored full-text embeddings (euclidean, `cluster_selection_epsilon` 0.2). Clusters with more
   than 15 items are re-clustered at epsilon 0.1; noise from that split is dropped.
3. **Link refinement (`refine_cluster`).** The link rule `_linked` decides which items are linked:
   - within 72 h;
   - different outlet: full-text cosine ≥ **0.53**;
   - same outlet: headline ratio ≥ 90.

   Each HDBSCAN cluster becomes the **connected components** of these links, and members below cosine 0.45 to their
   component's centroid are dropped.
4. **Noise rescue (`_attach_to_clusters`).** A noise item joins the cluster it links to and sits closest to (centroid
   cosine ≥ 0.45). Leftover noise is linked into components the same way.
5. **Segmentation (`development_segmentation.segment`).** Inside each cluster, every link is re-checked by
   `incompatibility`:
   - analysis vs report headline;
   - headline cosine < 0.5 between different outlets, unless the 6 h shared-place override or the P7 occurrence match
     (within 24 h, no place conflict, a specific shared anchor or the same cited source) applies;
   - disjoint places, which needs **both** items to name places.

   The cluster becomes the **connected components** of the remaining links.

### 1b. Membership (`development_identity.reconcile`, per cluster, fixed order)

- **Existing members are never moved.** A cluster that touches existing Developments compares each **new** item with
  **all** members of those Developments (any age; the 72 h pair limit still applies).
- **Later attachment.** A new item continues a Development when it has a compatible link (`compatible_link` =
  `_linked` and no segmentation guard) to **at least one** member. Among several Developments, the one with the most
  linked members wins.

  **CURRENT RULE = a valid link to any existing member is sufficient.**
- **Initial formation.** New items that continue nothing become a new Development when they are a **connected
  component** of compatible links (size ≥ 2) with ≥ 2 independent provenance origins (single-source policy).
  Otherwise they stay below the Development layer.
- **Dedup path (`pipeline.py`).** A near-duplicate of an item from another outlet is added straight to that item's
  Development, with no link or guard check (19 of D398's 593 members).
- **Structured records** are grouped by record identity, not similarity. They are out of scope.

### 1c. Formation and attachment do not fail the same way

| | Initial formation | Later attachment |
|---|---|---|
| Unit | the new items of one cluster, one run | one new item at a time, over many runs |
| Rule | connected component of compatible links among the new items + 2 origins | one compatible link to any member |
| Transitivity | **within one run**: A–B–C is one Development even if A and C are incompatible | **across runs**: every admitted item becomes a new attachment surface |
| Reference to "the occurrence" | none beyond pairwise links (and the 0.45 centroid trim at cluster level) | none: no core, no representative, no bound |
| Forensic failure | all 8 giants were multi-occurrence at birth (e.g., D398: announcement + statements + strikes over 36 h) | relay growth for 5–16 days; 89% of D398 is ≥ 2 hops from the seed; joiners resemble current members, not the seed |

**How existing members influence future joins.** Every member is a full attachment surface for 72 h after
publication, so the surface grows with the Development (D398: 15 → 249 members in reach within four days) and slides
with the storyline. The Development has no representation of what it is, so it can drift indefinitely.

## 2. Candidate interventions

All candidates keep the existing pair rule as the **local** test and add a **Development-level** test. None changes a
threshold.

| | A. Stable founder / core set | B. Stable representative (medoid) | C. k-support | D. Core + local link |
|---|---|---|---|---|
| New item must | link to a member AND be compatible with a frozen core | link to a member AND be compatible with one or a few fixed representatives | have ≥ k compatible links to members of ≥ k independent origins | link to any member (unchanged) AND be compatible with the frozen core (majority of core) |
| Stops drift? | yes, if the core is frozen | yes, if the representative is fixed | **no**: in a dense storyline mesh, k links are easy (D398: 8.8 links per member; 81% of joins had ≥ 2) | yes |
| Stops relay chains? | yes (every joiner must resemble the core) | yes | partly (raises the cost per hop, not the reach) | yes |
| Risk to late corroboration | low if core compatibility is lenient (majority, existing thresholds) | higher: one representative can be atypical; multilingual or short items miss it | high for small Developments and the first late report (only 1–2 members to support it) | low |
| Risk of freezing a bad start | high if the core is the whole founder set (all 8 giants were mixed at birth) | high if the representative is a mixed founder's medoid | n/a | mitigated by a cohesive kernel (section 4) |
| New parameters | core size, compatibility quorum | number of representatives, threshold | k | core size (≤ 5), quorum (majority) |
| Explainability | "matches 3 of the 4 core reports" | "matches the representative" | "supported by 2 origins" | local partner + core quorum, both explicit |

**Why not C as the main lever.** Forensics show D398's joins already had a median of several links, and removing all
single-link joins would not have split the mesh. k-support also penalises the first late report of a genuine
occurrence. It is kept as one comparison variant (DA3), not as the recommendation.

**Why not a continuously averaged centroid.** The current centroid drifted from 0.96 to 0.75 cosine against the seed
within two days. Joiners matched the moving centroid (19% below 0.53) but not the seed (68% below). Any
representation that updates with every member reproduces the failure, so all representations proposed here are
**fixed member items**.

## 3. Recommendation: D, core + local link, with a cohesive founder kernel

```
admit(item, D) =  local:  compatible_link(item, m) for some member m of D        (current rule, unchanged)
              AND global: core_compatible(item, core(D))                        (new, Development-level)
```

**Local evidence** says the item belongs to this neighbourhood. **Global evidence** says it still represents the same
occurrence. Both are booleans with named sub-conditions; there is no blended score.

The **cohesive founder kernel** (section 4) applies the same idea at birth, because every giant was already mixed when
it was created. It is tested as a separate variant (DA2), so formation and attachment effects can be measured apart.

## 4. The stable occurrence core

**When it is created.** At Development creation, from the founder set F: the new items of the creating decision,
after segmentation.

**Kernel selection.** Deterministic, using real member item ids, with provenance recorded:

1. **Eligible items:** members of F whose headline kind is REPORT (not analysis, live blog or roundup), plus
   primary/official evidence.
2. **Seed pair:** the eligible pair with a compatible link and **different provenance origins** (the
   `ProvenanceResolver` origin, not just the outlet). The highest cosine wins; ties go to the earliest publication,
   then the lowest ids.
3. **Growth:** repeatedly add the eligible item that is compatibly linked to **every** current kernel member,
   highest minimum cosine first, until 5 items or none qualifies (complete-link cohesion).
4. **Core** = the kernel (2–5 items).

**If the founder cluster is mixed.**
- **In DA2:** founder items outside the kernel are admitted only if they pass `core_compatible`, like any later item.
  The others are held below the layer and stay available to form or join another Development in a later run.
- **In DA1:** formation is unchanged, so the core is the kernel computed from the founders, but every founder stays a
  member.

**If no eligible cross-origin pair exists.** The founders cannot show two independent reports of one occurrence.
- **DA2:** the Development is not created (stricter than today's 2-origin rule, which also counts non-report
  evidence).
- **DA1:** the core falls back to the founder set (at most 5, earliest first).

**Can the core change?** Not in round 1. It is frozen at creation. No item is ever removed from it and nothing is
promoted into it.
- **Later primary or official sources** are admitted as members if compatible, but do not join the core. Core
  promotion, for example of a later official document that is compatible with every core member, is deferred to a
  separately preregistered round. A mutable core needs its own evidence that it does not drift.
- **A bad core cannot freeze an error for ever.** A mixed core is limited to items that are pairwise compatible, which
  is much harder to satisfy than single-link connectivity. And no existing Development is ever split or merged (ID
  stability), so a wrong core only stops the Development from growing; items it rejects form their own Development.

**Size.** 2–5 items.

**Source independence.** The seed pair must come from two provenance origins; wire copies collapse into one origin.
Later core growth may include more items of the same origin, but that never substitutes for the second origin.

**Language.** Any language may be in the core. The embedding is English-only, so `core_compatible` is weak evidence
for Spanish and Italian text (failure family F2). No cross-language rule is added: cross-language identity stays
disabled.

**Existing Developments at deploy time** (if ever deployed). Their core is computed with the same kernel rule from
their first-run members (`event_items.added_run_id`). Existing memberships are not changed. Repairing existing giant
Developments is a separate, separately approved task.

## 5. Development-level compatibility (`core_compatible`, booleans only)

`core_compatible(item, core)` holds when **all** of the following hold. They reuse existing thresholds; nothing is
tuned.

| Condition | Definition | Why |
|---|---|---|
| **C-sem (quorum)** | full-text cosine ≥ 0.53 (the link threshold) to **at least ⌈\|core\|/2⌉** core members | Global semantic agreement with the occurrence, not with one neighbour. D398's joiners resembled neighbours, not the seed |
| **C-head** (report headlines only) | headline cosine ≥ 0.5 to at least one core report, **or** the P7 occurrence evidence with a core member | The existing headline guard, applied against the core instead of a neighbour |
| **C-place** | no specific-place conflict: if the item and the core's union of places both name places, some pair must be compatible (gazetteer containment, `use_regions: false`) | The existing disjoint-place guard, applied against the core |

Considered and **not used** in round 1:
- **Actors.** State-level overlap is shared by whole storylines (74% of D398 links shared only states), so it is no
  positive evidence. There is no validated actor-conflict rule.
- **Time since the occurrence started.** Elapsed time alone is not identity (T24 lost genuine 32–34 h pairs).
- **Action classes.** E1 found them unreliable.
- **Any new NLP ontology.**

**Evidence type.** Analysis, live-blog and roundup items are not excluded. They are skipped by C-head, because their
headline form differs, but must pass C-sem and C-place against the core. They still need a local link, which the
existing analysis guard constrains.

**Explanation per decision.** `local partner #id (cosine x); core quorum 3/4 (ids…); place: compatible`, or the first
failing condition.

## 6. Initial formation, a separate subproblem

**What the forensics establish.** Formation is transitive within a run (connected components of compatible links),
and every giant's founder set was multi-occurrence. Two levers are available:

1. **Cohesive kernel before promotion (DA2, recommended for testing).** Promote only a complete-link kernel. The rest
   of the founder component must pass the core test or wait. This is simple, deterministic and explainable.
2. **Stricter cluster assembly** (complete-link or local-density components in `refine_cluster` or segmentation).
   It changes the clusterer for every consumer, so it is not in round 1.

Graph community methods are not proposed; the kernel rule is simpler and was not yet shown to fail.

**Before measuring formation effects, characterise** on the frozen data: how many founder sets of the relay set
contain a complete-link kernel of ≥ 2 cross-origin reports, and what fraction of founder items fall outside it
(`EXPERIMENT-PLAN.md`, step 2).

## 7. Explicitly not the primary mechanism

These are not proposed: a maximum Development size, a hard age cap, a global higher cosine, excluding GDELT,
excluding commentary, requiring places, and per-case actor or place exceptions. The forensics show none addresses
transitive growth without damaging genuine SAME cases; some may become secondary safeguards later. The target is
**coherence, not cardinality**. A real occurrence may gather hundreds of reports over days, in several languages,
with commentary.

## 8. Risks and known limits

- **Non-English (F2) giants.** `core_compatible` relies on the same English-only embedding, so Spanish and Italian
  cores may admit name-driven items. Expected improvement: partial. Measured separately.
- **Frozen core misses a later legitimate development of the same occurrence** (for example, the casualty count
  updated two days later with different wording). The quorum is lenient by design (majority at the existing link
  threshold). Late-attachment recall is a gate metric.
- **More, smaller Developments.** Items rejected by a core form their own Developments when corroborated. This is
  desired, but it raises the Development count and lowers ID stability for SAME pairs the core wrongly rejects.
  Both are gated.
- **Situations are untouched.** Smaller Developments change Situation inputs indirectly. Situation rules do not
  change; any Situation effect is reported, not gated, in round 1.
- **Dedup path unchanged.** Near-duplicates still attach directly. They inherit the admitted member's correctness;
  their count is reported.

## Amendment 1 (2026-10-27): the dedup path is subject to admission

The dedup attachment (section 1b) is no longer a bypass in the experiment. A cross-origin near-duplicate may use the
near-duplicate match as its local link, but it joins an existing Development only if it also passes that variant's
Development-level check (DA1, DA2: `core_compatible`; DA4: the medoid check; DA3: it counts as one of the two
supporting links). Otherwise it is processed as an ordinary new item. Deduplication itself is unchanged. DA1 is the
attachment-control experiment and may keep a mixed founder set; DA2 tests formation as well (`EXPERIMENT-PLAN.md`,
amendment 1 C).
