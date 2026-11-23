"""Write MANIFEST.json from the laptop HF cache snapshot (read-only)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *

snap = snapshot_dir()
files = []
for p in sorted(x for x in snap.rglob("*") if x.is_file()):
    rel = p.relative_to(snap).as_posix()
    files.append({"path": rel, "size": p.stat().st_size, "sha256": sha256_file(p),
                  "needed_for_inference": rel in NEEDED})
assert {f["path"] for f in files if f["needed_for_inference"]} == set(NEEDED)
needed = [f for f in files if f["needed_for_inference"]]
m = {
    "repo_id": REPO_ID, "revision": REVISION, "cache_dir_name": CACHE_DIR_NAME,
    "files": files,
    "total_size_all": sum(f["size"] for f in files),
    "total_size_needed": sum(f["size"] for f in needed),
    "weights_format": "safetensors",
    "weights_justification": (
        "model.safetensors (470641600 bytes) is the only weights file in the pinned snapshot; "
        "sentence-transformers 6.1.0 / transformers 5.17.0 load safetensors natively. safetensors "
        "is loaded without pickle (no arbitrary code execution) which matters for files moved onto "
        "production by hand. pytorch_model.bin is not in the laptop snapshot and is not shipped "
        "(it would double the size and needs pickle loading). The all-MiniLM-L6-v2 production model is unaffected."),
    "excluded": {"README.md": "documentation only; not read at inference"},
    "inference_loader_note": ("tokenizer.json (fast tokenizer) is present; sentencepiece.bpe.model is not in "
                              "the snapshot and not needed offline (verified by encode on the laptop)."),
}
out = pathlib.Path(__file__).parent / "MANIFEST.json"
out.write_text(json.dumps(m, indent=2) + "\n")
print(len(files), "files; needed", len(needed), m["total_size_needed"])
