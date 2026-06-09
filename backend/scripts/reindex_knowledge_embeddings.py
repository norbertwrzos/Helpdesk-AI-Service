#!/usr/bin/env python3
"""
Reindeksacja embeddingów artykułów bazy wiedzy.

Uruchomienie (z katalogu backend/):
    python scripts/reindex_knowledge_embeddings.py
    python scripts/reindex_knowledge_embeddings.py --force
    python scripts/reindex_knowledge_embeddings.py --limit 10
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.services.knowledge_embedding_service import KnowledgeEmbeddingService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reindeksacja embeddingów bazy wiedzy")
    parser.add_argument("--force", action="store_true", help="Wymusza ponowne przeliczenie embeddingów")
    parser.add_argument("--limit", type=int, default=None, help="Ogranicza liczbę przetwarzanych artykułów")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db = SessionLocal()
    service = KnowledgeEmbeddingService()

    try:
        summary = service.reindex_all(db, force=args.force, limit=args.limit)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())