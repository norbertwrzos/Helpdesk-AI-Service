from fastapi.testclient import TestClient


def test_create_category(client: TestClient) -> None:
    response = client.post(
        "/categories",
        json={"name": "Sieć i VPN", "description": "Problemy z siecią i VPN."},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sieć i VPN"
    assert "id" in data


def test_list_categories(client: TestClient) -> None:
    client.post("/categories", json={"name": "Sprzęt komputerowy"})
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_duplicate_category(client: TestClient) -> None:
    client.post("/categories", json={"name": "Duplikat"})
    response = client.post("/categories", json={"name": "Duplikat"})
    assert response.status_code == 409
