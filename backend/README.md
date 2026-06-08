# Backend — Helpdesk AI Service

Backend FastAPI obsługuje zgłoszenia, bazę wiedzy, analizę AI, feedback i metryki jakości.

## Uruchomienie

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_data.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testy

```bash
source .venv/bin/activate
pytest
```

## Migracje

Repozytorium używa jednej czystej migracji bazowej zgodnej z aktualnym schematem prototypu.

Jeśli lokalna baza pochodzi sprzed cleanupu migracji:

```bash
docker compose down -v
docker compose up -d
source .venv/bin/activate
alembic upgrade head
python scripts/seed_data.py
```

Jeżeli baza ma już poprawny schemat, ale Alembic nadal wskazuje usuniętą rewizję `007_remove_email_features`, wykonaj:

```bash
source .venv/bin/activate
alembic stamp 001_initial --purge
alembic upgrade head
```
