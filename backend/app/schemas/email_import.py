from datetime import datetime

from pydantic import BaseModel


class EmailImportLogResponse(BaseModel):
    id: int
    message_id: str | None
    sender: str | None
    subject: str | None
    status: str
    ticket_id: int | None
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class EmailImportRunRequest(BaseModel):
    limit: int = 10
    analyze_imported: bool = True


class EmailImportRunResponse(BaseModel):
    imported_count: int
    skipped_count: int
    error_count: int
    analyzed_count: int
    logs: list[EmailImportLogResponse]


class ParsedEmail(BaseModel):
    """Wynik parsowania pojedynczej wiadomości e-mail."""

    message_id: str
    sender: str
    subject: str
    body: str
    received_at: datetime | None
