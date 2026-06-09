from __future__ import annotations

import logging

from app.services.embeddings.base import BaseEmbeddingProvider, EMBEDDING_DIMENSION

logger = logging.getLogger(__name__)


class OpenAIEmbeddingProvider(BaseEmbeddingProvider):
    provider_name = "openai"

    def __init__(self, api_key: str, model_name: str) -> None:
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not configured.")

        super().__init__(model_name=model_name, vector_dimension=EMBEDDING_DIMENSION)

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("The openai package is required for OpenAI embeddings.") from exc

        self._client = OpenAI(api_key=api_key)

    def embed_text(self, text: str) -> list[float]:
        normalized = self.normalize_text(text)
        if not normalized:
            return self.zero_vector()

        try:
            response = self._client.embeddings.create(
                model=self.model_name,
                input=normalized,
            )
        except Exception as exc:  # pragma: no cover - external API errors are environment-specific
            logger.warning(
                "OpenAI embedding request failed for model '%s': %s",
                self.model_name,
                exc,
            )
            raise RuntimeError("Embedding provider request failed.") from exc

        if not response.data:
            logger.warning("OpenAI embedding request returned no vectors for model '%s'.", self.model_name)
            return self.zero_vector()

        return [float(value) for value in response.data[0].embedding]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        normalized_texts = [self.normalize_text(text) for text in texts]
        empty_indexes = [index for index, text in enumerate(normalized_texts) if not text]
        request_payload = [text for text in normalized_texts if text]

        if not request_payload:
            return [self.zero_vector() for _ in normalized_texts]

        try:
            response = self._client.embeddings.create(
                model=self.model_name,
                input=request_payload,
            )
        except Exception as exc:  # pragma: no cover - external API errors are environment-specific
            logger.warning(
                "OpenAI embedding batch request failed for model '%s': %s",
                self.model_name,
                exc,
            )
            raise RuntimeError("Embedding provider request failed.") from exc

        embeddings = [[float(value) for value in item.embedding] for item in response.data]
        result: list[list[float]] = []
        embedding_index = 0
        empty_lookup = set(empty_indexes)
        for index in range(len(normalized_texts)):
            if index in empty_lookup:
                result.append(self.zero_vector())
                continue
            result.append(embeddings[embedding_index])
            embedding_index += 1

        return result