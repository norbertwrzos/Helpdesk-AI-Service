# Plan testów — Helpdesk AI Service

## Cel

Plan testów obejmuje aktualny zakres prototypu helpdesk: zgłoszenia, portal użytkownika końcowego, bazę wiedzy agenta, analizę AI rule-based, feedback, metryki jakości oraz konfigurację kategorii i priorytetów.

## Zakres

### Backend

- endpointy zgłoszeń, kategorii, priorytetów, bazy wiedzy i feedbacku,
- `AnalysisPipeline`, `ClassificationService`, `PriorityAnalysisService`, `MockAIGenerator`,
- moduł ewaluacji offline i raportowania,
- migracje Alembic dla aktualnego schematu.

### Frontend

- build produkcyjny (`npm run build`),
- ręczny smoke test dla ról `agent` i `end_user`,
- walidacja ustawień kategorii i priorytetów,
- walidacja zakresu portalu użytkownika końcowego.

### Poza zakresem

- prawdziwa autentykacja i autoryzacja backendowa,
- testy wydajnościowe i bezpieczeństwa,
- pełne automatyczne testy end-to-end frontendu,
- integracje z zewnętrznymi modelami AI.

## Dane testowe

- `data/seed/categories.json`
- `data/seed/priorities.json`
- `data/seed/knowledge_base.json`
- `data/test_cases/evaluation_tickets.csv`
- `data/test_cases/evaluation_tickets.json`

Zbiór ewaluacyjny pozostaje syntetyczny i służy wyłącznie do weryfikacji prototypu rule-based.

## Najważniejsze scenariusze do pokrycia

- dodanie zgłoszenia przez formularz,
- analiza AI i zmiana statusu na `ai_reviewed`,
- dodanie odpowiedzi agenta,
- zapis feedbacku dla odpowiedzi AI,
- CRUD bazy wiedzy agenta,
- dodawanie i edycja kategorii,
- dodawanie i edycja priorytetów,
- ograniczony zakres portalu `end_user`,
- uruchomienie ewaluacji offline i wygenerowanie raportów.

## Środowisko testowe

| Element | Konfiguracja |
|---|---|
| Python | 3.12 |
| Backend tests | pytest + FastAPI TestClient |
| Baza dla testów backendu | SQLite in-memory |
| Baza developerska | PostgreSQL 16 |
| Frontend validation | TypeScript build + Vite build |

## Komendy

### Backend tests

```bash
cd backend
source .venv/bin/activate
pytest
```

### Frontend build

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

## Ryzyka i ograniczenia

- brak testów E2E dla ścieżek UI,
- pipeline AI jest deterministyczny i rule-based,
- wyniki ewaluacji nie reprezentują zachowania produkcyjnych modeli ML/LLM,
- po konsolidacji migracji starsze lokalne bazy developerskie wymagają resetu.
