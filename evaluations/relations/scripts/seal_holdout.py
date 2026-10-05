"""Seal the relation holdout before any relation logic exists.

    python evaluations/relations/scripts/seal_holdout.py

Replays the holdout windows and generates their candidate cases with the same rules as the development split,
writing holdout/runs/*.json and holdout/cases.sealed.json. Nothing about their content is printed. Then writes
holdout/SEALED.yaml with the SHA-256 of every input and output. scripts/check_sealed.py verifies it.

Opening holdout/ while relation logic is being developed or tuned breaks the seal. The holdout is labelled
blind (separate annotator, then owner) only after the implementation is frozen, and scored once.
"""
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    py = sys.executable
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    if not all((ROOT / "holdout" / "runs" / f"{w['id']}.json").exists()
               for w in manifest["windows"] if w["split"] == "holdout"):
        subprocess.run([py, str(SCRIPTS / "replay_windows.py"), "holdout"], check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    subprocess.run([py, str(SCRIPTS / "build_cases.py"), "holdout"], check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    hold = [w for w in manifest["windows"] if w["split"] == "holdout"]
    files = sorted((ROOT / "holdout").rglob("*.json"))
    sealed = {
        "sealed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "rule": "Do not open, print or score anything under holdout/ until the relation implementation is frozen. "
                "Then: blind annotator draft, owner verdicts, freeze labels, one scored run.",
        "windows": [{"id": w["id"], "items_sha256": w["items_sha256"], "occurrences": w["occurrences"]} for w in hold],
        "files": {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in files},
        "scripts": {f"scripts/{n}": sha(SCRIPTS / n) for n in ("replay_windows.py", "build_cases.py")},
    }
    (ROOT / "holdout" / "SEALED.yaml").write_text(yaml.safe_dump(sealed, sort_keys=False, width=110),
                                                 encoding="utf-8", newline="\n")
    print("sealed", len(hold), "windows,", len(files), "files")


if __name__ == "__main__":
    main()
