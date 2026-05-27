from datetime import datetime

from pydantic import BaseModel


class AIResponseResponse(BaseModel):
    id: int
    ticket_id: int
    response_text: str
    model_name: str
    provider_name: str
    sources_used: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
