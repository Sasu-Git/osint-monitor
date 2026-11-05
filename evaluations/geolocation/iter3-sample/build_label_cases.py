"""Blind labelling cases for the iteration-3 fresh sample (read-only on the frozen snapshot).

    python build_label_cases.py --db <snap-20261105.db> --countries <d06af11>/osint_monitor/api/data/countries.json

Writes label-cases.json: per sampled Development its headline and member reports (source, time, title, first
LEAD_SHOWN characters of text), in item order. Nothing a labeller must not see is included: no stored place,
coordinates, region, map decision, stratum or rule output. Also writes countries-iso3.json (id, name) from the
map baseline's country list, for the label form's suggestions.
"""
import argparse, json, sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS_SHOWN = 25
LEAD_SHOWN = 600


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--countries", required=True)
    a = ap.parse_args()

    ids = [c["development_id"] for c in json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))["cases"]]
    db = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True)
    cases = []
    for i in ids:
        (headline,) = db.execute("select summary from events where id = ?", (i,)).fetchone()
        rows = db.execute(
            "select r.id, s.name, r.published_at, r.title, r.content from event_items ei"
            " join raw_items r on r.id = ei.item_id left join sources s on s.id = r.source_id"
            " where ei.event_id = ? order by r.id", (i,)).fetchall()
        cases.append({
            "development_id": i,
            "headline": headline,
            "members": len(rows),
            "items": [{"item_id": r[0], "source": r[1], "published_at": r[2], "title": r[3],
                       "text": (r[4] or "")[:LEAD_SHOWN]} for r in rows[:ITEMS_SHOWN]],
        })
    (HERE / "label-cases.json").write_text(json.dumps({"cases": cases}, ensure_ascii=False, indent=1),
                                           encoding="utf-8", newline="\n")
    countries = sorted(({"id": c["id"], "name": c["name"]} for c in json.loads(
        Path(a.countries).read_text(encoding="utf-8"))), key=lambda c: c["name"])
    (HERE / "countries-iso3.json").write_text(json.dumps(countries, ensure_ascii=False, indent=0),
                                              encoding="utf-8", newline="\n")
    print(len(cases), "cases,", sum(c["members"] for c in cases), "member reports,", len(countries), "countries")


if __name__ == "__main__":
    main()
