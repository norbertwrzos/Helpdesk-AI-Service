from datetime import datetime

from pydantic import BaseModel


class PriorityCreate(BaseModel):
    name: str
    level: int
    description: str | None = None


class PriorityResponse(BaseModel):
    id: int
    name: str
    level: int
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
