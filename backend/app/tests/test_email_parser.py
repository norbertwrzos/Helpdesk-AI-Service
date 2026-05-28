"""Testy jednostkowe EmailParser."""

import email as email_lib
import email.mime.text
import email.mime.multipart
from datetime import timezone

import pytest

from app.services.email_parser import EmailParser, ParsedEmail


def _make_plain_email(
    subject: str = "Test subject",
    body: str = "Test body",
    sender: str = "user@example.com",
    date: str = "Wed, 28 May 2026 10:00:00 +0000",
    message_id: str | None = "<test-id@example.com>",
) -> bytes:
    msg = email.mime.text.MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Date"] = date
    if message_id:
        msg["Message-ID"] = message_id
    return msg.as_bytes()


def _make_html_email(
    subject: str = "HTML subject",
    html_body: str = "<p>Hello <b>world</b></p>",
    sender: str = "sender@example.com",
    message_id: str | None = "<html-id@example.com>",
) -> bytes:
    msg = email.mime.multipart.MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Date"] = "Wed, 28 May 2026 12:00:00 +0000"
    if message_id:
        msg["Message-ID"] = message_id
    html_part = email.mime.text.MIMEText(html_body, "html", "utf-8")
    msg.attach(html_part)
    return msg.as_bytes()


class TestEmailParserPlain:
    def setup_method(self) -> None:
        self.parser = EmailParser()

    def test_parse_plain_email_returns_parsed_email(self) -> None:
        raw = _make_plain_email()
        result = self.parser.parse(raw)
        assert isinstance(result, ParsedEmail)

    def test_parse_plain_email_subject(self) -> None:
        raw = _make_plain_email(subject="Nie działa drukarka")
        result = self.parser.parse(raw)
        assert result.subject == "Nie działa drukarka"

    def test_parse_plain_email_sender(self) -> None:
        raw = _make_plain_email(sender="jan.kowalski@firma.pl")
        result = self.parser.parse(raw)
        assert result.sender == "jan.kowalski@firma.pl"

    def test_parse_plain_email_body(self) -> None:
        raw = _make_plain_email(body="Treść zgłoszenia technicznego.")
        result = self.parser.parse(raw)
        assert "Treść zgłoszenia technicznego." in result.body

    def test_parse_plain_email_message_id(self) -> None:
        raw = _make_plain_email(message_id="<unique-id-123@mail.example.com>")
        result = self.parser.parse(raw)
        assert result.message_id == "<unique-id-123@mail.example.com>"

    def test_parse_plain_email_received_at(self) -> None:
        raw = _make_plain_email(date="Wed, 28 May 2026 10:00:00 +0000")
        result = self.parser.parse(raw)
        assert result.received_at is not None
        assert result.received_at.tzinfo is not None

    def test_parse_plain_email_received_at_utc(self) -> None:
        raw = _make_plain_email(date="Wed, 28 May 2026 10:00:00 +0000")
        result = self.parser.parse(raw)
        assert result.received_at.tzinfo == timezone.utc or str(
            result.received_at.tzinfo
        ) in ("UTC", "utc")


class TestEmailParserHtml:
    def setup_method(self) -> None:
        self.parser = EmailParser()

    def test_parse_html_email_strips_tags(self) -> None:
        raw = _make_html_email(html_body="<p>Witaj <b>świecie</b>!</p>")
        result = self.parser.parse(raw)
        assert "<p>" not in result.body
        assert "<b>" not in result.body
        assert "świecie" in result.body

    def test_parse_html_email_subject(self) -> None:
        raw = _make_html_email(subject="Problem z siecią")
        result = self.parser.parse(raw)
        assert result.subject == "Problem z siecią"


class TestEmailParserFallbacks:
    def setup_method(self) -> None:
        self.parser = EmailParser()

    def test_missing_message_id_generates_fallback(self) -> None:
        raw = _make_plain_email(message_id=None)
        result = self.parser.parse(raw)
        assert result.message_id.startswith("generated-")

    def test_fallback_message_id_is_stable(self) -> None:
        """Ten sam e-mail bez Message-ID powinien generować ten sam hash."""
        raw = _make_plain_email(message_id=None)
        result1 = self.parser.parse(raw)
        result2 = self.parser.parse(raw)
        assert result1.message_id == result2.message_id

    def test_missing_subject_uses_default(self) -> None:
        raw = _make_plain_email(subject="")
        result = self.parser.parse(raw)
        assert result.subject == "Zgłoszenie e-mail bez tematu"

    def test_missing_body_uses_placeholder(self) -> None:
        # Tworzymy wiadomość bez treści
        msg = email.mime.text.MIMEText("", "plain", "utf-8")
        msg["Subject"] = "Empty body"
        msg["From"] = "sender@example.com"
        msg["Date"] = "Wed, 28 May 2026 10:00:00 +0000"
        msg["Message-ID"] = "<empty-body@test>"
        result = self.parser.parse(msg.as_bytes())
        assert result.body == "Brak treści wiadomości e-mail"


class TestEmailParserPolishChars:
    def setup_method(self) -> None:
        self.parser = EmailParser()

    def test_polish_chars_in_subject(self) -> None:
        subject = "Błąd konfiguracji sieci — prośba o pomoc"
        raw = _make_plain_email(subject=subject)
        result = self.parser.parse(raw)
        assert "Błąd" in result.subject
        assert "prośba" in result.subject

    def test_polish_chars_in_body(self) -> None:
        body = "Nie mogę się zalogować. Hasło wygasło. Proszę o pomoc."
        raw = _make_plain_email(body=body)
        result = self.parser.parse(raw)
        assert "zalogować" in result.body
        assert "Proszę" in result.body

    def test_encoded_subject_rfc2047(self) -> None:
        """Temat zakodowany RFC 2047 (=?UTF-8?...?=) powinien być poprawnie zdekodowany."""
        import email.header

        encoded = email.header.make_header(
            email.header.decode_header("=?UTF-8?Q?Prosz=C4=99_o_pomoc?=")
        )
        raw = _make_plain_email(subject=str(encoded))
        result = self.parser.parse(raw)
        assert "Proszę" in result.subject

    def test_body_length_truncated(self) -> None:
        long_body = "a" * 20_000
        raw = _make_plain_email(body=long_body)
        result = self.parser.parse(raw)
        assert len(result.body) <= EmailParser.MAX_BODY_LENGTH
