# Wymiana wiadomości w zgłoszeniu

## 1. Cel funkcjonalności

Celem wdrożonej funkcjonalności jest implementacja pełnej historii komunikacji prowadzonej w ramach jednego ticketu. W rezultacie system może przechowywać i prezentować wieloetapową wymianę informacji pomiędzy użytkownikiem końcowym i agentem, co lepiej odzwierciedla realny proces pracy service desk.

## 2. Uzasadnienie projektowe

W systemach helpdesk komunikacja stanowi integralną część procesu obsługi incydentu lub zapytania. Użytkownik zgłasza problem, agent dopytuje o szczegóły, a następnie przekazuje kolejne instrukcje diagnostyczne. Utrzymywanie jedynie ostatniej odpowiedzi agenta nie zapewnia pełnej transparentności procesu. Zastosowanie dedykowanego wątku wiadomości zwiększa audytowalność i czytelność historii obsługi, przy jednoczesnym zachowaniu prostoty implementacyjnej wymaganej dla prototypu akademickiego.

## 3. Model danych

Wprowadzono model `TicketMessage` oraz tabelę `ticket_messages`. Każda wiadomość zawiera identyfikator zgłoszenia, dane autora, treść, typ wiadomości oraz znaczniki czasu.

Najważniejsze atrybuty:

- `id` – klucz główny,
- `ticket_id` – klucz obcy do tabeli `tickets`,
- `author_role` – rola autora wiadomości,
- `author_name` – nazwa wyświetlana autora,
- `author_email` – opcjonalny kontakt autora,
- `message_text` – właściwa treść wiadomości,
- `message_type` – typ wiadomości (`public`),
- `created_at`, `updated_at` – znaczniki czasu.

Relacja danych ma charakter 1:N: jeden `Ticket` posiada wiele `TicketMessage`, a każda `TicketMessage` należy do jednego `Ticket`.

## 4. Role autorów wiadomości

W bieżącym etapie aktywnie wykorzystywane są role:

- `agent`,
- `end_user`.

Rola `system` pozostaje zarezerwowana na przyszłe rozszerzenia (np. wpisy automatyczne), ale nie jest używana operacyjnie w tej iteracji.

## 5. Endpointy API

Zaimplementowano dwa endpointy REST:

- `GET /tickets/{ticket_id}/messages` – pobiera listę wiadomości dla zgłoszenia,
- `POST /tickets/{ticket_id}/messages` – dodaje nową wiadomość do zgłoszenia.

Wiadomości zwracane są chronologicznie (rosnąco po `created_at`). Walidacja obejmuje między innymi wymagalność treści wiadomości oraz poprawność roli autora.

## 6. Integracja z widokiem agenta

W widoku szczegółów zgłoszenia po stronie agenta dodano sekcję "Konwersacja". Sekcja ta zawiera:

- listę historycznych wiadomości,
- formularz dodawania nowej wiadomości,
- stany `loading`, `error` i `empty`.

Wysłanie wiadomości przez agenta aktualizuje listę konwersacji i znacznik czasu aktualizacji zgłoszenia. Historia wiadomości jest jedynym źródłem prawdy komunikacji.

## 7. Integracja z portalem użytkownika

W portalu użytkownika końcowego dodano analogiczną sekcję "Wiadomości". Użytkownik widzi wyłącznie wiadomości własnego zgłoszenia i może dopisać kolejną informację diagnostyczną. Dostęp do szczegółów ticketu pozostaje ograniczony frontendowym guardem opartym o porównanie `requester_email` z kontem mock usera.

## 8. Integracja z odpowiedzią AI

W systemie istnieje możliwość wygenerowania odpowiedzi przez moduł AI. Po użyciu akcji "Zapisz jako odpowiedź agenta" treść zostaje:

1. dodana jako `TicketMessage` z rolą `agent`.

Takie podejście zapewnia spójność i audytowalność całej komunikacji w jednym modelu danych.

## 9. Ograniczenia

Zakres wdrożenia świadomie pomija funkcje poza celem etapu:

- brak komunikacji realtime,
- brak WebSocket,
- brak załączników,
- mock auth zamiast pełnego auth backendowego,
- brak usuwania i edycji wiadomości.

## 10. Materiał do pracy inżynierskiej

Proponowany akapit do rozdziału implementacyjnego:

"W celu zwiększenia zgodności prototypu z praktyką działania systemów service desk zaimplementowano mechanizm konwersacji w obrębie pojedynczego zgłoszenia. W warstwie danych wprowadzono encję TicketMessage powiązaną relacją 1:N z encją Ticket. Warstwa API została rozszerzona o endpointy pobierania oraz dodawania wiadomości. Pełna historia wymiany informacji jest utrzymywana w tabeli ticket_messages, która stanowi źródło prawdy dla komunikacji między stronami procesu." 

Proponowany akapit do opisu sesji użytkownika:

"Podczas scenariusza obsługi zgłoszenia użytkownik końcowy dopisuje kolejne informacje o problemie bezpośrednio w sekcji wiadomości. Agent, analizując zgłoszenie i kontekst AI/RAG, odpowiada w tej samej sekcji, a każda wiadomość jest zapisywana i prezentowana chronologicznie. Dzięki temu przebieg komunikacji jest czytelny i może zostać wykorzystany zarówno do celów operacyjnych, jak i dokumentacyjnych." 
