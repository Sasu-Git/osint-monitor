"""Gold-completion checker (library + CLI). Called by the scorer before anything else.

    python -m upstream_harness.checker --gold-root <dir> [--track topic|location|both] [--require all|development|acceptance]

Exit 0 only if, for every requested track: the frozen inputs match the sha256 block of FREEZE.md; the split is
complete, disjoint, covers the sample and equals the output of split.py; the labels are frozen
(label_server --freeze marker present and matching labels.yaml / label-history.jsonl); every case in the required set
has a primary label (first answer) and a final label; every label is valid against the taxonomy / vocabulary.
Output is counts and case ids only; label values are never printed.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .common import TRACKS, sha256_file, sha256_text_lf
from .gold import GoldError, GoldTrack, label_problems, parse_freeze_md


@dataclass
class TrackCheck:
    track: str
    problems: list[str] = field(default_factory=list)
    counts: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.problems


class GoldIncomplete(GoldError):
    def __init__(self, results: list[TrackCheck]):
        self.results = results
        super().__init__(format_results(results))


def _regen_split(root: Path, track: GoldTrack) -> bytes | None:
    """Run split.py on a temporary copy of the (frozen) manifests and return the track's split.json bytes."""
    sp = root / "split.py"
    if not sp.exists():
        return None
    with tempfile.TemporaryDirectory(prefix="split-regen-") as td:
        t = Path(td)
        shutil.copy2(sp, t / "split.py")
        for name in TRACKS:
            m = root / name / "manifest.json"
            if m.exists():
                (t / name).mkdir()
                shutil.copy2(m, t / name / "manifest.json")
        r = subprocess.run([sys.executable, "-I", str(t / "split.py")], capture_output=True, text=True, cwd=td)
        out = t / track.track / "split.json"
        if r.returncode != 0 or not out.exists():
            return None
        return out.read_bytes()


def split_problems(root: Path, tr: GoldTrack) -> list[str]:
    """Frozen-input hashes (FREEZE.md), split completeness / disjointness, split.json == split.py output."""
    out: list[str] = []
    P = out.append
    for p in (tr.cases_path, tr.manifest_path, tr.split_path):
        if not p.exists():
            P(f"missing file {p.name}")
    if out:
        return out
    try:
        pins = parse_freeze_md(root)
    except FileNotFoundError:
        pins = {}
        P("FREEZE.md missing")
    rels = [f"{tr.track}/cases.json", f"{tr.track}/manifest.json", f"{tr.track}/split.json",
            f"{tr.track}/label_server.py", "split.py", "sample.py"]
    for rel in rels:
        f = root / rel
        if rel not in pins:
            P(f"{rel}: no sha256 pinned in FREEZE.md")
        elif not f.exists():
            P(f"{rel}: file missing")
        elif sha256_text_lf(f) != pins[rel]:
            P(f"{rel}: sha256 differs from FREEZE.md")
    cases = tr.cases()
    manifest_ids = sorted(c["development_id"] for c in json.loads(tr.manifest_path.read_text(encoding="utf-8"))["cases"])
    s = tr.split()
    dev, acc = set(s["development"]), set(s["acceptance"])
    if dev & acc:
        P(f"split: {len(dev & acc)} cases in both development and acceptance")
    if dev | acc != set(cases):
        P("split: development + acceptance does not equal the case set")
    if sorted(cases) != manifest_ids:
        P("cases.json and manifest.json list different cases")
    if len(s["development"]) != len(dev) or len(s["acceptance"]) != len(acc):
        P("split: duplicate ids")
    regen = _regen_split(root, tr)
    if regen is None:
        P("split: split.py could not be re-run")
    elif regen != tr.split_path.read_bytes().replace(b"\r\n", b"\n"):
        P("split: split.json differs from split.py output")
    return out


def check_track(root: Path, track_name: str, require: str = "all") -> TrackCheck:
    res = TrackCheck(track_name)
    P = res.problems.append
    tr = GoldTrack(root, track_name)
    res.problems += split_problems(root, tr)
    if any(x.startswith("missing file") for x in res.problems):
        return res
    cases = tr.cases()

    # 3. labels frozen
    if not tr.freeze_path.exists():
        P("labels not frozen (labels-freeze.json absent)")
    else:
        fr = json.loads(tr.freeze_path.read_text(encoding="utf-8"))
        if not tr.labels_path.exists() or fr.get("labels_sha256") != sha256_file(tr.labels_path):
            P("labels.yaml differs from the freeze record")
        hs = sha256_file(tr.history_path) if tr.history_path.exists() else None
        if fr.get("history_sha256") != hs:
            P("label-history.jsonl differs from the freeze record")
        if fr.get("cases") != len(cases):
            P("freeze record case count differs from the case set")

    # 4. labels present and valid in the required set
    required = tr.split_ids(require)
    final, primary = tr.load_final(), tr.load_primary()
    vocab = tr.vocabulary()
    roles = tr.role_subset_ids()
    stray = sorted((set(final) | set(primary)) - set(cases))
    if stray:
        P(f"labels for cases outside the sample: {stray[:10]}")
    counts = {}
    for which in ("development", "acceptance"):
        ids = tr.split_ids(which)
        counts[which] = {
            "cases": len(ids),
            "required": require in ("all", which),
            "primary_labelled": sum(i in primary for i in ids),
            "final_labelled": sum(i in final for i in ids),
        }
    for i in required:
        if i not in primary:
            P(f"D{i}: no primary label")
        if i not in final:
            P(f"D{i}: no final label")
        item_ids = [it["item_id"] for it in cases[i]["items"]]
        for basis in (primary, final):
            if i in basis:
                for x in label_problems(tr, vocab, i, basis[i], roles, item_ids):
                    if x not in res.problems:
                        P(x)
    counts["labels_frozen"] = tr.freeze_path.exists()
    res.counts = counts
    return res


def check(gold_root: Path | str, tracks: tuple[str, ...] = TRACKS, require: str = "all") -> list[TrackCheck]:
    root = Path(gold_root)
    return [check_track(root, t, require) for t in tracks]


def require_complete(gold_root: Path | str, tracks: tuple[str, ...], require: str = "all") -> list[TrackCheck]:
    """Library entry used by the scorer: raises GoldIncomplete unless every requested track passes."""
    results = check(gold_root, tracks, require)
    if not all(r.ok for r in results):
        raise GoldIncomplete(results)
    return results


def format_results(results: list[TrackCheck], max_problems: int = 15) -> str:
    lines = []
    for r in results:
        lines.append(f"[{r.track}] {'PASS' if r.ok else 'REFUSE'}")
        for which in ("development", "acceptance"):
            c = r.counts.get(which)
            if c:
                lines.append(f"  {which}: {c['cases']} cases, primary labelled {c['primary_labelled']}, "
                             f"final labelled {c['final_labelled']}{'' if c['required'] else ' (not required)'}")
        if "labels_frozen" in r.counts:
            lines.append(f"  labels frozen: {r.counts['labels_frozen']}")
        for p in r.problems[:max_problems]:
            lines.append(f"  - {p}")
        if len(r.problems) > max_problems:
            lines.append(f"  - ... {len(r.problems) - max_problems} more problems")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Gold-completion checker")
    ap.add_argument("--gold-root", required=True, type=Path)
    ap.add_argument("--track", choices=[*TRACKS, "both"], default="both")
    ap.add_argument("--require", choices=["all", "development", "acceptance"], default="all")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    tracks = TRACKS if a.track == "both" else (a.track,)
    results = check(a.gold_root, tracks, a.require)
    if a.json:
        print(json.dumps([{"track": r.track, "ok": r.ok, "counts": r.counts, "problems": r.problems} for r in results],
                         indent=1))
    else:
        print(format_results(results))
    if not all(r.ok for r in results):
        print("REFUSED: gold is not complete; nothing may be scored.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
