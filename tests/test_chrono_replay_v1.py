"""Chronological-replay instrumentation: synthetic inputs only, no snapshot, no model, no network."""
import json
import random
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent / "evaluations" / "situation-membership" / "chrono-replay-v1"
sys.path.insert(0, str(ROOT))

from chrono_replay import guard, metrics                                   # noqa: E402
from chrono_replay.driver import BaseDev, chronological_order              # noqa: E402
from chrono_replay.providers import (ComponentEvidenceProvider, DictProvider, FrozenPredictions,  # noqa: E402
                                     ModelLocationProvider, ModelPrincipalsProvider, ModelTopicProvider, derive_v4)
from chrono_replay.runner import execute                                   # noqa: E402
from chrono_replay.snapshot import copy_snapshot, load_engine              # noqa: E402
from chrono_replay.util import load_pins, sha256_file                      # noqa: E402

T0 = datetime(2026, 11, 1, 12, 0, 0)


@pytest.fixture(scope="module")
def engine():
    pins = load_pins()
    return load_engine(ROOT / pins["engine"]["path"], pins["engine"]["sha256"])


def bases(n=6, same_time=False):
    out = []
    for i in range(n):
        t = T0 if same_time else T0 + timedelta(hours=26 * i)
        out.append(BaseDev(dev_id=100 + i, headline=f"Talks between A and B round {i}", lead="", first_reported_at=t,
                           report_share=1.0, hazard=None, hedges=[]))
    return out


def stored_providers(bs, with_components=True):
    topic = {b.dev_id: {"family": "diplomacy", "label": "negotiation", "confidence": None} for b in bs}
    loc = {b.dev_id: {"places": {"geneva": "switzerland"}, "event_country": "switzerland"} for b in bs}
    pr = {b.dev_id: {"names": ["A", "B"], "parties": ["a", "b"], "has_principals": True} for b in bs}
    p = {"topic": DictProvider("topic", topic), "location": DictProvider("location", loc),
         "principals": DictProvider("principals", pr)}
    if with_components:
        comp = {b.dev_id: {"component_sizes": [3, 2], "report_item_count": 5} for b in bs}
        p["components"] = DictProvider("components", comp)
    return p


def run(engine, tmp_path, bs, providers, mode="smoke", limit=None, mixed_from="none", name="o"):
    return execute(engine=engine, bases=bs, providers=providers, seeded_factory=lambda: [],
                   party_countries=lambda keys: set(), mode=mode, limit=limit, mixed_from=mixed_from,
                   out_root=tmp_path / name, identity={"test": 1}, manifest_extra={"git": {"sha": "t", "dirty": False}})


# -- ordering determinism ---------------------------------------------------------------------------------------

def test_order_is_total_and_input_order_independent(engine, tmp_path):
    bs = bases(8) + bases(2, same_time=True)           # ids collide in time at T0 for the last two
    for i, b in enumerate(bs[-2:]):
        b.dev_id = 900 - i                             # same timestamp, ids 900 and 899: id breaks the tie
    ref = [b.dev_id for b in chronological_order(bs)]
    for seed in range(5):
        sh = bs[:]
        random.Random(seed).shuffle(sh)
        assert [b.dev_id for b in chronological_order(sh)] == ref
    assert ref.index(899) < ref.index(900)
    a = run(engine, tmp_path, bs, stored_providers(bs), name="a")
    b_ = run(engine, tmp_path, sorted(bs, key=lambda x: -x.dev_id), stored_providers(bs), name="b")
    assert (a["out"] / "trace.jsonl").read_bytes() == (b_["out"] / "trace.jsonl").read_bytes()


def test_trace_rows_follow_time_order(engine, tmp_path):
    bs = bases(5)
    r = run(engine, tmp_path, bs, stored_providers(bs))
    times = [json.loads(l)["time"] for l in (r["out"] / "trace.jsonl").read_text().splitlines()]
    assert times == sorted(times) and len(times) == 5


# -- provenance in the trace -------------------------------------------------------------------------------------

def test_every_row_carries_provider_values_and_provenance(engine, tmp_path):
    bs = bases(4)
    r = run(engine, tmp_path, bs, stored_providers(bs), mixed_from="v4")
    for line in (r["out"] / "trace.jsonl").read_text().splitlines():
        row = json.loads(line)
        for role in ("topic", "location", "principals", "components"):
            assert row["inputs"][role]["provenance"]["provider_id"] == f"dict-{role}"
            assert row["inputs"][role]["provenance"]["origin"] == "stored"
            assert "value" in row["inputs"][role]
        assert row["inputs"]["components"]["value"]["v4_derived"] is True
        assert row["inputs"]["mixed"] == {"value": True, "from": "v4 (OWNER DECISION PENDING)"}
        assert r["summary"]["mixed_from"] == r["manifest"]["mixed_from"] == "v4 (OWNER DECISION PENDING)"
        assert row["mode"] == guard.SMOKE_LABEL and "candidates" in row and "reason" in row


def write_pred(tmp, name, rows, model_id="m-test", eval_scored=True, tamper=False):
    p = tmp / f"{name}.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    sha = sha256_file(p)
    rec = tmp / f"{name}.eval.json"
    rec.write_text(json.dumps({"model_id": model_id, "predictions_sha256": sha,
                               "acceptance": {"scored": eval_scored}}), encoding="utf-8")
    meta = {"model_id": model_id, "predictions_sha256": ("0" * 64 if tamper else sha),
            "acceptance_eval": {"record_path": rec.name, "record_sha256": sha256_file(rec)}}
    (tmp / f"{name}.jsonl.meta.json").write_text(json.dumps(meta), encoding="utf-8")
    return p


def test_model_provider_provenance_and_t3_consumption(engine, tmp_path):
    bs = bases(3)
    tp = write_pred(tmp_path, "topic", [
        {"development_id": 100, "topic_family": "diplomacy", "confidence": "high"},
        {"development_id": 101, "topic_family": "diplomacy", "confidence": "low"},
        {"development_id": 102, "topic_family": "out_of_scope", "confidence": "high"}])
    lp = write_pred(tmp_path, "loc", [
        {"development_id": 100, "event_country": "switzerland", "confidence": "medium",
         "places": [{"place": "geneva", "country": "switzerland", "role": "venue"},
                    {"place": "bern", "country": "switzerland", "role": "event"}]},
        {"development_id": 101, "event_country": "france", "confidence": "abstain", "places": []}])
    pp = write_pred(tmp_path, "pr", [{"development_id": 100, "principal_parties": ["A", "B"]}])
    prov = stored_providers(bs)
    prov["topic"] = ModelTopicProvider(FrozenPredictions(tp))
    prov["location"] = ModelLocationProvider(FrozenPredictions(lp))
    prov["principals"] = ModelPrincipalsProvider(FrozenPredictions(pp), lambda names: frozenset(n.lower() for n in names))
    r = run(engine, tmp_path, bs, prov)
    rows = [json.loads(l) for l in (r["out"] / "trace.jsonl").read_text().splitlines()]
    assert rows[0]["inputs"]["topic"]["provenance"]["model_id"] == "m-test"
    assert len(rows[0]["inputs"]["topic"]["provenance"]["predictions_sha256"]) == 12
    assert rows[0]["inputs"]["topic"]["value"]["family"] == "diplomacy"
    assert rows[1]["inputs"]["topic"]["value"]["family"] is None            # low confidence not consumed
    assert rows[1]["inputs"]["topic"]["value"]["label"] == "diplomacy"      # but visible
    assert rows[2]["inputs"]["topic"]["value"]["family"] is None            # out_of_scope is not a v2 family
    assert rows[0]["inputs"]["location"]["value"]["places"] == {"bern": "switzerland"}   # venue role not consumed
    assert rows[1]["inputs"]["location"]["value"]["event_country"] is None
    assert rows[2]["inputs"]["location"]["provenance"]["present"] is False
    assert rows[0]["inputs"]["principals"]["value"]["parties"] == ["a", "b"]
    m = r["manifest"]["providers"]
    assert m["topic"]["model_id"] == "m-test" and len(m["topic"]["predictions_sha256"]) == 64


def test_predictions_hash_mismatch_stops(tmp_path):
    p = write_pred(tmp_path, "t", [{"development_id": 1}], tamper=True)
    with pytest.raises(SystemExit, match="hash mismatch"):
        FrozenPredictions(p)


def test_duplicate_development_in_predictions_stops(tmp_path):
    p = write_pred(tmp_path, "d", [{"development_id": 1}, {"development_id": 1}])
    with pytest.raises(SystemExit, match="duplicate"):
        FrozenPredictions(p)


# -- refusal of final mode ---------------------------------------------------------------------------------------

def ok_kwargs(tmp_path, **over):
    t = FrozenPredictions(write_pred(tmp_path, "ft", [{"development_id": 1}], model_id="topic-1"))
    l = FrozenPredictions(write_pred(tmp_path, "fl", [{"development_id": 1}], model_id="loc-1"))
    kw = dict(topic=t, location=l, owner_approved="owner message 2026-12-01 approving final replay", limit=None,
              evalset_labels_present=True, git_dirty=False)
    kw.update(over)
    return kw


def test_final_allowed_only_when_everything_holds(tmp_path):
    assert guard.final_problems(**ok_kwargs(tmp_path)) == []


@pytest.mark.parametrize("over,needle", [
    ({"topic": None}, "topic: no model predictions"),
    ({"location": None}, "location: no model predictions"),
    ({"owner_approved": None}, "--owner-approved"),
    ({"owner_approved": "yes"}, "--owner-approved"),
    ({"limit": 50}, "--limit"),
    ({"evalset_labels_present": False}, "labels"),
    ({"git_dirty": True}, "dirty"),
    ({"git_dirty": None}, "dirty"),
    ({"mixed_from": "v4"}, "diagnostic only"),
])
def test_final_refused(tmp_path, over, needle):
    with pytest.raises(SystemExit) as e:
        guard.require_final(**ok_kwargs(tmp_path, **over))
    assert "REFUSED" in str(e.value) and needle in str(e.value)


def test_final_refused_when_acceptance_not_scored(tmp_path):
    t = FrozenPredictions(write_pred(tmp_path, "nt", [{"development_id": 1}], eval_scored=False))
    with pytest.raises(SystemExit) as e:
        guard.require_final(**ok_kwargs(tmp_path, topic=t))
    assert "acceptance scored" in str(e.value)


def test_final_refused_when_eval_record_missing_or_changed(tmp_path):
    p = write_pred(tmp_path, "mt", [{"development_id": 1}])
    (tmp_path / "mt.eval.json").write_text("{}", encoding="utf-8")        # hash no longer as the sidecar says
    with pytest.raises(SystemExit) as e:
        guard.require_final(**ok_kwargs(tmp_path, topic=FrozenPredictions(p)))
    assert "no acceptance-evaluation record" in str(e.value)


def test_cli_final_refuses_before_touching_the_snapshot(tmp_path):
    import run_replay
    with pytest.raises(SystemExit) as e:
        run_replay.main(["--mode", "final", "--snapshot", str(tmp_path / "does-not-exist.db")])
    assert "REFUSED" in str(e.value)


def test_smoke_output_is_labelled_and_reads_no_label(engine, tmp_path):
    bs = bases(3)
    r = run(engine, tmp_path, bs, stored_providers(bs))
    assert r["out"].name.startswith("SMOKE-NOT-A-RESULT-")
    assert (r["out"] / "NOT-A-RESULT.txt").exists()
    assert r["summary"]["status"] == guard.SMOKE_LABEL and r["summary"]["label_metrics"] is None
    with pytest.raises(SystemExit):                                       # final with no labels stops
        execute(engine=engine, bases=bs, providers=stored_providers(bs), seeded_factory=lambda: [],
                party_countries=lambda k: set(), mode="final", limit=None, mixed_from="none", out_root=tmp_path / "f",
                identity={}, manifest_extra={}, evalset={"key": {}, "case_ids": [], "anchors_of": {}, "founders_of": {},
                                                         "scopes": {"automatic": []}}, labels=None)


# -- byte-identical rerun and parity -------------------------------------------------------------------------------

def test_rerun_is_byte_identical_except_manifest_times(engine, tmp_path):
    bs = bases(7)
    a = run(engine, tmp_path, bs, stored_providers(bs), name="r1")
    b = run(engine, tmp_path, bs, stored_providers(bs), name="r2")
    assert a["out"].name == b["out"].name
    for f in ("trace.jsonl", "summary.json"):
        assert (a["out"] / f).read_bytes() == (b["out"] / f).read_bytes()
    ma, mb = a["manifest"], b["manifest"]
    for k in ("started_utc", "finished_utc"):
        ma.pop(k), mb.pop(k)
    assert ma == mb


def test_creation_retro_assignment_and_engine_parity(engine, tmp_path):
    bs = bases(4)
    r = run(engine, tmp_path, bs, stored_providers(bs, with_components=False))
    assert r["summary"]["engine_parity"]["engine_chronological_equal"] is True
    res = r["result"]
    assert res.created and res.created[0]["mode"] == "actor_process"
    assert res.assigned[100] == res.created[0]["slug"]                    # first Development joined retroactively
    row0 = json.loads((r["out"] / "trace.jsonl").read_text().splitlines()[0])
    assert row0["decision"]["assigned"] is None and row0["final_assigned"] == res.created[0]["slug"]
    assert row0["retro"] and row0["retro"][0]["as_founder"] is True


def test_limit_takes_the_first_developments_in_time_order(engine, tmp_path):
    bs = bases(10)
    r = run(engine, tmp_path, list(reversed(bs)), stored_providers(bs), limit=3)
    assert r["summary"]["trace_rows"] == 3
    assert r["result"].order == [100, 101, 102]


def test_mixed_from_none_never_sets_the_flag(engine, tmp_path):
    bs = bases(2)
    r = run(engine, tmp_path, bs, stored_providers(bs), mixed_from="none")
    row = json.loads((r["out"] / "trace.jsonl").read_text().splitlines()[0])
    assert row["inputs"]["mixed"]["value"] is None


# -- small pieces --------------------------------------------------------------------------------------------------

def test_derive_v4_on_read():
    assert derive_v4([5, 2, 1]) and not derive_v4([9, 1, 1]) and not derive_v4([]) and not derive_v4([3])


def test_component_provider_reads_pinned_file_and_checks_version(tmp_path):
    p = tmp_path / "c.jsonl"
    p.write_text(json.dumps({"development_id": 1, "algorithm_version": "report-components-v1",
                             "report_item_count": 3, "component_sizes": [2, 1]}) + "\n", encoding="utf-8")
    c = ComponentEvidenceProvider(p)
    assert c.get(1).value["component_sizes"] == [2, 1] and c.get(2).value == {}
    assert "mixed" not in json.dumps(c.get(1).value)                      # never stored under that name
    p.write_text(p.read_text().replace("v1", "v9"), encoding="utf-8")
    with pytest.raises(SystemExit):
        ComponentEvidenceProvider(p)


def test_snapshot_sha_mismatch_stops_and_source_untouched(tmp_path):
    src = tmp_path / "s.db"
    c = sqlite3.connect(src)
    c.execute("create table t(x)")
    c.commit()
    c.close()
    before = sha256_file(src)
    with pytest.raises(SystemExit, match="mismatch"):
        copy_snapshot(src, "0" * 64, tmp_path)
    conn, cp = copy_snapshot(src, before, tmp_path)
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("create table u(y)")                                 # copy is query_only
    conn.close()
    assert sha256_file(src) == before


def test_score_cases_on_synthetic_labels():
    key = {c: {"seed_group": "positive" if c == "S1" else None} for c in ("S1", "S2", "S3", "S4")}
    dec = {"S1": {"decision": "entered"}, "S2": {"decision": "entered"}, "S3": {"decision": "rejected"},
           "S4": {"decision": "entered"}}
    lab = {"S1": "MEMBER", "S2": "NOT_MEMBER", "S3": "MEMBER", "S4": "AMBIGUOUS"}
    s = metrics.score_cases(dec, lab, key)
    assert s["member_recall"] == {"n": 1, "of": 2, "rate": 0.5}
    assert s["member_precision"] == {"n": 1, "of": 2, "rate": 0.5}
    assert s["false_joins"]["cases"] == ["S2"] and s["false_joins"]["by_label"] == {"NOT_MEMBER": 1}
    assert s["owner_ambiguous"]["n"] == 1 and s["positive_seed_regressions"] == {"n": 0, "of": 1}
    assert "verdict" not in json.dumps(s)


def test_pins_are_verified_files():
    pins = load_pins()
    assert sha256_file(ROOT / pins["engine"]["path"]) == pins["engine"]["sha256"]
    assert sha256_file(ROOT / pins["seeded_scopes"]["path"]) == pins["seeded_scopes"]["sha256"]
    assert sha256_file(ROOT / pins["component_evidence"]["path"]) == pins["component_evidence"]["sha256"]


def test_default_is_none_and_labelled(engine, tmp_path):
    bs = bases(2)
    r = run(engine, tmp_path, bs, stored_providers(bs))
    assert r["summary"]["mixed_from"] == "none" and r["manifest"]["mixed_from"] == "none"
    import run_replay
    assert run_replay.parse_args(["--snapshot", "x"]).mixed_from == "none"
