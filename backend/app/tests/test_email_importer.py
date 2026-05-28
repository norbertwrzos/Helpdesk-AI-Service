"""Testy jednostkowe EmailImporter (bez połączenia z prawdziwym serwerem IMAP)."""

import email.mime.text
from unittest.mock import MagicMock, patch

import pytest

from app.models.email_import_log import EmailImportLog
from app.models.ticket import Ticket, TicketSource, TicketStatus
from app.services.email_parser import ParsedEmail
from app.services.email_importer import EmailImporter


def _raw_email(
    subject: str = "Problem z VPN",
    body: str = "Nie mogę połączyć się z VPN.",
    sender: str = "user@example.com",
    message_id: str = "<vpn-001@example.com>",
) -> bytes:
    msg = email.mime.text.MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Date"] = "Wed, 28 May 2026 10:00:00 +0000"
    msg["Message-ID"] = message_id
    return msg.as_bytes()


@pytest.fixture()
def importer() -> EmailImporter:
    return EmailImporter()


class TestEmailImporterCreateTicket:
    """Testy tworzenia zgłoszenia z wiadomości e-mail."""

    def test_creates_ticket_from_parsed_email(self, importer: EmailImporter, db) -> None:
        raw = _raw_email()
        parsed = importer.parser.parse(raw)

        # Symuluj _process_message bez połączenia IMAP
        with patch.object(importer, "_connect") as mock_connect:
            imap_mock = MagicMock()
            mock_connect.return_value = imap_mock
            imap_mock.login.return_value = ("OK", [])
            imap_mock.select.return_value = ("OK", [])
            imap_mock.search.return_value = ("OK", [b"1"])
            imap_mock.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

            # Wyłącz automatyczną analizę, żeby nie wymagać danych bazowych
            with patch("app.services.email_importer.settings") as mock_settings:
                mock_settings.EMAIL_IMPORT_ENABLED = True
                mock_settings.EMAIL_IMAP_USE_SSL = False
                mock_settings.EMAIL_IMAP_HOST = "localhost"
                mock_settings.EMAIL_IMAP_PORT = 3143
                mock_settings.EMAIL_IMAP_USERNAME = "test@localhost"
                mock_settings.EMAIL_IMAP_PASSWORD = "test"
                mock_settings.EMAIL_FOLDER = "INBOX"

                result = importer.import_messages(db=db, limit=10, analyze_imported=False)

        assert result.imported_count == 1
        assert result.skipped_count == 0
        assert result.error_count == 0

        ticket = db.query(Ticket).filter(Ticket.email_message_id == "<vpn-001@example.com>").first()
        assert ticket is not None

    def test_ticket_has_source_email(self, importer: EmailImporter, db) -> None:
        raw = _raw_email(message_id="<source-test@example.com>")

        with patch.object(importer, "_connect") as mock_connect:
            imap_mock = MagicMock()
            mock_connect.return_value = imap_mock
            imap_mock.login.return_value = ("OK", [])
            imap_mock.select.return_value = ("OK", [])
            imap_mock.search.return_value = ("OK", [b"1"])
            imap_mock.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

            with patch("app.services.email_importer.settings") as mock_settings:
                mock_settings.EMAIL_IMPORT_ENABLED = True
                mock_settings.EMAIL_IMAP_USE_SSL = False
                mock_settings.EMAIL_IMAP_HOST = "localhost"
                mock_settings.EMAIL_IMAP_PORT = 3143
                mock_settings.EMAIL_IMAP_USERNAME = "test@localhost"
                mock_settings.EMAIL_IMAP_PASSWORD = "test"
                mock_settings.EMAIL_FOLDER = "INBOX"

                importer.import_messages(db=db, limit=10, analyze_imported=False)

        ticket = db.query(Ticket).filter(Ticket.email_message_id == "<source-test@example.com>").first()
        assert ticket is not None
        assert ticket.source == TicketSource.email

    def test_ticket_has_email_fields(self, importer: EmailImporter, db) -> None:
        raw = _raw_email(
            sender="jan.kowalski@firma.pl",
            subject="Błąd logowania",
            message_id="<fields-test@example.com>",
        )

        with patch.object(importer, "_connect") as mock_connect:
            imap_mock = MagicMock()
            mock_connect.return_value = imap_mock
            imap_mock.login.return_value = ("OK", [])
            imap_mock.select.return_value = ("OK", [])
            imap_mock.search.return_value = ("OK", [b"1"])
            imap_mock.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

            with patch("app.services.email_importer.settings") as mock_settings:
                mock_settings.EMAIL_IMPORT_ENABLED = True
                mock_settings.EMAIL_IMAP_USE_SSL = False
                mock_settings.EMAIL_IMAP_HOST = "localhost"
                mock_settings.EMAIL_IMAP_PORT = 3143
                mock_settings.EMAIL_IMAP_USERNAME = "test@localhost"
                mock_settings.EMAIL_IMAP_PASSWORD = "test"
                mock_settings.EMAIL_FOLDER = "INBOX"

                importer.import_messages(db=db, limit=10, analyze_imported=False)

        ticket = db.query(Ticket).filter(Ticket.email_message_id == "<fields-test@example.com>").first()
        assert ticket is not None
        assert ticket.email_sender == "jan.kowalski@firma.pl"
        assert ticket.email_subject == "Błąd logowania"
        assert ticket.email_message_id == "<fields-test@example.com>"


class TestEmailImporterDeduplication:
    """Testy deduplikacji — ten sam e-mail nie może tworzyć drugiego zgłoszenia."""

    def test_skips_duplicate_message_id(self, importer: EmailImporter, db) -> None:
        raw = _raw_email(message_id="<dup-001@example.com>")

        imap_mock = MagicMock()
        imap_mock.login.return_value = ("OK", [])
        imap_mock.select.return_value = ("OK", [])
        imap_mock.search.return_value = ("OK", [b"1"])
        imap_mock.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

        settings_mock = MagicMock()
        settings_mock.EMAIL_IMPORT_ENABLED = True
        settings_mock.EMAIL_IMAP_USE_SSL = False
        settings_mock.EMAIL_IMAP_HOST = "localhost"
        settings_mock.EMAIL_IMAP_PORT = 3143
        settings_mock.EMAIL_IMAP_USERNAME = "test@localhost"
        settings_mock.EMAIL_IMAP_PASSWORD = "test"
        settings_mock.EMAIL_FOLDER = "INBOX"

        with patch.object(importer, "_connect", return_value=imap_mock), \
             patch("app.services.email_importer.settings", settings_mock):
            # Pierwszy import
            result1 = importer.import_messages(db=db, limit=10, analyze_imported=False)

        # Drugi import tej samej wiadomości
        imap_mock2 = MagicMock()
        imap_mock2.login.return_value = ("OK", [])
        imap_mock2.select.return_value = ("OK", [])
        imap_mock2.search.return_value = ("OK", [b"1"])
        imap_mock2.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

        with patch.object(importer, "_connect", return_value=imap_mock2), \
             patch("app.services.email_importer.settings", settings_mock):
            result2 = importer.import_messages(db=db, limit=10, analyze_imported=False)

        assert result1.imported_count == 1
        assert result2.imported_count == 0
        assert result2.skipped_count == 1

        # Tylko jedno zgłoszenie w bazie
        count = db.query(Ticket).filter(
            Ticket.email_message_id == "<dup-001@example.com>"
        ).count()
        assert count == 1

    def test_skipped_log_has_status_skipped(self, importer: EmailImporter, db) -> None:
        raw = _raw_email(message_id="<dup-002@example.com>")
        imap_mock = MagicMock()
        imap_mock.login.return_value = ("OK", [])
        imap_mock.select.return_value = ("OK", [])
        imap_mock.search.return_value = ("OK", [b"1"])
        imap_mock.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

        settings_mock = MagicMock()
        settings_mock.EMAIL_IMPORT_ENABLED = True
        settings_mock.EMAIL_IMAP_USE_SSL = False
        settings_mock.EMAIL_IMAP_HOST = "localhost"
        settings_mock.EMAIL_IMAP_PORT = 3143
        settings_mock.EMAIL_IMAP_USERNAME = "test@localhost"
        settings_mock.EMAIL_IMAP_PASSWORD = "test"
        settings_mock.EMAIL_FOLDER = "INBOX"

        with patch.object(importer, "_connect", return_value=imap_mock), \
             patch("app.services.email_importer.settings", settings_mock):
            importer.import_messages(db=db, limit=10, analyze_imported=False)

        imap_mock2 = MagicMock()
        imap_mock2.login.return_value = ("OK", [])
        imap_mock2.select.return_value = ("OK", [])
        imap_mock2.search.return_value = ("OK", [b"1"])
        imap_mock2.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

        with patch.object(importer, "_connect", return_value=imap_mock2), \
             patch("app.services.email_importer.settings", settings_mock):
            result = importer.import_messages(db=db, limit=10, analyze_imported=False)

        assert len(result.logs) == 1
        assert result.logs[0].status == "skipped"

    def test_imported_log_has_status_imported(self, importer: EmailImporter, db) -> None:
        raw = _raw_email(message_id="<imported-log@example.com>")
        imap_mock = MagicMock()
        imap_mock.login.return_value = ("OK", [])
        imap_mock.select.return_value = ("OK", [])
        imap_mock.search.return_value = ("OK", [b"1"])
        imap_mock.fetch.return_value = ("OK", [(b"1 (RFC822 {size})", raw)])

        settings_mock = MagicMock()
        settings_mock.EMAIL_IMPORT_ENABLED = True
        settings_mock.EMAIL_IMAP_USE_SSL = False
        settings_mock.EMAIL_IMAP_HOST = "localhost"
        settings_mock.EMAIL_IMAP_PORT = 3143
        settings_mock.EMAIL_IMAP_USERNAME = "test@localhost"
        settings_mock.EMAIL_IMAP_PASSWORD = "test"
        settings_mock.EMAIL_FOLDER = "INBOX"

        with patch.object(importer, "_connect", return_value=imap_mock), \
             patch("app.services.email_importer.settings", settings_mock):
            result = importer.import_messages(db=db, limit=10, analyze_imported=False)

        assert len(result.logs) == 1
        assert result.logs[0].status == "imported"


class TestEmailImporterDisabled:
    def test_returns_empty_when_disabled(self, importer: EmailImporter, db) -> None:
        with patch("app.services.email_importer.settings") as mock_settings:
            mock_settings.EMAIL_IMPORT_ENABLED = False
            result = importer.import_messages(db=db, limit=10, analyze_imported=False)

        assert result.imported_count == 0
        assert result.skipped_count == 0
        assert result.error_count == 0
        assert result.logs == []
