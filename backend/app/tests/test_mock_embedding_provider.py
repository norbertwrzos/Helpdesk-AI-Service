from app.services.embeddings.base import EMBEDDING_DIMENSION
from app.services.embeddings.mock_embedding_provider import MockEmbeddingProvider


def test_mock_embedding_is_deterministic():
    provider = MockEmbeddingProvider()

    first = provider.embed_text("Nie dziala VPN i polaczenie jest zrywane")
    second = provider.embed_text("Nie dziala VPN i polaczenie jest zrywane")

    assert first == second
    assert len(first) == EMBEDDING_DIMENSION


def test_mock_embedding_handles_empty_text():
    provider = MockEmbeddingProvider()

    embedding = provider.embed_text("   ")

    assert embedding == [0.0] * EMBEDDING_DIMENSION