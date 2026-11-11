"""Iteration 3, FREEZE.md step 3: audit the evaluation's country lookup against every gold label. Read-only.

    PYTHONPATH=<this worktree> python lookup_audit.py --countries <checkout of ab45312> [--overrides lookup-overrides.json]

The lookup maps the location module's country output (a gazetteer country name, a U4 disputed entity, a rule-5a
territory, or a rule-4a Congo name) to ISO3. It is iteration 1/2's lookup unchanged (web geo.py CountryIndex at
ab45312 + DISPUTED_ISO), plus an evaluation-local equivalence table (lookup-overrides.json) that fixes gaps. Rule code,
labels, sample and the gazetteer extension are not touched.

Checks:
  A. every country name the module can emit maps to an ISO3 code that exists in countries.json;
  B. every gold code (final labels and blind first answers) is reachable: some emittable name maps to it;
  C. every gold code is a code of the frozen labeller list (countries-iso3.json) or NONE.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SAMPLE = HERE.parent / "iter3-sample"
DISPUTED_ISO = {"west bank": "PSE", "gaza": "PSE", "east jerusalem": "PSE", "crimea": "UKR", "western sahara": "ESH"}


def load_index(countries_tree: Path):
    spec = importlib.util.spec_from_file_location("web_geo", countries_tree / "osint_monitor" / "api" / "geo.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["web_geo"] = mod
    spec.loader.exec_module(mod)
    return mod.CountryIndex.load()


def make_iso(index, overrides: dict[str, str]):
    def iso(name: str | None) -> str | None:
        if name is None:
            return None
        return overrides.get(name) or DISPUTED_ISO.get(name) or index.of_place(name)
    return iso


def emittable_names(geo) -> dict[str, str]:
    """Every country value decide() can return, with where it comes from."""
    from osint_monitor.processors import event_location as el
    names = {n: "gazetteer country" for n in geo.countries}
    names.update({v: "U4 disputed" for v in el.DISPUTED.values()})
    names.update({v: "5a territory" for v in el.TERRITORIES.values()})
    names.update({el.COD: "4a Congo", el.COG: "4a Congo"})
    for _, cands in el.load_extension().items():
        for country in cands:
            names.setdefault(country, "extension country")
    return names


def gold_codes() -> tuple[dict[int, str], dict[int, str]]:
    final = {int(k): v["event_country"] for k, v in yaml.safe_load((SAMPLE / "owner-labels.yaml").read_text(encoding="utf-8")).items()}
    first: dict[int, str] = {}
    for line in (SAMPLE / "owner-label-history.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            first.setdefault(int(r["case"]), r["event_country"])
    return final, first


def audit(index, overrides: dict[str, str]) -> dict:
    from osint_monitor.processors.geography import Gazetteer
    geo = Gazetteer.load()
    iso = make_iso(index, overrides)
    valid_ids = set(index.countries)
    names = emittable_names(geo)
    mapped = {n: iso(n) for n in sorted(names)}
    unmapped = sorted(n for n, c in mapped.items() if c is None)
    bad_id = sorted(n for n, c in mapped.items() if c is not None and c not in valid_ids)
    reachable = {c for c in mapped.values() if c}
    final, first = gold_codes()
    labeller_codes = {x["id"] for x in json.loads((SAMPLE / "countries-iso3.json").read_text(encoding="utf-8"))}
    gold = {("final", i): c for i, c in final.items()} | {("first", i): c for i, c in first.items()}
    unreachable = sorted({c for c in gold.values() if c != "NONE" and c not in reachable})
    not_in_labeller = sorted({c for c in gold.values() if c != "NONE" and labeller_codes and c not in labeller_codes})
    not_in_countries = sorted({c for c in gold.values() if c != "NONE" and c not in valid_ids})
    return {
        "emittable_names": len(names),
        "A_unmapped_names": [{"name": n, "source": names[n]} for n in unmapped],
        "A_mapped_to_unknown_id": [{"name": n, "iso": mapped[n]} for n in bad_id],
        "B_gold_codes": sorted({c for c in gold.values()}),
        "B_unreachable_gold_codes": unreachable,
        "C_gold_not_in_labeller_list": not_in_labeller,
        "C_gold_not_in_countries_json": not_in_countries,
        "mapping": {n: mapped[n] for n in sorted(names) if names[n] != "gazetteer country" or mapped[n] is None
                    or n in overrides},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--countries", type=Path, required=True)
    ap.add_argument("--overrides", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    overrides = json.loads(a.overrides.read_text(encoding="utf-8"))["overrides"] if a.overrides else {}
    rep = audit(load_index(a.countries), overrides)
    text = json.dumps(rep, indent=1, ensure_ascii=False)
    if a.out:
        a.out.write_text(text + "\n", encoding="utf-8", newline="\n")
    print(text)


if __name__ == "__main__":
    main()
