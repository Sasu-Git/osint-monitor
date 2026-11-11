"""Score replay_v2.py decisions on the 126-case DIAGNOSTIC set with the frozen metric code, both label bases.

Development evidence only, never acceptance. Uses evalset/score.py and subsample/score_subsample.py unchanged
(imported from the evaluation branch's worktree); their loader expects all 379 cases, so the 126 decisions are passed
to ``score_restricted`` directly.

    python score_dev.py EVALSET_DIR DECISIONS.json OUT.json
"""
import json
import sys
from pathlib import Path


def main(evalset: str, decisions: str, out: str) -> int:
    ev = Path(evalset)
    sys.path[:0] = [str(ev / "subsample"), str(ev)]
    import labels_subsample
    import score
    import score_subsample
    from score_first_answers import first_answers

    key = score.load_key(ev)
    ids = labels_subsample.manifest_ids(ev / "subsample")
    raw = json.loads(Path(decisions).read_text(encoding="utf-8"))
    dec = raw["decisions"]
    assert set(dec) == set(ids), "decisions must cover exactly the 126 cases"
    final = score_subsample.load_frozen_labels(ev / "subsample")
    first = first_answers(ids)
    res = {"rule": raw["rule"], "status": "DEVELOPMENT EVIDENCE on the diagnostic set; not acceptance"}
    for basis, labels in (("first", first), ("final", final)):
        res[basis] = score_subsample.score_restricted({c: labels[c] for c in ids}, key, ids, (raw["rule"], dec))
    Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    for basis in ("first", "final"):
        for s in res[basis]["systems"]:
            o = s["overall"]
            print(f"{basis:5} {s['system'][:44]:44} recall {o['recall_member']['n']}/{o['recall_member']['of']} "
                  f"precision {o['precision_member']['n']}/{o['precision_member']['of']} "
                  f"NOT_MEMBER-rej {o['not_member_rejected']['rate']} "
                  f"per-label {{{', '.join(f'{k}: {v['rate']}' for k, v in o['non_member_label_rejected'].items())}}} "
                  f"pos-seed-reg {o['positive_seed_regressions']['all']['n']}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(*sys.argv[1:4]))
