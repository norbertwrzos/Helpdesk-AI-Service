from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def _normalize_keywords(expected_keywords: Sequence[str]) -> list[str]:
    return [keyword.strip() for keyword in expected_keywords if keyword and keyword.strip()]


def _article_text(article: Any) -> str:
    title = getattr(article, "title", "") or ""
    excerpt = getattr(article, "excerpt", "") or ""
    return f"{title} {excerpt}".lower()


def _has_expected_keyword(article: Any, expected_keywords: Sequence[str]) -> bool:
    haystack = _article_text(article)
    return any(keyword.lower() in haystack for keyword in expected_keywords)


def hit_at_k(
    expected_keywords: Sequence[str],
    retrieved_articles: Sequence[Any],
    k: int,
) -> float:
    normalized_keywords = _normalize_keywords(expected_keywords)
    if not normalized_keywords or k <= 0:
        return 0.0

    top_articles = list(retrieved_articles[:k])
    return 1.0 if any(_has_expected_keyword(article, normalized_keywords) for article in top_articles) else 0.0


def mean_reciprocal_rank(
    expected_keywords: Sequence[str],
    retrieved_articles: Sequence[Any],
) -> float:
    normalized_keywords = _normalize_keywords(expected_keywords)
    if not normalized_keywords:
        return 0.0

    for index, article in enumerate(retrieved_articles, start=1):
        if _has_expected_keyword(article, normalized_keywords):
            return 1.0 / index
    return 0.0


def average_retrieval_score(retrieved_articles: Sequence[Any]) -> float:
    if not retrieved_articles:
        return 0.0

    scores = [float(getattr(article, "score", 0.0) or 0.0) for article in retrieved_articles]
    return sum(scores) / len(scores)


def source_keyword_coverage(
    expected_keywords: Sequence[str],
    retrieved_articles: Sequence[Any],
) -> float:
    normalized_keywords = _normalize_keywords(expected_keywords)
    if not normalized_keywords:
        return 0.0

    haystack = " ".join(_article_text(article) for article in retrieved_articles)
    matched = [keyword for keyword in normalized_keywords if keyword.lower() in haystack]
    return len(matched) / len(normalized_keywords)