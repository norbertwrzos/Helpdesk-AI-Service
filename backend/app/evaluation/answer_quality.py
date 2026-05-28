"""
answer_quality.py — heurystyczna ocena jakości odpowiedzi generowanych przez AI.

Ponieważ odpowiedzi są generowane przez MockAIGenerator (rule-based),
ocena jest oparta na prostych kryteriach eksperckich:
1. Odpowiedź nie jest pusta.
2. Zawiera co najmniej jedno słowo kluczowe z expected_solution_keywords.
3. Zawiera co najmniej połowę oczekiwanych słów kluczowych.
4. Zawiera sugestię diagnostyczną lub opis kroków rozwiązania.
5. Zawiera informację o weryfikacji przez IT Support.
"""

from __future__ import annotations

# Wskaźniki sugestii diagnostycznych (min. jeden musi być w odpowiedzi)
_DIAGNOSTIC_INDICATORS = [
    "sprawdź",
    "zrestartuj",
    "uruchom",
    "zweryfikuj",
    "skontaktuj",
    "zalecane kroki",
    "kroki diagnostyczne",
    "zaleca się",
    "należy",
    "upewnij się",
]

# Wskaźniki weryfikacji przez IT Support
_IT_SUPPORT_INDICATORS = [
    "it support",
    "pracownik it",
    "dział it",
    "zweryfikowana przez",
    "powinna zostać zweryfikowana",
    "pracownika it",
    "działu it",
]


def evaluate_answer_quality(
    generated_answer: str,
    expected_keywords: list[str],
) -> dict:
    """Ocenia jakość wygenerowanej odpowiedzi na podstawie heurystyki.

    Punktacja (0–5):
    - 1 pkt: odpowiedź nie jest pusta,
    - 1 pkt: zawiera co najmniej jedno oczekiwane słowo kluczowe,
    - 1 pkt: zawiera co najmniej połowę oczekiwanych słów kluczowych,
    - 1 pkt: zawiera sugestię diagnostyczną lub opis kroków,
    - 1 pkt: zawiera informację o weryfikacji przez IT Support.

    Args:
        generated_answer: tekst odpowiedzi wygenerowany przez system.
        expected_keywords: lista oczekiwanych słów/fraz kluczowych.

    Returns:
        Słownik z kluczami:
        - score (int 0–5),
        - matched_keywords (list[str]),
        - missing_keywords (list[str]),
        - notes (str).
    """
    score = 0
    notes_parts: list[str] = []

    # Kryterium 1: odpowiedź nie jest pusta
    if not generated_answer or not generated_answer.strip():
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": list(expected_keywords),
            "notes": "Pusta odpowiedź — brak jakiejkolwiek treści.",
        }

    score += 1
    answer_lower = generated_answer.lower()

    # Kryterium 2 i 3: słowa kluczowe
    matched: list[str] = []
    missing: list[str] = []
    for kw in expected_keywords:
        if kw.lower() in answer_lower:
            matched.append(kw)
        else:
            missing.append(kw)

    if matched:
        score += 1  # co najmniej jedno słowo kluczowe
        notes_parts.append(f"Dopasowano {len(matched)}/{len(expected_keywords)} słów kluczowych.")
    else:
        notes_parts.append("Brak dopasowania słów kluczowych.")

    if expected_keywords and len(matched) >= len(expected_keywords) / 2:
        score += 1  # co najmniej połowa słów kluczowych
        notes_parts.append("Odpowiedź pokrywa co najmniej połowę oczekiwanych słów kluczowych.")

    # Kryterium 4: sugestia diagnostyczna
    if any(indicator in answer_lower for indicator in _DIAGNOSTIC_INDICATORS):
        score += 1
        notes_parts.append("Odpowiedź zawiera sugestię diagnostyczną lub kroki rozwiązania.")
    else:
        notes_parts.append("Brak wyraźnej sugestii diagnostycznej.")

    # Kryterium 5: informacja o weryfikacji przez IT Support
    if any(indicator in answer_lower for indicator in _IT_SUPPORT_INDICATORS):
        score += 1
        notes_parts.append("Odpowiedź zawiera informację o weryfikacji przez IT Support.")
    else:
        notes_parts.append("Brak informacji o weryfikacji przez IT Support.")

    return {
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "notes": " ".join(notes_parts),
    }
