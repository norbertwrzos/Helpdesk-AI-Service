"""
PriorityAnalysisService — nadawanie priorytetu zgłoszeniu na podstawie reguł słów kluczowych.

Architektura celowo oddziela logikę priorytetyzacji od bazy danych,
aby w przyszłości można było łatwo zastąpić tę klasę modelem ML/NLP.

Uwaga: plik priority_service.py obsługuje CRUD priorytetów.
Ten plik odpowiada wyłącznie za analizę treści i wnioskowanie o priorytecie.
"""

import re

from app.models.priority import Priority
from app.schemas.analysis import PriorityResult

# Kolejność ważna — sprawdzamy od najwyższego priorytetu
PRIORITY_RULES: list[tuple[list[str], str, float]] = [
    (
        ["cały dział", "wszyscy", "produkcja", "system niedostępny",
         "brak dostępu dla wielu użytkowników", "awaria krytyczna"],
        "Krytyczny",
        0.85,
    ),
    (
        ["pilne", "nie mogę pracować", "awaria", "bezpieczeństwo",
         "phishing", "podejrzany link", "incydent"],
        "Wysoki",
        0.85,
    ),
    (
        ["problem jednego użytkownika", "nie działa", "błąd logowania", "nie mogę się zalogować"],
        "Średni",
        0.70,
    ),
    (
        ["prośba", "pytanie", "konfiguracja", "drukarka", "informacja"],
        "Niski",
        0.65,
    ),
]

DEFAULT_PRIORITY = "Średni"
DEFAULT_CONFIDENCE = 0.50


def _contains_keyword(text: str, keyword: str) -> bool:
    """
    Sprawdza, czy tekst zawiera słowo kluczowe jako całe słowo lub frazę.
    Działa zarówno dla pojedynczych słów jak i wielowyrazowych fraz.
    """
    # Dla fraz wielowyrazowych używamy prostego dopasowania podciągu
    if " " in keyword:
        return keyword in text
    # Dla pojedynczych słów szukamy dopasowania otoczonego białymi znakami lub granicami ciągu
    pattern = r"(?<![a-ząćęłńóśźżA-ZĄĆĘŁŃÓŚŹŻ])" + re.escape(keyword) + r"(?![a-ząćęłńóśźżA-ZĄĆĘŁŃÓŚŹŻ])"
    return bool(re.search(pattern, text, re.IGNORECASE))


class PriorityAnalysisService:
    """
    Nadaje priorytet zgłoszeniu na podstawie reguł słów kluczowych.

    W przyszłości można zastąpić tę klasę implementacją opartą
    na modelu ML bez zmian w AnalysisPipeline.
    """

    def analyze(
        self,
        title: str,
        description: str,
        priorities: list[Priority],
    ) -> PriorityResult:
        text = (title + " " + description).lower()
        priority_map = {p.name: p for p in priorities}

        for keywords, priority_name, confidence in PRIORITY_RULES:
            matched = [kw for kw in keywords if _contains_keyword(text, kw)]
            if matched:
                pri = priority_map.get(priority_name) or priority_map.get(DEFAULT_PRIORITY)
                used_name = pri.name if pri else priority_name
                pri_id = pri.id if pri else None
                explanation = (
                    f'Priorytet ustawiono jako "{used_name}", '
                    f"ponieważ treść zgłoszenia zawiera słowo kluczowe: {matched[0]}."
                )
                return PriorityResult(
                    priority_id=pri_id,
                    priority_name=used_name,
                    confidence=confidence,
                    explanation=explanation,
                )

        # Domyślny priorytet
        pri = priority_map.get(DEFAULT_PRIORITY)
        explanation = (
            'Priorytet ustawiono jako domyslny "Sredni", '
            "ponieważ treść zgłoszenia nie pasuje do żadnej ze zdefiniowanych reguł priorytetyzacji."
        )
        if pri is None:
            explanation = (
                "Nie udało się dopasować priorytetu. "
                'Priorytet "Sredni" nie istnieje w bazie danych.'
            )
        return PriorityResult(
            priority_id=pri.id if pri else None,
            priority_name=pri.name if pri else DEFAULT_PRIORITY,
            confidence=DEFAULT_CONFIDENCE,
            explanation=explanation,
        )
