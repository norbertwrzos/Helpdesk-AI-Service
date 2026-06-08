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


def test_update_priority(client: TestClient) -> None:
    created = client.post(
        "/priorities",
        json={"name": "Średni", "level": 2, "description": "Standardowy."},
    )

    response = client.patch(
        f"/priorities/{created.json()['id']}",
        json={"name": "Wysoki", "level": 3, "description": "Wymaga szybkiej reakcji."},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Wysoki"
    assert data["level"] == 3
    assert data["description"] == "Wymaga szybkiej reakcji."


def test_update_missing_priority_returns_404(client: TestClient) -> None:
    response = client.patch(
        "/priorities/999",
        json={"name": "Nieistniejący", "level": 2},
    )

    assert response.status_code == 404


def test_update_priority_duplicate_name_returns_409(client: TestClient) -> None:
    first = client.post("/priorities", json={"name": "Niski", "level": 1})
    second = client.post("/priorities", json={"name": "Wysoki", "level": 3})

    response = client.patch(
        f"/priorities/{second.json()['id']}",
        json={"name": first.json()["name"]},
    )

    assert response.status_code == 409
