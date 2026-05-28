"""
export_test_report.py — kopiuje najnowszy raport ewaluacji do docs/testing/.

Użycie:
    cd backend
    python scripts/export_test_report.py

Skrypt kopiuje plik reports/evaluation/evaluation_report.md
do docs/testing/latest_evaluation_report.md.
"""

from __future__ import annotations

import os
import shutil
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.dirname(_SCRIPT_DIR)
_REPO_ROOT = os.path.dirname(_BACKEND_DIR)

SOURCE = os.path.join(_REPO_ROOT, "reports", "evaluation", "evaluation_report.md")
DEST_DIR = os.path.join(_REPO_ROOT, "docs", "testing")
DEST = os.path.join(DEST_DIR, "latest_evaluation_report.md")


def main() -> None:
    if not os.path.exists(SOURCE):
        print(f"[BŁĄD] Raport źródłowy nie istnieje: {SOURCE}")
        print("  Uruchom najpierw: python scripts/run_evaluation.py")
        sys.exit(1)

    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copy2(SOURCE, DEST)
    print(f"[OK] Skopiowano raport:")
    print(f"     {SOURCE}")
    print(f"  -> {DEST}")


if __name__ == "__main__":
    main()
