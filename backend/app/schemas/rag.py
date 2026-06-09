from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.analysis import SimilarArticle


class KnowledgeReindexRequest(BaseModel):
    force: bool = False


class KnowledgeReindexResponse(BaseModel):
    total_articles: int
    indexed: int
    skipped: int
    errors: list[dict[str, Any]] = Field(default_factory=list)


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)


class KnowledgeSearchResult(BaseModel):
    article_id: int
    title: str
    excerpt: str
    category_id: int | None
    score: float


class RagRetrievedArticle(KnowledgeSearchResult):
    source_type: Literal["knowledge_article"] = "knowledge_article"

    def to_similar_article(self) -> SimilarArticle:
        return SimilarArticle(
            id=self.article_id,
            title=self.title,
            excerpt=self.excerpt,
            category_id=self.category_id,
            score=self.score,
        )