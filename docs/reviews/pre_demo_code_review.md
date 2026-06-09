# Pre-demo Code Review

Etap 12.5 — Pre-demo Code Review & Simplification
Data przeglądu: 9 czerwca 2026

## 1. Cel przeglądu

Celem przeglądu jest przygotowanie kodu projektu Helpdesk AI Service do Etapu 13, czyli
wersji demonstracyjnej oraz materiałów do pracy inżynierskiej. Przegląd ma charakter
porządkujący: usuwa martwy kod, oczywiste duplikaty oraz nieaktualne fragmenty
dokumentacji, nie zmieniając przy tym zachowania aplikacji z punktu widzenia użytkownika.
W ramach etapu nie dodano żadnych nowych funkcji biznesowych, nie przebudowano
architektury i nie usunięto żadnych mechanizmów bezpieczeństwa (fallbacków).

## 2. Zakres przeglądu

Przeglądem objęto następujące obszary:

- **backend** — FastAPI, routery, serwisy, modele, schematy, konfiguracja,
- **frontend** — React + TypeScript + Vite, strony, komponenty, typy, narzędzia,
- **RAG** — `RagRetriever`, `KnowledgeEmbeddingService`, providerzy embeddingów, fallback do `SimilarityService`,
- **OpenAI provider** — `BaseAIResponseProvider`, `MockAIResponseProvider`, `OpenAIResponseProvider`, `prompt_builder`, factory providerów,
- **ewaluacja** — offline evaluator, metryki RAG i jakości odpowiedzi mailowej,
- **testy** — pytest (backend), build TypeScript (frontend),
- **dokumentacja** — `README.md`, `docs/ai`, `docs/reviews`,
- **konfiguracja** — `backend/.env.example`, `backend/app/core/config.py`, `docker-compose.yml`.

## 3. Najważniejsze obserwacje

1. Backend jest w dobrym stanie: wszystkie 8 routerów jest zarejestrowanych w `app/main.py`,
   a wszystkie 14 serwisów jest realnie używanych (przez routery, pipeline, skrypty lub ewaluator).
2. Provider factory dla generowania odpowiedzi i embeddingów jest prosta i bezpieczna —
   brak `OPENAI_API_KEY` powoduje przewidywalny fallback do providerów `mock`.
3. `prompt_builder` nie przekazuje `requester_email` do modelu, co potwierdza dedykowany test.
4. Frontend zawierał kilka jednoznacznie martwych plików: nieroutowane strony oraz
   komponenty zastąpione w toku wcześniejszych redesignów.
5. W warstwie frontendu występowała powtórzona, identyczna logika formatowania daty.
6. W backendzie znaleziono nieaktualny komentarz-placeholder w `app/services/__init__.py`
   opisujący moduły jako „planowane”, mimo że dawno powstały.
7. W typach frontendu istniała zduplikowana, nieużywana definicja interfejsu `AIResponse`.

## 4. Dead code

Usunięty jednoznaczny martwy kod (zweryfikowany brakiem importów i braku routingu):

Strony (frontend):

- `frontend/src/pages/HomePage.tsx` — strona bez żadnej trasy w `App.tsx`.
- `frontend/src/pages/UserPortalPage.tsx` — placeholder z wcześniejszego etapu, zastąpiony trasami `/portal/*`.
- `frontend/src/pages/QualityPage.tsx` — trasa `/quality` przekierowuje do `/ai`; widok jakości realizuje `AIPage`.

Komponenty (frontend):

- `frontend/src/components/QualityMetricsPanel.tsx` — używany wyłącznie przez usuniętą `QualityPage`.
- `frontend/src/components/Layout.tsx` — stary layout zastąpiony przez `AppShell` i `PortalLayout`.
- `frontend/src/components/TicketList.tsx` — zastąpiony przez `TicketsTable`.
- `frontend/src/components/TicketDetails.tsx` — zastąpiony przez `TicketMainPanel` + `TicketPropertiesPanel`.
- `frontend/src/components/TicketForm.tsx` — zastąpiony przez formularz w `NewTicketModal`.
- `frontend/src/components/TicketSourceBadge.tsx` — używany wyłącznie przez usunięte `TicketList` i `TicketDetails`.

Typy (frontend):

- nieużywana definicja interfejsu `AIResponse` w `frontend/src/types/analysis.ts` (aktywna definicja znajduje się w `types/aiResponse.ts`).

## 5. Duplikaty

Ujednolicone duplikaty:

1. **Formatowanie daty** — trzy komponenty/strony (`AIResponseCard`, `TicketPropertiesPanel`,
   `PortalTicketDetailsPage`) zawierały identyczną lokalną funkcję `formatDate`
   (`dateStyle: 'medium', timeStyle: 'short'`). Logikę wydzielono do
   `frontend/src/utils/dateFormat.ts` (`formatDateTime`) i podmieniono w tych trzech miejscach
   bez zmiany formatu wyświetlania.
2. **Zduplikowany typ `AIResponse`** — nieużywaną kopię usunięto z `types/analysis.ts`,
   pozostawiając jedno źródło prawdy w `types/aiResponse.ts`.

Duplikaty świadomie pozostawione (opisane w sekcji 6 i 12):

- pozostałe lokalne funkcje `formatDate` używają różnych formatów (date-only, long/medium),
  więc ich łączenie wymagałoby parametryzacji i zmiany zachowania — pozostawiono jako możliwy dalszy refactor,
- współistnienie `StatusBadge` (klasy Tailwind inline) i `TicketStatusBadge` (klasy CSS),
  gdzie oba są nadal używane (`TicketStatusBadge` przez `RecentTickets`) — ujednolicenie
  zmieniłoby wygląd badge'y, więc pozostawiono bez zmian dla zachowania UX.

## 6. Over-engineering

Przegląd nie wykazał istotnego over-engineeringu wymagającego pilnej interwencji.
Provider factory (`get_ai_response_provider`, `get_embedding_provider`) są krótkie i czytelne
(prosty wybór po nazwie providera z fallbackiem `try/except`). Drobne uproszczenia
(np. ujednolicenie dat) wykonano lokalnie. Większe refaktory (ujednolicenie warstwy badge'y,
pełna parametryzacja formatowania dat) świadomie odłożono jako „możliwy dalszy refactor”,
ponieważ ich wykonanie groziłoby zmianą UX lub było nieproporcjonalne do korzyści przed demo.

## 7. Zmiany backendowe

- Zaktualizowano nieaktualny komentarz-placeholder w `backend/app/services/__init__.py`,
  który opisywał moduły jako „planowane” i wymieniał nazwy plików (`classifier_service.py`,
  `ai_service.py`), które nigdy nie powstały w tej formie. Komentarz zastąpiono zwięzłym,
  aktualnym opisem rzeczywistych modułów. Zmiana jest wyłącznie dokumentacyjna i nie
  wpływa na działanie.

Nie zmieniono logiki żadnego serwisu, routera, modelu ani migracji Alembic.

## 8. Zmiany frontendowe

- Usunięto 9 jednoznacznie martwych plików (3 strony, 5 komponentów, 1 wynikowo martwy badge) — patrz sekcja 4.
- Usunięto nieużywaną definicję typu `AIResponse` z `types/analysis.ts`.
- Dodano `frontend/src/utils/dateFormat.ts` i podmieniono trzy identyczne lokalne funkcje `formatDate`.

Routing, widoki agenta i portalu end_user, tabela zgłoszeń, analiza AI w szczegółach
zgłoszenia oraz feedback pozostają bez zmian funkcjonalnych. Build frontendu przechodzi.

## 9. Zmiany w AI/RAG

W obszarze AI/RAG nie wprowadzono zmian w logice. Zweryfikowano i potwierdzono jako poprawne:

- factory providerów generacji i embeddingów z bezpiecznym fallbackiem do `mock` przy braku klucza,
- brak przekazywania `requester_email` do promptu (potwierdzone testem `test_prompt_builder.py`),
- fallback `RagRetriever` do `SimilarityService` (bag-of-words) przy niedostępności wektorów,
- idempotentność reindeksacji embeddingów (pomijanie artykułów o niezmienionym hashu treści),
- brak realnych wywołań OpenAI w testach (mockowane klienty `FakeOpenAIClient`).

Architektura RAG nie była modyfikowana, ponieważ działa poprawnie.

## 10. Zmiany w dokumentacji

- Dodano niniejszy raport `docs/reviews/pre_demo_code_review.md`.
- Dodano dokument akademicki `docs/ai/ai_etap_12_5_code_review.md`.
- Zaktualizowano `README.md` o sekcję „Etap 12.5 — Code review i uproszczenie implementacji”.
- Nie usunięto żadnych dokumentów `docs/ai` opisujących wcześniejsze etapy AI.

## 11. Testy po review

Oczekiwane komendy i wyniki:

Backend (pytest, bez `OPENAI_API_KEY`):

```bash
cd backend
source .venv/bin/activate
pytest
```

Oczekiwany wynik: wszystkie testy przechodzą (suite działa na fallbacku SQLite, bez realnych wywołań OpenAI).

Frontend (build):

```bash
cd frontend
npm install
npm run build
```

Oczekiwany wynik: `tsc -b` oraz `vite build` kończą się sukcesem (build zweryfikowany — 112 modułów).

Ewaluacja offline:

```bash
cd backend
source .venv/bin/activate
python scripts/run_evaluation.py --mode mock
python scripts/run_evaluation.py --mode rag
```

Tryb `openai_rag` wymaga `OPENAI_API_KEY` oraz jawnej flagi `--allow-openai`.

Reindeksacja embeddingów RAG:

```bash
cd backend
source .venv/bin/activate
python scripts/reindex_knowledge_embeddings.py
```

Reindeksacja jest idempotentna (pomija artykuły o niezmienionym hashu). Pełny tryb wektorowy
wymaga PostgreSQL z `pgvector` oraz `OPENAI_API_KEY`; przy ich braku działa fallback bag-of-words.

## 12. Elementy pozostawione świadomie

- **Mock auth** — logowanie mockowe z rolami `agent`/`end_user` jest celowym ograniczeniem prototypu.
- **Fallback mock dla AI** — `MockAIResponseProvider` i `MockEmbeddingProvider` są mechanizmami
  bezpieczeństwa i nie zostały usunięte.
- **`SimilarityService`** — pozostaje jako fallback dla `RagRetriever`.
- **`MockAIGenerator`** (`ai_generator.py`) — wrapper kompatybilności wykorzystywany przez
  offline evaluator; pozostawiony.
- **Rule-based klasyfikacja i priorytetyzacja** — zgodnie z aktualnym zakresem produktu.
- **Brak automatycznej wysyłki odpowiedzi** — system generuje wyłącznie szkice do weryfikacji.
- **Współistnienie `StatusBadge` i `TicketStatusBadge`** — ujednolicenie zmieniłoby wygląd; odłożone.

## 13. Ryzyka i ograniczenia

- Przegląd celowo nie dotyczył architektury RAG, mechanizmów auth ani migracji bazy danych.
- Nie zmieniano migracji Alembic ani schematu bazy.
- Standardowy pytest działa na SQLite i nie weryfikuje realnego `pgvector`, tylko ścieżki fallbackowe.
- Część duplikatów (formatowanie dat date-only, warstwa badge'y) pozostawiono, aby nie ryzykować
  zmiany UX; opisano je jako możliwy dalszy refactor.
- Usunięto wyłącznie kod zweryfikowany jako martwy (brak importów, brak routingu, brak użycia w testach).

## 14. Wnioski

Kod został uporządkowany: usunięto jednoznaczny martwy kod, ujednolicono oczywiste duplikaty
oraz poprawiono nieaktualną dokumentację, bez zmiany zachowania aplikacji i bez usuwania
mechanizmów bezpieczeństwa. Build frontendu i testy backendu pozostają zielone. Projekt jest
przygotowany do Etapu 13 — wersji demonstracyjnej i materiałów do pracy inżynierskiej.
