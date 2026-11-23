# Pre-model baseline, 2026-11-23

Named baseline: **`pre-model-baseline-20261123`**. The repaired production state and the decision state before any
upstream topic or location model exists. Later replays and model evaluations compare against this.

## Production database snapshot

| | |
|---|---|
| Taken | 2026-11-23 ~14:43Z, backup API, right after the Burnham retirement (repair-20261123c step 6) |
| Code live | `deploy-vm-20261123` = `4ffee11` (pinned); schema 6 |
| `baseline.db` sha256 | `31c6edd74cb041151390de2010ba8fcaa955d10a9d0f9a0d611f6a6321e6ada7` |
| `baseline.db.gz` sha256 (`gzip -n`) | `bdc5f5aac7b0c81669604b3d3fd87b67615fd747661d170f32a94d92cb4817db` (229,550,289 B) |
| VM copy | `/opt/osint/data/archive/pre-model-baseline-20261123/` (`baseline.db`, `baseline.db.gz`) |
| Laptop copy | `data/archive/pre-model-baseline-20261123/baseline.db.gz` (gitignored) |
| Detector state | repair detector: no invalid created Situation; founder detector: 0 candidates of 16 open created Situations |

Situation repairs reflected (all 2026-11-23, allow-listed, detach only, none regrouped): 11 Situations retired
(ids 12, 16, 17, 18, 22, 24, 25, 27, 28, 31, 35), 152 Developments detached.

The upstream gold sets and every diagnostic so far were built on the earlier snapshot `7463859a…964c3c`
(2026-11-23 09:43Z). Developments are identical in kind between the two; only Situation assignments and new
collection differ.

## Code and evaluation state (origin)

| Branch / tag | SHA | State |
|---|---|---|
| `main` | `b92acc6` | = `production-stable-20261112` (`03841eb`) + eval-worker agent |
| `deploy-vm-20261123` (tag) | `4ffee11` | live on the VM; soak C1 OK |
| `eval/upstream-gold-20261123` | `5813379` | topic 130 / location 133 / roles 50, split 40/60 frozen; labelling in progress |
| `design/event-topic-model` | `b12cd98` | spec frozen |
| `design/event-location-model` | `508f0bd` | spec frozen (amendment wording only) |
| `eval/upstream-model-harness` | `29a1e50` | harness + gold-completion checker; no fit, no score |
| `deploy/multilingual-model-package` | `8bc7938` | package prepared; NOT installed |
| `eval/chrono-replay-instrumentation` | `e889510` | instrumentation; smoke only; final mode guarded |
| `eval/long-horizon-identity` | `593340c` | DRAFT spec + blind sample (157); not frozen |
| `eval/report-component-partition` | `7fb2cbb` | component evidence JSONL v1; no consumer |
| `eval/d398-identity-diagnostic` | `4be8ac3` | diagnostic only |
| `eval/identity-chaining-diagnostic` | `a20e629` | diagnostic only |
| `design/situation-membership-v2-r2` | `bbc9bba` | v2 contract frozen; **paused** |
| `feat/situation-membership-v2-candidate` | `4f4f85d` | v2 engine; **paused**, not deployed |

## Decision state

`docs/upstream/DECISIONS.md` on this branch, including the third round (Burnham executed; Development definition
adopted; no chaining guard; list of things not to do yet).
