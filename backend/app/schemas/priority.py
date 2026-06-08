from datetime import datetime

from pydantic import BaseModel, Field


class PriorityCreate(BaseModel):
    name: str
    level: int = Field(ge=1, le=4)
    description: str | None = None


class PriorityUpdate(BaseModel):
    name: str | None = None
    level: int | None = Field(default=None, ge=1, le=4)
    description: str | None = None


class PriorityResponse(BaseModel):
    id: int
    name: str
    level: int
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
