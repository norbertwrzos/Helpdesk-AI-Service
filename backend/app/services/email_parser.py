"""
EmailParser — parsuje surową wiadomość e-mail (bytes) do struktury ParsedEmail.

Obsługuje:
- wiadomości text/plain,
- wiadomości text/html (HTML jest czyszczony do tekstu),
- polskie znaki w temacie i treści (RFC 2047 / UTF-8),
- brak Message-ID (generuje hash zastępczy),
- brak tematu (domyślny tytuł po polsku),
- brak treści (komunikat zastępczy).

Nie analizuje załączników.
"""

import email
import email.header
import email.utils
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.message import Message


@dataclass
class ParsedEmail:
    """Wynik parsowania pojedynczej wiadomości e-mail."""

    message_id: str
    sender: str
    subject: str
    body: str
    received_at: datetime | None


class EmailParser:
    """Parsuje surową wiadomość RFC 2822 do struktury ParsedEmail."""

    MAX_BODY_LENGTH = 10_000

    def parse(self, raw_message: bytes) -> ParsedEmail:
        msg: Message = email.message_from_bytes(raw_message)

        sender = self._decode_header(msg.get("From", ""))
        raw_subject = self._decode_header(msg.get("Subject", ""))
        subject = raw_subject if raw_subject else "Zgłoszenie e-mail bez tematu"
        date_str = msg.get("Date")
        message_id = (msg.get("Message-ID") or "").strip()
        received_at = self._parse_date(date_str)
        body = self._extract_body(msg)

        if not message_id:
            message_id = self._generate_fallback_id(
                sender, subject, date_str or "", body
            )

        return ParsedEmail(
            message_id=message_id,
            sender=sender,
            subject=subject,
            body=body or "Brak treści wiadomości e-mail",
            received_at=received_at,
        )

    # ------------------------------------------------------------------
    # Metody pomocnicze
    # ------------------------------------------------------------------

    def _decode_header(self, value: str) -> str:
        """Dekoduje nagłówek RFC 2047 (obsługuje kodowania UTF-8, ISO-8859-2 itp.)."""
        if not value:
            return ""
        parts = email.header.decode_header(value)
        decoded_parts: list[str] = []
        for part, charset in parts:
            if isinstance(part, bytes):
                decoded_parts.append(
                    part.decode(charset or "utf-8", errors="replace")
                )
            else:
                decoded_parts.append(part)
        return "".join(decoded_parts).strip()

    def _parse_date(self, date_str: str | None) -> datetime | None:
        if not date_str:
            return None
        try:
            parsed = email.utils.parsedate_to_datetime(date_str)
            return parsed.astimezone(timezone.utc)
        except Exception:
            return None

    def _extract_body(self, msg: Message) -> str:
        """Wyciąga treść wiadomości; preferuje text/plain nad text/html."""
        plain_text: str | None = None
        html_text: str | None = None

        if msg.is_multipart():
            for part in msg.walk():
                ct = part.get_content_type()
                if ct == "text/plain" and plain_text is None:
                    plain_text = self._decode_part(part)
                elif ct == "text/html" and html_text is None:
                    html_text = self._decode_part(part)
        else:
            ct = msg.get_content_type()
            if ct == "text/plain":
                plain_text = self._decode_part(msg)
            elif ct == "text/html":
                html_text = self._decode_part(msg)

        if plain_text is not None:
            body = plain_text
        elif html_text is not None:
            body = self._strip_html(html_text)
        else:
            body = ""

        return body[: self.MAX_BODY_LENGTH]

    def _decode_part(self, part: Message) -> str:
        charset = part.get_content_charset() or "utf-8"
        payload = part.get_payload(decode=True)
        if payload is None:
            return ""
        return payload.decode(charset, errors="replace")

    def _strip_html(self, html: str) -> str:
        """Usuwa tagi HTML. Używa BeautifulSoup jeśli dostępny, w przeciwnym razie regex."""
        try:
            from bs4 import BeautifulSoup  # type: ignore[import]

            soup = BeautifulSoup(html, "html.parser")
            return soup.get_text(separator="\n").strip()
        except ImportError:
            text = re.sub(r"<[^>]+>", " ", html)
            return re.sub(r" +", " ", text).strip()

    def _generate_fallback_id(
        self, sender: str, subject: str, date_str: str, body: str
    ) -> str:
        """Generuje stabilny identyfikator zastępczy gdy brakuje Message-ID."""
        raw = f"{sender}|{subject}|{date_str}|{body[:200]}"
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        return f"generated-{digest}"
