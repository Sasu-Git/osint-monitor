"""Phase 0 foundation fixes (evaluations/system/full-basis-audit.md, stop condition S4 and risks 7, 9): writes
that were silently lost, and collector failures that turned into signals."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, Entity, EntityRelationship, RawItem, Source


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'f.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)
    yield factory
    engine.dispose()


# --- lost JSON writes ---------------------------------------------------------------------------

def test_an_alias_added_to_a_stored_entity_is_persisted(db):
    from osint_monitor.processors.entity_resolver import EntityResolver
    s = db()
    s.add(Entity(canonical_name="Pete Hegseth", entity_type="PERSON", aliases=["Hegseth"]))
    s.commit()
    s.close()

    s = db()
    resolver = EntityResolver(s)
    resolver._build_alias_map()
    resolver._register_alias(s.query(Entity).one(), "Pete Hegseth's")
    s.commit()
    s.close()

    assert db().query(Entity).one().aliases == ["Hegseth", "Pete Hegseth's"]


def _item(s):
    src = s.query(Source).filter_by(name="Test Wire").first()
    if src is None:
        src = Source(name="Test Wire", type="rss", url="https://x.invalid/")
        s.add(src)
        s.flush()
    n = s.query(RawItem).count()
    item = RawItem(source_id=src.id, title="t", content="c", url=f"https://x.invalid/{n}", external_id=str(n),
                   content_hash=f"h{n}")
    s.add(item)
    s.flush()
    return item.id


def test_relation_evidence_is_persisted_and_reruns_do_not_inflate_confidence(db):
    from osint_monitor.processors.relations import persist_relations
    rel = [{"subject": "Iran", "object": "Hezbollah", "predicate": "supports", "confidence": 0.5}]
    s = db()
    first, second = _item(s), _item(s)
    s.commit()
    persist_relations(s, first, rel)
    s.commit()
    persist_relations(s, second, rel)          # new evidence: recorded, confidence +0.05
    s.commit()
    for _ in range(3):
        persist_relations(s, second, rel)      # the same evidence again: no change
        s.commit()
    s.close()

    r = db().query(EntityRelationship).one()
    assert r.evidence_item_ids == [first, second]
    assert r.confidence == pytest.approx(0.55)


# --- alert recording and delivery ---------------------------------------------------------------

def _one_alert_engine(monkeypatch, key="corr:1:POSSIBLE→PROBABLE", severity=0.6):
    from osint_monitor.alerting import engine as E
    from osint_monitor.core.database import Alert
    for name in ("_tier1_iw_thresholds", "_tier1_corroboration_changes", "_tier1_fusion_convergence",
                 "_tier2_new_event_clusters", "_tier2_source_silence_break", "_tier3_signal_gaps",
                 "_tier4_first_report"):
        monkeypatch.setattr(E.AlertEngine, name, lambda self, *a, **k: [])
    monkeypatch.setattr(E.AlertEngine, "_tier1_corroboration_changes",
                        lambda self: [Alert(alert_type="corroboration_upgrade", severity=severity,
                                            title="Corroboration upgrade: test", trigger_key=key)])
    return E


def test_a_transition_in_quiet_hours_is_recorded_not_lost(db, monkeypatch):
    from osint_monitor.alerting.fatigue import FatigueManager
    from osint_monitor.core.database import Alert
    E = _one_alert_engine(monkeypatch)
    monkeypatch.setattr(FatigueManager, "_in_quiet_hours", lambda self: True)
    s = db()
    assert E.AlertEngine(s).evaluate_all() == []                 # nothing to notify now
    s.close()
    row = db().query(Alert).one()                                  # but the transition is on record
    assert row.trigger_key == "corr:1:POSSIBLE→PROBABLE" and row.delivered_via == E.QUIET_HOURS


def test_the_daemon_alert_job_delivers_and_records_the_channel(db, monkeypatch):
    from osint_monitor.alerting import channels as C
    from osint_monitor.core import scheduler
    from osint_monitor.core.database import Alert
    _one_alert_engine(monkeypatch)
    sent = []

    class Recorder(C.AlertChannel):
        def send(self, alert):
            sent.append(alert.title)                               # read after the job's session closed
            return True

    monkeypatch.setattr(scheduler, "get_session", db)
    monkeypatch.setattr(C, "build_channels", lambda cfg: [Recorder()])
    scheduler._run_alert_job()
    assert sent == ["Corroboration upgrade: test"]
    assert db().query(Alert).one().delivered_via == "Recorder"
