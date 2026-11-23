"""Sample builder for the long-horizon Development-identity evaluation (DRAFT, see SPEC.md).

    HF_HUB_OFFLINE=1 PYTHONPATH=<worktree> <main .venv python> build_sample.py \
        --snapshot <gold-snap.db> --sha256 <expected> --upstream-cases topic/cases.json location/cases.json

Read-only on the snapshot: the sha256 is verified first (stop on mismatch), the file is copied with the sqlite backup API
into a temporary directory and the copy is opened query_only. Writes cases.json (blind label input), key.json (case ->
Development, strata, features; never read by the labelling server), split.json (dev / acceptance) and manifest.json next to
this script. Stratification uses label-free features only (span, size, chain depth, cosine to founders, gap structure).

Definitions (fixed here, SPEC.md section 6):
  item time      published_at, else fetched_at (what development_segmentation uses). Members ordered by (time, item id).
  founders       members published within FOUNDER_H hours of the earliest member.
  late member    published more than LATE_H hours after the earliest member.
  chain depth    over members in time order: parent = the most cosine-similar earlier member that is link-compatible
                 (development_segmentation.compatible_link, the exact runtime pair test); no earlier link = depth 0.
  burst          maximal run of members with no gap >= BURST_GAP_H hours between consecutive members; the recurring-gap
                 stratum needs a second burst of at least 2 members.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import random
import re
import sqlite3
import statistics
import sys
import tempfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import numpy as np

HERE = Path(__file__).resolve().parent
SEED = 20261124
FOUNDER_H = 6.0
LATE_H = 48.0
BURST_GAP_H = 24.0
MIN_SIZE = 3
SIDE_ITEMS = 3                   # items shown per side
NEIGHBOUR_H = 24.0               # B-side companions are published within this many hours of the anchor
TEXT_CHARS = 600
LINK_WINDOW_H = 73.0             # compatible_link requires <= 72 h; looser bound only prefilters
LINK_COSINE = 0.53               # cross-source prefilter (the runtime cosine floor); same-source pairs are not prefiltered
DEPTH_MIN_SPAN_H = 48.0          # chain depth computed for Developments at least this long ...
DEPTH_MIN_SIZE = 4               # ... and this big (others: depth not computed, not needed for any stratum)

# gap bands, hours from the earliest founder to the B anchor: (name, lo, hi)  [lo, hi)
BANDS = [("G1_6h_48h", FOUNDER_H, 48.0), ("G2_2d_7d", 48.0, 168.0), ("G3_7d_21d", 168.0, 504.0),
         ("G4_21d_plus", 504.0, float("inf"))]

# Strata, first match wins, evaluated in this order. Thresholds are PROPOSED (SPEC.md owner decisions O6/O7).
STRATA = ["E_CHAIN_FAILURE", "C_RECURRING_GAP", "D_DRIFT_MULTIDAY", "B_CONTINUOUS_MULTIDAY", "A_SHORT"]
E_MIN_SPAN_H = 7 * 24.0
E_MIN_DEPTH = 8
D_MAX_LATE_COS = 0.55
B_MAX_GAP_H = 24.0
B_MAX_SPAN_H = 14 * 24.0
A_MIN_SPAN_H = 12.0
A_MAX_SPAN_H = 48.0
# wanted cases per stratum, Developments per stratum, cases per Development (PROPOSED sizes, owner decision O9)
PLAN = {"A_SHORT": (30, 1), "B_CONTINUOUS_MULTIDAY": (30, 1), "C_RECURRING_GAP": (30, 2),
        "D_DRIFT_MULTIDAY": (30, 2), "E_CHAIN_FAILURE": (40, 3)}
PINNED = {398: 6}                # known chaining failure: always drawn, with more cases (2 per long band)
SPLIT_ACCEPTANCE_FRACTION = 0.5


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def clean_text(s: str | None, n: int = TEXT_CHARS) -> str:
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()[:n]


def norm_url(u: str | None) -> str | None:
    if not u:
        return None
    p = urlsplit(u.strip())
    return f"{p.netloc.lower()}{p.path.rstrip('/')}" if p.netloc else None


def unit(v):
    n = np.linalg.norm(v)
    return v / n if n else v


# ------------------------------------------------------------------ data


def load_members(conn) -> dict[int, list[dict]]:
    """event_id -> members sorted by (time, item id). Developments with an unembedded member are kept; their
    features use the embedded members only."""
    q = ("select ei.event_id, r.id, coalesce(r.published_at, r.fetched_at), r.source_id, s.name, r.title, r.content, "
         "r.url, r.embedding from event_items ei join raw_items r on r.id = ei.item_id "
         "left join sources s on s.id = r.source_id")
    out: dict[int, list[dict]] = defaultdict(list)
    for e, i, t, sid, sname, title, content, url, emb in conn.execute(q):
        if t is None:
            continue
        out[e].append({"id": i, "t": datetime.fromisoformat(str(t)), "source_id": sid, "source": sname or str(sid),
                       "title": title or "", "content": content, "url": url,
                       "vec": unit(np.frombuffer(emb, dtype=np.float32)) if emb else None})
    for v in out.values():
        v.sort(key=lambda m: (m["t"], m["id"]))
    return out


def hours(a: datetime, b: datetime) -> float:
    return (b - a).total_seconds() / 3600.0


def link_matrix(mem: list[dict], link_fn) -> np.ndarray:
    """Pairwise link-compatibility restricted to pairs a runtime link could exist for (time window, cosine floor)."""
    n = len(mem)
    L = np.zeros((n, n), dtype=bool)
    for a in range(n):
        for b in range(a + 1, n):
            if hours(mem[a]["t"], mem[b]["t"]) > LINK_WINDOW_H:
                break                                   # sorted by time: later b only gets farther
            same = mem[a]["source_id"] == mem[b]["source_id"]
            if not same and float(mem[a]["vec"] @ mem[b]["vec"]) < LINK_COSINE:
                continue
            if link_fn(mem[a]["id"], mem[b]["id"]):
                L[a, b] = L[b, a] = True
    return L


def features(mem: list[dict], link_fn=None) -> dict:
    mem = [m for m in mem if m["vec"] is not None]
    t0 = mem[0]["t"]
    rel = [hours(t0, m["t"]) for m in mem]
    n = len(mem)
    founders = [k for k in range(n) if rel[k] <= FOUNDER_H]
    late = [k for k in range(n) if rel[k] > LATE_H]
    V = np.stack([m["vec"] for m in mem])
    cen = unit(V[founders].mean(axis=0))
    cos_f = V @ cen
    gaps = [rel[k] - rel[k - 1] for k in range(1, n)]
    bursts, cur = [], 1
    for g in gaps:
        if g >= BURST_GAP_H:
            bursts.append(cur)
            cur = 1
        else:
            cur += 1
    bursts.append(cur)
    f = {"size": n, "span_h": round(rel[-1], 2), "n_sources": len({m["source_id"] for m in mem}),
         "founder_n": len(founders), "late_n": len(late),
         "late_median_cos_founders": round(float(statistics.median(cos_f[late])), 4) if late else None,
         "all_median_cos_founders": round(float(statistics.median(cos_f)), 4),
         "max_gap_h": round(max(gaps), 2) if gaps else 0.0, "n_bursts": len(bursts),
         "largest_burst_share": round(max(bursts) / n, 4),
         "second_burst_n": sorted(bursts)[-2] if len(bursts) > 1 else 0,
         "chain_depth_max": None, "chain_depth_median": None, "late_no_founder_link_share": None}
    if link_fn is not None and rel[-1] >= DEPTH_MIN_SPAN_H and n >= DEPTH_MIN_SIZE:
        L = link_matrix(mem, link_fn)
        C = V @ V.T
        depth = [0] * n
        for k in range(1, n):
            cand = [j for j in range(k) if L[k, j]]
            if cand:
                depth[k] = depth[max(cand, key=lambda j: C[k, j])] + 1
        f["chain_depth_max"] = max(depth)
        f["chain_depth_median"] = statistics.median(depth)
        if late:
            f["late_no_founder_link_share"] = round(sum(1 for k in late if not L[k, founders].any()) / len(late), 4)
    return f


def assign_stratum(f: dict) -> str | None:
    span = f["span_h"]
    if span >= E_MIN_SPAN_H and (f["chain_depth_max"] or 0) >= E_MIN_DEPTH:
        return "E_CHAIN_FAILURE"
    if f["late_n"] >= 2 and f["n_bursts"] >= 2 and f["second_burst_n"] >= 2 and span >= LATE_H:
        return "C_RECURRING_GAP"
    if f["late_n"] >= 2 and f["late_median_cos_founders"] is not None and f["late_median_cos_founders"] < D_MAX_LATE_COS \
            and span >= LATE_H:
        return "D_DRIFT_MULTIDAY"
    if LATE_H <= span <= B_MAX_SPAN_H and f["late_n"] >= 1 and f["max_gap_h"] < B_MAX_GAP_H:
        return "B_CONTINUOUS_MULTIDAY"
    if A_MIN_SPAN_H <= span < A_MAX_SPAN_H and f["size"] > f["founder_n"]:
        return "A_SHORT"
    return None


# ------------------------------------------------------------------ exclusions


def identity_gold_items(identity_dir: Path) -> tuple[list[dict], dict]:
    """Items of the existing identity gold (cases' a/b) and of its replay windows, as {url_key, source, title}."""
    import yaml
    gold = yaml.safe_load((identity_dir / "gold" / "identity-gold.yaml").read_text(encoding="utf-8"))
    gold_ids = {c[k] for c in gold.values() for k in ("a", "b")}
    man = yaml.safe_load((identity_dir / "manifest.yaml").read_text(encoding="utf-8"))
    gold_items, window_items, files = [], [], {}
    for w in man["windows"]:
        p = (identity_dir / w["items_file"]).resolve()
        files[w["items_file"]] = sha256_file(p)
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            o = json.loads(line)
            rec = {"url_key": norm_url(o.get("url")), "source": (o.get("source") or "").lower(),
                   "title": (o.get("title") or "").strip().lower()}
            window_items.append(rec)
            if o.get("id") in gold_ids:
                gold_items.append(rec)
    info = {"gold_case_item_ids": len(gold_ids), "gold_items_found_in_windows": len(gold_items),
            "window_items": len(window_items), "window_files_sha256": files,
            "gold_yaml_sha256": sha256_file(identity_dir / "gold" / "identity-gold.yaml")}
    return gold_items, {"window_items_all": window_items, **info}


def match_items(members: dict[int, list[dict]], recs: list[dict]) -> set[int]:
    urls = {r["url_key"] for r in recs if r["url_key"]}
    st = {(r["source"], r["title"]) for r in recs if r["title"]}
    hit = set()
    for v in members.values():
        for m in v:
            if norm_url(m["url"]) in urls or ((m["source"] or "").lower(), m["title"].strip().lower()) in st:
                hit.add(m["id"])
    return hit


# ------------------------------------------------------------------ cases


def band_of(gap_h: float):
    for name, lo, hi in BANDS:
        if lo <= gap_h < hi:
            return name
    return None


def make_case_sides(mem: list[dict], rng: random.Random, band: str, used: set[int]):
    """(A items, B items, anchor gap hours) or None. A = earliest founders; B = a random anchor published in the band
    plus its nearest (cosine) non-founder companions within NEIGHBOUR_H of the anchor; items already used as B in another
    case of this Development are not reused."""
    mem = [m for m in mem if m["vec"] is not None]
    t0 = mem[0]["t"]
    founders = [m for m in mem if hours(t0, m["t"]) <= FOUNDER_H]
    lo, hi = next((lo, hi) for n, lo, hi in BANDS if n == band)
    cand = [m for m in mem if lo <= hours(t0, m["t"]) < hi and m["id"] not in used]
    if not cand:
        return None
    anchor = cand[rng.randrange(len(cand))]
    comp = [m for m in mem if m["id"] != anchor["id"] and m["id"] not in used and m not in founders
            and abs(hours(anchor["t"], m["t"])) <= NEIGHBOUR_H]
    comp.sort(key=lambda m: (-float(m["vec"] @ anchor["vec"]), m["id"]))
    b = sorted([anchor] + comp[:SIDE_ITEMS - 1], key=lambda m: (m["t"], m["id"]))
    return founders[:SIDE_ITEMS], b, hours(t0, anchor["t"])


def public_item(m: dict) -> dict:
    return {"source": m["source"], "published_at": m["t"].strftime("%Y-%m-%d %H:%M"), "title": m["title"],
            "text": clean_text(m["content"]) or m["title"]}


def build(conn, link_fn, excluded_devs: set[int], excluded_items: set[int], members=None, seed: int = SEED,
          plan: dict | None = None, pinned: dict | None = None) -> dict:
    plan = plan or PLAN
    pinned = PINNED if pinned is None else pinned
    members = members if members is not None else load_members(conn)
    feats, pool = {}, {s: [] for s in STRATA}
    n_frame = n_excl_dev = n_excl_item = 0
    for e in sorted(members):
        mem = members[e]
        if len([m for m in mem if m["vec"] is not None]) < MIN_SIZE:
            continue
        n_frame += 1
        if e in excluded_devs:
            n_excl_dev += 1
            continue
        if any(m["id"] in excluded_items for m in mem):
            n_excl_item += 1
            continue
        # chain depth is only needed for long Developments; compute lazily for those
        f = features(mem, link_fn)
        feats[e] = f
        if f["chain_depth_max"] is not None and len(feats) % 25 == 0 or f["size"] >= 300:
            print("features", len(feats), "dev", e, "size", f["size"], flush=True)
        s = assign_stratum(f)
        if s:
            pool[s].append(e)
    drawn: dict[str, list[int]] = {}
    cases = []
    for s in STRATA:
        want_cases, per_dev = plan[s]
        rng = random.Random(f"{seed}-{s}")
        n_dev = -(-want_cases // per_dev)
        ids = list(pool[s])
        pins = [p for p in pinned if p in ids]
        rest = [i for i in ids if i not in pins]
        chosen = pins + sorted(rng.sample(rest, min(len(rest), max(0, n_dev - len(pins)))))
        drawn[s] = chosen
        for e in chosen:
            mem = members[e]
            k = pinned.get(e, per_dev)
            f = feats[e]
            avail = [b for b, lo, hi in BANDS if any(lo <= hours(mem[0]["t"], m["t"]) < hi for m in mem
                                                      if m["vec"] is not None)]
            if s == "A_SHORT":
                avail = [b for b in avail if b == "G1_6h_48h"]
            else:
                avail = [b for b in avail if b != "G1_6h_48h"] or avail
            if e in pinned:
                bands = [avail[i % len(avail)] for i in range(k)]
            else:                                     # distinct bands first; when fewer bands than cases, repeat bands
                bands = sorted(rng.sample(avail, min(k, len(avail))))
                while len(bands) < k:
                    bands.append(avail[rng.randrange(len(avail))])
            used: set[int] = set()
            for b in bands:
                sides = make_case_sides(mem, rng, b, used)
                if not sides:
                    continue
                A, B, gap = sides
                used |= {m["id"] for m in B}
                cases.append({"development_id": e, "stratum": s, "band": b, "gap_h": round(gap, 2),
                              "a_items": [m["id"] for m in A], "b_items": [m["id"] for m in B],
                              "_a": [public_item(m) for m in A], "_b": [public_item(m) for m in B]})
    # blind order: shuffle, then assign opaque sequential ids so neither id nor order reveals stratum or Development
    random.Random(f"{seed}-order").shuffle(cases)
    for k, c in enumerate(cases, 1):
        c["case_id"] = f"LH{k:03d}"
    pool_sizes = {s: len(pool[s]) for s in STRATA}
    for c in cases:
        c["stratum_pool_size"] = pool_sizes[c["stratum"]]
        c["development_features"] = feats[c["development_id"]]
    # dev / acceptance split: by Development, stratified, fixed seed
    split = {}
    for s in STRATA:
        devs = sorted(drawn[s])
        r = random.Random(f"{seed}-split-{s}")
        r.shuffle(devs)
        n_acc = int(round(len(devs) * SPLIT_ACCEPTANCE_FRACTION))
        acc = set(devs[:n_acc])
        for c in cases:
            if c["stratum"] == s:
                split[c["case_id"]] = "acceptance" if c["development_id"] in acc else "development"
    return {"cases": sorted(cases, key=lambda c: c["case_id"]), "split": split, "pool_sizes": pool_sizes,
            "drawn_developments": {s: len(v) for s, v in drawn.items()},
            "frame": {"developments_ge_min_size": n_frame, "excluded_upstream_dev_id": n_excl_dev,
                      "excluded_identity_gold_item": n_excl_item, "eligible": len(feats)}}


def blind_cases(cases: list[dict]) -> dict:
    return {"cases": [{"case_id": c["case_id"], "a": {"items": c["_a"]}, "b": {"items": c["_b"]}} for c in cases]}


def key_of(cases: list[dict]) -> dict:
    return {"cases": [{k: v for k, v in c.items() if not k.startswith("_")} for c in cases]}


# ------------------------------------------------------------------ main


def real_link_fn(copy_db: Path, members: dict[int, list[dict]]):
    from sqlalchemy import create_engine, event
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.config import load_event_grouping_config
    from osint_monitor.processors.development_segmentation import compatible_link, segment_items

    engine = create_engine(f"sqlite:///{copy_db.as_posix()}")

    @event.listens_for(engine, "connect")
    def _q(c, _):
        c.execute("PRAGMA query_only=ON")
    session = sessionmaker(bind=engine)()
    cfg = load_event_grouping_config().development_segmentation
    need = sorted({m["id"] for v in members.values() for m in v if m["vec"] is not None
                   and len(v) >= DEPTH_MIN_SIZE and hours(v[0]["t"], v[-1]["t"]) >= DEPTH_MIN_SPAN_H})
    seg = {}
    for k in range(0, len(need), 4000):
        seg.update(segment_items(session, need[k:k + 4000], cfg))
    print("segment items", len(seg), flush=True)
    return lambda a, b: a in seg and b in seg and compatible_link(seg[a], seg[b], cfg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--sha256", required=True)
    ap.add_argument("--identity-dir", default=str(HERE.parents[1] / "identity"))
    ap.add_argument("--upstream-cases", nargs="*", default=[])
    ap.add_argument("--out", default=str(HERE))
    a = ap.parse_args()
    got = sha256_file(a.snapshot)
    if got != a.sha256:
        sys.exit(f"HASH MISMATCH {got} != {a.sha256}")
    out = Path(a.out)
    tmp = Path(tempfile.mkdtemp(prefix="lhid-snap-"))
    copy = tmp / "copy.db"
    src = sqlite3.connect(f"file:{Path(a.snapshot).as_posix()}?mode=ro", uri=True)
    dst = sqlite3.connect(copy)
    src.backup(dst)
    dst.close()
    src.close()
    conn = sqlite3.connect(f"file:{copy.as_posix()}?mode=ro", uri=True)
    members = load_members(conn)
    print("developments", len(members), flush=True)

    gold_items, ginfo = identity_gold_items(Path(a.identity_dir))
    window_items = ginfo.pop("window_items_all")
    gold_hit = match_items(members, gold_items)
    window_hit = match_items(members, window_items)
    up_ids, up_files = set(), {}
    for p in a.upstream_cases:
        up_files[Path(p).parent.name] = sha256_file(p)
        up_ids |= {c["development_id"] for c in json.loads(Path(p).read_text(encoding="utf-8"))["cases"]}
    link_fn = real_link_fn(copy, members)
    res = build(conn, link_fn, up_ids, gold_hit, members)
    cases = res["cases"]
    # overlap of the DRAWN sample (must be zero for the excluded kinds); window-level overlap is reported only
    drawn_items = {i for c in cases for i in c["a_items"] + c["b_items"]}
    drawn_devs = {c["development_id"] for c in cases}
    dev_items = {i for d in drawn_devs for i in (m["id"] for m in members[d])}
    overlap = {
        "upstream_gold_developments_total": len(up_ids),
        "upstream_gold_in_drawn_developments": len(up_ids & drawn_devs),
        "upstream_gold_in_frame_before_exclusion": sum(1 for d in up_ids if d in members and len(members[d]) >= MIN_SIZE),
        "identity_gold_items_total": ginfo["gold_case_item_ids"],
        "identity_gold_items_matched_in_snapshot": len(gold_hit),
        "identity_gold_matched_items_in_drawn_developments": len(gold_hit & dev_items),
        "identity_gold_matched_items_in_shown_case_items": len(gold_hit & drawn_items),
        "developments_excluded_for_identity_gold_items": res["frame"]["excluded_identity_gold_item"],
        "identity_window_items_total": ginfo["window_items"],
        "identity_window_items_matched_in_snapshot": len(window_hit),
        "identity_window_matched_items_in_drawn_developments": len(window_hit & dev_items),
        "identity_window_matched_items_in_shown_case_items": len(window_hit & drawn_items),
    }
    blind = blind_cases(cases)
    key = key_of(cases)
    for name, obj in (("cases.json", blind), ("key.json", key), ("split.json", res["split"])):
        (out / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    strata_counts = {s: {"pool": res["pool_sizes"][s], "developments": res["drawn_developments"][s],
                         "cases": sum(1 for c in cases if c["stratum"] == s)} for s in STRATA}
    band_counts = {b: sum(1 for c in cases if c["band"] == b) for b, _, _ in BANDS}
    manifest = {
        "status": "DRAFT", "snapshot": str(Path(a.snapshot).name), "snapshot_sha256": got, "seed": SEED,
        "script": "build_sample.py", "script_sha256": sha256_file(__file__),
        "parameters": {"FOUNDER_H": FOUNDER_H, "LATE_H": LATE_H, "BURST_GAP_H": BURST_GAP_H, "MIN_SIZE": MIN_SIZE,
                       "SIDE_ITEMS": SIDE_ITEMS, "NEIGHBOUR_H": NEIGHBOUR_H, "TEXT_CHARS": TEXT_CHARS,
                       "bands_h": [[n, lo, None if hi == float("inf") else hi] for n, lo, hi in BANDS],
                       "strata_order": STRATA, "E_MIN_SPAN_H": E_MIN_SPAN_H, "E_MIN_DEPTH": E_MIN_DEPTH,
                       "D_MAX_LATE_COS": D_MAX_LATE_COS, "B_MAX_GAP_H": B_MAX_GAP_H, "B_MAX_SPAN_H": B_MAX_SPAN_H,
                       "A_SPAN_H": [A_MIN_SPAN_H, A_MAX_SPAN_H], "plan_cases_and_per_development": PLAN,
                       "pinned_development_cases": {str(k): v for k, v in PINNED.items()},
                       "split_acceptance_fraction": SPLIT_ACCEPTANCE_FRACTION},
        "frame": res["frame"], "strata": strata_counts, "bands": band_counts, "cases": len(cases),
        "developments": len(drawn_devs),
        "split": {s: sum(1 for v in res["split"].values() if v == s) for s in ("development", "acceptance")},
        "overlap": overlap, "identity_inputs": {k: v for k, v in ginfo.items()},
        "upstream_inputs_sha256": up_files,
        "outputs_sha256": {n: sha256_file(out / n) for n in ("cases.json", "key.json", "split.json")},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                       newline="\n")
    print(json.dumps({k: manifest[k] for k in ("frame", "strata", "bands", "cases", "developments", "split", "overlap")},
                     indent=1))


if __name__ == "__main__":
    main()
