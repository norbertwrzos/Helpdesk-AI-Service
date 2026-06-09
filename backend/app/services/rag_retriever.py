from __future__ import annotations

import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.knowledge_article_embedding import KnowledgeArticleEmbedding
from app.models.priority import Priority
from app.models.ticket import Ticket
from app.schemas.rag import RagRetrievedArticle
from app.services.embeddings import BaseEmbeddingProvider, get_embedding_provider
from app.services.similarity_service import SimilarityService

logger = logging.getLogger(__name__)

EXCERPT_LENGTH = 200


def _excerpt(content: str) -> str:
    if len(content) <= EXCERPT_LENGTH:
        return content
    return content[:EXCERPT_LENGTH].rsplit(" ", 1)[0] + "…"


class RagRetriever:
    def __init__(
        self,
        provider: BaseEmbeddingProvider | None = None,
        similarity_service: SimilarityService | None = None,
        default_top_k: int | None = None,
        min_score: float | None = None,
    ) -> None:
        self.provider = provider or get_embedding_provider(settings)
        self.similarity_service = similarity_service or SimilarityService()
        self.default_top_k = default_top_k or settings.RAG_TOP_K
        self.min_score = settings.RAG_MIN_SCORE if min_score is None else min_score

    def is_vector_retrieval_available(self, db: Session) -> bool:
        bind = db.get_bind()
        if bind.dialect.name != "postgresql":
            return False
        if self.provider.provider_name == "mock":
            return False
        return (
            db.query(KnowledgeArticleEmbedding.id)
            .limit(1)
            .first()
            is not None
        )

    def retrieve_for_ticket(
        self,
        db: Session,
        ticket: Ticket,
        top_k: int | None = None,
    ) -> list[RagRetrievedArticle]:
        query_text = self._build_ticket_query(db, ticket)
        return self._retrieve(
            db,
            query_text=query_text,
            top_k=top_k,
            fallback_title=ticket.title,
            fallback_description=ticket.description,
            classification_category_id=ticket.category_id,
        )

    def retrieve_for_query(
        self,
        db: Session,
        query: str,
        top_k: int | None = None,
    ) -> list[RagRetrievedArticle]:
        normalized = query.strip()
        if not normalized:
            return []
        return self._retrieve(
            db,
            query_text=normalized,
            top_k=top_k,
            fallback_title=normalized,
            fallback_description=normalized,
            classification_category_id=None,
        )

    def _retrieve(
        self,
        db: Session,
        query_text: str,
        top_k: int | None,
        fallback_title: str,
        fallback_description: str,
        classification_category_id: int | None,
    ) -> list[RagRetrievedArticle]:
        normalized = query_text.strip()
        if not normalized:
            return []

        resolved_top_k = top_k or self.default_top_k

        if self.provider.provider_name == "mock":
            logger.info("RAG uses SimilarityService fallback because the mock provider is active.")
            return self._fallback_to_similarity(
                db,
                title=fallback_title,
                description=fallback_description,
                classification_category_id=classification_category_id,
                top_k=resolved_top_k,
            )

        bind = db.get_bind()
        if bind.dialect.name != "postgresql":
            logger.info(
                "RAG uses SimilarityService fallback because pgvector is unavailable for dialect '%s'.",
                bind.dialect.name,
            )
            return self._fallback_to_similarity(
                db,
                title=fallback_title,
                description=fallback_description,
                classification_category_id=classification_category_id,
                top_k=resolved_top_k,
            )

        if not self._has_embeddings(db):
            logger.info("RAG retrieval skipped because no knowledge article embeddings are indexed yet.")
            return []

        try:
            query_embedding = self.provider.embed_text(normalized)
            rows = db.execute(
                text(
                    """
                    SELECT
                        ka.id AS article_id,
                        ka.title AS title,
                        ka.content AS content,
                        ka.category_id AS category_id,
                        (kae.embedding <=> CAST(:query_embedding AS vector)) AS distance
                    FROM knowledge_article_embeddings AS kae
                    JOIN knowledge_articles AS ka
                        ON ka.id = kae.article_id
                    ORDER BY kae.embedding <=> CAST(:query_embedding AS vector)
                    LIMIT :top_k
                    """
                ),
                {
                    "query_embedding": self._to_pgvector_literal(query_embedding),
                    "top_k": resolved_top_k,
                },
            ).mappings().all()
        except Exception as exc:
            logger.warning(
                "RAG retrieval failed for model '%s'; using SimilarityService fallback: %s",
                self.provider.model_name,
                exc,
            )
            return self._fallback_to_similarity(
                db,
                title=fallback_title,
                description=fallback_description,
                classification_category_id=classification_category_id,
                top_k=resolved_top_k,
            )

        results: list[RagRetrievedArticle] = []
        for row in rows:
            score = max(0.0, min(1.0, 1.0 - float(row["distance"])))
            if score < self.min_score:
                continue
            results.append(
                RagRetrievedArticle(
                    article_id=int(row["article_id"]),
                    title=row["title"],
                    excerpt=_excerpt(row["content"]),
                    category_id=row["category_id"],
                    score=round(score, 4),
                )
            )

        return results

    def _build_ticket_query(self, db: Session, ticket: Ticket) -> str:
        parts = [ticket.title.strip(), ticket.description.strip()]

        category_name = self._get_category_name(db, ticket.category_id)
        if category_name:
            parts.append(f"Kategoria: {category_name}")

        priority_name = self._get_priority_name(db, ticket.priority_id)
        if priority_name:
            parts.append(f"Priorytet: {priority_name}")

        return "\n".join(part for part in parts if part)

    def _fallback_to_similarity(
        self,
        db: Session,
        title: str,
        description: str,
        classification_category_id: int | None,
        top_k: int,
    ) -> list[RagRetrievedArticle]:
        articles = db.query(KnowledgeArticle).all()
        similar_articles = self.similarity_service.find_similar(
            title=title,
            description=description,
            articles=articles,
            classification_category_id=classification_category_id,
            top_k=top_k,
        )
        return [
            RagRetrievedArticle(
                article_id=article.id,
                title=article.title,
                excerpt=article.excerpt,
                category_id=article.category_id,
                score=article.score,
            )
            for article in similar_articles
        ]

    def _has_embeddings(self, db: Session) -> bool:
        return db.query(KnowledgeArticleEmbedding.id).limit(1).first() is not None

    def _get_category_name(self, db: Session, category_id: int | None) -> str | None:
        if category_id is None:
            return None
        category = db.query(Category).filter(Category.id == category_id).first()
        return category.name if category else None

    def _get_priority_name(self, db: Session, priority_id: int | None) -> str | None:
        if priority_id is None:
            return None
        priority = db.query(Priority).filter(Priority.id == priority_id).first()
        return priority.name if priority else None

    def _to_pgvector_literal(self, vector: list[float]) -> str:
        values = ", ".join(f"{component:.12f}" for component in vector)
        return f"[{values}]"