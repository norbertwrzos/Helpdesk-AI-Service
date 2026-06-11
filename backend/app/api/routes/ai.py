from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.ai_response import AIResponse
from app.schemas.ai_response import AIResponseResponse
from app.schemas.analysis import AnalysisResult
from app.services.ai_response_service import AIResponseService
from app.services.analysis_pipeline import AnalysisPipeline

router = APIRouter()
_pipeline = AnalysisPipeline()
_ai_response_service = AIResponseService()


@router.post("/tickets/{ticket_id}/analyze", response_model=AnalysisResult)
def analyze_ticket(
    ticket_id: int, db: Session = Depends(get_db)
) -> AnalysisResult:
    """Uruchamia AnalysisPipeline dla wskazanego zgłoszenia."""
    return _pipeline.analyze_ticket(ticket_id, db)


@router.get(
    "/tickets/{ticket_id}/ai-responses",
    response_model=list[AIResponseResponse],
)
def list_ai_responses(
    ticket_id: int, db: Session = Depends(get_db)
) -> list[AIResponseResponse]:
    """Zwraca listę odpowiedzi AI dla zgłoszenia (od najnowszej)."""
    return _ai_response_service.get_ai_responses_for_ticket(db, ticket_id)


@router.get(
    "/ai-responses",
    response_model=list[AIResponseResponse],
    summary="Globalna lista ostatnich odpowiedzi AI",
)
def list_recent_ai_responses(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[AIResponseResponse]:
    """Zwraca ostatnie odpowiedzi AI ze wszystkich zgłoszeń."""
    rows = (
        db.query(AIResponse)
        .order_by(AIResponse.created_at.desc())
        .limit(limit)
        .all()
    )
    return [AIResponseResponse.model_validate(resp) for resp in rows]
