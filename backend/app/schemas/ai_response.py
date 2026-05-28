from datetime import datetime

from pydantic import BaseModel

from app.schemas.feedback import FeedbackResponse


class AIResponseResponse(BaseModel):
    id: int
    ticket_id: int
    response_text: str
    model_name: str
    provider_name: str
    sources_used: str | None
    created_at: datetime
    feedback: FeedbackResponse | None = None

    model_config = {"from_attributes": True}
