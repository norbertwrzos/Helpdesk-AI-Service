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

## AI Etap 11 — UI Integration for RAG and Mail Response

W tym etapie frontend został rozszerzony o pełną prezentację wyników RAG i wygenerowanej odpowiedzi mailowej w widoku szczegółów zgłoszenia. Agent widzi badge providera i modelu, datę wygenerowania, treść odpowiedzi zachowującą format mailowy, listę źródeł RAG z oceną dopasowania oraz linkami do artykułów bazy wiedzy, a także akcje kopiowania szkicu i zapisania go jako `agent_response`.

Sekcja AI nadal wymaga ręcznego uruchomienia analizy i nie wykonuje automatycznych działań w tle. Najnowsza odpowiedź jest eksponowana na górze historii, starsze odpowiedzi pozostają dostępne poniżej, a feedback i metryki jakości działają bez zmian.

## AI Etap 10 — OpenAI Mail Response Generator

W tym etapie system został rozszerzony o generowanie propozycji odpowiedzi mailowej dla użytkownika końcowego. Odpowiedź powstaje na podstawie treści zgłoszenia, wyniku rule-based classification, wyniku rule-based prioritization, kontekstu pobranego przez RAG oraz imienia przypisanego agenta. System nie wysyła wiadomości automatycznie; generuje wyłącznie szkic do weryfikacji przez człowieka.

Warstwa generowania działa w dwóch trybach:

- `mock` — bezpieczny provider lokalny, który nie wymaga klucza API,
- `openai` — provider korzystający z OpenAI Responses API i Structured Outputs.

Jeżeli `AI_GENERATION_PROVIDER=openai`, ale `OPENAI_API_KEY` nie jest ustawiony albo wywołanie OpenAI zakończy się błędem, backend bezpiecznie wraca do providera `mock`.

## AI Etap 9 — RAG Foundation

W tym etapie projekt otrzymał fundament mechanizmu RAG dla bazy wiedzy. System potrafi indeksować artykuły jako embeddingi, zapisywać je w PostgreSQL z użyciem `pgvector`, wykonywać techniczne wyszukiwanie top-k podobnych artykułów oraz wracać do istniejącego mechanizmu bag-of-words, gdy provider embeddingów lub pgvector są niedostępne.

Zakres etapu nie obejmuje jeszcze generowania odpowiedzi przez OpenAI. Generator odpowiedzi końcowej pozostaje mockowy, a warstwa RAG odpowiada wyłącznie za retrieval i przygotowanie kontekstu.

## Stack

| Warstwa | Technologia |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy, OpenAI SDK |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Baza danych | PostgreSQL 16 + pgvector |
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
cd backend
cp .env.example .env
```

Kluczowe zmienne:

| Zmienna | Opis |
|---|---|
| `DATABASE_URL` | Połączenie do lokalnego PostgreSQL |
| `AI_PROVIDER` | Dostawca AI, domyślnie `mock` |
| `AI_GENERATION_PROVIDER` | Provider generowania odpowiedzi mailowej: `mock` albo `openai` |
| `RAG_EMBEDDING_PROVIDER` | Dostawca embeddingów, domyślnie `openai` |
| `OPENAI_API_KEY` | Klucz OpenAI dla embeddingów; gdy pusty, działa fallback |
| `OPENAI_CHAT_MODEL` | Model generujący odpowiedź mailową, domyślnie `gpt-4o-mini` |
| `OPENAI_RESPONSE_TEMPERATURE` | Temperatura generowania odpowiedzi |
| `OPENAI_MAX_OUTPUT_TOKENS` | Limit tokenów odpowiedzi generatywnej |
| `OPENAI_EMBEDDING_MODEL` | Model embeddingów, domyślnie `text-embedding-3-small` |
| `RAG_TOP_K` | Liczba zwracanych artykułów w retrievalu |
| `RAG_MIN_SCORE` | Minimalny wynik podobieństwa dla wyników RAG |

Przykładowa konfiguracja dla trybu OpenAI:

```env
AI_GENERATION_PROVIDER=openai
OPENAI_API_KEY=twoj_klucz
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_RESPONSE_TEMPERATURE=0.2
OPENAI_MAX_OUTPUT_TOKENS=1200
```

### 2. Docker Compose

```bash
docker compose up -d
docker compose logs -f postgres
docker compose down
```

Compose uruchamia PostgreSQL z wbudowanym rozszerzeniem `pgvector` wymaganym przez etap RAG.

Po zmianie obrazu na `pgvector/pgvector:pg16` lokalny wolumen developerski zwykle można zachować, ale w razie problemów z poprzednią instancją najbezpieczniejszym wariantem jest reset lokalnego wolumenu i ponowne wykonanie migracji.

Weryfikacja rozszerzenia:

```bash
docker compose exec postgres psql -U helpdesk -d helpdesk_ai -c "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
```

### 3. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_data.py
python scripts/reindex_knowledge_embeddings.py
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
python scripts/reindex_knowledge_embeddings.py
```

Jeżeli lokalna baza ma już aktualne tabele, ale `alembic upgrade head` kończy się błędem `Can't locate revision identified by '007_remove_email_features'`, zsynchronizuj znacznik rewizji bez kasowania danych:

```bash
cd backend
source .venv/bin/activate
alembic stamp 001_initial --purge
alembic upgrade head
```

Nowa migracja `002_knowledge_article_embeddings` tworzy rozszerzenie `vector` i tabelę `knowledge_article_embeddings`.

## Główne funkcje

- tworzenie, przeglądanie i aktualizacja zgłoszeń,
- frontendowe filtrowanie listy zgłoszeń,
- status `ai_reviewed` po analizie AI,
- edycja kategorii i priorytetów w Ustawieniach,
- feedback do odpowiedzi AI,
- interfejs odpowiedzi AI z prezentacją źródeł RAG, kopiowaniem treści i zapisem do odpowiedzi agenta,
- agentowa baza wiedzy,
- embeddingi artykułów bazy wiedzy i techniczny retrieval RAG,
- portal użytkownika końcowego ograniczony do jego własnych zgłoszeń.

## Jak działa RAG w tym projekcie

1. Artykuły bazy wiedzy są zamieniane na tekst indeksowy z tytułu, treści, tagów i kategorii.
2. Serwis reindeksacji liczy hash treści i pomija artykuły, które się nie zmieniły.
3. Embeddingi są zapisywane w PostgreSQL w tabeli `knowledge_article_embeddings` z użyciem `pgvector`.
4. Endpoint `POST /knowledge/search` pozwala technicznie przetestować retrieval po embeddingach lub fallback bag-of-words.
5. Endpoint `POST /tickets/{ticket_id}/retrieve-context` zwraca kontekst dla konkretnego zgłoszenia bez generowania odpowiedzi OpenAI.
6. `AnalysisPipeline` używa RAG tylko wtedy, gdy embeddingi są dostępne; w przeciwnym razie wraca do `SimilarityService`.

## Jak działa generator odpowiedzi mailowej

1. `AnalysisPipeline` uruchamia klasyfikację i priorytetyzację w trybie rule-based.
2. `RAGRetriever` pobiera artykuły bazy wiedzy powiązane ze zgłoszeniem.
3. Provider AI buduje prompt na podstawie zgłoszenia, kategorii, priorytetu, artykułów RAG i imienia agenta.
4. Provider `openai` generuje ustrukturyzowaną odpowiedź mailową przez OpenAI Responses API.
5. Provider `mock` przygotowuje lokalny szkic maila, gdy OpenAI jest wyłączone lub niedostępne.
6. `AIResponse.response_text` zapisuje treść maila, a `sources_used` przechowuje JSON z metadanymi źródeł RAG użytych przez model.

## Jak działa UI odpowiedzi AI

1. Agent uruchamia `POST /tickets/{ticket_id}/analyze` z widoku szczegółów zgłoszenia.
2. Frontend odświeża historię odpowiedzi AI przez `GET /tickets/{ticket_id}/ai-responses`.
3. Najnowsza odpowiedź jest pokazywana jako główna karta, a starsze odpowiedzi pozostają w historii poniżej.
4. Pole `sources_used` jest parsowane po stronie frontendu do listy źródeł RAG z tytułem, score, fragmentem treści i linkiem do `/knowledge/{article_id}`.
5. Agent może skopiować szkic odpowiedzi albo zapisać go jako `agent_response` przez istniejący `PATCH /tickets/{ticket_id}`.
6. Feedback do odpowiedzi AI pozostaje dostępny bez zmian i nadal zasila metryki jakości w widoku `AI`.

Format odpowiedzi mailowej:

```text
Dzień dobry,

[krótkie odniesienie do problemu użytkownika]

[proponowane kroki rozwiązania]

[co zrobić, jeśli problem nadal występuje]

Pozdrawiam,
[imię agenta]
```

Analizę ticketu można uruchomić przez Swagger UI lub endpoint `POST /tickets/{ticket_id}/analyze`.

## Zasady bezpieczeństwa dla AI Etapu 10

- klucz `OPENAI_API_KEY` jest używany wyłącznie po stronie backendu,
- system nie wysyła maili i nie wykonuje automatycznych działań administracyjnych,
- każda odpowiedź AI wymaga weryfikacji przez agenta,
- do modelu nie jest przekazywany `requester_email`,
- przy braku wystarczających źródeł model powinien wskazać potrzebę dalszej analizy przez pracownika IT.

## Reindeksacja bazy wiedzy

```bash
cd backend
source .venv/bin/activate
python scripts/reindex_knowledge_embeddings.py
python scripts/reindex_knowledge_embeddings.py --force
python scripts/reindex_knowledge_embeddings.py --limit 10
```

Reindeksację należy uruchomić po seedowaniu danych oraz po każdej istotnej zmianie treści artykułów.

## Test retrievalu

Można użyć Swagger UI lub bezpośrednio endpointów technicznych:

- `POST /knowledge/search`
- `POST /tickets/{ticket_id}/retrieve-context`
- `POST /knowledge/reindex`

Jeżeli `OPENAI_API_KEY` nie jest ustawiony albo środowisko nie udostępnia `pgvector`, aplikacja zachowuje działanie dzięki fallbackowi do obecnego mechanizmu bag-of-words.

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

### Manualny scenariusz Etapu 11

1. Zaloguj się jako `agent@helpdesk.local`.
2. Otwórz szczegóły zgłoszenia i uruchom analizę AI.
3. Sprawdź, czy karta odpowiedzi pokazuje providera, model, datę, treść maila i źródła RAG.
4. Kliknij „Kopiuj odpowiedź” i zweryfikuj komunikat sukcesu.
5. Kliknij „Zapisz jako odpowiedź agenta” i potwierdź nadpisanie, jeśli pole odpowiedzi agenta było już uzupełnione.
6. Otwórz link do artykułu bazy wiedzy z sekcji źródeł i wystaw feedback dla odpowiedzi AI.

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
- klasyfikacja i priorytetyzacja pozostają rule-based,
- jakość odpowiedzi zależy od jakości treści zgłoszenia i bazy wiedzy,
- odpowiedzi AI mają charakter propozycji i wymagają weryfikacji człowieka,
- system nie wysyła wiadomości e-mail automatycznie,
- retrieval RAG wymaga wcześniejszej reindeksacji po zmianie artykułów,
- standardowe testy SQLite nie uruchamiają realnego pgvector, tylko ścieżki fallbackowe i logikę serwisów,
- brak testów end-to-end frontendu.
