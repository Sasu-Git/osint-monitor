"""Downstream Situation impact of Phase 2 (read-only copies only).

  export SNAPSHOT_DB OUT_DIR      items of a (copied) snapshot DB -> OUT_DIR/items.jsonl + window.json, replayed in
                                  12 h ticks over the snapshot's own time span
  replay OUT_DIR TRACE.json       replay that window with the osint_monitor code on sys.path (run with the cwd of
                                  the code tree to compare: a worktree of the pre-Phase-2 commit, or this tree)
  compare BEFORE.json AFTER.json  Developments whose identity changed, Situation memberships affected, Situation
                                  actor-set changes, and whether each change follows from a Development change

No database under data/ is opened for writing; the snapshot is opened read-only.
"""
import json
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
sys.path.insert(0, str(Path(__file__).resolve().parent))


def export(db: str, out: Path) -> None:
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    rows = c.execute("SELECT r.id, r.title, r.content, r.url, r.published_at, r.fetched_at, s.name, s.type "
                     "FROM raw_items r JOIN sources s ON s.id = r.source_id ORDER BY r.id").fetchall()
    c.close()
    out.mkdir(parents=True, exist_ok=True)
    items, times = [], []
    with open(out / "items.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for rid, title, content, url, pub, fetched, src, stype in rows:
            item = {"id": f"s-{rid}", "published_at": pub, "fetched_at": fetched, "source": src, "source_type": stype,
                    "title": title, "excerpt": (content or "")[:600], "url": url or ""}
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            t = fetched or pub
            if t:
                times.append(datetime.fromisoformat(t[:19]))
    start = min(times).replace(minute=0, second=0, microsecond=0)
    end = max(times) + timedelta(hours=1)
    ticks, t, n = [], start, 1
    while t < end:
        ticks.append({"tick": n, "from": t.isoformat(), "to": (t + timedelta(hours=12)).isoformat()})
        t, n = t + timedelta(hours=12), n + 1
    window = {"id": Path(db).stem, "split": "impact", "start": start.isoformat(), "end": end.isoformat(),
              "items_file": str((out / "items.jsonl").resolve()), "ticks": ticks}
    (out / "window.json").write_text(json.dumps(window, indent=1), encoding="utf-8")
    print(len(rows), "items,", len(ticks), "ticks")


def replay(out: Path, trace_path: Path) -> None:
    import replay_current
    window = json.loads((out / "window.json").read_text(encoding="utf-8"))
    trace = replay_current.replay(window)
    keep = {"developments": trace["developments"], "situations": trace.get("situations", {}),
            "items": {i: {"title": r["title"], "source": r["source"]} for i, r in trace["items"].items()}}
    trace_path.write_text(json.dumps(keep, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(len(trace["developments"]), "Developments,", sum(1 for d in trace["developments"].values() if d.get("situation")),
          "assigned to a Situation")


def compare(before_path: Path, after_path: Path) -> dict:
    b = json.loads(before_path.read_text(encoding="utf-8"))
    a = json.loads(after_path.read_text(encoding="utf-8"))

    def by_members(t):
        return {frozenset(d["members"]): d for d in t["developments"].values()}

    bm, am = by_members(b), by_members(a)
    unchanged = set(bm) & set(am)
    changed_before = [m for m in bm if m not in am]
    created_after = [m for m in am if m not in bm]
    sit_members = lambda t: {s: sorted(frozenset(d["members"]) for d in t["developments"].values()
                                       if d.get("situation") == s) for s in t.get("situations", {})}
    sb, sa = sit_members(b), sit_members(a)
    membership_changes = []
    for s in sorted(set(sb) | set(sa)):
        before, after = set(map(frozenset, sb.get(s, []))), set(map(frozenset, sa.get(s, [])))
        lost, gained = before - after, after - before
        if lost or gained:
            membership_changes.append({
                "situation": s,
                "lost": [{"summary": bm[m]["summary"], "items": len(m),
                          "development_changed": m not in am} for m in lost],
                "gained": [{"summary": am[m]["summary"], "items": len(m),
                            "development_changed": m not in bm} for m in gained]})
    actor_changes = {s: {"before": b["situations"].get(s, {}).get("primary_actors"),
                         "after": a["situations"].get(s, {}).get("primary_actors")}
                     for s in sorted(set(b.get("situations", {})) | set(a.get("situations", {})))
                     if b["situations"].get(s, {}).get("primary_actors") != a["situations"].get(s, {}).get("primary_actors")}
    unexplained = [c for c in membership_changes
                   for x in c["lost"] + c["gained"] if not x["development_changed"]]
    out = {
        "developments_before": len(bm), "developments_after": len(am), "unchanged": len(unchanged),
        "changed_or_removed": len(changed_before), "new_or_reshaped": len(created_after),
        "situations_before": sorted(b.get("situations", {})), "situations_after": sorted(a.get("situations", {})),
        "situation_membership_changes": membership_changes,
        "situations_created_only_before": sorted(set(b.get("situations", {})) - set(a.get("situations", {}))),
        "situations_created_only_after": sorted(set(a.get("situations", {})) - set(b.get("situations", {}))),
        "situation_actor_set_changes": actor_changes,
        "membership_changes_not_explained_by_development_change": len(unexplained),
    }
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "export":
        export(sys.argv[2], Path(sys.argv[3]))
    elif cmd == "replay":
        replay(Path(sys.argv[2]), Path(sys.argv[3]))
    elif cmd == "compare":
        result = compare(Path(sys.argv[2]), Path(sys.argv[3]))
        print(json.dumps(result, indent=1, ensure_ascii=False))
        if len(sys.argv) > 4:
            Path(sys.argv[4]).write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
