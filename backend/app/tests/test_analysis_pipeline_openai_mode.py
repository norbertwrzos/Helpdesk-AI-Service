import json

from sqlalchemy.orm import Session

from app.models.ai_response import AIResponse
from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.priority import Priority
from app.models.ticket import Ticket, TicketSource, TicketStatus
from app.services.ai_generation.base import BaseAIResponseProvider
from app.services.ai_generation.schemas import (
    TicketResponseGenerationInput,
    TicketResponseGenerationResult,
)
from app.services.analysis_pipeline import AnalysisPipeline
from app.services.embeddings.mock_embedding_provider import MockEmbeddingProvider
from app.services.rag_retriever import RagRetriever


class StubOpenAIProvider(BaseAIResponseProvider):
    provider_name = "openai"

    def __init__(self) -> None:
        super().__init__(model_name="gpt-4o-mini")

    def generate_ticket_response(
        self,
        data: TicketResponseGenerationInput,
    ) -> TicketResponseGenerationResult:
        used_sources = [article.article_id for article in data.retrieved_articles[:1]]
        return TicketResponseGenerationResult(
            subject=f"Re: {data.title}",
            email_body=(
                "Dzień dobry,\n\n"
                "przygotowaliśmy propozycję dalszych kroków dla zgłoszenia VPN.\n\n"
                "Pozdrawiam,\n"
                f"{data.agent_name}"
            ),
            confidence=0.82,
            used_sources=used_sources,
            requires_human_review=True,
            limitations="Wymaga weryfikacji przez agenta.",
            model_name=self.model_name,
            provider_name=self.provider_name,
            raw_response='{"subject":"Re"}',
        )


class FailingOpenAIProvider(BaseAIResponseProvider):
    provider_name = "openai"

    def __init__(self) -> None:
        super().__init__(model_name="gpt-4o-mini")

    def generate_ticket_response(
        self,
        data: TicketResponseGenerationInput,
    ) -> TicketResponseGenerationResult:
        raise RuntimeError("OpenAI upstream failure")


def _seed_pipeline_data(db: Session) -> Ticket:
    category = Category(name="Sieć i VPN", description="Problemy sieciowe")
    priority = Priority(name="Wysoki", level=3, description="Wysoki priorytet")
    db.add(category)
    db.add(priority)
    db.flush()

    article = KnowledgeArticle(
        title="Diagnostyka VPN",
        content="Sprawdź połączenie internetowe, klienta VPN i poprawność danych logowania.",
        category_id=category.id,
        tags="vpn, sieć",
    )
    db.add(article)

    ticket = Ticket(
        title="Nie działa VPN",
        description="Nie mogę połączyć się z siecią firmową.",
        status=TicketStatus.open,
        source=TicketSource.manual,
        assigned_agent_name="Norbert",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def test_pipeline_saves_openai_response_with_rag_sources(db: Session):
    ticket = _seed_pipeline_data(db)
    pipeline = AnalysisPipeline(
        ai_response_provider=StubOpenAIProvider(),
        rag_retriever=RagRetriever(provider=MockEmbeddingProvider()),
    )

    result = pipeline.analyze_ticket(ticket.id, db)
    saved = db.query(AIResponse).filter(AIResponse.ticket_id == ticket.id).first()

    assert result.ai_response.provider_name == "openai"
    assert saved is not None
    assert saved.provider_name == "openai"
    assert saved.model_name == "gpt-4o-mini"

    metadata = json.loads(saved.sources_used)
    assert metadata["sources"]
    assert metadata["sources"][0]["title"] == "Diagnostyka VPN"
    assert metadata["sources"][0]["used_by_model"] is True

    db.refresh(ticket)
    assert ticket.status == TicketStatus.ai_reviewed


def test_pipeline_falls_back_to_mock_when_openai_provider_fails(db: Session):
    ticket = _seed_pipeline_data(db)
    pipeline = AnalysisPipeline(
        ai_response_provider=FailingOpenAIProvider(),
        rag_retriever=RagRetriever(provider=MockEmbeddingProvider()),
    )

    result = pipeline.analyze_ticket(ticket.id, db)
    saved = db.query(AIResponse).filter(AIResponse.ticket_id == ticket.id).first()

    assert result.ai_response.provider_name == "mock"
    assert saved is not None
    assert saved.provider_name == "mock"