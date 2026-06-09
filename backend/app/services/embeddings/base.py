from __future__ import annotations

from abc import ABC, abstractmethod


EMBEDDING_DIMENSION = 1536


class BaseEmbeddingProvider(ABC):
    provider_name = "base"

    def __init__(self, model_name: str, vector_dimension: int = EMBEDDING_DIMENSION) -> None:
        self.model_name = model_name
        self.vector_dimension = vector_dimension

    @staticmethod
    def normalize_text(text: str) -> str:
        return text.strip()

    def zero_vector(self) -> list[float]:
        return [0.0] * self.vector_dimension

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError

    @abstractmethod
    def embed_many(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError