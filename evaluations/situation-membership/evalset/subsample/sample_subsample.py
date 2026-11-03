"""Stratified labelling subsample of the frozen 379-case Situation-membership evaluation set. Blind.

    python sample_subsample.py            writes manifest.json and owner-labels-subsample.yaml (template) here

Reads only blind or public inputs:
  * ../cases.json (verified against its frozen sha256), which carries no origin, membership or score;
  * the seed list SEED_CASES, parsed from ../build_evalset.py (public: CONTRACT-V2 section 4);
  * ../scopes.json, only for the list of automatic Situations the labels file needs a scope for.
It never opens ../key.json (sealed until LABELS-FREEZE, PREREGISTRATION section 4), owner-labels.yaml or any score.

Strata (all derivable without the key):
  * seed group: every seed case is included (10 positive, 10 negative, 9 boundary). Each seed Development is a current
    member and appears in exactly one case, so its case is found by Development id;
  * Situation: every one of the 28 open Situations is represented; seeded vs automatic comes from cases.json;
  * within a Situation's non-seed cases, two blind sub-strata:
      - "repeated": the Development appears in more than one case. A Development in several cases is unassigned, so
        every such case is a near-miss (PREREGISTRATION section 10);
      - "single": the Development appears once: a current member or a near-miss, which only the key tells apart.
Allocation per Situation: k = min(N, max(MIN_PER_SITUATION, round(FRACTION * N))) of its N non-seed cases, split
between the sub-strata in proportion, with at least one from each sub-stratum that is non-empty when k >= 2.
Draws: random.Random(SEED), sub-strata visited in sorted (Situation, sub-stratum) order, ids sorted before drawing.
"""

from __future__ import annotations

import ast
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
EVALSET = HERE.parent
CASES_SHA256 = "725d7a2d50e18e20ead4e773f17a0fdc014c2784bfb21096ac10b7550cb88b17"
SEED = 20261103
FRACTION = 0.25
MIN_PER_SITUATION = 2
LF = "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seed_cases() -> dict[str, list[int]]:
    """SEED_CASES from build_evalset.py, read as a literal (the module itself needs the runtime and is not imported)."""
    tree = ast.parse((EVALSET / "build_evalset.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "SEED_CASES" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("SEED_CASES not found in build_evalset.py")


def allocate(n_rep: int, n_single: int) -> tuple[int, int]:
    n = n_rep + n_single
    k = min(n, max(MIN_PER_SITUATION, round(FRACTION * n)))
    if n_rep == 0 or n_single == 0:
        return (k, 0) if n_rep else (0, k)
    k_rep = round(k * n_rep / n)
    if k >= 2:
        k_rep = min(max(k_rep, 1), k - 1)
    k_rep = min(k_rep, n_rep)
    k_single = min(k - k_rep, n_single)
    return k_rep, k_single


def main() -> None:
    path = EVALSET / "cases.json"
    if sha256(path) != CASES_SHA256:
        raise SystemExit("cases.json does not match its frozen hash")
    cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
    by_id = {c["case_id"]: c for c in cases}
    dev_cases = Counter(c["development"]["development_id"] for c in cases)

    seeds = seed_cases()
    seed_ids: dict[str, str] = {}
    for group, devs in seeds.items():
        for d in devs:
            hits = [c["case_id"] for c in cases if c["development"]["development_id"] == d]
            if len(hits) != 1:
                raise SystemExit(f"seed D{d}: expected exactly one case, found {hits}")
            seed_ids[hits[0]] = group

    strata: dict[tuple[str, str], list[str]] = defaultdict(list)
    kind: dict[str, str] = {}
    for c in cases:
        slug = c["situation"]["slug"]
        kind[slug] = c["situation"]["kind"]
        if c["case_id"] in seed_ids:
            continue
        sub = "repeated" if dev_cases[c["development"]["development_id"]] > 1 else "single"
        strata[(slug, sub)].append(c["case_id"])

    rng = random.Random(SEED)
    chosen: dict[str, str] = {cid: f"seed_{g}" for cid, g in seed_ids.items()}
    plan = {}
    for slug in sorted(kind):
        rep, single = sorted(strata[(slug, "repeated")]), sorted(strata[(slug, "single")])
        k_rep, k_single = allocate(len(rep), len(single))
        for sub, ids, k in (("repeated", rep, k_rep), ("single", single, k_single)):
            for cid in sorted(rng.sample(ids, k)):
                chosen[cid] = sub
        plan[slug] = {"kind": kind[slug], "non_seed": {"repeated": len(rep), "single": len(single)},
                      "drawn": {"repeated": k_rep, "single": k_single},
                      "seeds": sum(1 for cid in seed_ids if by_id[cid]["situation"]["slug"] == slug)}

    ids = sorted(chosen)
    strata_counts = Counter(chosen.values())
    manifest = {
        "evalset": "situation-membership", "subsample_of": "cases.json", "cases_sha256": CASES_SHA256,
        "seed": SEED, "fraction": FRACTION, "min_per_situation": MIN_PER_SITUATION,
        "size": len(ids),
        "counts": {
            "by_stratum": dict(sorted(strata_counts.items())),
            "by_situation_kind": dict(sorted(Counter(kind[by_id[c]["situation"]["slug"]] for c in ids).items())),
            "situations_represented": len({by_id[c]["situation"]["slug"] for c in ids}),
            "situations_open": len(kind),
        },
        "per_situation": plan,
        "case_ids": ids,
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + LF, encoding="utf-8",
                                        newline=LF)

    scopes = json.loads((EVALSET / "scopes.json").read_text(encoding="utf-8"))
    template = {
        "instructions": "Fill label (MEMBER | CONTEXT | SPILLOVER | OTHER_SITUATION | NOT_MEMBER | AMBIGUOUS), a "
                        "one-line reason and reviewer for every case; for every automatic Situation fill its intended "
                        "scope. See ../PREREGISTRATION.md and SUBSAMPLE.md. Do not open ../key.json.",
        "cases": [{"case_id": c, "label": None, "reason": None, "reviewer": None} for c in ids],
        "situation_scopes": [{"slug": a["slug"], "domains_or_types": None, "places": None, "note": None,
                              "reviewer": None} for a in scopes["automatic"]],
    }
    (HERE / "owner-labels-subsample.yaml").write_text(
        yaml.safe_dump(template, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8", newline=LF)
    print(json.dumps({k: v for k, v in manifest.items() if k not in ("case_ids", "per_situation")}, indent=1))


if __name__ == "__main__":
    main()
