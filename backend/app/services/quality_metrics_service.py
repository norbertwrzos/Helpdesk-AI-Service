from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ai_response import AIResponse
from app.models.feedback import Feedback
from app.schemas.quality_metrics import QualityMetricsResponse


class QualityMetricsService:
    """Serwis liczący podstawowe metryki jakości odpowiedzi AI."""

    def get_ai_response_metrics(self, db: Session) -> QualityMetricsResponse:
        total_ai_responses: int = db.query(func.count(AIResponse.id)).scalar() or 0
        total_tickets_analyzed: int = (
            db.query(func.count(func.distinct(AIResponse.ticket_id))).scalar() or 0
        )
        total_feedback: int = db.query(func.count(Feedback.id)).scalar() or 0

        avg_rating_raw = db.query(func.avg(Feedback.rating)).scalar()
        average_rating = float(round(avg_rating_raw, 2)) if avg_rating_raw is not None else None

        helpful_count: int = (
            db.query(func.count(Feedback.id))
            .filter(Feedback.is_helpful.is_(True))
            .scalar()
        ) or 0

        not_helpful_count: int = (
            db.query(func.count(Feedback.id))
            .filter(Feedback.is_helpful.is_(False))
            .scalar()
        ) or 0

        feedback_coverage_percent = (
            round(total_feedback / total_ai_responses * 100, 1)
            if total_ai_responses > 0
            else 0.0
        )

        responses_without_feedback = total_ai_responses - total_feedback

        # Rozkład ocen 1-5
        rating_distribution: dict[str, int] = {str(i): 0 for i in range(1, 6)}
        rows = (
            db.query(Feedback.rating, func.count(Feedback.id))
            .group_by(Feedback.rating)
            .all()
        )
        for rating_value, count in rows:
            rating_distribution[str(rating_value)] = count

        return QualityMetricsResponse(
            total_ai_responses=total_ai_responses,
            total_tickets_analyzed=total_tickets_analyzed,
            total_feedback=total_feedback,
            average_rating=average_rating,
            helpful_count=helpful_count,
            not_helpful_count=not_helpful_count,
            feedback_coverage_percent=feedback_coverage_percent,
            rating_distribution=rating_distribution,
            responses_without_feedback=responses_without_feedback,
        )
