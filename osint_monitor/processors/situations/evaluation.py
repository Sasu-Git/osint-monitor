"""Read-only situation grouping diagnostics: what the grouper would decide for every
event, and why.

For each event: principal actors (canonical), every situation sharing an actor with the
signals behind its score, the grouper's decision, and the situation stored in the DB.
For creation: the unassigned principal actor sets and actor *pairs* and how often each
recurs -- the evidence for or against the exact-set recurrence rule.

    python main.py inspect situations
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations

from sqlalchemy.orm import Session

from osint_monitor.core.database import Event, Situation
from osint_monitor.processors.situations.grouper import SituationGrouper
from osint_monitor.processors.situations.store import load_profiles, signature_for_event


def situation_report(session: Session, grouper: SituationGrouper | None = None) -> dict:
    grouper = grouper or SituationGrouper()
    profiles = load_profiles(session, grouper.config)
    slugs = dict(session.query(Situation.id, Situation.slug))
    events = session.query(Event).order_by(Event.first_reported_at, Event.id).all()

    rows, signatures = [], []
    for event in events:
        sig = signature_for_event(session, event)
        signatures.append(sig)
        explained = [grouper.explain(sig, p) for p in profiles]
        touching = sorted((e for e in explained if e["shared_actors"]),
                          key=lambda e: (-(e["score"] or -1), e["slug"]))
        decision = grouper.assign(sig, profiles)
        rows.append({
            "event_id": event.id,
            "summary": event.summary,
            "actors": sorted(grouper.actors.keys(sig.actors)),
            "actors_are_principal": sig.actors_are_principal,
            "region": sig.region,
            "candidates": touching,
            "decision": decision.slug,
            "decision_reasons": [r.value for r in decision.reasons],
            "stored": slugs.get(event.situation_id),
        })

    unassigned = [(sig, row) for sig, row in zip(signatures, rows)
                  if row["decision"] is None and sig.actors_are_principal]
    sets: dict[frozenset, list[int]] = defaultdict(list)
    pairs: dict[tuple, list[int]] = defaultdict(list)
    for sig, row in unassigned:
        key = frozenset(row["actors"])
        if len(key) >= grouper.config.policy.min_actors_to_create:
            sets[key].append(row["event_id"])
        for pair in combinations(sorted(key), 2):
            pairs[pair].append(row["event_id"])
    _, created = grouper.group([s for s, _ in unassigned], profiles)
    return {
        "generated_at": datetime.utcnow().isoformat(timespec="seconds"),
        "events": rows,
        "with_principals": sum(1 for r in rows if r["actors_are_principal"]),
        "decisions": dict(Counter(r["decision"] or "-" for r in rows)),
        "unassigned_actor_sets": {" + ".join(sorted(k)): v for k, v in sets.items()},
        "recurring_pairs": {" + ".join(k): v for k, v in pairs.items() if len(v) >= 2},
        "would_create": [p.slug for p in created],
    }


def format_situation_report(report: dict, principal_only: bool = True) -> str:
    lines = [f"{len(report['events'])} events, {report['with_principals']} with principal actors; "
             f"decisions: {report['decisions']}", ""]
    for r in report["events"]:
        if principal_only and not r["actors_are_principal"]:
            continue
        lines.append(f"#{r['event_id']} {r['summary'][:90]!r}")
        lines.append(f"    principal actors: {r['actors'] or '-'}"
                     + ("" if r["actors_are_principal"] else " (mentioned entities: no principals)")
                     + f"   region: {r['region']}")
        for c in r["candidates"]:
            if c["candidate"]:
                sig = ", ".join(f"{s['signal']}={s['value']}" for s in c["signals"])
                lines.append(f"    candidate {c['slug']}: score {c['score']:.2f} ({sig})")
            else:
                lines.append(f"    near-miss {c['slug']}: shares {c['shared_actors']}, {c['excluded']}")
        stored = f"   stored: {r['stored']}" if r["stored"] else ""
        lines.append(f"    -> {r['decision'] or 'unassigned'} {r['decision_reasons']}{stored}")
    lines += ["", "Creation (unassigned principal developments):",
              f"  exact actor sets: {report['unassigned_actor_sets'] or '-'}",
              f"  actor pairs recurring >= 2: {report['recurring_pairs'] or '-'}",
              f"  current rule would create: {report['would_create'] or '-'}"]
    return "\n".join(lines)
