from app.services.ai_generation.prompt_builder import (
    build_system_instruction,
    build_user_prompt,
)
from app.services.ai_generation.schemas import (
    RetrievedArticleForGeneration,
    TicketResponseGenerationInput,
)


def _input() -> TicketResponseGenerationInput:
    return TicketResponseGenerationInput(
        ticket_id=10,
        title="Nie działa VPN",
        description="Połączenie VPN nie zestawia się od rana.",
        category_name="Sieć i VPN",
        priority_name="Wysoki",
        requester_name="Jan Kowalski",
        agent_name="Norbert",
        retrieved_articles=[
            RetrievedArticleForGeneration(
                article_id=1,
                title="Diagnostyka VPN",
                excerpt="Sprawdź połączenie internetowe i dane logowania.",
                score=0.91,
                category_id=2,
            )
        ],
        classification_explanation="W treści występuje VPN.",
        priority_explanation="Wpływ na pracę użytkownika.",
    )


def test_prompt_contains_mail_format():
    payload = _input()
    system_instruction = build_system_instruction(payload.agent_name)
    user_prompt = build_user_prompt(payload)

    assert "Dzień dobry," in system_instruction
    assert "Pozdrawiam," in user_prompt


def test_prompt_contains_agent_name_and_retrieved_articles():
    payload = _input()
    system_instruction = build_system_instruction(payload.agent_name)
    user_prompt = build_user_prompt(payload)

    assert "Norbert" in system_instruction
    assert "Diagnostyka VPN" in user_prompt
    assert "article_id: 1" in user_prompt


def test_prompt_does_not_contain_requester_email():
    payload = _input()
    user_prompt = build_user_prompt(payload)

    assert "requester_email" not in user_prompt.lower()
    assert "@" not in user_prompt