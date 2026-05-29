"""
EmailImporter — importuje wiadomości e-mail z serwera IMAP i tworzy zgłoszenia.

Przepływ:
  1. Sprawdź EMAIL_IMPORT_ENABLED.
  2. Połącz się z serwerem IMAP.
  3. Zaloguj się i wybierz folder INBOX.
  4. Pobierz listę wiadomości (z ograniczeniem `limit`).
  5. Dla każdej wiadomości:
     a. Parsuj przez EmailParser.
     b. Sprawdź duplikat (email_message_id).
     c. Utwórz Ticket (source=email) lub zapisz log "skipped".
     d. Opcjonalnie uruchom AnalysisPipeline.
  6. Zapisuj EmailImportLog dla każdej wiadomości.
  7. Błąd jednej wiadomości nie przerywa importu reszty.
  8. Zamknij połączenie IMAP.
  9. Zwróć EmailImportRunResponse ze statystykami.
"""

import imaplib
import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.email_import_log import EmailImportLog
from app.models.ticket import Ticket, TicketSource, TicketStatus
from app.schemas.email_import import EmailImportLogResponse, EmailImportRunResponse
from app.services.email_parser import EmailParser

logger = logging.getLogger(__name__)


class EmailImporter:
    """Importuje wiadomości e-mail z serwera IMAP do bazy danych jako zgłoszenia."""

    def __init__(self) -> None:
        self.parser = EmailParser()

    def import_messages(
        self,
        db: Session,
        limit: int = 10,
        analyze_imported: bool = True,
    ) -> EmailImportRunResponse:
        """
        Główna metoda importu.

        Parametry:
            db: sesja bazy danych SQLAlchemy,
            limit: maksymalna liczba wiadomości do przetworzenia,
            analyze_imported: czy uruchamiać AnalysisPipeline po imporcie.
        """
        if not settings.EMAIL_IMPORT_ENABLED:
            logger.info("Import e-mail jest wyłączony (EMAIL_IMPORT_ENABLED=false).")
            return EmailImportRunResponse(
                imported_count=0,
                skipped_count=0,
                error_count=0,
                analyzed_count=0,
                logs=[],
            )

        imported_count = 0
        skipped_count = 0
        error_count = 0
        analyzed_count = 0
        logs: list[EmailImportLog] = []

        imap: imaplib.IMAP4 | None = None
        try:
            imap = self._connect()
            imap.login(settings.EMAIL_IMAP_USERNAME, settings.EMAIL_IMAP_PASSWORD)
            imap.select(settings.EMAIL_FOLDER)

            _, message_numbers = imap.search(None, "ALL")
            ids = message_numbers[0].split()
            # IMAP returns sequence numbers oldest -> newest; import the newest
            # messages first so fresh test emails are not starved by old mail.
            ids = ids[-limit:]
            logger.info(
                "Znaleziono %d wiadomości w skrzynce %s (limit: %d).",
                len(ids),
                settings.EMAIL_FOLDER,
                limit,
            )

            for num in ids:
                log = self._process_message(
                    imap=imap,
                    num=num,
                    db=db,
                    analyze_imported=analyze_imported,
                )
                if log.status == "imported":
                    imported_count += 1
                    if log.error_message and log.error_message.startswith(
                        "Analiza nie powiodła się"
                    ):
                        pass  # import był poprawny, analiza opcjonalna
                    else:
                        # sprawdź czy analiza się powiodła (brak error_message)
                        analyzed_count += (
                            1
                            if analyze_imported and not log.error_message
                            else 0
                        )
                elif log.status == "skipped":
                    skipped_count += 1
                else:
                    error_count += 1
                logs.append(log)

        except Exception as exc:
            logger.error("Błąd połączenia z serwerem IMAP: %s", exc)
            err_log = EmailImportLog(
                status="error",
                error_message=f"Błąd połączenia IMAP: {exc}",
            )
            db.add(err_log)
            db.commit()
            db.refresh(err_log)
            logs.append(err_log)
            error_count += 1
        finally:
            if imap is not None:
                try:
                    imap.close()
                    imap.logout()
                except Exception:
                    pass

        return EmailImportRunResponse(
            imported_count=imported_count,
            skipped_count=skipped_count,
            error_count=error_count,
            analyzed_count=analyzed_count,
            logs=[EmailImportLogResponse.model_validate(log) for log in logs],
        )

    # ------------------------------------------------------------------
    # Metody prywatne
    # ------------------------------------------------------------------

    def _connect(self) -> imaplib.IMAP4:
        if settings.EMAIL_IMAP_USE_SSL:
            return imaplib.IMAP4_SSL(
                settings.EMAIL_IMAP_HOST, settings.EMAIL_IMAP_PORT
            )
        return imaplib.IMAP4(settings.EMAIL_IMAP_HOST, settings.EMAIL_IMAP_PORT)

    def _process_message(
        self,
        imap: imaplib.IMAP4,
        num: bytes,
        db: Session,
        analyze_imported: bool,
    ) -> EmailImportLog:
        """
        Przetwarza jedną wiadomość.
        Zwraca EmailImportLog z wynikiem (imported / skipped / error).
        Błąd pojedynczej wiadomości jest zapisywany w logu, nie przerywa importu.
        """
        try:
            _, msg_data = imap.fetch(num, "(RFC822)")
            raw: bytes = msg_data[0][1]  # type: ignore[index]

            parsed = self.parser.parse(raw)

            # Deduplikacja na podstawie email_message_id
            existing = (
                db.query(Ticket)
                .filter(Ticket.email_message_id == parsed.message_id)
                .first()
            )
            if existing:
                log = EmailImportLog(
                    message_id=parsed.message_id,
                    sender=parsed.sender,
                    subject=parsed.subject,
                    status="skipped",
                    ticket_id=existing.id,
                )
                db.add(log)
                db.commit()
                db.refresh(log)
                logger.info(
                    "Wiadomość %s pominięta (duplikat, ticket_id=%d).",
                    parsed.message_id,
                    existing.id,
                )
                return log

            # Utwórz nowe zgłoszenie
            ticket = Ticket(
                title=parsed.subject,
                description=parsed.body,
                source=TicketSource.email,
                status=TicketStatus.open,
                requester_email=parsed.sender,
                email_sender=parsed.sender,
                email_subject=parsed.subject,
                email_message_id=parsed.message_id,
                email_received_at=parsed.received_at,
            )
            db.add(ticket)
            db.flush()

            log = EmailImportLog(
                message_id=parsed.message_id,
                sender=parsed.sender,
                subject=parsed.subject,
                status="imported",
                ticket_id=ticket.id,
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            logger.info(
                "Zaimportowano wiadomość %s jako ticket_id=%d.",
                parsed.message_id,
                ticket.id,
            )

            # Opcjonalna analiza AI
            if analyze_imported:
                self._run_analysis(ticket.id, db, log)

            return log

        except Exception as exc:
            logger.error("Błąd przetwarzania wiadomości %s: %s", num, exc)
            db.rollback()
            err_log = EmailImportLog(
                status="error",
                error_message=str(exc),
            )
            db.add(err_log)
            db.commit()
            db.refresh(err_log)
            return err_log

    def _run_analysis(
        self, ticket_id: int, db: Session, log: EmailImportLog
    ) -> None:
        """Uruchamia AnalysisPipeline. Błąd analizy nie unieważnia importu."""
        try:
            from app.services.analysis_pipeline import AnalysisPipeline

            pipeline = AnalysisPipeline()
            pipeline.analyze_ticket(ticket_id, db)
            logger.info("Analiza zgłoszenia %d zakończona pomyślnie.", ticket_id)
        except Exception as exc:
            logger.warning(
                "Analiza zgłoszenia %d nie powiodła się: %s", ticket_id, exc
            )
            log.error_message = f"Analiza nie powiodła się: {exc}"
            db.commit()
