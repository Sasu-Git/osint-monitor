# Lexical identity evaluation scripts

Reproduce `evaluations/clustering/lexical-identity.md` on the frozen development windows. Every
replay uses a temporary database; benchmark files are only read. Run from the repository root:

```bash
export PYTHONPATH=. HF_HUB_OFFLINE=1
python scripts/lexical_identity/replay_cache.py /tmp/dev-cache.pkl development   # one replay per window
python scripts/lexical_identity/audit.py /tmp/dev-cache.pkl /tmp/audit.json      # lexical evidence per pair
python scripts/lexical_identity/candidate.py /tmp/candidate.json                 # baseline vs lexical guard
```

Development windows only: the hold-out windows have already been run (holdout_runs.jsonl).
