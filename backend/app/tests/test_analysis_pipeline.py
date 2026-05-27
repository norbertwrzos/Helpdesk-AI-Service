import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.priority import Priority
from app.models.ticket import Ticket, TicketStatus, TicketSource


def _seed_base_data(db: Session) -> tuple[int, int]:
    """Dodaje kategorię i priorytet, zwraca ich id."""
    cat = Category(name="Sieć i VPN", description="Sieć")
    db.add(cat)
    pri = Priority(name="Wysoki", level=3, description="Wysoki priorytet")
    db.add(pri)
    db.flush()
    db.commit()
    return cat.id, pri.id


def _create_ticket(db: Session, title: str = "Nie działa VPN") -> Ticket:
    ticket = Ticket(
        title=title,
        description="Klient VPN nie łączy się z siecią firmową.",
        status=TicketStatus.new,
        source=TicketSource.manual,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


class TestAnalysisPipelineIntegration:
    def test_analyze_assigns_category(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        response = client.post(f"/tickets/{ticket.id}/analyze")
        assert response.status_code == 200
        data = response.json()
        assert data["classification"]["category_name"] is not None

    def test_analyze_assigns_priority(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        response = client.post(f"/tickets/{ticket.id}/analyze")
        assert response.status_code == 200
        data = response.json()
        assert data["priority"]["priority_name"] is not None

    def test_analyze_returns_ai_response(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        response = client.post(f"/tickets/{ticket.id}/analyze")
        assert response.status_code == 200
        data = response.json()
        assert data["ai_response"]["response_text"]

    def test_analyze_sets_status_answered(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        client.post(f"/tickets/{ticket.id}/analyze")
        db.refresh(ticket)
        assert ticket.status == TicketStatus.answered

    def test_analyze_saves_ai_response_to_db(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        client.post(f"/tickets/{ticket.id}/analyze")

        from app.models.ai_response import AIResponse
        saved = db.query(AIResponse).filter(AIResponse.ticket_id == ticket.id).first()
        assert saved is not None
        assert saved.response_text

    def test_analyze_returns_404_for_missing_ticket(self, client: TestClient, db: Session):
        response = client.post("/tickets/99999/analyze")
        assert response.status_code == 404

    def test_analyze_stores_confidence_on_ticket(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        client.post(f"/tickets/{ticket.id}/analyze")
        db.refresh(ticket)
        assert ticket.classification_confidence is not None
        assert ticket.priority_confidence is not None

    def test_analyze_stores_explanation_on_ticket(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        client.post(f"/tickets/{ticket.id}/analyze")
        db.refresh(ticket)
        assert ticket.classification_explanation
        assert ticket.priority_explanation


class TestAIResponsesEndpoint:
    def test_list_ai_responses_empty(self, client: TestClient, db: Session):
        ticket = _create_ticket(db)
        response = client.get(f"/tickets/{ticket.id}/ai-responses")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_ai_responses_after_analysis(self, client: TestClient, db: Session):
        _seed_base_data(db)
        ticket = _create_ticket(db)

        client.post(f"/tickets/{ticket.id}/analyze")
        response = client.get(f"/tickets/{ticket.id}/ai-responses")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["ticket_id"] == ticket.id
        assert data[0]["response_text"]
