from pydantic import BaseModel


class ClassificationResult(BaseModel):
    category_id: int | None
    category_name: str
    confidence: float
    explanation: str


class PriorityResult(BaseModel):
    priority_id: int | None
    priority_name: str
    confidence: float
    explanation: str


class SimilarArticle(BaseModel):
    id: int
    title: str
    excerpt: str
    category_id: int | None
    score: float


class GeneratedAnswer(BaseModel):
    response_text: str
    model_name: str
    provider_name: str
    sources_used: str | None


class AnalysisResult(BaseModel):
    ticket_id: int
    classification: ClassificationResult
    priority: PriorityResult
    similar_articles: list[SimilarArticle]
    ai_response: GeneratedAnswer
