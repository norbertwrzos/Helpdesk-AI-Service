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


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None
    category_id: int | None = None
    priority_id: int | None = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    source: TicketSource
    category_id: int | None
    priority_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
