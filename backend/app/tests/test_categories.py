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


def test_update_category(client: TestClient) -> None:
    created = client.post(
        "/categories",
        json={"name": "Sieć i VPN", "description": "Problemy z siecią."},
    )

    response = client.patch(
        f"/categories/{created.json()['id']}",
        json={"name": "Sieć lokalna", "description": "LAN i VPN."},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sieć lokalna"
    assert data["description"] == "LAN i VPN."


def test_update_missing_category_returns_404(client: TestClient) -> None:
    response = client.patch(
        "/categories/999",
        json={"name": "Nieistniejąca"},
    )

    assert response.status_code == 404


def test_update_category_duplicate_name_returns_409(client: TestClient) -> None:
    first = client.post("/categories", json={"name": "Sieć"})
    second = client.post("/categories", json={"name": "Bezpieczeństwo"})

    response = client.patch(
        f"/categories/{second.json()['id']}",
        json={"name": first.json()["name"]},
    )

    assert response.status_code == 409
