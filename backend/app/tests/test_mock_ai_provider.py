from app.services.ai_generation.mock_provider import MockAIResponseProvider
from app.services.ai_generation.schemas import (
    RetrievedArticleForGeneration,
    TicketResponseGenerationInput,
)


def _input() -> TicketResponseGenerationInput:
    return TicketResponseGenerationInput(
        ticket_id=15,
        title="Nie działa VPN",
        description="Nie mogę zalogować się do sieci firmowej.",
        category_name="Sieć i VPN",
        priority_name="Wysoki",
        agent_name="Norbert",
        retrieved_articles=[
            RetrievedArticleForGeneration(
                article_id=1,
                title="Diagnostyka VPN",
                excerpt="Sprawdź połączenie internetowe.",
                score=0.88,
                category_id=2,
            )
        ],
    )


def test_mock_provider_generates_mail_format():
    provider = MockAIResponseProvider()

    result = provider.generate_ticket_response(_input())

    assert "Dzień dobry," in result.email_body
    assert "Pozdrawiam," in result.email_body
    assert result.provider_name == "mock"


def test_mock_provider_requires_human_review():
    provider = MockAIResponseProvider()

    result = provider.generate_ticket_response(_input())

    assert result.requires_human_review is True