"""
run_evaluation.py — skrypt uruchamiający ewaluację pipeline'u analizy zgłoszeń.

Użycie:
    cd backend
    python scripts/run_evaluation.py

Opcjonalne argumenty:
    --input  ścieżka do pliku CSV z danymi testowymi
    --output katalog docelowy dla raportów

Domyślne ścieżki:
    --input  ../../data/test_cases/evaluation_tickets.csv
    --output ../../reports/evaluation
"""

from __future__ import annotations

import argparse
import os
import sys

# Dodaj katalog backendu do sys.path, aby działały importy app.*
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_SCRIPT_DIR)
 
sys.path.insert(0, _BACKEND_DIR)

from app.evaluation.evaluator import EvaluationRunner


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ewaluacja pipeline'u analizy zgłoszeń helpdesk."
    )
    parser.add_argument(
        "--input",
        default=os.path.join(_BACKEND_DIR, "..", "data", "test_cases", "evaluation_tickets.csv"),
        help="Ścieżka do pliku CSV lub JSON z danymi testowymi.",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(_BACKEND_DIR, "..", "reports", "evaluation"),
        help="Katalog docelowy dla raportów.",
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
        parser.add_argument(
            "--mode",
            choices=["mock", "rag", "openai_rag"],
            default="rag",
            help="Tryb ewaluacji: mock, rag lub openai_rag.",
        )
        parser.add_argument(
            "--allow-openai",
            action="store_true",
            help="Jawnie zezwala na użycie OpenAI w trybie openai_rag.",
        )
    output_dir = os.path.abspath(args.output)

    if not os.path.exists(input_path):
        print(f"[BŁĄD] Nie znaleziono pliku wejściowego: {input_path}")
        sys.exit(1)

    print("=" * 60)
    print("  Ewaluacja modułu analizy zgłoszeń — Helpdesk AI Service")
    print("=" * 60)
    print(f"  Plik wejściowy : {input_path}")
    print(f"  Katalog wyjścia: {output_dir}")
    print()

    runner = EvaluationRunner()
    result = runner.run(input_path=input_path, output_dir=output_dir)

    print(f"  Liczba przypadków testowych: {result.total_cases}")
    print()
    print("  Klasyfikacja kategorii:")
    print(f"    Accuracy      : {result.classification_accuracy:.2%}")
    print(f"    Macro F1      : {result.classification_macro_f1:.4f}")
    print(f"    Weighted F1   : {result.classification_weighted_f1:.4f}")
    print()
    print("  Priorytetyzacja:")
    print(f"    Accuracy      : {result.priority_accuracy:.2%}")
    print(f"    Macro F1      : {result.priority_macro_f1:.4f}")
    print(f"    Weighted F1   : {result.priority_weighted_f1:.4f}")
    print()
    print("  Jakość odpowiedzi:")
    print(f"    Śr. ocena (0-5): {result.average_answer_quality_score:.2f}")
    print(f"    Śr. długość    : {result.average_response_length:.0f} znaków")
    print()
    print("  Wygenerowane raporty:")
    print(f"    {os.path.join(output_dir, 'evaluation_summary.json')}")
    print(f"    {os.path.join(output_dir, 'evaluation_results.csv')}")
    print(f"    {os.path.join(output_dir, 'evaluation_report.md')}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
