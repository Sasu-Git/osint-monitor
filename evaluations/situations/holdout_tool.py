"""Blind hold-out for situation creation (actor-pair vs exact actor-set). Read-only on inputs.

    python evaluations/situations/holdout_tool.py freeze  --db SNAPSHOT --start ISO --end ISO --id ID
    python evaluations/situations/holdout_tool.py sheet   --id ID
    python evaluations/situations/holdout_tool.py score   --id ID

freeze  replays nothing: it copies the snapshot (never the daemon DB), recomputes principal actors
        for the events first reported in [start, end) with the current code, and writes the
        developments (items, principals, embedding, timestamps, sources) to
        evaluations/situations/<ID>/developments.jsonl with its SHA-256 in manifest.json.
sheet   writes labels.yaml: every pair of developments that share a canonical principal-actor pair,
        shuffled, with titles, leads, sources and times only (no counts, similarities, decisions).
        The labeller fills SAME_SITUATION / DIFFERENT_SITUATION / AMBIGUOUS.
score   verifies both hashes, then replays the frozen policies (exact actor set, actor pair >= 0.40,
        actor pair >= 0.50 as a diagnostic) after seed matching and scores them against the labels.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).parent
LABELS = ("SAME_SITUATION", "DIFFERENT_SITUATION", "AMBIGUOUS")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze(args):
    from osint_monitor.core.database import Event, EventItem, RawItem, Source, get_session, init_db
    from osint_monitor.processors.embeddings import blob_to_embedding
    from osint_monitor.processors.principals import _lead, mark_principal_actors
    from osint_monitor.processors.situations.store import signature_for_event

    out = ROOT / args.id
    out.mkdir(parents=True, exist_ok=False)                       # never overwrite a frozen hold-out
    tmp = Path(tempfile.mkdtemp()) / "holdout.db"
    shutil.copyfile(args.db, tmp)                                 # the snapshot copy is the only thing written
    url = f"sqlite:///{tmp}"
    init_db(url)
    s = get_session(url)
    start, end = datetime.fromisoformat(args.start), datetime.fromisoformat(args.end)
    events = [e for e in s.query(Event).order_by(Event.first_reported_at, Event.id)
              if e.first_reported_at and start <= e.first_reported_at < end]
    mark_principal_actors(s, now=end, window_days=(end - start).days + 2)
    rows = []
    for e in events:
        sig = signature_for_event(s, e)
        items = (s.query(RawItem, Source).join(EventItem, EventItem.item_id == RawItem.id)
                 .join(Source, Source.id == RawItem.source_id).filter(EventItem.event_id == e.id).all())
        rows.append({
            "dev": f"d{e.id}", "first_reported_at": e.first_reported_at.isoformat(),
            "last_updated_at": (e.last_updated_at or e.first_reported_at).isoformat(),
            "region": e.region, "actors": sig.actors, "actors_are_principal": sig.actors_are_principal,
            "embedding": [round(float(x), 6) for x in sig.embedding] if sig.embedding else None,
            "items": [{"source": src.name, "title": r.title, "lead": _lead(r.content),
                       "published_at": (r.published_at or r.fetched_at).isoformat()} for r, src in items],
        })
    s.close()
    path = out / "developments.jsonl"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    manifest = {"id": args.id, "start": args.start, "end": args.end, "source_snapshot": str(args.db),
                "developments": len(rows), "developments_sha256": sha(path),
                "frozen_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print(f"frozen {len(rows)} developments -> {path} ({manifest['developments_sha256'][:12]})")


def load(args):
    out = ROOT / args.id
    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    path = out / "developments.jsonl"
    assert sha(path) == manifest["developments_sha256"], "developments changed since freeze"
    devs = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return out, manifest, devs


def _keys(devs):
    from osint_monitor.processors.actors import ActorNormalizer
    n = ActorNormalizer.load()
    return {d["dev"]: sorted(n.keys(d["actors"])) if d["actors_are_principal"] else [] for d in devs}


def candidate_pairs(devs):
    """Development pairs that share a canonical principal-actor pair: everything either policy can join."""
    keys = _keys(devs)
    by_pair = defaultdict(set)
    for d in devs:
        for p in combinations(keys[d["dev"]], 2):
            by_pair[p].add(d["dev"])
    out = set()
    for members in by_pair.values():
        out |= {tuple(sorted(x)) for x in combinations(sorted(members), 2)}
    return sorted(out)


def sheet(args):
    out, manifest, devs = load(args)
    by = {d["dev"]: d for d in devs}
    pairs = candidate_pairs(devs)
    random.Random(manifest["developments_sha256"]).shuffle(pairs)   # deterministic, unrelated to any score
    path = out / "labels.yaml"
    assert not path.exists(), "labels already written"
    lines = ["# Blind situation-identity labels. For each pair: SAME_SITUATION (one persistent state of",
             "# affairs), DIFFERENT_SITUATION, or AMBIGUOUS. A situation is broader than one development",
             "# or storyline, but must be one persistent geopolitical state of affairs. A coherent",
             "# multi-day event (a diplomatic visit, a summit, a papal visit, a disaster response) is",
             "# NOT SAME_SITUATION by that fact alone: it must belong to a persistent state of affairs",
             "# (e.g. summit bargaining that continues a bilateral dispute), otherwise DIFFERENT or AMBIGUOUS.",
             f"holdout: {args.id}", "labelled_by: ''", "labels:"]
    for a, b in pairs:
        lines.append(f"- pair: [{a}, {b}]")
        lines.append("  label: ''")
        lines.append("  note: ''")
        for tag, dev in (("A", by[a]), ("B", by[b])):
            for it in dev["items"][:3]:
                lines.append(f"  # {tag} {it['published_at'][:16]} [{it['source']}] {it['title']}")
                if it["lead"]:
                    lines.append(f"  #   {it['lead'][:220]}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(pairs)} development pairs to label -> {path}")


def score(args):
    import yaml

    from osint_monitor.core.config import load_situations_config
    from osint_monitor.core.models import DevelopmentSignature, SituationProfile
    from osint_monitor.processors.situations import SituationGrouper
    from osint_monitor.processors.situations.grouper import _cosine

    out, manifest, devs = load(args)
    lab_path = out / "labels.yaml"
    frozen = json.loads((out / "labels.freeze.json").read_text(encoding="utf-8"))
    assert sha(lab_path) == frozen["labels_sha256"], "labels changed since they were frozen"
    raw = yaml.safe_load(lab_path.read_text(encoding="utf-8"))
    gold = {tuple(sorted(x["pair"])): x["label"] for x in raw["labels"]}
    assert all(v in LABELS for v in gold.values()), "unlabelled or invalid entries"

    cfg = load_situations_config()
    seeds = [SituationProfile(slug=x.slug, title=x.title, region=x.region, primary_actors=x.primary_actors,
                              keywords=x.keywords) for x in cfg.situations]
    sigs = [DevelopmentSignature(event_id=i, title=d["items"][0]["title"] if d["items"] else "", actors=d["actors"],
                                 actors_are_principal=d["actors_are_principal"], region=d["region"],
                                 occurred_at=datetime.fromisoformat(d["first_reported_at"]), embedding=d["embedding"])
            for i, d in enumerate(devs)]
    name = {i: d["dev"] for i, d in enumerate(devs)}
    vec = {d["dev"]: d["embedding"] for d in devs}
    title = {d["dev"]: (d["items"][0]["title"] if d["items"] else "") for d in devs}
    policies = {"A exact actor set": ("actor_set", 0.40), "B actor pair >= 0.40": ("actor_pair", 0.40),
                "diagnostic: actor pair >= 0.50": ("actor_pair", 0.50)}
    same_pairs = {p for p, v in gold.items() if v == "SAME_SITUATION"}
    report = {}
    for label, (rule, sim) in policies.items():
        c = cfg.model_copy(deep=True)
        c.policy.create_by, c.policy.create_min_similarity = rule, sim
        assignments, created = SituationGrouper(c).group(sigs, seeds)
        seeded = Counter(a.slug for a in assignments if a.slug and not a.created)
        groups = defaultdict(list)
        for i, a in enumerate(assignments):
            if a.created:
                groups[a.slug].append(name[i])
        rows, joined = [], set()
        for slug, members in groups.items():
            ps = [tuple(sorted(p)) for p in combinations(members, 2)]
            joined |= set(ps)
            verdict = Counter(gold.get(p, "UNLABELLED") for p in ps)
            sims = [round(_cosine(vec[a], vec[b]), 2) if vec[a] and vec[b] else None for a, b in ps]
            rows.append({"slug": slug, "members": members, "titles": [title[m][:70] for m in members],
                         "pair_labels": dict(verdict), "similarities": sims})
        missed = sorted(p for p in same_pairs if p not in joined)
        report[label] = {"seed_assignments": dict(seeded), "created": rows, "missed_same_pairs": missed}
        n_ps = sum(sum(r["pair_labels"].values()) for r in rows)
        same = sum(r["pair_labels"].get("SAME_SITUATION", 0) for r in rows)
        diff = sum(r["pair_labels"].get("DIFFERENT_SITUATION", 0) for r in rows)
        amb = sum(r["pair_labels"].get("AMBIGUOUS", 0) for r in rows)
        print(f"\n[{label}] situations created {len(rows)}, developments via creation "
              f"{sum(len(r['members']) for r in rows)}; member pairs SAME {same} / DIFFERENT {diff} / AMBIGUOUS {amb}"
              f" of {n_ps}; missed SAME pairs {len(missed)}; seed assignments {dict(seeded)}")
        for r in rows:
            print(f"   {r['slug']}: {r['pair_labels']} sims {r['similarities']}")
            for t in r["titles"]:
                print(f"      - {t}")
    (out / "score.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def freeze_labels(args):
    out = ROOT / args.id
    path = out / "labels.yaml"
    import yaml
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert raw.get("labelled_by"), "labelled_by missing"
    assert all(x["label"] in LABELS for x in raw["labels"]), "unlabelled or invalid entries"
    (out / "labels.freeze.json").write_text(json.dumps({"labels_sha256": sha(path), "pairs": len(raw["labels"]),
                                                        "frozen_at": datetime.now().astimezone().isoformat(timespec="seconds")},
                                                       indent=1) + "\n", encoding="utf-8")
    print("labels frozen:", sha(path)[:12], dict(Counter(x["label"] for x in raw["labels"])))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("freeze")
    f.add_argument("--db", required=True)
    f.add_argument("--start", required=True)
    f.add_argument("--end", required=True)
    f.add_argument("--id", required=True)
    for n in ("sheet", "freeze-labels", "score"):
        sub.add_parser(n).add_argument("--id", required=True)
    a = ap.parse_args()
    {"freeze": freeze, "sheet": sheet, "freeze-labels": freeze_labels, "score": score}[a.cmd](a)
