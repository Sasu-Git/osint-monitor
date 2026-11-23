"""Part 2: illustrative chaining guards on the identity gold DEVELOPMENT windows (replay harness, offline).
Each guard is a monkeypatch of development_identity.reconcile applied only inside this script; runtime code is
unchanged.  The holdout window is never replayed or scored (score_identity's development filter is reused).

Guard hook = a copy of reconcile() whose only difference is one filter on the candidate links of each new item
against a touched Development (state = members at the start of reconcile, as in the runtime):
  size         receiving Development has >= S members            -> no link counts
  age_h        item published more than N h after the Development's first item
  centroid     cos(item, centroid of the Development's members) < c
  founder_k_h  only links to members published within K h of the Development's first item count
Times in a replay are publication times (shifted by one common offset), because added_at in a replay is wall clock.
"none-copy" is the unmodified copy and must equal the original reconcile (equivalence check).

Usage: python chain_guards_replay.py OUT.json label[,label...]   labels: baseline, nonecopy, size=4, age_h=12, ...
"""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
HERE = Path(__file__).resolve().parent
ID = HERE.parents[1] / "identity"
sys.path.insert(0, str(ID / "scripts"))

import numpy as np  # noqa: E402
import yaml  # noqa: E402

import replay_current  # noqa: E402
from phase2_baseline import score  # noqa: E402
from score_identity import totals  # noqa: E402

SWEEP = {"size": [4, 6, 8, 12], "age_h": [6, 12, 24, 36], "centroid": [0.40, 0.45, 0.50, 0.55],
         "founder_k_h": [6, 12, 24, 36]}
BLOCKED = {"n": 0, "items": []}


def make_reconcile(guard):
    from osint_monitor.core.database import EventItem
    from osint_monitor.processors import development_identity as DI
    from osint_monitor.processors.development_identity import Decision, _components, independent_origins, MIN_SIZE, MIN_INDEPENDENT_ORIGINS
    from osint_monitor.processors.development_segmentation import _cosine, compatible_link, segment_items
    from osint_monitor.processors.event_grouping import STRUCTURED

    def reconcile(session, cluster, config):
        ids = sorted(set(cluster["item_ids"]))
        member_of = {ei.item_id: ei.event_id for ei in session.query(EventItem).filter(EventItem.item_id.in_(ids))}
        new_ids = [i for i in ids if i not in member_of]
        if not new_ids:
            return []
        touched = sorted(set(member_of.values()))
        if cluster.get("kind") == STRUCTURED:
            d = Decision(cluster=cluster, event_id=touched[0] if touched else None, created=not touched, added=new_ids)
            d.reasons.append("structured record group" + (f" extends D{touched[0]}" if touched else ""))
            return [d]
        members = {e: sorted(i for (i,) in session.query(EventItem.item_id).filter(EventItem.event_id == e))
                   for e in touched}
        seg = segment_items(session, set(new_ids) | {m for ms in members.values() for m in ms}, config)
        cache = {}

        def linked(a, b):
            key = (a, b) if a < b else (b, a)
            if key not in cache:
                cache[key] = a in seg and b in seg and compatible_link(seg[a], seg[b], config)
            return cache[key]

        decisions, extend, rest = [], {}, []
        for n in new_ids:
            best = None
            for e in touched:
                links = [m for m in members[e] if linked(n, m)]
                if links and guard is not None:
                    kept = guard(n, members[e], links, seg)
                    if not kept:
                        BLOCKED["n"] += 1
                        BLOCKED["items"].append((n, e))
                    links = kept
                if links:
                    score_ = (len(links), max(_cosine(seg[n].vector, seg[m].vector) for m in links), -e)
                    if best is None or score_ > best[0]:
                        best = (score_, e)
            if best:
                extend.setdefault(best[1], []).append(n)
            else:
                rest.append(n)
        for e in sorted(extend):
            d = Decision(cluster=cluster, event_id=e, added=sorted(extend[e]))
            d.reasons.append(f"continues D{e}: {len(d.added)} new item(s) linked to its members")
            decisions.append(d)
        held = Decision(cluster=cluster)
        for part in _components(sorted(rest), linked):
            if len(part) < MIN_SIZE:
                for n in part:
                    held.held[n] = ("linked to no member of an overlapping Development" if touched
                                    else "not linked compatibly to another new item")
                continue
            origins = independent_origins(session, part)
            if origins < MIN_INDEPENDENT_ORIGINS:
                for n in part:
                    held.held[n] = f"single-source: {origins} independent origin(s)"
                continue
            d = Decision(cluster=cluster, created=True, added=part)
            d.reasons.append(f"new Development: {len(part)} items, {origins} independent origins")
            decisions.append(d)
        if held.held:
            held.reasons.append("below the Development layer")
            decisions.append(held)
        return decisions

    return reconcile


def guard_for(fam, val):
    from osint_monitor.processors.development_segmentation import _cosine

    def hours(a, b):
        return (a - b).total_seconds() / 3600 if a and b else 0.0

    def g(n, mem, links, seg):
        ms = [m for m in mem if m in seg]
        if fam == "size":
            return links if len(mem) < val else []
        first = min((seg[m].published_at for m in ms if seg[m].published_at), default=None)
        if fam == "age_h":
            return links if hours(seg[n].published_at, first) <= val else []
        if fam == "centroid":
            cen = np.mean([seg[m].vector for m in ms], axis=0)
            return links if _cosine(seg[n].vector, cen) >= val else []
        if fam == "founder_k_h":
            return [m for m in links if hours(seg[m].published_at, first) <= val]
        raise ValueError(fam)
    return g


def run_config(label, manifest, gold):
    from osint_monitor.processors import development_identity as DI
    original = DI.reconcile
    if label == "baseline":
        DI.reconcile = original
    elif label == "nonecopy":
        DI.reconcile = make_reconcile(None)
    else:
        fam, val = label.split("=")
        DI.reconcile = make_reconcile(guard_for(fam, float(val) if "." in val else int(val)))
    BLOCKED["n"], BLOCKED["items"] = 0, []
    try:
        wins, traces = [], {}
        for w in manifest["windows"]:
            if w["split"] != "development":
                continue
            t = replay_current.replay(w)
            wins.append(score(t, gold))
            traces[w["id"]] = {d: sorted(v["members"]) for d, v in t["developments"].items()}
    finally:
        DI.reconcile = original
    T = totals(wins)
    m = {k: list(v) if isinstance(v, tuple) else v for k, v in T.items()}
    return {"label": label, "metrics": m, "blocked_attachments_in_replay": BLOCKED["n"],
            "memberships": traces}


def main():
    out = Path(sys.argv[1])
    labels = sys.argv[2].split(",")
    manifest = yaml.safe_load((ID / "manifest.yaml").read_text(encoding="utf-8"))
    gm = yaml.safe_load((ID / "gold" / "manifest.yaml").read_text(encoding="utf-8"))
    assert gm["revision"] == 2
    gold = {k: v for k, v in yaml.safe_load((ID / "gold" / "identity-gold.yaml").read_text(encoding="utf-8")).items()
            if v["split"] == "development"}
    res = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    for label in labels:
        if label in res:
            continue
        res[label] = run_config(label, manifest, gold)
        out.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        m = res[label]["metrics"]
        print(label, {k: m[k] for k in ("continuity_precision", "continuity_recall", "split_failures", "merge_failures",
                                       "id_stability", "mixed_developments")}, "blocked", res[label]["blocked_attachments_in_replay"],
              flush=True)


if __name__ == "__main__":
    main()
