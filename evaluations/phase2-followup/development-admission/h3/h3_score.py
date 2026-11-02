"""H3 feasibility check (EXPERIMENT-PLAN.md step 3): DA1's Development-level test on the 8 giants, scored against the
frozen owner labels. Offline, read-only, no runtime change, no variant implementation.

    python h3_score.py --code-wt <osint-monitor-timing @ adacb83> --db <snapshot-20261027-forensic.db> --out h3-results.json

Applied exactly as written in ARCHITECTURE.md, nothing tuned:

Core (section 4, DA1): from the giant's founder set F (dataset/giant-label-sample.json):
  1. eligible = founders whose headline kind is REPORT, plus primary/official evidence (ProvenanceResolver on F);
  2. seed pair = eligible pair with compatible_link and different provenance origins; highest full-text cosine wins,
     ties to the earliest publication, then the lowest ids;
  3. growth = repeatedly add the eligible item compatibly linked to every kernel member, highest minimum cosine first,
     until 5 items or none qualifies;
  4. DA1 fallback when no seed pair exists: the founder set, at most 5, earliest first.
core_compatible(item, core) (section 5), all of:
  C-sem   full-text cosine >= LINK_SIMILARITY (0.53) to at least ceil(|core|/2) core members;
  C-head  only when the item's headline is a REPORT: headline cosine >= min_headline_similarity (0.5) to at least one
          REPORT core member, or P7 occurrence_evidence with a core member;
  C-place if the item and the core's union of places both name places, they must be compatible (gazetteer
          containment, use_regions false: places_compatible with the frozen segmentation config).
DA1 rejects an L2 member when core_compatible is False (the member already had its local link: it attached).

Gate (plan step 3): F1 = share of L2-DIFFERENT members rejected >= 60%; F2 = share of L2-SAME members rejected <= 10%.
AMBIGUOUS members are reported separately and excluded from F1/F2 (the plan defines F1/F2 on SAME and DIFFERENT only).
"""
from __future__ import annotations

import argparse, ctypes, hashlib, json, math, os, subprocess, sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DA = HERE.parent


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float] | None:
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 4), round(c + h, 4))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-wt", type=Path, required=True)
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    code_sha = subprocess.run(["git", "-C", str(a.code_wt), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "-C", str(a.code_wt), "status", "--porcelain", "--untracked-files=no"],
                                capture_output=True, text=True).stdout.strip())
    freeze = json.loads((DA / "labelling" / "FREEZE-LABELLING.json").read_text(encoding="utf-8"))
    assert code_sha == freeze["code"]["sha"] and not dirty, f"code {code_sha} dirty={dirty} != frozen {freeze['code']['sha']}"
    os.environ["OSINT_DB_URL"] = f"sqlite:///file:{a.db.resolve().as_posix()}?mode=ro&uri=true"
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    sys.path.insert(0, str(a.code_wt.resolve()))

    import yaml
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.core.models import EvidenceType
    from osint_monitor.processors.clustering import LINK_SIMILARITY
    from osint_monitor.processors.development_segmentation import (
        REPORT, _cosine, compatible_link, headline_kind, occurrence_evidence, places_compatible, segment_items)
    from osint_monitor.processors.provenance import ProvenanceResolver, build_evidence

    cfg = load_event_grouping_config().development_segmentation
    assert LINK_SIMILARITY == 0.53 and cfg.min_headline_similarity == 0.5 and cfg.location_match == "containment" \
        and cfg.use_regions is False, "frozen thresholds changed"
    session = sessionmaker(bind=create_engine(f"sqlite:///file:{a.db.resolve().as_posix()}?mode=ro&uri=true"))()

    key = json.loads((DA / "labelling" / "key.json").read_text(encoding="utf-8"))
    labels = yaml.safe_load((DA / "labelling" / "owner-labels.yaml").read_text(encoding="utf-8"))
    giants = {g["event_id"]: g for g in json.loads((DA / "dataset" / "giant-label-sample.json").read_text(encoding="utf-8"))}
    cases = sorted((c, k) for c, k in key.items() if k["set"] == "L2")
    resolver = ProvenanceResolver()

    out = {"inputs": {"code_sha": code_sha, "db": str(a.db), "labels_sha256":
                      hashlib.sha256((DA / "labelling" / "owner-labels.yaml").read_bytes().replace(b"\r\n", b"\n")).hexdigest()},
           "thresholds": {"link_similarity": LINK_SIMILARITY, "min_headline_similarity": cfg.min_headline_similarity,
                          "location_match": cfg.location_match, "use_regions": cfg.use_regions},
           "giants": {}, "cases": []}
    cores = {}
    for eid, g in sorted(giants.items()):
        founder_ids = [f["item_id"] for f in g["founders"]]
        ev = [e for e in build_evidence(session, eid) if e.item_id in set(founder_ids)]
        prov = {p.item_id: p for p in resolver.resolve(ev)}
        items = segment_items(session, founder_ids, cfg)
        eligible = sorted(i for i in items if headline_kind(items[i].title) == REPORT
                          or (i in prov and prov[i].evidence_type == EvidenceType.PRIMARY))
        pub = lambda i: items[i].published_at or datetime.max
        seeds = []
        for x in range(len(eligible)):
            for y in range(x + 1, len(eligible)):
                i, j = eligible[x], eligible[y]
                if prov.get(i) and prov.get(j) and prov[i].origin != prov[j].origin and compatible_link(items[i], items[j], cfg):
                    seeds.append((-_cosine(items[i].vector, items[j].vector), min(pub(i), pub(j)), min(i, j), max(i, j)))
        if seeds:
            _, _, s1, s2 = min(seeds)
            core, how = [s1, s2], "kernel"
            while len(core) < 5:
                cand = []
                for i in eligible:
                    if i in core or not all(compatible_link(items[i], items[k], cfg) for k in core):
                        continue
                    cand.append((-min(_cosine(items[i].vector, items[k].vector) for k in core), pub(i), i))
                if not cand:
                    break
                core.append(min(cand)[2])
        else:
            core, how = sorted(items, key=lambda i: (pub(i), i))[:5], "founder-set fallback"
        cores[eid] = core
        out["giants"][eid] = {"founders": len(founder_ids), "founders_with_embedding": len(items),
                              "eligible": len(eligible), "core": core, "core_rule": how,
                              "core_titles": [items[i].title for i in core]}

    for case, k in cases:
        eid, cand = k["event_id"], k["candidate_item"]
        core = cores[eid]
        items = segment_items(session, core + [cand], cfg)
        lab = labels[case]["label"]
        rec = {"case": case, "event_id": eid, "item": cand, "reference_item": k["reference_item"],
               "stratum": k.get("stratum"), "label": lab}
        if cand not in items:
            rec.update(scorable=False, reason="no stored embedding")
            out["cases"].append(rec)
            continue
        it, core_items = items[cand], [items[i] for i in core if i in items]
        need = math.ceil(len(core_items) / 2)
        sem_hits = [c.id for c in core_items if _cosine(it.vector, c.vector) >= LINK_SIMILARITY]
        c_sem = len(sem_hits) >= need
        if headline_kind(it.title) == REPORT:
            reports = [c for c in core_items if headline_kind(c.title) == REPORT]
            head_hits = [c.id for c in reports if it.headline_vector is not None and c.headline_vector is not None
                         and _cosine(it.headline_vector, c.headline_vector) >= cfg.min_headline_similarity]
            p7 = [c.id for c in reports if occurrence_evidence(it, c, cfg)]
            c_head = bool(head_hits or p7)
            head_note = {"headline_hits": head_hits, "p7": p7}
        else:
            c_head, head_note = True, {"skipped": headline_kind(it.title)}
        core_places = set().union(*(c.locations for c in core_items)) if core_items else set()
        c_place = not (it.locations and core_places) or places_compatible(it.locations, core_places, cfg)
        compatible = c_sem and c_head and c_place
        rec.update(scorable=True, title=it.title, rejected=not compatible, c_sem=c_sem,
                   c_sem_quorum=f"{len(sem_hits)}/{len(core_items)} (need {need})", c_head=c_head, c_head_detail=head_note,
                   c_place=c_place, item_places=sorted(it.locations), core_places=sorted(core_places))
        out["cases"].append(rec)

    scored = [c for c in out["cases"] if c["scorable"]]
    def tally(label):
        xs = [c for c in scored if c["label"] == label]
        k = sum(c["rejected"] for c in xs)
        return {"n": len(xs), "rejected": k, "share": round(k / len(xs), 4) if xs else None, "wilson95": wilson(k, len(xs))}
    f1, f2 = tally("DIFFERENT_OCCURRENCE"), tally("SAME_OCCURRENCE")
    out["summary"] = {
        "L2_cases": len(cases), "scorable": len(scored), "not_scorable": [c["case"] for c in out["cases"] if not c["scorable"]],
        "F1_different_rejected": f1, "F1_gate": ">= 0.60", "F1_pass": f1["share"] is not None and f1["share"] >= 0.60,
        "F2_same_rejected": f2, "F2_gate": "<= 0.10", "F2_pass": f2["share"] is not None and f2["share"] <= 0.10,
        "ambiguous": tally("AMBIGUOUS"),
    }
    out["summary"]["H3"] = "PASS" if out["summary"]["F1_pass"] and out["summary"]["F2_pass"] else "FAIL"
    a.out.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(json.dumps(out["summary"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
