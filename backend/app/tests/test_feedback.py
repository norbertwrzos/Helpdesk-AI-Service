"""Testy endpointów feedbacku odpowiedzi AI."""
import pytest
from fastapi.testclient import TestClient


def _create_ticket(client: TestClient) -> int:
    resp = client.post(
        "/tickets",
        json={"title": "Problem z VPN", "description": "Nie działa VPN."},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def _run_analysis(client: TestClient, ticket_id: int) -> int:
    resp = client.post(f"/tickets/{ticket_id}/analyze")
    assert resp.status_code == 200
    # Pobierz id pierwszej odpowiedzi AI
    ai_resp = client.get(f"/tickets/{ticket_id}/ai-responses")
    assert ai_resp.status_code == 200
    responses = ai_resp.json()
    assert len(responses) >= 1
    return responses[0]["id"]


# ---------------------------------------------------------------------------
# POST /tickets/{ticket_id}/feedback
# ---------------------------------------------------------------------------

def test_create_feedback(client: TestClient) -> None:
    ticket_id = _create_ticket(client)
    ai_response_id = _run_analysis(client, ticket_id)

    resp = client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 5, "is_helpful": True, "comment": "Świetna odpowiedź."},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["rating"] == 5
    assert data["is_helpful"] is True
    assert data["comment"] == "Świetna odpowiedź."
    assert data["ticket_id"] == ticket_id
    assert data["ai_response_id"] == ai_response_id


def test_update_feedback_when_exists(client: TestClient) -> None:
    ticket_id = _create_ticket(client)
    ai_response_id = _run_analysis(client, ticket_id)

    # Pierwsza ocena
    client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 3, "is_helpful": False},
    )

    # Aktualizacja oceny
    resp = client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 4, "is_helpful": True, "comment": "Zaktualizowano."},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["rating"] == 4
    assert data["is_helpful"] is True
    assert data["comment"] == "Zaktualizowano."


def test_create_feedback_ticket_not_found(client: TestClient) -> None:
    resp = client.post(
        "/tickets/99999/feedback",
        json={"ai_response_id": 1, "rating": 3},
    )
    assert resp.status_code == 404


def test_create_feedback_ai_response_not_found(client: TestClient) -> None:
    ticket_id = _create_ticket(client)

    resp = client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": 99999, "rating": 3},
    )
    assert resp.status_code == 404


def test_create_feedback_ai_response_wrong_ticket(client: TestClient) -> None:
    ticket_id_1 = _create_ticket(client)
    ticket_id_2 = _create_ticket(client)
    ai_response_id = _run_analysis(client, ticket_id_1)

    # Próba dodania feedbacku dla odpowiedzi AI z ticketu 1 do ticketu 2
    resp = client.post(
        f"/tickets/{ticket_id_2}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 3},
    )
    assert resp.status_code == 400


def test_create_feedback_rating_out_of_range(client: TestClient) -> None:
    ticket_id = _create_ticket(client)
    ai_response_id = _run_analysis(client, ticket_id)

    # Rating 6 — poza zakresem
    resp = client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 6},
    )
    assert resp.status_code == 422

    # Rating 0 — poza zakresem
    resp2 = client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 0},
    )
    assert resp2.status_code == 422


# ---------------------------------------------------------------------------
# GET /tickets/{ticket_id}/feedback
# ---------------------------------------------------------------------------

def test_get_ticket_feedback(client: TestClient) -> None:
    ticket_id = _create_ticket(client)
    ai_response_id = _run_analysis(client, ticket_id)

    client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 4, "is_helpful": True},
    )

    resp = client.get(f"/tickets/{ticket_id}/feedback")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["rating"] == 4


def test_get_ticket_feedback_empty(client: TestClient) -> None:
    ticket_id = _create_ticket(client)
    resp = client.get(f"/tickets/{ticket_id}/feedback")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_ticket_feedback_not_found(client: TestClient) -> None:
    resp = client.get("/tickets/99999/feedback")
    assert resp.status_code == 404
