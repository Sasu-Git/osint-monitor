"""Development location contract (evaluations/geolocation/LOCATION-CONTRACT.md, owner rulings U1-U4): the decision
over occurrence-report place mentions, without a database."""

import pytest

from osint_monitor.processors.event_location import (
    ACTOR_POSITION, NON_PLACE, OUTSIDE_NAMED, Confidence, OccurrenceMention, Role, decide)
from osint_monitor.processors.geography import Gazetteer


@pytest.fixture(scope="module")
def geo():
    return Gazetteer.load()


def m(span, title, origin="Reuters", lead="", item=1):
    return OccurrenceMention(item_id=item, origin=origin, span=span, title=title, lead=lead)


def test_target_city_not_the_attacker(geo):
    t = "Russia strikes second major bridge in Kyiv, mayor says"
    loc = decide([m("Russia", t), m("Kyiv", t), m("Kyiv", t, origin="BBC World", item=2)], {"russia"}, geo)
    assert (loc.role, loc.place, loc.country, loc.confidence) == (Role.EVENT_PLACE, "kyiv", "ukraine",
                                                                  Confidence.CONFIRMED_PLACE)
    assert ("Russia", ACTOR_POSITION) in loc.rejected


def test_several_places_in_one_country_give_the_country_ring(geo):          # U2 (a)
    t = "Ukraine strikes factory in Russia's Tolyatti, airfield in Krasnodar Krai"
    loc = decide([m("Ukraine", t), m("Russia", t), m("Tolyatti", t), m("Krasnodar Krai", t)], {"ukraine"}, geo)
    assert loc.role == Role.EVENT_COUNTRY and loc.country == "russia" and loc.confidence == Confidence.COUNTRY_ONLY
    assert set(loc.places) >= {"Tolyatti"}


def test_disputed_territory_is_its_own_entity(geo):                         # U4 (a)
    t = "Israeli settlers attack Jalud village in occupied West Bank"
    loc = decide([m("West Bank", t)], {"israel"}, geo)
    assert loc.country == "west bank" and loc.role in (Role.EVENT_PLACE, Role.EVENT_COUNTRY)


def test_regions_are_labels_not_points(geo):                                # U3 (a)
    t = "NATO to send additional patrol planes to Black Sea"
    loc = decide([m("Black Sea", t)], {"nato"}, geo)
    assert loc.role == Role.NONE and loc.confidence == Confidence.REGION and loc.region == "black sea"


def test_statement_without_a_stated_place_has_no_location(geo):             # U1 (a)
    t = "Putin says blaming Russia for unrest is a sign of weakness"
    loc = decide([m("Russia", t)], {"russia", "vladimir putin"}, geo)
    assert loc.role == Role.NONE


def test_statement_with_a_stated_place_is_located_there(geo):               # U1 (a)
    t = "Zelensky speaks at summit in Brussels"
    loc = decide([m("Brussels", t)], {"ukraine"}, geo)
    assert loc.role == Role.EVENT_PLACE and loc.country == "belgium"


def test_non_places_are_rejected(geo):
    t = "Real Madrid demand resignation of La Liga chief"
    loc = decide([m("La Liga", t)], set(), geo)
    assert loc.role == Role.NONE and ("La Liga", NON_PLACE) in loc.rejected


def test_country_wide_occurrence(geo):                                      # L4
    t = "Brazil votes in tight presidential runoff"
    loc = decide([m("Brazil", t)], {"lula", "bolsonaro"}, geo)
    assert loc.role == Role.EVENT_COUNTRY and loc.country == "brazil"


def test_places_in_different_countries_without_a_dominant_one(geo):        # L5
    t = "Protests in Paris and Berlin over pension plans"
    loc = decide([m("Paris", t), m("Berlin", t)], set(), geo)
    assert loc.role == Role.NONE and set(loc.places) == {"paris", "berlin"}


def test_mentions_outside_headline_and_lead_do_not_count(geo):
    loc = decide([m("Kyiv", "Talks resume", lead="Officials met in Geneva on Monday.")], set(), geo)
    assert loc.role == Role.NONE


# --- iteration 2: gazetteer extension, non-place filter, L1 revision ---------------------------------------------

EXT = {"fooville": {"ukraine": [50000, 49.0, 30.0]},
       "twinton": {"france": [90000, 45.0, 2.0], "canada": [60000, 45.0, -75.0]},
       "bigburg": {"germany": [800000, 50.0, 8.0], "brazil": [20000, -20.0, -45.0]}}


def test_extension_place_resolves_inside_named_country(geo):
    t = "Drone hits refinery near Fooville, Ukraine"
    loc = decide([m("Fooville", t), m("Ukraine", t)], set(), geo, extension=EXT)
    assert (loc.role, loc.place, loc.country) == (Role.EVENT_PLACE, "Fooville", "ukraine")


def test_extension_place_outside_named_countries_is_rejected(geo):         # L2
    t = "Floods in Twinton as Germany sends aid"
    loc = decide([m("Twinton", t), m("Germany", t)], set(), geo, extension=EXT)
    assert ("Twinton", OUTSIDE_NAMED) in loc.rejected and loc.country == "germany"


def test_extension_ambiguity_without_named_country(geo):
    assert decide([m("Bigburg", "Blast at Bigburg plant")], set(), geo, extension=EXT).country == "germany"
    loc = decide([m("Twinton", "Blast at Twinton plant")], set(), geo, extension=EXT)
    assert loc.place == "Twinton" and loc.country is None          # 90k vs 60k: not dominant, unresolved


def test_gazetteer_wins_over_extension(geo):
    loc = decide([m("Kyiv", "Strike in Kyiv")], set(), geo, extension={"kyiv": {"russia": [1, 0.0, 0.0]}})
    assert loc.country == "ukraine"


def test_locative_non_places_are_filtered(geo):
    for span, t in (("La Liga", "Record crowd in La Liga"), ("Man City", "Late winner at Man City"),
                    ("Labour Party", "Revolt in Labour Party")):
        loc = decide([m(span, t)], set(), geo, extension={})
        assert loc.role == Role.NONE and (span, NON_PLACE) in loc.rejected, span


def test_country_wide_occurrence_in_actor_country(geo):                     # L1 revision
    t = "Brazil heads to the polls in tight presidential runoff"
    loc = decide([m("Brazil", t)], {"brazil"}, geo, extension={})
    assert (loc.role, loc.country, loc.confidence) == (Role.EVENT_COUNTRY, "brazil", Confidence.COUNTRY_ONLY)


def test_actor_country_without_country_wide_occurrence_stays_excluded(geo):
    loc = decide([m("Russia", "Russia launches drones overnight")], {"russia"}, geo, extension={})
    assert loc.role == Role.NONE


def test_point_location_beats_country_wide_actor(geo):
    t = "Ukraine votes on martial law as strikes hit Kharkiv"
    loc = decide([m("Ukraine", t), m("Kharkiv", t)], {"ukraine"}, geo, extension={})
    assert loc.place == "kharkiv"


# Iteration 3 rules (evaluations/geolocation/iter3-design/DESIGN.md): each is off by default and switchable.

def test_iter3_rules_are_off_by_default(geo):
    t = "Brazil delegation lands in Japan for talks"
    ms = [m("Brazil", t), m("Japan", t)]
    assert decide(ms, set(), geo) == decide(ms, set(), geo, rules=())


def test_unknown_rule_is_refused(geo):
    with pytest.raises(AssertionError):
        decide([], set(), geo, rules={"1a"})


def test_2a_tied_places_in_one_country_collapse_to_it(geo):
    t = "Drones hit Kharkiv and Odesa; debris reported in Belgorod"
    ms = [m("Kharkiv", t), m("Kharkiv", t, origin="BBC World", item=2), m("Odesa", t),
          m("Odesa", t, origin="BBC World", item=2), m("Belgorod", t)]
    assert decide(ms, set(), geo).role == Role.NONE
    loc = decide(ms, set(), geo, rules={"2a"})
    assert (loc.role, loc.country, loc.confidence) == (Role.EVENT_COUNTRY, "ukraine", Confidence.COUNTRY_ONLY)


def test_3a_bare_country_is_not_the_place(geo):
    t = "Brazil delegation lands in Japan for talks"
    ms = [m("Brazil", t), m("Japan", t)]
    assert decide(ms, set(), geo).role == Role.NONE                      # iteration 2: two countries tie (L5)
    loc = decide(ms, set(), geo, rules={"3a"})
    assert (loc.role, loc.country) == (Role.EVENT_COUNTRY, "japan")
    assert ("Brazil", "COUNTRY_NOT_LOCATIVE") in loc.rejected


def test_3a_admits_a_country_wide_occurrence(geo):
    t = "Brazil floods kill 20"
    loc = decide([m("Brazil", t)], set(), geo, rules={"3a"})
    assert (loc.role, loc.country) == (Role.EVENT_COUNTRY, "brazil")


def test_4a_congo_cues(geo):
    t = "Clashes erupt in Congo"
    cod = decide([m("Congo", t, lead="M23 rebels advanced overnight.")], set(), geo, rules={"4a"})
    cog = decide([m("Congo", t, lead="Shops closed in Brazzaville.")], set(), geo, rules={"4a"})
    none = decide([m("Congo", t)], set(), geo, rules={"4a"})
    assert decide([m("Congo", t, lead="M23 rebels advanced overnight.")], set(), geo).country == "congo"
    assert cod.country == "democratic republic of the congo" and cog.country == "congo"
    assert none.role == Role.NONE and ("Congo", "AMBIGUOUS_CONGO") in none.rejected


def test_5a_hong_kong_is_its_own_entity(geo):
    t = "Police clear protest camp in Kowloon"
    assert decide([m("Kowloon", t)], set(), geo).country == "china"
    assert decide([m("Kowloon", t)], set(), geo, rules={"5a"}).country == "hong kong"
    t = "Thousands march in Hong Kong"
    loc = decide([m("Hong Kong", t)], set(), geo, rules={"5a"})
    assert (loc.role, loc.country) == (Role.EVENT_COUNTRY, "hong kong")
