"""Setup problems surface as actionable messages, not tracebacks or silent downloads."""

import pytest
import yaml
from pydantic import ValidationError

from osint_monitor import cli
from osint_monitor.analysis.llm import LLMConfigurationError, OpenAIProvider, get_llm
from osint_monitor.core.config import SituationsConfig
from osint_monitor.core.migrations import MigrationError
from osint_monitor.processors import nlp


@pytest.fixture()
def no_models(monkeypatch):
    def missing(name, *a, **kw):
        raise OSError(f"[E050] Can't find model '{name}'")

    monkeypatch.setattr(nlp, "_nlp_instance", None)
    monkeypatch.setattr(nlp.spacy, "load", missing)
    monkeypatch.setattr(nlp.spacy.cli, "download", lambda *a, **kw: pytest.fail("must not download models"))


def test_missing_spacy_model_gives_install_command(no_models):
    with pytest.raises(nlp.SpacyModelMissing) as exc:
        nlp.get_nlp()
    assert "python -m spacy download en_core_web_lg" in str(exc.value)
    assert "python -m spacy download" in cli._setup_error_message(exc.value)


def test_missing_openai_key_is_a_configuration_error(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OSINT_OPENAI_API_KEY", raising=False)
    monkeypatch.setattr("osint_monitor.analysis.llm.get_settings",
                        lambda: type("S", (), {"openai_api_key": None, "openai_model": "m"})())
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **kw: False)
    with pytest.raises(LLMConfigurationError, match="OPENAI_API_KEY"):
        OpenAIProvider()
    with pytest.raises(LLMConfigurationError):
        get_llm("no-such-provider")


def test_cli_maps_setup_errors_to_messages():
    assert "Database migration failed" in cli._setup_error_message(MigrationError("m2 failed"))
    assert ".env" in cli._setup_error_message(LLMConfigurationError("OpenAI API key not found"))
    assert "Invalid configuration" in cli._setup_error_message(yaml.YAMLError("bad indent"))
    with pytest.raises(ValidationError) as exc:
        SituationsConfig(situations=[{"slug": "Bad Slug", "title": "x", "primary_actors": ["A"]}])
    assert "Invalid configuration" in cli._setup_error_message(exc.value)
    assert "pip install -e" in cli._setup_error_message(ModuleNotFoundError("No module", name="feedparser"))
    assert cli._setup_error_message(KeyError("bug")) is None      # real bugs keep their traceback
