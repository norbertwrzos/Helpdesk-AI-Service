from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    ai_response_id: int
    rating: int = Field(..., ge=1, le=5)
    is_helpful: bool | None = None
    comment: str | None = None


class FeedbackUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    is_helpful: bool | None = None
    comment: str | None = None


class FeedbackResponse(BaseModel):
    id: int
    ticket_id: int
    ai_response_id: int
    rating: int
    is_helpful: bool | None
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
