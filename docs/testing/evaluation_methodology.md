# Metodyka ewaluacji — Helpdesk AI Service

Dokument opisuje metodykę przeprowadzonej ewaluacji prototypowego pipeline'u
analizy zgłoszeń technicznych.

---

## 1. Zbiór ewaluacyjny — evaluation_tickets.csv

### Opis

Plik `data/test_cases/evaluation_tickets.csv` zawiera 64 syntetyczne zgłoszenia
technicznego działu pomocy (helpdesk).

Każde zgłoszenie składa się z:

| Pole | Opis |
|------|------|
| `id` | Unikalny identyfikator (T001–T064) |
| `title` | Krótki tytuł zgłoszenia |
| `description` | Opis problemu (1–3 zdania) |
| `expected_category` | Referencyjna kategoria problemu |
| `expected_priority` | Referencyjny priorytet zgłoszenia |
| `expected_solution_keywords` | Słowa kluczowe oczekiwane w odpowiedzi (separator: `;`) |
| `notes` | Uwagi o charakterze przypadku testowego |

### Geneza danych

Dane zostały wygenerowane **ręcznie przez autora systemu** na potrzeby
ewaluacji prototypu. Nie pochodzą z rzeczywistych systemów helpdesk.

Dane są:
- syntetyczne i bezpieczne do publikacji w repozytorium,
- wolne od danych osobowych i firmowych,
- zaprojektowane tak, aby pokrywać różne kombinacje kategorii i priorytetów.

### Rozkład klas

Zbiór zawiera przypadki ze wszystkich 8 kategorii i 4 poziomów priorytetu,
uwzględniając zarówno przypadki **jednoznaczne** (bezpośrednie dopasowanie słów
kluczowych), jak i **niejednoznaczne** (np. zgłoszenia dotyczące wielu kategorii).

---

## 2. Definicja expected_category

Etykieta `expected_category` reprezentuje kategorię, którą **człowiek**
(autor systemu) przypisałby danemu zgłoszeniu na podstawie jego treści.

Kategorie:

| Kategoria | Typowe słowa kluczowe |
|-----------|----------------------|
| Konto i dostęp | hasło, logowanie, konto, uprawnienia |
| Sieć i VPN | VPN, sieć, internet, wifi, router |
| Aplikacje biznesowe | CRM, ERP, aplikacja, system sprzedażowy |
| Sprzęt komputerowy | laptop, drukarka, monitor, klawiatura |
| Poczta e-mail | Outlook, mail, wiadomość, skrzynka |
| Bezpieczeństwo | phishing, wirus, incydent, malware |
| System operacyjny | Windows, aktualizacja, sterownik, blue screen |
| Inne | brak wyraźnego dopasowania |

W przypadkach **niejednoznacznych** (np. zgłoszenie zawierające zarówno „CRM"
jak i „dostęp"), jako oczekiwaną kategorię przyjęto tę, którą **dominujący
kontekst problemu** sugeruje w ocenie eksperta.

---

## 3. Definicja expected_priority

Etykieta `expected_priority` reprezentuje priorytet, który **człowiek**
przypisałby danemu zgłoszeniu na podstawie jego treści i kontekstu.

Priorytety:

| Priorytet | Definicja |
|-----------|-----------|
| Niski | Zgłoszenie nie blokuje pracy; prośba lub pytanie |
| Średni | Zgłoszenie utrudnia pracę, ale istnieje obejście |
| Wysoki | Zgłoszenie blokuje pracę użytkownika lub zespołu |
| Krytyczny | Awaria wpływająca na wiele osób lub ciągłość firmy |

W zidentyfikowanych przypadkach, gdzie systemowa reguła może być niezgodna
z ludzką oceną, `expected_priority` odzwierciedla **ocenę eksperta**, a nie
wynik reguł systemowych.

---

## 4. Obliczanie Accuracy

Accuracy (dokładność) klasyfikacji wyraża się wzorem:

$$
\text{Accuracy} = \frac{\text{TP}_{\text{total}}}{\text{N}}
$$

gdzie:
- $\text{TP}_{\text{total}}$ — całkowita liczba poprawnych klasyfikacji,
- $\text{N}$ — całkowita liczba przypadków testowych.

W implementacji:

```python
def accuracy_score(y_true, y_pred):
    return sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)
```

Accuracy jest obliczana osobno dla klasyfikacji kategorii i priorytetyzacji.

---

## 5. Obliczanie Precision, Recall i F1-score

Dla każdej klasy (etykiety) $c$ oblicza się:

$$
\text{Precision}_c = \frac{\text{TP}_c}{\text{TP}_c + \text{FP}_c}
$$

$$
\text{Recall}_c = \frac{\text{TP}_c}{\text{TP}_c + \text{FN}_c}
$$

$$
\text{F1}_c = \frac{2 \cdot \text{Precision}_c \cdot \text{Recall}_c}{\text{Precision}_c + \text{Recall}_c}
$$

gdzie:
- $\text{TP}_c$ — true positives: prawidłowo przewidziane jako klasa $c$,
- $\text{FP}_c$ — false positives: błędnie przewidziane jako klasa $c$,
- $\text{FN}_c$ — false negatives: pominięte przypadki klasy $c$.

### Macro F1

Makro-średnie F1 nadaje **równe wagi** wszystkim klasom:

$$
\text{Macro F1} = \frac{1}{|C|} \sum_{c \in C} \text{F1}_c
$$

### Weighted F1

Ważone F1 uwzględnia **liczebnośc każdej klasy**:

$$
\text{Weighted F1} = \frac{\sum_{c \in C} \text{F1}_c \cdot \text{support}_c}{N}
$$

---

## 6. Ocena jakości odpowiedzi AI

Ponieważ odpowiedzi generuje **MockAIGenerator** (system oparty na szablonach),
ocena jakości ma charakter **heurystyczny** i nie wymaga oceny przez człowieka.

### Kryteria oceny (0–5 pkt)

| Kryterium | Punkty | Opis |
|-----------|--------|------|
| Odpowiedź nie jest pusta | 1 | Minimalny warunek konieczny |
| Co najmniej jedno słowo kluczowe | 1 | Z expected_solution_keywords |
| Co najmniej połowa słów kluczowych | 1 | ≥ 50% oczekiwanych słów |
| Sugestia diagnostyczna | 1 | Zawiera „sprawdź", „zrestartuj" itp. |
| Informacja o IT Support | 1 | Zawiera „IT Support", „dział IT" itp. |

### Interpretacja

| Wynik | Interpretacja |
|-------|---------------|
| 0–1 | Odpowiedź nieużyteczna |
| 2–3 | Odpowiedź częściowo pomocna |
| 4 | Odpowiedź dobra |
| 5 | Odpowiedź pełna i zgodna z oczekiwaniami |

---

## 7. Charakter prototypowy ewaluacji

Przeprowadzona ewaluacja ma charakter **prototypowy** z następujących powodów:

1. **Pipeline rule-based** — klasyfikacja opiera się na predefiniowanej liście
   słów kluczowych, a nie na modelu ML. Wyniki nie są reprezentatywne
   dla rozwiązań AI/NLP.

2. **Dane syntetyczne** — zbiór testowy zaprojektowany ręcznie może nie
   odzwierciedlać rzeczywistego rozkładu zgłoszeń w produkcyjnym systemie.

3. **Brak cross-walidacji** — ewaluacja jednorazowa na całym zbiorze.
   W właściwej ewaluacji należałoby zastosować k-krotną walidację krzyżową.

4. **Brak niezależnego eksperta** — etykiety referencyjne nie były weryfikowane
   przez zewnętrznego eksperta dziedzinowego.

5. **Brak miar dla odpowiedzi** — ocena odpowiedzi AI opiera się wyłącznie
   na prostych regułach, a nie na metrykach NLG (BLEU, ROUGE, BERTScore).

---

## 8. Możliwości rozbudowy ewaluacji

W kolejnych etapach rozwoju systemu ewaluacja może być rozszerzona o:

1. **Prawdziwy model ML** — zastąpienie reguł słów kluczowych klasyfikatorem
   (np. SVM, Random Forest, fine-tuned BERT).

2. **Embeddingi i pgvector** — wyszukiwanie podobnych artykułów oparte
   na semantycznych embeddingach zamiast bag-of-words.

3. **OpenAI API** — zastąpienie MockAIGenerator prawdziwym modelem językowym
   i ocena odpowiedzi metrykami NLG.

4. **Większy zbiór testowy** — pozyskanie rzeczywistych zgłoszeń helpdesk
   (po anonimizacji) do ewaluacji.

5. **Cross-walidacja** — podział danych na treningowe i testowe dla właściwej
   oceny generalizacji modelu.

6. **Ocena ekspercka** — zaangażowanie specjalisty IT do ręcznej weryfikacji
   etykiet referencyjnych i jakości odpowiedzi.
