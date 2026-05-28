# Dane testowe — zbiór ewaluacyjny

Ten katalog zawiera syntetyczny zbiór zgłoszeń do ewaluacji modułu analizy systemu helpdesk.

## Pliki

| Plik | Opis |
|------|------|
| `evaluation_tickets.csv` | Zbiór 64 syntetycznych zgłoszeń w formacie CSV |
| `evaluation_tickets.json` | Ten sam zbiór w formacie JSON (generowany skryptem) |

## Struktura danych

Każde zgłoszenie zawiera następujące pola:

| Kolumna | Opis |
|---------|------|
| `id` | Unikalny identyfikator zgłoszenia (np. T001) |
| `title` | Tytuł zgłoszenia |
| `description` | Opis problemu |
| `expected_category` | Oczekiwana kategoria (etykieta referencyjna) |
| `expected_priority` | Oczekiwany priorytet (etykieta referencyjna) |
| `expected_solution_keywords` | Słowa kluczowe oczekiwane w odpowiedzi (rozdzielone średnikiem) |
| `notes` | Uwagi o przypadku testowym |

## Kategorie referencyjne

- Konto i dostęp
- Sieć i VPN
- Aplikacje biznesowe
- Sprzęt komputerowy
- Poczta e-mail
- Bezpieczeństwo
- System operacyjny
- Inne

## Priorytety referencyjne

| Priorytet | Opis |
|-----------|------|
| Niski | Zgłoszenie nie blokuje pracy |
| Średni | Zgłoszenie utrudnia pracę, istnieje obejście |
| Wysoki | Zgłoszenie blokuje pracę użytkownika |
| Krytyczny | Awaria wpływająca na wielu użytkowników lub ciągłość firmy |

## Rozkład danych

| Kategoria | Liczba zgłoszeń |
|-----------|----------------|
| Konto i dostęp | 8 |
| Sieć i VPN | 8 |
| Aplikacje biznesowe | 8 |
| Sprzęt komputerowy | 8 |
| Poczta e-mail | 7 |
| Bezpieczeństwo | 8 |
| System operacyjny | 7 |
| Inne | 7 |
| Inne (dodatkowe) | 3 |
| **Łącznie** | **64** |

## Uwagi

- Dane są **syntetyczne** i bezpieczne do publikacji w repozytorium.
- Nie zawierają danych osobowych ani rzeczywistych danych firmowych.
- Zawierają celowo trudne, niejednoznaczne przypadki testowe.
- Służą wyłącznie jako materiał do ewaluacji prototypowego pipeline'u analizy.
