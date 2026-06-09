from __future__ import annotations

import re

_ACTIONABLE_VERBS = [
    "proszę",
    "sprawdź",
    "sprawdzić",
    "uruchom",
    "uruchomić",
    "zweryfikuj",
    "zweryfikować",
    "skontaktuj",
    "upewnij się",
]


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def _match_keywords(text: str, expected_keywords: list[str]) -> tuple[list[str], list[str]]:
    normalized_text = _normalize(text)
    matched = [keyword for keyword in expected_keywords if keyword.lower() in normalized_text]
    missing = [keyword for keyword in expected_keywords if keyword.lower() not in normalized_text]
    return matched, missing


def has_email_greeting(text: str) -> bool:
    first_line = next((line.strip().lower() for line in (text or "").splitlines() if line.strip()), "")
    return first_line.startswith("dzień dobry")


def has_email_closing(text: str) -> bool:
    return "pozdrawiam" in _normalize(text)


def has_agent_signature(text: str, agent_name: str) -> bool:
    normalized_agent_name = _normalize(agent_name)
    return bool(normalized_agent_name) and normalized_agent_name in _normalize(text)


def has_actionable_steps(text: str) -> bool:
    normalized_text = _normalize(text)
    if re.search(r"(^|\n)\s*(?:[-*]|\d+[.)])\s+", text or ""):
        return True
    return any(verb in normalized_text for verb in _ACTIONABLE_VERBS)


def evaluate_mail_response(text: str, expected_keywords: list[str], agent_name: str) -> dict:
    if not text or not text.strip():
        return {
            "score": 0,
            "has_greeting": False,
            "has_closing": False,
            "has_signature": False,
            "has_actionable_steps": False,
            "matched_keywords": [],
            "missing_keywords": list(expected_keywords),
            "notes": "Brak treści odpowiedzi mailowej.",
        }

    matched_keywords, missing_keywords = _match_keywords(text, expected_keywords)
    greeting = has_email_greeting(text)
    closing = has_email_closing(text)
    signature = has_agent_signature(text, agent_name)
    actionable_steps = has_actionable_steps(text)

    score = 0
    notes: list[str] = []

    if greeting:
        score += 1
    else:
        notes.append("Brak standardowego powitania mailowego.")

    if closing:
        score += 1
    else:
        notes.append("Brak standardowego zakończenia mailowego.")

    if signature:
        score += 1
    else:
        notes.append("Brak podpisu agenta.")

    if actionable_steps:
        score += 1
    else:
        notes.append("Brak jasnych kroków do wykonania.")

    if matched_keywords or not expected_keywords:
        score += 1
    else:
        notes.append("Brak oczekiwanych słów kluczowych w odpowiedzi.")

    if not notes:
        notes.append("Odpowiedź spełnia oczekiwany format mailowy.")

    return {
        "score": score,
        "has_greeting": greeting,
        "has_closing": closing,
        "has_signature": signature,
        "has_actionable_steps": actionable_steps,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "notes": " ".join(notes),
    }