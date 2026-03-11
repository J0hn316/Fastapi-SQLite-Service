from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_note_requires_api_key(client: TestClient) -> None:
    response = client.post(
        "/notes", json={"title": "Unauthorized note", "content": "No key"}
    )
    assert response.status_code == 401


def test_create_note_success(client: TestClient, api_headers: dict[str, str]) -> None:
    response = client.post(
        "/notes",
        headers=api_headers,
        json={"title": "Test Note", "content": "Hello", "tags": "demo"},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Hello"
    assert data["tags"] == "demo"
    assert "id" in data


def test_list_notes_returns_created_note(
    client: TestClient, api_headers: dict[str, str]
) -> None:
    client.post(
        "/notes",
        headers=api_headers,
        json={"title": "List Me", "content": "Present in list"},
    )

    response = client.get("/notes", headers=api_headers)

    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["total"] >= 1

    titles = [item["title"] for item in data["items"]]
    assert "List Me" in titles
