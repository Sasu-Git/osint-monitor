#!/usr/bin/env bash
# Install the multilingual embedding model into the HF hub cache. NOT RUN by the package builder.
# Default is DRY-RUN; pass --apply to change anything. Idempotent. Never touches other model dirs.
#
# Usage: install_model.sh --tarball PATH --expected-sha256 HEX --manifest PATH [--hub-dir DIR]
#                         [--owner osint:osint] [--apply]
set -euo pipefail

TARBALL=""; EXPECTED=""; MANIFEST=""; HUB="/opt/osint/.cache/huggingface/hub"; OWNER="osint:osint"; APPLY=0
DIRNAME="models--sentence-transformers--paraphrase-multilingual-MiniLM-L12-v2"
REV="e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
while [ $# -gt 0 ]; do case "$1" in
  --tarball) TARBALL="$2"; shift 2;; --expected-sha256) EXPECTED="$2"; shift 2;;
  --manifest) MANIFEST="$2"; shift 2;; --hub-dir) HUB="$2"; shift 2;;
  --owner) OWNER="$2"; shift 2;; --apply) APPLY=1; shift;; --dry-run) APPLY=0; shift;;
  *) echo "unknown arg $1" >&2; exit 2;; esac; done
[ -f "$TARBALL" ] && [ -n "$EXPECTED" ] && [ -f "$MANIFEST" ] || { echo "need --tarball --expected-sha256 --manifest" >&2; exit 2; }
[ "$APPLY" = 1 ] && echo "MODE: APPLY" || echo "MODE: DRY-RUN (no changes; pass --apply)"
run() { if [ "$APPLY" = 1 ]; then "$@"; else echo "  [dry-run] $*"; fi; }

echo "1. verify tarball sha256"
ACTUAL=$(sha256sum "$TARBALL" | cut -d' ' -f1)
[ "$ACTUAL" = "$EXPECTED" ] || { echo "FAIL tarball sha mismatch: $ACTUAL != $EXPECTED" >&2; exit 1; }
echo "   ok $ACTUAL"

TARGET="$HUB/$DIRNAME"
# every manifest file sha must verify against the existing install -> already installed
verify_dir() { # $1 = snapshot dir ; uses python3 stdlib only (no venv needed)
  python3 - "$MANIFEST" "$1" <<'PY'
import hashlib, json, os, sys
m = json.load(open(sys.argv[1])); snap = sys.argv[2]; bad = 0
for f in m["files"]:
    if not f["needed_for_inference"]: continue
    p = os.path.join(snap, f["path"])
    if not os.path.isfile(p): print("MISSING", f["path"]); bad += 1; continue
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    if h.hexdigest() != f["sha256"] or os.path.getsize(p) != f["size"]:
        print("MISMATCH", f["path"]); bad += 1
print("verified" if not bad else "FAILED", "(%d bad)" % bad); sys.exit(1 if bad else 0)
PY
}
if [ -d "$TARGET/snapshots/$REV" ] && verify_dir "$TARGET/snapshots/$REV" >/dev/null 2>&1 \
   && [ "$(cat "$TARGET/refs/main" 2>/dev/null)" = "$REV" ]; then
  echo "already installed and verified at $TARGET -> nothing to do"; exit 0
fi
[ -d "$TARGET" ] && echo "NOTE: $TARGET exists but is incomplete/different (partial cache expected); will be replaced atomically, old copy kept as .old-<ts>"

if [ "$APPLY" = 1 ]; then STAGE=$(mktemp -d "$HUB/.stage-mlmodel.XXXXXX"); else STAGE=$(mktemp -d); fi  # apply: same fs as target => atomic mv
trap 'rm -rf "$STAGE"' EXIT
echo "2. extract to staging $STAGE"
tar -xzf "$TARBALL" -C "$STAGE" --no-same-owner
[ -d "$STAGE/$DIRNAME" ] || { echo "FAIL tarball layout" >&2; exit 1; }
# refuse anything outside the one model dir
[ "$(ls -A "$STAGE" | wc -l)" = 1 ] || { echo "FAIL tarball has extra top-level entries" >&2; exit 1; }
[ "$(cat "$STAGE/$DIRNAME/refs/main")" = "$REV" ] || { echo "FAIL refs/main != pinned revision" >&2; exit 1; }
echo "3. verify every file against MANIFEST (sha256 + size, symlinks resolved)"
verify_dir "$STAGE/$DIRNAME/snapshots/$REV" || { echo "FAIL manifest verification" >&2; exit 1; }
# no symlink may escape the model dir
if find "$STAGE/$DIRNAME" -type l -exec readlink -f {} \; | grep -v "^$STAGE/$DIRNAME/" >/dev/null; then
  echo "FAIL symlink escapes model dir" >&2; exit 1; fi

echo "4. ownership + atomic move"
run chown -R "$OWNER" "$STAGE/$DIRNAME"
run chmod -R u=rwX,go=rX "$STAGE/$DIRNAME"
if [ -d "$TARGET" ]; then run mv "$TARGET" "$TARGET.old-$(date -u +%Y%m%dT%H%M%SZ)"; fi
run mv "$STAGE/$DIRNAME" "$TARGET"
if [ "$APPLY" = 1 ]; then
  verify_dir "$TARGET/snapshots/$REV" && echo "INSTALLED at $TARGET"
else echo "DRY-RUN complete: extraction and manifest verification passed; nothing moved."; fi
