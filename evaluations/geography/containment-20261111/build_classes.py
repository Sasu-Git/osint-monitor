"""Write classes.yaml: the frozen classification of zero-country places (DIAGNOSIS.md), with proposed targets.

Classes: a = real sub-national place in 2+ Developments, missing a parent (fix: places entry);
a_left = real place deliberately left unmapped (ambiguous name, contested status, or its country is absent from the
gazetteer's country list); b = a country spelling (any frequency) missing an alias (fix: aliases entry);
c = sea, region or multi-country area (correctly no single country; left); d = junk, organisation, person or generic
word (left; for event-location upstream work). Places in 1 Development that are not country spellings are not
classified (out of this fix's scope).

    python build_classes.py INVENTORY.json OUT.yaml
"""
import json
import sys

import yaml

A = {  # place -> parent (a known gazetteer place or country)
    "fort hood": "texas", "oleshky": "ukraine", "oleshki": "ukraine", "leipzig": "germany", "kharkiv oblast": "ukraine",
    "strasbourg": "france", "kramatorsk": "ukraine", "lille": "france", "limoge": "france", "tirana": "albania",
    "montevideo": "uruguay", "nantes": "france", "rostov oblast": "russia", "san diego": "california",
    "chernihiv": "ukraine", "dnipropetrovsk oblast": "ukraine", "dnipropetrovsk": "ukraine", "el fasher": "darfur",
    "fort carson": "colorado", "guayaquil": "ecuador", "huntsville": "alabama", "kaliningrad": "russia",
    "kordofan": "sudan", "west kordofan": "sudan", "krasnodar krai": "russia", "minneapolis": "minnesota",
    "mokha": "yemen", "najran": "saudi arabia", "oporto": "portugal", "orsay": "france", "san salvador": "el salvador",
    "sarajevo": "bosnia and herzegovina", "toulouse": "france", "turin": "italy", "vilnius": "lithuania",
    "west palm beach": "florida", "palm beach": "florida", "yuma proving ground": "arizona", "yuma county": "arizona",
    "kalimantan": "indonesia", "mar-a-lago": "florida", "abha": "saudi arabia", "aden international airport": "aden",
    "bronx": "new york city", "bryansk oblast": "russia", "castilla-la mancha": "spain", "charleston": "united states",
    "corpus christi": "texas", "cusco": "peru", "chiclayo": "peru", "dandong": "china", "darnitsky": "kyiv",
    "donbas": "ukraine", "donetsk oblast": "ukraine", "fort bragg": "north carolina", "futenma": "okinawa",
    "gloucestershire": "england", "irkutsk": "russia", "izium": "ukraine", "johor": "malaysia", "karak": "jordan",
    "king khalid international airport": "riyadh", "kupiansk": "ukraine", "leipzig/halle airport": "germany",
    "lutsk": "ukraine", "mazatlan": "mexico", "sinaloa": "mexico", "mekelle": "tigray", "nagaland": "india",
    "nagqu": "tibet", "naha": "okinawa", "nottingham": "england", "palermo": "sicily", "paysandu": "uruguay",
    "pavlohrad": "ukraine", "pryluky": "ukraine", "rivne": "ukraine", "sakhalin": "russia", "samarkand": "uzbekistan",
    "sloviansk": "ukraine", "tampa": "florida", "voronezh": "russia", "wangaratta": "australia", "yerevan": "armenia",
    "yvelines": "france", "la verriere": "france",
}
A_SPELLINGS = {  # foreign-language spellings of known sub-national places (aliases; same 2+ rule)
    "marsiglia": "marseille", "lione": "lyon", "estambul": "istanbul", "riad": "riyadh", "nueva york": "new york",
    "d.c": "washington dc", "dc": "washington dc", "belgrado": "belgrade", "berlino": "berlin", "lisboa": "lisbon",
    "misisipi": "mississippi", "pensilvania": "pennsylvania", "jerson": "kherson", "seul": "seoul", "atenas": "athens",
    "abu dabi": "abu dhabi", "kaliningrado": "kaliningrad", "la habana": "havana", "la meca": "mecca", "ny": "new york",
    "puerto principe": "port-au-prince", "san petersburgo": "saint petersburg", "santiago de chile": "santiago",
    "varsavia": "warsaw", "varsovia": "warsaw", "cataluna": "catalonia",
}
B = {  # country spellings -> country
    "u.k": "united kingdom", "gb": "united kingdom", "el reino unido": "united kingdom",
    "united kingdom of great britain": "united kingdom", "ee uu": "united states",
    "emiratos arabes unidos": "united arab emirates", "emiratos": "united arab emirates",
    "emirati": "united arab emirates", "belgica": "belgium", "belgio": "belgium", "bosnia": "bosnia and herzegovina",
    "bosnia y herzegovina": "bosnia and herzegovina", "bosnia-herzegovina": "bosnia and herzegovina",
    "finlandia": "finland", "rumania": "romania", "noruega": "norway", "norvegia": "norway", "jordania": "jordan",
    "giordania": "jordan", "marruecos": "morocco", "marocco": "morocco", "cile": "chile", "palestina": "palestine",
    "occupied palestinian territory": "palestine", "territorios palestinos ocupados": "palestine",
    "ruanda": "rwanda", "republic of rwanda": "rwanda", "viet nam": "vietnam", "socialist republic of viet nam": "vietnam",
    "lituania": "lithuania", "irlanda": "ireland", "etiopia": "ethiopia", "suecia": "sweden", "svezia": "sweden",
    "luxemburgo": "luxembourg", "republic of moldova": "moldova", "moldavia": "moldova", "s korea": "south korea",
    "democratic republic of congo": "democratic republic of the congo", "argelia": "algeria", "bahrein": "bahrain",
    "barein": "bahrain", "bielorrusia": "belarus", "bielorussia": "belarus", "danimarca": "denmark",
    "dinamarca": "denmark", "filipinas": "philippines", "gibuti": "djibouti", "kenia": "kenya", "lettonia": "latvia",
    "libia": "libya", "malasia": "malaysia", "nuova zelanda": "new zealand", "olanda": "netherlands",
    "sudafrica": "south africa", "ungheria": "hungary", "singapur": "singapore", "groenlandia": "greenland",
    "costa d'avorio": "cote d'ivoire", "kyrgyz republic": "kyrgyzstan", "hellenic republic": "greece",
    "italian republic": "italy", "federative republic of brazil": "brazil", "republic of iceland": "iceland",
    "republic of zambia": "zambia", "republica dominicana": "dominican republic", "saudi-arabia": "saudi arabia",
}
A_LEFT = {
    "valencia": "ambiguous (Spain / Venezuela)", "cordoba": "ambiguous (Spain / Argentina)",
    "toledo": "ambiguous (Spain / United States)", "saint-denis": "ambiguous (France / Reunion)",
    "jackson": "ambiguous (several US places, a surname)", "bend": "ambiguous", "trinidad": "ambiguous (country / Cuba)",
    "parana": "ambiguous (Brazil / Argentina)", "copacabana": "ambiguous (Brazil / Bolivia)", "saba": "ambiguous",
    "taybeh": "ambiguous (West Bank / Israel)", "epirus": "ambiguous (Greece / Albania)", "sana": "ambiguous token",
    "addis": "truncated name", "marble hill": "ambiguous", "carson": "ambiguous", "rio": "ambiguous", "st": "fragment",
    "king khalid": "ambiguous (person / airport)", "san pedro": "ambiguous", "antigua": "ambiguous",
    "barbuda": "country absent from the country list", "grenada": "country absent from the country list (or Granada)",
    "palau": "country absent from the country list", "jerusalem": "contested status (owner decision)",
    "jerusalen": "contested status (owner decision)", "east jerusalem": "contested status (owner decision)",
    "dongsha island": "contested (China / Taiwan)", "falklands": "contested (United Kingdom / Argentina)",
    "falkland islands": "contested (United Kingdom / Argentina)", "western sahara": "contested",
    "la santa sede": "the Holy See is absent from the country list", "vaticano": "absent from the country list",
    "ciudad del vaticano": "absent from the country list", "gemelli": "ambiguous", "hospital gemelli": "landmark",
    "place de la republique": "landmark", "parc des princes": "landmark", "korea": "ambiguous (North / South)",
}
C = """europe middle east|africa|hormuz|europa|strait of hormuz|asia|mideast|latin america|black sea|gulf|america latina|
arctic|pacific|atlantic|south china sea|pacifico|southeast asia|mediterranean|ormuz|red sea|caribbean|sudamerica|
asia-pacific|balkans|caribe|central asia|north atlantic|north sea|western hemisphere|atlantico|azov|horn of africa|
persian gulf|golfo|golfo persico|persico|oriente medio|taiwan strait|east china sea|east sea|sea of japan|baltic sea|
mar nero|stretto di hormuz|east africa|east asia|central europe|arabian peninsula|korean peninsula|himalayas|iguazu|
dnipro river|blue nile|pacific coast|pacific ocean|sahara|kurdistan|soviet union|earth|middle east monitor"""
C = {x.strip() for x in C.replace("\n", "").replace("europe middle east", "europe|middle east").split("|") if x.strip()}


def main(inv: str, out: str) -> int:
    places = json.load(open(inv, encoding="utf-8"))["places"]
    cls, targets = {}, {}
    for p, v in places.items():
        n = v["developments"]
        if p in B:
            cls[p], targets[p] = "b", {"alias": B[p]}
        elif n < 2:
            continue
        elif p in A:
            cls[p], targets[p] = "a", {"parent": A[p]}
        elif p in A_SPELLINGS:
            cls[p], targets[p] = "a", {"alias": A_SPELLINGS[p]}
        elif p in A_LEFT:
            cls[p], targets[p] = "a_left", {"why": A_LEFT[p]}
        elif p in C:
            cls[p] = "c"
        else:
            cls[p] = "d"
    missing = sorted((set(A) | set(A_SPELLINGS) | set(B) | set(A_LEFT) | C) - set(places))
    yaml.safe_dump({"classes": dict(sorted(cls.items())), "targets": dict(sorted(targets.items())),
                    "listed_but_not_in_inventory": missing},
                   open(out, "w", encoding="utf-8", newline="\n"), allow_unicode=True, sort_keys=False, width=120)
    from collections import Counter
    print(Counter(cls.values()), "| listed but not in inventory:", missing)
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
