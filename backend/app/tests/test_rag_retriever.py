from __future__ import annotations

from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.ticket import Ticket, TicketSource, TicketStatus
from app.services.embeddings.mock_embedding_provider import MockEmbeddingProvider
from app.services.rag_retriever import RagRetriever


def _seed_rag_data(db) -> Ticket:
    category = Category(name="Sieć i VPN", description="Problemy sieciowe")
    db.add(category)
    db.flush()

    article = KnowledgeArticle(
        title="Diagnostyka problemów z VPN",
        content="Jeśli VPN nie działa, sprawdź połączenie internetowe i poprawność danych logowania.",
        category_id=category.id,
        tags="vpn, sieć, dostęp",
    )
    db.add(article)

    ticket = Ticket(
        title="Nie działa VPN",
        description="Mam problem z połączeniem VPN i nie mogę zalogować się do sieci firmowej.",
        status=TicketStatus.open,
        source=TicketSource.manual,
        category_id=category.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def test_retriever_returns_articles_for_ticket(db):
    ticket = _seed_rag_data(db)
    retriever = RagRetriever(provider=MockEmbeddingProvider())

    result = retriever.retrieve_for_ticket(db, ticket)

    assert len(result) == 1
    assert result[0].title == "Diagnostyka problemów z VPN"
    assert result[0].source_type == "knowledge_article"


def test_retriever_falls_back_when_mock_provider_is_active(db):
    ticket = _seed_rag_data(db)
    retriever = RagRetriever(provider=MockEmbeddingProvider(), default_top_k=5)

    result = retriever.retrieve_for_ticket(db, ticket)

    assert result
    assert result[0].score > 0


def test_retriever_handles_missing_articles(db):
    ticket = Ticket(
        title="Nie działa VPN",
        description="Brak artykułów w bazie wiedzy.",
        status=TicketStatus.open,
        source=TicketSource.manual,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    retriever = RagRetriever(provider=MockEmbeddingProvider())
    result = retriever.retrieve_for_ticket(db, ticket)

    assert result == []