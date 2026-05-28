"""
report_writer.py — zapis wyników ewaluacji do plików JSON, CSV i Markdown.

Generowane pliki:
- evaluation_summary.json — metryki zbiorcze i macierze pomyłek
- evaluation_results.csv  — wyniki dla każdego zgłoszenia
- evaluation_report.md    — raport po polsku do pracy inżynierskiej
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime

from app.evaluation.evaluator import EvaluationResult


class ReportWriter:
    """Zapisuje wyniki ewaluacji w formatach JSON, CSV i Markdown."""

    def write_all(self, result: EvaluationResult, output_dir: str) -> dict[str, str]:
        """Zapisuje wszystkie raporty do katalogu output_dir.

        Args:
            result: wynik ewaluacji z EvaluationRunner.
            output_dir: katalog docelowy.

        Returns:
            Słownik {typ: ścieżka} dla zapisanych plików.
        """
        os.makedirs(output_dir, exist_ok=True)

        paths = {
            "json": self.write_json(result, output_dir),
            "csv": self.write_csv(result, output_dir),
            "markdown": self.write_markdown(result, output_dir),
        }
        return paths

    def write_json(self, result: EvaluationResult, output_dir: str) -> str:
        """Zapisuje podsumowanie ewaluacji w formacie JSON."""
        path = os.path.join(output_dir, "evaluation_summary.json")

        summary = {
            "generated_at": result.generated_at,
            "total_cases": result.total_cases,
            "classification_accuracy": result.classification_accuracy,
            "classification_macro_f1": result.classification_macro_f1,
            "classification_weighted_f1": result.classification_weighted_f1,
            "priority_accuracy": result.priority_accuracy,
            "priority_macro_f1": result.priority_macro_f1,
            "priority_weighted_f1": result.priority_weighted_f1,
            "average_answer_quality_score": round(result.average_answer_quality_score, 4),
            "average_response_length": round(result.average_response_length, 1),
            "classification_report": result.classification_report,
            "priority_report": result.priority_report,
            "classification_confusion_matrix": result.classification_confusion_matrix,
            "priority_confusion_matrix": result.priority_confusion_matrix,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        return path

    def write_csv(self, result: EvaluationResult, output_dir: str) -> str:
        """Zapisuje wyniki dla każdego zgłoszenia w formacie CSV."""
        path = os.path.join(output_dir, "evaluation_results.csv")

        fieldnames = [
            "id",
            "title",
            "expected_category",
            "predicted_category",
            "category_correct",
            "expected_priority",
            "predicted_priority",
            "priority_correct",
            "answer_quality_score",
            "answer_quality_notes",
        ]

        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for case in result.case_results:
                writer.writerow(
                    {
                        "id": case.id,
                        "title": case.title,
                        "expected_category": case.expected_category,
                        "predicted_category": case.predicted_category,
                        "category_correct": case.category_correct,
                        "expected_priority": case.expected_priority,
                        "predicted_priority": case.predicted_priority,
                        "priority_correct": case.priority_correct,
                        "answer_quality_score": case.answer_quality_score,
                        "answer_quality_notes": case.answer_quality_notes,
                    }
                )

        return path

    def write_markdown(self, result: EvaluationResult, output_dir: str) -> str:
        """Zapisuje raport ewaluacji w formacie Markdown (po polsku)."""
        path = os.path.join(output_dir, "evaluation_report.md")

        correct_cat = sum(1 for c in result.case_results if c.category_correct)
        correct_pri = sum(1 for c in result.case_results if c.priority_correct)
        total = result.total_cases

        # Najczęstsze błędy klasyfikacji
        category_errors: list[tuple[str, str]] = [
            (c.expected_category, c.predicted_category)
            for c in result.case_results
            if not c.category_correct
        ]
        priority_errors: list[tuple[str, str]] = [
            (c.expected_priority, c.predicted_priority)
            for c in result.case_results
            if not c.priority_correct
        ]

        # Agreguj błędy
        cat_error_counts: dict[str, int] = {}
        for expected, predicted in category_errors:
            key = f"{expected} → {predicted}"
            cat_error_counts[key] = cat_error_counts.get(key, 0) + 1

        pri_error_counts: dict[str, int] = {}
        for expected, predicted in priority_errors:
            key = f"{expected} → {predicted}"
            pri_error_counts[key] = pri_error_counts.get(key, 0) + 1

        top_cat_errors = sorted(cat_error_counts.items(), key=lambda x: -x[1])[:5]
        top_pri_errors = sorted(pri_error_counts.items(), key=lambda x: -x[1])[:5]

        # Raport klasyfikacji kategorii
        cat_table = _format_metrics_table(result.classification_report)
        pri_table = _format_metrics_table(result.priority_report)

        # Data generowania
        try:
            gen_dt = datetime.fromisoformat(result.generated_at.replace("Z", "+00:00"))
            gen_date = gen_dt.strftime("%d.%m.%Y %H:%M UTC")
        except (ValueError, AttributeError):
            gen_date = result.generated_at

        lines = [
            "# Raport ewaluacji modułu analizy zgłoszeń",
            "",
            f"**Data wygenerowania:** {gen_date}  ",
            f"**Liczba przypadków testowych:** {total}  ",
            f"**Wersja pipeline'u:** mock/rule-based (etap 6)",
            "",
            "---",
            "",
            "## 1. Metodyka testów",
            "",
            "Ewaluacja przeprowadzona na syntetycznym zbiorze zgłoszeń (`evaluation_tickets.csv`).",
            "Każde zgłoszenie zawiera etykiety referencyjne (`expected_category`, `expected_priority`),",
            "które zostały przypisane ręcznie przez autora systemu na podstawie treści zgłoszenia.",
            "",
            "Dla każdego zgłoszenia uruchomiono:",
            "- `ClassificationService` — klasyfikacja kategorii na podstawie reguł słów kluczowych,",
            "- `PriorityAnalysisService` — priorytetyzacja na podstawie reguł słów kluczowych,",
            "- `MockAIGenerator` — generowanie odpowiedzi na podstawie szablonu.",
            "",
            "Usługi uruchomiono bezpośrednio (bez zapisu do bazy danych).",
            "Kategorie i priorytety wczytano z plików seed (`data/seed/`).",
            "",
            "---",
            "",
            "## 2. Wyniki klasyfikacji kategorii",
            "",
            f"| Metryka | Wartość |",
            f"|---------|---------|",
            f"| Accuracy | **{result.classification_accuracy:.2%}** ({correct_cat}/{total}) |",
            f"| Macro F1 | **{result.classification_macro_f1:.4f}** |",
            f"| Weighted F1 | **{result.classification_weighted_f1:.4f}** |",
            "",
            "### Szczegółowe metryki per kategoria",
            "",
            cat_table,
            "",
            "---",
            "",
            "## 3. Wyniki priorytetyzacji",
            "",
            f"| Metryka | Wartość |",
            f"|---------|---------|",
            f"| Accuracy | **{result.priority_accuracy:.2%}** ({correct_pri}/{total}) |",
            f"| Macro F1 | **{result.priority_macro_f1:.4f}** |",
            f"| Weighted F1 | **{result.priority_weighted_f1:.4f}** |",
            "",
            "### Szczegółowe metryki per priorytet",
            "",
            pri_table,
            "",
            "---",
            "",
            "## 4. Ocena jakości generowanych odpowiedzi",
            "",
            f"| Metryka | Wartość |",
            f"|---------|---------|",
            f"| Średnia ocena jakości (0–5) | **{result.average_answer_quality_score:.2f}** |",
            f"| Średnia długość odpowiedzi (znaki) | **{result.average_response_length:.0f}** |",
            "",
            "Ocena jakości odpowiedzi opiera się na 5 kryteriach heurystycznych:",
            "1. Odpowiedź nie jest pusta (+1 pkt),",
            "2. Zawiera co najmniej jedno oczekiwane słowo kluczowe (+1 pkt),",
            "3. Zawiera co najmniej połowę oczekiwanych słów kluczowych (+1 pkt),",
            "4. Zawiera sugestię diagnostyczną lub kroki rozwiązania (+1 pkt),",
            "5. Zawiera informację o weryfikacji przez IT Support (+1 pkt).",
            "",
            "---",
            "",
            "## 5. Najczęstsze błędy klasyfikacji",
            "",
        ]

        if top_cat_errors:
            lines.append("### Błędy kategorii (oczekiwana → przewidziana)")
            lines.append("")
            lines.append("| Błąd klasyfikacji | Liczba |")
            lines.append("|-------------------|--------|")
            for err, count in top_cat_errors:
                lines.append(f"| {err} | {count} |")
        else:
            lines.append("Brak błędów klasyfikacji kategorii.")

        lines += [
            "",
            "### Błędy priorytetu (oczekiwany → przewidziany)",
            "",
        ]

        if top_pri_errors:
            lines.append("| Błąd priorytetu | Liczba |")
            lines.append("|-----------------|--------|")
            for err, count in top_pri_errors:
                lines.append(f"| {err} | {count} |")
        else:
            lines.append("Brak błędów priorytetyzacji.")

        lines += [
            "",
            "---",
            "",
            "## 6. Ograniczenia ewaluacji",
            "",
            "1. **Dane syntetyczne** — zbiór testowy został wygenerowany ręcznie przez autora.",
            "   Może nie odzwierciedlać pełnej różnorodności rzeczywistych zgłoszeń.",
            "2. **Pipeline rule-based** — klasyfikacja opiera się na słowach kluczowych,",
            "   a nie na prawdziwym modelu ML/NLP. Wyniki nie są reprezentatywne",
            "   dla metod uczenia maszynowego.",
            "3. **Ocena odpowiedzi heurystyczna** — jakość odpowiedzi oceniana jest",
            "   na podstawie prostych reguł, a nie przez eksperta dziedzinowego.",
            "4. **Brak cross-walidacji** — ewaluacja przeprowadzona jednorazowo",
            "   na całym zbiorze testowym.",
            "5. **Brak danych produkcyjnych** — wyniki odnoszą się wyłącznie",
            "   do prototypowego etapu systemu.",
            "",
            "---",
            "",
            "## 7. Wnioski do pracy inżynierskiej",
            "",
            "Przeprowadzona ewaluacja prototypowego pipeline'u rule-based pozwala na:",
            "",
            f"- Określenie **bazowych metryk** przed wdrożeniem właściwych modeli AI/NLP.",
            f"  Accuracy klasyfikacji kategorii: **{result.classification_accuracy:.2%}**,",
            f"  accuracy priorytetyzacji: **{result.priority_accuracy:.2%}**.",
            "- Identyfikację **słabych punktów** systemu rule-based —",
            "  najczęstsze błędy wynikają z nakładania się słów kluczowych",
            "  między kategoriami (np. Konto i dostęp vs Aplikacje biznesowe).",
            "- Zdefiniowanie **punktu odniesienia** (baseline) dla przyszłego porównania",
            "  z modelami opartymi na embeddingach lub fine-tunowanych modelach językowych.",
            "- Weryfikację, że **MockAIGenerator** generuje odpowiedzi zawierające",
            "  kroki diagnostyczne i odwołanie do IT Support, co jest poprawną",
            "  charakterystyką odpowiedzi helpdesk.",
            "",
            "Wyniki ewaluacji zostaną przedstawione w rozdziale",
            "\"Testowanie systemu\" pracy inżynierskiej jako porównanie",
            "podejścia rule-based z podejściem AI/NLP (etap 7+).",
            "",
            "---",
            "",
            "*Raport wygenerowany automatycznie przez skrypt `backend/scripts/run_evaluation.py`.*",
            "",
        ]

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return path


def _format_metrics_table(report: list[dict]) -> str:
    """Formatuje raport klasyfikacji jako tabelę Markdown."""
    lines = [
        "| Etykieta | Precision | Recall | F1-score | Support |",
        "|----------|-----------|--------|----------|---------|",
    ]
    for row in report:
        lines.append(
            f"| {row['label']} "
            f"| {row['precision']:.4f} "
            f"| {row['recall']:.4f} "
            f"| {row['f1_score']:.4f} "
            f"| {row['support']} |"
        )
    return "\n".join(lines)
