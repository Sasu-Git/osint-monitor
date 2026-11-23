"""Small committed record of a (large, git-ignored) features file: hashes and header, no content.

    python -m upstream_harness.manifest --features features/topic-features.json [--verify-rerun other.json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .common import sha256_file, write_canonical
from .features import load_features


def build_manifest(features_path: Path) -> dict:
    body = load_features(features_path)          # verifies the content hash
    h = body["header"]
    return {"track": h["track"], "file": Path(features_path).name, "file_bytes": Path(features_path).stat().st_size,
            "file_sha256": sha256_file(features_path), "content_hash": body["content_hash"],
            "n_cases": h["n_cases"], "n_items": sum(c["members"] for c in body["cases"].values()),
            "snapshot_sha256": h["snapshot_sha256"], "cases_json_sha256_lf": h["cases_json_sha256_lf"],
            "spacy": h["spacy"], "embedding": h["embedding"], "lead": h["lead"], "excluded": h["excluded"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True, type=Path)
    ap.add_argument("--verify-rerun", type=Path, help="second extraction; must be byte-identical")
    a = ap.parse_args(argv)
    m = build_manifest(a.features)
    if a.verify_rerun:
        m["rerun_file_sha256"] = sha256_file(a.verify_rerun)
        m["rerun_byte_identical"] = m["rerun_file_sha256"] == m["file_sha256"]
    out = a.features.with_name(a.features.name.replace("-features.json", "-features.manifest.json"))
    write_canonical(out, m)
    keys = ["track", "file_sha256", "content_hash", "n_cases", "n_items"] + (["rerun_byte_identical"] if a.verify_rerun else [])
    print(json.dumps({k: m[k] for k in keys}))
    return 0 if m.get("rerun_byte_identical", True) else 1


if __name__ == "__main__":
    sys.exit(main())
