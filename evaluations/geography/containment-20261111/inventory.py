"""Inventory of stored Development places that resolve to NO country (containment gaps).

Runs on a backup-API copy of a snapshot; never writes the snapshot.

    python inventory.py SNAPSHOT_DB OUT.json [--classes CLASSES.yaml]

Per distinct specific place stored on any Development (``_specific_places``, the same helper Situation scope uses):
the country ancestors under the running code's gazetteer. Output: every place with zero countries, with the number
of Developments naming it. With --classes (place -> a|b|c|d), adds per-class counts, so the same script measures
before and after a fix.
"""
import argparse
import json
import os
import sqlite3
import sys
import tempfile
from collections import Counter
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot")
    ap.add_argument("out")
    ap.add_argument("--classes", type=Path)
    a = ap.parse_args()

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.database import Event
    from osint_monitor.processors.development_segmentation import gazetteer
    from osint_monitor.processors.situations.store import _specific_places

    tmp = Path(tempfile.mkdtemp(prefix="containment-")) / "copy.db"
    src = sqlite3.connect(f"file:{a.snapshot}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    geo = gazetteer(False)

    dev_count = Counter()
    for (eid,) in s.query(Event.id).order_by(Event.id):
        for p in _specific_places(s, eid):
            dev_count[p] += 1

    def countries_of(place: str) -> list[str]:
        return sorted(set(geo.ancestors(place)) & set(geo.countries))

    zero = {p: n for p, n in dev_count.items() if not countries_of(p)}
    report = {
        "snapshot": a.snapshot,
        "distinct_places": len(dev_count),
        "zero_country_places": len(zero),
        "zero_country_development_references": sum(zero.values()),
        "places": {p: {"developments": n} for p, n in sorted(zero.items(), key=lambda kv: (-kv[1], kv[0]))},
    }
    if a.classes:
        import yaml
        raw = yaml.safe_load(a.classes.read_text(encoding="utf-8"))
        cls = raw.get("classes", raw)
        by_class = Counter()
        refs_by_class = Counter()
        unclassified = []
        for p, n in zero.items():
            c = cls.get(p)
            if c is None:
                unclassified.append(p)
            else:
                by_class[c] += 1
                refs_by_class[c] += n
        report["by_class"] = {c: {"places": by_class[c], "development_references": refs_by_class[c]}
                              for c in sorted(by_class)}
        report["unclassified"] = sorted(unclassified)
    Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{report['distinct_places']} distinct places, {report['zero_country_places']} with zero countries "
          f"({report['zero_country_development_references']} Development references) -> {a.out}")
    if a.classes:
        print("by class:", {c: v["places"] for c, v in report["by_class"].items()},
              "| unclassified:", len(report.get("unclassified", [])))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
