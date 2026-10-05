"""Post-migration and post-start verification (docs/operations/deployment-runbook.md, steps M2 and S2-S3).

    python scripts/postdeploy_check.py --db LIVE.db --pre OUT/predeploy-final.json [--since UTC] [--runtime]
           [--logs-dir NEW_WORKTREE/data/logs] [--out OUT] [--max-new-situations 3] [--explosion-factor 5]

Run it with the target code on sys.path. Read-only: the database is opened with mode=ro and the status files
are only read.

- Without --runtime (step M2, after migration, before starting the daemon): structure only. That covers
  schema version, integrity, foreign keys, tables/columns/indexes, duplicates, row-count loss, invented
  historical timestamps and the summary columns.
- With --runtime --since <daemon start UTC> (steps S2-S3): the same, plus checks that the new daemon writes
  what it should.

Exit code 0: all checks passed. 1: a rollback criterion failed (see the runbook). 3: warnings only (review).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deploy_checks as D  # noqa: E402


def runtime_checks(conn, pre: dict, since: datetime, logs_dir: Path | None, max_new_situations: int,
                   explosion_factor: float) -> list[dict]:
    out = []

    def check(name, ok, detail="", warn=False):
        out.append({"check": name, "ok": bool(ok), "detail": detail, "warn_only": warn})

    s = since.isoformat(sep=" ")
    target_sha = (pre.get("target") or {}).get("sha")
    runs = conn.execute("SELECT id, tier, status, code_sha, config_hash, stages, items_collected FROM pipeline_runs "
                        "WHERE started_at >= ? ORDER BY started_at", (s,)).fetchall()
    check("pipeline runs recorded since start", runs, f"{len(runs)} runs")
    if runs:
        shas = {r[3] for r in runs}
        check("runs carry the target code SHA", shas == {target_sha}, f"run SHAs {sorted(x or '?' for x in shas)}, "
                                                                       f"target {target_sha}")
        check("runs carry a config hash", all(r[4] for r in runs), f"{sum(1 for r in runs if not r[4])} without")
        empty = [r[0][:8] for r in runs if r[2] != "running" and not json.loads(r[5] or "{}")]
        check("finished runs record stage statuses", not empty, f"{len(empty)} finished runs without stages")
        failed = [(r[1], r[2]) for r in runs if r[2] == "failed"]
        check("no failed pipeline runs", not failed, f"{len(failed)} failed: {failed[:5]}", warn=True)
    new_items = conn.execute("SELECT COUNT(*), SUM(ingested_run_id IS NULL) FROM raw_items WHERE id > ?",
                             ((pre["live_state"]["max_ids"]["raw_items"] or 0),)).fetchone()
    check("new items carry run provenance (ingested_run_id)", (new_items[1] or 0) == 0,
          f"{new_items[0]} new items, {new_items[1] or 0} without a run")
    cutoff = pre["live_state"]["max_ids"]["event_items"] or 0
    mem = conn.execute("SELECT COUNT(*), SUM(added_at IS NULL OR added_run_id IS NULL) FROM event_items WHERE id > ?",
                       (cutoff,)).fetchone()
    check("new memberships carry added_at / added_run_id", (mem[1] or 0) == 0,
          f"{mem[0]} new memberships, {mem[1] or 0} unstamped")
    single = conn.execute(
        "SELECT e.id, e.summary FROM events e JOIN event_items ei ON ei.event_id = e.id JOIN raw_items r ON r.id = ei.item_id "
        "WHERE e.id > ? GROUP BY e.id HAVING COUNT(DISTINCT r.source_id) < 2",
        (pre["live_state"]["max_ids"]["events"] or 0,)).fetchall()
    check("new Developments have >= 2 sources (single-source stays below the Development layer)", not single,
          f"{len(single)} single-source: {[x[0] for x in single[:10]]}")
    pre_slugs = set(pre["live_state"].get("situation_slugs") or [])
    now_slugs = {r[0] for r in conn.execute("SELECT slug FROM situations")}
    new_slugs = sorted(now_slugs - pre_slugs)
    check("Situation creation within bounds", len(new_slugs) <= max_new_situations,
          f"{len(new_slugs)} new: {new_slugs[:10]} (limit {max_new_situations})")
    check("no Situation disappeared", pre_slugs <= now_slugs, f"missing {sorted(pre_slugs - now_slugs)[:10]}")
    hours = max((datetime.utcnow() - since).total_seconds() / 3600, 0.25)
    new_dev = conn.execute("SELECT COUNT(*) FROM events WHERE id > ?", (pre["live_state"]["max_ids"]["events"] or 0,)
                           ).fetchone()[0]
    base = conn.execute("SELECT COUNT(*) FROM events WHERE id <= ? AND first_reported_at >= ?",
                        (pre["live_state"]["max_ids"]["events"] or 0,
                         (since - timedelta(days=7)).isoformat(sep=" "))).fetchone()[0] / (7 * 24)
    rate = new_dev / hours
    check("no Development count explosion", rate <= max(explosion_factor * base, 2.0),
          f"{new_dev} new in {hours:.1f} h = {rate:.2f}/h vs pre-deploy {base:.2f}/h (limit x{explosion_factor})")
    alerts = conn.execute("SELECT alert_type, delivered_via FROM alerts WHERE created_at >= ?", (s,)).fetchall()
    outage_like = [a for a in alerts if a[0] in ("signal_gap_opened", "source_silence_break")]
    check("no signal-gap / silence-break alerts to review", not outage_like,
          f"{len(outage_like)} since start: confirm each is not a collector outage", warn=True)
    if logs_dir is not None:
        status_file = logs_dir / "collector_status.json"
        try:
            raw = json.loads(status_file.read_text(encoding="utf-8"))
            ok = raw.get("schema") == 2 and isinstance(raw.get("collectors"), dict)
            failing = [e.get("name") for e in raw.get("collectors", {}).values() if e.get("state") == "failed"]
            check("collector status file valid (schema 2)", ok, f"{len(raw.get('collectors', {}))} collectors")
            check("no failed collectors", not failing, f"{len(failing)} failed: {failing[:10]}", warn=True)
        except FileNotFoundError:
            check("collector status file valid (schema 2)", False, f"{status_file} missing")
        except ValueError as e:
            check("collector status file valid (schema 2)", False, f"malformed: {e}")
        delivery = logs_dir / "alert_delivery.json"
        try:
            d = json.loads(delivery.read_text(encoding="utf-8"))
            bad = {k: v.get("last_error") for k, v in d.items() if v.get("consecutive_failures")}
            check("alert delivery channels not failing", not bad, str(bad) if bad else f"{len(d)} channels ok")
        except FileNotFoundError:
            check("alert delivery recorded", not alerts, "no delivery record"
                  + (f" although {len(alerts)} alerts were created (channels configured?)" if alerts else ""), warn=True)
        except ValueError as e:
            check("alert delivery status readable", False, f"malformed: {e}")
        log = logs_dir / "daemon.log"
        check("daemon.log written (rotating, 10 MB x 5)", log.exists() and log.stat().st_size > 0,
              f"{log} {'present' if log.exists() else 'missing'}")
    try:
        from osint_monitor.processors.nlp import MISSING, ner_status
        st = ner_status()
        missing = [k for k, (_, s_) in st.items() if s_ == MISSING]
        check("NER models available (en/it/es)", not missing, f"missing: {missing}" if missing else str(st),
              warn=bool(missing) and "en" not in missing)
    except Exception as e:
        check("NER status readable", False, str(e), warn=True)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, type=Path)
    ap.add_argument("--pre", required=True, type=Path, help="predeploy-final.json from predeploy_check.py")
    ap.add_argument("--runtime", action="store_true")
    ap.add_argument("--since", help="UTC time the new daemon started (runtime checks)")
    ap.add_argument("--logs-dir", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--max-new-situations", type=int, default=3)
    ap.add_argument("--explosion-factor", type=float, default=5.0)
    a = ap.parse_args(argv)
    pre = json.loads(a.pre.read_text(encoding="utf-8"))
    conn = D.ro(a.db)
    try:
        checks = [{**c, "warn_only": False} for c in D.verify_structure(conn, pre["live_state"])]
        if a.runtime:
            if not a.since:
                print("--runtime needs --since")
                return 2
            checks += runtime_checks(conn, pre, datetime.fromisoformat(a.since), a.logs_dir, a.max_new_situations,
                                     a.explosion_factor)
    finally:
        conn.close()
    for c in checks:
        tag = "PASS" if c["ok"] else ("WARN" if c["warn_only"] else "FAIL")
        print(f"  [{tag}] {c['check']}: {c['detail']}")
    failed = [c for c in checks if not c["ok"] and not c["warn_only"]]
    warned = [c for c in checks if not c["ok"] and c["warn_only"]]
    if a.out:
        D.dump({"at_utc": datetime.utcnow().isoformat(timespec="seconds"), "runtime": a.runtime, "checks": checks},
               a.out / f"postdeploy-{'runtime' if a.runtime else 'structure'}.json")
    if failed:
        print(f"POST-DEPLOY FAILED: {len(failed)} rollback criteria hit -- see the runbook, section R")
        return 1
    print("POST-DEPLOY OK" + (f" with {len(warned)} warnings to review" if warned else ""))
    return 3 if warned else 0


if __name__ == "__main__":
    sys.exit(main())
