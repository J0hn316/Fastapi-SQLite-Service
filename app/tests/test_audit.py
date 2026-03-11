from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_note_generates_audit_event(
    client: TestClient, api_headers: dict[str, str]
) -> None:
    create_response = client.post(
        "/notes",
        headers=api_headers,
        json={"title": "Audited Note", "content": "Track me", "tags": "audit"},
    )
    assert create_response.status_code == 201

    audit_response = client.get("/audit", headers=api_headers)
    assert audit_response.status_code == 200

    data = audit_response.json()
    assert "items" in data
    assert data["total"] >= 1

    actions = [item["action"] for item in data["items"]]
    assert "notes.create" in actions


def test_update_note_generates_audit_event(
    client: TestClient, api_headers: dict[str, str]
) -> None:
    create_response = client.post(
        "/notes",
        headers=api_headers,
        json={"title": "Before Update", "content": "Old content"},
    )
    note_id = create_response.json()["id"]

    update_response = client.patch(
        f"/notes/{note_id}",
        headers=api_headers,
        json={"title": "After Update"},
    )
    assert update_response.status_code == 200

    audit_response = client.get("/audit", headers=api_headers)
    data = audit_response.json()

    actions = [item["action"] for item in data["items"]]
    assert "notes.update" in actions
