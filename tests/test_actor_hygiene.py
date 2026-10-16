"""Actor hygiene fixes for the frozen 2026-10-16 defects (evaluations/entities/defects/2026-10-16/):
D1 elon-musk-musk (headline/body glue, stale possessive canonical names, a bare surname typed as another entity,
two entities flagged principal for one person) and D2 rachel-simon (named storms typed PERSON and made actors)."""

import importlib.util

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, Entity
from osint_monitor.core.models import EntityType, ExtractedEntity
from osint_monitor.processors import nlp as NLP
from osint_monitor.processors.entity_resolver import EntityResolver


def _has(model):
    return importlib.util.find_spec(model) is not None


EN = pytest.mark.skipif(not _has("en_core_web_lg"), reason="English model not installed")
ES = pytest.mark.skipif(not _has("es_core_news_md"), reason="Spanish model not installed")


@pytest.fixture
def session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'r.db'}")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    yield s
    s.close()
    engine.dispose()


def add(session, name, etype, aliases=()):
    e = Entity(canonical_name=name, entity_type=etype, aliases=list(aliases))
    session.add(e)
    session.commit()
    return e


def mentions(text, lang="en"):
    return [(m.text, m.entity_type.value, m.refers_to) for m in NLP.extract_entities(text, lang)]


# --- D1: headline / body glue ----------------------------------------------------------------------

@pytest.mark.parametrize("title, content, expected", [
    ("after Elon Musk jab", "Musk has claimed", "after Elon Musk jab. Musk has claimed"),
    ("Is it over?", "Yes.", "Is it over? Yes."),
    ("Headline", None, "Headline"),
    (None, "Body only", "Body only"),
])
def test_ner_text_separates_headline_and_body(title, content, expected):
    assert NLP.ner_text(title, content) == expected


@EN
def test_headline_and_body_no_longer_glue_into_one_name():
    got = mentions(NLP.ner_text("India defends satellite internet approval process after Elon Musk jab",
                                "Musk has claimed unnamed entities are blocking Starlink's launch."))
    assert not any("jab" in t for t, _, _ in got)
    got = mentions(NLP.ner_text("US firm gets sub deal after boss joins war study with Musk", "Anduril said it would invest."))
    assert not any(t == "Musk Anduril" for t, _, _ in got)


# --- D1: stale canonical names are renamed only when safe, by an explicit script (dry run by default) --------

def _names_db(tmp_path, rows):
    import json
    import sqlite3
    db = tmp_path / "names.db"
    c = sqlite3.connect(db)
    c.execute("CREATE TABLE entities (id INTEGER PRIMARY KEY, canonical_name TEXT, entity_type TEXT, aliases TEXT)")
    c.executemany("INSERT INTO entities VALUES (?, ?, ?, ?)", [(i, n, t, json.dumps(a)) for i, n, t, a in rows])
    c.commit()
    c.close()
    return db


def test_stale_possessive_name_is_a_safe_rename_and_a_collision_is_only_reported(tmp_path):
    import sqlite3
    from scripts.repair_entity_names import plan
    db = _names_db(tmp_path, [(1, "Elon Musk's", "PERSON", ["Elon Musk’s"]), (2, "Tehran's", "GPE", []),
                              (3, "Tehran", "GPE", []), (4, "Donald Trump", "PERSON", [])])
    safe, collisions = plan(sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True))
    assert [(s["id"], s["to"]) for s in safe] == [(1, "Elon Musk")]
    assert "Elon Musk's" in safe[0]["aliases"]
    assert [(c["id"], c["would_merge_with"]) for c in collisions] == [(2, [3])]   # never a merge


def test_rename_script_dry_run_writes_nothing(tmp_path):
    import sqlite3
    from scripts.repair_entity_names import main
    db = _names_db(tmp_path, [(1, "Elon Musk's", "PERSON", [])])
    assert main(["--db", str(db)]) == 0
    assert sqlite3.connect(db).execute("SELECT canonical_name FROM entities").fetchone()[0] == "Elon Musk's"


# --- D1: a bare surname stands for the full name the same item gives -------------------------------

def _person(name, etype=EntityType.PERSON):
    return ExtractedEntity(text=name, entity_type=etype, canonical_name=name)


def test_surname_links_to_the_only_full_name_in_the_item():
    ents = [_person("Elon Musk"), _person("Musk", EntityType.PRODUCT)]
    NLP._link_surnames(ents)
    assert ents[1].refers_to == "Elon Musk" and ents[1].entity_type == EntityType.PERSON


def test_surname_stays_unlinked_when_two_people_share_it():
    ents = [_person("Flávio Bolsonaro"), _person("Jair Bolsonaro"), _person("Bolsonaro")]
    NLP._link_surnames(ents)
    assert ents[2].refers_to is None


def test_surname_without_a_full_name_in_the_item_is_not_linked():
    ents = [_person("Musk", EntityType.PRODUCT), _person("Donald Trump")]
    NLP._link_surnames(ents)
    assert ents[0].refers_to is None and ents[0].entity_type == EntityType.PRODUCT


def test_a_linked_surname_resolves_as_the_person_and_is_not_stored_as_an_alias(session):
    person = add(session, "Elon Musk", "PERSON")
    add(session, "Musk", "PRODUCT")
    r = EntityResolver(session)
    got = r.resolve(ExtractedEntity(text="Musk", entity_type=EntityType.PERSON, refers_to="Elon Musk"))
    assert got.id == person.id and r.last_method == "in-item"
    assert "Musk" not in (session.get(Entity, person.id).aliases or [])


# --- D2: named storms are storm events, not people ----------------------------------------------------

@EN
@pytest.mark.parametrize("text, name, storm", [
    ("Two deaths reported as Hurricane Simon, storm Rachel batter Mexico’s coast", "Rachel", "Storm Rachel"),
    ("Death toll rises as Hurricanes Simon, Rachel remnants unleash floods", "Rachel", "Hurricane Rachel"),
    ("Death toll rises to 6 as Hurricane Simon and Rachel remnants unleash floods in Mexico", "Rachel", "Hurricane Rachel"),
])
def test_english_storm_names_are_events(text, name, storm):
    got = mentions(text)
    assert (name, "EVENT", storm) in got
    assert not any(t == name and ty == "PERSON" for t, ty, _ in got)


@ES
@pytest.mark.parametrize("text, names", [
    ("Huracanes en México: Simón y Rachel dejan al menos dos muertos y 10 desaparecidos", {"Simón", "Rachel"}),
    ("Al menos siete muertos por el paso del ciclón 'Rachel' en Baja California, en México", {"Rachel"}),
])
def test_spanish_storm_names_are_events(text, names):
    got = mentions(text, "es")
    assert not any(ty == "PERSON" for _, ty, _ in got)
    assert {r.split(" ", 1)[1] for _, ty, r in got if ty == "EVENT" and r} >= names


@EN
@pytest.mark.parametrize("text, person", [
    ("Hurricane relief: Sheinbaum visits Acapulco", "Sheinbaum"),         # storm word, no storm name
    ("Hurricane Helene, Biden says aid is coming", "Biden"),             # a comma after a singular storm: no list
    ("Lula meets Xi in Beijing", "Lula"),                                 # one-word names outside storm context
])
def test_people_outside_a_storm_name_stay_people(text, person):
    assert (person, "PERSON", None) in mentions(text)


@EN
def test_a_storm_name_repeated_alone_in_the_item_is_still_the_storm():
    got = mentions("Hurricane Simon batters Mexico's Pacific coast. Officials said Simon weakened overnight.")
    assert not any(t == "Simon" and ty == "PERSON" for t, ty, _ in got)
    # another item without the storm context keeps its person (linked to the full name that item gives)
    assert ("Simon", "PERSON", "Paul Simon") in mentions("Paul Simon said Simon and Garfunkel will not reunite")


@EN
def test_storm_named_products_are_untouched():
    assert ("Storm Shadow", "PRODUCT", None) in mentions("UK sends Storm Shadow missiles to Ukraine")


@EN
def test_storm_names_are_not_actor_candidates():
    from osint_monitor.processors.principals import item_candidates
    nlp = NLP.get_language_nlp("en")
    cands = item_candidates(nlp, "Death toll rises as Hurricanes Simon, Rachel remnants unleash floods")
    assert all(not c.participant for c in cands if c.text in ("Rachel", "Hurricanes Simon", "Simon"))
