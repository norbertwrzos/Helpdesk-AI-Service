"""
TicketMessageService — obsługa wiadomości w ramach konwersacji zgłoszenia.

Pozwala pobierać historię wiadomości i dodawać nowe wiadomości
do zgłoszenia przez agenta lub użytkownika końcowego.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.ticket import Ticket
from app.models.ticket_message import TicketMessage
from app.schemas.ticket_message import TicketMessageCreate


def get_messages_for_ticket(db: Session, ticket_id: int) -> list[TicketMessage]:
    """
    Zwraca wszystkie wiadomości dla zgłoszenia posortowane rosnąco po dacie.

    Raises:
        HTTPException 404: jeśli zgłoszenie nie istnieje.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    return (
        db.query(TicketMessage)
        .filter(TicketMessage.ticket_id == ticket_id)
        .order_by(TicketMessage.created_at.asc())
        .all()
    )


def create_message_for_ticket(
    db: Session, ticket_id: int, payload: TicketMessageCreate
) -> TicketMessage:
    """
    Dodaje nową wiadomość do zgłoszenia.

    Raises:
        HTTPException 404: jeśli zgłoszenie nie istnieje.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    message = TicketMessage(
        ticket_id=ticket_id,
        author_role=payload.author_role,
        author_name=payload.author_name.strip(),
        author_email=payload.author_email,
        message_text=payload.message_text.strip(),
        message_type="public",
    )
    db.add(message)

    # Każda nowa wiadomość aktualizuje znacznik modyfikacji zgłoszenia.
    ticket.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(message)
    return message
