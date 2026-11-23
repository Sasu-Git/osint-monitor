"""Shared constants/helpers for the multilingual model package (no network, no installs)."""
import hashlib, os, pathlib

REPO_ID = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
REVISION = "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
CACHE_DIR_NAME = "models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2"
# Inference needs these only (safetensors only; no pytorch_model.bin, no README).
NEEDED = [
    "1_Pooling/config.json", "config.json", "config_sentence_transformers.json",
    "model.safetensors", "modules.json", "sentence_bert_config.json",
    "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json",
]
LFS = {"model.safetensors"}  # LFS upstream => blob name is sha256; others use git blob sha1 (cosmetic)


def hub_dir():
    root = os.environ.get("HF_HUB_CACHE") or os.path.join(
        os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface")), "hub")
    return pathlib.Path(root)


def snapshot_dir():
    return hub_dir() / CACHE_DIR_NAME / "snapshots" / REVISION


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def git_blob_sha1(p):
    data = pathlib.Path(p).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
