# AI Etap 12.6 — Konwersacja ticketu i integracja odpowiedzi AI

## 1. Cel etapu

Etap 12.6 rozszerza interakcję użytkownika z systemem Helpdesk AI Service o pełny wątek komunikacji w obrębie zgłoszenia. Historia wiadomości pomiędzy rolami `end_user` i `agent` stanowi jedyne źródło prawdy dla komunikacji w procesie obsługi ticketu.

## 2. Kontekst AI i service desk

W praktyce service desk wygenerowana odpowiedź AI stanowi propozycję działań, natomiast rzeczywista komunikacja z użytkownikiem ma charakter iteracyjny. Użytkownik może doprecyzować problem po wykonaniu zaleceń, a agent może udzielić kolejnych instrukcji. Dodanie konwersacji ticketu umożliwia osadzenie odpowiedzi AI w rzeczywistym procesie operacyjnym.

## 3. Transformacja odpowiedzi AI w odpowiedź agenta

Wprowadzono spójny mechanizm, w którym akcja "Zapisz jako odpowiedź agenta":

1. tworzy nowy wpis `TicketMessage` z rolą `agent`.

Dzięki temu treść wygenerowana przez AI staje się częścią historii komunikacji widocznej dla obu stron procesu.

## 4. Człowiek w pętli decyzyjnej

Projekt zachowuje założenie human-in-the-loop:

- AI generuje sugestię odpowiedzi,
- agent podejmuje decyzję o akceptacji, modyfikacji lub odrzuceniu,
- dopiero decyzja agenta utrwala odpowiedź w konwersacji.

To podejście jest istotne zarówno z perspektywy jakości komunikacji, jak i odpowiedzialności operacyjnej w środowisku wsparcia IT.

## 5. Wpływ historii wiadomości na audytowalność

Historia wiadomości poprawia audytowalność procesu, ponieważ umożliwia odtworzenie kolejnych kroków obsługi zgłoszenia:

- jakie informacje przekazał użytkownik,
- jakie zalecenia przekazał agent,
- które odpowiedzi były inspirowane przez AI.

W konsekwencji system lepiej wspiera analizę jakości pracy, retrospektywę incydentów i dokumentowanie przebiegu obsługi w materiałach projektowych.

## 6. Ograniczenia etapu

Etap 12.6 zachowuje świadomie uproszczony charakter prototypu:

- brak kanału realtime,
- brak WebSocket,
- brak pełnego backend auth/JWT,
- brak załączników i edycji/usuwania wiadomości.

Zakres ten jest zgodny z celem pracy inżynierskiej: przedstawienie czytelnej i możliwej do obrony implementacji, która pokazuje pełny przepływ AI + agent + użytkownik końcowy bez nadmiernej złożoności infrastrukturalnej.
