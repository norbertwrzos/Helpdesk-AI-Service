from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TicketMessageCreate(BaseModel):
    message_text: str = Field(min_length=1)
    author_role: Literal["agent", "end_user"]
    author_name: str = Field(min_length=1)
    author_email: str | None = None

    @field_validator("message_text")
    @classmethod
    def message_text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Treść wiadomości nie może być pusta.")
        return v

    @field_validator("author_name")
    @classmethod
    def author_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Imię autora nie może być puste.")
        return v


class TicketMessageResponse(BaseModel):
    id: int
    ticket_id: int
    author_role: str
    author_name: str
    author_email: str | None
    message_text: str
    message_type: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
