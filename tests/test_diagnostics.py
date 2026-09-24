"""Event diagnostics flag the cluster problems seen in live data."""

from osint_monitor.core.config import load_sources_config
from osint_monitor.core.database import Entity, Event, EventEntity, EventItem, RawItem, Source
from osint_monitor.processors.diagnostics import describe_event, format_event


def test_diagnostics_flag_large_mixed_clusters_without_principals(session):
    src = Source(name="UN Consolidated", type="sanctions", url="u")
    session.add(src)
    event = Event(summary="Earthquake M5.3 - 15 km SSW of Hilvan, Turkey")
    session.add(event)
    session.flush()
    titles = [f"UN Sanctions: person {n} in Iran and Tehran" for n in range(6)] + \
             [f"China and Beijing trade note {n}" for n in range(6)]
    for n, title in enumerate(titles):
        item = RawItem(source_id=src.id, title=title, content="", content_hash=f"h{n}")
        session.add(item)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=item.id))
    session.commit()

    d = describe_event(session, event, load_sources_config().regions)
    joined = "; ".join(d["warnings"])
    assert "large cluster (12 items)" in joined
    assert "mixed regions (china, iran)" in joined
    assert "no principal actors" in joined
    assert "WARNING" in format_event(d)


def test_diagnostics_report_principals_separately_from_mentions(session):
    iran, oman = Entity(canonical_name="Iran", entity_type="GPE"), Entity(canonical_name="Oman", entity_type="GPE")
    event = Event(summary="US and Iran resume talks")
    session.add_all([iran, oman, event])
    session.flush()
    session.add_all([EventEntity(event_id=event.id, entity_id=iran.id, is_principal=True),
                     EventEntity(event_id=event.id, entity_id=oman.id, is_principal=False)])
    session.commit()
    d = describe_event(session, event, {})
    assert d["principal_actors"] == ["Iran"] and d["entities"] == ["Iran", "Oman"]
