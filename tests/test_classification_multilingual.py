"""Spanish / Italian fallback of the rules classifier (evaluations/classification/unknown-20261111)."""
import pytest

from osint_monitor.core.models import ClusterContext, ContextItem, EventType
from osint_monitor.processors.classification import RuleBasedClassifier


def classify(*titles: str) -> EventType:
    ctx = ClusterContext(event_id=1, items=[ContextItem(title=t, excerpt="", source_name="") for t in titles])
    return RuleBasedClassifier().classify(ctx).event_type


@pytest.mark.parametrize("title,expected", [
    ("Ucrania ataca la región de Moscú con 650 drones y mata a dos personas", EventType.MILITARY_ACTION),
    ("Rusia derriba más de 1.200 drones de Ucrania", EventType.MILITARY_ACTION),
    ("El Salvador avvia la campagna per le presidenziali del 2027", EventType.ELECTION),
    ("Israel y Hamás acuerdan una tregua de tres días", EventType.CEASEFIRE),
    ("La Unión Europea aprueba nuevas sanciones contra Rusia por la guerra en Ucrania", EventType.SANCTIONS),
    ("Il premier incontra il presidente francese a Roma", EventType.BILATERAL_MEETING),
    ("Cómo es la revolucionaria misión que busca traer un trozo de luna", EventType.COMMENTARY),
])
def test_spanish_italian_types(title, expected):
    assert classify(title) == expected


@pytest.mark.parametrize("title", [
    "Los ejércitos de Estados Unidos e Israel desarrollan planes para atacar Irán",   # hypothetical
    "Muere a los 86 años Patrick Stewart, legendario actor de Star Trek",            # outside the taxonomy
    "Las graves inundaciones en el este de España dejan al menos cuatro muertos",    # hazard: no type
    "Police raid home of suspect in Leeds",                                         # English: es/it rules not used
])
def test_stays_unknown(title):
    assert classify(title) == EventType.UNKNOWN


def test_english_typed_development_never_changes():
    """The fallback runs only when no English rule matched anything in the Development."""
    assert classify("Russia strikes Kharkiv overnight", "Rusia y Ucrania firman un acuerdo") == EventType.MILITARY_ACTION
