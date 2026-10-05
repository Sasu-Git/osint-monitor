"""Phase 3 relation review UI (osint_monitor/api/relation_review.py): an annotation tool over
evaluations/relations/review. Cases load intact, verdicts persist per case and validate direction, drafts stay
blind until a verdict exists, the sealed holdout is never read, and no runtime table or configuration is touched."""

import hashlib
import importlib.util
import re
import shutil
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from osint_monitor.api import relation_review as RR

REAL_REVIEW = RR.REVIEW_DIR
REAL_VERDICTS = (REAL_REVIEW / "owner-verdicts.yaml").read_bytes()


@pytest.fixture
def review_dir(tmp_path):
    d = tmp_path / "review"
    d.mkdir()
    for name in ("cases.json", "draft-labels.json", "owner-verdicts.yaml", "relation-review-sheet.md"):
        shutil.copyfile(REAL_REVIEW / name, d / name)
    return d


@pytest.fixture
def store(review_dir, monkeypatch):
    s = RR.ReviewStore(review_dir)
    monkeypatch.setattr(RR, "_store", s)
    return s


@pytest.fixture
def client(store):
    return TestClient(RR.standalone_app)


def _entries(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# --- loading ---------------------------------------------------------------------------------------------------------

def test_all_142_cases_load_with_unique_ids_matching_the_sheet(store):
    assert len(store.cases) == 142 == len(set(store.order))
    sheet = (store.dir / "relation-review-sheet.md").read_text(encoding="utf-8")
    assert set(re.findall(r"^## (R\d{3})$", sheet, flags=re.M)) == set(store.cases)
    assert set(store._drafts) == set(store.cases)


def test_every_case_page_renders(client, store):
    for cid in store.order:
        r = client.get(f"/eval/relations/case/{cid}")
        assert r.status_code == 200, cid
        assert cid in r.text


# --- persistence -----------------------------------------------------------------------------------------------------

def test_saving_a_verdict_modifies_only_that_case(store):
    before = _entries(store.verdicts_path)
    store.save("R010", "same_calamity_lifecycle", None, None)
    after = _entries(store.verdicts_path)
    assert after["R010"]["label"] == "same_calamity_lifecycle"
    assert {k: v for k, v in after.items() if k != "R010"} == {k: v for k, v in before.items() if k != "R010"}


def test_notes_round_trip_exactly(store):
    note = '  "quoted": colon, apostrophe\'s, ünïcödé — 中文\nsecond line # not a comment\n\ttab  '
    store.save("R001", "AMBIGUOUS", None, note)
    assert RR.ReviewStore(store.dir).verdict("R001")["note"] == note


def test_existing_verdicts_survive_reload_and_other_saves(store):
    store.save("R002", "reaction_to", "B->A", "first")
    store.save("R003", "NO_RELATION", None, None)
    fresh = RR.ReviewStore(store.dir)
    assert fresh.verdict("R002")["direction"] == "B->A" and fresh.verdict("R002")["note"] == "first"
    assert fresh.verdict("R003")["label"] == "NO_RELATION"


def test_regenerating_the_sheet_never_overwrites_owner_verdicts(store, monkeypatch):
    store.save("R004", "same_visit_or_summit", None, "keep me")
    before = store.verdicts_path.read_bytes()
    spec = importlib.util.spec_from_file_location(
        "build_review_sheet", RR.RELATIONS_DIR / "scripts" / "build_review_sheet.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "REVIEW", store.dir)
    mod.main()
    assert store.verdicts_path.read_bytes() == before


# --- validation ------------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("label", RR.DIRECTED)
def test_directed_relations_require_a_valid_direction(store, label):
    for bad in (None, "", "A-B", "both", "none"):
        with pytest.raises(ValueError):
            store.save("R005", label, bad, None)
    for good in RR.DIRECTIONS:
        assert store.save("R005", label, good, None)["direction"] == good


@pytest.mark.parametrize("label", [v for v in RR.VERDICTS if v not in RR.DIRECTED])
def test_symmetric_and_review_labels_reject_a_direction(store, label):
    with pytest.raises(ValueError):
        store.save("R006", label, "A->B", None)
    assert store.save("R006", label, None, None)["direction"] is None


def test_unknown_verdicts_are_rejected_and_nothing_is_written(store, client):
    before = store.verdicts_path.read_bytes()
    with pytest.raises(ValueError):
        store.save("R007", "official_package", None, None)
    r = client.post("/eval/relations/case/R007", data={"label": "caused_by", "direction": ""})
    assert r.status_code == 422 and "needs a direction" in r.text
    assert store.verdicts_path.read_bytes() == before


def test_identity_suspect_sets_the_identity_flag(store):
    v = store.save("R008", RR.IDENTITY, None, None)
    assert v["identity_flag"] == RR.IDENTITY


# --- blind review ----------------------------------------------------------------------------------------------------

def test_draft_is_hidden_until_the_owner_has_decided(client, store):
    draft = store._drafts["R009"]
    page = client.get("/eval/relations/case/R009").text
    assert draft["rationale"] not in page
    assert client.get("/eval/relations/case/R009/draft").status_code == 403
    client.post("/eval/relations/case/R009", data={"label": "NO_RELATION"}, headers={"HX-Request": "true"})
    stored = store.verdict("R009")
    r = client.get("/eval/relations/case/R009/draft")
    assert r.status_code == 200 and draft["label"] in r.text
    assert store.verdict("R009") == stored                   # revealing changes nothing


def test_r045_is_reviewable_and_not_pre_labelled(client, store):
    assert store.verdict("R045") is None
    r = client.get("/eval/relations/case/R045")
    assert r.status_code == 200 and "not reviewed yet" in r.text


def test_filters_and_summary(client, store):
    store.save("R011", "AMBIGUOUS", None, None)
    store.save("R012", RR.IDENTITY, None, None)
    store.save("R013", "reaction_to", "B->A", None)
    assert store.filtered("ambiguous") == ["R011"]
    assert store.filtered("identity") == ["R012"]
    assert store.filtered("all", "reaction_to") == ["R013"]
    assert "R011" not in store.filtered("unreviewed") and len(store.filtered("reviewed")) == 3
    s = store.summary()
    assert (s["reviewed"], s["identity"], s["ambiguous"], s["positives"]["reaction_to"]) == (3, 1, 1, 1)
    assert set(store.filtered("disagree")) == set(s["disagreements"])
    assert client.get("/eval/relations/summary").status_code == 200


def test_the_ui_is_localhost_only(store):
    remote = TestClient(RR.standalone_app, client=("10.1.2.3", 5000))
    assert remote.get("/eval/relations/case/R001").status_code == 403


# --- isolation -------------------------------------------------------------------------------------------------------

def test_the_sealed_holdout_is_never_loaded_or_exposed(client, store, monkeypatch):
    with pytest.raises(ValueError):
        RR.ReviewStore(RR.HOLDOUT_DIR)
    opened = []
    real_read_text, real_read_bytes = Path.read_text, Path.read_bytes
    monkeypatch.setattr(Path, "read_text", lambda self, *a, **k: opened.append(self) or real_read_text(self, *a, **k))
    monkeypatch.setattr(Path, "read_bytes", lambda self, *a, **k: opened.append(self) or real_read_bytes(self, *a, **k))
    RR.ReviewStore(store.dir)
    pages = [client.get(u).text for u in ("/eval/relations/summary", "/eval/relations/case/R001",
                                          "/eval/relations?filter=all")]
    holdout = RR.HOLDOUT_DIR.resolve()
    assert not [p for p in opened if holdout in (p.resolve(), *p.resolve().parents)]
    assert not any(re.search(r"\bRH\d{3}\b", t) for t in pages)


def test_no_runtime_table_or_configuration_is_touched(client, store, monkeypatch):
    import osint_monitor.core.database as db
    for name in ("init_db", "get_session", "get_engine"):
        if hasattr(db, name):
            monkeypatch.setattr(db, name, lambda *a, **k: pytest.fail("the review UI opened the runtime database"))
    root = RR.REPO
    watched = sorted((root / "config").glob("*.yaml")) + [p for p in (root / "data" / "osint.db",) if p.exists()]
    digest = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in watched}
    client.get("/eval/relations/case/R014")
    client.post("/eval/relations/case/R014", data={"label": "NO_RELATION", "note": "x"})
    client.get("/eval/relations/summary")
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in watched} == digest
    assert (REAL_REVIEW / "owner-verdicts.yaml").read_bytes() == REAL_VERDICTS   # tests write only to copies
