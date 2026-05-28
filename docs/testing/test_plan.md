# Plan testów — Helpdesk AI Service

## 1. Cel testów

Celem testów jest weryfikacja poprawności działania prototypowego systemu helpdesk,
ze szczególnym uwzględnieniem modułów analizy zgłoszeń:

- klasyfikacji kategorii,
- nadawania priorytetów,
- generowania odpowiedzi AI (mock/rule-based),
- importu zgłoszeń z poczty e-mail,
- mechanizmu feedbacku i metryk jakości.

Testy mają na celu wyznaczenie **bazowych metryk** pipeline'u rule-based
przed ewentualnym wdrożeniem prawdziwych modeli AI/NLP.

---

## 2. Zakres testów

### Testowane komponenty

| Komponent | Rodzaj testów |
|-----------|---------------|
| Endpointy CRUD (zgłoszenia, kategorie, priorytety) | Integracyjne (pytest + httpx) |
| AnalysisPipeline | Integracyjne + jednostkowe |
| ClassificationService | Jednostkowe |
| PriorityAnalysisService | Jednostkowe |
| MockAIGenerator | Jednostkowe |
| EmailImporter / EmailParser | Jednostkowe |
| FeedbackService | Integracyjne |
| QualityMetricsService | Integracyjne |
| EvaluationRunner | Jednostkowe |
| metrics.py | Jednostkowe |
| answer_quality.py | Jednostkowe |
| report_writer.py | Jednostkowe |

### Poza zakresem testów

- Testy wydajnościowe i obciążeniowe.
- Testy bezpieczeństwa (penetracyjne).
- Testy end-to-end interfejsu użytkownika (frontend).
- Testy prawdziwych modeli ML/NLP (nie są zaimplementowane).
- Integracja z zewnętrznymi API (OpenAI, SMTP produkcyjny).

---

## 3. Dane testowe

### Dane syntetyczne — zbiór ewaluacyjny

Plik: `data/test_cases/evaluation_tickets.csv`

- 64 syntetyczne zgłoszenia w języku polskim,
- każde zgłoszenie ma etykiety referencyjne: `expected_category` i `expected_priority`,
- dane nie zawierają danych osobowych ani rzeczywistych danych firmowych,
- bezpieczne do publikacji w repozytorium,
- kategorie i priorytety zgodne z danymi seed (`data/seed/`).

### Dane seed

Pliki: `data/seed/categories.json`, `data/seed/priorities.json`, `data/seed/knowledge_base.json`

Używane do:
- inicjalizacji bazy danych,
- ewaluacji bez połączenia z bazą (stub-obiekty).

---

## 4. Testowane moduły

### 4.1 ClassificationService

- Reguły słów kluczowych dla 7 kategorii + domyślna "Inne".
- Testowane przypadki: jednoznaczne, niejednoznaczne, wielosłowne.
- Plik testów: `backend/app/tests/test_classification_service.py`

### 4.2 PriorityAnalysisService

- Reguły priorytetyzacji: Krytyczny, Wysoki, Średni, Niski.
- Domyślny priorytet Średni, gdy brak dopasowania.
- Plik testów: `backend/app/tests/test_priority_service.py`

### 4.3 AnalysisPipeline

- Pełny przepływ: klasyfikacja → priorytet → podobne artykuły → odpowiedź AI.
- Plik testów: `backend/app/tests/test_analysis_pipeline.py`

### 4.4 Moduł ewaluacji

- `metrics.py` — testy metryk (accuracy, F1, confusion matrix).
- `answer_quality.py` — testy oceny jakości odpowiedzi.
- `evaluator.py` — testy integracyjne runnera.
- Pliki testów: `backend/app/tests/test_evaluation_*.py`

---

## 5. Metryki oceny jakości

### Klasyfikacja kategorii i priorytetyzacja

| Metryka | Opis |
|---------|------|
| Accuracy | Odsetek poprawnych klasyfikacji |
| Precision (per label) | TP / (TP + FP) |
| Recall (per label) | TP / (TP + FN) |
| F1-score (per label) | Harmoniczna średnia precision i recall |
| Macro F1 | Średnia F1 ze wszystkich etykiet (równe wagi) |
| Weighted F1 | Średnia F1 ważona liczebnością etykiet |

### Jakość odpowiedzi AI

Skala 0–5 pkt (heurystyczna):
1. Odpowiedź nie jest pusta,
2. Zawiera co najmniej jedno oczekiwane słowo kluczowe,
3. Zawiera co najmniej połowę oczekiwanych słów kluczowych,
4. Zawiera sugestię diagnostyczną lub kroki rozwiązania,
5. Zawiera informację o weryfikacji przez IT Support.

---

## 6. Ograniczenia

1. **Dane syntetyczne** — zbiór ewaluacyjny nie pochodzi z rzeczywistych systemów helpdesk.
2. **Pipeline rule-based** — wyniki nie są reprezentatywne dla modeli AI/NLP.
3. **Brak cross-walidacji** — ewaluacja jednorazowa na całym zbiorze.
4. **Ocena odpowiedzi heurystyczna** — brak oceny eksperckiej przez człowieka.
5. **Brak danych produkcyjnych** — wyniki dotyczą wyłącznie prototypu.

---

## 7. Środowisko testowe

| Element | Wersja/Konfiguracja |
|---------|---------------------|
| Python | 3.12 |
| Framework testowy | pytest 8.3.4 |
| Klient HTTP | httpx 0.28.1 |
| Baza danych (testy) | SQLite (in-memory) |
| Backend | FastAPI 0.115.5 |

### Uruchomienie testów

```bash
cd backend
source .venv/bin/activate
pytest app/tests/ -v
```

### Uruchomienie ewaluacji batchowej

```bash
cd backend
source .venv/bin/activate
python scripts/run_evaluation.py
```
