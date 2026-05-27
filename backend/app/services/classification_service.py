"""
ClassificationService — klasyfikacja zgłoszenia do kategorii na podstawie reguł słów kluczowych.

Architektura celowo oddziela logikę klasyfikacji od bazy danych,
aby w przyszłości można było łatwo zastąpić tę klasę modelem ML/NLP.
"""

from app.models.category import Category
from app.schemas.analysis import ClassificationResult

# Reguły: (lista słów kluczowych, oczekiwana nazwa kategorii)
KEYWORD_RULES: list[tuple[list[str], str]] = [
    (
        ["phishing", "podejrzany link", "wirus", "malware", "incydent", "podejrzana wiadomość"],
        "Bezpieczeństwo",
    ),
    (
        ["vpn", "sieć", "internet", "połączenie", "wifi", "wi-fi", "router"],
        "Sieć i VPN",
    ),
    (
        ["hasło", "logowanie", "konto", "dostęp", "uprawnienia", "zablokowane konto"],
        "Konto i dostęp",
    ),
    (
        ["crm", "erp", "aplikacja", "system sprzedażowy", "system magazynowy", "błąd aplikacji"],
        "Aplikacje biznesowe",
    ),
    (
        ["laptop", "komputer", "drukarka", "monitor", "klawiatura", "mysz", "stacja dokująca"],
        "Sprzęt komputerowy",
    ),
    (
        ["mail", "poczta", "outlook", "wiadomość", "skrzynka", "załącznik"],
        "Poczta e-mail",
    ),
    (
        ["windows", "system operacyjny", "aktualizacja", "sterownik", "blue screen"],
        "System operacyjny",
    ),
]

DEFAULT_CATEGORY = "Inne"


class ClassificationService:
    """
    Klasyfikuje zgłoszenie do kategorii na podstawie reguł słów kluczowych.

    W przyszłości można zastąpić tę klasę implementacją opartą
    na modelu ML lub embeddingach bez zmian w AnalysisPipeline.
    """

    def classify(
        self,
        title: str,
        description: str,
        categories: list[Category],
    ) -> ClassificationResult:
        text = (title + " " + description).lower()
        category_map = {c.name: c for c in categories}

        for keywords, category_name in KEYWORD_RULES:
            matched = [kw for kw in keywords if kw in text]
            if matched:
                confidence = 0.85 if len(matched) >= 2 else 0.65
                cat = category_map.get(category_name) or category_map.get(DEFAULT_CATEGORY)
                used_name = cat.name if cat else category_name
                cat_id = cat.id if cat else None
                explanation = (
                    f'Zgłoszenie przypisano do kategorii "{used_name}", '
                    f"ponieważ treść zawiera słowo kluczowe: {matched[0]}."
                )
                return ClassificationResult(
                    category_id=cat_id,
                    category_name=used_name,
                    confidence=confidence,
                    explanation=explanation,
                )

        # Domyślna kategoria
        cat = category_map.get(DEFAULT_CATEGORY)
        explanation = (
            'Zgłoszenie przypisano do kategorii domyślnej "Inne", '
            "ponieważ treść nie pasuje do żadnej ze zdefiniowanych reguł klasyfikacji."
        )
        if cat is None:
            explanation = (
                "Nie udało się dopasować kategorii. "
                'Kategoria "Inne" nie istnieje w bazie danych.'
            )
        return ClassificationResult(
            category_id=cat.id if cat else None,
            category_name=cat.name if cat else DEFAULT_CATEGORY,
            confidence=0.40,
            explanation=explanation,
        )
