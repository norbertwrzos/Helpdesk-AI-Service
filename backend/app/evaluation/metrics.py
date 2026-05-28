"""
metrics.py — metryki jakości klasyfikacji i priorytetyzacji.

Implementacja oparta na czystym Pythonie (bez zewnętrznych bibliotek ML).
Obliczane metryki:
- accuracy
- precision, recall, F1 per label
- macro F1
- weighted F1
- macierz pomyłek
- raport klasyfikacji
"""

from __future__ import annotations


def accuracy_score(y_true: list[str], y_pred: list[str]) -> float:
    """Zwraca dokładność (accuracy) klasyfikacji.

    Args:
        y_true: lista oczekiwanych etykiet.
        y_pred: lista przewidywanych etykiet.

    Returns:
        Wartość accuracy w przedziale [0.0, 1.0].
    """
    if not y_true:
        return 0.0
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return correct / len(y_true)


def precision_recall_f1_per_label(
    y_true: list[str],
    y_pred: list[str],
) -> dict[str, dict[str, float]]:
    """Oblicza precision, recall i F1 dla każdej etykiety.

    Args:
        y_true: lista oczekiwanych etykiet.
        y_pred: lista przewidywanych etykiet.

    Returns:
        Słownik {etykieta: {precision, recall, f1_score, support}}.
    """
    labels = sorted(set(y_true) | set(y_pred))
    results: dict[str, dict[str, float]] = {}

    for label in labels:
        tp = sum(1 for a, b in zip(y_true, y_pred) if a == label and b == label)
        fp = sum(1 for a, b in zip(y_true, y_pred) if a != label and b == label)
        fn = sum(1 for a, b in zip(y_true, y_pred) if a == label and b != label)
        support = sum(1 for a in y_true if a == label)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        results[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "support": support,
        }

    return results


def macro_f1(y_true: list[str], y_pred: list[str]) -> float:
    """Oblicza makro-średnie F1 (równe wagi dla każdej etykiety).

    Args:
        y_true: lista oczekiwanych etykiet.
        y_pred: lista przewidywanych etykiet.

    Returns:
        Wartość macro F1 w przedziale [0.0, 1.0].
    """
    prf = precision_recall_f1_per_label(y_true, y_pred)
    if not prf:
        return 0.0
    # Uwzględnij tylko etykiety, które faktycznie wystąpiły w y_true
    true_labels = {label for label in prf if prf[label]["support"] > 0}
    if not true_labels:
        return 0.0
    return round(
        sum(prf[label]["f1_score"] for label in true_labels) / len(true_labels),
        4,
    )


def weighted_f1(y_true: list[str], y_pred: list[str]) -> float:
    """Oblicza ważone F1 (wagi proporcjonalne do liczby próbek danej etykiety).

    Args:
        y_true: lista oczekiwanych etykiet.
        y_pred: lista przewidywanych etykiet.

    Returns:
        Wartość weighted F1 w przedziale [0.0, 1.0].
    """
    prf = precision_recall_f1_per_label(y_true, y_pred)
    total = len(y_true)
    if total == 0:
        return 0.0
    return round(
        sum(v["f1_score"] * v["support"] for v in prf.values()) / total,
        4,
    )


def confusion_matrix_as_dict(
    y_true: list[str],
    y_pred: list[str],
    labels: list[str],
) -> dict[str, dict[str, int]]:
    """Zwraca macierz pomyłek jako zagnieżdżony słownik.

    Klucz zewnętrzny to etykieta oczekiwana (true), wewnętrzny — przewidywana (pred).

    Args:
        y_true: lista oczekiwanych etykiet.
        y_pred: lista przewidywanych etykiet.
        labels: lista etykiet do uwzględnienia.

    Returns:
        Słownik {true_label: {pred_label: count}}.
    """
    matrix: dict[str, dict[str, int]] = {
        true_label: {pred_label: 0 for pred_label in labels}
        for true_label in labels
    }

    for true, pred in zip(y_true, y_pred):
        if true in matrix:
            if pred in matrix[true]:
                matrix[true][pred] += 1
            # Jeśli przewidziana etykieta nie jest na liście — ignoruj

    return matrix


def classification_report_as_dict(
    y_true: list[str],
    y_pred: list[str],
    labels: list[str],
) -> list[dict]:
    """Zwraca raport klasyfikacji jako listę słowników.

    Args:
        y_true: lista oczekiwanych etykiet.
        y_pred: lista przewidywanych etykiet.
        labels: lista etykiet do uwzględnienia (w kolejności wyświetlania).

    Returns:
        Lista słowników {label, precision, recall, f1_score, support}.
    """
    prf = precision_recall_f1_per_label(y_true, y_pred)
    report = []

    for label in labels:
        if label in prf:
            row = {"label": label, **prf[label]}
        else:
            row = {
                "label": label,
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "support": 0,
            }
        report.append(row)

    return report
