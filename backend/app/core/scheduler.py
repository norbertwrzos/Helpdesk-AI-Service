"""
Scheduler importu e-mail — uruchamia EmailImporter cyklicznie jako tło asyncio.

Konfiguracja (app/core/config.py / zmienne środowiskowe):
  EMAIL_IMPORT_ENABLED          — włącza/wyłącza scheduler (domyślnie True)
  EMAIL_POLL_INTERVAL_SECONDS   — odstęp między kolejnymi importami (domyślnie 60)
  EMAIL_AUTO_ANALYZE_IMPORTED   — czy analizować nowe zgłoszenia po imporcie (domyślnie True)
"""

import asyncio
import logging
from datetime import datetime, UTC

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.email_importer import EmailImporter

logger = logging.getLogger(__name__)

_scheduler_task: asyncio.Task | None = None


async def _email_import_loop() -> None:
    """Pętla działająca w tle — importuje e-maile co EMAIL_POLL_INTERVAL_SECONDS."""
    logger.info(
        "Scheduler importu e-mail uruchomiony "
        "(interwał: %ds, analiza: %s).",
        settings.EMAIL_POLL_INTERVAL_SECONDS,
        settings.EMAIL_AUTO_ANALYZE_IMPORTED,
    )
    while True:
        await asyncio.sleep(settings.EMAIL_POLL_INTERVAL_SECONDS)
        started_at = datetime.now(UTC)
        try:
            db = SessionLocal()
            try:
                importer = EmailImporter()
                result = importer.import_messages(
                    db=db,
                    analyze_imported=settings.EMAIL_AUTO_ANALYZE_IMPORTED,
                )
                if result.imported_count or result.error_count:
                    logger.info(
                        "Import e-mail: zaimportowano=%d, pominięto=%d, błędy=%d "
                        "(%.1fs).",
                        result.imported_count,
                        result.skipped_count,
                        result.error_count,
                        (datetime.now(UTC) - started_at).total_seconds(),
                    )
            finally:
                db.close()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Błąd podczas automatycznego importu e-mail.")


def start_scheduler() -> None:
    """Uruchamia pętlę importu jako task asyncio. Wywołać przy starcie aplikacji."""
    global _scheduler_task
    if not settings.EMAIL_IMPORT_ENABLED:
        logger.info("Scheduler importu e-mail wyłączony (EMAIL_IMPORT_ENABLED=false).")
        return
    _scheduler_task = asyncio.create_task(_email_import_loop(), name="email-import-scheduler")
    logger.info("Scheduler importu e-mail zarejestrowany.")


def stop_scheduler() -> None:
    """Zatrzymuje pętlę importu. Wywołać przy zamknięciu aplikacji."""
    global _scheduler_task
    if _scheduler_task and not _scheduler_task.done():
        _scheduler_task.cancel()
        logger.info("Scheduler importu e-mail zatrzymany.")
    _scheduler_task = None


def scheduler_status() -> dict:
    """Zwraca bieżący stan schedulera (używane przez endpoint /email/import/scheduler)."""
    running = (
        _scheduler_task is not None
        and not _scheduler_task.done()
        and not _scheduler_task.cancelled()
    )
    return {
        "enabled": settings.EMAIL_IMPORT_ENABLED,
        "running": running,
        "interval_seconds": settings.EMAIL_POLL_INTERVAL_SECONDS,
        "auto_analyze": settings.EMAIL_AUTO_ANALYZE_IMPORTED,
    }
