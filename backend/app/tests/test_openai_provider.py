from types import SimpleNamespace

import pytest

from app.services.ai_generation.openai_provider import OpenAIResponseProvider
from app.services.ai_generation.schemas import (
    RetrievedArticleForGeneration,
    StructuredMailResponse,
    TicketResponseGenerationInput,
)


class FakeResponsesClient:
    def __init__(self, response=None, error: Exception | None = None) -> None:
        self._response = response
        self._error = error
        self.calls = []

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        if self._error:
            raise self._error
        return self._response


class FakeOpenAIClient:
    def __init__(self, response=None, error: Exception | None = None) -> None:
        self.responses = FakeResponsesClient(response=response, error=error)


def _input() -> TicketResponseGenerationInput:
    return TicketResponseGenerationInput(
        ticket_id=20,
        title="Nie działa VPN",
        description="Nie mogę połączyć się z siecią firmową.",
        category_name="Sieć i VPN",
        priority_name="Wysoki",
        agent_name="Norbert",
        retrieved_articles=[
            RetrievedArticleForGeneration(
                article_id=1,
                title="Diagnostyka VPN",
                excerpt="Sprawdź połączenie internetowe.",
                score=0.92,
                category_id=2,
            )
        ],
    )


def test_openai_provider_maps_structured_output():
    parsed = StructuredMailResponse(
        subject="Re: Problem z VPN",
        email_body="Dzień dobry,\n\nProszę sprawdzić VPN.\n\nPozdrawiam,\nNorbert",
        confidence=0.84,
        used_sources=[1],
        requires_human_review=True,
        limitations="Wymaga weryfikacji agenta.",
    )
    client = FakeOpenAIClient(
        response=SimpleNamespace(output_parsed=parsed, output_text='{"subject": "Re: Problem z VPN"}')
    )
    provider = OpenAIResponseProvider(
        api_key="test-key",
        model_name="gpt-4o-mini",
        temperature=0.2,
        max_output_tokens=1200,
        client=client,
    )

    result = provider.generate_ticket_response(_input())

    assert result.provider_name == "openai"
    assert result.model_name == "gpt-4o-mini"
    assert result.subject == "Re: Problem z VPN"
    assert result.used_sources == [1]


def test_openai_provider_handles_api_error():
    client = FakeOpenAIClient(error=RuntimeError("boom"))
    provider = OpenAIResponseProvider(
        api_key="test-key",
        model_name="gpt-4o-mini",
        temperature=0.2,
        max_output_tokens=1200,
        client=client,
    )

    with pytest.raises(RuntimeError, match="OpenAI response generation failed"):
        provider.generate_ticket_response(_input())


def test_openai_provider_does_not_require_real_key_when_client_is_mocked():
    parsed = StructuredMailResponse(
        subject="Re: Problem z VPN",
        email_body="Dzień dobry,\n\nTo jest szkic.\n\nPozdrawiam,\nNorbert",
        confidence=0.5,
        used_sources=[],
        requires_human_review=True,
        limitations="Brak pełnej wiedzy.",
    )
    client = FakeOpenAIClient(response=SimpleNamespace(output_parsed=parsed, output_text="{}"))

    provider = OpenAIResponseProvider(
        api_key="",
        model_name="gpt-4o-mini",
        temperature=0.2,
        max_output_tokens=1200,
        client=client,
    )

    result = provider.generate_ticket_response(_input())

    assert result.email_body.startswith("Dzień dobry,")