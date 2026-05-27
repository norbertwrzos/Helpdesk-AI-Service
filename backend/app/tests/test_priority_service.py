import pytest

from app.models.priority import Priority
from app.services.priority_analysis_service import PriorityAnalysisService


def _make_priorities() -> list[Priority]:
    data = [
        ("Niski", 1),
        ("Średni", 2),
        ("Wysoki", 3),
        ("Krytyczny", 4),
    ]
    return [Priority(id=i + 1, name=name, level=level) for i, (name, level) in enumerate(data)]


@pytest.fixture()
def service() -> PriorityAnalysisService:
    return PriorityAnalysisService()


@pytest.fixture()
def priorities() -> list[Priority]:
    return _make_priorities()


def test_critical_priority(service, priorities):
    result = service.analyze(
        "Cały dział nie ma dostępu do systemu",
        "System niedostępny dla wszystkich użytkowników produkcji",
        priorities,
    )
    assert result.priority_name == "Krytyczny"
    assert result.confidence >= 0.85


def test_high_priority_phishing(service, priorities):
    result = service.analyze(
        "Podejrzany link",
        "Otrzymałem podejrzany link, potencjalny phishing",
        priorities,
    )
    assert result.priority_name == "Wysoki"
    assert result.confidence >= 0.85


def test_medium_priority_single_user(service, priorities):
    result = service.analyze(
        "Problem jednego użytkownika z logowaniem",
        "Jeden pracownik nie może się zalogować do systemu",
        priorities,
    )
    assert result.priority_name == "Średni"
    assert result.confidence >= 0.70


def test_low_priority_printer(service, priorities):
    result = service.analyze(
        "Prośba o konfigurację drukarki",
        "Proszę o konfigurację nowej drukarki sieciowej",
        priorities,
    )
    assert result.priority_name == "Niski"
    assert result.confidence >= 0.65


def test_default_medium_when_no_match(service, priorities):
    result = service.analyze(
        "Ogólne zapytanie",
        "Mam ogólne zapytanie",
        priorities,
    )
    assert result.priority_name == "Średni"
    assert result.confidence == 0.50


def test_explanation_not_empty(service, priorities):
    result = service.analyze("Awaria systemu", "System nie działa", priorities)
    assert result.explanation
    assert len(result.explanation) > 10
