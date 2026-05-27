from fastapi.testclient import TestClient


def test_create_priority(client: TestClient) -> None:
    response = client.post(
        "/priorities",
        json={"name": "Wysoki", "level": 3, "description": "Wysoki priorytet."},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Wysoki"
    assert data["level"] == 3
    assert "id" in data


def test_list_priorities(client: TestClient) -> None:
    client.post("/priorities", json={"name": "Niski", "level": 1})
    response = client.get("/priorities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_duplicate_priority(client: TestClient) -> None:
    client.post("/priorities", json={"name": "Krytyczny", "level": 4})
    response = client.post("/priorities", json={"name": "Krytyczny", "level": 4})
    assert response.status_code == 409
