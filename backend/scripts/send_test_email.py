#!/usr/bin/env python3
"""
Skrypt pomocniczy: wysyła przykładową wiadomość e-mail do GreenMail przez SMTP.

Cel: umożliwić ręczne testowanie importu e-mail bez potrzeby konfiguracji
zewnętrznego klienta pocztowego.

Użycie:
    python scripts/send_test_email.py
    python scripts/send_test_email.py --subject "Problem z VPN" --body "Opis problemu"
    python scripts/send_test_email.py --sender user@example.com --recipient test@localhost
"""

import argparse
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Domyślne wartości — zgodne z konfiguracją GreenMail w docker-compose.yml
SMTP_HOST = os.getenv("EMAIL_SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "3025"))
SMTP_USERNAME = os.getenv("EMAIL_SMTP_USERNAME", "test@localhost")
SMTP_PASSWORD = os.getenv("EMAIL_SMTP_PASSWORD", "test")
SMTP_USE_TLS = os.getenv("EMAIL_SMTP_USE_TLS", "false").lower() == "true"


def send_email(
    subject: str,
    body: str,
    sender: str,
    recipient: str,
) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    part = MIMEText(body, "plain", "utf-8")
    msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        if SMTP_USE_TLS:
            server.starttls()
        # GreenMail w trybie testowym nie wymaga uwierzytelnienia SMTP
        try:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        except smtplib.SMTPException:
            pass  # GreenMail może nie obsługiwać AUTH — kontynuuj bez logowania
        server.sendmail(sender, [recipient], msg.as_bytes())

    print(f"✓ Wiadomość wysłana pomyślnie.")
    print(f"  Temat:    {subject}")
    print(f"  Nadawca:  {sender}")
    print(f"  Odbiorca: {recipient}")
    print(f"  Serwer:   {SMTP_HOST}:{SMTP_PORT}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wyślij testową wiadomość e-mail do GreenMail."
    )
    parser.add_argument(
        "--subject",
        default="Nie działa VPN",
        help="Temat wiadomości (domyślnie: 'Nie działa VPN')",
    )
    parser.add_argument(
        "--body",
        default=(
            "Nie mogę połączyć się z VPN od rana. "
            "Internet działa poprawnie, ale klient VPN pokazuje błąd logowania."
        ),
        help="Treść wiadomości",
    )
    parser.add_argument(
        "--sender",
        default="user@example.com",
        help="Adres nadawcy (domyślnie: user@example.com)",
    )
    parser.add_argument(
        "--recipient",
        default="test@localhost",
        help="Adres odbiorcy (domyślnie: test@localhost)",
    )
    args = parser.parse_args()

    send_email(
        subject=args.subject,
        body=args.body,
        sender=args.sender,
        recipient=args.recipient,
    )


if __name__ == "__main__":
    main()
