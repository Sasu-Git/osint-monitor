"""score_events (config read once, queries batched) gives exactly compute_corroboration_score's result per event:
same items, sources, claims, provenance and float order (evaluations/performance/corroboration-config-once/)."""

from datetime import datetime, timedelta

import osint_monitor.processors.provenance.context as context
import osint_monitor.processors.provenance.resolve as resolve
from osint_monitor.core.database import Claim, Event, EventItem, RawItem, Source
from osint_monitor.processors.corroboration import compute_corroboration_score, score_events

T0 = datetime(2026, 9, 24, 8, 0)
BODY = ("Iran's foreign minister and the US special envoy met in Muscat on Tuesday with Omani mediation, the first "
        "in-person round of talks since June, officials from both sides said. The meeting lasted three hours.")


def _event(session, rows, claims=()):
    event = Event(summary="Envoys meet in Muscat")
    session.add(event)
    session.flush()
    for n, (source_name, source_type, text) in enumerate(rows):
        src = session.query(Source).filter_by(name=source_name).first()
        if not src:
            src = Source(name=source_name, type=source_type, url=f"https://{source_name}.example")
            session.add(src)
            session.flush()
        ri = RawItem(source_id=src.id, title=f"Envoys meet in Muscat {n}", content=text,
                     content_hash=f"{event.id}-{n}", published_at=T0 + timedelta(hours=n))
        session.add(ri)
        session.flush()
        session.add(EventItem(event_id=event.id, item_id=ri.id))
        for subject, ctype, on_event in claims:
            if n == 0:
                session.add(Claim(item_id=ri.id, event_id=event.id if on_event else None, subject=subject, verb="said",
                                  claim_text=f"{subject} {ctype}", claim_type=ctype, source_name=source_name))
    session.commit()
    return event.id


def test_batch_equals_per_event_on_varied_events(session, monkeypatch):
    ids = [
        _event(session, [(o, "rss", "MUSCAT (Reuters) - envoys met.") for o in ("BBC World", "Al Jazeera", "Daily Blog")]),
        _event(session, [("BBC World", "rss", BODY), ("Al Jazeera", "rss", BODY), ("State Department", "rss", "No.")],
               claims=[("Iran", "assertion", True), ("Iran", "denial", True)]),
        _event(session, [("@someone", "twitter", BODY), ("Defense News", "rss", BODY + " Extra.")],
               claims=[("US", "confirmation", False), ("US", "denial", False)]),
        _event(session, [("Reuters World", "rss", BODY)]),
    ]
    empty = Event(summary="No members")
    session.add(empty)
    session.commit()
    ids.append(empty.id)

    want = {e: compute_corroboration_score(session, e) for e in ids}
    reads = {"categories": 0, "resolver": 0}
    orig_cat, orig_init = context._feed_categories, resolve.ProvenanceResolver.__init__
    monkeypatch.setattr(context, "_feed_categories", lambda: (reads.__setitem__("categories", reads["categories"] + 1),
                                                              orig_cat())[1])
    def init(self, *a, **k):
        reads["resolver"] += 1
        orig_init(self, *a, **k)
    monkeypatch.setattr(resolve.ProvenanceResolver, "__init__", init)

    got = score_events(session, ids, chunk=2)                       # several chunks
    assert got == want
    assert reads == {"categories": 1, "resolver": 1}                # configuration read once for the whole call
    assert want[ids[1]]["has_contradictions"] and want[ids[2]]["has_contradictions"]
    assert want[ids[-1]]["corroboration_level"] == "UNCONFIRMED"


def test_batch_reports_a_failing_event_without_stopping_the_others(session, monkeypatch):
    ok = _event(session, [("BBC World", "rss", BODY)])
    bad = _event(session, [("Al Jazeera", "rss", BODY)])
    import osint_monitor.processors.corroboration as corroboration
    real = corroboration._score
    def flaky(event_id, *args):
        if event_id == bad:
            raise RuntimeError("boom")
        return real(event_id, *args)
    monkeypatch.setattr(corroboration, "_score", flaky)
    got = score_events(session, [ok, bad])
    assert isinstance(got[bad], RuntimeError) and got[ok]["outlets"] == 1
