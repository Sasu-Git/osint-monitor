# Labelling subsample: freeze (2026-11-03)

Frozen before any labelling. Not labelled, not scored. The full set's `../FREEZE.md` is unchanged and still verifies;
the 379 cases remain the expansion set.

- Source: `../cases.json` sha256 `725d7a2d50e18e20ead4e773f17a0fdc014c2784bfb21096ac10b7550cb88b17` (unchanged; verified by `sample_subsample.py` before reading).
- Draw: `python sample_subsample.py`, seed 20261103, fraction 0.25, minimum 2 per Situation; re-run gave
  byte-identical outputs. `key.json` was not opened.
- `labels_subsample.py validate` checks every file below against its hash, except the labels template, which changes
  when the owner fills it (its template hash is kept for the record).

```sha256
1f441e71a05b14cb56406cfdf2fda244c04ee827cfd7c2218fc3ae9da3697446  sample_subsample.py
c745d15c66df2823f8f1dbecb02b3d88a5580875db582a854fad0faae6f0458a  manifest.json
e6f0f287d320660cc1123f02cfd0a894a1ca84a2496e038600bec6da12738527  label_server.py
4660f3f02512cc7dd51c7ad5ac08e832ff98ad9de0e8ec131134c2bff58763bf  labels_subsample.py
1e9dfe1f55971fd2cd3c9456785a1aef787a80fcc114f9790b61ae785b7e7aa0  score_subsample.py
d9a2250b8c0cf826cc6bca2567075a773c3d30f3a93e718f4b62d00daeafaf63  SUBSAMPLE.md
339cdb3c3430a97c861c2ec6ef47f63e7f327c6481ca2742eb324288ebe9d958  owner-labels-subsample.yaml (empty template)
```
