from __future__ import annotations

from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.knowledge_article_embedding import KnowledgeArticleEmbedding
from app.models.ticket import Ticket, TicketSource, TicketStatus


def _seed_context(db) -> Ticket:
    category = Category(name="Sieć i VPN", description="Problemy sieciowe")
    db.add(category)
    db.flush()

    article = KnowledgeArticle(
        title="VPN nie działa",
        content="Sprawdź połączenie internetowe, klienta VPN i dane logowania.",
        category_id=category.id,
        tags="vpn, połączenie",
    )
    db.add(article)

    ticket = Ticket(
        title="Problem z VPN",
        description="Nie mogę połączyć się z siecią firmową przez VPN.",
        status=TicketStatus.open,
        source=TicketSource.manual,
        category_id=category.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def test_post_knowledge_search_returns_articles(client, db):
    _seed_context(db)

    response = client.post(
        "/knowledge/search",
        json={"query": "Nie działa VPN, problem z połączeniem", "top_k": 5},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "VPN nie działa"


def test_post_knowledge_reindex_creates_embeddings(client, db):
    ticket = _seed_context(db)

    response = client.post("/knowledge/reindex", json={"force": False})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_articles"] == 1
    assert payload["indexed"] == 1

    saved = (
        db.query(KnowledgeArticleEmbedding)
        .join(KnowledgeArticle, KnowledgeArticle.id == KnowledgeArticleEmbedding.article_id)
        .filter(KnowledgeArticle.title == "VPN nie działa")
        .first()
    )
    assert saved is not None
    assert ticket.id is not None


def test_post_ticket_retrieve_context_returns_articles(client, db):
    ticket = _seed_context(db)

    response = client.post(f"/tickets/{ticket.id}/retrieve-context")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["article_id"] > 0