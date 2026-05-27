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

# Uruchom serwer deweloperski
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend dostępny pod: http://localhost:8000

Dokumentacja Swagger UI: http://localhost:8000/docs

---

## Uruchomienie frontendu

```bash
cd frontend

# Zainstaluj zależności
npm install

# Uruchom serwer deweloperski
npm run dev
```

Frontend dostępny pod: http://localhost:5173

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
