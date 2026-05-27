# Helpdesk AI Service

> Projekt inżynierski: „Projekt i implementacja serwisu do zautomatyzowanego rozwiązywania zgłoszeń technicznych z wykorzystaniem metod sztucznej inteligencji"

---

## Opis projektu

Helpdesk AI Service to prototyp systemu IT Support, który automatyzuje obsługę zgłoszeń technicznych przy użyciu metod sztucznej inteligencji i przetwarzania języka naturalnego (NLP).

System docelowo:

- przyjmuje i importuje zgłoszenia techniczne (formularz, e-mail),
- analizuje i klasyfikuje zgłoszenia,
- nadaje priorytety,
- wyszukuje podobne historyczne przypadki,
- generuje propozycje rozwiązań z użyciem AI,
- przechowuje historię zgłoszeń,
- umożliwia ocenę jakości odpowiedzi AI.

---

## Cel pracy

Celem pracy inżynierskiej jest zaprojektowanie i zaimplementowanie prototypu serwisu helpdesk wspomaganego przez AI, który demonstruje praktyczne zastosowanie metod NLP w automatyzacji obsługi zgłoszeń technicznych.

---

## Technologie

| Warstwa      | Technologia                         |
|--------------|-------------------------------------|
| Backend      | Python 3.12, FastAPI                |
| Frontend     | React, TypeScript, Vite             |
| Baza danych  | PostgreSQL 16                       |
| ORM          | SQLAlchemy                          |
| Migracje     | Alembic                             |
| Kontenery    | Docker, Docker Compose              |
| Serwer email | GreenMail                           |
| Konfiguracja | pydantic-settings, .env             |
| Testy        | pytest                              |

---

## Struktura katalogów

```
helpdesk-ai-service/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # Endpointy FastAPI
│   │   ├── core/             # Konfiguracja aplikacji
│   │   ├── db/               # Sesja i silnik bazy danych
│   │   ├── models/           # Modele SQLAlchemy (ORM)
│   │   ├── schemas/          # Schematy Pydantic
│   │   ├── services/         # Logika biznesowa, AI, email
│   │   ├── tests/            # Testy jednostkowe i integracyjne
│   │   └── main.py           # Punkt wejściowy aplikacji
│   ├── alembic/              # Migracje bazy danych
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── api/              # Klienci HTTP (axios/fetch)
│   │   ├── components/       # Komponenty React
│   │   ├── pages/            # Strony aplikacji
│   │   ├── types/            # Typy TypeScript
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── data/
│   ├── seed/                 # Dane startowe
│   └── test_cases/           # Testowe zgłoszenia
├── docs/
│   ├── diagrams/             # Diagramy UML, C4
│   ├── api/                  # Dokumentacja API
│   ├── screenshots/          # Zrzuty ekranu
│   └── decisions/            # Decyzje architektoniczne (ADR)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Wymagania środowiskowe

- Python 3.12+
- Node.js 20+
- Docker + Docker Compose v2
- WSL2 Ubuntu (zalecane)

---

## Konfiguracja `.env`

Skopiuj plik `.env.example` i uzupełnij wartości:

```bash
cp .env.example .env
```

Kluczowe zmienne:

| Zmienna            | Opis                                      |
|--------------------|-------------------------------------------|
| `APP_ENV`          | Środowisko: `development` / `production`  |
| `DATABASE_URL`     | Connection string PostgreSQL              |
| `SECRET_KEY`       | Klucz aplikacji (zmień przed produkcją!)  |
| `AI_PROVIDER`      | Dostawca AI: `mock` / `openai`            |
| `OPENAI_API_KEY`   | Klucz API OpenAI (opcjonalny)             |
| `EMAIL_IMAP_*`     | Konfiguracja importu e-mail (GreenMail)   |

---

## Uruchomienie Dockera

Uruchamia PostgreSQL i GreenMail:

```bash
docker compose up -d
```

Zatrzymanie:

```bash
docker compose down
```

Logi:

```bash
docker compose logs -f
```

---

## Uruchomienie backendu

```bash
cd backend

# Utwórz i aktywuj środowisko wirtualne
python3 -m venv .venv
source .venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Wykonaj migracje (wymaga uruchomionego PostgreSQL)
alembic upgrade head

# Uruchom serwer deweloperski
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend dostępny pod: http://localhost:8000

Dokumentacja Swagger UI: http://localhost:8000/docs

---

## Uruchomienie testów

Testy używają bazy SQLite w pamięci — **nie wymagają uruchomionego PostgreSQL**.

```bash
cd backend
source .venv/bin/activate
pytest
```

---

## Dostępne endpointy (Etap 1)

| Metoda | Ścieżka                   | Opis                              |
|--------|---------------------------|-----------------------------------|
| GET    | /health                   | Weryfikacja dostępności serwisu   |
| GET    | /tickets                  | Lista zgłoszeń                    |
| POST   | /tickets                  | Utwórz zgłoszenie                 |
| GET    | /tickets/{id}             | Szczegóły zgłoszenia              |
| PATCH  | /tickets/{id}             | Aktualizacja zgłoszenia           |
| GET    | /categories               | Lista kategorii                   |
| POST   | /categories               | Utwórz kategorię                  |
| GET    | /priorities               | Lista priorytetów                 |
| POST   | /priorities               | Utwórz priorytet                  |

---

## Uruchomienie frontendu

```bash
cd frontend
npm install
npm run dev
```

Frontend dostępny pod: http://localhost:5173

Zmienna środowiskowa (opcjonalna):
```bash
cp frontend/.env.example frontend/.env
# VITE_API_BASE_URL=http://localhost:8000  (domyślna wartość)
```

---

## Weryfikacja buildu frontendu

```bash
cd frontend
npm run build
```

---

## Scenariusz testowy (Etap 2)

1. Uruchom PostgreSQL: `docker compose up -d`
2. Uruchom migracje: `cd backend && alembic upgrade head`
3. Uruchom backend: `uvicorn app.main:app --reload`
4. Uruchom frontend: `cd frontend && npm run dev`
5. Otwórz http://localhost:5173
6. Przejdź do `/tickets` → dodaj zgłoszenie przez formularz
7. Sprawdź, że zgłoszenie pojawia się na liście
8. Kliknij „Szczegóły" → zmień status → zapisz zmiany
9. Sprawdź, że zmiany są widoczne po odświeżeniu

---

## Endpoint `/health`

Służy do weryfikacji dostępności serwisu.

**Request:**
```
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

Używany przez Docker healthcheck, monitoring i testy integracyjne.

---

## Autor

Norbert Wrzos — Praca inżynierska, 2025/2026
