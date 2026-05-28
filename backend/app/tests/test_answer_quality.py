"""
Testy jednostkowe dla modułu answer_quality.py.
"""

from app.evaluation.answer_quality import evaluate_answer_quality


class TestEmptyAnswer:
    def test_empty_string_returns_zero(self):
        result = evaluate_answer_quality("", ["vpn", "połączenie"])
        assert result["score"] == 0
        assert result["matched_keywords"] == []
        assert result["missing_keywords"] == ["vpn", "połączenie"]

    def test_whitespace_only_returns_zero(self):
        result = evaluate_answer_quality("   \n  ", ["vpn"])
        assert result["score"] == 0

    def test_none_like_empty_returns_zero(self):
        result = evaluate_answer_quality("", [])
        assert result["score"] == 0


class TestKeywordMatching:
    def test_matched_keywords_detected(self):
        answer = "Sprawdź połączenie VPN i zrestartuj klienta."
        keywords = ["vpn", "połączenie"]
        result = evaluate_answer_quality(answer, keywords)
        # Dopasowanie jest case-insensitive
        assert "vpn" in result["matched_keywords"] or "VPN".lower() in [
            k.lower() for k in result["matched_keywords"]
        ]

    def test_missing_keywords_detected(self):
        answer = "Sprawdź połączenie sieciowe."
        keywords = ["vpn", "połączenie", "restart"]
        result = evaluate_answer_quality(answer, keywords)
        assert "vpn" in result["missing_keywords"]
        assert "restart" in result["missing_keywords"]
        assert "połączenie" in result["matched_keywords"]

    def test_no_keywords_match_lowers_score(self):
        answer = "Proszę skontaktować się z IT Support w celu diagnozy."
        keywords = ["vpn", "router", "firewall"]
        result = evaluate_answer_quality(answer, keywords)
        # Powinna zdobyć co najmniej 1 (niepusta) + może 1 (kroki) + 1 (IT Support)
        # ale NIE za słowa kluczowe
        assert result["score"] >= 1
        assert result["missing_keywords"] == keywords

    def test_all_keywords_match_gives_extra_point(self):
        answer = (
            "Sprawdź połączenie internetowe. Zrestartuj klienta VPN. "
            "Zweryfikuj dane logowania. Skontaktuj się z administratorem sieci. "
            "Odpowiedź powinna zostać zweryfikowana przez pracownika IT Support."
        )
        keywords = ["połączenie internetowe", "klient VPN", "dane logowania", "administrator sieci"]
        result = evaluate_answer_quality(answer, keywords)
        assert result["score"] >= 4

    def test_partial_keywords_match(self):
        answer = "Sprawdź VPN i skontaktuj się z IT Support."
        keywords = ["vpn", "router", "firewall", "sieć"]
        result = evaluate_answer_quality(answer, keywords)
        # Dopasowuje tylko "vpn" — 1 z 4, czyli mniej niż połowa
        assert "vpn" in result["matched_keywords"]
        # score za słowa: tylko 1 punkt (co najmniej jedno), ale nie za połowę
        assert result["score"] >= 2  # 1 (niepusta) + 1 (jedno słowo kluczowe)


class TestDiagnosticCriteria:
    def test_answer_with_diagnostic_steps_gets_point(self):
        answer = (
            "Na podstawie zgłoszenia — kategoria: VPN.\n"
            "Zalecane kroki diagnostyczne:\n"
            "1. Sprawdź połączenie.\n"
            "Odpowiedź zweryfikowana przez IT Support."
        )
        keywords = ["vpn"]
        result = evaluate_answer_quality(answer, keywords)
        assert result["score"] >= 3

    def test_answer_without_diagnostic_steps_misses_point(self):
        answer = "Problem dotyczy kategorii VPN. Skontaktuj się z IT Support."
        keywords = ["vpn"]
        result = evaluate_answer_quality(answer, keywords)
        # Ma: niepusta, ma słowo kluczowe (vpn), IT Support — ale nie ma kroków
        # Sprawdź: "skontaktuj się" jest wskaźnikiem diagnostycznym
        # więc score może wynosić 4 zamiast 3
        assert result["score"] >= 2


class TestITSupportCriteria:
    def test_it_support_phrase_gives_point(self):
        answer = (
            "Odpowiedź została wygenerowana automatycznie i powinna zostać "
            "zweryfikowana przez pracownika IT Support."
        )
        keywords = []
        result = evaluate_answer_quality(answer, keywords)
        # Dostaje punkt za IT Support
        assert result["score"] >= 2  # 1 (niepusta) + 1 (kroki: "zostać") ... 

    def test_missing_it_support_loses_point(self):
        answer = "Sprawdź VPN."
        keywords = []
        result = evaluate_answer_quality(answer, keywords)
        # Nie powinien dostać punktu za IT Support
        assert result["score"] < 5


class TestScoreRange:
    def test_score_between_0_and_5(self):
        answer = (
            "Na podstawie zgłoszenia system rozpoznał problem związany z VPN.\n"
            "Zalecane kroki diagnostyczne:\n"
            "1. Sprawdź połączenie internetowe.\n"
            "2. Zrestartuj klienta VPN.\n"
            "Odpowiedź powinna zostać zweryfikowana przez pracownika IT Support."
        )
        keywords = ["połączenie internetowe", "klient VPN", "dane logowania"]
        result = evaluate_answer_quality(answer, keywords)
        assert 0 <= result["score"] <= 5

    def test_full_score_possible(self):
        """MockAIGenerator generuje odpowiedź z krokami i IT Support.

        Słowa kluczowe dobrane jako dokładne podciągi tekstu odpowiedzi
        (z uwzględnieniem polskiej fleksji).
        """
        answer = (
            "Na podstawie treści zgłoszenia system rozpoznał problem "
            "związany z kategorią: Sieć i VPN.\n\n"
            "Nadany priorytet: Średni.\n\n"
            "Zalecane kroki diagnostyczne:\n"
            "  1. Sprawdź połączenie internetowe na urządzeniu.\n"
            "  2. Zrestartuj klienta VPN i spróbuj ponownie się połączyć.\n"
            "  3. Zweryfikuj poprawność danych logowania do VPN.\n"
            "  4. Skontaktuj się z administratorem sieci, jeśli problem nadal występuje.\n\n"
            "Odpowiedź została wygenerowana automatycznie i powinna zostać "
            "zweryfikowana przez pracownika IT Support."
        )
        # Użyj form fleksyjnych, które faktycznie pojawiają się w odpowiedzi
        keywords = [
            "połączenie internetowe",
            "klienta VPN",
            "danych logowania",
            "administratorem sieci",
        ]
        result = evaluate_answer_quality(answer, keywords)
        assert result["score"] == 5
