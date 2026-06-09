# AI Etap 12 — Ewaluacja RAG i jakości odpowiedzi mailowej

## 1. Cel etapu

Celem etapu 12 było rozszerzenie dotychczasowej ewaluacji offline o metryki jakości retrievalu RAG oraz jakości wygenerowanej odpowiedzi mailowej. Ocenie podlega nie tylko poprawność klasyfikacji kategorii i priorytetu zgłoszenia, ale również trafność doboru artykułów bazy wiedzy, obecność oczekiwanych słów kluczowych w odpowiedzi końcowej i zgodność tekstu z wymaganym formatem komunikacji e-mail.

Istotnym założeniem etapu było zachowanie bezpieczeństwa kosztowego i testowego. Z tego powodu tryb `openai_rag` może zostać uruchomiony wyłącznie po jawnym przekazaniu flagi `--allow-openai`, a brak zmiennej `OPENAI_API_KEY` skutkuje pominięciem lub fallbackiem do providera mock. Dzięki temu automatyczne testy i standardowa ewaluacja deweloperska nie wymagają dostępu do rzeczywistego API OpenAI.

## 2. Metodyka ewaluacji

Metodyka ewaluacji opiera się na kontrolowanym zbiorze testowym z referencyjną kategorią, priorytetem, oczekiwanymi słowami kluczowymi rozwiązania, oczekiwanymi słowami kluczowymi źródeł RAG oraz oczekiwanym formatem odpowiedzi. Dla każdego przypadku testowego wykonywane są kolejno: klasyfikacja rule-based, priorytetyzacja rule-based, opcjonalny retrieval RAG, generacja odpowiedzi końcowej i obliczenie metryk jakości.

Ewaluacja może działać w trzech trybach. Tryb `mock` stanowi baseline bez realnego retrievalu RAG i bez wywołań OpenAI. Tryb `rag` wykorzystuje retriever RAG, ale może pozostać przy mockowym generatorze odpowiedzi, co pozwala oddzielić wpływ źródeł od wpływu modelu generatywnego. Tryb `openai_rag` uruchamia wariant z generacją OpenAI wyłącznie po spełnieniu warunków bezpieczeństwa konfiguracji.

## 3. Zbiór danych testowych

Zbiór testowy składa się z syntetycznych zgłoszeń helpdesk obejmujących obszary takie jak konto i dostęp, sieć i VPN, aplikacje biznesowe, sprzęt komputerowy, poczta e-mail, bezpieczeństwo oraz system operacyjny. Każdy rekord zawiera opis problemu, etykietę oczekiwanej kategorii, etykietę oczekiwanego priorytetu oraz słowa kluczowe opisujące pożądane rozwiązanie.

W etapie 12 zbiór został rozszerzony o pola `expected_article_keywords`, `expected_answer_format` oraz `expected_rag_category`. Dzięki temu możliwe stało się nie tylko sprawdzenie poprawności predykcji klasyfikacyjnych, ale również ilościowa ocena, czy system pobrał artykuły zgodne z oczekiwanym kontekstem oraz czy odpowiedź końcowa zachowuje formę mailową przydatną dla agenta helpdesk.

## 4. Metryki retrievalu

Ocena retrievalu została oparta na czterech metrykach. `hit@k` przyjmuje wartość 1, gdy w top-k zwróconych artykułach wystąpi przynajmniej jedno oczekiwane słowo kluczowe. `MRR` (Mean Reciprocal Rank) mierzy odwrotność pozycji pierwszego trafnego wyniku, dzięki czemu premiuje poprawne dopasowanie wysoko na liście. `average_retrieval_score` opisuje średni score zwróconych wyników retrievalu. `source_keyword_coverage` pokazuje, jaki odsetek oczekiwanych słów kluczowych został pokryty przez zretrievowane źródła.

Tak zdefiniowany zestaw metryk pozwala spojrzeć na retriever wielowymiarowo. Sam `hit@k` mówi, czy w ogóle pojawiło się trafienie, ale nie uwzględnia jego pozycji. `MRR` uzupełnia ten brak. `Coverage` dobrze pokazuje, czy zwrócone artykuły reprezentują pełniejszy kontekst rozwiązania, a nie tylko pojedyncze przypadkowe dopasowanie.

## 5. Metryki formatu odpowiedzi mailowej

Jakość odpowiedzi mailowej jest oceniana heurystycznie. Sprawdzane są: obecność powitania `Dzień dobry`, obecność zamknięcia `Pozdrawiam`, podpis agenta, występowanie praktycznych kroków do wykonania oraz obecność oczekiwanych słów kluczowych w treści odpowiedzi. Końcowy `mail_format_score` mieści się w przedziale od 0 do 5.

Takie podejście nie zastępuje oceny eksperta, ale daje powtarzalny i tani obliczeniowo mechanizm porównywania wariantów systemu. W kontekście pracy inżynierskiej metryka może zostać użyta jako obiektywizowany wskaźnik tego, czy generowana odpowiedź ma strukturę zbliżoną do wiadomości przygotowywanej przez pracownika helpdesk.

## 6. Tryby ewaluacji

Tryb `mock` służy jako bezpieczny punkt odniesienia. Pozwala uruchomić pełny pipeline ewaluacyjny bez użycia zewnętrznych usług oraz bez kosztów API. W tym wariancie metryki retrievalu są zerowe albo ograniczone zgodnie z implementacją, co pozwala łatwo porównać go z trybem rozszerzonym o RAG.

Tryb `rag` wykorzystuje `RAGRetriever`, dzięki czemu możliwa jest realna ocena trafności doboru artykułów z bazy wiedzy. Generacja odpowiedzi może pozostać mockowa, co pozwala skupić analizę na wpływie kontekstu źródłowego. Tryb `openai_rag` uruchamia wariant z providerem OpenAI tylko wtedy, gdy ustawiono `OPENAI_API_KEY` i przekazano flagę `--allow-openai`. Brak jednego z tych warunków oznacza bezpieczny fallback do lokalnego providera mock.

## 7. Wyniki i interpretacja

Wyniki ewaluacji są zapisywane w trzech artefaktach: `evaluation_summary.json`, `evaluation_results.csv` oraz `evaluation_report.md`. Plik JSON zawiera zagregowane metryki i szczegóły per-case, plik CSV ułatwia dalszą analizę tabelaryczną, a raport Markdown dostarcza gotowego opisu po polsku z interpretacją wyników, przykładami przypadków poprawnych i błędnych oraz listą ograniczeń.

Interpretacja wyników powinna uwzględniać zależność między jakością retrievalu i jakością odpowiedzi końcowej. Wysokie `hit@3` i `MRR` sugerują, że system potrafi pobrać adekwatne źródła, jednak dopiero zestawienie tych metryk z `answer_quality_score` i `mail_format_score` pokazuje, czy retrieved context przekłada się na użyteczną odpowiedź dla użytkownika końcowego.

## 8. Ograniczenia

Najważniejszym ograniczeniem rozwiązania jest syntetyczny charakter datasetu. Chociaż taki zbiór pozwala na kontrolowane eksperymenty, nie odzwierciedla w pełni różnorodności zgłoszeń rzeczywistych użytkowników. Dodatkowo metryki retrievalu opierają się na dopasowaniu słów kluczowych, a nie na ręcznie oznaczonych zbiorach relewantnych dokumentów.

Drugim ograniczeniem jest heurystyczna ocena jakości odpowiedzi mailowej. Obecność powitania, zamknięcia czy listy kroków nie gwarantuje, że odpowiedź jest merytorycznie kompletna lub optymalna. Trzecim ograniczeniem jest zależność jakości wariantu `openai_rag` od konfiguracji środowiska oraz od modelu zewnętrznego, co utrudnia pełną powtarzalność wyników bez zamrożenia całego środowiska eksperymentalnego.

## 9. Materiał do rozdziału testowego pracy

Poniższy akapit można wykorzystać bezpośrednio w pracy inżynierskiej:

„W etapie 12 rozszerzono moduł ewaluacji offline o ocenę retrievalu RAG oraz jakości odpowiedzi mailowej generowanej przez system helpdesk AI. Oprócz klasycznych metryk klasyfikacji i priorytetyzacji zastosowano metryki `hit@k`, `MRR` i `coverage`, które pozwalają ocenić trafność doboru artykułów z bazy wiedzy. Dodatkowo wprowadzono heurystyczną ocenę formatu odpowiedzi mailowej, sprawdzającą obecność powitania, zakończenia, podpisu agenta, praktycznych kroków do wykonania oraz oczekiwanych słów kluczowych.”

Poniższy akapit można wykorzystać do interpretacji wyników:

„Rozszerzona ewaluacja umożliwia analizę zależności między trafnością retrievalu a jakością odpowiedzi końcowej. Dzięki porównaniu trybów `mock`, `rag` oraz opcjonalnie `openai_rag` możliwe jest wskazanie, w jakim stopniu użycie źródeł RAG oraz modelu generatywnego wpływa na kompletność i użyteczność odpowiedzi przygotowywanej dla użytkownika końcowego. Jednocześnie zachowano bezpieczne zasady uruchamiania eksperymentów, eliminujące niezamierzone koszty API w standardowym pipeline testowym.”

Poniższy akapit można wykorzystać do omówienia ograniczeń:

„Należy podkreślić, że przedstawione wyniki mają charakter eksperymentalny i zostały uzyskane na syntetycznym zbiorze testowym. Zastosowane metryki jakości odpowiedzi mailowej mają charakter heurystyczny, a metryki retrievalu opierają się na dopasowaniu słów kluczowych do zwróconych artykułów. Z tego względu wyniki należy traktować jako wskaźnik porównawczy przydatny do oceny kierunku rozwoju systemu, a nie jako pełny substytut eksperckiej walidacji produkcyjnej.”