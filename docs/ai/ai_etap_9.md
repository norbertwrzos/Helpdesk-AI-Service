# AI Etap 9 — Fundament RAG dla bazy wiedzy

## 1. Cel etapu

Celem etapu było przygotowanie fundamentu architektury Retrieval-Augmented Generation w systemie Helpdesk AI Service bez zmiany końcowego generatora odpowiedzi. Zakres obejmuje wytwarzanie embeddingów artykułów bazy wiedzy, ich składowanie w PostgreSQL z wykorzystaniem rozszerzenia `pgvector`, reindeksację zasobu wiedzy oraz wyszukiwanie top-k podobnych artykułów dla treści zgłoszenia. Etap celowo nie obejmuje jeszcze generowania odpowiedzi przez model OpenAI, ponieważ priorytetem było odseparowanie warstwy retrievalu od warstwy generatywnej.

## 2. Problem projektowy

Dotychczasowy mechanizm wyszukiwania podobnych artykułów opierał się na prostym modelu bag-of-words. Rozwiązanie tego typu jest łatwe do implementacji i dobrze sprawdza się w demonstracji podstawowego przepływu AI, jednak jest ograniczone semantycznie. Nie radzi sobie dobrze z parafrazami, różnymi formami językowymi oraz sytuacjami, w których zgłoszenie i artykuł opisują ten sam problem innymi słowami. W konsekwencji projekt wymagał wprowadzenia reprezentacji wektorowej treści, która pozwala porównywać podobieństwo znaczeniowe, a nie tylko dosłowne współwystępowanie tokenów.

## 3. Założenia techniczne

Przyjęto, że fundament RAG ma zostać zbudowany przy minimalnym ryzyku dla istniejącej architektury. Z tego powodu pozostawiono obecny `SimilarityService` jako ścieżkę fallbackową, a nowy komponent retrievalu został zaprojektowany jako osobna warstwa usługowa. Do generowania embeddingów wybrano OpenAI Embeddings API z domyślnym modelem `text-embedding-3-small`, natomiast do testów i pracy bez klucza API dodano deterministyczny provider mockowy. Jako magazyn wektorów wybrano PostgreSQL z rozszerzeniem `pgvector`, ponieważ system już używa PostgreSQL, a integracja wektorów w tej samej bazie upraszcza architekturę, migracje oraz opis rozwiązania w pracy inżynierskiej.

## 4. Architektura rozwiązania

Architektura etapu składa się z pięciu głównych elementów. Pierwszym jest warstwa providerów embeddingów, odpowiedzialna za wytwarzanie wektorów dla tekstu. Drugim jest model danych `KnowledgeArticleEmbedding`, przechowujący embedding, nazwę modelu, hash treści oraz znaczniki czasu. Trzecim komponentem jest `KnowledgeEmbeddingService`, który realizuje reindeksację i kontroluje, czy dany artykuł wymaga ponownego przeliczenia embeddingu. Czwartym elementem jest `RagRetriever`, który buduje zapytanie na podstawie zgłoszenia, generuje embedding zgłoszenia i wykonuje wyszukiwanie top-k po tabeli wektorowej. Piątym elementem jest integracja z `AnalysisPipeline`, która pozwala użyć retrievalu RAG, ale zachowuje bezpieczny fallback do dotychczasowej implementacji.

## 5. Opis komponentów

`BaseEmbeddingProvider` definiuje dwa podstawowe kontrakty: generowanie embeddingu pojedynczego tekstu oraz wsadowe generowanie embeddingów. `OpenAIEmbeddingProvider` korzysta z oficjalnego klienta OpenAI i pobiera konfigurację modelu z ustawień aplikacji. Provider ten obsługuje pusty tekst i zapisuje jedynie bezpieczne logi diagnostyczne, bez ujawniania klucza API. `MockEmbeddingProvider` generuje deterministyczne wektory na podstawie funkcji skrótu SHA-256, co pozwala testować warstwę usługową bez połączenia z siecią.

`KnowledgeEmbeddingService` buduje tekst indeksowy artykułu z tytułu, treści, tagów i kategorii. Następnie wylicza hash treści, aby uniknąć zbędnego przeliczania embeddingów dla niezmienionych rekordów. Serwis udostępnia reindeksację pojedynczego artykułu oraz pełnej bazy wiedzy. W przypadku błędu pojedynczego rekordu błąd jest raportowany, ale proces reindeksacji całej bazy nie jest przerywany.

`RagRetriever` buduje tekst zapytania na podstawie zgłoszenia, łącząc tytuł, opis, kategorię i priorytet. Następnie generuje embedding zapytania i wykonuje zapytanie top-k po operatorze cosine distance `embedding <=> query_vector`. Wynik jest przeliczany na czytelną skalę podobieństwa. Gdy provider embeddingów nie jest dostępny albo baza nie udostępnia pgvector, retriever korzysta z istniejącego `SimilarityService`. Gdy same embeddingi artykułów nie zostały jeszcze zbudowane, zwracana jest pusta lista oraz czytelna informacja w logach.

## 6. Model danych

Wprowadzono tabelę `knowledge_article_embeddings`, która zawiera następujące pola: klucz główny, identyfikator artykułu, wektor embeddingu, nazwę modelu embeddingowego, hash treści, datę utworzenia oraz datę ostatniej aktualizacji. Relacja `article_id` jest unikalna, co oznacza, że każdy artykuł ma najwyżej jeden aktualny embedding. W bazie PostgreSQL kolumna `embedding` wykorzystuje typ `vector(1536)`, natomiast w testach SQLite zastosowano bezpieczny fallback typu JSON na poziomie ORM. Takie podejście pozwala utrzymać wspólny model domenowy bez psucia testów jednostkowych.

## 7. Proces reindeksacji bazy wiedzy

Proces reindeksacji rozpoczyna się od pobrania artykułu lub zbioru artykułów bazy wiedzy. Dla każdego rekordu budowany jest tekst indeksowy oraz hash treści. Jeżeli istniejący hash jest identyczny i nie ustawiono flagi wymuszenia, artykuł zostaje pominięty. W przeciwnym razie generowany jest nowy embedding, który jest zapisywany w tabeli `knowledge_article_embeddings`. Reindeksacja całej bazy zwraca podsumowanie zawierające liczbę artykułów ogółem, liczbę rekordów zindeksowanych, pominiętych oraz listę błędów.

## 8. Proces wyszukiwania podobnych artykułów

Wyszukiwanie podobnych artykułów przebiega w kilku krokach. Najpierw budowany jest tekst zapytania na podstawie zgłoszenia technicznego. Następnie dla tego tekstu wyliczany jest embedding. Kolejny etap to zapytanie do PostgreSQL z użyciem operatora cosine distance `<=>`, które zwraca rekordy uporządkowane od najbardziej podobnych do najmniej podobnych. Na końcu wynik jest zamieniany na czytelną strukturę z identyfikatorem artykułu, tytułem, skrótem treści, kategorią oraz wynikiem podobieństwa. Parametr top-k jest konfigurowalny i domyślnie wynosi pięć rekordów.

## 9. Integracja z istniejącym AnalysisPipeline

Integracja z `AnalysisPipeline` została zaprojektowana tak, aby nie naruszać istniejącego generatora odpowiedzi. Pipeline najpierw ustala kategorię i priorytet zgłoszenia, a następnie sprawdza, czy retrieval wektorowy jest dostępny. Jeśli tak, pobierany jest kontekst przez `RagRetriever`. Jeżeli nie, pipeline wraca do `SimilarityService`. Dzięki temu obecny generator odpowiedzi może nadal przyjmować listę podobnych artykułów w niezmienionym formacie, a projekt zyskuje możliwość stopniowego przejścia od podejścia rule-based do pełnego RAG.

## 10. Testowanie

Testy etapu obejmują kilka poziomów. Dla narzędzi pomocniczych dodano testy deterministyczności funkcji hashującej oraz mockowego providera embeddingów. Dla warstwy usługowej przygotowano testy reindeksacji pojedynczego artykułu, pomijania aktualnych rekordów oraz wymuszonej aktualizacji. Dla retrievera dodano testy zwracania artykułów, działania fallbacku oraz obsługi pustej bazy wiedzy. Ponieważ standardowe testy projektu działają na SQLite in-memory, nie uruchamiają one realnego `pgvector`, lecz weryfikują logikę aplikacyjną oraz ścieżki fallbackowe. Integrację z PostgreSQL i pgvector można zweryfikować lokalnie przez migracje, seed danych i wywołanie endpointów technicznych.

## 11. Ograniczenia

Najważniejszym ograniczeniem etapu jest brak generowania odpowiedzi przez model zewnętrzny. System wykorzystuje już embeddingi do retrievalu, ale końcowa odpowiedź nadal pochodzi z generatora mockowego. Drugim ograniczeniem jest konieczność ręcznej reindeksacji po istotnych zmianach treści artykułów. Trzecim ograniczeniem jest brak produkcyjnego indeksu ANN, ponieważ na obecnym etapie wystarcza exact search po operatorze pgvector. Czwartym ograniczeniem jest fakt, że testy automatyczne oparte o SQLite nie sprawdzają realnej pracy operatorów wektorowych w PostgreSQL.

## 12. Możliwości dalszego rozwoju

Naturalnym kolejnym krokiem jest połączenie warstwy retrievalu z generowaniem odpowiedzi przez model językowy i zbudowanie pełnego przepływu RAG. Następnie można dodać ranking hybrydowy łączący wektory z wyszukiwaniem leksykalnym, wprowadzić indeks HNSW lub IVFFlat dla większej liczby artykułów oraz zbudować metryki oceny jakości retrievalu. Dalszy rozwój może także objąć obsługę chunkowania długich artykułów, filtrowanie po kategorii oraz wersjonowanie embeddingów dla różnych modeli.

## 13. Materiał do pracy inżynierskiej

W ramach implementacji fundamentu RAG zdecydowano się na wykorzystanie embeddingów semantycznych, ponieważ klasyczne wyszukiwanie oparte wyłącznie na wspólnych tokenach nie zapewniało wystarczającej jakości dopasowania artykułów bazy wiedzy do treści zgłoszeń. Embeddingi umożliwiają reprezentację tekstu w przestrzeni wektorowej, w której podobieństwo można analizować z użyciem odległości kosinusowej. Dzięki temu system może rozpoznawać podobieństwo znaczeniowe nawet wtedy, gdy zgłoszenie i artykuł używają innych sformułowań językowych.

Z perspektywy architektonicznej istotnym założeniem było zachowanie spójności stosu technologicznego. Zamiast wprowadzać osobną bazę wektorową, wykorzystano PostgreSQL rozszerzony o `pgvector`. Takie rozwiązanie upraszcza wdrożenie, migracje oraz zarządzanie danymi, ponieważ rekordy domenowe i reprezentacje wektorowe pozostają w jednym systemie transakcyjnym. W kontekście pracy inżynierskiej jest to korzystne również dlatego, że pozwala jasno pokazać ewolucję istniejącej architektury relacyjnej w kierunku architektury wspierającej mechanizmy AI.

Zaimplementowany proces reindeksacji wykorzystuje hash treści artykułu, aby ograniczyć koszt przeliczania embeddingów tylko do rekordów rzeczywiście zmienionych. Mechanizm ten zwiększa efektywność rozwiązania i stanowi przykład praktycznego kompromisu pomiędzy prostotą implementacji a wydajnością. Jednocześnie zachowano ścieżkę fallbackową do wcześniejszego mechanizmu bag-of-words, co było istotne z punktu widzenia odporności systemu na brak konfiguracji klucza API lub niedostępność komponentów wektorowych.

Wdrożenie tego etapu można traktować jako przygotowanie warstwy retrievalu pod pełny model RAG. W obecnej wersji system potrafi już pobierać semantycznie podobne artykuły i przekazywać je dalej jako kontekst, natomiast sama generacja odpowiedzi pozostaje jeszcze w trybie mockowym. Takie rozdzielenie etapów implementacyjnych pozwala na czytelne opisanie procesu rozwoju systemu w pracy inżynierskiej: od klasycznego rule-based NLP, przez warstwę retrievalu semantycznego, aż do przyszłej integracji z modelem generatywnym.