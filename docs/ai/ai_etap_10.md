# AI Etap 10 — Generowanie odpowiedzi mailowej z wykorzystaniem OpenAI API

## 1. Cel etapu

Celem etapu było rozszerzenie systemu Helpdesk AI Service o możliwość generowania propozycji odpowiedzi mailowej dla użytkownika końcowego. Odpowiedź ma wspierać pracę agenta helpdesk, ale nie zastępuje jego decyzji i nie jest wysyłana automatycznie. Implementacja etapu opiera się na połączeniu istniejących komponentów analitycznych, w szczególności rule-based classification, rule-based prioritization oraz warstwy retrieval zbudowanej w ramach fundamentu RAG.

## 2. Uzasadnienie wykorzystania LLM

Dotychczasowy mockowy generator odpowiedzi pozwalał jedynie na tworzenie szablonowych komunikatów diagnostycznych. Tego typu mechanizm dobrze sprawdza się w demonstracji przepływu analizy, lecz nie zapewnia naturalnej, spójnej i kontekstowej komunikacji z użytkownikiem. Zastosowanie modelu językowego pozwala generować odpowiedź w bardziej naturalnym języku, zachowując przy tym jednolity format mailowy oraz zależność od danych wejściowych systemu. Model nie zastępuje istniejącej logiki klasyfikacji ani priorytetyzacji, lecz pełni rolę warstwy formułującej odpowiedź na podstawie wcześniej przygotowanego kontekstu.

## 3. Założenia bezpieczeństwa

Na etapie projektowym przyjęto, że wygenerowana treść ma charakter propozycji dla agenta, a nie automatycznej decyzji systemu. Z tego powodu każda odpowiedź jest oznaczona jako wymagająca weryfikacji człowieka. System nie wysyła wiadomości e-mail, nie wykonuje działań administracyjnych oraz nie deklaruje rozwiązania problemu bez potwierdzenia. Do modelu nie są przekazywane dane niepotrzebne do budowy odpowiedzi, w szczególności `requester_email`. Dodatkowo przewidziano bezpieczny fallback do providera `mock`, gdy konfiguracja OpenAI jest niepełna albo wywołanie API zakończy się błędem.

## 4. Architektura providerów AI

Warstwę generowania odpowiedzi zorganizowano zgodnie z wzorcem providerów. Abstrakcja `BaseAIResponseProvider` definiuje kontrakt generowania odpowiedzi na podstawie ustrukturyzowanego wejścia. `MockAIResponseProvider` zapewnia lokalny, deterministyczny fallback niewymagający sieci ani klucza API. `OpenAIResponseProvider` korzysta z OpenAI Responses API i zwraca dane zgodne z określonym schematem strukturalnym. Fabryka providerów wybiera właściwą implementację na podstawie konfiguracji, a `AnalysisPipeline` może w sposób bezpieczny przełączyć się na providera zapasowego, jeśli provider podstawowy zawiedzie.

## 5. Struktura promptu

Prompt został podzielony na dwie części: instrukcję systemową oraz komunikat użytkownika. Instrukcja systemowa określa rolę modelu jako asystenta działu IT Support przygotowującego propozycję odpowiedzi mailowej. Wymusza także odpowiedź w języku polskim, zakaz halucynowania procedur spoza dostarczonych danych oraz obowiązek zachowania formatu mailowego. Komunikat użytkownika przekazuje treść zgłoszenia, kategorię, priorytet, imię agenta oraz listę artykułów odzyskanych przez RAG. Jeżeli dostępne źródła są niewystarczające, model otrzymuje wyraźne polecenie, aby zaznaczyć potrzebę dalszej analizy przez pracownika IT.

## 6. Dane wejściowe i wyjściowe

Dane wejściowe dla providera mają postać obiektu `TicketResponseGenerationInput`, który zawiera identyfikator zgłoszenia, tytuł, opis, nazwę kategorii, nazwę priorytetu, opcjonalne imię zgłaszającego, imię agenta, artykuły odnalezione przez RAG oraz opcjonalne uzasadnienia klasyfikacji i priorytetu. Wynik działania providera przyjmuje postać `TicketResponseGenerationResult`, zawierając temat wiadomości, treść maila, poziom pewności, identyfikatory źródeł wykorzystanych przez model, informację o obowiązku weryfikacji przez człowieka, opis ograniczeń, nazwę modelu, nazwę providera oraz opcjonalną surową odpowiedź modelu.

## 7. Format odpowiedzi mailowej

Wymagany format odpowiedzi ma charakter prosty i powtarzalny, co ułatwia jego prezentację w interfejsie użytkownika i opis w dokumentacji projektowej. Wiadomość rozpoczyna się od zwrotu grzecznościowego „Dzień dobry,”, następnie zawiera krótkie odniesienie do problemu użytkownika, zestaw proponowanych kroków diagnostycznych lub naprawczych oraz informację, co zrobić w przypadku utrzymywania się problemu. Końcowa część wiadomości zawiera podpis agenta. Taki format odzwierciedla realną praktykę działów wsparcia technicznego i pozwala traktować wynik modelu jako gotowy szkic odpowiedzi.

## 8. Integracja z AnalysisPipeline

Integracja z `AnalysisPipeline` przebiega po wykonaniu klasyfikacji, priorytetyzacji i retrievalu. Pipeline buduje obiekt wejściowy dla providera generatywnego, wykorzystując dane zgłoszenia, wyniki rule-based analysis oraz artykuły pobrane przez `RAGRetriever`. Wynik generowania jest mapowany na dotychczasowy model `GeneratedAnswer`, tak aby nie naruszyć istniejącego kontraktu API. Treść maila jest zapisywana w `AIResponse.response_text`, natomiast nazwa modelu i providera trafia odpowiednio do pól `model_name` i `provider_name`. Pole `sources_used` zawiera JSON z metadanymi źródeł RAG oraz informacją, czy dane źródło zostało oznaczone jako wykorzystane przez model.

## 9. Obsługa błędów i fallback

Obsługa błędów została zaprojektowana warstwowo. Na etapie tworzenia providera brak `OPENAI_API_KEY` skutkuje bezpiecznym powrotem do providera `mock`. Na etapie samego wywołania API błąd OpenAI nie przerywa całego `AnalysisPipeline`, lecz jest logowany i powoduje wygenerowanie odpowiedzi przez providera zapasowego. Dzięki temu analiza ticketu może zakończyć się powodzeniem nawet przy chwilowej niedostępności usługi zewnętrznej. W logach nie są ujawniane żadne wartości kluczy API.

## 10. Testowanie

Testy etapu obejmują kilka poziomów. Dla prompt buildera sprawdzono obecność wymaganych elementów formatu mailowego, imienia agenta, treści artykułów RAG oraz brak przekazywania `requester_email`. Dla mockowego providera zweryfikowano generowanie maila z poprawnym powitaniem i podpisem oraz wymuszenie weryfikacji przez człowieka. Dla providera OpenAI zastosowano mockowanie klienta SDK, dzięki czemu testy nie wykonują prawdziwych wywołań sieciowych, a jednocześnie sprawdzają mapowanie structured output oraz obsługę błędów. Na poziomie pipeline dodano test trybu `openai` oraz test fallbacku do `mock` w przypadku błędu providera zewnętrznego.

## 11. Ograniczenia

Najważniejszym ograniczeniem etapu jest to, że klasyfikacja i priorytetyzacja nadal pozostają rule-based. Oznacza to, że jakość końcowej odpowiedzi zależy nie tylko od modelu językowego, ale również od jakości wcześniejszych etapów analizy. Drugim ograniczeniem jest zależność jakości maila od jakości i kompletności bazy wiedzy oraz od jakości retrievalu RAG. Trzecim ograniczeniem jest brak automatycznej wysyłki wiadomości, co jest decyzją świadomą z punktu widzenia bezpieczeństwa, ale ogranicza automatyzację procesu. Czwartym ograniczeniem jest konieczność weryfikacji każdej odpowiedzi przez człowieka.

## 12. Materiał do pracy inżynierskiej

W systemie Helpdesk AI Service odpowiedź generowana przez model językowy została zaprojektowana jako propozycja dla agenta, a nie jako samodzielna decyzja systemu. Takie podejście wynika z charakteru obsługi zgłoszeń technicznych, w której nawet poprawnie sformułowana odpowiedź może wymagać dodatkowego kontekstu organizacyjnego lub technicznego, niedostępnego dla modelu. Utrzymanie człowieka w pętli decyzyjnej pozwala ograniczyć ryzyko błędnych rekomendacji i zachować zgodność z praktyką pracy zespołów wsparcia IT.

Wymóg weryfikacji odpowiedzi przez agenta pełni funkcję zarówno bezpieczeństwa operacyjnego, jak i kontroli jakości. Model może przygotować spójny językowo szkic odpowiedzi, lecz nie ma bezpośredniej wiedzy o stanie infrastruktury, politykach organizacyjnych ani bieżących działaniach serwisowych. Z tego względu każda wiadomość wygenerowana przez AI jest oznaczana jako wymagająca przeglądu przez pracownika IT Support przed użyciem w komunikacji z użytkownikiem końcowym.

Zastosowanie architektury RAG ogranicza ryzyko halucynacji modelu poprzez zawężenie kontekstu do artykułów bazy wiedzy powiązanych ze zgłoszeniem. Model nie otrzymuje pełnej, nieograniczonej przestrzeni wiedzy, lecz zestaw konkretnych materiałów dobranych przez retriever. Dzięki temu odpowiedź generatywna ma silniejsze zakotwiczenie w bazie wiedzy projektu i lepiej odzwierciedla procedury rzeczywiście dostępne w systemie.

Istotnym elementem implementacji jest również zapisywanie źródeł wykorzystanych przy generowaniu odpowiedzi. W polu `sources_used` przechowywane są metadane artykułów RAG, w tym identyfikator artykułu, tytuł, wynik podobieństwa, fragment treści oraz znacznik określający, czy model wskazał dane źródło jako wykorzystane. Rozwiązanie to zwiększa przejrzystość działania modułu AI, wspiera audytowalność i stanowi wartościowy materiał analityczny do dalszego rozwoju systemu.