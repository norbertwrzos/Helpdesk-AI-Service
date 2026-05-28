# ADR 0002 — Import zgłoszeń z wiadomości e-mail

**Status:** Zaakceptowany  
**Data:** 2026-05-28  
**Autor:** Norbert Wrzos

---

## Kontekst

Jednym z wymagań funkcjonalnych systemu Helpdesk AI Service jest możliwość automatycznego
importu zgłoszeń technicznych z wiadomości e-mail. W środowisku korporacyjnym duża część
zgłoszeń helpdesk trafia przez pocztę elektroniczną — użytkownicy opisują problemy w treści
wiadomości, a system powinien automatycznie je zarejestrować, sklasyfikować i zaproponować
odpowiedź.

Na etapie prototypu (praca inżynierska) kluczowe było:
- użycie prostego, standardowego protokołu do odbioru poczty (IMAP),
- możliwość testowania bez dostępu do zewnętrznego serwera poczty,
- zachowanie jednoznacznej, testowalnej architektury.

---

## Decyzja 1: IMAP jako protokół importu

### Wybór: `imaplib` (Python stdlib)

**Uzasadnienie:**
- IMAP jest przemysłowym standardem odbioru poczty obsługiwanym przez większość dostawców
  (Microsoft Exchange, Gmail, Zimbra itp.),
- `imaplib` jest częścią biblioteki standardowej Pythona — bez dodatkowych zależności,
- interfejs jest prosty, deterministyczny i łatwy do mockowania w testach,
- w przyszłości możliwa jest migracja na wyższy poziom abstrakcji (np. `imapclient`)
  lub na dedykowane API (Microsoft Graph API, Gmail API).

**Alternatywy odrzucone:**
- **POP3** — brak obsługi folderów i flag wiadomości, mniejsza elastyczność,
- **Microsoft Graph API** — wymaga rejestracji aplikacji w Azure AD, nie nadaje się do prototypu,
- **Gmail API** — wymaga konta Google i konfiguracji OAuth2, zbędna złożoność na etapie MVP.

---

## Decyzja 2: GreenMail jako testowy serwer e-mail

### Wybór: `greenmail/standalone:2.0.1` (Docker)

**Uzasadnienie:**
- GreenMail to lekki, izolowany serwer SMTP/IMAP przeznaczony do testów,
- działa jako kontener Docker bez konfiguracji zewnętrznej,
- udostępnia porty: SMTP (3025), IMAP (3143), HTTP API (8080),
- pozwala wysyłać testowe wiadomości przez SMTP i natychmiast importować je przez IMAP,
- jest powszechnie stosowany w testach integracyjnych w ekosystemie JVM i Docker,
- interfejs HTTP (port 8080) pozwala zarządzać skrzynkami bez klienta poczty.

**Konfiguracja GreenMail w `docker-compose.yml`:**
- jeden użytkownik: `test:test@localhost`,
- porty: 3025 (SMTP), 3143 (IMAP), 8080 (API/UI),
- konto testowe jest zgodne z konfiguracją w `.env.example`.

---

## Przepływ importu

```
1. POST /email/import/run
        │
        ▼
2. EmailImporter.import_messages(db, limit, analyze_imported)
        │
        ├─► IMAP login (test@localhost na GreenMail)
        │
        ├─► imap.search("ALL") → lista ID wiadomości
        │
        └─► Dla każdej wiadomości:
                │
                ├─► imap.fetch(num, "RFC822") → raw bytes
                │
                ├─► EmailParser.parse(raw) → ParsedEmail
                │   ├─ dekodowanie nagłówków (RFC 2047, UTF-8)
                │   ├─ wyciągnięcie text/plain lub text/html
                │   ├─ obsługa brakującego Message-ID (hash zastępczy)
                │   └─ obsługa brakującego tematu / treści
                │
                ├─► Sprawdzenie duplikatu (email_message_id w tickets)
                │   ├─ jeśli duplikat → EmailImportLog(status=skipped)
                │   └─ jeśli nowe → utwórz Ticket(source=email)
                │
                ├─► EmailImportLog(status=imported, ticket_id=...)
                │
                └─► [opcjonalnie] AnalysisPipeline.analyze_ticket(ticket_id)
                        └─ błąd analizy NIE przerywa importu
```

---

## Zapobieganie duplikatom

Każda wiadomość e-mail ma unikalny identyfikator `Message-ID` (nagłówek RFC 2822).

System używa `email_message_id` jako klucza deduplikacji:
- pole `email_message_id` w tabeli `tickets` ma ograniczenie `UNIQUE`,
- przed zapisaniem zgłoszenia sprawdzany jest istniejący rekord z tym samym `email_message_id`,
- jeśli wiadomość była już importowana, zapisywany jest log ze statusem `skipped`,
- jeśli wiadomość nie ma nagłówka `Message-ID`, system generuje stabilny hash zastępczy
  na podstawie `From + Subject + Date + body[:200]`.

Dzięki temu ponowne wywołanie `POST /email/import/run` jest **idempotentne** — te same wiadomości
nie tworzą kolejnych zgłoszeń.

---

## Dlaczego nie wysyłamy odpowiedzi e-mail (MVP)

W MVP zaimplementowany jest wyłącznie **jednokierunkowy import** wiadomości przychodzących.

**Uzasadnienie:**
1. **Zakres pracy inżynierskiej** — demonstracja klasyfikacji i analizy AI jest ważniejsza niż
   pełna dwukierunkowa synchronizacja poczty.
2. **Złożoność techniczna** — wysyłanie odpowiedzi wymaga obsługi wątków (`In-Reply-To`,
   `References`), szablonów e-mail, kolejkowania i mechanizmu ponownych prób (retry).
3. **Ryzyko testowe** — przypadkowe wysłanie odpowiedzi na rzeczywisty adres e-mail
   byłoby błędem w środowisku prototypowym.
4. **Separacja odpowiedzialności** — najpierw działający import, potem wysyłanie — zgodnie
   z zasadą incremental delivery.

---

## Możliwości rozbudowy w przyszłości

| Funkcja | Opis | Technologia |
|---|---|---|
| Wysyłanie odpowiedzi e-mail | Odpowiedź AI do nadawcy zgłoszenia | SMTP z obsługą `In-Reply-To` |
| Obsługa wątków | Korelacja wiadomości przez `References` | Parsowanie nagłówków MIME |
| Analiza załączników | Parsowanie PDF / DOCX / obrazów | OCR, `python-docx`, `pdfplumber` |
| Microsoft Graph API | Integracja z Exchange / Microsoft 365 | `msal`, Microsoft Graph REST API |
| Gmail API | Integracja z Gmail | Google OAuth2, Gmail API |
| Cykliczny import | Automatyczne odpytywanie IMAP co N sekund | APScheduler lub Celery + Redis |
| Zarządzanie flagami | Oznaczanie wiadomości jako przeczytane po imporcie | `imap.store(num, "+FLAGS", "\\Seen")` |

---

## Powiązane decyzje

- [ADR 0001 — Mock AnalysisPipeline](0001-mock-analysis-pipeline.md)
