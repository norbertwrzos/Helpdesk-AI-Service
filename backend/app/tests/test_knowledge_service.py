import pytest

from app.models.knowledge_article import KnowledgeArticle
from app.services.similarity_service import SimilarityService


def _make_articles() -> list[KnowledgeArticle]:
    return [
        KnowledgeArticle(
            id=1,
            title="Problemy z połączeniem VPN",
            content="Jeśli klient VPN nie może się połączyć, sprawdź połączenie internetowe i dane logowania.",
            category_id=2,
        ),
        KnowledgeArticle(
            id=2,
            title="Reset hasła użytkownika",
            content="Procedura resetu hasła w Active Directory: ADUC, zmiana hasła, wymuszenie zmiany.",
            category_id=1,
        ),
        KnowledgeArticle(
            id=3,
            title="Podejrzana wiadomość e-mail",
            content="Nie klikaj w linki phishingowe. Zgłoś incydent do działu bezpieczeństwa IT.",
            category_id=6,
        ),
    ]


@pytest.fixture()
def service() -> SimilarityService:
    return SimilarityService()


@pytest.fixture()
def articles() -> list[KnowledgeArticle]:
    return _make_articles()


def test_finds_vpn_article(service, articles):
    result = service.find_similar("Nie działa VPN", "Problem z połączeniem VPN", articles)
    assert len(result) > 0
    assert any("VPN" in r.title for r in result)


def test_same_category_bonus(service, articles):
    """Artykuł z tej samej kategorii powinien dostać bonus i być wyżej."""
    result = service.find_similar(
        "Problem z połączeniem VPN",
        "Klient VPN nie działa",
        articles,
        classification_category_id=2,
    )
    assert result[0].category_id == 2


def test_empty_articles_returns_empty(service):
    result = service.find_similar("Coś", "Opis", [])
    assert result == []


def test_no_match_returns_empty_or_low_score(service, articles):
    result = service.find_similar("Xyzyq brak", "Nic wspólnego", articles)
    # Albo pusta lista, albo wszystkie z score = 0
    assert all(r.score == 0 for r in result) or len(result) == 0


def test_excerpt_length(service, articles):
    result = service.find_similar("VPN połączenie", "VPN nie działa", articles)
    for r in result:
        assert len(r.excerpt) <= 210  # EXCERPT_LENGTH + trochę marginesu
