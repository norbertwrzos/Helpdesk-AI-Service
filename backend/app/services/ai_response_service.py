from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ai_response import AIResponse
from app.models.feedback import Feedback
from app.models.ticket import Ticket
from app.schemas.ai_response import AIResponseResponse
from app.schemas.feedback import FeedbackResponse


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

        result = []
        for resp in ai_responses:
            feedback_row = (
                db.query(Feedback)
                .filter(Feedback.ai_response_id == resp.id)
                .first()
            )
            feedback = FeedbackResponse.model_validate(feedback_row) if feedback_row else None
            response_data = AIResponseResponse.model_validate(resp)
            response_data.feedback = feedback
            result.append(response_data)

        return result
