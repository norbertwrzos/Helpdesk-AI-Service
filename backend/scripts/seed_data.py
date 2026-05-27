#!/usr/bin/env python3
"""
Skrypt seedowania danych — wczytuje kategorie, priorytety i artykuły bazy wiedzy
z plików JSON i zapisuje je w bazie danych.

Uruchomienie (z katalogu backend/):
    python scripts/seed_data.py

Skrypt jest idempotentny — nie tworzy duplikatów przy ponownym uruchomieniu.
"""

import json
import os
import sys

# Upewnij się, że app jest na ścieżce importów
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.priority import Priority

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "seed",
)


def load_json(filename: str) -> list[dict]:
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def seed_categories(db) -> dict[str, int]:
    """Tworzy kategorie i zwraca mapę nazwa→id."""
    data = load_json("categories.json")
    category_map: dict[str, int] = {}
    created = 0

    for item in data:
        existing = db.query(Category).filter(Category.name == item["name"]).first()
        if existing:
            category_map[existing.name] = existing.id
        else:
            cat = Category(name=item["name"], description=item.get("description"))
            db.add(cat)
            db.flush()
            category_map[cat.name] = cat.id
            created += 1

    db.commit()
    print(f"  Kategorie: {created} dodanych, {len(data) - created} już istniało.")
    return category_map


def seed_priorities(db) -> None:
    data = load_json("priorities.json")
    created = 0

    for item in data:
        existing = db.query(Priority).filter(Priority.name == item["name"]).first()
        if not existing:
            pri = Priority(
                name=item["name"],
                level=item["level"],
                description=item.get("description"),
            )
            db.add(pri)
            created += 1

    db.commit()
    print(f"  Priorytety: {created} dodanych, {len(data) - created} już istniało.")


def seed_knowledge_base(db, category_map: dict[str, int]) -> None:
    data = load_json("knowledge_base.json")
    created = 0

    for item in data:
        existing = (
            db.query(KnowledgeArticle)
            .filter(KnowledgeArticle.title == item["title"])
            .first()
        )
        if not existing:
            category_id = category_map.get(item.get("category_name", ""))
            article = KnowledgeArticle(
                title=item["title"],
                content=item["content"],
                category_id=category_id,
                tags=item.get("tags"),
            )
            db.add(article)
            created += 1

    db.commit()
    print(f"  Artykuły bazy wiedzy: {created} dodanych, {len(data) - created} już istniało.")


def main() -> None:
    print("Seedowanie bazy danych…")
    db = SessionLocal()
    try:
        print("→ Kategorie")
        category_map = seed_categories(db)

        print("→ Priorytety")
        seed_priorities(db)

        print("→ Baza wiedzy")
        seed_knowledge_base(db, category_map)

        print("✓ Seedowanie zakończone pomyślnie.")
    except Exception as exc:
        db.rollback()
        print(f"✗ Błąd podczas seedowania: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
