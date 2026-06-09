"""Zgodnościowy wrapper dla historycznego MockAIGenerator."""

from __future__ import annotations

import json

from app.models.ticket import Ticket
from app.schemas.analysis import ClassificationResult, GeneratedAnswer, PriorityResult, SimilarArticle
from app.services.ai_generation.mock_provider import MockAIResponseProvider
from app.services.ai_generation.schemas import (
    RetrievedArticleForGeneration,
    TicketResponseGenerationInput,
)


class MockAIGenerator:
    def __init__(self, provider: MockAIResponseProvider | None = None) -> None:
        self.provider = provider or MockAIResponseProvider()

    def generate(
        self,
        ticket: Ticket,
        classification: ClassificationResult,
        priority: PriorityResult,
        similar_articles: list[SimilarArticle],
    ) -> GeneratedAnswer:
        generation_input = TicketResponseGenerationInput(
            ticket_id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            category_name=classification.category_name,
            priority_name=priority.priority_name,
            requester_name=getattr(ticket, "requester_name", None),
            agent_name=getattr(ticket, "assigned_agent_name", None)
            or "Agent IT Support",
            retrieved_articles=[
                RetrievedArticleForGeneration(
                    article_id=article.id,
                    title=article.title,
                    excerpt=article.excerpt,
                    score=article.score,
                    category_id=article.category_id,
                )
                for article in similar_articles
            ],
            classification_explanation=classification.explanation,
            priority_explanation=priority.explanation,
        )
        result = self.provider.generate_ticket_response(generation_input)

        sources = None
        if similar_articles:
            sources = json.dumps(
                [
                    {
                        "id": article.id,
                        "title": article.title,
                        "score": article.score,
                        "excerpt": article.excerpt,
                    }
                    for article in similar_articles
                ],
                ensure_ascii=False,
            )

        return GeneratedAnswer(
            response_text=result.email_body,
            model_name=result.model_name,
            provider_name=result.provider_name,
            sources_used=sources,
        )
