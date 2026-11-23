# Multilingual embedding model package

**STATUS: NOT INSTALLED -- owner approval required.** Nothing here was run against the VM; the VM was not contacted.
Model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, revision
`e8f8c211226b894fcb81acc59f3b34ba3efd5f42` (384-dim, 12 layers, 250037-token vocab).

## Files
| File | Purpose |
|---|---|
| `MANIFEST.json` | every snapshot file with size + sha256; which are needed (9 of 10; README.md excluded); 479,725,122 B needed |
| `requirements-vm.lock.txt` | version pins (identical on laptop and VM) and what is missing |
| `build_manifest.py`, `build_tarball.py` | rebuild manifest / deterministic tarball from the laptop HF cache (read-only) |
| `install_model.sh` | VM installer (dry-run by default) |
| `repro_check.py`, `compare_repro.py`, `repro-laptop.json` | reproducibility check and laptop reference output |
| `footprint.py` | RSS / throughput measurement (stdlib + torch only) |

## Weights format
Safetensors only. `model.safetensors` is the sole weights file in the pinned snapshot; sentence-transformers 6.1.0 /
transformers 5.17.0 load it natively and it is loaded without pickle (no code execution from a hand-moved file).
`pytorch_model.bin` is not in the snapshot and is not shipped. `tokenizer.json` (fast tokenizer) is used;
`sentencepiece.bpe.model` is not needed offline (verified by encoding on the laptop).

## Tarball
`data/model-packages/multilingual-minilm-l12-e8f8c211.tar.gz` (gitignored, not in git), 435,633,154 B,
**sha256 `195b0fc5769196b33ad8ae50b0af8127b304592c99467f26f1c58272c3e04c62`**. Built twice, byte-identical (sorted
entries, mtime 0, uid/gid 0, gzip mtime 0). Layout is the HF cache layout (`models--.../{blobs,refs,snapshots}`;
snapshot entries are relative symlinks into blobs; `refs/main` is the pinned revision).

## Steps (all need owner approval; none done)
1. Owner approves an install window (daemon RSS ~2.4-2.9 GB; see headroom).
2. Laptop: `python deploy/multilingual-model/build_tarball.py`; confirm the sha256 above.
3. IAP scp the tarball, `MANIFEST.json` and `install_model.sh` to a scratch dir on the VM (not the hub dir); re-check `sha256sum`.
4. Record VM state first: `ls -la /opt/osint/.cache/huggingface/hub/` and `du -sh` on the multilingual dir (expected
   ~1.3 MB = partial cache, weights absent; to be verified, not assumed).
5. Dry run (default): `./install_model.sh --tarball T --expected-sha256 195b0fc5...04c62 --manifest MANIFEST.json`.
   Extracts to a `mktemp -d` under /tmp (~0.5 GB), verifies tarball sha and every file sha/size; changes nothing else.
6. Apply: same command plus `--apply`. As root it chowns to `osint:osint`; as `osint` use `--owner osint:osint`.
   Stages in `$HUB/.stage-mlmodel.*` (same filesystem, so `mv` is atomic). An existing partial multilingual dir is
   renamed `*.old-<UTC ts>`. The `all-MiniLM-L6-v2` dir is never read, written or listed by the script.
7. Run `repro_check.py --out repro-vm.json` as `osint` with the daemon env (`HF_HOME`, `HF_HUB_OFFLINE=1`) using
   `/opt/osint/venv`; copy back; `compare_repro.py repro-laptop.json repro-vm.json`.
8. Idempotent: if everything already verifies the script prints "already installed" and exits 0.

## Rollback
`rm -rf /opt/osint/.cache/huggingface/hub/models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2`
(plus any `.old-*` copy). The install changes no other directory, config, env file or service.

## Footprint (laptop CPU, torch threads=2, `footprint.py`)
- Disk: 479.7 MB needed files (470.6 MB fp32 weights, 9.1 MB tokenizer); tarball 435.6 MB.
- RSS (Windows working set): 422 MB after importing torch + sentence-transformers; 834 MB after load (**+412 MB**);
  peak 870 MB after 5 x encode of 256 short texts, batch 32 (**+448 MB total**). Load 6.3 s.
- Throughput: best 25.4 texts/s (10.1 s per 256), median 11.7 s per 256. The laptop was under other load, so this is
  noisy; the VM has 2 vCPU, so expect the same order of magnitude, not the same number.
- VM headroom: ~4.8 GB available vs about +0.45 GB if run inside a process that already has torch and sentence-transformers
  loaded (as the daemon does for all-MiniLM-L6-v2), about 0.85 GB as a new process. Long texts and larger batches add
  activation memory (not measured). Safetensors is mmapped, so part of the weights may be page cache rather than RSS;
  the figures above are the conservative working-set numbers.

## Reproducibility
`repro_check.py` encodes 20 fixed sentences (en 3, es 3, it 3, fr 2, de 2, uk 2, ru 2, ar 3), float32; it writes the
sha256 of the raw embedding bytes and first-5 dims rounded to 1e-5. Laptop reference (`repro-laptop.json`, torch 2.14.0,
2 threads) bitwise sha256 **`f2b3f68b3e9a0007308a94d6cdf6e20dda512bf0639a9d15ea972c4beb86a7d0`**; two laptop runs were
bitwise identical.

**OPEN DECISION (owner/engineering): tolerance policy for laptop vs VM.** Options: (a) bitwise equality, (b) per-sentence
cosine distance <= 1e-4. PROPOSED recommendation: (b) as the gate, (a) reported as informational. Reason: laptop is
Windows and the VM is Linux, possibly with a different CPU/BLAS kernel path, so bitwise float equality is not guaranteed
even with identical package versions; 1e-4 cosine is far below anything a topic model resolves. Not an approved policy.

## Version comparison (laptop `.venv` vs VM)
Identical: Python 3.14.3, torch 2.14.0 (VM +cpu), sentence-transformers 6.1.0, transformers 5.17.0, tokenizers 0.23.2,
huggingface-hub 1.33.0, numpy 2.5.3, safetensors 0.8.0, spacy 3.8.16, scipy 1.18.1.
Laptop only: scikit-learn 1.9.1 (not on VM); spaCy models en_core_web_lg / es_core_news_md / it_core_news_md 3.8.0
(the spec says they are deployed on the VM; their VM versions were not supplied and are unverified).

## Facts to verify at install time
- The VM multilingual cache dir is 1.3 MB: weights probably absent (partial cache).
- `install_model.sh` was exercised only against a temporary hub dir on the Windows laptop (dry-run, apply with a simulated
  partial dir, idempotent rerun, L6-v2 dir untouched, model loads from the result). Git-bash tar may extract symlinks as
  copies there, so the Linux symlink path and symlink-escape guard are untested until the VM dry run.
