# Freeze record: actor-identity defects 2026-10-16

Frozen before any fix. Hashes over LF bytes (text) and raw bytes (snapshot).

- code: `3eda6d0` (`production-stable-20261016`)
- snapshot: `data/eval/actor-defects-20261016.snapshot.db` (backup-API copy of the live DB taken 2026-10-16 after the Situation repair; host-local, immutable; KEEP under the retention rule: sole input of this frozen set)
- snapshot sha256: `dc291eaa779be29f45b2b48446327ef8b767cb5ff0db836773eb8b611cee70d7`

| file | sha256 |
|---|---|
| README.md | `865130d9a8aca9b29d028983e405be35ed188ad6d46e0968367dd77bdb5479e9` |
| extract.py | `bda964102f1e52cf8dbb1c96b92a0635c24e8cfaaba096d0850ae5ae2e671074` |
| evidence.json | `5b688bacec8e9575b5eea9de08f5a463dfa579078ea3b909da68cc226c4b7a72` |

Reproduce: `python extract.py <snapshot>` must reproduce `evidence.json` byte-for-byte (LF).
