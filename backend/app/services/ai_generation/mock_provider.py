from __future__ import annotations

from app.services.ai_generation.base import BaseAIResponseProvider
from app.services.ai_generation.schemas import (
    TicketResponseGenerationInput,
    TicketResponseGenerationResult,
)

MODEL_NAME = "mock-ai-generator"

DIAGNOSTIC_STEPS: dict[str, list[str]] = {
    "Sieć i VPN": [
        "Proszę sprawdzić połączenie internetowe na urządzeniu.",
        "Proszę uruchomić ponownie klienta VPN i spróbować ponownie się połączyć.",
        "Proszę zweryfikować poprawność danych logowania do VPN.",
    ],
    "Konto i dostęp": [
        "Proszę upewnić się, że konto jest aktywne i nie zostało zablokowane.",
        "Proszę spróbować ponownie zalogować się po weryfikacji hasła.",
        "Jeśli problem dotyczy uprawnień, proszę wskazać dokładnie, do którego zasobu brakuje dostępu.",
    ],
}

DEFAULT_STEPS = [
    "Na podstawie aktualnych danych rekomendujemy wstępną weryfikację okoliczności wystąpienia problemu.",
    "Jeżeli problem powtarza się, proszę wskazać dokładny moment i komunikat błędu.",
]


class MockAIResponseProvider(BaseAIResponseProvider):
    provider_name = "mock"

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        super().__init__(model_name=model_name)

    def generate_ticket_response(
        self,
        data: TicketResponseGenerationInput,
    ) -> TicketResponseGenerationResult:
        steps = DIAGNOSTIC_STEPS.get(data.category_name, DEFAULT_STEPS)
        referenced_titles = [article.title for article in data.retrieved_articles]
        source_ids = [article.article_id for article in data.retrieved_articles]

        intro = (
            f"dziękujemy za zgłoszenie dotyczące problemu: {data.title.lower()}. "
            f"Na obecnym etapie rozpoznano kategorię „{data.category_name}” "
            f"oraz priorytet „{data.priority_name}”."
        )

        if referenced_titles:
            knowledge_line = (
                "W oparciu o powiązane artykuły bazy wiedzy rekomendujemy następujące kroki: "
                + ", ".join(f"„{title}”" for title in referenced_titles)
                + "."
            )
        else:
            knowledge_line = (
                "W bazie wiedzy nie znaleziono wystarczających materiałów, dlatego zgłoszenie "
                "wymaga dalszej analizy przez pracownika IT."
            )

        steps_text = "\n".join(f"- {step}" for step in steps)
        follow_up = (
            "Jeżeli po wykonaniu powyższych czynności problem nadal będzie występował, "
            "proszę o odpowiedź na tę wiadomość z dodatkowymi szczegółami lub zrzutem komunikatu błędu."
        )

        email_body = (
            "Dzień dobry,\n\n"
            f"{intro}\n\n"
            f"{knowledge_line}\n\n"
            f"{steps_text}\n\n"
            f"{follow_up}\n\n"
            "Propozycja odpowiedzi została wygenerowana automatycznie i wymaga weryfikacji przez pracownika IT Support.\n\n"
            "Pozdrawiam,\n"
            f"{data.agent_name}"
        )

        return TicketResponseGenerationResult(
            subject=f"Odpowiedź do zgłoszenia #{data.ticket_id}: {data.title}",
            email_body=email_body,
            confidence=0.55 if referenced_titles else 0.35,
            used_sources=source_ids,
            requires_human_review=True,
            limitations=(
                "Odpowiedź została przygotowana przez mock provider i ma charakter szkicu dla agenta."
            ),
            model_name=self.model_name,
            provider_name=self.provider_name,
        )