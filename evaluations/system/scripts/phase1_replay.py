"""Phase 1 gate: replay a frozen benchmark window as incremental pipeline runs in a temporary database and show
that the stored facts separate (a) newly ingested items, (b) existing items newly attached to a Development and
(c) reprocessing that creates no membership.

Run 1 ingests the window's first half (by publication time), run 2 the second half, run 3 re-runs
post-processing with no new items. Items get fetched_at = now at ingest (as collectors do), so the 48 h
clustering window holds them. No database under data/ is touched.

Usage: python evaluations/system/scripts/phase1_replay.py [WINDOW_ID] [--out report.json]
"""
import json
import os
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    window_id = args[0] if args else "2026-07-21"
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    tmp = Path(tempfile.mkdtemp(prefix="osint-phase1-replay-"))
    os.environ["OSINT_DB_URL"] = f"sqlite:///{tmp / 'replay.db'}"

    from osint_monitor.benchmark.format import BENCHMARK_DIR, load_items, load_manifest
    from osint_monitor.core import runs
    from osint_monitor.core.database import EventItem, PipelineRun, RawItem, get_session, init_db, reset_engine
    from osint_monitor.core.models import RawItemModel
    from osint_monitor.processors.pipeline import process_new_items, run_post_processing

    reset_engine()
    init_db(os.environ["OSINT_DB_URL"], backup_dir=tmp / "backups")
    window = next(w for w in load_manifest(BENCHMARK_DIR).windows if w.id == window_id)
    items = sorted(load_items(BENCHMARK_DIR / window.items_file), key=lambda i: i.published_at)
    half = len(items) // 2
    batches = [items[:half], items[half:], []]

    # the window is replayed in the present: every publication time moves by one offset (relative order and
    # spacing kept), so the clustering window (fetched and published within 48 h) holds it
    shift = datetime.utcnow() - max(i.published_at for i in items)
    session = get_session()
    run_ids = []
    for n, batch in enumerate(batches, 1):
        run, token = runs.start_run(session, "replay", tier=f"batch{n}")
        now = datetime.utcnow()
        models = [RawItemModel(title=i.title, content=i.excerpt, url=i.url, published_at=i.published_at + shift,
                               source_name=i.source, source_type="rss", external_id=i.id, fetched_at=now)
                  for i in batch]
        stats = process_new_items(session, models) if models else {"new_items": 0}
        stats.update(run_post_processing(session, quiet=True, offline=True))   # run 3: reprocessing only
        runs.finish_run(session, run, token, stats, items_collected=len(batch))
        run_ids.append(run.id)

    ingested = dict(session.query(RawItem.id, RawItem.ingested_run_id))
    memberships = session.query(EventItem).all()
    order = {rid: n for n, rid in enumerate(run_ids, 1)}
    kinds = Counter()
    per_run = Counter()
    for m in memberships:
        per_run[order.get(m.added_run_id, "unstamped")] += 1
        if m.added_run_id is None or ingested.get(m.item_id) is None:
            kinds["unstamped"] += 1
        elif ingested[m.item_id] == m.added_run_id:
            kinds["new_item_new_membership"] += 1
        elif order[ingested[m.item_id]] < order[m.added_run_id]:
            kinds["existing_item_newly_attached"] += 1
        else:
            kinds["impossible_attached_before_ingested"] += 1
    ledger = [{"batch": r.tier, "status": r.status, "items_collected": r.items_collected, "items_new": r.items_new,
               "code_sha": r.code_sha, "code_dirty": r.code_dirty, "config_hash": (r.config_hash or "")[:12],
               "models": r.models}
              for r in sorted(session.query(PipelineRun), key=lambda r: order[r.id])]
    report = {
        "window": window_id, "items": len(items), "batches": [len(b) for b in batches],
        "memberships": len(memberships), "memberships_added_per_run": dict(per_run), "membership_kinds": dict(kinds),
        "items_ingested_per_run": dict(Counter(order.get(v, "none") for v in ingested.values())),
        "run_ids_unique_hex32": len(set(run_ids)) == 3 and all(len(r) == 32 for r in run_ids),
        "ledger": ledger,
    }
    session.close()
    reset_engine()
    gate = (report["run_ids_unique_hex32"] and kinds["unstamped"] == 0 and kinds["impossible_attached_before_ingested"] == 0
            and per_run.get(3, 0) == 0 and kinds["new_item_new_membership"] > 0)
    report["gate"] = "PASS" if gate else "FAIL"
    text = json.dumps(report, indent=1, default=str)
    print(text)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    return 0 if gate else 1


if __name__ == "__main__":
    sys.exit(main())
