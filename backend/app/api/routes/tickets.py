from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.rag import RagRetrievedArticle
from app.services.rag_retriever import RagRetriever
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.services import ticket_service

router = APIRouter()
_rag_retriever = RagRetriever()


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


@router.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)) -> Response:
    ticket_service.delete_ticket(db, ticket_id)
    return Response(status_code=204)


@router.post(
    "/tickets/{ticket_id}/retrieve-context",
    response_model=list[RagRetrievedArticle],
)
def retrieve_ticket_context(
    ticket_id: int,
    top_k: int | None = Query(default=None, ge=1, le=20),
    db: Session = Depends(get_db),
) -> list[RagRetrievedArticle]:
    ticket = ticket_service.get_ticket(db, ticket_id)
    return _rag_retriever.retrieve_for_ticket(db, ticket, top_k=top_k)
