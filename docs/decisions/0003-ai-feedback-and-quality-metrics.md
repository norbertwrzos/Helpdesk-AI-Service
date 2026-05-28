# 0003 — Mechanizm oceny odpowiedzi AI i metryki jakości

**Data:** 2026-05-28  
**Status:** Zaakceptowana  
**Etap:** 5  

---

## Kontekst

System generuje odpowiedzi AI dla każdego zgłoszenia technicznego. Bez mechanizmu oceny nie jest możliwe zmierzenie jakości wygenerowanych odpowiedzi ani identyfikacja przypadków, w których model działa źle. Praca inżynierska wymaga możliwości opisania i zmierzenia jakości działania systemu w rozdziale testowym.

---

## Problem

Jak zbierać i prezentować oceny jakości odpowiedzi AI w sposób prosty, działający i możliwy do opisania w pracy inżynierskiej — bez konieczności implementacji uczenia maszynowego na tym etapie?

---

## Decyzja

Zaimplementowano prosty mechanizm feedbacku z następującymi zasadami:

### Model danych

Tabela `feedback` przechowuje:
- `ticket_id` — powiązanie ze zgłoszeniem,
- `ai_response_id` — powiązanie z konkretną odpowiedzią AI (unique — jedna ocena na odpowiedź),
- `rating` (int, 1–5) — ocena numeryczna,
- `is_helpful` (bool, nullable) — flaga pomocności,
- `comment` (text, nullable) — komentarz tekstowy,
- `created_at` — data i czas oceny.

### Strategia: jedna ocena per AIResponse (upsert)

Zamiast dodawać unique constraint na poziomie bazy i obsługiwać wyjątki IntegrityError, logika upsert jest realizowana w `FeedbackService`:
- jeśli feedback dla `ai_response_id` już istnieje → aktualizuje istniejący rekord,
- jeśli nie istnieje → tworzy nowy.

Upraszcza to obsługę błędów po stronie frontendu (zawsze HTTP 200 przy zapisie).

Unique constraint na `ai_response_id` w bazie danych zabezpiecza integralność danych.

---

## Jakie dane są zapisywane

| Pole | Typ | Opis |
|------|-----|------|
| `rating` | int 1–5 | Ocena numeryczna odpowiedzi AI |
| `is_helpful` | bool / null | Czy odpowiedź pomogła rozwiązać problem |
| `comment` | text / null | Opcjonalny komentarz eksperta |
| `created_at` | datetime | Data wystawienia oceny |

---

## Jak feedback wspiera ocenę jakości

1. **Metryki agregatowe** — `GET /quality/ai-responses` zwraca:
   - łączną liczbę odpowiedzi AI i liczbę ocenionych,
   - średnią ocenę w skali 1–5,
   - pokrycie feedbackiem (procent odpowiedzi z oceną),
   - rozkład ocen 1–5,
   - liczbę odpowiedzi pomocnych i niepomocnych.

2. **Historia per zgłoszenie** — `GET /tickets/{id}/ai-responses` zwraca wszystkie odpowiedzi AI wraz z feedbackiem.

3. **Dane testowe** — zebrane oceny stanowią materiał do rozdziału testowego pracy.

---

## Jakie metryki są liczone

| Metryka | Opis |
|---------|------|
| `total_ai_responses` | Łączna liczba wygenerowanych odpowiedzi AI |
| `total_feedback` | Liczba ocenionych odpowiedzi |
| `average_rating` | Średnia arytmetyczna ocen (null jeśli brak ocen) |
| `helpful_count` | Liczba odpowiedzi oznaczonych jako pomocne |
| `not_helpful_count` | Liczba odpowiedzi oznaczonych jako niepomocne |
| `feedback_coverage_percent` | `(total_feedback / total_ai_responses) * 100` |
| `rating_distribution` | Słownik `{"1": n, "2": n, "3": n, "4": n, "5": n}` |
| `responses_without_feedback` | `total_ai_responses - total_feedback` |

---

## Ograniczenia

- Feedback nie wpływa na zachowanie modelu — jest zbierany wyłącznie w celach ewaluacyjnych.
- Brak autoryzacji — każdy użytkownik może wystawić ocenę.
- Metryki nie są podzielone na okresy czasu (brak filtrowania po dacie).
- Brak wykresów — tylko dane tabelaryczne/kafelkowe.
- Jedna ocena per odpowiedź AI — nie można zebrać wielu niezależnych ocen od różnych ekspertów dla tej samej odpowiedzi.

---

## Możliwy rozwój

| Obszar | Opis |
|--------|------|
| Uczenie na feedbacku | Wykorzystanie ocen jako sygnału do fine-tuningu lub reranking odpowiedzi |
| Porównywanie modeli | Metryki rozbite na `model_name` / `provider_name` |
| Monitoring jakości | Alerty, gdy średnia ocena spada poniżej progu |
| Audyt odpowiedzi AI | Przeglądanie odpowiedzi z niską oceną przez eksperta |
| Dashboard jakości | Wykresy trendu ocen, heatmapy kategorii, eksport CSV |
| Multi-user feedback | Wiele ocen per odpowiedź AI, agregacja metodą majority voting |
| Filtrowanie po dacie | Metryki za ostatni tydzień / miesiąc / kwartał |
