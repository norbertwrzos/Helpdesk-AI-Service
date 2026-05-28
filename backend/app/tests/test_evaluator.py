"""
Testy jednostkowe dla modułu evaluator.py.

Testy uruchamiają EvaluationRunner na małym przykładowym zestawie danych
bez zapisu do bazy danych.
"""

from __future__ import annotations

import csv
import json
import os
import tempfile

import pytest

from app.evaluation.evaluator import EvaluationRunner, EvaluationResult


# Minimalny zestaw przypadków testowych do testów
SAMPLE_CASES = [
    {
        "id": "S001",
        "title": "Nie mogę się zalogować — błąd hasła",
        "description": "Nie mogę się zalogować do systemu. Pojawia się błąd logowania.",
        "expected_category": "Konto i dostęp",
        "expected_priority": "Średni",
        "expected_solution_keywords": "reset hasła; konto; logowanie",
        "notes": "Jasny przypadek logowania",
    },
    {
        "id": "S002",
        "title": "VPN nie łączy się",
        "description": "Klient VPN zwraca błąd połączenia z siecią firmową.",
        "expected_category": "Sieć i VPN",
        "expected_priority": "Średni",
        "expected_solution_keywords": "klient VPN; połączenie; administrator sieci",
        "notes": "Klasyczny problem VPN",
    },
    {
        "id": "S003",
        "title": "Wykryto wirusa na stacji",
        "description": "Antywirus wykrył wirusa na stacji roboczej pracownika.",
        "expected_category": "Bezpieczeństwo",
        "expected_priority": "Wysoki",
        "expected_solution_keywords": "wirus; antywirus; skanowanie; incydent",
        "notes": "Incydent bezpieczeństwa",
    },
    {
        "id": "S004",
        "title": "Prośba o konfigurację drukarki",
        "description": "Proszę o konfigurację drukarki sieciowej w biurze.",
        "expected_category": "Sprzęt komputerowy",
        "expected_priority": "Niski",
        "expected_solution_keywords": "drukarka; konfiguracja; sterownik",
        "notes": "Niski priorytet",
    },
    {
        "id": "S005",
        "title": "Cały dział bez dostępu do systemu",
        "description": "Awaria krytyczna — cały dział nie ma dostępu do systemu od rana.",
        "expected_category": "Konto i dostęp",
        "expected_priority": "Krytyczny",
        "expected_solution_keywords": "dostęp; awaria; administrator",
        "notes": "Krytyczny problem",
    },
]


def _write_csv(path: str, cases: list[dict]) -> None:
    """Pomocnik: zapisuje przypadki testowe do pliku CSV."""
    if not cases:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(cases[0].keys()))
        writer.writeheader()
        writer.writerows(cases)


def _write_json(path: str, cases: list[dict]) -> None:
    """Pomocnik: zapisuje przypadki testowe do pliku JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)


class TestEvaluationRunnerBasics:
    def test_run_returns_evaluation_result(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            _write_csv(csv_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            result = runner.run(input_path=csv_path)

        assert isinstance(result, EvaluationResult)

    def test_total_cases_correct(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            _write_csv(csv_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            result = runner.run(input_path=csv_path)

        assert result.total_cases == len(SAMPLE_CASES)

    def test_case_results_length_matches_total(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            _write_csv(csv_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            result = runner.run(input_path=csv_path)

        assert len(result.case_results) == result.total_cases

    def test_run_from_json_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "test.json")
            _write_json(json_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            result = runner.run(input_path=json_path)

        assert result.total_cases == len(SAMPLE_CASES)


class TestEvaluationMetrics:
    @pytest.fixture
    def result(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            _write_csv(csv_path, SAMPLE_CASES)
            runner = EvaluationRunner()
            return runner.run(input_path=csv_path)

    def test_classification_accuracy_in_range(self, result):
        assert 0.0 <= result.classification_accuracy <= 1.0

    def test_classification_macro_f1_in_range(self, result):
        assert 0.0 <= result.classification_macro_f1 <= 1.0

    def test_classification_weighted_f1_in_range(self, result):
        assert 0.0 <= result.classification_weighted_f1 <= 1.0

    def test_priority_accuracy_in_range(self, result):
        assert 0.0 <= result.priority_accuracy <= 1.0

    def test_priority_macro_f1_in_range(self, result):
        assert 0.0 <= result.priority_macro_f1 <= 1.0

    def test_priority_weighted_f1_in_range(self, result):
        assert 0.0 <= result.priority_weighted_f1 <= 1.0

    def test_average_quality_score_in_range(self, result):
        assert 0.0 <= result.average_answer_quality_score <= 5.0

    def test_average_response_length_positive(self, result):
        assert result.average_response_length > 0

    def test_classification_report_has_entries(self, result):
        assert len(result.classification_report) > 0
        for row in result.classification_report:
            assert "label" in row
            assert "precision" in row
            assert "recall" in row
            assert "f1_score" in row
            assert "support" in row

    def test_priority_report_has_entries(self, result):
        assert len(result.priority_report) > 0

    def test_confusion_matrices_not_empty(self, result):
        assert result.classification_confusion_matrix
        assert result.priority_confusion_matrix


class TestReportGeneration:
    def test_reports_written_to_output_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            output_dir = os.path.join(tmpdir, "reports")
            _write_csv(csv_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            runner.run(input_path=csv_path, output_dir=output_dir)

            assert os.path.exists(os.path.join(output_dir, "evaluation_summary.json"))
            assert os.path.exists(os.path.join(output_dir, "evaluation_results.csv"))
            assert os.path.exists(os.path.join(output_dir, "evaluation_report.md"))

    def test_json_report_is_valid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            output_dir = os.path.join(tmpdir, "reports")
            _write_csv(csv_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            runner.run(input_path=csv_path, output_dir=output_dir)

            json_path = os.path.join(output_dir, "evaluation_summary.json")
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)

            assert "total_cases" in data
            assert "classification_accuracy" in data
            assert "priority_accuracy" in data
            assert data["total_cases"] == len(SAMPLE_CASES)

    def test_markdown_report_contains_polish_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            output_dir = os.path.join(tmpdir, "reports")
            _write_csv(csv_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            runner.run(input_path=csv_path, output_dir=output_dir)

            md_path = os.path.join(output_dir, "evaluation_report.md")
            with open(md_path, encoding="utf-8") as f:
                content = f.read()

            assert "Raport ewaluacji" in content
            assert "klasyfikacji" in content.lower()

    def test_csv_results_has_all_cases(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            output_dir = os.path.join(tmpdir, "reports")
            _write_csv(csv_path, SAMPLE_CASES)

            runner = EvaluationRunner()
            runner.run(input_path=csv_path, output_dir=output_dir)

            results_csv = os.path.join(output_dir, "evaluation_results.csv")
            with open(results_csv, encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            assert len(rows) == len(SAMPLE_CASES)


class TestCaseResults:
    @pytest.fixture
    def case_results(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            _write_csv(csv_path, SAMPLE_CASES)
            runner = EvaluationRunner()
            result = runner.run(input_path=csv_path)
            return result.case_results

    def test_each_case_has_id(self, case_results):
        for case in case_results:
            assert case.id != ""

    def test_each_case_has_predicted_category(self, case_results):
        for case in case_results:
            assert case.predicted_category != ""

    def test_each_case_has_predicted_priority(self, case_results):
        for case in case_results:
            assert case.predicted_priority != ""

    def test_quality_score_in_range(self, case_results):
        for case in case_results:
            assert 0 <= case.answer_quality_score <= 5

    def test_vpn_ticket_classified_as_siec(self, case_results):
        vpn_case = next((c for c in case_results if c.id == "S002"), None)
        assert vpn_case is not None
        assert vpn_case.predicted_category == "Sieć i VPN"

    def test_security_ticket_classified_correctly(self, case_results):
        sec_case = next((c for c in case_results if c.id == "S003"), None)
        assert sec_case is not None
        assert sec_case.predicted_category == "Bezpieczeństwo"
