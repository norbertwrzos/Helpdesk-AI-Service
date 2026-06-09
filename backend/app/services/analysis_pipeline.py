"""
AnalysisPipeline — koordynuje pełny proces analizy zgłoszenia.

Kolejność kroków:
1. Pobierz zgłoszenie (404 jeśli nie istnieje).
2. Pobierz kategorie, priorytety i artykuły bazy wiedzy.
3. Uruchom ClassificationService.
4. Uruchom PriorityAnalysisService.
5. Zaktualizuj zgłoszenie o wyniki klasyfikacji.
6. Uruchom RAGRetriever.
7. Uruchom provider generowania odpowiedzi mailowej.
8. Zapisz AIResponse w bazie.
9. Ustaw status zgłoszenia na ai_reviewed.
10. Zatwierdź wszystkie zmiany.
11. Zapisz wszystkie zmiany.
12. Zwróć AnalysisResult.
"""

import json
import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.ai_response import AIResponse
from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.priority import Priority
from app.models.ticket import Ticket, TicketStatus
from app.schemas.analysis import AnalysisResult, GeneratedAnswer
from app.schemas.rag import RagRetrievedArticle
from app.services.ai_generation import BaseAIResponseProvider, MockAIResponseProvider, get_ai_response_provider
from app.services.ai_generation.schemas import (
    RetrievedArticleForGeneration,
    TicketResponseGenerationInput,
    TicketResponseGenerationResult,
)
from app.services.classification_service import ClassificationService
from app.services.priority_analysis_service import PriorityAnalysisService
from app.services.rag_retriever import RagRetriever
from app.services.similarity_service import SimilarityService

logger = logging.getLogger(__name__)


class AnalysisPipeline:
    """
    Koordynuje pełny proces analizy zgłoszenia.

    Każdy komponent (ClassificationService, PriorityAnalysisService,
    SimilarityService, provider odpowiedzi AI) jest wstrzykiwany przez konstruktor,
    co ułatwia testy jednostkowe i wymianę na właściwe implementacje AI/NLP.

    Po zapisaniu wyniku analizy zgłoszenie otrzymuje status `ai_reviewed`.
    """

    def __init__(
        self,
        classifier: ClassificationService | None = None,
        priority_analyzer: PriorityAnalysisService | None = None,
        similarity: SimilarityService | None = None,
        rag_retriever: RagRetriever | None = None,
        ai_response_provider: BaseAIResponseProvider | None = None,
        fallback_ai_response_provider: BaseAIResponseProvider | None = None,
    ) -> None:
        self.classifier = classifier or ClassificationService()
        self.priority_analyzer = priority_analyzer or PriorityAnalysisService()
        self.similarity = similarity or SimilarityService()
        self.rag_retriever = rag_retriever or RagRetriever(
            similarity_service=self.similarity
        )
        self.ai_response_provider = ai_response_provider or get_ai_response_provider(settings)
        self.fallback_ai_response_provider = (
            fallback_ai_response_provider or MockAIResponseProvider()
        )

    def analyze_ticket(self, ticket_id: int, db: Session) -> AnalysisResult:
        # 1. Pobierz zgłoszenie
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Zgłoszenie o ID {ticket_id} nie zostało znalezione.",
            )

        # 2. Statusu nie zmieniamy do czasu zakończenia analizy
        db.flush()

        # 3. Pobierz dane pomocnicze
        categories = db.query(Category).all()
        priorities = db.query(Priority).all()
        articles = db.query(KnowledgeArticle).all()

        # 4. Klasyfikacja
        classification = self.classifier.classify(
            title=ticket.title,
            description=ticket.description,
            categories=categories,
        )

        # 5. Priorytetyzacja
        priority_result = self.priority_analyzer.analyze(
            title=ticket.title,
            description=ticket.description,
            priorities=priorities,
        )

        # 6. Zaktualizuj zgłoszenie
        ticket.category_id = classification.category_id
        ticket.priority_id = priority_result.priority_id
        ticket.classification_confidence = classification.confidence
        ticket.priority_confidence = priority_result.confidence
        ticket.classification_explanation = classification.explanation
        ticket.priority_explanation = priority_result.explanation
        db.flush()

        # 7. Wyszukiwanie podobnych artykułów
        retrieved_articles = self.rag_retriever.retrieve_for_ticket(db, ticket)
        similar_articles = [
            article.to_similar_article() for article in retrieved_articles
        ]

        # 8. Generowanie odpowiedzi AI
        generation_input = self._build_generation_input(
            ticket=ticket,
            classification=classification,
            priority_result=priority_result,
            retrieved_articles=retrieved_articles,
        )
        generation_result = self._generate_response(generation_input)
        generated = self._to_generated_answer(generation_result, retrieved_articles)

        # 9. Zapisz AIResponse
        ai_response = AIResponse(
            ticket_id=ticket.id,
            response_text=generated.response_text,
            model_name=generated.model_name,
            provider_name=generated.provider_name,
            sources_used=generated.sources_used,
        )
        db.add(ai_response)
        db.flush()

        # 10. Status ai_reviewed
        ticket.status = TicketStatus.ai_reviewed

        # 11. Zatwierdź zmiany
        db.commit()
        db.refresh(ticket)

        # 12. Zwróć wynik
        return AnalysisResult(
            ticket_id=ticket.id,
            classification=classification,
            priority=priority_result,
            similar_articles=similar_articles,
            ai_response=generated,
        )

    def _build_generation_input(
        self,
        ticket: Ticket,
        classification,
        priority_result,
        retrieved_articles: list[RagRetrievedArticle],
    ) -> TicketResponseGenerationInput:
        return TicketResponseGenerationInput(
            ticket_id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            category_name=classification.category_name,
            priority_name=priority_result.priority_name,
            requester_name=ticket.requester_name,
            agent_name=ticket.assigned_agent_name or "Agent IT Support",
            retrieved_articles=[
                RetrievedArticleForGeneration(
                    article_id=article.article_id,
                    title=article.title,
                    excerpt=article.excerpt,
                    score=article.score,
                    category_id=article.category_id,
                )
                for article in retrieved_articles
            ],
            classification_explanation=classification.explanation,
            priority_explanation=priority_result.explanation,
        )

    def _generate_response(
        self,
        generation_input: TicketResponseGenerationInput,
    ) -> TicketResponseGenerationResult:
        try:
            return self.ai_response_provider.generate_ticket_response(generation_input)
        except Exception as exc:
            if self.ai_response_provider.provider_name == "mock":
                raise

            logger.warning(
                "AI generation failed for provider '%s'; falling back to mock provider: %s",
                self.ai_response_provider.provider_name,
                exc,
            )
            return self.fallback_ai_response_provider.generate_ticket_response(
                generation_input
            )

    def _to_generated_answer(
        self,
        generation_result: TicketResponseGenerationResult,
        retrieved_articles: list[RagRetrievedArticle],
    ) -> GeneratedAnswer:
        return GeneratedAnswer(
            response_text=generation_result.email_body,
            model_name=generation_result.model_name,
            provider_name=generation_result.provider_name,
            sources_used=self._serialize_sources_metadata(
                generation_result,
                retrieved_articles,
            ),
        )

    def _serialize_sources_metadata(
        self,
        generation_result: TicketResponseGenerationResult,
        retrieved_articles: list[RagRetrievedArticle],
    ) -> str | None:
        payload = {
            "subject": generation_result.subject,
            "requires_human_review": generation_result.requires_human_review,
            "limitations": generation_result.limitations,
            "sources": [
                {
                    "article_id": article.article_id,
                    "title": article.title,
                    "score": article.score,
                    "used_by_model": article.article_id in set(generation_result.used_sources),
                    "excerpt": article.excerpt,
                }
                for article in retrieved_articles
            ],
        }
        return json.dumps(payload, ensure_ascii=False)
