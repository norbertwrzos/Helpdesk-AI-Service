# Helpdesk AI Service

> Projekt inżynierski: „Projekt i implementacja serwisu do zautomatyzowanego rozwiązywania zgłoszeń technicznych z wykorzystaniem metod sztucznej inteligencji"

---

## Opis projektu

Helpdesk AI Service to prototyp systemu IT Support, który automatyzuje obsługę zgłoszeń technicznych przy użyciu metod sztucznej inteligencji i przetwarzania języka naturalnego (NLP).

System docelowo:

- przyjmuje i importuje zgłoszenia techniczne (formularz, e-mail),
- analizuje i klasyfikuje zgłoszenia,
- nadaje priorytety,
- wyszukuje podobne historyczne przypadki,
- generuje propozycje rozwiązań z użyciem AI,
- przechowuje historię zgłoszeń,
- umożliwia ocenę jakości odpowiedzi AI.

---

## Cel pracy

Celem pracy inżynierskiej jest zaprojektowanie i zaimplementowanie prototypu serwisu helpdesk wspomaganego przez AI, który demonstruje praktyczne zastosowanie metod NLP w automatyzacji obsługi zgłoszeń technicznych.

---

## Technologie

| Warstwa      | Technologia                         |
|--------------|-------------------------------------|
| Backend      | Python 3.12, FastAPI                |
| Frontend     | React 18, TypeScript, Vite, Tailwind CSS v3 |
| Baza danych  | PostgreSQL 16                       |
| ORM          | SQLAlchemy                          |
| Migracje     | Alembic                             |
| Kontenery    | Docker, Docker Compose              |
| Serwer email | GreenMail                           |
| Konfiguracja | pydantic-settings, .env             |
| Testy        | pytest                              |

---

## Struktura katalogów

```
helpdesk-ai-service/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # Endpointy FastAPI
│   │   ├── core/             # Konfiguracja aplikacji
│   │   ├── db/               # Sesja i silnik bazy danych
│   │   ├── models/           # Modele SQLAlchemy (ORM)
│   │   ├── schemas/          # Schematy Pydantic
│   │   ├── services/         # Logika biznesowa, AI, email
│   │   ├── tests/            # Testy jednostkowe i integracyjne
│   │   └── main.py           # Punkt wejściowy aplikacji
│   ├── alembic/              # Migracje bazy danych
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── api/              # Klienci HTTP (axios/fetch)
│   │   ├── components/       # Komponenty React
│   │   ├── pages/            # Strony aplikacji
│   │   ├── types/            # Typy TypeScript
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── data/
│   ├── seed/                 # Dane startowe
│   └── test_cases/           # Testowe zgłoszenia
├── docs/
│   ├── diagrams/             # Diagramy UML, C4
│   ├── api/                  # Dokumentacja API
│   ├── screenshots/          # Zrzuty ekranu
│   └── decisions/            # Decyzje architektoniczne (ADR)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Wymagania środowiskowe

- Python 3.12+
- Node.js 20+
- Docker + Docker Compose v2
- WSL2 Ubuntu (zalecane)

---

## Konfiguracja `.env`

Skopiuj plik `.env.example` i uzupełnij wartości:

```bash
cp .env.example .env
```

Kluczowe zmienne:

| Zmienna            | Opis                                      |
|--------------------|-------------------------------------------|
| `APP_ENV`          | Środowisko: `development` / `production`  |
| `DATABASE_URL`     | Connection string PostgreSQL              |
| `SECRET_KEY`       | Klucz aplikacji (zmień przed produkcją!)  |
| `AI_PROVIDER`      | Dostawca AI: `mock` / `openai`            |
| `OPENAI_API_KEY`   | Klucz API OpenAI (opcjonalny)             |
| `EMAIL_IMAP_*`     | Konfiguracja importu e-mail (GreenMail)   |

---

## Uruchomienie Dockera

Uruchamia PostgreSQL i GreenMail:

```bash
docker compose up -d
```

Zatrzymanie:

```bash
docker compose down
```

Logi:

```bash
docker compose logs -f
```

---

## Uruchomienie backendu

```bash
cd backend

# Utwórz i aktywuj środowisko wirtualne
python3 -m venv .venv
source .venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Wykonaj migracje (wymaga uruchomionego PostgreSQL)
alembic upgrade head

# Uruchom serwer deweloperski
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend dostępny pod: http://localhost:8000

Dokumentacja Swagger UI: http://localhost:8000/docs

---

## Uruchomienie testów

Testy używają bazy SQLite w pamięci — **nie wymagają uruchomionego PostgreSQL**.

```bash
cd backend
source .venv/bin/activate
pytest
```

---

## Dostępne endpointy (Etap 1 + Etap 3)

| Metoda | Ścieżka                              | Opis                              |
|--------|--------------------------------------|-----------------------------------|
| GET    | /health                              | Weryfikacja dostępności serwisu   |
| GET    | /tickets                             | Lista zgłoszeń                    |
| POST   | /tickets                             | Utwórz zgłoszenie                 |
| GET    | /tickets/{id}                        | Szczegóły zgłoszenia              |
| PATCH  | /tickets/{id}                        | Aktualizacja zgłoszenia           |
| POST   | /tickets/{id}/analyze                | **[Etap 3]** Uruchom analizę AI   |
| GET    | /tickets/{id}/ai-responses           | **[Etap 3]** Odpowiedzi AI        |
| GET    | /categories                          | Lista kategorii                   |
| POST   | /categories                          | Utwórz kategorię                  |
| GET    | /priorities                          | Lista priorytetów                 |
| POST   | /priorities                          | Utwórz priorytet                  |
| GET    | /knowledge                           | **[Etap 3]** Lista artykułów      |
| POST   | /knowledge                           | **[Etap 3]** Dodaj artykuł        |
| GET    | /knowledge/{id}                      | **[Etap 3]** Szczegóły artykułu   |
| PATCH  | /knowledge/{id}                      | **[Etap 3]** Aktualizuj artykuł   |
| DELETE | /knowledge/{id}                      | **[Etap 3]** Usuń artykuł         |

---

## Seedowanie danych (Etap 3)

Załadowanie kategorii, priorytetów i artykułów bazy wiedzy:

```bash
cd backend
source .venv/bin/activate
python scripts/seed_data.py
```

Skrypt jest idempotentny — nie tworzy duplikatów przy ponownym uruchomieniu.

---

## Etap 3 — AnalysisPipeline (mock AI/NLP)

### Opis

Etap 3 dodaje pełen przepływ analizy zgłoszenia:

```
Zgłoszenie → Klasyfikacja → Priorytetyzacja → Podobne artykuły → Odpowiedź AI → Zapis
```

### Komponenty

| Komponent | Plik | Opis |
|---|---|---|
| `AnalysisPipeline` | `services/analysis_pipeline.py` | Koordynator analizy |
| `ClassificationService` | `services/classification_service.py` | Klasyfikacja do kategorii (reguły słów kluczowych) |
| `PriorityAnalysisService` | `services/priority_analysis_service.py` | Nadanie priorytetu (reguły słów kluczowych) |
| `SimilarityService` | `services/similarity_service.py` | Wyszukiwanie podobnych artykułów (bag-of-words) |
| `MockAIGenerator` | `services/ai_generator.py` | Generowanie odpowiedzi AI (szablon po polsku) |

### Uwaga

Aktualny moduł AI jest **mock/rule-based** — używa reguł słów kluczowych zamiast prawdziwego modelu AI/NLP.
Architektura jest zaprojektowana tak, aby w przyszłości można było łatwo zastąpić każdy komponent
prawdziwą implementacją (np. klasyfikator ML, embeddingi, OpenAI API) bez zmian w reszcie systemu.

Szczegóły decyzji architektonicznych: [docs/decisions/0001-mock-analysis-pipeline.md](docs/decisions/0001-mock-analysis-pipeline.md)

---

## Scenariusz testowy (Etap 3)

1. Uruchom PostgreSQL: `docker compose up -d`
2. Uruchom migracje: `cd backend && alembic upgrade head`
3. Załaduj dane seed: `python scripts/seed_data.py`
4. Uruchom backend: `uvicorn app.main:app --reload`
5. Uruchom frontend: `cd frontend && npm run dev`
6. Otwórz http://localhost:5173
7. Przejdź do `/tickets` → dodaj zgłoszenie z tytułem **„Nie działa VPN"**
8. Kliknij „Szczegóły" zgłoszenia
9. Kliknij przycisk **„Analizuj zgłoszenie"**
10. Sprawdź, że wyświetla się:
    - kategoria: **Sieć i VPN** (confidence ≥ 85%)
    - priorytet z uzasadnieniem
    - podobne artykuły z bazy wiedzy
    - wygenerowana propozycja rozwiązania

---

## Uruchomienie frontendu

```bash
cd frontend
npm install
npm run dev
```

Frontend dostępny pod: http://localhost:5173

Zmienna środowiskowa (opcjonalna):
```bash
cp frontend/.env.example frontend/.env
# VITE_API_BASE_URL=http://localhost:8000  (domyślna wartość)
```

---

## Weryfikacja buildu frontendu

```bash
cd frontend
npm run build
```

---

## Scenariusz testowy (Etap 2)

1. Uruchom PostgreSQL: `docker compose up -d`
2. Uruchom migracje: `cd backend && alembic upgrade head`
3. Uruchom backend: `uvicorn app.main:app --reload`
4. Uruchom frontend: `cd frontend && npm run dev`
5. Otwórz http://localhost:5173
6. Przejdź do `/tickets` → dodaj zgłoszenie przez formularz
7. Sprawdź, że zgłoszenie pojawia się na liście
8. Kliknij „Szczegóły" → zmień status → zapisz zmiany
9. Sprawdź, że zmiany są widoczne po odświeżeniu


---

## Etap 4 — Import zgłoszeń z e-maila

### Opis

Etap 4 dodaje jednokierunkowy import wiadomości przychodzących z testowej skrzynki IMAP (GreenMail)
jako zgłoszenia techniczne w systemie.

```
Wiadomość e-mail → IMAP Importer → EmailParser → Ticket (source=email) → EmailImportLog → AnalysisPipeline
```

### Uruchomienie

**1. Uruchom Docker Compose** (PostgreSQL + GreenMail):
```bash
docker compose up -d
```

**2. Wykonaj migracje Alembic:**
```bash
cd backend
alembic upgrade head
```

**3. Załaduj dane seed (potrzebne do analizy AI):**
```bash
python scripts/seed_data.py
```

**4. Uruchom backend:**
```bash
uvicorn app.main:app --reload
```

**5. Uruchom frontend:**
```bash
cd frontend
npm run dev
```

**6. Wyślij testową wiadomość do GreenMail:**
```bash
cd backend
python scripts/send_test_email.py
# Lub z parametrami:
python scripts/send_test_email.py --subject "Problem z drukarką" --body "Drukarka nie drukuje od rana."
```

**7. Uruchom import przez frontend:**

Otwórz http://localhost:5173/email-import, ustaw limit i kliknij „Uruchom import".

**8. Uruchom import przez Swagger UI:**
```
POST http://localhost:8000/email/import/run
Body: { "limit": 10, "analyze_imported": true }
```

**9. Sprawdź logi importu:**
```
GET http://localhost:8000/email/import/logs
```

### Nowe endpointy (Etap 4)

| Metoda | Ścieżka                        | Opis                                   |
|--------|--------------------------------|----------------------------------------|
| POST   | /email/import/run              | Uruchom import wiadomości z IMAP       |
| GET    | /email/import/logs             | Lista logów importu                    |
| GET    | /email/import/logs/{id}        | Szczegóły pojedynczego logu importu    |

### Przykładowy scenariusz testowy (Etap 4)

1. Uruchom `docker compose up -d`
2. Uruchom migracje: `alembic upgrade head`
3. Załaduj seed: `python scripts/seed_data.py`
4. Uruchom backend: `uvicorn app.main:app --reload`
5. Uruchom frontend: `cd frontend && npm run dev`
6. Wyślij testowy e-mail: `python scripts/send_test_email.py`
7. Przejdź do http://localhost:5173/email-import
8. Kliknij „Uruchom import" (z zaznaczoną opcją analizy)
9. Sprawdź podsumowanie: `imported_count=1, analyzed_count=1`
10. Kliknij link do zgłoszenia w tabeli logów
11. Sprawdź, że zgłoszenie ma `source=email`, wypełnione pola `email_sender`, `email_subject`
12. Sprawdź, że AnalysisPipeline uruchomił się automatycznie

### Uruchomienie testów (Etap 4)

```bash
cd backend
pytest app/tests/test_email_parser.py
pytest app/tests/test_email_importer.py
pytest app/tests/test_email_import_api.py
# Lub wszystkie testy naraz:
pytest
```

### Weryfikacja buildu frontendu

```bash
cd frontend
npm run build
```

### Ograniczenia (MVP)

- System importuje **wyłącznie wiadomości przychodzące** — nie wysyła odpowiedzi e-mail.
- System nie obsługuje wątków korespondencji.
- Załączniki nie są analizowane przez AI.
- Import e-mail jest testowany na GreenMail (nie na produkcyjnym serwerze SMTP/IMAP).
- Brak schedulera — import uruchamiany jest ręcznie (panel `/email-import` dla admina lub endpoint Swagger `POST /api/email/import`).

Szczegóły decyzji architektonicznych: [docs/decisions/0002-email-import.md](docs/decisions/0002-email-import.md)

---

## Etap 7 — Kontrakt danych i mock autentykacja (role)

### Logowanie mockowe

Logowanie w aplikacji jest **mockowe** i służy wyłącznie do demonstracji ról użytkowników w prototypie.
**Nie ma prawdziwego JWT, haseł ani sesji backendowej.** Wybór użytkownika zapisywany jest w `localStorage`.

Dostępne konta demonstracyjne:

| Użytkownik | E-mail | Rola | Dostęp |
|---|---|---|---|
| Administrator | `admin@helpdesk.local` | `admin` | Główny panel (dashboard, zgłoszenia, import) |
| Agent IT | `agent@helpdesk.local` | `agent` | Główny panel (dashboard, zgłoszenia, import) |
| Jan (użytkownik) | `user@company.local` | `end_user` | Portal użytkownika (`/portal`) |

### Nowe statusy zgłoszeń

| Wartość | Polska etykieta | Mapowanie ze starego |
|---|---|---|
| `open` | Otwarte | ← `new` |
| `ai_reviewed` | Zweryfikowane przez AI | ← `in_analysis` / `answered` |
| `pending` | Oczekujące | ← `answered` |
| `resolved` | Rozwiązane | bez zmian |
| `rejected` | Odrzucone | bez zmian |

### Nowe pola Ticket

Dodano: `requester_email`, `requester_name`, `assigned_agent_name`, `agent_response`.
Migracja: `alembic/versions/005_service_desk_fields.py`.

### Scenariusz testowy (Etap 7)

1. Uruchom backend i frontend jak zwykle.
2. Otwórz http://localhost:5173 — zostaniesz przekierowany na `/login`.
3. Wybierz **Adam — agent@helpdesk.local (Agent IT Support)** i kliknij „Zaloguj się".
4. Główny panel powinien być dostępny.
5. Wyloguj się i zaloguj jako **Jan — user@company.local (Użytkownik końcowy)**.
6. Użytkownik końcowy powinien trafić na portal `/portal`.
7. Zaloguj się jako **Administrator** i sprawdź dostęp do wszystkich sekcji.

---

## Etap 8 — Nowy layout aplikacji (sidebar, topbar, dark mode)

### Opis

Etap 8 wprowadza nowy układ UI inspirowany komercyjnymi systemami service desk.
Logika AI, backend i kontrakt danych pozostają bez zmian.

### Nowa architektura UI

```
AppShell
├── Sidebar (lewy, stały, w-64)
│   ├── Logo "H" + nazwa aplikacji
│   ├── RoleBasedNavigation
│   │   ├── admin/agent: Dashboard, Zgłoszenia, Baza wiedzy, AI, Ustawienia
│   │   └── end_user: Moje zgłoszenia, Baza wiedzy
│   └── Stopka z numerem wersji
├── Topbar (górny, stały, h-16)
│   ├── Tytuł aplikacji
│   ├── Pole wyszukiwania
│   ├── Przycisk "Nowe zgłoszenie" (role-aware)
│   └── UserMenu (avatar, rola, wylogowanie)
└── Obszar treści (ml-64, mt-16)
```

### Technologia

| Element | Technologia |
|---|---|
| CSS utility-first | Tailwind CSS v3 |
| Tryb kolorystyczny | Dark mode (domyślny) |
| Akcent kolorystyczny | Violet (`#6366f1`) |
| Tło sidebara | `#13151f` |
| Tło powierzchni | `#1a1d27` |

### Nowe strony

| Ścieżka | Komponent | Dostęp |
|---|---|---|
| `/` | `HomeRedirect` → rola decyduje | wszyscy |
| `/dashboard` | `DashboardPage` | admin, agent |
| `/tickets` | `TicketsPage` | admin, agent |
| `/tickets/:id` | `TicketDetailsPage` | wszyscy |
| `/knowledge` | `KnowledgePage` | wszyscy |
| `/ai` | `AIPage` | admin, agent |
| `/settings` | `SettingsPage` | admin, agent |
| `/email-import` | `EmailImportPage` | admin, agent |
| `/portal/tickets` | `PortalTicketsPage` | end_user |
| `/portal/tickets/:id` | `PortalTicketDetailsPage` | end_user |

### Scenariusz testowy (Etap 8)

1. Uruchom backend i frontend: `cd frontend && npm run dev`
2. Otwórz http://localhost:5173 → przekierowanie na `/login`
3. Zaloguj się jako **Adam (agent)** → widoczny sidebar z nawigacją agenta, topbar z przyciskiem „Nowe zgłoszenie"
4. Kliknij kolejno: Dashboard, Zgłoszenia, Baza wiedzy, AI, Ustawienia
5. Wyloguj się → zaloguj jako **Jan (end_user)** → sidebar z opcjami portalu, przycisk topbara prowadzi do `/portal/tickets`
6. Sprawdź, że `/dashboard` po zalogowaniu jako end_user przekierowuje do `/portal/tickets`
7. Zweryfikuj build: `npm run build` — powinien przejść bez błędów

---

## Endpoint `/health`

Służy do weryfikacji dostępności serwisu.

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

Używany przez Docker healthcheck, monitoring i testy integracyjne.

---

---

## Etap 6 — Ewaluacja klasyfikacji, priorytetyzacji i odpowiedzi AI

### Cel etapu

Przeprowadzenie ewaluacji batchowej prototypowego pipeline'u analizy zgłoszeń:
- klasyfikacja kategorii i priorytetyzacja na 64 syntetycznych zgłoszeniach,
- porównanie przewidywań systemu z etykietami referencyjnymi,
- obliczenie metryk jakości (accuracy, precision, recall, F1),
- heurystyczna ocena jakości generowanych odpowiedzi AI,
- wygenerowanie raportu gotowego do wykorzystania w pracy inżynierskiej.

### Dane testowe

Plik: `data/test_cases/evaluation_tickets.csv`

- 64 syntetyczne zgłoszenia techniczne po polsku,
- każde zgłoszenie zawiera `expected_category` i `expected_priority` (etykiety referencyjne),
- dane wolne od danych osobowych i firmowych, bezpieczne do publikacji.

### Uruchomienie ewaluacji

```bash
cd backend
source .venv/bin/activate
python scripts/run_evaluation.py
```

Opcjonalne argumenty:

```bash
python scripts/run_evaluation.py \
  --input ../../data/test_cases/evaluation_tickets.csv \
  --output ../../reports/evaluation
```

### Wygenerowane raporty

Pliki zapisywane w `reports/evaluation/`:

| Plik | Opis |
|------|------|
| `evaluation_summary.json` | Metryki zbiorcze i macierze pomyłek (JSON) |
| `evaluation_results.csv` | Wyniki dla każdego zgłoszenia (CSV) |
| `evaluation_report.md` | Raport po polsku do pracy inżynierskiej |

### Eksport raportu do docs/testing

```bash
cd backend
python scripts/export_test_report.py
```

Kopiuje najnowszy `evaluation_report.md` do `docs/testing/latest_evaluation_report.md`.

### Interpretacja metryk

| Metryka | Opis |
|---------|------|
| **Accuracy** | Odsetek poprawnych klasyfikacji (poprawne / wszystkie) |
| **Precision** | TP / (TP + FP) — jak wiele przewidzianych etykiet jest poprawnych |
| **Recall** | TP / (TP + FN) — jak wiele rzeczywistych etykiet zostało wykrytych |
| **F1-score** | Harmoniczna średnia precision i recall |
| **Macro F1** | Średnia F1 ze wszystkich klas (równe wagi) |
| **Weighted F1** | Średnia F1 ważona liczebnością klas |
| **Ocena odpowiedzi (0–5)** | Heurystyczna ocena jakości odpowiedzi AI |

### Ograniczenia ewaluacji

- Dane testowe są **syntetyczne** — nie pochodzą z rzeczywistego systemu helpdesk.
- Aktualny moduł analizy jest **mock/rule-based** — wyniki stanowią baseline przed wdrożeniem AI/NLP.
- Ocena odpowiedzi ma charakter **heurystyczny** (nie ekspercki).
- Wyniki służą jako **punkt odniesienia** dla dalszej rozbudowy systemu.

### Dokumentacja testów

| Plik | Opis |
|------|------|
| [`docs/testing/test_plan.md`](docs/testing/test_plan.md) | Plan testów |
| [`docs/testing/test_scenarios.md`](docs/testing/test_scenarios.md) | Scenariusze testowe |
| [`docs/testing/evaluation_methodology.md`](docs/testing/evaluation_methodology.md) | Metodyka ewaluacji |

---

## Autor

Norbert Wrzos — Praca inżynierska, 2025/2026

---

## Etap 5 — Ocena odpowiedzi AI i metryki jakości

### Cel etapu

- zbieranie ocen odpowiedzi AI od użytkowników (skala 1–5),
- historia odpowiedzi AI dla każdego zgłoszenia,
- podstawowe metryki jakości w dedykowanej sekcji aplikacji.

### Nowe endpointy

| Metoda | Ścieżka | Opis |
|--------|---------|------|
| `POST` | `/tickets/{ticket_id}/feedback` | Tworzy lub aktualizuje ocenę odpowiedzi AI |
| `GET`  | `/tickets/{ticket_id}/feedback` | Zwraca wszystkie oceny dla zgłoszenia |
| `GET`  | `/ai-responses/{ai_response_id}/feedback` | Zwraca ocenę konkretnej odpowiedzi AI |
| `GET`  | `/tickets/{ticket_id}/ai-responses` | Historia odpowiedzi AI z feedbackiem |
| `GET`  | `/quality/ai-responses` | Podstawowe metryki jakości odpowiedzi AI |

### Uruchomienie migracji

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

### Uruchomienie backendu

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

### Uruchomienie frontendu

```bash
cd frontend
npm run dev
```

### Uruchomienie testów

```bash
cd backend
source .venv/bin/activate
python3.12 -m pytest app/tests/ -v
```

### Weryfikacja buildu frontendu

```bash
cd frontend
npm run build
```

### Przykładowy scenariusz

1. Dodaj zgłoszenie na `/tickets`.
2. Otwórz szczegóły zgłoszenia i kliknij „Analizuj zgłoszenie".
3. Przejdź do sekcji „Historia odpowiedzi AI" — pojawi się wygenerowana odpowiedź.
4. Kliknij „+ Dodaj ocenę", wybierz ocenę 1–5, zaznacz pomocność i dodaj komentarz.
5. Kliknij „Zapisz ocenę" — feedback zostanie zapisany.
6. Przejdź do `/quality` (zakładka „Jakość AI") i sprawdź metryki.

### Ograniczenia

- Feedback nie służy jeszcze do automatycznego uczenia modelu.
- Metryki mają charakter podstawowy — brak wykresów.
- Brak autoryzacji użytkowników — każdy może ocenić odpowiedź.
- Ocena ma charakter ekspercki/manualny.

Szczegóły decyzji architektonicznych: [docs/decisions/0003-ai-feedback-and-quality-metrics.md](docs/decisions/0003-ai-feedback-and-quality-metrics.md)
