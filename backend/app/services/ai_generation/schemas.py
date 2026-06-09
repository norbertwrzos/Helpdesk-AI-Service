from __future__ import annotations

from pydantic import BaseModel, Field


class RetrievedArticleForGeneration(BaseModel):
    article_id: int
    title: str
    excerpt: str
    score: float
    category_id: int | None = None


class TicketResponseGenerationInput(BaseModel):
    ticket_id: int | str
    title: str
    description: str
    category_name: str
    priority_name: str
    requester_name: str | None = None
    agent_name: str
    retrieved_articles: list[RetrievedArticleForGeneration] = Field(default_factory=list)
    classification_explanation: str | None = None
    priority_explanation: str | None = None


class TicketResponseGenerationResult(BaseModel):
    subject: str
    email_body: str
    confidence: float
    used_sources: list[int] = Field(default_factory=list)
    requires_human_review: bool
    limitations: str
    model_name: str
    provider_name: str
    raw_response: str | None = None


class StructuredMailResponse(BaseModel):
    subject: str
    email_body: str
    confidence: float
    used_sources: list[int]
    requires_human_review: bool
    limitations: str