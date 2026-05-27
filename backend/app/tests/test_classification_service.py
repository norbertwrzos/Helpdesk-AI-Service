import pytest

from app.models.category import Category
from app.services.classification_service import ClassificationService


def _make_categories() -> list[Category]:
    names = [
        "Konto i dostęp",
        "Sieć i VPN",
        "Aplikacje biznesowe",
        "Sprzęt komputerowy",
        "Poczta e-mail",
        "Bezpieczeństwo",
        "System operacyjny",
        "Inne",
    ]
    cats = []
    for i, name in enumerate(names, start=1):
        c = Category(id=i, name=name)
        cats.append(c)
    return cats


@pytest.fixture()
def service() -> ClassificationService:
    return ClassificationService()


@pytest.fixture()
def categories() -> list[Category]:
    return _make_categories()


def test_classify_vpn(service, categories):
    result = service.classify("Nie działa VPN", "Nie mogę się połączyć z VPN", categories)
    assert result.category_name == "Sieć i VPN"
    assert result.category_id is not None
    assert result.confidence >= 0.65


def test_classify_login(service, categories):
    result = service.classify("Nie mogę się zalogować", "Problem z logowaniem do konta domenowego", categories)
    assert result.category_name == "Konto i dostęp"
    assert result.confidence >= 0.65


def test_classify_security(service, categories):
    result = service.classify("Podejrzany link w wiadomości", "Otrzymałem podejrzaną wiadomość z phishingiem", categories)
    assert result.category_name == "Bezpieczeństwo"
    assert result.confidence >= 0.65


def test_classify_default_when_no_match(service, categories):
    result = service.classify("Ogólny problem", "Coś nie działa, nie wiem co", categories)
    assert result.category_name == "Inne"
    assert result.confidence == 0.40


def test_classify_returns_none_category_id_when_category_missing(service):
    """Gdy kategoria wynikowa nie istnieje w bazie, category_id powinno być None."""
    result = service.classify("Nie działa VPN", "Problem z VPN", categories=[])
    assert result.category_id is None


def test_classify_explanation_not_empty(service, categories):
    result = service.classify("Drukarka nie działa", "Problem ze sprzętem", categories)
    assert result.explanation
    assert len(result.explanation) > 10
