from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.ticket_message import TicketMessageCreate, TicketMessageResponse
from app.services import ticket_message_service

router = APIRouter()


@router.get(
    "/tickets/{ticket_id}/messages",
    response_model=list[TicketMessageResponse],
    summary="Pobierz wiadomości zgłoszenia",
    description="Zwraca historię wiadomości dla zgłoszenia posortowaną chronologicznie rosnąco.",
)
def list_ticket_messages(
    ticket_id: int, db: Session = Depends(get_db)
) -> list[TicketMessageResponse]:
    return ticket_message_service.get_messages_for_ticket(db, ticket_id)


@router.post(
    "/tickets/{ticket_id}/messages",
    response_model=TicketMessageResponse,
    status_code=201,
    summary="Dodaj wiadomość do zgłoszenia",
    description=(
        "Dodaje nową wiadomość agenta lub użytkownika końcowego do zgłoszenia."
    ),
)
def create_ticket_message(
    ticket_id: int,
    payload: TicketMessageCreate,
    db: Session = Depends(get_db),
) -> TicketMessageResponse:
    return ticket_message_service.create_message_for_ticket(db, ticket_id, payload)
