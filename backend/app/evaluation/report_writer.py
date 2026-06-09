from __future__ import annotations

import csv
import json
import os
from datetime import datetime

from app.evaluation.evaluator import CaseResult, EvaluationResult


class ReportWriter:
    def write_all(self, result: EvaluationResult, output_dir: str) -> dict[str, str]:
        os.makedirs(output_dir, exist_ok=True)
        return {
            "json": self.write_json(result, output_dir),
            "csv": self.write_csv(result, output_dir),
            "markdown": self.write_markdown(result, output_dir),
        }

    def write_json(self, result: EvaluationResult, output_dir: str) -> str:
        path = os.path.join(output_dir, "evaluation_summary.json")
        summary = {
            "generated_at": result.generated_at,
            "mode": result.mode,
            "total_cases": result.total_cases,
            "classification_accuracy": result.classification_accuracy,
            "classification_macro_f1": result.classification_macro_f1,
            "classification_weighted_f1": result.classification_weighted_f1,
            "priority_accuracy": result.priority_accuracy,
            "priority_macro_f1": result.priority_macro_f1,
            "priority_weighted_f1": result.priority_weighted_f1,
            "average_answer_quality_score": round(result.average_answer_quality_score, 4),
            "average_mail_format_score": round(result.average_mail_format_score, 4),
            "average_response_length": round(result.average_response_length, 1),
            "retrieval_hit_at_1": round(result.retrieval_hit_at_1, 4),
            "retrieval_hit_at_3": round(result.retrieval_hit_at_3, 4),
            "retrieval_hit_at_5": round(result.retrieval_hit_at_5, 4),
            "retrieval_mrr": round(result.retrieval_mrr, 4),
            "average_retrieval_score": round(result.average_retrieval_score, 4),
            "average_retrieval_keyword_coverage": round(result.average_retrieval_keyword_coverage, 4),
            "provider_mode": result.provider_mode,
            "openai_used": result.openai_used,
            "limitations": result.limitations,
            "classification_report": result.classification_report,
            "priority_report": result.priority_report,
            "classification_confusion_matrix": result.classification_confusion_matrix,
            "priority_confusion_matrix": result.priority_confusion_matrix,
            "case_results": [
                {
                    "id": case.id,
                    "title": case.title,
                    "expected_category": case.expected_category,
                    "predicted_category": case.predicted_category,
                    "category_correct": case.category_correct,
                    "expected_priority": case.expected_priority,
                    "predicted_priority": case.predicted_priority,
                    "priority_correct": case.priority_correct,
                    "expected_article_keywords": case.expected_article_keywords,
                    "expected_answer_format": case.expected_answer_format,
                    "expected_rag_category": case.expected_rag_category,
                    "retrieved_article_ids": case.retrieved_article_ids,
                    "retrieved_article_titles": case.retrieved_article_titles,
                    "retrieval_hit_at_1": round(case.retrieval_hit_at_1, 4),
                    "retrieval_hit_at_3": round(case.retrieval_hit_at_3, 4),
                    "retrieval_hit_at_5": round(case.retrieval_hit_at_5, 4),
                    "retrieval_mrr": round(case.retrieval_mrr, 4),
                    "retrieval_average_score": round(case.retrieval_average_score, 4),
                    "retrieval_keyword_coverage": round(case.retrieval_keyword_coverage, 4),
                    "generated_answer": case.generated_answer,
                    "answer_quality_score": case.answer_quality_score,
                    "answer_quality_notes": case.answer_quality_notes,
                    "mail_format_score": case.mail_format_score,
                    "mail_format_notes": case.mail_format_notes,
                    "matched_keywords": case.matched_keywords,
                    "missing_keywords": case.missing_keywords,
                    "provider_name": case.provider_name,
                    "model_name": case.model_name,
                }
                for case in result.case_results
            ],
        }
        with open(path, "w", encoding="utf-8") as file_handle:
            json.dump(summary, file_handle, ensure_ascii=False, indent=2)
        return path

    def write_csv(self, result: EvaluationResult, output_dir: str) -> str:
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
            "retrieved_article_ids",
            "retrieved_article_titles",
            "retrieval_hit_at_1",
            "retrieval_hit_at_3",
            "retrieval_hit_at_5",
            "retrieval_mrr",
            "retrieval_average_score",
            "retrieval_keyword_coverage",
            "generated_answer",
            "answer_quality_score",
            "mail_format_score",
            "provider_name",
            "model_name",
            "answer_quality_notes",
            "mail_format_notes",
        ]

        with open(path, "w", encoding="utf-8", newline="") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
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
                        "retrieved_article_ids": " | ".join(str(article_id) for article_id in case.retrieved_article_ids),
                        "retrieved_article_titles": " | ".join(case.retrieved_article_titles),
                        "retrieval_hit_at_1": f"{case.retrieval_hit_at_1:.4f}",
                        "retrieval_hit_at_3": f"{case.retrieval_hit_at_3:.4f}",
                        "retrieval_hit_at_5": f"{case.retrieval_hit_at_5:.4f}",
                        "retrieval_mrr": f"{case.retrieval_mrr:.4f}",
                        "retrieval_average_score": f"{case.retrieval_average_score:.4f}",
                        "retrieval_keyword_coverage": f"{case.retrieval_keyword_coverage:.4f}",
                        "generated_answer": case.generated_answer,
                        "answer_quality_score": case.answer_quality_score,
                        "mail_format_score": case.mail_format_score,
                        "provider_name": case.provider_name,
                        "model_name": case.model_name,
                        "answer_quality_notes": case.answer_quality_notes,
                        "mail_format_notes": case.mail_format_notes,
                    }
                )

        return path

    def write_markdown(self, result: EvaluationResult, output_dir: str) -> str:
        path = os.path.join(output_dir, "evaluation_report.md")

        generated_at = _format_generated_at(result.generated_at)
        classification_table = _format_metrics_table(result.classification_report)
        priority_table = _format_metrics_table(result.priority_report)
        case_table = _format_case_table(result.case_results)
        good_cases = _select_good_cases(result.case_results, result.provider_mode)
        bad_cases = _select_bad_cases(result.case_results, result.provider_mode)

        lines = [
            "# AI Etap 12 — Raport ewaluacji RAG i jakości odpowiedzi mailowej",
            "",
            f"**Data wygenerowania:** {generated_at}",
            f"**Liczba przypadków testowych:** {result.total_cases}",
            f"**Tryb providera:** {result.provider_mode}",
            f"**OpenAI użyte:** {'tak' if result.openai_used else 'nie'}",
            "",
            "## 1. Cel ewaluacji RAG",
            "",
            "Celem ewaluacji było rozszerzenie dotychczasowego offline evaluation o ocenę retrievalu artykułów bazy wiedzy, obecności oczekiwanych słów kluczowych w wygenerowanych odpowiedziach, zgodności odpowiedzi z formatem mailowym oraz wpływu trybu uruchomienia providera na końcowy wynik jakościowy.",
            "",
            "## 2. Opis danych testowych",
            "",
            "Zbiór testowy zawiera syntetyczne zgłoszenia helpdesk z etykietami referencyjnymi dla kategorii, priorytetu oraz oczekiwanych słów kluczowych rozwiązania. W etapie 12 dane zostały rozszerzone o oczekiwane słowa kluczowe artykułów RAG, oczekiwany format odpowiedzi (`mail`) oraz opcjonalną kategorię retrievalu.",
            "",
            "## 3. Opis metryk klasyfikacji",
            "",
            "Dla klasyfikacji kategorii raportowane są Accuracy, Macro F1 i Weighted F1. Pozwala to osobno ocenić ogólną trafność reguł oraz odporność metryk na nierówny rozkład klas.",
            "",
            "| Metryka | Wartość |",
            "|---|---|",
            f"| Accuracy | {result.classification_accuracy:.2%} |",
            f"| Macro F1 | {result.classification_macro_f1:.4f} |",
            f"| Weighted F1 | {result.classification_weighted_f1:.4f} |",
            "",
            classification_table,
            "",
            "## 4. Opis metryk priorytetyzacji",
            "",
            "Priorytetyzacja jest oceniana analogicznie jak klasyfikacja kategorii. Accuracy pokazuje udział poprawnych decyzji, a metryki F1 lepiej ujawniają przypadki mylenia zgłoszeń niskiego, wysokiego i krytycznego priorytetu.",
            "",
            "| Metryka | Wartość |",
            "|---|---|",
            f"| Accuracy | {result.priority_accuracy:.2%} |",
            f"| Macro F1 | {result.priority_macro_f1:.4f} |",
            f"| Weighted F1 | {result.priority_weighted_f1:.4f} |",
            "",
            priority_table,
            "",
            "## 5. Opis metryk retrievalu",
            "",
            "Metryki retrievalu obejmują hit@k, MRR, średni score retrievalu oraz coverage oczekiwanych słów kluczowych źródeł. Hit@k sprawdza, czy w top-k artykułach pojawia się co najmniej jedno oczekiwane słowo kluczowe. MRR premiuje trafienie wysoko na liście wyników. Coverage mierzy, jaki odsetek oczekiwanych słów kluczowych wystąpił w zwróconych artykułach.",
            "",
            "| Metryka | Wartość |",
            "|---|---|",
            f"| hit@1 | {result.retrieval_hit_at_1:.4f} |",
            f"| hit@3 | {result.retrieval_hit_at_3:.4f} |",
            f"| hit@5 | {result.retrieval_hit_at_5:.4f} |",
            f"| MRR | {result.retrieval_mrr:.4f} |",
            f"| Średni score retrievalu | {result.average_retrieval_score:.4f} |",
            f"| Średnie coverage słów kluczowych | {result.average_retrieval_keyword_coverage:.4f} |",
            "",
            "## 6. Opis metryk odpowiedzi mailowej",
            "",
            "Jakość odpowiedzi mailowej jest oceniana przez heurystyki wykrywające powitanie, zakończenie, podpis agenta, obecność kroków do wykonania oraz oczekiwanych słów kluczowych w treści odpowiedzi. `mail_format_score` mieści się w przedziale 0-5.",
            "",
            "| Metryka | Wartość |",
            "|---|---|",
            f"| Średnia ocena jakości odpowiedzi | {result.average_answer_quality_score:.4f} |",
            f"| Średni mail_format_score | {result.average_mail_format_score:.4f} |",
            f"| Średnia długość odpowiedzi | {result.average_response_length:.1f} |",
            "",
            "## 7. Wyniki tabelaryczne",
            "",
            case_table,
            "",
            "## 8. Przykładowe poprawne przypadki",
            "",
        ]

        if good_cases:
            lines.extend(_format_examples(good_cases))
        else:
            lines.append("Brak przypadków spełniających jednocześnie kryteria poprawnej klasyfikacji, priorytetyzacji oraz jakości odpowiedzi dla aktualnego trybu.")

        lines.extend([
            "",
            "## 9. Przykładowe błędne przypadki",
            "",
        ])

        if bad_cases:
            lines.extend(_format_examples(bad_cases))
        else:
            lines.append("Brak wyraźnie błędnych przypadków według zdefiniowanych heurystyk ewaluacyjnych.")

        lines.extend([
            "",
            "## 10. Ograniczenia",
            "",
        ])
        for index, limitation in enumerate(result.limitations, start=1):
            lines.append(f"{index}. {limitation}")

        lines.extend([
            "",
            "## 11. Wnioski do pracy inżynierskiej",
            "",
            f"Uruchomienie ewaluacji w trybie `{result.provider_mode}` pozwala wyznaczyć punkt odniesienia dla wpływu retrievalu RAG oraz providera generacji na jakość odpowiedzi helpdesk. W aktualnym przebiegu średni hit@3 wyniósł {result.retrieval_hit_at_3:.4f}, średni MRR {result.retrieval_mrr:.4f}, a średni `mail_format_score` {result.average_mail_format_score:.4f}.",
            "Otrzymane wyniki mogą zostać wykorzystane w rozdziale testowym pracy do porównania baseline'u mock z wariantem RAG oraz z wariantem `openai_rag`, jeśli został uruchomiony z jawną zgodą na użycie API. Raport umożliwia osobne omówienie trafności klasyfikacji, priorytetyzacji, retrievalu oraz jakości odpowiedzi końcowej.",
            "",
            "Raport został wygenerowany automatycznie przez `backend/scripts/run_evaluation.py`.",
        ])

        with open(path, "w", encoding="utf-8") as file_handle:
            file_handle.write("\n".join(lines))

        return path


def _format_generated_at(value: str) -> str:
    try:
        dt_value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt_value.strftime("%d.%m.%Y %H:%M UTC")
    except (ValueError, AttributeError):
        return value


def _format_metrics_table(report: list[dict]) -> str:
    lines = [
        "| Etykieta | Precision | Recall | F1-score | Support |",
        "|---|---|---|---|---|",
    ]
    for row in report:
        lines.append(
            f"| {row['label']} | {row['precision']:.4f} | {row['recall']:.4f} | {row['f1_score']:.4f} | {row['support']} |"
        )
    return "\n".join(lines)


def _format_case_table(case_results: list[CaseResult]) -> str:
    lines = [
        "| ID | Kategoria | Priorytet | hit@3 | coverage | mail_format_score | Provider |",
        "|---|---|---|---|---|---|---|",
    ]
    for case in case_results:
        lines.append(
            f"| {case.id} | {'tak' if case.category_correct else 'nie'} | {'tak' if case.priority_correct else 'nie'} | {case.retrieval_hit_at_3:.2f} | {case.retrieval_keyword_coverage:.2f} | {case.mail_format_score} | {case.provider_name}/{case.model_name} |"
        )
    return "\n".join(lines)


def _score_total(case: CaseResult) -> float:
    return case.answer_quality_score + case.mail_format_score + case.retrieval_hit_at_3


def _select_good_cases(case_results: list[CaseResult], provider_mode: str) -> list[CaseResult]:
    candidates = []
    for case in case_results:
        retrieval_ok = True if provider_mode == "mock" else case.retrieval_hit_at_3 >= 1.0
        if case.category_correct and case.priority_correct and retrieval_ok and case.mail_format_score >= 4:
            candidates.append(case)
    return sorted(candidates, key=_score_total, reverse=True)[:5]


def _select_bad_cases(case_results: list[CaseResult], provider_mode: str) -> list[CaseResult]:
    candidates = [
        case
        for case in case_results
        if not case.category_correct
        or not case.priority_correct
        or case.mail_format_score <= 3
        or (provider_mode != "mock" and case.retrieval_hit_at_3 == 0.0)
    ]
    return sorted(candidates, key=_score_total)[:5]


def _format_examples(cases: list[CaseResult]) -> list[str]:
    lines: list[str] = []
    for case in cases:
        lines.extend(
            [
                f"### {case.id} — {case.title}",
                "",
                f"- Klasyfikacja: oczekiwano `{case.expected_category}`, otrzymano `{case.predicted_category}`.",
                f"- Priorytet: oczekiwano `{case.expected_priority}`, otrzymano `{case.predicted_priority}`.",
                f"- Retrieval: hit@3={case.retrieval_hit_at_3:.2f}, coverage={case.retrieval_keyword_coverage:.2f}, źródła={', '.join(case.retrieved_article_titles) or 'brak'}.",
                f"- Odpowiedź: answer_quality_score={case.answer_quality_score}, mail_format_score={case.mail_format_score}, provider={case.provider_name}/{case.model_name}.",
                f"- Uwagi: {(case.answer_quality_notes + ' ' + case.mail_format_notes).strip()}",
                "",
            ]
        )
    return lines