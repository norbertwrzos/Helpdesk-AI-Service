from fastapi.testclient import TestClient


def test_create_ticket(client: TestClient) -> None:
    response = client.post(
        "/tickets",
        json={"title": "Brak dostępu do VPN", "description": "Nie mogę połączyć się z VPN."},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Brak dostępu do VPN"
    assert data["status"] == "open"
    assert data["source"] == "manual"
    assert "id" in data


def test_list_tickets(client: TestClient) -> None:
    client.post(
        "/tickets",
        json={"title": "Problem z drukarką", "description": "Drukarka nie drukuje."},
    )
    response = client.get("/tickets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_ticket(client: TestClient) -> None:
    create_resp = client.post(
        "/tickets",
        json={"title": "Reset hasła", "description": "Zapomniałem hasła do konta."},
    )
    ticket_id = create_resp.json()["id"]

    response = client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id


def test_get_ticket_not_found(client: TestClient) -> None:
    response = client.get("/tickets/99999")
    assert response.status_code == 404


def test_update_ticket(client: TestClient) -> None:
    create_resp = client.post(
        "/tickets",
        json={"title": "Awaria monitora", "description": "Monitor nie wyświetla obrazu."},
    )
    ticket_id = create_resp.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={"status": "pending"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_create_ticket_with_email_source(client: TestClient) -> None:
    response = client.post(
        "/tickets",
        json={
            "title": "Problem z pocztą",
            "description": "Nie dostaję e-maili.",
            "source": "email",
        },
    )
    assert response.status_code == 201
    assert response.json()["source"] == "email"
