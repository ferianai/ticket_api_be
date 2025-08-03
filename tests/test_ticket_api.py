import pytest
from datetime import timedelta
from shared.crono import now


# Helper function to build ticket data
# This function creates a dictionary with default values for a ticket. It can be customized by passing different parameters.
def build_ticket_data(name="Concert", location="Stadium", days=1, is_used=False):
    return {
        "event_name": name,
        "location": location,
        "time": (now() + timedelta(days=days)).isoformat(),
        "is_used": is_used,
    }


def test_get_all_tickets_empty(client):
    response = client.get("/tickets")
    assert response.status_code == 200
    assert response.json == []


def test_create_ticket_success(client):
    response = client.post("/tickets", json=build_ticket_data())
    assert response.status_code == 201
    ticket = response.json["ticket"]
    assert ticket["event_name"] == "Concert"
    assert ticket["location"] == "Stadium"
    assert ticket["is_used"] is False


def test_create_ticket_missing_fields(client):
    response = client.post("/tickets", json={"location": "Stadium"})
    assert response.status_code == 400
    assert "Missing required fields" in response.json.get("error", "")


def test_create_ticket_invalid_time(client):
    data = build_ticket_data()
    data["time"] = "not-a-valid-time"
    response = client.post("/tickets", json=data)
    assert response.status_code == 400
    assert "Invalid time format" in response.json.get("error", "")


def test_get_ticket_by_id(client):
    post = client.post("/tickets", json=build_ticket_data(name="Show", days=2))
    ticket_id = post.json["ticket"]["id"]

    get_resp = client.get(f"/tickets/{ticket_id}")
    assert get_resp.status_code == 200
    assert get_resp.json["id"] == ticket_id


def test_get_ticket_not_found(client):
    response = client.get("/tickets/999999")
    assert response.status_code == 404
    assert "Ticket not found" in response.json.get("error", "")


def test_patch_mark_ticket_as_used(client):
    post = client.post("/tickets", json=build_ticket_data(name="Event", days=3))
    ticket_id = post.json["ticket"]["id"]

    patch = client.patch(f"/tickets/{ticket_id}")
    assert patch.status_code == 200
    assert patch.json["is_used"] is True


def test_patch_ticket_not_found(client):
    response = client.patch("/tickets/999999")
    assert response.status_code == 404
    assert "Ticket not found" in response.json.get("error", "")


def test_delete_ticket(client):
    post = client.post("/tickets", json=build_ticket_data(name="To Delete", days=4))
    ticket_id = post.json["ticket"]["id"]

    delete_resp = client.delete(f"/tickets/{ticket_id}")
    assert delete_resp.status_code == 200
    assert "Ticket deleted successfully" in delete_resp.json.get("message", "")


def test_delete_ticket_not_found(client):
    response = client.delete("/tickets/999999")
    assert response.status_code == 404
    assert "Ticket not found" in response.json.get("error", "")


def test_create_ticket_duplicate_should_fail(client):
    data = {
        "event_name": "Same Event",
        "location": "Same Place",
        "time": (now() + timedelta(days=5)).isoformat(),
        "is_used": False,
    }
    client.post("/tickets", json=data)
    response = client.post("/tickets", json=data)
    assert response.status_code == 400
    assert "already exists" in response.json.get("error", "")
