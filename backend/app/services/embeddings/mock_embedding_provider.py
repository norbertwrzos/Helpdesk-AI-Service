from __future__ import annotations

import hashlib
import math

from app.services.embeddings.base import BaseEmbeddingProvider, EMBEDDING_DIMENSION


class MockEmbeddingProvider(BaseEmbeddingProvider):
    provider_name = "mock"

    def __init__(self, model_name: str = "mock-embedding-v1") -> None:
        super().__init__(model_name=model_name, vector_dimension=EMBEDDING_DIMENSION)

    def embed_text(self, text: str) -> list[float]:
        normalized = self.normalize_text(text)
        if not normalized:
            return self.zero_vector()

        values: list[float] = []
        seed = normalized.encode("utf-8")
        block_index = 0

        while len(values) < self.vector_dimension:
            digest = hashlib.sha256(seed + block_index.to_bytes(4, "big")).digest()
            for offset in range(0, len(digest), 4):
                chunk = digest[offset : offset + 4]
                if len(chunk) < 4:
                    continue
                raw = int.from_bytes(chunk, "big")
                values.append((raw / 0xFFFFFFFF) * 2.0 - 1.0)
                if len(values) == self.vector_dimension:
                    break
            block_index += 1

        magnitude = math.sqrt(sum(component * component for component in values))
        if magnitude == 0:
            return self.zero_vector()

        return [component / magnitude for component in values]

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]