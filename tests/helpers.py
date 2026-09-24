"""Small builders shared by tests."""

from osint_monitor.analysis.llm import LLMProvider
from osint_monitor.core.models import ClusterContext, ContextEntity, ContextItem


def make_context(*titles: str, sources: list[str] | None = None, excerpts: list[str] | None = None,
                 entities: dict[str, str] | None = None, **kwargs) -> ClusterContext:
    """One item per title. Sources default to distinct outlets (so no single_source flag
    unless there is only one title). ``entities`` maps name -> entity type."""
    sources = sources or [f"Outlet {n}" for n in range(len(titles))]
    excerpts = excerpts or [""] * len(titles)
    return ClusterContext(
        items=[ContextItem(title=t, source_name=s, excerpt=e) for t, s, e in zip(titles, sources, excerpts)],
        entities=[ContextEntity(name=n, entity_type=t) for n, t in (entities or {}).items()],
        **kwargs,
    )


class FakeProvider(LLMProvider):
    """Scripted LLM replies; an Exception in the script is raised instead of returned."""
    model = "fake-1"

    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls: list[dict] = []

    def generate(self, prompt, system="", temperature=0.3):
        self.calls.append({"prompt": prompt, "system": system, "temperature": temperature})
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply
