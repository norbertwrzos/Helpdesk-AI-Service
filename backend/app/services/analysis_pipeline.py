"""
AnalysisPipeline — koordynuje pełny proces analizy zgłoszenia.

Kolejność kroków:
1. Pobierz zgłoszenie (404 jeśli nie istnieje).
2. Pobierz kategorie, priorytety i artykuły bazy wiedzy.
3. Uruchom ClassificationService.
4. Uruchom PriorityAnalysisService.
5. Zaktualizuj zgłoszenie o wyniki klasyfikacji.
6. Uruchom SimilarityService.
7. Uruchom MockAIGenerator.
8. Zapisz AIResponse w bazie.
9. Ustaw status zgłoszenia na ai_reviewed.
10. Zatwierdź wszystkie zmiany.
11. Zapisz wszystkie zmiany.
12. Zwróć AnalysisResult.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ai_response import AIResponse
from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.priority import Priority
from app.models.ticket import Ticket, TicketStatus
from app.schemas.analysis import AnalysisResult
from app.services.ai_generator import MockAIGenerator
from app.services.classification_service import ClassificationService
from app.services.priority_analysis_service import PriorityAnalysisService
from app.services.similarity_service import SimilarityService


class AnalysisPipeline:
    """
    Koordynuje pełny proces analizy zgłoszenia.

    Każdy komponent (ClassificationService, PriorityAnalysisService,
    SimilarityService, MockAIGenerator) jest wstrzykiwany przez konstruktor,
    co ułatwia testy jednostkowe i wymianę na właściwe implementacje AI/NLP.

    Po zapisaniu wyniku analizy zgłoszenie otrzymuje status `ai_reviewed`.
    """

    def __init__(
        self,
        classifier: ClassificationService | None = None,
        priority_analyzer: PriorityAnalysisService | None = None,
        similarity: SimilarityService | None = None,
        ai_generator: MockAIGenerator | None = None,
    ) -> None:
        self.classifier = classifier or ClassificationService()
        self.priority_analyzer = priority_analyzer or PriorityAnalysisService()
        self.similarity = similarity or SimilarityService()
        self.ai_generator = ai_generator or MockAIGenerator()

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
        similar_articles = self.similarity.find_similar(
            title=ticket.title,
            description=ticket.description,
            articles=articles,
            classification_category_id=classification.category_id,
        )

        # 8. Generowanie odpowiedzi AI
        generated = self.ai_generator.generate(
            ticket=ticket,
            classification=classification,
            priority=priority_result,
            similar_articles=similar_articles,
        )

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
