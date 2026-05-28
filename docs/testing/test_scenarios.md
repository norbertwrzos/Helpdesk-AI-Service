# Scenariusze testowe — Helpdesk AI Service

Dokument opisuje scenariusze testowe dla głównych funkcjonalności systemu.
Scenariusze podzielono na testy manualne (MT) i automatyczne (AT).

---

## MT-01: Dodanie zgłoszenia ręcznie

**Cel:** Weryfikacja możliwości ręcznego dodania zgłoszenia przez API i frontend.

**Kroki:**
1. Otwórz interfejs frontendowy (`http://localhost:5173`).
2. Kliknij „Nowe zgłoszenie".
3. Wypełnij formularz: tytuł „Test VPN", opis „Nie mogę połączyć się z VPN".
4. Zatwierdź formularz.
5. Sprawdź, czy zgłoszenie pojawiło się na liście.
6. Sprawdź status zgłoszenia (powinien być „Nowe").

**Oczekiwany wynik:**
- Zgłoszenie zostało zapisane z poprawnym tytułem i opisem.
- Status to `new`.
- Źródło to `manual`.

**Walidacja API:**
```
POST /api/v1/tickets
Body: {"title": "Test VPN", "description": "Nie mogę połączyć się z VPN."}
Oczekiwany kod: 201
```

---

## MT-02: Analiza zgłoszenia VPN

**Cel:** Weryfikacja poprawności klasyfikacji i priorytetyzacji zgłoszenia VPN.

**Kroki:**
1. Utwórz zgłoszenie: tytuł „VPN nie działa", opis „Klient VPN zwraca błąd połączenia".
2. Uruchom analizę: `POST /api/v1/tickets/{id}/analyze`.
3. Sprawdź wynik analizy.

**Oczekiwany wynik:**
- `category_name` = „Sieć i VPN"
- `priority_name` = „Średni" (brak słów krytycznych)
- Odpowiedź AI zawiera kroki diagnostyczne dla VPN.
- Odpowiedź AI zawiera zdanie o weryfikacji przez IT Support.

**Weryfikacja:**
```
GET /api/v1/tickets/{id}
Sprawdź: category, priority, ostatnia odpowiedź AI
```

---

## MT-03: Analiza zgłoszenia z problemem logowania

**Cel:** Weryfikacja klasyfikacji zgłoszenia jako „Konto i dostęp".

**Kroki:**
1. Utwórz zgłoszenie: tytuł „Nie mogę się zalogować", opis „Pojawia się błąd logowania".
2. Uruchom analizę: `POST /api/v1/tickets/{id}/analyze`.
3. Sprawdź kategorię i priorytet.

**Oczekiwany wynik:**
- `category_name` = „Konto i dostęp"
- `priority_name` = „Średni"
- Odpowiedź AI zawiera kroki dotyczące resetowania hasła.

---

## MT-04: Analiza incydentu bezpieczeństwa

**Cel:** Weryfikacja poprawnej klasyfikacji phishingu i nadania wysokiego priorytetu.

**Kroki:**
1. Utwórz zgłoszenie: tytuł „Podejrzana wiadomość", opis „Dostałem e-mail wyglądający jak phishing".
2. Uruchom analizę.

**Oczekiwany wynik:**
- `category_name` = „Bezpieczeństwo"
- `priority_name` = „Wysoki"
- Odpowiedź AI zawiera informację o nieklikaniu w linki.
- Odpowiedź AI zawiera informację o zgłoszeniu do działu bezpieczeństwa.

---

## MT-05: Import zgłoszenia z wiadomości e-mail

**Cel:** Weryfikacja importu zgłoszeń przez protokół IMAP (GreenMail).

**Wymagania wstępne:**
- Docker Compose uruchomiony (`docker-compose up`).
- GreenMail dostępny na porcie 3025 (SMTP) i 3143 (IMAP).

**Kroki:**
1. Wyślij testowy e-mail na skrzynkę helpdesk: `python backend/scripts/send_test_email.py`.
2. Uruchom import: `POST /api/v1/email-import/run`.
3. Sprawdź logi importu: `GET /api/v1/email-import/logs`.
4. Sprawdź, czy nowe zgłoszenie pojawiło się na liście: `GET /api/v1/tickets`.

**Oczekiwany wynik:**
- Import statusu `imported`.
- Nowe zgłoszenie ze źródłem `email`.
- Temat e-maila jako tytuł zgłoszenia.
- Treść e-maila jako opis zgłoszenia.
- Brak duplikatu przy ponownym imporcie.

---

## MT-06: Ocena odpowiedzi AI (feedback)

**Cel:** Weryfikacja mechanizmu oceny jakości odpowiedzi AI.

**Kroki:**
1. Uruchom analizę dowolnego zgłoszenia.
2. Pobierz ID odpowiedzi AI z wyników analizy.
3. Wystaw ocenę: `POST /api/v1/ai-responses/{id}/feedback`.
   Body: `{"rating": 4, "is_helpful": true, "comment": "Dobra odpowiedź"}`
4. Sprawdź, czy feedback został zapisany: `GET /api/v1/ai-responses/{id}`.

**Oczekiwany wynik:**
- Ocena (rating) zapisana poprawnie.
- `is_helpful` = `true`.
- Komentarz zapisany.

---

## MT-07: Weryfikacja metryk jakości na stronie /quality

**Cel:** Weryfikacja poprawności wyświetlania metryk jakości w interfejsie.

**Kroki:**
1. Uruchom kilka analiz zgłoszeń.
2. Dla każdej odpowiedzi AI wystaw ocenę (różne oceny: 1-5).
3. Otwórz stronę `/quality` w przeglądarce.
4. Sprawdź wyświetlane metryki.

**Oczekiwany wynik:**
- Widoczna liczba odpowiedzi AI.
- Widoczna średnia ocena.
- Widoczny odsetek pomocnych odpowiedzi.

---

## AT-01: Testy jednostkowe ClassificationService

**Cel:** Weryfikacja poprawności reguł klasyfikacji słowami kluczowymi.

**Uruchomienie:**
```bash
cd backend
pytest app/tests/test_classification_service.py -v
```

**Przypadki:**
- Zgłoszenie z „VPN" → „Sieć i VPN".
- Zgłoszenie z „hasło" → „Konto i dostęp".
- Zgłoszenie z „phishing" → „Bezpieczeństwo".
- Zgłoszenie z „drukarka" → „Sprzęt komputerowy".
- Zgłoszenie bez słów kluczowych → „Inne".

---

## AT-02: Testy jednostkowe modułu ewaluacji

**Cel:** Weryfikacja poprawności modułu metrics.py i answer_quality.py.

**Uruchomienie:**
```bash
cd backend
pytest app/tests/test_evaluation_metrics.py app/tests/test_answer_quality.py -v
```

**Przypadki:**
- `accuracy_score`: 100% trafień, 0% trafień, wynik częściowy.
- `macro_f1`: wynik idealny, wynik zerowy.
- `confusion_matrix_as_dict`: poprawne zliczenia TP/FP/FN.
- `evaluate_answer_quality`: pusta odpowiedź = 0 pkt, pełna odpowiedź = 5 pkt.

---

## AT-03: Ewaluacja batchowa na zbiorze 64 zgłoszeń

**Cel:** Weryfikacja działania EvaluationRunner na pełnym zbiorze testowym.

**Uruchomienie:**
```bash
cd backend
python scripts/run_evaluation.py
```

**Oczekiwany wynik:**
- Skrypt kończy się bez błędów.
- W `reports/evaluation/` generowane są 3 pliki.
- W terminalu widoczne metryki: accuracy, macro F1, jakość odpowiedzi.
- Raport `evaluation_report.md` jest czytelny i po polsku.

---

## AT-04: Testy integracyjne AnalysisPipeline

**Cel:** Weryfikacja pełnego przepływu analizy zgłoszenia.

**Uruchomienie:**
```bash
cd backend
pytest app/tests/test_analysis_pipeline.py -v
```

**Oczekiwane wyniki:**
- Wszystkie testy przechodzą.
- Pipeline nie modyfikuje istniejących zgłoszeń poza analizowanym.

---

## AT-05: Testy istniejących endpointów po zmianach Etapu 6

**Cel:** Weryfikacja, że Etap 6 nie psuje istniejących endpointów.

**Uruchomienie:**
```bash
cd backend
pytest app/tests/ -v
```

**Oczekiwany wynik:**
- Wszystkie istniejące testy przechodzą.
- Nowe testy modułu ewaluacji przechodzą.
- Brak regresji w endpointach CRUD, analizy, importu e-mail, feedbacku.
