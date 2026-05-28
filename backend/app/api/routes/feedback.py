from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import FeedbackService

router = APIRouter()
_service = FeedbackService()


@router.post(
    "/tickets/{ticket_id}/feedback",
    response_model=FeedbackResponse,
    summary="Utwórz lub zaktualizuj ocenę odpowiedzi AI",
)
def create_or_update_feedback(
    ticket_id: int,
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
) -> FeedbackResponse:
    """
    Tworzy lub aktualizuje ocenę dla konkretnej odpowiedzi AI.
    Jeśli feedback dla ai_response_id już istnieje, zostaje zaktualizowany.
    """
    return _service.create_or_update_feedback(db, ticket_id, payload)


@router.get(
    "/tickets/{ticket_id}/feedback",
    response_model=list[FeedbackResponse],
    summary="Pobierz wszystkie oceny dla zgłoszenia",
)
def get_ticket_feedback(
    ticket_id: int,
    db: Session = Depends(get_db),
) -> list[FeedbackResponse]:
    """Zwraca wszystkie oceny odpowiedzi AI powiązane ze zgłoszeniem."""
    return _service.get_feedback_for_ticket(db, ticket_id)


@router.get(
    "/ai-responses/{ai_response_id}/feedback",
    response_model=FeedbackResponse | None,
    summary="Pobierz ocenę konkretnej odpowiedzi AI",
)
def get_ai_response_feedback(
    ai_response_id: int,
    db: Session = Depends(get_db),
) -> FeedbackResponse | None:
    """
    Zwraca ocenę dla konkretnej odpowiedzi AI.
    Jeśli ocena nie istnieje, zwraca null (HTTP 200).
    """
    return _service.get_feedback_for_ai_response(db, ai_response_id)
