"""Testy endpointów API importu e-mail."""

from unittest.mock import patch, MagicMock

import pytest

from app.schemas.email_import import EmailImportLogResponse, EmailImportRunResponse


def _mock_run_response(
    imported: int = 1,
    skipped: int = 0,
    errors: int = 0,
    analyzed: int = 0,
    logs: list[EmailImportLogResponse] | None = None,
) -> EmailImportRunResponse:
    from datetime import datetime, timezone

    default_log = EmailImportLogResponse(
        id=1,
        message_id="<test@example.com>",
        sender="user@example.com",
        subject="Test subject",
        status="imported",
        ticket_id=1,
        error_message=None,
        created_at=datetime.now(timezone.utc),
    )
    return EmailImportRunResponse(
        imported_count=imported,
        skipped_count=skipped,
        error_count=errors,
        analyzed_count=analyzed,
        logs=logs if logs is not None else [default_log],
    )


class TestRunEmailImportEndpoint:
    def test_post_email_import_run_returns_200(self, client) -> None:
        with patch(
            "app.api.routes.email_import.EmailImporter.import_messages",
            return_value=_mock_run_response(),
        ):
            response = client.post(
                "/email/import/run",
                json={"limit": 5, "analyze_imported": False},
            )

        assert response.status_code == 200

    def test_post_email_import_run_response_structure(self, client) -> None:
        with patch(
            "app.api.routes.email_import.EmailImporter.import_messages",
            return_value=_mock_run_response(imported=2, skipped=1),
        ):
            response = client.post(
                "/email/import/run",
                json={"limit": 10, "analyze_imported": False},
            )

        data = response.json()
        assert "imported_count" in data
        assert "skipped_count" in data
        assert "error_count" in data
        assert "analyzed_count" in data
        assert "logs" in data
        assert isinstance(data["logs"], list)

    def test_post_email_import_run_default_body(self, client) -> None:
        """Endpoint powinien działać z domyślnymi wartościami."""
        with patch(
            "app.api.routes.email_import.EmailImporter.import_messages",
            return_value=_mock_run_response(),
        ):
            response = client.post("/email/import/run", json={})

        assert response.status_code == 200


class TestGetEmailImportLogsEndpoint:
    def test_get_logs_returns_200(self, client) -> None:
        response = client.get("/email/import/logs")
        assert response.status_code == 200

    def test_get_logs_returns_list(self, client) -> None:
        response = client.get("/email/import/logs")
        data = response.json()
        assert isinstance(data, list)

    def test_get_logs_empty_when_no_logs(self, client) -> None:
        response = client.get("/email/import/logs")
        assert response.json() == []

    def test_get_logs_returns_created_log(self, client, db) -> None:
        from datetime import datetime, timezone
        from app.models.email_import_log import EmailImportLog

        log = EmailImportLog(
            message_id="<log-test@example.com>",
            sender="sender@example.com",
            subject="Test",
            status="imported",
        )
        db.add(log)
        db.commit()

        response = client.get("/email/import/logs")
        data = response.json()
        assert len(data) >= 1
        statuses = [entry["status"] for entry in data]
        assert "imported" in statuses

    def test_get_log_by_id_returns_404_for_missing(self, client) -> None:
        response = client.get("/email/import/logs/99999")
        assert response.status_code == 404

    def test_get_log_by_id_returns_log(self, client, db) -> None:
        from app.models.email_import_log import EmailImportLog

        log = EmailImportLog(
            message_id="<single-log@example.com>",
            status="skipped",
        )
        db.add(log)
        db.commit()
        db.refresh(log)

        response = client.get(f"/email/import/logs/{log.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "skipped"
        assert data["id"] == log.id
