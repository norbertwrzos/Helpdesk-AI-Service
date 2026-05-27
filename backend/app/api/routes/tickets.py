from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.services import ticket_service

router = APIRouter()


@router.get("/tickets", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)) -> list[TicketResponse]:
    return ticket_service.get_tickets(db)


@router.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(
    data: TicketCreate, db: Session = Depends(get_db)
) -> TicketResponse:
    return ticket_service.create_ticket(db, data)


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)) -> TicketResponse:
    return ticket_service.get_ticket(db, ticket_id)


@router.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int, data: TicketUpdate, db: Session = Depends(get_db)
) -> TicketResponse:
    return ticket_service.update_ticket(db, ticket_id, data)
