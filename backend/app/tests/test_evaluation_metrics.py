"""
Testy jednostkowe dla modułu metrics.py.
"""

from app.evaluation.metrics import (
    accuracy_score,
    classification_report_as_dict,
    confusion_matrix_as_dict,
    macro_f1,
    weighted_f1,
)


class TestAccuracyScore:
    def test_perfect_accuracy(self):
        y_true = ["A", "B", "C"]
        y_pred = ["A", "B", "C"]
        assert accuracy_score(y_true, y_pred) == 1.0

    def test_zero_accuracy(self):
        y_true = ["A", "A", "A"]
        y_pred = ["B", "B", "B"]
        assert accuracy_score(y_true, y_pred) == 0.0

    def test_partial_accuracy(self):
        y_true = ["A", "B", "A", "B"]
        y_pred = ["A", "A", "A", "B"]
        # 3 z 4 poprawnych
        assert accuracy_score(y_true, y_pred) == 0.75

    def test_empty_lists(self):
        assert accuracy_score([], []) == 0.0

    def test_single_element_correct(self):
        assert accuracy_score(["X"], ["X"]) == 1.0

    def test_single_element_wrong(self):
        assert accuracy_score(["X"], ["Y"]) == 0.0


class TestMacroF1:
    def test_perfect_macro_f1(self):
        y_true = ["A", "B", "A", "B"]
        y_pred = ["A", "B", "A", "B"]
        assert macro_f1(y_true, y_pred) == 1.0

    def test_simple_binary_case(self):
        # Jeden błąd: A -> B
        y_true = ["A", "A", "B", "B"]
        y_pred = ["A", "B", "B", "B"]
        score = macro_f1(y_true, y_pred)
        assert 0.0 < score < 1.0

    def test_empty_returns_zero(self):
        assert macro_f1([], []) == 0.0

    def test_multiclass(self):
        y_true = ["A", "B", "C", "A", "B", "C"]
        y_pred = ["A", "B", "C", "A", "B", "C"]
        assert macro_f1(y_true, y_pred) == 1.0


class TestWeightedF1:
    def test_perfect_weighted_f1(self):
        y_true = ["A", "B", "C"]
        y_pred = ["A", "B", "C"]
        assert weighted_f1(y_true, y_pred) == 1.0

    def test_empty_returns_zero(self):
        assert weighted_f1([], []) == 0.0

    def test_all_wrong(self):
        y_true = ["A", "A"]
        y_pred = ["B", "B"]
        assert weighted_f1(y_true, y_pred) == 0.0


class TestConfusionMatrix:
    def test_perfect_matrix(self):
        y_true = ["A", "B"]
        y_pred = ["A", "B"]
        labels = ["A", "B"]
        matrix = confusion_matrix_as_dict(y_true, y_pred, labels)
        assert matrix["A"]["A"] == 1
        assert matrix["A"]["B"] == 0
        assert matrix["B"]["A"] == 0
        assert matrix["B"]["B"] == 1

    def test_one_error(self):
        y_true = ["A", "A", "B"]
        y_pred = ["A", "B", "B"]
        labels = ["A", "B"]
        matrix = confusion_matrix_as_dict(y_true, y_pred, labels)
        assert matrix["A"]["A"] == 1
        assert matrix["A"]["B"] == 1  # błąd: A przewidziane jako B
        assert matrix["B"]["B"] == 1

    def test_returns_all_labels(self):
        y_true = ["A"]
        y_pred = ["A"]
        labels = ["A", "B", "C"]
        matrix = confusion_matrix_as_dict(y_true, y_pred, labels)
        assert set(matrix.keys()) == {"A", "B", "C"}
        for row in matrix.values():
            assert set(row.keys()) == {"A", "B", "C"}


class TestClassificationReport:
    def test_report_contains_required_fields(self):
        y_true = ["A", "B", "A"]
        y_pred = ["A", "A", "B"]
        labels = ["A", "B"]
        report = classification_report_as_dict(y_true, y_pred, labels)

        assert len(report) == 2
        for row in report:
            assert "label" in row
            assert "precision" in row
            assert "recall" in row
            assert "f1_score" in row
            assert "support" in row

    def test_report_labels_order(self):
        y_true = ["A", "B", "C"]
        y_pred = ["A", "B", "C"]
        labels = ["C", "B", "A"]
        report = classification_report_as_dict(y_true, y_pred, labels)
        assert [r["label"] for r in report] == ["C", "B", "A"]

    def test_report_perfect_scores(self):
        y_true = ["A", "B"]
        y_pred = ["A", "B"]
        labels = ["A", "B"]
        report = classification_report_as_dict(y_true, y_pred, labels)
        for row in report:
            assert row["precision"] == 1.0
            assert row["recall"] == 1.0
            assert row["f1_score"] == 1.0

    def test_report_support_counts(self):
        y_true = ["A", "A", "B"]
        y_pred = ["A", "B", "B"]
        labels = ["A", "B"]
        report = classification_report_as_dict(y_true, y_pred, labels)
        support = {r["label"]: r["support"] for r in report}
        assert support["A"] == 2
        assert support["B"] == 1
