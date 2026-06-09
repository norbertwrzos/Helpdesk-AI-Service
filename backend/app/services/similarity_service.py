"""
SimilarityService — wyszukiwanie podobnych artykułów w bazie wiedzy.

Na tym etapie stosuje prostą metodę opartą na liczeniu wspólnych słów
(bag-of-words). W przyszłości można zastąpić tę klasę implementacją
opartą na embeddingach i pgvector bez zmian w AnalysisPipeline.
"""

import re

from app.models.knowledge_article import KnowledgeArticle
from app.schemas.analysis import SimilarArticle

EXCERPT_LENGTH = 200
TOP_K = 3
SAME_CATEGORY_BONUS = 0.2


def _tokenize(text: str) -> set[str]:
    """Zamienia tekst na zbiór tokenów (słów) bez interpunkcji."""
    return set(re.findall(r"\w+", text.lower()))


def _excerpt(content: str) -> str:
    if len(content) <= EXCERPT_LENGTH:
        return content
    return content[:EXCERPT_LENGTH].rsplit(" ", 1)[0] + "…"


class SimilarityService:
    """
    Wyszukuje podobne artykuły metodą bag-of-words.

    W przyszłości można zastąpić tę klasę implementacją
    opartą na embeddingach bez zmian w AnalysisPipeline.
    """

    def find_similar(
        self,
        title: str,
        description: str,
        articles: list[KnowledgeArticle],
        classification_category_id: int | None = None,
        top_k: int | None = None,
    ) -> list[SimilarArticle]:
        if not articles:
            return []

        query_tokens = _tokenize(title + " " + description)
        if not query_tokens:
            return []

        scored: list[tuple[float, KnowledgeArticle]] = []
        for article in articles:
            article_tokens = _tokenize(article.title + " " + article.content)
            if not article_tokens:
                continue

            common = query_tokens & article_tokens
            score = len(common) / (len(query_tokens | article_tokens) + 1e-9)

            if (
                classification_category_id is not None
                and article.category_id == classification_category_id
            ):
                score += SAME_CATEGORY_BONUS

            scored.append((score, article))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[: (top_k or TOP_K)]

        return [
            SimilarArticle(
                id=art.id,
                title=art.title,
                excerpt=_excerpt(art.content),
                category_id=art.category_id,
                score=round(score, 4),
            )
            for score, art in top
            if score > 0
        ]
