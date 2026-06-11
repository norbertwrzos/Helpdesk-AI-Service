from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ai_response import AIResponse
from app.models.ticket import Ticket
from app.schemas.ai_response import AIResponseResponse


class AIResponseService:
    """Serwis zarządzający historią odpowiedzi AI dla zgłoszeń."""

    def get_ai_responses_for_ticket(
        self, db: Session, ticket_id: int
    ) -> list[AIResponseResponse]:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Zgłoszenie nie zostało znalezione.")

        ai_responses = (
            db.query(AIResponse)
            .filter(AIResponse.ticket_id == ticket_id)
            .order_by(AIResponse.created_at.desc())
            .all()
        )

        return [AIResponseResponse.model_validate(resp) for resp in ai_responses]
