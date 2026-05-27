import pytest

from app.models.ticket import Ticket, TicketStatus, TicketSource
from app.schemas.analysis import ClassificationResult, PriorityResult, SimilarArticle
from app.services.ai_generator import MockAIGenerator


def _make_ticket() -> Ticket:
    t = Ticket()
    t.id = 1
    t.title = "Nie działa VPN"
    t.description = "Klient VPN nie może się połączyć z siecią firmową."
    t.status = TicketStatus.in_analysis
    t.source = TicketSource.manual
    return t


def _classification() -> ClassificationResult:
    return ClassificationResult(
        category_id=2,
        category_name="Sieć i VPN",
        confidence=0.85,
        explanation="Zgłoszenie przypisano do kategorii Sieć i VPN, ponieważ treść zawiera słowo kluczowe: vpn.",
    )


def _priority() -> PriorityResult:
    return PriorityResult(
        priority_id=3,
        priority_name="Wysoki",
        confidence=0.85,
        explanation="Priorytet ustawiono jako Wysoki.",
    )


@pytest.fixture()
def generator() -> MockAIGenerator:
    return MockAIGenerator()


@pytest.fixture()
def ticket() -> Ticket:
    return _make_ticket()


@pytest.fixture()
def classification() -> ClassificationResult:
    return _classification()


@pytest.fixture()
def priority() -> PriorityResult:
    return _priority()


def test_generates_non_empty_response(generator, ticket, classification, priority):
    result = generator.generate(ticket, classification, priority, [])
    assert result.response_text
    assert len(result.response_text) > 50


def test_response_contains_category(generator, ticket, classification, priority):
    result = generator.generate(ticket, classification, priority, [])
    assert "Sieć i VPN" in result.response_text


def test_response_contains_priority(generator, ticket, classification, priority):
    result = generator.generate(ticket, classification, priority, [])
    assert "Wysoki" in result.response_text


def test_response_contains_it_support_disclaimer(generator, ticket, classification, priority):
    result = generator.generate(ticket, classification, priority, [])
    assert "IT Support" in result.response_text


def test_model_and_provider_names(generator, ticket, classification, priority):
    result = generator.generate(ticket, classification, priority, [])
    assert result.model_name == "mock-ai-generator"
    assert result.provider_name == "mock"


def test_sources_used_when_similar_articles(generator, ticket, classification, priority):
    articles = [
        SimilarArticle(id=1, title="Artykuł o VPN", excerpt="Opis...", category_id=2, score=0.75)
    ]
    result = generator.generate(ticket, classification, priority, articles)
    assert result.sources_used is not None
    assert "Artykuł o VPN" in result.sources_used


def test_sources_none_when_no_articles(generator, ticket, classification, priority):
    result = generator.generate(ticket, classification, priority, [])
    assert result.sources_used is None
