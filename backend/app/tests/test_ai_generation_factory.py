from app.core.config import Settings
from app.services.ai_generation import MockAIResponseProvider, get_ai_response_provider


def test_factory_falls_back_to_mock_when_openai_key_is_missing():
    settings = Settings(
        AI_GENERATION_PROVIDER="openai",
        OPENAI_API_KEY="",
        OPENAI_CHAT_MODEL="gpt-4o-mini",
        OPENAI_RESPONSE_TEMPERATURE=0.2,
        OPENAI_MAX_OUTPUT_TOKENS=1200,
    )

    provider = get_ai_response_provider(settings)

    assert isinstance(provider, MockAIResponseProvider)