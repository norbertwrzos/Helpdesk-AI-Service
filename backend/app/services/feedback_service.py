from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ai_response import AIResponse
from app.models.feedback import Feedback
from app.models.ticket import Ticket
from app.schemas.feedback import FeedbackCreate, FeedbackResponse


class FeedbackService:
    """
    Serwis obsługujący oceny odpowiedzi AI.

    MVP: jedna aktualna ocena per AIResponse.
    Ponowne przesłanie feedbacku dla tego samego ai_response_id
    aktualizuje istniejący rekord.
    """

    def create_or_update_feedback(
        self,
        db: Session,
        ticket_id: int,
        payload: FeedbackCreate,
    ) -> FeedbackResponse:
        # Weryfikacja: ticket istnieje
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Zgłoszenie nie zostało znalezione.")

        # Weryfikacja: AIResponse istnieje
        ai_response = (
            db.query(AIResponse)
            .filter(AIResponse.id == payload.ai_response_id)
            .first()
        )
        if not ai_response:
            raise HTTPException(
                status_code=404,
                detail="Odpowiedź AI nie została znaleziona.",
            )

        # Weryfikacja: AIResponse należy do tego ticketu
        if ai_response.ticket_id != ticket_id:
            raise HTTPException(
                status_code=400,
                detail="Odpowiedź AI nie należy do wskazanego zgłoszenia.",
            )

        # Utwórz lub zaktualizuj feedback
        existing = (
            db.query(Feedback)
            .filter(Feedback.ai_response_id == payload.ai_response_id)
            .first()
        )

        if existing:
            existing.rating = payload.rating
            if payload.is_helpful is not None:
                existing.is_helpful = payload.is_helpful
            if payload.comment is not None:
                existing.comment = payload.comment
            db.commit()
            db.refresh(existing)
            return FeedbackResponse.model_validate(existing)

        feedback = Feedback(
            ticket_id=ticket_id,
            ai_response_id=payload.ai_response_id,
            rating=payload.rating,
            is_helpful=payload.is_helpful,
            comment=payload.comment,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return FeedbackResponse.model_validate(feedback)

    def get_feedback_for_ticket(
        self, db: Session, ticket_id: int
    ) -> list[FeedbackResponse]:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Zgłoszenie nie zostało znalezione.")

        feedbacks = (
            db.query(Feedback)
            .filter(Feedback.ticket_id == ticket_id)
            .order_by(Feedback.created_at.desc())
            .all()
        )
        return [FeedbackResponse.model_validate(f) for f in feedbacks]

    def get_feedback_for_ai_response(
        self, db: Session, ai_response_id: int
    ) -> FeedbackResponse | None:
        feedback = (
            db.query(Feedback)
            .filter(Feedback.ai_response_id == ai_response_id)
            .first()
        )
        if not feedback:
            return None
        return FeedbackResponse.model_validate(feedback)
