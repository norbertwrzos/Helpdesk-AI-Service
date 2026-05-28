from datetime import datetime

from pydantic import BaseModel

from app.models.ticket import TicketSource, TicketStatus


class TicketBase(BaseModel):
    title: str
    description: str


class TicketCreate(TicketBase):
    category_id: int | None = None
    priority_id: int | None = None
    source: TicketSource = TicketSource.manual
    requester_email: str | None = None
    requester_name: str | None = None


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None
    category_id: int | None = None
    priority_id: int | None = None
    assigned_agent_name: str | None = None
    agent_response: str | None = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    source: TicketSource
    category_id: int | None
    priority_id: int | None
    requester_email: str | None
    requester_name: str | None
    assigned_agent_name: str | None
    agent_response: str | None
    classification_confidence: float | None
    priority_confidence: float | None
    classification_explanation: str | None
    priority_explanation: str | None
    email_sender: str | None
    email_subject: str | None
    email_message_id: str | None
    email_received_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
