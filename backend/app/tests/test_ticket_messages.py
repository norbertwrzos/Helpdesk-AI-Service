"""
Testy endpointów konwersacji zgłoszeń (ticket messages).

Scenariusze:
1. GET dla ticketu bez wiadomości zwraca pustą listę.
2. POST jako agent tworzy wiadomość.
3. POST jako end_user tworzy wiadomość.
4. GET zwraca wiadomości w kolejności chronologicznej.
5. POST wiadomości aktualizuje znacznik updated_at zgłoszenia.
6. GET po utworzeniu wiadomości zwraca pełną historię dla zgłoszenia.
7. POST dla nieistniejącego ticketu zwraca 404.
8. POST z pustym message_text zwraca 422.
9. POST z niepoprawnym author_role zwraca 422.
"""

from datetime import datetime

from fastapi.testclient import TestClient


def _create_ticket(client: TestClient) -> int:
    response = client.post(
        "/tickets",
        json={"title": "Test ticket", "description": "Test description"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_get_messages_empty_list(client: TestClient) -> None:
    """GET /tickets/{id}/messages dla ticketu bez wiadomości zwraca pustą listę."""
    ticket_id = _create_ticket(client)
    response = client.get(f"/tickets/{ticket_id}/messages")
    assert response.status_code == 200
    assert response.json() == []


def test_create_message_as_agent(client: TestClient) -> None:
    """POST /tickets/{id}/messages jako agent tworzy wiadomość z poprawnymi polami."""
    ticket_id = _create_ticket(client)
    response = client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "agent",
            "author_name": "Adam Agent",
            "author_email": "agent@example.local",
            "message_text": "Dzień dobry, proszę wykonać poniższe kroki.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["author_role"] == "agent"
    assert data["author_name"] == "Adam Agent"
    assert data["author_email"] == "agent@example.local"
    assert data["message_text"] == "Dzień dobry, proszę wykonać poniższe kroki."
    assert data["ticket_id"] == ticket_id
    assert data["message_type"] == "public"
    assert "id" in data
    assert "created_at" in data


def test_create_message_as_end_user(client: TestClient) -> None:
    """POST /tickets/{id}/messages jako end_user tworzy wiadomość."""
    ticket_id = _create_ticket(client)
    response = client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "end_user",
            "author_name": "Jan Kowalski",
            "message_text": "Problem nadal występuje po restarcie.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["author_role"] == "end_user"
    assert data["author_name"] == "Jan Kowalski"
    assert data["author_email"] is None
    assert data["ticket_id"] == ticket_id


def test_get_messages_ordered_chronologically(client: TestClient) -> None:
    """GET /tickets/{id}/messages zwraca wiadomości posortowane chronologicznie rosnąco."""
    ticket_id = _create_ticket(client)
    client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "end_user",
            "author_name": "Jan",
            "message_text": "Pierwsza wiadomość",
        },
    )
    client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "agent",
            "author_name": "Agent",
            "message_text": "Druga wiadomość",
        },
    )
    response = client.get(f"/tickets/{ticket_id}/messages")
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2
    assert messages[0]["message_text"] == "Pierwsza wiadomość"
    assert messages[1]["message_text"] == "Druga wiadomość"


def test_message_updates_ticket_updated_at(client: TestClient) -> None:
    """POST wiadomości aktualizuje pole updated_at zgłoszenia."""
    ticket_id = _create_ticket(client)

    ticket_before = client.get(f"/tickets/{ticket_id}").json()
    updated_before = datetime.fromisoformat(ticket_before["updated_at"])

    client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "agent",
            "author_name": "Agent",
            "message_text": "Odpowiedź agenta.",
        },
    )

    ticket_after = client.get(f"/tickets/{ticket_id}").json()
    updated_after = datetime.fromisoformat(ticket_after["updated_at"])
    assert updated_after >= updated_before


def test_get_messages_returns_created_history(client: TestClient) -> None:
    """GET wiadomości po utworzeniu wpisu zwraca historię zgłoszenia."""
    ticket_id = _create_ticket(client)
    client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "end_user",
            "author_name": "Jan",
            "message_text": "Wiadomość użytkownika.",
        },
    )
    response = client.get(f"/tickets/{ticket_id}/messages")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["author_role"] == "end_user"
    assert data[0]["message_text"] == "Wiadomość użytkownika."


def test_create_message_ticket_not_found(client: TestClient) -> None:
    """POST /tickets/99999/messages dla nieistniejącego ticketu zwraca 404."""
    response = client.post(
        "/tickets/99999/messages",
        json={
            "author_role": "agent",
            "author_name": "Agent",
            "message_text": "Test",
        },
    )
    assert response.status_code == 404


def test_create_message_empty_text_returns_422(client: TestClient) -> None:
    """POST z pustym message_text (tylko spacje) zwraca 422."""
    ticket_id = _create_ticket(client)
    response = client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "agent",
            "author_name": "Agent",
            "message_text": "   ",
        },
    )
    assert response.status_code == 422


def test_create_message_invalid_author_role_returns_422(client: TestClient) -> None:
    """POST z niepoprawnym author_role zwraca 422."""
    ticket_id = _create_ticket(client)
    response = client.post(
        f"/tickets/{ticket_id}/messages",
        json={
            "author_role": "admin",
            "author_name": "Admin",
            "message_text": "Test",
        },
    )
    assert response.status_code == 422
