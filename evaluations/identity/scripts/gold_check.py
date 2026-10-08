"""Consistency checks for the frozen Development-identity gold (run after every revision).

1 hashes: every file in gold/manifest.yaml matches its SHA-256
2 history: each previous revision's gold and verdict hashes match the git blobs of the commit that froze it
3 integrity: case ids unique, labels valid, two distinct items per case, items exist in their frozen window,
  splits agree with the windows manifest
4 holdout: every holdout case is byte-for-byte the same as in revision 1
5 changes: the labels that differ from the previous revision are exactly the recorded changes; nothing else in
  any case changed except the label and its source; owner notes are verbatim from owner-verdicts.yaml
6 totals: the expected counts (``--expect SAME,DIFFERENT,AMBIGUOUS``) and the case count
7 revision 3 additions (when present): integrity as in 3, development split only, notes verbatim from
  review-rev3/owner-verdicts.yaml, ids disjoint from the main gold, counts (``--expect-additions S,D,A``)

Usage: python evaluations/identity/scripts/gold_check.py [--expect 68,120,1] [--cases 189] [--holdout 30]
       [--expect-additions 39,35,0]
"""
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
REL = "evaluations/identity/"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import verdicts as V  # noqa: E402


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def blob(commit: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{commit}:{REL}{path}"], cwd=REPO, capture_output=True,
                          check=True).stdout


def main() -> int:
    failures = []

    def check(n, ok, msg):
        if not ok:
            failures.append(f"[{n}] {msg}")

    m = yaml.safe_load((ROOT / "gold" / "manifest.yaml").read_text(encoding="utf-8"))
    for path, digest in m["sha256"].items():
        check(1, hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, f"{path} hash mismatch")
    gold = yaml.safe_load((ROOT / "gold" / "identity-gold.yaml").read_text(encoding="utf-8"))

    revisions = m.get("previous_revisions") or []
    check(2, [r["revision"] for r in revisions] == list(range(m["revision"] - 1, 0, -1)),
          f"revision history {[r['revision'] for r in revisions]} for revision {m['revision']}")
    rev1 = None
    for r in revisions:
        for path in ("gold/identity-gold.yaml", "review/owner-verdicts.yaml"):
            data = blob(r["git"], path)
            check(2, hashlib.sha256(data).hexdigest() == r["sha256"][path],
                  f"revision {r['revision']} {path} != blob at {r['git']}")
        if r["revision"] == 1:
            rev1 = yaml.safe_load(blob(r["git"], "gold/identity-gold.yaml"))

    windows = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))["windows"]
    by_window = {w["id"]: w for w in windows}
    items = {}
    for w in windows:
        lines = (ROOT / w["items_file"]).resolve().read_text(encoding="utf-8").splitlines()
        items[w["id"]] = {json.loads(line)["id"] for line in lines if line.strip()}
    for cid, e in gold.items():
        check(3, e["label"] in V.VERDICTS, f"{cid} label {e['label']}")
        check(3, e["a"] != e["b"], f"{cid} pairs an item with itself")
        check(3, e["window"] in by_window and e["split"] == by_window[e["window"]]["split"], f"{cid} split/window")
        check(3, e["a"] in items.get(e["window"], ()) and e["b"] in items.get(e["window"], ()),
              f"{cid} item not in its frozen window")
    check(3, len(gold) == len(set(gold)), "duplicate case ids")

    holdout = {k: v for k, v in gold.items() if v["split"] == "holdout"}
    check(4, len(holdout) == int(arg("--holdout", 30)), f"{len(holdout)} holdout cases")
    if rev1:
        for cid, e in holdout.items():
            check(4, rev1.get(cid) == e, f"holdout case {cid} changed since revision 1")

    if revisions:
        prev_rev = revisions[0]
        prev = yaml.safe_load(blob(prev_rev["git"], "gold/identity-gold.yaml"))
        changed = sorted(k for k in gold if prev[k]["label"] != gold[k]["label"])
        recorded = sorted(c["case"] for c in m.get("changes_from_previous") or [] if c["case"] in gold)
        check(5, changed == recorded, f"changed {changed} != recorded {recorded}")
        for cid in gold:
            other = {k for k in gold[cid] if gold[cid][k] != prev[cid][k]} - {"label", "source"}
            check(5, not other, f"{cid}: fields {sorted(other)} changed")
    owner = V.load(sorted(gold))
    for cid, e in gold.items():
        check(5, e["note"] == owner[cid]["note"], f"{cid} note not verbatim")

    add_path = ROOT / "gold" / "identity-gold-rev3-additions.yaml"
    if m["revision"] >= 3:
        adds = yaml.safe_load(add_path.read_text(encoding="utf-8"))
        owner3 = yaml.safe_load((ROOT / "review-rev3" / "owner-verdicts.yaml").read_text(encoding="utf-8"))
        for cid, e in adds.items():
            check(7, cid not in gold, f"{cid} also in the main gold")
            check(7, e["label"] in V.VERDICTS and e["a"] != e["b"], f"{cid} label/items")
            check(7, e["split"] == "development" and by_window.get(e["window"], {}).get("split") == "development",
                  f"{cid} not a development case")
            check(7, e["a"] in items.get(e["window"], ()) and e["b"] in items.get(e["window"], ()),
                  f"{cid} item not in its frozen window")
            check(7, e["note"] == owner3[cid].get("note") and e["label"] == owner3[cid]["verdict"],
                  f"{cid} label/note not verbatim")
        if revisions and m["revision"] >= 4:     # addition labels changed only where recorded
            try:
                prev_adds = yaml.safe_load(blob(revisions[0]["git"], "gold/identity-gold-rev3-additions.yaml"))
            except subprocess.CalledProcessError:
                prev_adds = None
            if prev_adds:
                changed_a = sorted(k for k in adds if prev_adds[k]["label"] != adds[k]["label"])
                recorded_a = sorted(c["case"] for c in m.get("changes_from_previous") or [] if c["case"] in adds)
                check(7, changed_a == recorded_a, f"addition changes {changed_a} != recorded {recorded_a}")
        ac = Counter(e["label"] for e in adds.values())
        exp_a = [int(x) for x in arg("--expect-additions", "39,35,0").split(",")]
        got_a = [ac["SAME_DEVELOPMENT"], ac["DIFFERENT_DEVELOPMENT"], ac["AMBIGUOUS"]]
        check(7, got_a == exp_a, f"additions SAME/DIFFERENT/AMBIGUOUS {got_a} != expected {exp_a}")
        print(f"revision 3 additions: {len(adds)} cases, SAME {got_a[0]}, DIFFERENT {got_a[1]}, AMBIGUOUS {got_a[2]}")

    counts = Counter(e["label"] for e in gold.values())
    exp = [int(x) for x in arg("--expect", "68,120,1").split(",")]
    got = [counts["SAME_DEVELOPMENT"], counts["DIFFERENT_DEVELOPMENT"], counts["AMBIGUOUS"]]
    check(6, got == exp, f"counts SAME/DIFFERENT/AMBIGUOUS {got} != expected {exp}")
    check(6, len(gold) == int(arg("--cases", 189)), f"{len(gold)} cases")

    print(f"revision {m['revision']}: {len(gold)} cases, SAME {got[0]}, DIFFERENT {got[1]}, AMBIGUOUS {got[2]}; "
          f"holdout {len(holdout)}; history {[r['revision'] for r in revisions]}")
    for f in failures:
        print("FAIL", f)
    print("gold check:", "FAILED" if failures else f"passed (checks 1-{7 if m['revision'] >= 3 else 6})")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
