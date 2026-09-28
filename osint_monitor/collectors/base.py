"""Abstract base collector interface."""

import time
from abc import ABC, abstractmethod

from osint_monitor.core.models import RawItemModel


class BaseCollector(ABC):
    """Base class for all source collectors.

    ``time_budget_seconds`` bounds one ``collect()`` call. Collectors that loop over many
    targets call ``over_budget()`` between targets and return what they have when it
    is spent, so one slow endpoint cannot hold a tier past its next tick. The pipeline
    starts the clock and logs a collector that stopped early.
    """

    time_budget_seconds: float | None = None

    def __init__(self, name: str, source_type: str, url: str, **kwargs):
        self.name = name
        self.source_type = source_type
        self.url = url
        self.max_items = kwargs.get("max_items", 20)
        if kwargs.get("time_budget_seconds") is not None:
            self.time_budget_seconds = kwargs["time_budget_seconds"]
        self._started: float | None = None
        self.budget_exceeded = False

    @abstractmethod
    def collect(self) -> list[RawItemModel]:
        """Collect items from the source. Returns list of raw items."""
        ...

    def start_budget(self) -> None:
        self._started = time.monotonic()
        self.budget_exceeded = False

    def elapsed(self) -> float:
        started = getattr(self, "_started", None)      # subclasses may skip BaseCollector.__init__
        return time.monotonic() - started if started is not None else 0.0

    def over_budget(self) -> bool:
        """True once the time budget is spent (always False without a budget or a started clock)."""
        if self.time_budget_seconds is None or getattr(self, "_started", None) is None:
            return False
        if self.elapsed() >= self.time_budget_seconds:
            self.budget_exceeded = True
        return self.budget_exceeded

    def health_check(self) -> bool:
        """Check if the source is reachable."""
        try:
            items = self.collect()
            return len(items) > 0
        except Exception:
            return False

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name!r}>"
