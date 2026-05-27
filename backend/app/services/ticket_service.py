from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ticket import Ticket, TicketStatus
from app.schemas.ticket import TicketCreate, TicketUpdate


def get_tickets(db: Session) -> list[Ticket]:
    return db.query(Ticket).all()


def get_ticket(db: Session, ticket_id: int) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )
    return ticket


def create_ticket(db: Session, data: TicketCreate) -> Ticket:
    ticket = Ticket(
        title=data.title,
        description=data.description,
        status=TicketStatus.new,
        source=data.source,
        category_id=data.category_id,
        priority_id=data.priority_id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def update_ticket(db: Session, ticket_id: int, data: TicketUpdate) -> Ticket:
    ticket = get_ticket(db, ticket_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket
