from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.knowledge_article_embedding import KnowledgeArticleEmbedding
from app.services.embeddings import BaseEmbeddingProvider, get_embedding_provider
from app.utils.hash_utils import calculate_content_hash

logger = logging.getLogger(__name__)


class KnowledgeEmbeddingService:
    def __init__(self, provider: BaseEmbeddingProvider | None = None) -> None:
        self.provider = provider or get_embedding_provider(settings)

    def build_article_text(
        self,
        article: KnowledgeArticle,
        category_name: str | None = None,
    ) -> str:
        parts = [f"Tytuł: {article.title.strip()}"]
        if category_name:
            parts.append(f"Kategoria: {category_name.strip()}")
        elif article.category_id is not None:
            parts.append(f"Kategoria ID: {article.category_id}")
        if article.tags:
            parts.append(f"Tagi: {article.tags.strip()}")
        parts.append(f"Treść: {article.content.strip()}")
        return "\n".join(parts)

    def reindex_article(
        self,
        db: Session,
        article_id: int,
        force: bool = False,
    ) -> dict[str, Any]:
        article = (
            db.query(KnowledgeArticle)
            .filter(KnowledgeArticle.id == article_id)
            .first()
        )
        if not article:
            return {
                "article_id": article_id,
                "status": "error",
                "message": "Artykuł nie został znaleziony.",
            }

        category_name = self._get_category_name(db, article.category_id)
        article_text = self.build_article_text(article, category_name)
        content_hash = calculate_content_hash(
            "\n".join(
                [
                    f"title:{article.title}",
                    f"content:{article.content}",
                    f"tags:{article.tags or ''}",
                    f"category_id:{article.category_id or ''}",
                    f"category_name:{category_name or ''}",
                ]
            )
        )

        existing = (
            db.query(KnowledgeArticleEmbedding)
            .filter(KnowledgeArticleEmbedding.article_id == article.id)
            .first()
        )
        if existing and existing.content_hash == content_hash and not force:
            return {
                "article_id": article.id,
                "status": "skipped",
                "content_hash": content_hash,
            }

        try:
            embedding = self.provider.embed_text(article_text)
            if existing:
                existing.embedding = embedding
                existing.embedding_model = self.provider.model_name
                existing.content_hash = content_hash
            else:
                db.add(
                    KnowledgeArticleEmbedding(
                        article_id=article.id,
                        embedding=embedding,
                        embedding_model=self.provider.model_name,
                        content_hash=content_hash,
                    )
                )
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.warning(
                "Nie udało się zreindeksować artykułu %s przy użyciu modelu '%s': %s",
                article.id,
                self.provider.model_name,
                exc,
            )
            return {
                "article_id": article.id,
                "status": "error",
                "message": str(exc),
            }

        return {
            "article_id": article.id,
            "status": "indexed",
            "content_hash": content_hash,
            "embedding_model": self.provider.model_name,
        }

    def reindex_all(
        self,
        db: Session,
        force: bool = False,
        limit: int | None = None,
    ) -> dict[str, Any]:
        query = db.query(KnowledgeArticle).order_by(KnowledgeArticle.id.asc())
        if limit is not None:
            query = query.limit(limit)

        articles = query.all()
        summary: dict[str, Any] = {
            "total_articles": len(articles),
            "indexed": 0,
            "skipped": 0,
            "errors": [],
        }

        for article in articles:
            result = self.reindex_article(db, article.id, force=force)
            if result["status"] == "indexed":
                summary["indexed"] += 1
            elif result["status"] == "skipped":
                summary["skipped"] += 1
            else:
                summary["errors"].append(result)

        return summary

    def _get_category_name(self, db: Session, category_id: int | None) -> str | None:
        if category_id is None:
            return None
        category = db.query(Category).filter(Category.id == category_id).first()
        return category.name if category else None