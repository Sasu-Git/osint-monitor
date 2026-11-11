# Iteration 3: closed as a negative result (owner, 2026-11-11)

**Verdict.** No rule set of iteration 3 (2a, 3a, 4a, 5a, alone or together) beats the deployed map (`d06af11`) on the
frozen 100-case gold sample, on either label basis (blind first answers / final labels). Every candidate fails both
PROPOSED gates (≥ 80% wrong points removed, ≥ 90% right points kept) on both bases. The gates were never approved, so
every verdict is report-only; the substantive conclusion does not depend on them.

| System | Agrees with gold (blind / final) |
|---|---|
| deployed map `d06af11` | 54 / 55 |
| map + aliases `346456f` | 54 / 57 |
| iteration 1 = iteration 2 = 2a | 50 / 52 |
| 4a | 51 / 53 |
| 5a | 49 / 53 |
| 3a | 47 / 48 |
| all four | 47 / 50 |

**Owner rulings at closure:**

1. **No more heuristics in this rule family.** The headline-rule approach is exhausted: three iterations moved
   agreement by at most ±3 cases, and the deployed map already beats them all.
2. **The result is preserved, not deleted.** The frozen inputs, labels, rules, lookup and scores on this branch stay
   as the record (`FREEZE.md`, `labels-freeze.json`, `iter3-score/`). The iteration-2 rules remain what runs today;
   nothing from iteration 3 is deployed.
3. **Future geolocation work moves upstream** into event-location extraction and place-role modelling: extracting
   where the occurrence happens (dateline vs venue vs target vs mentioned place) as a property of the item text, not
   post-hoc rules over pooled member places. Tracked as its own future contract; not started here.
4. The two lookup fixes from the audit (South Sudan; Hong Kong / Macau as their own entities) are generic lookup
   correctness, not iteration-3 heuristics. They stay frozen with this record for whichever system is scored next.

**What the negative result taught** (for the upstream track):
- Pooled member places are the wrong input: members of one Development legitimately name launch sites, targets,
  reporting venues and analysis datelines. Rules over the pool cannot recover which role a place plays.
- The gold labels encode a role decision (owner 2026-11-10: a strike is located at its impact, not its launch site),
  which is only decidable per item, before pooling.
- Language mix matters: the Italian and Spanish strata carried most of the residual errors.
