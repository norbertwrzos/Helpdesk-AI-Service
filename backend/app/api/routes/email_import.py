from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.scheduler import scheduler_status
from app.models.email_import_log import EmailImportLog
from app.schemas.email_import import (
    EmailImportLogResponse,
    EmailImportRunRequest,
    EmailImportRunResponse,
)
from app.services.email_importer import EmailImporter

router = APIRouter()


@router.get(
    "/email/import/scheduler",
    summary="Stan schedulera importu e-mail",
    description="Zwraca czy scheduler działa, interwał oraz ustawienia automatycznej analizy.",
)
def get_scheduler_status() -> dict:
    return scheduler_status()


@router.post(
    "/email/import/run",
    response_model=EmailImportRunResponse,
    summary="Uruchom import wiadomości e-mail",
    description=(
        "Pobiera wiadomości z testowej skrzynki IMAP (GreenMail) "
        "i tworzy na ich podstawie zgłoszenia techniczne. "
        "Opcjonalnie uruchamia AnalysisPipeline dla nowych zgłoszeń."
    ),
)
def run_email_import(
    request: EmailImportRunRequest,
    db: Session = Depends(get_db),
) -> EmailImportRunResponse:
    importer = EmailImporter()
    return importer.import_messages(
        db=db,
        limit=request.limit,
        analyze_imported=request.analyze_imported,
    )


@router.get(
    "/email/import/logs",
    response_model=list[EmailImportLogResponse],
    summary="Lista logów importu e-mail",
    description="Zwraca historię logów importu wiadomości e-mail. Najnowsze jako pierwsze.",
)
def get_email_import_logs(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
) -> list[EmailImportLogResponse]:
    logs = (
        db.query(EmailImportLog)
        .order_by(EmailImportLog.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return logs


@router.get(
    "/email/import/logs/{log_id}",
    response_model=EmailImportLogResponse,
    summary="Szczegóły logu importu e-mail",
)
def get_email_import_log(
    log_id: int,
    db: Session = Depends(get_db),
) -> EmailImportLogResponse:
    log = db.query(EmailImportLog).filter(EmailImportLog.id == log_id).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log importu o ID {log_id} nie został znaleziony.",
        )
    return log
