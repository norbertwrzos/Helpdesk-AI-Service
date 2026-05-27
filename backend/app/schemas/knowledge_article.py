from datetime import datetime

from pydantic import BaseModel


class KnowledgeArticleBase(BaseModel):
    title: str
    content: str
    category_id: int | None = None
    tags: str | None = None


class KnowledgeArticleCreate(KnowledgeArticleBase):
    pass


class KnowledgeArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category_id: int | None = None
    tags: str | None = None


class KnowledgeArticleResponse(KnowledgeArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
