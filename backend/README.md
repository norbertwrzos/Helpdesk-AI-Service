# Backend — Helpdesk AI Service

Backend FastAPI obsługuje zgłoszenia, bazę wiedzy, analizę AI, feedback i metryki jakości.

## Uruchomienie

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_data.py
python scripts/reindex_knowledge_embeddings.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## AI Etap 9 — RAG Foundation

Backend obsługuje obecnie fundament RAG dla bazy wiedzy:

- embeddingi artykułów zapisane w PostgreSQL z użyciem `pgvector`,
- reindeksację całej bazy wiedzy lub pojedynczych artykułów przez serwis backendowy,
- techniczny endpoint `POST /knowledge/search`,
- techniczny endpoint `POST /knowledge/reindex`,
- techniczny endpoint `POST /tickets/{ticket_id}/retrieve-context`,
- fallback do `SimilarityService`, gdy provider embeddingów albo pgvector są niedostępne.

Wymagane zmienne środowiskowe:

- `AI_PROVIDER=mock`
- `OPENAI_API_KEY=`
- `OPENAI_EMBEDDING_MODEL=text-embedding-3-small`
- `RAG_EMBEDDING_PROVIDER=openai`
- `RAG_TOP_K=5`
- `RAG_MIN_SCORE=0.0`

Jeżeli `OPENAI_API_KEY` pozostaje pusty, backend nadal działa, ale retrieval wraca do mechanizmu bag-of-words.

## AI Etap 10 — OpenAI Mail Response Generator

Backend obsługuje teraz dwa providery generowania odpowiedzi mailowej:

- `mock` — lokalny szkic odpowiedzi, bez sieci i bez klucza API,
- `openai` — generowanie szkicu odpowiedzi przez OpenAI Responses API.

Cel etapu polega na generowaniu propozycji odpowiedzi dla agenta, a nie na automatycznej wysyłce wiadomości. Odpowiedź jest zapisywana w `AIResponse.response_text`, natomiast `provider_name`, `model_name` i `sources_used` dokumentują, jak została wygenerowana i z jakich źródeł skorzystano.

Wymagane zmienne środowiskowe dla generowania odpowiedzi:

- `AI_GENERATION_PROVIDER=mock`
- `OPENAI_API_KEY=`
- `OPENAI_CHAT_MODEL=gpt-4o-mini`
- `OPENAI_RESPONSE_TEMPERATURE=0.2`
- `OPENAI_MAX_OUTPUT_TOKENS=1200`

Przykład konfiguracji OpenAI:

```env
AI_GENERATION_PROVIDER=openai
OPENAI_API_KEY=twoj_klucz
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_RESPONSE_TEMPERATURE=0.2
OPENAI_MAX_OUTPUT_TOKENS=1200
```

Fallback do `mock` działa w dwóch sytuacjach:

- gdy `AI_GENERATION_PROVIDER=openai`, ale brakuje `OPENAI_API_KEY`,
- gdy wywołanie OpenAI zakończy się błędem w trakcie analizy ticketu.

Format generowanej odpowiedzi:

```text
Dzień dobry,

[krótkie odniesienie do problemu użytkownika]

[proponowane kroki rozwiązania]

[co zrobić, jeśli problem nadal występuje]

Pozdrawiam,
[imię agenta]
```

Bezpieczeństwo:

- klucz OpenAI pozostaje wyłącznie w backendzie,
- backend nie wysyła wiadomości e-mail,
- każda odpowiedź AI wymaga weryfikacji przez agenta,
- do modelu nie są przekazywane dane niepotrzebne do wygenerowania szkicu, w tym `requester_email`.

## Testy

```bash
source .venv/bin/activate
pytest
```

## Migracje

Repozytorium używa jednej czystej migracji bazowej zgodnej z aktualnym schematem prototypu.

Jeśli lokalna baza pochodzi sprzed cleanupu migracji:

```bash
docker compose down -v
docker compose up -d
source .venv/bin/activate
alembic upgrade head
python scripts/seed_data.py
python scripts/reindex_knowledge_embeddings.py
```

Jeżeli baza ma już poprawny schemat, ale Alembic nadal wskazuje usuniętą rewizję `007_remove_email_features`, wykonaj:

```bash
source .venv/bin/activate
alembic stamp 001_initial --purge
alembic upgrade head
```

Nowa migracja `002_knowledge_article_embeddings` wymaga obrazu PostgreSQL z `pgvector`.

Weryfikacja rozszerzenia:

```bash
docker compose exec postgres psql -U helpdesk -d helpdesk_ai -c "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
```

## Reindeksacja i testy techniczne

```bash
source .venv/bin/activate
python scripts/reindex_knowledge_embeddings.py
pytest app/tests/test_hash_utils.py app/tests/test_mock_embedding_provider.py app/tests/test_knowledge_embedding_service.py app/tests/test_rag_retriever.py app/tests/test_rag_endpoints.py app/tests/test_prompt_builder.py app/tests/test_mock_ai_provider.py app/tests/test_openai_provider.py app/tests/test_analysis_pipeline_openai_mode.py
```

Retrieval można przetestować przez Swagger UI na endpointach `POST /knowledge/search` i `POST /tickets/{ticket_id}/retrieve-context`.
Generowanie odpowiedzi mailowej można przetestować przez `POST /tickets/{ticket_id}/analyze`.
