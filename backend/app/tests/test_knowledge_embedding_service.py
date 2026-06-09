from __future__ import annotations

from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.knowledge_article_embedding import KnowledgeArticleEmbedding
from app.services.embeddings.base import BaseEmbeddingProvider, EMBEDDING_DIMENSION
from app.services.knowledge_embedding_service import KnowledgeEmbeddingService


class StubEmbeddingProvider(BaseEmbeddingProvider):
    provider_name = "stub"

    def __init__(self, model_name: str, fill_value: float) -> None:
        super().__init__(model_name=model_name, vector_dimension=EMBEDDING_DIMENSION)
        self.fill_value = fill_value
        self.calls = 0

    def embed_text(self, text: str) -> list[float]:
        self.calls += 1
        return [self.fill_value] + [0.0] * (self.vector_dimension - 1)

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]


def _create_article(db) -> KnowledgeArticle:
    category = Category(name="Sieć i VPN", description="Problemy sieciowe")
    db.add(category)
    db.flush()

    article = KnowledgeArticle(
        title="VPN nie łączy się z siecią",
        content="Sprawdź klienta VPN, połączenie internetowe i dane logowania.",
        category_id=category.id,
        tags="vpn, sieć",
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def test_reindex_article_creates_embedding(db):
    article = _create_article(db)
    provider = StubEmbeddingProvider(model_name="stub-v1", fill_value=0.5)
    service = KnowledgeEmbeddingService(provider=provider)

    result = service.reindex_article(db, article.id)
    saved = (
        db.query(KnowledgeArticleEmbedding)
        .filter(KnowledgeArticleEmbedding.article_id == article.id)
        .first()
    )

    assert result["status"] == "indexed"
    assert saved is not None
    assert saved.embedding_model == "stub-v1"
    assert saved.content_hash == result["content_hash"]


def test_reindex_article_skips_up_to_date_article(db):
    article = _create_article(db)
    provider = StubEmbeddingProvider(model_name="stub-v1", fill_value=0.5)
    service = KnowledgeEmbeddingService(provider=provider)

    first = service.reindex_article(db, article.id)
    second = service.reindex_article(db, article.id)

    assert first["status"] == "indexed"
    assert second["status"] == "skipped"
    assert provider.calls == 1


def test_reindex_article_force_updates_existing_embedding(db):
    article = _create_article(db)
    first_provider = StubEmbeddingProvider(model_name="stub-v1", fill_value=0.5)
    second_provider = StubEmbeddingProvider(model_name="stub-v2", fill_value=0.9)

    KnowledgeEmbeddingService(provider=first_provider).reindex_article(db, article.id)
    result = KnowledgeEmbeddingService(provider=second_provider).reindex_article(
        db,
        article.id,
        force=True,
    )
    saved = (
        db.query(KnowledgeArticleEmbedding)
        .filter(KnowledgeArticleEmbedding.article_id == article.id)
        .first()
    )

    assert result["status"] == "indexed"
    assert saved is not None
    assert saved.embedding_model == "stub-v2"
    assert saved.embedding[0] == 0.9