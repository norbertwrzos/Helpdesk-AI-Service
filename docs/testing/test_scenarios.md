# Scenariusze testowe — Helpdesk AI Service

Scenariusze obejmują aktualny zakres produktu po cleanupie repozytorium. Podzielono je na testy manualne (MT) i automatyczne (AT).

## MT-01: Dodanie zgłoszenia ręcznie

**Cel:** Potwierdzenie, że agent lub użytkownik końcowy może utworzyć zgłoszenie z formularza.

**Kroki:**
1. Otwórz frontend.
2. Wejdź w „Nowe zgłoszenie”.
3. Wypełnij tytuł, opis oraz dane kontaktowe zgłaszającego.
4. Zapisz formularz.
5. Otwórz listę zgłoszeń.

**Oczekiwany wynik:**
- zgłoszenie jest widoczne na liście,
- status początkowy to `open`,
- źródło zgłoszenia to `manual`.

**Walidacja API:**

```text
POST /tickets
```

## MT-02: Analiza AI zgłoszenia

**Cel:** Potwierdzenie, że analiza AI działa z widoku szczegółów zgłoszenia i kończy się statusem `ai_reviewed`.

**Kroki:**
1. Utwórz zgłoszenie dotyczące VPN lub logowania.
2. Otwórz szczegóły zgłoszenia.
3. Uruchom analizę AI.
4. Odczytaj wynik klasyfikacji, priorytet i wygenerowaną odpowiedź.

**Oczekiwany wynik:**
- zgłoszenie otrzymuje kategorię i priorytet,
- status zmienia się na `ai_reviewed`,
- odpowiedź AI zawiera kroki diagnostyczne.

## MT-03: Odpowiedź agenta na zgłoszenie

**Cel:** Potwierdzenie, że agent może uzupełnić odpowiedź i zaktualizować zgłoszenie.

**Kroki:**
1. Otwórz szczegóły istniejącego zgłoszenia jako agent.
2. Dodaj odpowiedź agenta.
3. Zapisz zmiany.

**Oczekiwany wynik:**
- odpowiedź agenta jest widoczna w szczegółach zgłoszenia,
- zapis nie nadpisuje wyników wcześniejszej analizy AI.

## MT-04: Feedback do odpowiedzi AI

**Cel:** Potwierdzenie działania formularza feedbacku.

**Kroki:**
1. Uruchom analizę AI dla dowolnego zgłoszenia.
2. Dodaj ocenę i komentarz do odpowiedzi AI.
3. Odśwież widok zgłoszenia.

**Oczekiwany wynik:**
- feedback zostaje zapisany,
- metryki jakości uwzględniają nową ocenę.

## MT-05: Zarządzanie bazą wiedzy agenta

**Cel:** Potwierdzenie, że baza wiedzy pozostaje dostępna tylko w panelu agenta.

**Kroki:**
1. Zaloguj się jako agent.
2. Otwórz `Baza wiedzy`.
3. Dodaj lub edytuj artykuł.
4. Zaloguj się jako `end_user`.

**Oczekiwany wynik:**
- agent ma dostęp do widoków `/knowledge` i `/knowledge/:id`,
- `end_user` nie ma osobnej portalowej bazy wiedzy.

## MT-06: Edycja kategorii i priorytetów

**Cel:** Potwierdzenie działania nowej edycji słowników w Ustawieniach.

**Kroki:**
1. Zaloguj się jako agent.
2. Otwórz `Ustawienia -> Kategorie`.
3. Dodaj kategorię i następnie ją edytuj.
4. Otwórz `Ustawienia -> Priorytety`.
5. Dodaj priorytet i następnie go edytuj.

**Oczekiwany wynik:**
- zapisy kończą się powodzeniem,
- lista odświeża się po zmianie,
- brak opcji usuwania kategorii i priorytetów.

## MT-07: Zakres portalu użytkownika końcowego

**Cel:** Potwierdzenie finalnego zakresu roli `end_user`.

**Kroki:**
1. Zaloguj się jako `end_user`.
2. Sprawdź elementy menu bocznego.
3. Spróbuj otworzyć bezpośrednio `/dashboard`, `/tickets`, `/ai`, `/settings`.

**Oczekiwany wynik:**
- portal pokazuje tylko `Moje zgłoszenia`, `Nowe zgłoszenie`, `Profil`,
- trasy panelu agenta są niedostępne dla `end_user`.

## AT-01: Endpointy kategorii i priorytetów

**Uruchomienie:**

```bash
cd backend
source .venv/bin/activate
pytest app/tests/test_categories.py app/tests/test_priorities.py -v
```

**Oczekiwany wynik:**
- przechodzą testy tworzenia,
- przechodzą testy `PATCH`,
- przechodzą przypadki 404 i konfliktu nazw.

## AT-02: Tickety i AnalysisPipeline

**Uruchomienie:**

```bash
cd backend
source .venv/bin/activate
pytest app/tests/test_tickets.py app/tests/test_analysis_pipeline.py -v
```

**Oczekiwany wynik:**
- nowe zgłoszenia mają status `open`,
- analiza kończy się statusem `ai_reviewed`,
- brak regresji w głównym workflow ticketu.

## AT-03: Pełny backend test suite

**Uruchomienie:**

```bash
cd backend
source .venv/bin/activate
pytest
```

## AT-04: Frontend build

**Uruchomienie:**

```bash
cd frontend
npm run build
```

**Oczekiwany wynik:**
- build przechodzi bez błędów typów i routingu.

## AT-05: Ewaluacja offline

**Uruchomienie:**

```bash
cd backend
source .venv/bin/activate
python scripts/run_evaluation.py
```

**Oczekiwany wynik:**
- generowane są raporty w `reports/evaluation/`,
- skrypt kończy się bez błędów.
