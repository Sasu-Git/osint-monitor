# Situation membership evaluation set: freeze (2026-11-02)

Frozen inputs and outputs of the blind evaluation set. Built, not labelled, not scored.

- Snapshot: `snap.db` (2026-11-02 soak-safe snapshot, outside the repository), opened read-only (sqlite `mode=ro`),
  sha256 `b5bb5728ce76d3eb28c70712b088b026268538243f4fa099744856dc2c29af40` (verified by `build_evalset.py` before
  reading).
- Code: runtime code and config at `38ffb79` (branch `eval/situation-membership-evalset`); no runtime file is changed
  on this branch. The evaluation scripts are committed with this file; their hashes are below.
- Build: `PYTHONPATH=<worktree> PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 python build_evalset.py --snapshot <snap.db>`,
  seed 20261102. Re-running produced byte-identical outputs. `.gitattributes` here keeps LF on every checkout.
- `labels_tool.py validate` checks every file in the block below against its hash, except the labels template,
  which is expected to change when the owner fills it (its template hash is kept for the record).

```sha256
725d7a2d50e18e20ead4e773f17a0fdc014c2784bfb21096ac10b7550cb88b17  cases.json
5817074a533be24cb7610eb6b6d5096e4369c8edb396d48d8ee5813b03042632  key.json
fa3da833e246efbb28cfb93ee0e3b12c81e79939d02f42060c5432cdfa28da3e  scopes.json
0c5acfc90e6d1879f1477527db98c3bda10c12365bc93304813ad6c4fc0f77a1  build_evalset.py
2ffe77f8d7f6105ebdebcebf0f6594bbed2ea5d0f651050f9016c1f43aaf48e4  labels_tool.py
a48568b8e404c9c2d06cb49be3f2db0c1b57462ea01b2618864b491fff95034c  score.py
fd48bef8faccb65947124fcd6a05d67ba6ba871c25f5c55a591a52f280cf7072  PREREGISTRATION.md
ef7ecb356e99a344ac7f8d2e8227d7c5cf8c5233fec88ebee1bff13c958f6a1b  owner-labels.yaml (empty template)
```
