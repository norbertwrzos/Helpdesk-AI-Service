"""
evaluator.py — główny runner ewaluacji pipeline'u analizy zgłoszeń.

EvaluationRunner:
- Wczytuje dane testowe z CSV lub JSON.
- Dla każdego zgłoszenia uruchamia ClassificationService, PriorityAnalysisService
  i MockAIGenerator bez zapisu do bazy danych.
- Oblicza metryki klasyfikacji, priorytetyzacji i jakości odpowiedzi.
- Zwraca EvaluationResult z pełnymi wynikami.

Uwaga: usługi są uruchamiane bezpośrednio (bez bazy danych).
Kategorie i priorytety są wczytywane z plików seed lub z uproszczonych stub-obiektów.
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any

from app.evaluation.answer_quality import evaluate_answer_quality
from app.evaluation.metrics import (
    accuracy_score,
    classification_report_as_dict,
    confusion_matrix_as_dict,
    macro_f1,
    weighted_f1,
)
from app.services.ai_generator import MockAIGenerator
from app.services.classification_service import ClassificationService
from app.services.priority_analysis_service import PriorityAnalysisService

# Ścieżka do pliku seed kategorii (względem lokalizacji tego pliku)
_THIS_DIR = os.path.dirname(__file__)
_SEED_DIR = os.path.normpath(os.path.join(_THIS_DIR, "../../../../data/seed"))

CATEGORY_LABELS = [
    "Konto i dostęp",
    "Sieć i VPN",
    "Aplikacje biznesowe",
    "Sprzęt komputerowy",
    "Poczta e-mail",
    "Bezpieczeństwo",
    "System operacyjny",
    "Inne",
]

PRIORITY_LABELS = ["Niski", "Średni", "Wysoki", "Krytyczny"]


def _load_stub_categories() -> list:
    """Wczytuje kategorie z pliku seed albo zwraca domyślne stubs."""
    seed_path = os.path.join(_SEED_DIR, "categories.json")
    try:
        with open(seed_path, encoding="utf-8") as f:
            data = json.load(f)
        return [
            SimpleNamespace(id=i + 1, name=item["name"], description=item.get("description", ""))
            for i, item in enumerate(data)
        ]
    except (FileNotFoundError, json.JSONDecodeError):
        return [
            SimpleNamespace(id=i + 1, name=name, description="")
            for i, name in enumerate(CATEGORY_LABELS)
        ]


def _load_stub_priorities() -> list:
    """Wczytuje priorytety z pliku seed albo zwraca domyślne stubs."""
    seed_path = os.path.join(_SEED_DIR, "priorities.json")
    try:
        with open(seed_path, encoding="utf-8") as f:
            data = json.load(f)
        return [
            SimpleNamespace(id=i + 1, name=item["name"], level=item.get("level", i + 1))
            for i, item in enumerate(data)
        ]
    except (FileNotFoundError, json.JSONDecodeError):
        return [
            SimpleNamespace(id=i + 1, name=name, level=i + 1)
            for i, name in enumerate(PRIORITY_LABELS)
        ]


def _make_stub_ticket(row: dict[str, str]) -> SimpleNamespace:
    """Tworzy uproszczony obiekt zgłoszenia dla MockAIGenerator."""
    return SimpleNamespace(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        status="new",
        source="csv",
        category_id=None,
        priority_id=None,
    )


def _parse_keywords(raw: str) -> list[str]:
    """Parsuje listę słów kluczowych rozdzielonych średnikiem."""
    return [kw.strip() for kw in raw.split(";") if kw.strip()]


@dataclass
class CaseResult:
    """Wynik ewaluacji pojedynczego zgłoszenia."""

    id: str
    title: str
    expected_category: str
    predicted_category: str
    category_correct: bool
    category_confidence: float
    expected_priority: str
    predicted_priority: str
    priority_correct: bool
    priority_confidence: float
    generated_answer: str
    answer_quality_score: int
    answer_quality_notes: str
    matched_keywords: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    """Zbiorczy wynik ewaluacji."""

    generated_at: str
    total_cases: int
    case_results: list[CaseResult]

    classification_accuracy: float
    classification_macro_f1: float
    classification_weighted_f1: float

    priority_accuracy: float
    priority_macro_f1: float
    priority_weighted_f1: float

    average_answer_quality_score: float
    average_response_length: float

    classification_report: list[dict]
    priority_report: list[dict]
    classification_confusion_matrix: dict[str, dict[str, int]]
    priority_confusion_matrix: dict[str, dict[str, int]]


class EvaluationRunner:
    """
    Uruchamia ewaluację pipeline'u analizy zgłoszeń na zbiorze testowym.

    Nie zapisuje zgłoszeń do bazy danych — usługi są wywoływane bezpośrednio
    z uproszczonymi stub-obiektami. Pozwala to na szybkie uruchamianie ewaluacji
    bez konieczności posiadania uruchomionej bazy danych.
    """

    def __init__(self) -> None:
        self.classifier = ClassificationService()
        self.priority_analyzer = PriorityAnalysisService()
        self.ai_generator = MockAIGenerator()
        self.categories = _load_stub_categories()
        self.priorities = _load_stub_priorities()

    def run(
        self,
        input_path: str,
        output_dir: str | None = None,
    ) -> EvaluationResult:
        """Uruchamia ewaluację i zwraca wyniki.

        Args:
            input_path: ścieżka do pliku CSV lub JSON z danymi testowymi.
            output_dir: katalog docelowy dla raportów (opcjonalnie).

        Returns:
            EvaluationResult z pełnymi wynikami ewaluacji.
        """
        rows = self._load_input(input_path)
        case_results = [self._evaluate_case(row) for row in rows]

        y_true_cat = [r.expected_category for r in case_results]
        y_pred_cat = [r.predicted_category for r in case_results]
        y_true_pri = [r.expected_priority for r in case_results]
        y_pred_pri = [r.predicted_priority for r in case_results]

        result = EvaluationResult(
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_cases=len(case_results),
            case_results=case_results,
            classification_accuracy=accuracy_score(y_true_cat, y_pred_cat),
            classification_macro_f1=macro_f1(y_true_cat, y_pred_cat),
            classification_weighted_f1=weighted_f1(y_true_cat, y_pred_cat),
            priority_accuracy=accuracy_score(y_true_pri, y_pred_pri),
            priority_macro_f1=macro_f1(y_true_pri, y_pred_pri),
            priority_weighted_f1=weighted_f1(y_true_pri, y_pred_pri),
            average_answer_quality_score=(
                sum(r.answer_quality_score for r in case_results) / len(case_results)
                if case_results else 0.0
            ),
            average_response_length=(
                sum(len(r.generated_answer) for r in case_results) / len(case_results)
                if case_results else 0.0
            ),
            classification_report=classification_report_as_dict(
                y_true_cat, y_pred_cat, CATEGORY_LABELS
            ),
            priority_report=classification_report_as_dict(
                y_true_pri, y_pred_pri, PRIORITY_LABELS
            ),
            classification_confusion_matrix=confusion_matrix_as_dict(
                y_true_cat, y_pred_cat, CATEGORY_LABELS
            ),
            priority_confusion_matrix=confusion_matrix_as_dict(
                y_true_pri, y_pred_pri, PRIORITY_LABELS
            ),
        )

        if output_dir:
            from app.evaluation.report_writer import ReportWriter
            writer = ReportWriter()
            writer.write_all(result, output_dir)

        return result

    def _load_input(self, path: str) -> list[dict[str, str]]:
        """Wczytuje dane z CSV lub JSON."""
        if path.endswith(".json"):
            return self._load_json(path)
        return self._load_csv(path)

    @staticmethod
    def _load_csv(path: str) -> list[dict[str, str]]:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]

    @staticmethod
    def _load_json(path: str) -> list[dict[str, str]]:
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _evaluate_case(self, row: dict[str, str]) -> CaseResult:
        """Ewaluuje jedno zgłoszenie."""
        title = row.get("title", "")
        description = row.get("description", "")
        expected_category = row.get("expected_category", "")
        expected_priority = row.get("expected_priority", "")
        expected_keywords = _parse_keywords(row.get("expected_solution_keywords", ""))

        # Klasyfikacja
        classification = self.classifier.classify(title, description, self.categories)

        # Priorytetyzacja
        priority = self.priority_analyzer.analyze(title, description, self.priorities)

        # Generowanie odpowiedzi
        ticket = _make_stub_ticket(row)
        generated = self.ai_generator.generate(
            ticket=ticket,
            classification=classification,
            priority=priority,
            similar_articles=[],
        )

        # Ocena jakości odpowiedzi
        quality = evaluate_answer_quality(generated.response_text, expected_keywords)

        return CaseResult(
            id=row.get("id", ""),
            title=title,
            expected_category=expected_category,
            predicted_category=classification.category_name,
            category_correct=(classification.category_name == expected_category),
            category_confidence=classification.confidence,
            expected_priority=expected_priority,
            predicted_priority=priority.priority_name,
            priority_correct=(priority.priority_name == expected_priority),
            priority_confidence=priority.confidence,
            generated_answer=generated.response_text,
            answer_quality_score=quality["score"],
            answer_quality_notes=quality["notes"],
            matched_keywords=quality["matched_keywords"],
            missing_keywords=quality["missing_keywords"],
        )
