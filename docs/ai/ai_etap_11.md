# AI Etap 11 — Integracja UI dla RAG i generowania odpowiedzi mailowej

## 1. Cel etapu

Celem etapu było domknięcie przepływu RAG i generowania odpowiedzi mailowej po stronie interfejsu użytkownika. Po realizacji poprzednich etapów backend potrafił pobierać kontekst z bazy wiedzy i generować szkic odpowiedzi dla zgłoszenia, jednak agent nie otrzymywał jeszcze czytelnego interfejsu, który prezentowałby pochodzenie tej odpowiedzi, źródła RAG oraz praktyczne akcje robocze. Etap 11 koncentruje się więc na warstwie prezentacji i ergonomii pracy agenta.

## 2. Zakres funkcjonalny

W widoku szczegółów zgłoszenia rozbudowano sekcję AI tak, aby najnowsza odpowiedź była prezentowana jako główna karta robocza. Karta pokazuje nazwę providera, nazwę modelu, datę wygenerowania, treść odpowiedzi w formacie mailowym oraz ostrzeżenie, że wynik wymaga weryfikacji człowieka. Dodatkowo interfejs prezentuje listę źródeł RAG wraz z oceną dopasowania, fragmentem treści oraz linkiem prowadzącym bezpośrednio do artykułu bazy wiedzy.

Niżej zachowano historię starszych odpowiedzi, dzięki czemu agent może porównywać kolejne generacje odpowiedzi dla tego samego zgłoszenia. Zachowano także dotychczasowy mechanizm feedbacku, aby rozbudowa warstwy prezentacji nie zaburzyła zbierania ocen jakości.

## 3. Architektura zmian frontendowych

Architektura Etapu 11 została oparta na minimalnej ingerencji w istniejący kontrakt API. Zamiast wprowadzać nowe endpointy, frontend wykorzystuje już dostępne pola `provider_name`, `model_name`, `response_text`, `created_at` i `sources_used`, które wcześniej były zapisywane przez backend. Dzięki temu etap UI pozostaje spójny z wcześniejszą architekturą providerów i nie wymaga poszerzania modelu domenowego po stronie serwera.

Logika prezentacji została skupiona przede wszystkim w komponentach `AIResponseCard`, `AIResponseHistory` oraz `TicketAiSection`. `AIResponseCard` odpowiada za renderowanie pojedynczej odpowiedzi wraz z metadanymi i akcjami użytkownika. `AIResponseHistory` rozdziela najnowszą odpowiedź od starszych wpisów. `TicketAiSection` pozostaje miejscem uruchamiania analizy i odświeżania historii po wykonaniu `POST /tickets/{ticket_id}/analyze`.

## 4. Parser metadanych RAG

Szczególnym elementem implementacji było wprowadzenie pomocniczego parsera `sources_used`. Pole to jest przechowywane w bazie jako tekst JSON, ale ze względu na wcześniejsze iteracje projektu może przyjmować więcej niż jeden kształt danych. Z tego powodu frontend nie zakłada jednego sztywnego formatu, lecz wykonuje defensywne parsowanie i normalizację listy źródeł. Jeżeli parsowanie się nie powiedzie, interfejs nie pokazuje surowego JSON-a, lecz czytelny komunikat o braku możliwości odczytania metadanych.

Takie podejście zwiększa odporność aplikacji na starsze dane historyczne oraz ogranicza ryzyko prezentowania użytkownikowi technicznych struktur wewnętrznych, które byłyby mało zrozumiałe z perspektywy pracy operacyjnej.

## 5. Akcje użytkownika i ergonomia pracy agenta

W karcie odpowiedzi dodano dwie akcje robocze. Pierwsza umożliwia skopiowanie wygenerowanej odpowiedzi do schowka, co przyspiesza dalszą edycję lub wykorzystanie treści poza aplikacją. Druga pozwala dodać wygenerowany szkic bezpośrednio jako wiadomość agenta do konwersacji ticketu.

Istotna była również synchronizacja sekcji AI z historią komunikacji. Po zapisaniu szkicu z karty AI konwersacja powinna od razu pokazywać nową wiadomość agenta, dzięki czemu użytkownik końcowy i agent widzą spójny przebieg kontaktu.

## 6. Kontrola dostępu i bezpieczeństwo

Z punktu widzenia bezpieczeństwa zachowano wcześniejsze założenie, że wygenerowana odpowiedź nie może zostać wysłana automatycznie. Interfejs podkreśla, że jest to wyłącznie propozycja wymagająca weryfikacji człowieka. Akcja dodania odpowiedzi AI do konwersacji pozostaje dostępna jedynie w panelu agenta, ponieważ sam widok szczegółów zgłoszenia jest chroniony rolą `agent`. W ten sposób warstwa UI nie osłabia modelu uprawnień już obecnego w aplikacji.

## 7. Wpływ na widok AI

Widok `AI` został odświeżony w niewielkim zakresie, aby lista ostatnich odpowiedzi prezentowała ujednolicone etykiety providerów zamiast surowych nazw technicznych. Zmiana ta poprawia spójność interfejsu i zmniejsza liczbę technicznych szczegółów, które agent musi interpretować samodzielnie.

## 8. Walidacja

Walidację etapu przeprowadzono przez produkcyjny build frontendu (`npm run build`). Test ten potwierdził poprawność typów TypeScript, importów, tras nawigacyjnych oraz integracji nowych komponentów z istniejącymi endpointami API. Dodatkowo przewidziano manualny scenariusz sprawdzający uruchomienie analizy, wyświetlenie źródeł RAG, kopiowanie treści, dodanie odpowiedzi AI jako wiadomości agenta oraz przejście do artykułu bazy wiedzy.

## 9. Ograniczenia

Etap 11 nie wprowadza automatycznego odświeżania wyników w tle ani nowych mechanizmów filtrowania historii odpowiedzi AI. Interfejs opiera się nadal na ręcznym uruchomieniu analizy przez agenta. Drugim ograniczeniem jest zależność jakości prezentowanych źródeł od jakości danych zapisanych wcześniej w `sources_used`. Jeżeli backend zapisze niepełne metadane albo starszy format danych, frontend ograniczy się do najlepszego możliwego odczytu bez gwarancji pełnej prezentacji wszystkich pól.

## 10. Materiał do pracy inżynierskiej

Etap 11 pokazuje, że samo zastosowanie RAG i modelu generatywnego nie wystarcza do zbudowania użytecznego systemu wspomagania pracy helpdesku. Równie istotna jest warstwa interfejsu, która musi ujawniać pochodzenie odpowiedzi, eksponować źródła, umożliwiać szybkie użycie wygenerowanego szkicu i jednocześnie wymuszać kontrolę człowieka. W praktyce to właśnie ta warstwa decyduje, czy rozwiązanie będzie postrzegane jako narzędzie wspomagające, czy jako nieprzejrzysta automatyzacja.

Zaprojektowany interfejs wzmacnia audytowalność działania modułu AI. Agent widzi nie tylko samą treść odpowiedzi, lecz także zbiór artykułów, które mogły wpłynąć na jej powstanie. Dzięki temu może łatwiej ocenić, czy model rzeczywiście oparł się na wiarygodnym kontekście, a projekt zyskuje ważny argument metodologiczny w opisie rozwiązania typu retrieval-augmented generation w środowisku wsparcia technicznego.