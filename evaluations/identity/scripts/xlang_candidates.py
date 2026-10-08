"""Cross-language candidate pairs for identity gold revision 3 (owner review before any benchmark).

    python evaluations/identity/scripts/xlang_candidates.py [--min-cosine 0.50]
      -> review-rev3/xlang-candidates.json

Replays the identity **development** windows that contain non-English items (2026-09-30-multilingual,
2026-10-03-live, 2026-10-05-live) with the cross-language stage switched on in memory only. The configuration file
is unchanged and the stage stays off in production. Every proposed pair is recorded, accepted or rejected by the
anchor guard, with external item ids and the guard's evidence. A lower ``--min-cosine`` widens the net, so the
review also sees near misses and the threshold can be judged on labels.

The rules decide which pairs are reviewed, never their labels. The identity holdout window is never replayed.
"""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

WINDOWS = ["2026-09-30-multilingual", "2026-10-03-live", "2026-10-05-live"]


def main() -> int:
    min_cos = float(sys.argv[sys.argv.index("--min-cosine") + 1]) if "--min-cosine" in sys.argv else 0.50
    import replay_current
    from osint_monitor.core import config as C
    from osint_monitor.core.database import RawItem
    from osint_monitor.processors import cross_language as X

    original_loader = C.load_event_grouping_config

    def loader(*a, **k):
        cfg = original_loader(*a, **k)
        cfg.cross_language.enabled = True
        cfg.cross_language.min_cosine = min_cos
        return cfg

    C.load_event_grouping_config = loader
    import osint_monitor.processors.clustering as CL
    CL.load_event_grouping_config = loader

    found: list[dict] = []
    original_propose = X.propose

    def recording_propose(units, config, geo):
        links = original_propose(units, config, geo)
        from osint_monitor.core.database import get_session
        s = get_session()
        ext = {r.id: (r.external_id, r.title) for r in s.query(RawItem.id, RawItem.external_id, RawItem.title)
               .filter(RawItem.id.in_([i for l in links for i in l.a.items + l.b.items]))}
        s.close()
        for l in links:
            found.append({"window": current["window"], "accepted": l.accepted, "cosine": round(l.cosine, 3),
                          "evidence": l.evidence,
                          "a": [ext[i][0] for i in l.a.items], "a_langs": sorted(l.a.langs),
                          "a_titles": [ext[i][1][:110] for i in l.a.items[:3]],
                          "b": [ext[i][0] for i in l.b.items], "b_langs": sorted(l.b.langs),
                          "b_titles": [ext[i][1][:110] for i in l.b.items[:3]]})
        return links

    X.propose = recording_propose
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    current = {}
    for w in manifest["windows"]:
        if w["id"] not in WINDOWS:
            continue
        assert w["split"] == "development"
        current["window"] = w["id"]
        trace = replay_current.replay(w)
        print(w["id"], len(trace["developments"]), "Developments", flush=True)
    # one entry per unordered unit pair (the same pair recurs at every tick it is re-proposed)
    uniq = {}
    for f in found:
        key = (f["window"], frozenset(f["a"]), frozenset(f["b"]))
        if key not in uniq or f["cosine"] > uniq[key]["cosine"]:
            uniq[key] = f
    out = ROOT / "review-rev3"
    out.mkdir(exist_ok=True)
    rows = sorted(uniq.values(), key=lambda f: (f["window"], -f["cosine"]))
    (out / "xlang-candidates.json").write_text(json.dumps({"min_cosine": min_cos, "pairs": rows}, indent=1,
                                                          ensure_ascii=False) + "\n", encoding="utf-8")
    print(len(rows), "distinct candidate pairs;", sum(1 for r in rows if r["accepted"]), "accepted by the anchor guard")
    return 0


if __name__ == "__main__":
    sys.exit(main())
