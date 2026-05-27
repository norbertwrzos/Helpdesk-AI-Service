# Etap 3 — AnalysisPipeline z mockową logiką AI/NLP

## Kontekst

W Etapie 3 systemu Helpdesk AI Service zaimplementowano pełen przepływ analizy zgłoszenia technicznegoz użyciem mock/rule-based implementacji komponentów AI/NLP.

## Problem i uzasadnienie decyzji

### Dlaczego mock zamiast prawdziwego modelu AI?

Na etapie 3 projektu praca inżynierska wymaga:

1. **Działającego przepływu end-to-end** — od zgłoszenia do wygenerowanej odpowiedzi.
2. **Testowalności** — komponenty mockowe są w pełni deterministyczne, co umożliwia pisanie testów jednostkowych i integracyjnych.
3. **Niskich kosztów** — brak konieczności integracji z płatnym API (OpenAI) na etapie projektowania architektury.
4. **Szybkości iteracji** — mockowe klasy pozwalają skupić się na architekturze systemu.
5. **Gotowości do wymiany** — każdy komponent jest zaprojektowany tak, aby w przyszłości można było go zastąpić prawdziwą implementacją AI/NLP.

## Komponenty AnalysisPipeline

```
POST /tickets/{ticket_id}/analyze
          │
          ▼
  AnalysisPipeline.analyze_ticket()
          │
    ┌─────┴──────────────────────────────────┐
    │                                        │
    ▼                                        ▼
ClassificationService              PriorityAnalysisService
(reguły słów kluczowych)           (reguły słów kluczowych)
    │                                        │
    └─────────────────┬──────────────────────┘
                      │
                      ▼
               SimilarityService
             (bag-of-words matching)
                      │
                      ▼
              MockAIGenerator
            (szablon po polsku)
                      │
                      ▼
           Zapis AIResponse w bazie
           Aktualizacja Ticket
                      │
                      ▼
              AnalysisResult (JSON)
```

### ClassificationService (`classification_service.py`)

- **Metoda**: reguły słów kluczowych (keyword matching).
- **Wejście**: title, description, lista kategorii z bazy.
- **Wyjście**: `ClassificationResult` z category_id, category_name, confidence, explanation.
- **Przyszła wymiana**: zastąpienie przez klasyfikator oparty na embeddingach (np. Sentence Transformers) lub wywołanie API modelu językowego.

### PriorityAnalysisService (`priority_analysis_service.py`)

- **Metoda**: reguły słów kluczowych z hierarchią priorytetów.
- **Wejście**: title, description, lista priorytetów z bazy.
- **Wyjście**: `PriorityResult` z priority_id, priority_name, confidence, explanation.
- **Przyszła wymiana**: zastąpienie przez model regresji lub klasyfikacji wieloklasowej.

### SimilarityService (`similarity_service.py`)

- **Metoda**: Jaccard similarity (bag-of-words) z bonusem za zgodność kategorii.
- **Wejście**: title, description, artykuły z bazy wiedzy.
- **Wyjście**: lista `SimilarArticle` (max 3), posortowana wg score.
- **Przyszła wymiana**: zastąpienie przez embedding similarity z pgvector (cosine distance).

### MockAIGenerator (`ai_generator.py`)

- **Metoda**: generowanie odpowiedzi na podstawie szablonu po polsku.
- **Wejście**: ticket, classification result, priority result, similar articles.
- **Wyjście**: `GeneratedAnswer` z response_text, model_name, provider_name, sources_used.
- **Przyszła wymiana**: zastąpienie przez wywołanie OpenAI API (ChatCompletion) lub lokalnego modelu LLM.

## Jak podmienić mock na prawdziwy model AI

Każdy komponent jest klasą z jedną metodą publiczną. `AnalysisPipeline` przyjmuje je przez konstruktor (wstrzykiwanie zależności):

```python
class AnalysisPipeline:
    def __init__(
        self,
        classifier: ClassificationService | None = None,
        priority_analyzer: PriorityAnalysisService | None = None,
        similarity: SimilarityService | None = None,
        ai_generator: MockAIGenerator | None = None,
    ) -> None: ...
```

Aby zastąpić np. `ClassificationService` prawdziwym modelem:

1. Utwórz `MLClassificationService` z tą samą sygnaturą metody `classify()`.
2. Zwróć `ClassificationResult` z taką samą strukturą.
3. Wstrzyknij do `AnalysisPipeline`:
   ```python
   pipeline = AnalysisPipeline(classifier=MLClassificationService())
   ```

Nie trzeba zmieniać kodu w routerach, schematach ani testach integracyjnych.

## Ograniczenia obecnego podejścia

| Ograniczenie | Opis |
|---|---|
| Brak semantyki | Reguły słów kluczowych nie rozumieją kontekstu — „odblokowanie konta" i „zablokowanie konta" są traktowane tak samo. |
| Brak uczenia się | System nie poprawia się na podstawie historycznych zgłoszeń. |
| Słaba generalizacja | Nowe słowa kluczowe muszą być ręcznie dodawane do reguł. |
| Brak embeddingów | Wyszukiwanie podobnych artykułów jest oparte na prostym bag-of-words, nie na semantycznym podobieństwie. |
| Szablonowe odpowiedzi | MockAIGenerator generuje przewidywalne odpowiedzi ze stałego szablonu. |

## Następne kroki (Etap 5+)

- Zastąpienie `ClassificationService` klasyfikatorem opartym na embeddingach (Sentence Transformers, `all-MiniLM-L6-v2`).
- Zastąpienie `SimilarityService` wyszukiwaniem opartym na pgvector (cosine similarity).
- Zastąpienie `MockAIGenerator` wywołaniem OpenAI ChatCompletion API lub lokalnego Ollama.
- Dodanie feedbacku użytkownika i mechanizmu uczenia się na bazie ocen odpowiedzi.
