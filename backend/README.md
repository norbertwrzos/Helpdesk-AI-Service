# Backend — Helpdesk AI Service

Backend aplikacji oparty na FastAPI + PostgreSQL + SQLAlchemy.

## Uruchomienie

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testy

```bash
pytest app/tests/
```

## Migracje (Alembic)

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```
