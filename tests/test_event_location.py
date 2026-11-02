"""Development location contract (evaluations/geolocation/LOCATION-CONTRACT.md, owner rulings U1-U4): the decision
over occurrence-report place mentions, without a database."""

import pytest

from osint_monitor.processors.event_location import (
    ACTOR_POSITION, NON_PLACE, Confidence, OccurrenceMention, Role, decide)
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
