from pydantic import BaseModel


class QualityMetricsResponse(BaseModel):
    total_ai_responses: int
    total_tickets_analyzed: int
    total_feedback: int
    average_rating: float | None
    helpful_count: int
    not_helpful_count: int
    feedback_coverage_percent: float
    rating_distribution: dict[str, int]
    responses_without_feedback: int
