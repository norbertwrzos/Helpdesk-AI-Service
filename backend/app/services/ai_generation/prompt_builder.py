from __future__ import annotations

from app.services.ai_generation.schemas import TicketResponseGenerationInput


def build_system_instruction(agent_name: str) -> str:
    return (
        "Jesteś asystentem działu IT Support przygotowującym propozycję odpowiedzi "
        "mailowej dla użytkownika. Odpowiadasz wyłącznie po polsku. "
        "Buduj odpowiedź tylko na podstawie treści zgłoszenia, rozpoznanej kategorii, "
        "nadanego priorytetu oraz przekazanych artykułów bazy wiedzy. "
        "Nie wymyślaj procedur, kroków administracyjnych ani informacji, których nie ma w danych wejściowych. "
        "Jeżeli baza wiedzy nie daje wystarczających podstaw, napisz wyraźnie, że zgłoszenie wymaga dalszej analizy przez pracownika IT. "
        "Odpowiedź ma mieć format mailowy: 'Dzień dobry,', treść, 'Pozdrawiam,' i podpis agenta. "
        f"Podpis ma zawierać dokładnie imię agenta: {agent_name}. "
        "To jest propozycja odpowiedzi dla agenta, a nie automatyczne zamknięcie zgłoszenia. "
        "Nie obiecuj rozwiązania problemu, jeśli nie wynika to jednoznacznie z danych wejściowych. "
        "Zwróć wynik jako ustrukturyzowany obiekt zgodny ze schematem."
    )


def build_user_prompt(data: TicketResponseGenerationInput) -> str:
    articles_section = "Brak artykułów RAG."
    if data.retrieved_articles:
        article_lines = []
        for article in data.retrieved_articles:
            article_lines.append(
                "\n".join(
                    [
                        f"- article_id: {article.article_id}",
                        f"  title: {article.title}",
                        f"  score: {article.score:.4f}",
                        f"  excerpt: {article.excerpt}",
                    ]
                )
            )
        articles_section = "\n\n".join(article_lines)

    requester_line = f"Zgłaszający: {data.requester_name}\n" if data.requester_name else ""
    classification_line = (
        f"Uzasadnienie klasyfikacji: {data.classification_explanation}\n"
        if data.classification_explanation
        else ""
    )
    priority_line = (
        f"Uzasadnienie priorytetu: {data.priority_explanation}\n"
        if data.priority_explanation
        else ""
    )

    return (
        "Przygotuj propozycję odpowiedzi mailowej dla użytkownika końcowego.\n\n"
        f"Ticket ID: {data.ticket_id}\n"
        f"Tytuł zgłoszenia: {data.title}\n"
        f"Opis zgłoszenia: {data.description}\n"
        f"Kategoria: {data.category_name}\n"
        f"Priorytet: {data.priority_name}\n"
        f"{requester_line}"
        f"Imię agenta: {data.agent_name}\n"
        f"{classification_line}"
        f"{priority_line}"
        "Artykuły znalezione przez RAG:\n"
        f"{articles_section}\n\n"
        "Wymagania odpowiedzi:\n"
        "- zacznij od 'Dzień dobry,'\n"
        "- uwzględnij krótkie odniesienie do problemu użytkownika\n"
        "- podaj tylko kroki wynikające z przekazanych źródeł\n"
        "- jeśli źródła nie wystarczają, zaznacz potrzebę dalszej analizy przez pracownika IT\n"
        "- zakończ 'Pozdrawiam,' i podpisem agenta\n"
        "- nie podawaj informacji o wysyłce maila ani automatycznym rozwiązaniu zgłoszenia\n"
    )