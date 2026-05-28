"""Testy historii odpowiedzi AI z feedbackiem."""
from fastapi.testclient import TestClient


def _create_ticket(client: TestClient) -> int:
    resp = client.post(
        "/tickets",
        json={"title": "Brak internetu", "description": "Brak połączenia sieciowego."},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def test_get_ai_responses_empty(client: TestClient) -> None:
    ticket_id = _create_ticket(client)
    resp = client.get(f"/tickets/{ticket_id}/ai-responses")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_ai_responses_with_feedback(client: TestClient) -> None:
    ticket_id = _create_ticket(client)

    # Uruchom analizę — tworzy AIResponse
    analyze_resp = client.post(f"/tickets/{ticket_id}/analyze")
    assert analyze_resp.status_code == 200

    # Pobierz odpowiedzi
    resp = client.get(f"/tickets/{ticket_id}/ai-responses")
    assert resp.status_code == 200
    responses = resp.json()
    assert len(responses) >= 1

    ai_resp = responses[0]
    assert "id" in ai_resp
    assert "response_text" in ai_resp
    assert "feedback" in ai_resp
    # Brak feedbacku — null
    assert ai_resp["feedback"] is None

    # Dodaj feedback
    client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_resp["id"], "rating": 5, "is_helpful": True},
    )

    # Pobierz ponownie — feedback powinien być widoczny
    resp2 = client.get(f"/tickets/{ticket_id}/ai-responses")
    assert resp2.status_code == 200
    responses2 = resp2.json()
    assert responses2[0]["feedback"] is not None
    assert responses2[0]["feedback"]["rating"] == 5


def test_get_ai_responses_ticket_not_found(client: TestClient) -> None:
    resp = client.get("/tickets/99999/ai-responses")
    assert resp.status_code == 404
