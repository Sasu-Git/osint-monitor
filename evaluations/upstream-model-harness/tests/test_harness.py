"""Harness tests on SYNTHETIC gold only. No real label, case or threshold is used."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

from fixtures import make_features_file, make_gold, make_snapshot  # noqa: E402
from upstream_harness import checker, features as F, metrics as M  # noqa: E402
from upstream_harness.gold import GoldError, GoldTrack  # noqa: E402
from upstream_harness.model import Bands, calibrate  # noqa: E402
from upstream_harness.run import do_calibrate, do_score, main as run_main  # noqa: E402
from upstream_harness.splits import (AcceptanceAlreadyScored, AcceptanceInCalibration, SplitGuard,  # noqa: E402
                                     acquire_acceptance_lock)


# ------------------------------------------------------------------ stub baseline (tests only)
class Stub:
    def __init__(self, track, label, model_id="stub-1"):
        self.track, self.label, self.model_id = track, label, model_id
        self.seen = []

    def predict(self, case):
        self.seen.append(case["development_id"])
        return self.label, (case["development_id"] % 10) / 10


@pytest.fixture
def gold(tmp_path):
    return make_gold(tmp_path / "gold")


# ------------------------------------------------------------------ checker
def test_checker_passes_complete_frozen_gold(gold, capsys):
    assert checker.main(["--gold-root", str(gold)]) == 0
    assert "PASS" in capsys.readouterr().out


def test_checker_passes_on_crlf_checkout(tmp_path):
    g = make_gold(tmp_path / "g", crlf=True)
    assert checker.main(["--gold-root", str(g)]) == 0


def test_checker_refuses_partial_labels_with_counts_not_values(tmp_path, capsys):
    g = make_gold(tmp_path / "g", label="partial", frozen=False)
    code = checker.main(["--gold-root", str(g)])
    cap = capsys.readouterr()
    assert code == 1
    out = cap.out + cap.err
    assert "REFUSE" in out and "primary labelled" in out and "not frozen" in out
    for forbidden in ("sanctions", "military_action", "UKR", "FRA", "out_of_scope"):
        assert forbidden not in out


def test_checker_refuses_no_labels(tmp_path):
    g = make_gold(tmp_path / "g", label="none", frozen=False)
    assert checker.main(["--gold-root", str(g)]) == 1


def test_checker_refuses_unfrozen_even_if_complete(tmp_path):
    g = make_gold(tmp_path / "g", frozen=False)
    res = checker.check(g)
    assert not all(r.ok for r in res)
    assert any("not frozen" in p for p in res[0].problems)


def test_checker_refuses_labels_edited_after_freeze(gold):
    p = gold / "topic" / "labels.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert any("freeze record" in x for x in checker.check(gold, ("topic",))[0].problems)


def test_checker_refuses_invalid_label_without_echoing_value(tmp_path):
    g = make_gold(tmp_path / "g", frozen=False)
    import yaml
    p = g / "topic" / "labels.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    first = sorted(d)[0]
    d[first]["action_type"] = "totally_made_up"
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    res = checker.check(g, ("topic",))[0]
    assert any("not in taxonomy" in x for x in res.problems)
    assert "totally_made_up" not in "\n".join(res.problems)


def test_checker_refuses_unknown_country_and_missing_role_mentions(tmp_path):
    g = make_gold(tmp_path / "g", frozen=False)
    import yaml
    p = g / "location" / "labels.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8"))
    ids = sorted(d)
    d[ids[1]]["event_country"] = "ZZZ"
    role_case = next(i for i in ids if "place_mentions" in d[i])
    d[role_case]["place_mentions"] = {}
    p.write_text(yaml.safe_dump(d), encoding="utf-8")
    probs = "\n".join(checker.check(g, ("location",))[0].problems)
    assert "event_country not in vocabulary" in probs and "place mentions missing" in probs


def test_checker_refuses_tampered_split(gold):
    p = gold / "topic" / "split.json"
    s = json.loads(p.read_text(encoding="utf-8"))
    s["development"].append(s["acceptance"].pop())
    p.write_text(json.dumps(s, indent=1) + "\n", encoding="utf-8")
    probs = "\n".join(checker.check(gold, ("topic",))[0].problems)
    assert "differs from FREEZE.md" in probs and "differs from split.py output" in probs


def test_checker_require_development_only(tmp_path):
    g = make_gold(tmp_path / "g", label="all")
    # remove acceptance labels from the unfrozen copy: development-only requirement still needs the freeze marker
    assert all(r.ok for r in checker.check(g, require="development"))


def test_checker_counts_per_split(gold):
    res = checker.check(gold, ("topic",))[0]
    assert res.counts["development"]["cases"] + res.counts["acceptance"]["cases"] == 20
    assert res.counts["development"]["primary_labelled"] == res.counts["development"]["cases"]


# ------------------------------------------------------------------ split guard / lock
def test_calibration_guard_refuses_acceptance_cases(gold):
    gt = GoldTrack(gold, "topic")
    g = SplitGuard(gt, "calibration")
    assert set(g.case_ids) == set(gt.split_ids("development"))
    acc = gt.split_ids("acceptance")[0]
    with pytest.raises(AcceptanceInCalibration):
        g.check_id(acc)
    assert set(g.labels("primary")) <= set(g.case_ids)
    assert not set(g.labels("secondary")) & set(gt.split_ids("acceptance"))


def test_calibrate_never_predicts_acceptance_cases(tmp_path):
    g = make_gold(tmp_path / "g")
    fp = tmp_path / "f.json"
    feats = make_features_file(tmp_path, g, "topic", fp)
    gt = GoldTrack(g, "topic")
    m = Stub("topic", "sanctions")
    calibrate(m, feats, SplitGuard(gt, "calibration"), bands=Bands(0.7, 0.3))
    assert set(m.seen) == set(gt.split_ids("development"))


def test_acceptance_lock_once_then_force_logged(tmp_path):
    d = tmp_path / "locks"
    acquire_acceptance_lock(d, "topic", "m1", {"x": 1})
    with pytest.raises(AcceptanceAlreadyScored):
        acquire_acceptance_lock(d, "topic", "m1", {"x": 2})
    acquire_acceptance_lock(d, "topic", "m2", {"x": 1})            # another model id is independent
    acquire_acceptance_lock(d, "topic", "m1", {"x": 3}, force_rescore=True, force_reason="owner asked")
    log = (d / "topic" / "rescore-log.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(log) == 1 and json.loads(log[0])["reason"] == "owner asked" and json.loads(log[0])["forced"]


# ------------------------------------------------------------------ calibration has no defaults
def test_bands_have_no_default():
    with pytest.raises(TypeError):
        Bands()
    with pytest.raises(ValueError):
        Bands(0.2, 0.5)


def test_calibrate_requires_exactly_one_of_bands_or_rule(tmp_path):
    g = make_gold(tmp_path / "g")
    feats = make_features_file(tmp_path, g, "topic", tmp_path / "f.json")
    guard = SplitGuard(GoldTrack(g, "topic"), "calibration")
    with pytest.raises(ValueError):
        calibrate(Stub("topic", "other"), feats, guard)
    with pytest.raises(ValueError):
        calibrate(Stub("topic", "other"), feats, guard, bands=Bands(1, 0), selection_rule=lambda r: Bands(1, 0))


def test_selection_rule_sees_only_development_records(tmp_path):
    g = make_gold(tmp_path / "g")
    feats = make_features_file(tmp_path, g, "topic", tmp_path / "f.json")
    gt = GoldTrack(g, "topic")
    seen = {}

    def rule(recs):
        seen["ids"] = {r["case"] for r in recs}
        seen["keys"] = set(recs[0])
        return Bands(0.6, 0.2)
    rec = calibrate(Stub("topic", "sanctions"), feats, SplitGuard(gt, "calibration"), selection_rule=rule)
    assert seen["ids"] == set(gt.split_ids("development"))
    assert not any("gold" in k for k in seen["keys"])
    assert rec["bands"] == {"high_min": 0.6, "medium_min": 0.2}


# ------------------------------------------------------------------ metrics (hand computed)
def rec(case, gold, label, band, lang="en", gold2=None):
    return {"case": case, "lang": lang, "label": label, "score": 0.0, "band": band,
            "gold": {"primary": gold, "secondary": gold2 or gold}}


TOPIC = [rec(1, "A", "A", "high"), rec(2, "A", "A", "high"), rec(3, "A", "B", "high"), rec(4, "B", "B", "medium"),
         rec(5, "B", "A", "medium"), rec(6, "C", "C", "low"), rec(7, "unknown", "A", "medium"),
         rec(8, "A", None, "high"), rec(9, "B", "B", "high"), rec(10, "A", "A", "medium", lang="es")]


def test_topic_metrics_hand_computed():
    ev = M.evaluate_basis(TOPIC, "primary", "topic", n_boot=50)
    ho, hm = ev["high_only"], ev["high_medium"]
    assert (ho["n"], ho["emitted"], ho["correct"]) == (10, 4, 3)           # cases 1,2,3,9 emitted; 1,2,9 correct
    assert ho["precision"] == pytest.approx(0.75) and ho["coverage"] == pytest.approx(0.4)
    assert (hm["emitted"], hm["correct"]) == (8, 5)                         # 1,2,3,4,5,7,9,10; correct 1,2,4,9,10
    assert hm["precision"] == pytest.approx(5 / 8) and hm["coverage"] == pytest.approx(0.8)
    assert hm["abstention"] == pytest.approx(0.2)
    assert hm["n_recall_base"] == 9 and hm["recall"] == pytest.approx(5 / 9)  # gold `unknown` excluded from recall base
    a = hm["per_class"]["A"]
    assert (a["predicted"], a["tp"], a["support"]) == (5, 3, 5)
    assert a["precision"] == pytest.approx(0.6) and a["recall"] == pytest.approx(0.6)
    assert hm["per_class"]["C"]["predicted"] == 0 and hm["per_class"]["C"]["precision"] is None
    assert hm["confusion"]["A"] == {"A": 3, "ABSTAIN": 1, "B": 1}
    assert hm["confusion"]["unknown"] == {"A": 1}
    assert hm["gold_unknown"] == {"n": 1, "abstained": 0, "emitted_a_type": 1}
    assert hm["by_language"]["es"] == {"n": 1, "emitted": 1, "coverage": 1.0, "abstention": 0.0, "precision": 1.0}


def test_other_counts_as_typed_and_unknown_label_is_abstention():
    r = [rec(1, "other", "other", "high"), rec(2, "A", "unknown", "high")]
    hm = M.evaluate_basis(r, "primary", "topic", n_boot=10)["high_medium"]
    assert hm["emitted"] == 1 and hm["precision"] == 1.0


def test_verdict_pass_fail_and_inconclusive():
    ok = [rec(i, "A", "A", "high") for i in range(10)]
    bad = ok[:8] + [rec(98, "A", "B", "high"), rec(99, "A", "B", "high")]
    ev = lambda r, b: M.evaluate_basis(r, b, "topic", n_boot=10)  # noqa: E731
    assert M.verdict("topic", {"primary": ev(ok, "primary"), "secondary": ev(ok, "secondary")})["verdict"] == "PASS"
    assert M.verdict("topic", {"primary": ev(bad, "primary"), "secondary": ev(bad, "secondary")})["verdict"] == "FAIL"
    # same predictions, secondary answers flip two cases to the predicted label -> pass on one basis, fail on the other
    flip = [dict(r, gold={"primary": r["gold"]["primary"], "secondary": r["label"]}) for r in bad]
    v = M.verdict("topic", {"primary": ev(flip, "primary"), "secondary": ev(flip, "secondary")})
    assert v["per_basis"] == {"primary": "FAIL", "secondary": "PASS"} and v["verdict"] == "INCONCLUSIVE"


def test_location_has_no_verdict_and_containment_aware_match():
    L = [rec(1, "FRA", "FRA", "high"), rec(2, "UKR", "RUS", "high"), rec(3, "MULTI", "MULTI", "medium"),
         rec(4, "NONE", "UKR", "medium"), rec(5, "NONE", "NONE", "high"), rec(6, "PSE", "ISR", "high")]
    contains = {"ISR": {"PSE"}}
    ev = M.evaluate_basis(L, "primary", "location", contains=contains, n_boot=10)["high_medium"]
    assert ev["precision"] == pytest.approx(3 / 6) and ev["precision_containment_aware"] == pytest.approx(4 / 6)
    assert ev["none"] == {"precision": 1.0, "recall": 0.5}
    assert ev["multi"] == {"precision": 1.0, "recall": 1.0}
    assert M.verdict("location", {"primary": {}})["verdict"] is None
    no_table = M.evaluate_basis(L, "primary", "location", n_boot=10)["high_medium"]
    assert no_table["precision_containment_aware"] == no_table["precision"]


def test_bootstrap_fixed_seed_reproducible():
    a = M.bootstrap(TOPIC, "primary", "high_medium", "topic", None, n_boot=200)
    b = M.bootstrap(TOPIC, "primary", "high_medium", "topic", None, n_boot=200)
    c = M.bootstrap(TOPIC, "primary", "high_medium", "topic", None, n_boot=200, seed=1)
    assert a == b and a != c
    lo, hi = a["intervals"]["precision"]["lo"], a["intervals"]["precision"]["hi"]
    assert 0 <= lo <= 5 / 8 + 1e-9 <= hi + 1e-9 or lo <= hi


# ------------------------------------------------------------------ end to end with the stub
def _setup(tmp_path, **kw):
    g = make_gold(tmp_path / "g", **kw)
    fp = tmp_path / "feat" / "f.json"
    make_features_file(tmp_path, g, "topic", fp)
    return g, fp, tmp_path / "out"


def test_end_to_end_calibrate_then_score_once(tmp_path):
    g, fp, out = _setup(tmp_path)
    m = Stub("topic", "sanctions")
    cal = do_calibrate(g, "topic", fp, m, out, bands=Bands(0.7, 0.3))
    cpath = out / "calibrations" / "topic" / "stub-1.json"
    assert cpath.exists() and cal["n_development"] == 8
    rep = do_score(g, "topic", fp, m, cpath, out)
    for k in ("git_sha", "dirty", "snapshot_sha256", "split_json_sha256_lf", "gold_labels_yaml_sha256", "features_hash",
              "package_versions", "bootstrap_seed", "timestamp_utc", "model_id"):
        assert k in rep["metadata"], k
    assert rep["n"] == 12 and set(rep["per_basis"]) == {"primary", "secondary"}
    assert rep["verdict"]["per_basis"]["primary"] in ("PASS", "FAIL", "NOT_EVALUABLE")
    assert (out / "reports" / "topic" / "stub-1.acceptance.json").exists()
    with pytest.raises(AcceptanceAlreadyScored):
        do_score(g, "topic", fp, m, cpath, out)
    do_score(g, "topic", fp, m, cpath, out, force_rescore=True, reason="test")
    assert (out / "locks" / "topic" / "rescore-log.jsonl").exists()


def test_score_is_deterministic(tmp_path):
    g, fp, out = _setup(tmp_path)
    m = Stub("topic", "sanctions")
    do_calibrate(g, "topic", fp, m, out, bands=Bands(0.7, 0.3))
    c = out / "calibrations" / "topic" / "stub-1.json"
    r1 = do_score(g, "topic", fp, m, c, out)
    r2 = do_score(g, "topic", fp, m, c, out, force_rescore=True, reason="determinism")
    assert r1["per_basis"] == r2["per_basis"] and r1["verdict"] == r2["verdict"]


def test_score_inconclusive_when_bases_disagree(tmp_path):
    g = make_gold(tmp_path / "g")
    gt = GoldTrack(g, "topic")
    acc = gt.split_ids("acceptance")
    g2 = make_gold(tmp_path / "g2", revise=tuple(acc))
    fp = tmp_path / "f.json"
    make_features_file(tmp_path, g2, "topic", fp)
    prim, sec = GoldTrack(g2, "topic").load_primary(), GoldTrack(g2, "topic").load_final()
    assert any(prim[i]["action_type"] != sec[i]["action_type"] for i in acc)
    # a model that answers the FIRST answers exactly passes the primary basis, fails the secondary basis
    class Oracle:
        track, model_id = "topic", "oracle"
        def predict(self, case):
            return prim[case["development_id"]]["action_type"], 1.0
    out = tmp_path / "out"
    do_calibrate(g2, "topic", fp, Oracle(), out, bands=Bands(0.5, 0.1))
    rep = do_score(g2, "topic", fp, Oracle(), out / "calibrations" / "topic" / "oracle.json", out)
    assert rep["verdict"]["per_basis"]["primary"] in ("PASS", "NOT_EVALUABLE")
    assert rep["verdict"]["verdict"] == "INCONCLUSIVE"


def test_score_refuses_incomplete_gold_and_takes_no_lock(tmp_path, capsys):
    g, fp, out = _setup(tmp_path)
    m = Stub("topic", "sanctions")
    do_calibrate(g, "topic", fp, m, out, bands=Bands(0.7, 0.3))
    (g / "topic" / "labels-freeze.json").unlink()
    with pytest.raises(checker.GoldIncomplete):
        do_score(g, "topic", fp, m, out / "calibrations" / "topic" / "stub-1.json", out)
    assert not (out / "locks").exists()
    assert m.seen and all(i in GoldTrack(g, "topic").split_ids("development") for i in m.seen)


def test_score_refuses_calibration_from_other_features_or_model(tmp_path):
    g, fp, out = _setup(tmp_path)
    m = Stub("topic", "sanctions")
    do_calibrate(g, "topic", fp, m, out, bands=Bands(0.7, 0.3))
    c = out / "calibrations" / "topic" / "stub-1.json"
    other = Stub("topic", "sanctions", model_id="stub-2")
    with pytest.raises(GoldError):
        do_score(g, "topic", fp, other, c, out)
    assert not (out / "locks").exists()


def test_cli_run_refuses_on_partial_gold(tmp_path, capsys):
    g = make_gold(tmp_path / "g", label="partial", frozen=False)
    fp = tmp_path / "f.json"
    make_features_file(tmp_path, g, "topic", fp)
    code = run_main(["calibrate", "--gold-root", str(g), "--track", "topic", "--features", str(fp),
                     "--model", "test_harness:_stub_factory", "--out-dir", str(tmp_path / "o"),
                     "--high-min", "0.7", "--medium-min", "0.3"])
    assert code == 1
    assert "REFUSED" in capsys.readouterr().err


def test_cli_calibrate_refuses_without_boundaries(tmp_path):
    g = make_gold(tmp_path / "g")
    fp = tmp_path / "f.json"
    make_features_file(tmp_path, g, "topic", fp)
    with pytest.raises(SystemExit):
        run_main(["calibrate", "--gold-root", str(g), "--track", "topic", "--features", str(fp),
                  "--model", "test_harness:_stub_factory", "--out-dir", str(tmp_path / "o")])


def _stub_factory():
    return Stub("topic", "sanctions")


# ------------------------------------------------------------------ features
class FakeParser:
    def info(self): return {"fake": "1"}
    def parse(self, text, lang): return {"tokens": [[text[:3], "l", "X", "dep", 0]], "ents": []} if lang in ("en", "es", "it") else None


class FakeEmbedder:
    def info(self): return {"fake": "emb"}
    def encode(self, texts): return [[round((sum(map(ord, t)) % 97) / 97, 6), float(len(t))] for t in texts]


def _snap(tmp_path, g):
    gt = GoldTrack(g, "topic")
    rows = {}
    for i, c in gt.cases().items():
        rows[i] = [(it["item_id"], "BBC News", "2026-11-0%d" % (1 + j), f"Russia strikes Kyiv {i}", f"<p>Body &amp; text {j}</p>")
                   for j, it in enumerate(c["items"])]
    p = tmp_path / "snap.db"
    return p, make_snapshot(p, rows)


def test_feature_extraction_byte_identical_and_hash_verified(tmp_path):
    g = make_gold(tmp_path / "g")
    snap, sha = _snap(tmp_path, g)
    outs = []
    for k in range(2):
        with F.snapshot_copy(snap, sha) as db:
            body = F.build_features(g, "topic", db, FakeParser(), FakeEmbedder(), sha)
        p = tmp_path / f"f{k}.json"
        F.write_features(body, p)
        outs.append(p.read_bytes())
    assert outs[0] == outs[1]
    body = F.load_features(tmp_path / "f0.json")
    c = next(iter(body["cases"].values()))
    assert "event_type" not in json.dumps(c) and "stratum" not in json.dumps(c)
    assert c["items"][0]["lead"].startswith("<p>Body & text")
    p = tmp_path / "f0.json"
    p.write_text(p.read_text(encoding="utf-8").replace("Body & text 0", "Tampered", 1), encoding="utf-8")
    with pytest.raises(GoldError):
        F.load_features(p)


def test_snapshot_sha_mismatch_stops(tmp_path):
    g = make_gold(tmp_path / "g")
    snap, sha = _snap(tmp_path, g)
    with pytest.raises(F.SnapshotMismatch):
        with F.snapshot_copy(snap, "0" * 64):
            pass
    before = snap.read_bytes()
    with F.snapshot_copy(snap, sha) as db:
        db.execute("create table scratch(x)")        # writes go to the temp copy only
    assert snap.read_bytes() == before


def test_real_spacy_and_embedder_deterministic(tmp_path):
    """Real spaCy models + the cached multilingual model, twice, on a 2-language synthetic snapshot."""
    pytest.importorskip("spacy")
    try:
        emb, par = F.STEmbedder(), F.SpacyParser()
        par.info()
    except Exception as e:   # model not cached in this environment
        pytest.skip(str(e))
    g = make_gold(tmp_path / "g", n=4)
    gt = GoldTrack(g, "topic")
    rows = {}
    for k, (i, c) in enumerate(gt.cases().items()):
        txt = ["Israel strikes Gaza after talks in Cairo", "Ucrania ataca Crimea con drones", "Il governo italiano annuncia sanzioni"][k % 3]
        rows[i] = [(it["item_id"], ["BBC News", "El Pais", "ANSA Mondo"][k % 3], "2026-11-01", txt, txt + " Lead text here.")
                   for it in c["items"]]
    snap = tmp_path / "s.db"
    sha = make_snapshot(snap, rows)
    outs = []
    for k in range(2):
        with F.snapshot_copy(snap, sha) as db:
            body = F.build_features(g, "topic", db, par, emb, sha)
        p = tmp_path / f"r{k}.json"
        F.write_features(body, p)
        outs.append(p.read_bytes())
    assert outs[0] == outs[1]
    h = F.load_features(tmp_path / "r0.json")["header"]
    assert h["embedding"]["revision"] == F.EMBED_REVISION and h["embedding"]["files_sha256"]
    assert "en_core_web_lg" in h["spacy"] and "spacy" in h["spacy"]
