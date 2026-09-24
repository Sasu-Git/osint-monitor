"""DevelopmentClassifier interface and helpers shared by all implementations.

A classifier turns a ClusterContext into a DevelopmentClassification. It never
touches the database, ranks developments, judges source credibility or clusters
articles -- those are separate pipeline stages.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from osint_monitor.core.models import (
    ClusterContext,
    DevelopmentClassification,
    UncertaintyFlag,
)

PERSON_TYPES = {"PERSON"}
COUNTRY_TYPES = {"GPE"}
ORGANIZATION_TYPES = {"ORG", "NORP"}


@runtime_checkable
class DevelopmentClassifier(Protocol):
    """Anything with this method can classify developments."""

    name: str

    def classify(self, context: ClusterContext) -> DevelopmentClassification:
        ...


def context_flags(context: ClusterContext) -> list[UncertaintyFlag]:
    """Uncertainty flags that follow from the cluster itself, whatever the classifier says."""
    flags = []
    if not context.items:
        flags.append(UncertaintyFlag.INSUFFICIENT_CONTEXT)
    elif len(context.distinct_sources) <= 1:
        flags.append(UncertaintyFlag.SINGLE_SOURCE)
    if context.has_contradictions:
        flags.append(UncertaintyFlag.CONTRADICTORY_REPORTS)
    return flags


def entities_by_kind(context: ClusterContext) -> tuple[list[str], list[str], list[str]]:
    """Split NER entities into (actors, countries, organizations)."""
    actors, countries, orgs = [], [], []
    for e in context.entities:
        if e.entity_type in PERSON_TYPES:
            actors.append(e.name)
        elif e.entity_type in COUNTRY_TYPES:
            countries.append(e.name)
        elif e.entity_type in ORGANIZATION_TYPES:
            orgs.append(e.name)
    return actors, countries, orgs
