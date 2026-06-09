from __future__ import annotations

import logging

from app.core.config import Settings
from app.services.ai_generation.base import BaseAIResponseProvider
from app.services.ai_generation.mock_provider import MockAIResponseProvider
from app.services.ai_generation.openai_provider import OpenAIResponseProvider

logger = logging.getLogger(__name__)


def get_ai_response_provider(
    settings: Settings,
    client=None,
) -> BaseAIResponseProvider:
    provider_name = settings.AI_GENERATION_PROVIDER.lower().strip()

    if provider_name == "openai":
        try:
            return OpenAIResponseProvider(
                api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_CHAT_MODEL,
                temperature=settings.OPENAI_RESPONSE_TEMPERATURE,
                max_output_tokens=settings.OPENAI_MAX_OUTPUT_TOKENS,
                client=client,
            )
        except Exception as exc:
            logger.warning(
                "OpenAI generation provider is unavailable, falling back to mock provider: %s",
                exc,
            )

    return MockAIResponseProvider()


__all__ = [
    "BaseAIResponseProvider",
    "MockAIResponseProvider",
    "OpenAIResponseProvider",
    "get_ai_response_provider",
]