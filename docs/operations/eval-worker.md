# Delegating evaluation work: the `eval-worker` agent

Decided by the owner on 2026-11-12, after `/usage` showed built-in `fork` subagents at 54% of usage.

**Default.** Delegate evaluation and replay work to the project agent `eval-worker` (`.claude/agents/eval-worker.md`,
model Sonnet). This covers:
- frozen and replay evaluations;
- blind scoring;
- benchmark and holdout runs (holdouts only when the brief explicitly authorises them);
- read-only diagnostics;
- reproducible reports.

**Not delegated.** Production and deploy work stays in the main session: the VM, the live database, merges to `main`
and stable tags.

**Why.**
- `fork` always runs on the session's model and inherits the whole conversation, about 530k tokens per agent in the
  2026-11-11 hardening cycle.
- `eval-worker` runs on a cheaper model with a fresh, short context.

**How.**
- Give `eval-worker` a self-contained brief: worktree, branch, inputs with hashes, gates, report shape.
- Use `fork` only when a task truly needs the full conversation.
- Review judgement-heavy results (precision calls, gate verdicts) closely before acting on them.
