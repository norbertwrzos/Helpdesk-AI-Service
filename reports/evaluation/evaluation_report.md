# Raport ewaluacji modułu analizy zgłoszeń

**Data wygenerowania:** 28.05.2026 17:13 UTC  
**Liczba przypadków testowych:** 64  
**Wersja pipeline'u:** mock/rule-based (etap 6)

---

## 1. Metodyka testów

Ewaluacja przeprowadzona na syntetycznym zbiorze zgłoszeń (`evaluation_tickets.csv`).
Każde zgłoszenie zawiera etykiety referencyjne (`expected_category`, `expected_priority`),
które zostały przypisane ręcznie przez autora systemu na podstawie treści zgłoszenia.

Dla każdego zgłoszenia uruchomiono:
- `ClassificationService` — klasyfikacja kategorii na podstawie reguł słów kluczowych,
- `PriorityAnalysisService` — priorytetyzacja na podstawie reguł słów kluczowych,
- `MockAIGenerator` — generowanie odpowiedzi na podstawie szablonu.

Usługi uruchomiono bezpośrednio (bez zapisu do bazy danych).
Kategorie i priorytety wczytano z plików seed (`data/seed/`).

---

## 2. Wyniki klasyfikacji kategorii

| Metryka | Wartość |
|---------|---------|
| Accuracy | **70.31%** (45/64) |
| Macro F1 | **0.6742** |
| Weighted F1 | **0.6913** |

### Szczegółowe metryki per kategoria

| Etykieta | Precision | Recall | F1-score | Support |
|----------|-----------|--------|----------|---------|
| Konto i dostęp | 0.5000 | 0.6250 | 0.5556 | 8 |
| Sieć i VPN | 1.0000 | 0.8889 | 0.9412 | 9 |
| Aplikacje biznesowe | 0.7000 | 0.7778 | 0.7368 | 9 |
| Sprzęt komputerowy | 0.5333 | 1.0000 | 0.6957 | 8 |
| Poczta e-mail | 1.0000 | 0.8571 | 0.9231 | 7 |
| Bezpieczeństwo | 1.0000 | 0.8889 | 0.9412 | 9 |
| System operacyjny | 1.0000 | 0.4286 | 0.6000 | 7 |
| Inne | 0.0000 | 0.0000 | 0.0000 | 7 |

---

## 3. Wyniki priorytetyzacji

| Metryka | Wartość |
|---------|---------|
| Accuracy | **65.62%** (42/64) |
| Macro F1 | **0.6945** |
| Weighted F1 | **0.6551** |

### Szczegółowe metryki per priorytet

| Etykieta | Precision | Recall | F1-score | Support |
|----------|-----------|--------|----------|---------|
| Niski | 1.0000 | 0.4000 | 0.5714 | 25 |
| Średni | 0.4595 | 1.0000 | 0.6296 | 17 |
| Wysoki | 0.8182 | 0.6429 | 0.7200 | 14 |
| Krytyczny | 1.0000 | 0.7500 | 0.8571 | 8 |

---

## 4. Ocena jakości generowanych odpowiedzi

| Metryka | Wartość |
|---------|---------|
| Średnia ocena jakości (0–5) | **4.16** |
| Średnia długość odpowiedzi (znaki) | **541** |

Ocena jakości odpowiedzi opiera się na 5 kryteriach heurystycznych:
1. Odpowiedź nie jest pusta (+1 pkt),
2. Zawiera co najmniej jedno oczekiwane słowo kluczowe (+1 pkt),
3. Zawiera co najmniej połowę oczekiwanych słów kluczowych (+1 pkt),
4. Zawiera sugestię diagnostyczną lub kroki rozwiązania (+1 pkt),
5. Zawiera informację o weryfikacji przez IT Support (+1 pkt).

---

## 5. Najczęstsze błędy klasyfikacji

### Błędy kategorii (oczekiwana → przewidziana)

| Błąd klasyfikacji | Liczba |
|-------------------|--------|
| Inne → Sprzęt komputerowy | 4 |
| Konto i dostęp → Inne | 3 |
| System operacyjny → Sprzęt komputerowy | 3 |
| Aplikacje biznesowe → Konto i dostęp | 2 |
| Inne → Aplikacje biznesowe | 2 |

### Błędy priorytetu (oczekiwany → przewidziany)

| Błąd priorytetu | Liczba |
|-----------------|--------|
| Niski → Średni | 15 |
| Wysoki → Średni | 5 |
| Krytyczny → Wysoki | 2 |

---

## 6. Ograniczenia ewaluacji

1. **Dane syntetyczne** — zbiór testowy został wygenerowany ręcznie przez autora.
   Może nie odzwierciedlać pełnej różnorodności rzeczywistych zgłoszeń.
2. **Pipeline rule-based** — klasyfikacja opiera się na słowach kluczowych,
   a nie na prawdziwym modelu ML/NLP. Wyniki nie są reprezentatywne
   dla metod uczenia maszynowego.
3. **Ocena odpowiedzi heurystyczna** — jakość odpowiedzi oceniana jest
   na podstawie prostych reguł, a nie przez eksperta dziedzinowego.
4. **Brak cross-walidacji** — ewaluacja przeprowadzona jednorazowo
   na całym zbiorze testowym.
5. **Brak danych produkcyjnych** — wyniki odnoszą się wyłącznie
   do prototypowego etapu systemu.

---

## 7. Wnioski do pracy inżynierskiej

Przeprowadzona ewaluacja prototypowego pipeline'u rule-based pozwala na:

- Określenie **bazowych metryk** przed wdrożeniem właściwych modeli AI/NLP.
  Accuracy klasyfikacji kategorii: **70.31%**,
  accuracy priorytetyzacji: **65.62%**.
- Identyfikację **słabych punktów** systemu rule-based —
  najczęstsze błędy wynikają z nakładania się słów kluczowych
  między kategoriami (np. Konto i dostęp vs Aplikacje biznesowe).
- Zdefiniowanie **punktu odniesienia** (baseline) dla przyszłego porównania
  z modelami opartymi na embeddingach lub fine-tunowanych modelach językowych.
- Weryfikację, że **MockAIGenerator** generuje odpowiedzi zawierające
  kroki diagnostyczne i odwołanie do IT Support, co jest poprawną
  charakterystyką odpowiedzi helpdesk.

Wyniki ewaluacji zostaną przedstawione w rozdziale
"Testowanie systemu" pracy inżynierskiej jako porównanie
podejścia rule-based z podejściem AI/NLP (etap 7+).

---

*Raport wygenerowany automatycznie przez skrypt `backend/scripts/run_evaluation.py`.*
