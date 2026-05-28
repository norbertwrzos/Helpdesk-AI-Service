# Raporty ewaluacji

Ten katalog zawiera wyniki ewaluacji modułu analizy zgłoszeń.

## Generowane pliki

Pliki są generowane przez skrypt `backend/scripts/run_evaluation.py`.

| Plik | Format | Opis |
|------|--------|------|
| `evaluation_summary.json` | JSON | Metryki zbiorcze i macierze pomyłek |
| `evaluation_results.csv` | CSV | Wyniki dla każdego zgłoszenia |
| `evaluation_report.md` | Markdown | Raport po polsku do pracy inżynierskiej |

## Jak uruchomić ewaluację

```bash
cd backend
source .venv/bin/activate
python scripts/run_evaluation.py
```

## Uwagi

- Pliki raportów nie są śledzone przez Git (`.gitignore`).
- Plik `.gitkeep` utrzymuje katalog w repozytorium.
- Raporty można regenerować w dowolnym momencie.
