from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
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
    """Zwraca listę odpowiedzi AI dla zgłoszenia (od najnowszej) wraz z feedbackiem."""
    return _ai_response_service.get_ai_responses_for_ticket(db, ticket_id)
