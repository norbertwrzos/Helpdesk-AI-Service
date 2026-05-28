from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.quality_metrics import QualityMetricsResponse
from app.services.quality_metrics_service import QualityMetricsService

router = APIRouter()
_service = QualityMetricsService()


@router.get(
    "/quality/ai-responses",
    response_model=QualityMetricsResponse,
    summary="Podstawowe metryki jakości odpowiedzi AI",
)
def get_ai_response_quality_metrics(
    db: Session = Depends(get_db),
) -> QualityMetricsResponse:
    """
    Zwraca podstawowe metryki jakości odpowiedzi AI:
    - łączna liczba odpowiedzi AI,
    - liczba ocen,
    - średnia ocena,
    - pokrycie feedbackiem,
    - liczba odpowiedzi pomocnych / niepomocnych,
    - rozkład ocen 1-5.
    """
    return _service.get_ai_response_metrics(db)
