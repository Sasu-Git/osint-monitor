"""The chronological driver: Developments in first-report order, each decided by the pinned v2 engine, with a trace.

``step_replay`` is the engine's ``chronological`` loop (candidate ``4f4f85d``, unmodified) with trace hooks added and
nothing else changed: same order, same ``decide`` / ``creation_keys`` / ``found`` calls, same pooling and retro
assignment. ``check_parity`` re-runs the engine's own ``chronological`` on the same features and compares the
assignments and the created Situations, so a drift between this loop and the engine is detected on every run.

No threshold is chosen here and no rule is changed. The driver reads no label.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from .providers import Provider, Provided, derive_v4
from .util import dumps

EVIDENCE_KEYS = ("coverage", "shared_parties", "generic_parties_matched", "scope_signals", "half_rule",
                 "better_situation", "tied_with", "hedge_terms", "mixed_flag", "founders")


@dataclass
class BaseDev:
    """What the Development is, independent of any upstream model: text-derived, not provider-supplied."""
    dev_id: int
    headline: str
    lead: str
    first_reported_at: datetime | None
    report_share: float
    hazard: tuple[str, str | None] | None
    hedges: list[str]


@dataclass
class ReplayResult:
    order: list[int]
    rows: list[dict]
    situations: list
    assigned: dict[int, str]
    created: list[dict] = field(default_factory=list)
    parity: dict = field(default_factory=dict)
    features: dict = field(default_factory=dict)


def chronological_order(bases: list[BaseDev]) -> list[BaseDev]:
    """first_reported_at ascending, ties by Development id: total, so a rerun orders identically."""
    return sorted(bases, key=lambda b: (b.first_reported_at or datetime.min, b.dev_id))


def build_features(engine, base: BaseDev, providers: dict[str, Provider], mixed_from: str):
    got: dict[str, Provided] = {r: p.get(base.dev_id) for r, p in providers.items()}
    topic = got["topic"].value
    loc = got["location"].value
    pr = got["principals"].value
    comp = got["components"].value if "components" in got else {}
    sizes = comp.get("component_sizes")
    v4 = derive_v4(sizes) if sizes is not None else None
    mixed = v4 if (mixed_from == "v4" and v4 is not None) else None
    feats = engine.DevFeatures(
        event_id=base.dev_id, headline=base.headline, lead=base.lead, first_reported_at=base.first_reported_at,
        parties=frozenset(pr.get("parties", [])), has_principals=bool(pr.get("has_principals")),
        family=topic.get("family"), places=dict(loc.get("places", {})), event_country=loc.get("event_country"),
        report_share=base.report_share, hazard=base.hazard, hedges=list(base.hedges), mixed=mixed)
    inputs = {
        "base": {"headline": base.headline, "lead": base.lead, "report_share": round(base.report_share, 6),
                 "hazard": list(base.hazard) if base.hazard else None, "hedges": list(base.hedges)},
        "topic": {"value": topic, "provenance": got["topic"].provenance},
        "location": {"value": loc, "provenance": got["location"].provenance},
        "principals": {"value": pr, "provenance": got["principals"].provenance},
        "components": ({"value": {**comp, "v4_derived": v4}, "provenance": got["components"].provenance}
                       if "components" in got else None),
        "mixed": {"value": mixed, "from": mixed_from if "components" in got else "no component provider"},
    }
    return feats, inputs


def _cand(slug, sit, dec) -> dict:
    ev = {k: dec.evidence[k] for k in EVIDENCE_KEYS if k in dec.evidence}
    return {"slug": slug, "mode": sit.mode, "outcome": dec.outcome, "reason": dec.reason, "evidence": ev}


def step_replay(engine, bases: list[BaseDev], providers: dict[str, Provider], seeded: list, party_countries: Callable,
                *, run_mode: str, mixed_from: str = "v4") -> ReplayResult:
    ordered = chronological_order(bases)
    sits = list(seeded)
    assigned: dict[int, str] = {}
    pool: dict[tuple, list] = {}
    rows: list[dict] = []
    created: list[dict] = []
    feats_by_id: dict[int, object] = {}
    row_of: dict[int, dict] = {}
    for step, base in enumerate(ordered):
        d, inputs = build_features(engine, base, providers, mixed_from)
        feats_by_id[d.event_id] = d
        row = {"step": step, "mode": run_mode, "development_id": d.event_id,
               "time": d.first_reported_at.isoformat() if d.first_reported_at else None, "inputs": inputs,
               "open_situations": [s.slug for s in sits], "candidates": [], "creation": [], "retro": [],
               "created_here": []}
        for s in sits:
            dec = engine.decide(d, s, sits)
            row["candidates"].append(_cand(s.slug, s, dec))
            if dec.outcome == "MEMBER":
                assigned[d.event_id] = s.slug
        row_of[d.event_id] = row
        rows.append(row)
        if d.event_id in assigned:
            row["decision"] = {"assigned": assigned[d.event_id], "via": "open_situation"}
            continue
        for key in engine.creation_keys(d):
            now = d.first_reported_at or datetime.min
            pool[key] = [m for m in pool.get(key, []) if m.event_id not in assigned
                         and now - (m.first_reported_at or datetime.min) <= engine.CREATE_WINDOW] + [d]
            c = {"key": list(_keyrepr(key)), "pool_size": len(pool[key]), "founded": None}
            row["creation"].append(c)
            if any(s.slug == engine._slug_of(key) for s in sits):
                c["founded"] = "exists:" + engine._slug_of(key)
                continue
            new = engine.found(key, pool[key], party_countries)
            if new is None:
                continue
            sits.append(new)
            c["founded"] = new.slug
            row["created_here"].append(new.slug)
            created.append({"slug": new.slug, "mode": new.mode, "founders": list(new.founders), "step": step,
                            "development_id": d.event_id, "scope": new.snapshot()})
            for m in pool[key]:
                assigned[m.event_id] = new.slug
                row_of[m.event_id]["retro"].append({"slug": new.slug, "outcome": "MEMBER",
                                                    "reason": "EXACT_KEY_RECURRENCE", "as_founder": True,
                                                    "at_step": step})
            for _k2, members in pool.items():
                for m in members:
                    if m.event_id in assigned:
                        continue
                    dec = engine.decide(m, new, sits)
                    row_of[m.event_id]["retro"].append({"slug": new.slug, "outcome": dec.outcome,
                                                        "reason": dec.reason, "as_founder": False, "at_step": step})
                    if dec.outcome == "MEMBER":
                        assigned[m.event_id] = new.slug
            break
        row["decision"] = {"assigned": None, "via": "none_at_step"}
    for r in rows:                       # final assignment after retro creation, and a plain reason for the row
        r["final_assigned"] = assigned.get(r["development_id"])
        r["reason"] = _reason(r)
    res = ReplayResult(order=[b.dev_id for b in ordered], rows=rows, situations=sits, assigned=assigned,
                       created=created, features=feats_by_id)
    return res


def _keyrepr(key: tuple):
    for k in key:
        yield sorted(k) if isinstance(k, (set, frozenset)) else k


def _reason(r: dict) -> str:
    if r["decision"]["assigned"]:
        mem = [c for c in r["candidates"] if c["slug"] == r["decision"]["assigned"]]
        return mem[0]["reason"] if mem else "ASSIGNED"
    if r["final_assigned"]:
        return "ASSIGNED_RETRO:" + r["final_assigned"]
    if not r["candidates"]:
        return "NO_OPEN_SITUATIONS"
    # the reason codes of the candidates, most frequent first, so a reader sees why nothing admitted it
    counts: dict[str, int] = {}
    for c in r["candidates"]:
        counts[c["reason"] or c["outcome"]] = counts.get(c["reason"] or c["outcome"], 0) + 1
    return "REJECTED_BY_ALL:" + ",".join(f"{k}x{v}" for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def check_parity(engine, result: ReplayResult, seeded_factory: Callable[[], list], party_countries: Callable) -> dict:
    """Run the engine's own ``chronological`` on the same features and compare. ``seeded_factory`` returns fresh
    Situation objects (the engine appends to the list it is given)."""
    devs = [result.features[i] for i in result.order]
    ref = engine.chronological(devs, seeded_factory(), party_countries)
    same_assign = ref["assigned"] == result.assigned
    same_sits = [s.slug for s in ref["situations"]] == [s.slug for s in result.situations]
    ref_log = {i: {slug: (d.outcome, d.reason) for slug, d in per.items()} for i, per in ref["log"].items()}
    mine = {}
    for r in result.rows:
        per = {c["slug"]: (c["outcome"], c["reason"]) for c in r["candidates"]}
        mine[r["development_id"]] = per
    same_open = all(all(ref_log[i].get(s) == v for s, v in per.items()) for i, per in mine.items())
    return {"engine_chronological_equal": bool(same_assign and same_sits and same_open),
            "assignments_equal": same_assign, "situation_list_equal": same_sits, "open_decisions_equal": same_open}


def trace_lines(result: ReplayResult) -> list[str]:
    return [dumps(r) for r in result.rows]
