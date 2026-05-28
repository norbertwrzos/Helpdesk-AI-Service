"""Testy endpointów metryk jakości odpowiedzi AI."""
from fastapi.testclient import TestClient


def _create_ticket_and_analyze(client: TestClient) -> tuple[int, int]:
    """Pomocnik: tworzy ticket, uruchamia analizę, zwraca (ticket_id, ai_response_id)."""
    resp = client.post(
        "/tickets",
        json={"title": "Awaria systemu", "description": "System nie odpowiada."},
    )
    ticket_id = resp.json()["id"]
    client.post(f"/tickets/{ticket_id}/analyze")
    ai_responses = client.get(f"/tickets/{ticket_id}/ai-responses").json()
    ai_response_id = ai_responses[0]["id"]
    return ticket_id, ai_response_id


def test_quality_metrics_empty(client: TestClient) -> None:
    resp = client.get("/quality/ai-responses")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_ai_responses"] == 0
    assert data["total_feedback"] == 0
    assert data["average_rating"] is None
    assert data["feedback_coverage_percent"] == 0.0
    assert data["helpful_count"] == 0
    assert data["not_helpful_count"] == 0
    assert data["responses_without_feedback"] == 0
    assert isinstance(data["rating_distribution"], dict)


def test_quality_metrics_with_data(client: TestClient) -> None:
    ticket_id, ai_response_id = _create_ticket_and_analyze(client)

    # Dodaj feedback
    client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 4, "is_helpful": True},
    )

    resp = client.get("/quality/ai-responses")
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_ai_responses"] >= 1
    assert data["total_feedback"] >= 1
    assert data["average_rating"] is not None
    assert 1.0 <= data["average_rating"] <= 5.0
    assert data["helpful_count"] >= 1
    assert data["feedback_coverage_percent"] > 0


def test_quality_metrics_rating_distribution(client: TestClient) -> None:
    ticket_id, ai_response_id = _create_ticket_and_analyze(client)

    client.post(
        f"/tickets/{ticket_id}/feedback",
        json={"ai_response_id": ai_response_id, "rating": 5, "is_helpful": True},
    )

    resp = client.get("/quality/ai-responses")
    data = resp.json()

    dist = data["rating_distribution"]
    assert isinstance(dist, dict)
    # Klucze 1-5 muszą być obecne
    for key in ["1", "2", "3", "4", "5"]:
        assert key in dist
    assert dist["5"] >= 1


def test_quality_metrics_coverage_percent(client: TestClient) -> None:
    # Utwórz 2 tickety z analizą
    ticket_id_1, ai_response_id_1 = _create_ticket_and_analyze(client)
    _create_ticket_and_analyze(client)

    # Dodaj feedback tylko dla jednego
    client.post(
        f"/tickets/{ticket_id_1}/feedback",
        json={"ai_response_id": ai_response_id_1, "rating": 3},
    )

    resp = client.get("/quality/ai-responses")
    data = resp.json()

    assert data["total_ai_responses"] >= 2
    assert data["total_feedback"] >= 1
    assert data["responses_without_feedback"] >= 1
    # Pokrycie < 100%
    assert data["feedback_coverage_percent"] < 100.0
