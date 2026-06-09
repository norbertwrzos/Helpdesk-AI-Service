from __future__ import annotations

import logging

from app.core.config import Settings
from app.services.embeddings.base import BaseEmbeddingProvider
from app.services.embeddings.mock_embedding_provider import MockEmbeddingProvider
from app.services.embeddings.openai_embedding_provider import OpenAIEmbeddingProvider

logger = logging.getLogger(__name__)


def get_embedding_provider(settings: Settings) -> BaseEmbeddingProvider:
    provider_name = settings.RAG_EMBEDDING_PROVIDER.lower().strip()

    if provider_name == "openai":
        try:
            return OpenAIEmbeddingProvider(
                api_key=settings.OPENAI_API_KEY,
                model_name=settings.OPENAI_EMBEDDING_MODEL,
            )
        except Exception as exc:
            logger.warning(
                "OpenAI embedding provider is unavailable, falling back to mock provider: %s",
                exc,
            )

    return MockEmbeddingProvider()


__all__ = [
    "BaseEmbeddingProvider",
    "MockEmbeddingProvider",
    "OpenAIEmbeddingProvider",
    "get_embedding_provider",
]