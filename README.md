# Helpdesk AI Service

Prototyp systemu helpdesk/service desk z modułem analizy AI dla zgłoszeń technicznych. Repozytorium obejmuje backend FastAPI, frontend React + TypeScript, PostgreSQL, migracje Alembic, mockowe role użytkowników oraz zestaw testów i narzędzi ewaluacyjnych.

## Aktywny zakres produktu

- zgłoszenia tworzone z formularzy agenta i użytkownika końcowego,
- panel agenta: dashboard, lista zgłoszeń, szczegóły, baza wiedzy, widok AI, ustawienia,
- portal end_user: moje zgłoszenia, nowe zgłoszenie, profil,
- baza wiedzy dostępna w panelu agenta,
- analiza AI rule-based uruchamiana z widoku szczegółów zgłoszenia,
- feedback do odpowiedzi AI i metryki jakości,
- offline evaluation na syntetycznym zbiorze testowym,
- mock auth z rolami `agent` i `end_user`.

Repozytorium nie zawiera aktywnej integracji/importu poczty. Pole `requester_email` pozostaje zwykłym polem kontaktowym zgłaszającego używanym w formularzach i portalu użytkownika.

## Stack

| Warstwa | Technologia |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Baza danych | PostgreSQL 16 |
| Migracje | Alembic |
| Kontenery | Docker Compose |
| Testy | pytest, TypeScript build |

## Role mockowe

Logowanie jest mockowe i zapisuje wybrane konto w `localStorage`.

| Użytkownik | E-mail | Rola | Zakres |
|---|---|---|---|
| Norbert | `agent@helpdesk.local` | `agent` | Dashboard, Zgłoszenia, Baza wiedzy, AI, Ustawienia |
| Jan | `user@company.local` | `end_user` | Moje zgłoszenia, Nowe zgłoszenie, Profil |

## Uruchomienie lokalne

### 1. Konfiguracja środowiska

```bash
cp .env.example .env
```

Kluczowe zmienne:

| Zmienna | Opis |
|---|---|
| `DATABASE_URL` | Połączenie do lokalnego PostgreSQL |
| `AI_PROVIDER` | Dostawca AI, domyślnie `mock` |

### 2. Docker Compose

```bash
docker compose up -d
docker compose logs -f postgres
docker compose down
```

Compose uruchamia wyłącznie PostgreSQL wymagany przez aplikację.

### 3. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_data.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend: http://localhost:8000  
Health: http://localhost:8000/health  
Swagger UI: http://localhost:8000/docs

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Migracje Alembic

Historia migracji została skonsolidowana do jednej czystej migracji bazowej odpowiadającej aktualnemu schematowi prototypu.

Jeżeli lokalna baza developerska była utworzona przed tym porządkowaniem, odtwórz ją od zera:

```bash
docker compose down -v
docker compose up -d
cd backend
source .venv/bin/activate
alembic upgrade head
python scripts/seed_data.py
```

Jeżeli lokalna baza ma już aktualne tabele, ale `alembic upgrade head` kończy się błędem `Can't locate revision identified by '007_remove_email_features'`, zsynchronizuj znacznik rewizji bez kasowania danych:

```bash
cd backend
source .venv/bin/activate
alembic stamp 001_initial --purge
alembic upgrade head
```

## Główne funkcje

- tworzenie, przeglądanie i aktualizacja zgłoszeń,
- frontendowe filtrowanie listy zgłoszeń,
- status `ai_reviewed` po analizie AI,
- edycja kategorii i priorytetów w Ustawieniach,
- feedback do odpowiedzi AI,
- agentowa baza wiedzy,
- portal użytkownika końcowego ograniczony do jego własnych zgłoszeń.

## Testy i weryfikacja

### Backend

```bash
cd backend
source .venv/bin/activate
pytest
```

### Frontend

```bash
cd frontend
npm run build
```

### Ewaluacja offline

```bash
cd backend
source .venv/bin/activate
python scripts/run_evaluation.py
```

Raporty są zapisywane w `reports/evaluation/`.

## Statusy zgłoszeń

| Wartość | Etykieta |
|---|---|
| `open` | Otwarte |
| `ai_reviewed` | Zweryfikowane przez AI |
| `pending` | Oczekujące |
| `resolved` | Rozwiązane |
| `rejected` | Odrzucone |

## ADR

| Numer | Tytuł |
|---|---|
| [0001](docs/decisions/0001-mock-analysis-pipeline.md) | Mock Analysis Pipeline |
| [0003](docs/decisions/0003-ai-feedback-and-quality-metrics.md) | AI Feedback i metryki jakości |
| [0004](docs/decisions/0004-frontend-final-ui-cleanup.md) | Finalne uporządkowanie UI |

## Ograniczenia prototypu

- brak prawdziwego auth/JWT i autoryzacji backendowej,
- brak backendowego filtrowania i paginacji listy zgłoszeń,
- analiza AI jest rule-based i nie używa zewnętrznych modeli,
- brak testów end-to-end frontendu.
