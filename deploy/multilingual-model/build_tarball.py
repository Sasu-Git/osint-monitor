"""Build the HF-cache-layout tarball under data/model-packages/ (gitignored). Deterministic."""
import gzip, io, json, pathlib, sys, tarfile
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *

here = pathlib.Path(__file__).parent
manifest = json.loads((here / "MANIFEST.json").read_text())
repo_root = here.parent.parent
outdir = repo_root / "data" / "model-packages"
outdir.mkdir(parents=True, exist_ok=True)
out = outdir / "multilingual-minilm-l12-e8f8c211.tar.gz"
snap = snapshot_dir()
root = CACHE_DIR_NAME
entries = []  # (arcname, TarInfo, data|None)

def ti(name, typ, size=0, link="", mode=0o644):
    t = tarfile.TarInfo(name); t.type = typ; t.size = size; t.mode = mode
    t.mtime = 0; t.uid = t.gid = 0; t.uname = t.gname = "root"; t.linkname = link
    return t

def add_dir(n): entries.append((ti(n, tarfile.DIRTYPE, mode=0o755), None))

add_dir(root); add_dir(f"{root}/blobs"); add_dir(f"{root}/refs"); add_dir(f"{root}/snapshots")
add_dir(f"{root}/snapshots/{REVISION}")
data = (REVISION).encode()
entries.append((ti(f"{root}/refs/main", tarfile.REGTYPE, len(data)), data))
dirs = sorted({str(pathlib.PurePosixPath(p).parent) for p in NEEDED} - {"."})
for d in dirs: add_dir(f"{root}/snapshots/{REVISION}/{d}")
for rel in sorted(NEEDED):
    src = snap / rel
    blob = sha256_file(src) if rel in LFS else git_blob_sha1(src)
    b = src.read_bytes()
    # same content may map to one blob name; avoid duplicate blob entries
    if not any(e[0].name == f"{root}/blobs/{blob}" for e in entries):
        entries.append((ti(f"{root}/blobs/{blob}", tarfile.REGTYPE, len(b)), b))
    depth = rel.count("/")
    target = "../" * (depth + 2) + f"blobs/{blob}"
    entries.append((ti(f"{root}/snapshots/{REVISION}/{rel}", tarfile.SYMTYPE, link=target, mode=0o777), None))

buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as tf:
    for t, d in entries:
        tf.addfile(t, io.BytesIO(d) if d is not None else None)
with open(out, "wb") as f:
    with gzip.GzipFile(filename="", mode="wb", fileobj=f, mtime=0, compresslevel=6) as gz:
        gz.write(buf.getvalue())
print(out, out.stat().st_size, sha256_file(out))
