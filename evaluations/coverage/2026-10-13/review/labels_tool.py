"""Validate owner labels against the frozen sample, and import labels made outside the review page.

    python labels_tool.py validate                       # owner-labels.yaml against sample-manifest.json
    python labels_tool.py import TEMPLATE.yaml --reviewer NAME [--write]

``validate`` checks every entry: the case is in the frozen manifest; the label is SHOULD_JOIN / SHOULD_NOT_JOIN /
AMBIGUOUS; a SHOULD_JOIN names at least one partner and every partner is one of that case's frozen partner ids;
every labelled entry names its reviewer. It prints the problems and exits 1 when there are any.

``import`` reads the exported ``labels-template.yaml`` (partners written as P1 / P2 / P3, the order the packet shows)
and maps them to the frozen partner ids. It never overwrites a case that already has a label from another reviewer
(one reviewer per case); a disagreement is reported, not merged. Without ``--write`` it only reports.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
LABELS = ("SHOULD_JOIN", "SHOULD_NOT_JOIN", "AMBIGUOUS")
FIELDS = ("label", "partners", "note", "reviewer", "labelled_at")


def frozen_partners() -> dict[str, list[int]]:
    cases = json.loads((HERE / "sample-manifest.json").read_text(encoding="utf-8"))["cases"]
    return {cid: list(c["partners"]) for cid, c in cases.items()}


def load_labels(path: Path = HERE / "owner-labels.yaml") -> dict:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.exists() else {}


def validate(labels: dict, partners: dict[str, list[int]]) -> list[str]:
    problems = []
    for cid, e in sorted(labels.items()):
        if cid not in partners:
            problems.append(f"{cid}: not in the frozen manifest")
            continue
        if not e or not e.get("label"):
            continue
        if e["label"] not in LABELS:
            problems.append(f"{cid}: label {e['label']!r}")
        chosen = e.get("partners") or []
        if e["label"] == "SHOULD_JOIN" and not chosen:
            problems.append(f"{cid}: SHOULD_JOIN without a partner")
        if any(p not in partners[cid] for p in chosen):
            problems.append(f"{cid}: partner(s) {[p for p in chosen if p not in partners[cid]]} not frozen for this case")
        if not e.get("reviewer"):
            problems.append(f"{cid}: no reviewer")
    return problems


def import_template(template: Path, reviewer: str, labels: dict, partners: dict[str, list[int]]):
    """(merged labels, report lines). Partners P1..P3 map to the frozen partner ids in packet order."""
    rows = yaml.safe_load(template.read_text(encoding="utf-8")) or {}
    merged, report = {k: dict(v or {}) for k, v in labels.items()}, []
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for cid, e in sorted(rows.items()):
        if not e or not e.get("label"):
            continue
        if cid not in partners:
            report.append(f"{cid}: not in the frozen manifest, skipped")
            continue
        label = str(e["label"]).strip().upper()
        if label not in LABELS:
            report.append(f"{cid}: label {e['label']!r} not recognised, skipped")
            continue
        ids = []
        for p in e.get("partners") or []:
            n = int(str(p).strip().upper().lstrip("P"))
            if not 1 <= n <= len(partners[cid]):
                report.append(f"{cid}: P{n} does not exist (case has {len(partners[cid])} partner(s)), skipped")
                break
            ids.append(partners[cid][n - 1])
        else:
            if label == "SHOULD_JOIN" and not ids:
                report.append(f"{cid}: SHOULD_JOIN without a partner, skipped")
                continue
            prior = merged.get(cid) or {}
            if prior.get("label") and prior.get("reviewer") not in (None, reviewer):
                agree = "agrees" if prior["label"] == label else "DISAGREES"
                report.append(f"{cid}: already labelled by {prior['reviewer']} ({prior['label']}); {reviewer} {agree} "
                              f"({label}) -- kept as is, record as a review note")
                continue
            merged[cid] = {"label": label, "partners": ids if label == "SHOULD_JOIN" else None,
                           "note": e.get("note") or None, "reviewer": reviewer, "labelled_at": now}
    return merged, report


def main(argv: list[str]) -> int:
    partners = frozen_partners()
    if argv[:1] == ["validate"]:
        labels = load_labels()
        problems = validate(labels, partners)
        n = sum(1 for e in labels.values() if e and e.get("label"))
        print(f"{n} labelled of {len(partners)} frozen cases; {len(problems)} problem(s)")
        print("\n".join(problems))
        return 1 if problems else 0
    if argv[:1] == ["import"] and len(argv) >= 2 and "--reviewer" in argv:
        reviewer = argv[argv.index("--reviewer") + 1].strip()
        if not reviewer:
            raise SystemExit("--reviewer must not be empty: anonymous labels are not merged")
        merged, report = import_template(Path(argv[1]), reviewer, load_labels(), partners)
        print("\n".join(report) or "no conflicts")
        problems = validate(merged, partners)
        if problems:
            print("validation failed:\n" + "\n".join(problems))
            return 1
        if "--write" in argv:
            out = HERE / "owner-labels.yaml"
            header = ("# Owner labels for the coverage-recoverability sample (see review_server.py for the fields).\n"
                      "# The sample, partners and key are frozen in sample-manifest.json / FREEZE.md.\n")
            full = {cid: {f: (merged.get(cid) or {}).get(f) for f in FIELDS} for cid in sorted(partners)}
            out.write_text(header + yaml.safe_dump(full, allow_unicode=True, sort_keys=True), encoding="utf-8")
            print(f"written {out}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
