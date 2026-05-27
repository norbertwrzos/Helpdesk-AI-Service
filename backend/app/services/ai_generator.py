"""
MockAIGenerator — generuje propozycję rozwiązania na podstawie wyników analizy.

Odpowiedź jest generowana w języku polskim na podstawie szablonu.
W przyszłości tę klasę można zastąpić wywołaniem OpenAI API lub
innego modelu językowego bez zmian w AnalysisPipeline.
"""

import json

from app.models.ticket import Ticket
from app.schemas.analysis import ClassificationResult, GeneratedAnswer, PriorityResult, SimilarArticle

MODEL_NAME = "mock-ai-generator"
PROVIDER_NAME = "mock"

# Kroki diagnostyczne dopasowane do kategorii
DIAGNOSTIC_STEPS: dict[str, list[str]] = {
    "Sieć i VPN": [
        "Sprawdź połączenie internetowe na urządzeniu.",
        "Zrestartuj klienta VPN i spróbuj ponownie się połączyć.",
        "Zweryfikuj poprawność danych logowania do VPN.",
        "Skontaktuj się z administratorem sieci, jeśli problem nadal występuje.",
    ],
    "Konto i dostęp": [
        "Upewnij się, że konto użytkownika jest aktywne w systemie AD.",
        "Zresetuj hasło użytkownika zgodnie z polityką bezpieczeństwa.",
        "Sprawdź, czy uprawnienia użytkownika są poprawnie skonfigurowane.",
        "Skontaktuj się z działem IT w celu odblokowania konta.",
    ],
    "Aplikacje biznesowe": [
        "Sprawdź, czy aplikacja jest aktualna (ostatnia wersja).",
        "Zweryfikuj poprawność połączenia z serwerem aplikacji.",
        "Sprawdź logi aplikacji pod kątem błędów.",
        "Skontaktuj się z administratorem systemu w celu dalszej diagnostyki.",
    ],
    "Sprzęt komputerowy": [
        "Sprawdź fizyczne połączenia kabli i zasilania urządzenia.",
        "Uruchom urządzenie ponownie.",
        "Zaktualizuj sterowniki urządzenia.",
        "Zgłoś problem do działu serwisu sprzętu w celu dalszej diagnozy.",
    ],
    "Poczta e-mail": [
        "Sprawdź połączenie z serwerem pocztowym.",
        "Zweryfikuj ustawienia konta e-mail w kliencie pocztowym.",
        "Sprawdź rozmiar skrzynki odbiorczej — może być pełna.",
        "Skontaktuj się z administratorem poczty.",
    ],
    "Bezpieczeństwo": [
        "Nie klikaj w podejrzane linki ani nie otwieraj nieznanych załączników.",
        "Zmień hasło do wszystkich kont, które mogły zostać narażone.",
        "Uruchom skanowanie antywirusowe na urządzeniu.",
        "Natychmiast zgłoś incydent do działu bezpieczeństwa IT.",
    ],
    "System operacyjny": [
        "Sprawdź, czy system operacyjny jest aktualny.",
        "Uruchom ponownie komputer i sprawdź, czy problem nadal występuje.",
        "Przywróć ostatni znany dobry punkt przywracania systemu.",
        "Skontaktuj się z administratorem systemów w celu dalszej diagnozy.",
    ],
}

DEFAULT_STEPS = [
    "Opisz szczegółowo problem i okoliczności jego wystąpienia.",
    "Sprawdź, czy problem dotyczy tylko Twojego urządzenia/konta.",
    "Uruchom ponownie urządzenie i sprawdź, czy problem nadal występuje.",
    "Skontaktuj się z działem IT w celu dalszej pomocy.",
]


class MockAIGenerator:
    """
    Generuje propozycję rozwiązania na podstawie szablonu i wyników analizy.

    W przyszłości tę klasę można zastąpić wywołaniem modelu językowego
    (np. OpenAI GPT, lokalny LLM) bez zmian w AnalysisPipeline.
    """

    def generate(
        self,
        ticket: Ticket,
        classification: ClassificationResult,
        priority: PriorityResult,
        similar_articles: list[SimilarArticle],
    ) -> GeneratedAnswer:
        category_name = classification.category_name
        priority_name = priority.priority_name

        steps = DIAGNOSTIC_STEPS.get(category_name, DEFAULT_STEPS)
        steps_text = "\n".join(f"  {i + 1}. {step}" for i, step in enumerate(steps))

        similar_section = ""
        if similar_articles:
            titles = ", ".join(f'„{a.title}"' for a in similar_articles)
            similar_section = (
                f"\n\nW bazie wiedzy znaleziono podobne artykuły, "
                f"które mogą pomóc w rozwiązaniu problemu: {titles}."
            )

        response_text = (
            f'Na podstawie treści zgłoszenia "{ticket.title}" system rozpoznał problem '
            f"związany z kategorią: {category_name}.\n\n"
            f"Nadany priorytet: {priority_name}.\n\n"
            f"Zalecane kroki diagnostyczne:\n{steps_text}"
            f"{similar_section}\n\n"
            "Odpowiedź została wygenerowana automatycznie i powinna zostać "
            "zweryfikowana przez pracownika IT Support."
        )

        sources = None
        if similar_articles:
            sources_data = [
                {"id": a.id, "title": a.title, "score": a.score}
                for a in similar_articles
            ]
            sources = json.dumps(sources_data, ensure_ascii=False)

        return GeneratedAnswer(
            response_text=response_text,
            model_name=MODEL_NAME,
            provider_name=PROVIDER_NAME,
            sources_used=sources,
        )
