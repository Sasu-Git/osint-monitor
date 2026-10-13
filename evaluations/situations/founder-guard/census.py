"""Census of founder pairs for the founder-distinctness guard evaluation (no labels, no sampling).

    python evaluations/situations/founder-guard/census.py DB   # -> census.json

A founder pair is two Developments with the same canonical principal actor set (>= min_actors_to_create actors,
the exact actor-set recurrence the Situation creation rule counts) whose first reports are at most create_window_days
apart. For each pair: languages, time gap, shared specific places (as the guard compares them), whether the guard
would count the pair as one occurrence, and the Situations its Developments belong to. The database is opened
read-only.
"""
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HERE = Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding="utf-8")


def main(db: str) -> int:
    from osint_monitor.core.config import load_situations_config
    from osint_monitor.core.database import Event, Situation
    from osint_monitor.processors.development_segmentation import gazetteer
    from osint_monitor.processors.situations.grouper import SituationGrouper
    from osint_monitor.processors.situations.store import signature_for_event

    s = sessionmaker(bind=create_engine(f"sqlite:///file:{db}?mode=ro&uri=true", connect_args={"uri": True}))()
    cfg = load_situations_config()
    guarded = SituationGrouper(cfg.model_copy(update={"policy": cfg.policy.model_copy(
        update={"founder_same_occurrence_hours": 48})}))
    geo = gazetteer(False)
    slugs = dict(s.query(Situation.id, Situation.slug))
    groups = defaultdict(list)
    sigs = {}
    for e in s.query(Event).order_by(Event.id):
        sig = signature_for_event(s, e)
        if not sig.actors_are_principal:
            continue
        key = guarded.actors.keys(sig.actors)
        if len(key) < cfg.policy.min_actors_to_create:
            continue
        sigs[e.id] = (sig, slugs.get(e.situation_id))
        groups[key].append(e.id)
    window = cfg.policy.create_window_days * 86400
    pairs = []
    for key, ids in groups.items():
        for a, b in combinations(sorted(ids), 2):
            sa, sb = sigs[a][0], sigs[b][0]
            if not (sa.occurred_at and sb.occurred_at):
                continue
            gap = abs((sa.occurred_at - sb.occurred_at).total_seconds())
            if gap > window:
                continue
            shared = sorted({f"{x}~{y}" for x in sa.places for y in sb.places
                             if x == y or geo.same_or_contains(x, y)})
            pairs.append({"a": a, "b": b, "actor_set": sorted(key), "gap_hours": round(gap / 3600, 1),
                          "langs": [sa.languages, sb.languages],
                          "cross_language": not (set(sa.languages) & set(sb.languages)),
                          "shared_places": shared[:8],
                          "guard_same": guarded.distinct_occurrences([sa, sb]) == 1,
                          "situations": [sigs[a][1], sigs[b][1]],
                          "titles": [sa.title[:140], sb.title[:140]]})
    out = {"db": db, "pairs": pairs, "actor_sets": len(groups),
           "developments": sum(len(v) for v in groups.values())}
    (HERE / "census.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str) + "\n",
                                      encoding="utf-8", newline="\n")
    n = len(pairs)
    print(f"{out['developments']} Developments in {out['actor_sets']} actor sets; {n} founder pairs")
    print(" cross-language:", sum(p["cross_language"] for p in pairs),
          "| cross-language + shared place <=48h (guard: one occurrence):", sum(p["guard_same"] for p in pairs))
    print(" same-language + shared place <=48h:", sum(1 for p in pairs if not p["cross_language"] and p["shared_places"]
                                                      and p["gap_hours"] <= 48))
    print(" shared place but >48h:", sum(1 for p in pairs if p["shared_places"] and p["gap_hours"] > 48))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
