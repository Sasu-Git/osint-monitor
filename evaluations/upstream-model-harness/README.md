# Upstream model evaluation harness (topic and location)

Harness only. No model, no fitting, no band boundary, no threshold is chosen here. Specs:
`../event-topic-model/SPEC.md`, `../event-location-model/SPEC.md`. Gold: `../upstream-gold-20261123/`.

Run from this directory with the main checkout's venv, `HF_HUB_OFFLINE=1` and
`PYTHONPATH=<this dir>;<worktree root>` (the worktree root provides `osint_monitor`).

```
# 1. gold-completion checker (also called by calibrate and score; exit 1 + counts only when not complete)
python -m upstream_harness.checker --gold-root ../upstream-gold-20261123 [--track topic|location|both] [--require all|development|acceptance]

# 2. features (verifies snapshot sha256, works on a backup copy; deterministic, content hash inside)
python -m upstream_harness.features --gold-root ../upstream-gold-20261123 --track topic --snapshot <gold-snap.db> --out features/topic-features.json

# 3. calibration: development cases only. Boundaries are explicit, or a rule (module:function over development records).
python -m upstream_harness.run calibrate --gold-root G --track topic --features F --model pkg.mod:factory --out-dir OUT --high-min X --medium-min Y
python -m upstream_harness.run calibrate ... --rule pkg.mod:fn

# 4. acceptance scoring: once per (track, model id). A second attempt refuses unless --force-rescore --reason TEXT (logged).
python -m upstream_harness.run score --gold-root G --track topic --features F --model pkg.mod:factory --calibration OUT/calibrations/topic/<model_id>.json --out-dir OUT
```

`factory()` returns an object with `model_id`, `track` (`topic`|`location`) and `predict(case) -> (label, score)`;
label `None` (and `unknown` for topic) is an abstention. Tests: `python -m pytest tests -q`.

Metric definitions are in the `upstream_harness/metrics.py` docstring.
