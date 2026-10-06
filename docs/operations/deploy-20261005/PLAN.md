# Post-soak fix plan (`fix/post-soak-20261006`)

**Base.** `production-stable-20261006` = `5f046b3`. The soak passed with follow-ups; the evidence is in
[soak-report-24h.md](soak-report-24h.md) and [post-soak-followups.md](post-soak-followups.md).

**The deployed code stays frozen.** Nothing from this branch reaches the live daemon until:

- the branch has its own tests and a passing regression gate (pytest, smoke, identity gold check, clustering
  benchmark, migration rehearsal);
- the owner has approved a new deploy candidate.

## Priority order (owner, 2026-10-06)

| # | Item | Why first | Done when |
|---|---|---|---|
| 1 | Spanish/Italian actor normalisation, and the Bolsonaro (Jair vs Flávio) ambiguity | The only follow-up that corrupts derived Situation identity (`estados-unidos-united-states`) | es/it country and organisation names normalise to their English canonical keys. "Bolsonaro" alone is not silently merged with "Flávio Bolsonaro". Tests cover both. A recompute plan exists for Situations on the live DB. |
| 2 | Trend baseline reset/rebuild | The source expansion invalidated the anomaly baseline: 377 trend alerts in 24 h | Baselines are rebuilt or normalised for the current source set, and a source-set change cannot raise an anomaly by itself. Trend alerts are treated as untrusted until then. |
| 3 | Post-deploy check fixes | False FAILs at every checkpoint | Stages are required only for runs that processed new items. The Development growth check excludes backlog (Developments first published before the deploy, or from first-time sources). |
| 4 | False operational alerts | Misleading operational alerts | No "Signal restored" when a stored analytic gap turns operational. "Source resumed" is suppressed when the silence predates the first ledger run, or when gaps are backfilled from the old daemon log. |
| 5 | Hot-tier latency | Hot awake coverage 88.5% | DNS/BGP runtime bounded (time budget or tier move). Skipped hot ticks are measured before and after. |
| 6 | Host power / deployment environment | 10.6 h of 24 h lost to lid close and battery standby | Runbook pre-soak checklist: AC power, lid state, `keepawake.py --display` (adopt the pythonw keep-awake). The deployment-host recommendation is documented. |

**Also open (no priority given):**
- the failing collectors: Nitter, Lawfare, X-ForYou, US Congress, Financial Intelligence (Quant);
- a "ledger starts at …" label in `main.py status`;
- the `python -c` import-probe note in the runbook.
