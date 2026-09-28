"""Developer smoke test: the real local pipeline on a temporary database.

    python main.py smoke

Runs migrations, entity seeding, NLP, embeddings, clustering, principal actors,
classification, corroboration, ranking and situation grouping on a small fixed set of articles -- no
collectors, no LLM, no network stages (full-text fetching and geocoding are
skipped). Needs the installed spaCy and sentence-transformers models; the
embedding model is downloaded to the Hugging Face cache on first use.

Never touches data/osint.db. Exits non-zero on failure.
"""

from __future__ import annotations

import logging
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path

from osint_monitor.core.models import RawItemModel

WIDTH = 22


def fixture_items(now: datetime) -> list[RawItemModel]:
    """Three storylines: two match configured situations, one matches none."""
    stories = [
        ("us-iran", [
            ("Reuters World", "US and Iran resume nuclear talks in Muscat",
             "The United States and Iran resumed indirect nuclear talks in Muscat on Tuesday, with Oman "
             "mediating between the US envoy and Iran's foreign minister over uranium enrichment limits."),
            ("BBC World", "Iran and US hold new round of nuclear talks in Oman",
             "Iran and the United States held a new round of nuclear talks in Muscat, Oman, as negotiators "
             "discussed enrichment limits and sanctions relief."),
            ("Al Jazeera", "Iranian and US negotiators meet in Muscat for nuclear talks",
             "Iranian and US negotiators met in Muscat for nuclear talks mediated by Oman, focusing on "
             "uranium enrichment and the easing of sanctions on Iran."),
        ]),
        ("russia-ukraine", [
            ("Reuters World", "Russian drones strike Kyiv energy infrastructure overnight",
             "Russia launched a wave of drones at Kyiv overnight, striking energy infrastructure, Ukraine's "
             "air force said, as Ukrainian air defences shot down most of the drones."),
            ("BBC World", "Russia hits Kyiv power grid in overnight drone attack",
             "Russia attacked Kyiv's power grid with drones overnight, Ukrainian officials said, leaving parts "
             "of the Ukrainian capital without electricity."),
            ("Al Jazeera", "Ukraine says Russian drone attack on Kyiv damaged energy sites",
             "Ukraine said a Russian drone attack on Kyiv overnight damaged energy sites, the latest Russian "
             "strike on Ukrainian power infrastructure."),
        ]),
        ("unrelated", [
            ("Reuters World", "Bank of Japan keeps interest rates unchanged",
             "The Bank of Japan kept its benchmark interest rate unchanged on Tuesday, as the central bank "
             "weighed wage growth and inflation before any further tightening."),
            ("BBC World", "Bank of Japan holds rates steady amid inflation debate",
             "Japan's central bank held interest rates steady, with the Bank of Japan governor saying inflation "
             "and wage data would decide the timing of the next rate rise."),
            ("Al Jazeera", "Japan central bank leaves interest rates on hold",
             "The Bank of Japan left interest rates on hold, the central bank said, citing uncertainty over "
             "wages and inflation in the Japanese economy."),
        ]),
    ]
    items = []
    for s, (story, articles) in enumerate(stories):
        for a, (source, title, content) in enumerate(articles):
            items.append(RawItemModel(
                title=title, content=content, source_name=source, source_type="rss",
                url=f"https://smoke.invalid/{story}/{a}", external_id=f"smoke-{story}-{a}",
                published_at=now - timedelta(minutes=30 + 10 * s + a), fetched_at=now,
            ))
    return items


class SmokeFailure(Exception):
    pass


class _Report:
    def __init__(self):
        self.ok = True

    def line(self, label: str, status: str = "OK", detail: str = "") -> None:
        dots = "." * max(2, WIDTH - len(label))
        print(f"{label}{dots} {status}{'  ' + detail if detail else ''}")

    def check(self, label: str, fn):
        start = time.monotonic()
        try:
            result = fn()
        except SmokeFailure as e:
            self.line(label, "FAIL", str(e))
            raise
        except Exception as e:
            self.line(label, "FAIL", f"{type(e).__name__}: {e}")
            raise SmokeFailure(f"{label}: {e}") from e
        self.line(label, "OK", f"({time.monotonic() - start:.1f}s)" if time.monotonic() - start > 2 else "")
        return result


def run_smoke(keep: bool = False) -> int:
    print("OSINT Monitor smoke test\n")
    workdir = Path(tempfile.mkdtemp(prefix="osint-smoke-"))
    db_url = f"sqlite:///{workdir / 'smoke.db'}"
    os.environ["OSINT_DB_URL"] = db_url       # anything that asks settings gets the temp DB
    report = _Report()
    try:
        _run(report, db_url, workdir)
        print("\nSMOKE TEST PASSED")
        return 0
    except SmokeFailure as e:
        print(f"\nSMOKE TEST FAILED: {e}")
        return 1
    finally:
        from osint_monitor.core.database import reset_engine
        reset_engine()
        if keep:
            print(f"(database kept at {workdir / 'smoke.db'})")
        else:
            shutil.rmtree(workdir, ignore_errors=True)


def _run(report: _Report, db_url: str, workdir: Path) -> None:
    from osint_monitor.core.database import (
        Entity, Event, EventItem, RawItem, Situation, get_engine, get_session, init_db, reset_engine,
    )
    from osint_monitor.core.migrations import current_version, head_version
    from osint_monitor.processors.entity_resolver import EntityResolver
    from osint_monitor.processors.pipeline import process_new_items, run_post_processing

    reset_engine()
    now = datetime.utcnow()

    def database():
        engine = get_engine(db_url)
        if not str(engine.url).startswith("sqlite") or "smoke" not in str(engine.url):
            raise SmokeFailure(f"refusing to run against {engine.url}")
        init_db(db_url, backup_dir=workdir / "backups")
    report.check("Database", database)

    def migrations():
        engine = get_engine()
        if current_version(engine) != head_version():
            raise SmokeFailure(f"schema version {current_version(engine)}, expected {head_version()}")
        init_db(db_url, backup_dir=workdir / "backups")          # second run: no-op
        if current_version(engine) != head_version() or (workdir / "backups").exists():
            raise SmokeFailure("re-running migrations was not a no-op")
    report.check("Migrations", migrations)

    session = get_session()

    def seed():
        EntityResolver(session).seed_from_config()
        session.commit()
        if session.query(Entity).count() == 0:
            raise SmokeFailure("no entities seeded from config/entities.yaml")
    report.check("Entity seed", seed)

    fixtures = fixture_items(now)

    def ingest():
        stats = process_new_items(session, fixtures)
        stored = session.query(RawItem).count()
        if stored != len(fixtures):
            raise SmokeFailure(f"{stored}/{len(fixtures)} fixture items stored")
        if stats["entities_extracted"] == 0:
            raise SmokeFailure("NLP extracted no entities")
        if session.query(RawItem).filter(RawItem.embedding.is_(None)).count():
            raise SmokeFailure("some items have no embedding")
        return stats
    ingest_stats = report.check("Fixture ingestion", ingest)

    post: dict = {}

    def post_processing():
        post.update(run_post_processing(session, quiet=True, offline=True))
    report.check("Post-processing", post_processing)
    stages = post["stages"]

    def stage(name: str):
        def check():
            status = stages.get(name, "not run")
            if status != "ok":
                raise SmokeFailure(status)
        return check

    def clustering():
        stage("clustering")()
        if session.query(Event).count() < 2:
            raise SmokeFailure(f"only {session.query(Event).count()} events from {len(fixtures)} items")
        mixed = [e.id for e in session.query(Event) if len(_stories(session, e.id, EventItem, RawItem)) > 1]
        if mixed:
            raise SmokeFailure(f"events {mixed} merge articles from different fixture stories")
    report.check("Event clustering", clustering)

    def principals():
        stage("principals")()
        missing = [e.id for e in session.query(Event)
                   if not any(ee.is_principal for ee in e.event_entities)]
        if missing:
            raise SmokeFailure(f"events {missing} have no principal actors")
    report.check("Principal actors", principals)

    def classification():
        stage("classification")()
        unclassified = [e.id for e in session.query(Event) if e.classified_at is None or not e.event_type]
        if unclassified:
            raise SmokeFailure(f"events {unclassified} not classified")
    report.check("Classification", classification)
    report.check("Corroboration", stage("corroboration"))

    def ranking():
        stage("ranking")()
        if any(e.rank_score is None for e in session.query(Event)):
            raise SmokeFailure("some events were not ranked")
    report.check("Ranking", ranking)

    def situations():
        stage("situations")()
        events = session.query(Event).all()
        by_slug = {s.id: s.slug for s in session.query(Situation)}
        assigned = {by_slug[e.situation_id] for e in events if e.situation_id}
        if not assigned & {"us-iran", "russia-ukraine-war"}:
            raise SmokeFailure(f"no event joined a configured situation (assigned: {sorted(assigned) or 'none'})")
        unrelated = [e for e in events if _stories(session, e.id, EventItem, RawItem) == {"unrelated"}]
        if any(e.situation_id for e in unrelated):
            raise SmokeFailure("the unrelated Bank of Japan event joined a situation")
        if not any(e.situation_id is None for e in events):
            raise SmokeFailure("every event was assigned; expected the unrelated one to stay separate")
    report.check("Situation grouping", situations)

    for name in ("relations", "indicators", "fusion"):
        status = stages.get(name, "not run")
        if status != "ok":
            report.line(f"  {name}", "WARN", status)

    events = session.query(Event).all()
    assigned = sum(1 for e in events if e.situation_id)
    print(f"\nItems ingested: {ingest_stats['new_items']}  (entities extracted: {ingest_stats['entities_extracted']})")
    print(f"Events created: {len(events)}")
    print(f"Situations: {session.query(Situation).count()} "
          f"({session.query(Situation).filter(Situation.slug.notin_(_seed_slugs())).count()} created from data)")
    print(f"Assigned events: {assigned}")
    print(f"Unassigned events: {len(events) - assigned}\n")

    def idempotency():
        before = _snapshot(session, Event, Situation)
        repeat = process_new_items(session, fixture_items(now))
        if repeat["new_items"]:
            raise SmokeFailure(f"{repeat['new_items']} fixture items re-ingested as new")
        again = run_post_processing(session, quiet=True, offline=True)
        failed = {k: v for k, v in again["stages"].items() if v.startswith("failed")}
        if failed:
            raise SmokeFailure(f"second run failed stages: {failed}")
        after = _snapshot(session, Event, Situation)
        if after != before:
            raise SmokeFailure(f"state changed on re-run: {before} -> {after}")
    report.check("Idempotency", idempotency)
    session.close()


def _stories(session, event_id, EventItem, RawItem) -> set[str]:
    """Fixture stories an event's items come from (encoded in the fixture URL)."""
    urls = (session.query(RawItem.url).join(EventItem, EventItem.item_id == RawItem.id)
            .filter(EventItem.event_id == event_id))
    return {url.split("/")[3] for (url,) in urls if url and url.startswith("https://smoke.invalid/")}


def _seed_slugs() -> list[str]:
    from osint_monitor.core.config import load_situations_config
    return [s.slug for s in load_situations_config().situations]


def _snapshot(session, Event, Situation):
    session.expire_all()
    return (
        sorted((e.id, e.situation_id) for e in session.query(Event)),
        sorted(s.slug for s in session.query(Situation)),
    )


def main(argv: list[str] | None = None) -> None:
    logging.getLogger().setLevel(logging.WARNING)
    sys.exit(run_smoke(keep="--keep" in (argv or [])))
