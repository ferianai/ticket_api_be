import pytest
from datetime import datetime, timedelta
from shared.crono import now
from instance.database import db
from models.ticket import Ticket
import json


def test_get_all_tickets_empty(client):
    response = client.get("/tickets")
    assert response.status_code == 200
    assert response.json == []


def test_create_ticket_success(client):
    data = {
        "event_name": "Concert",
        "location": "Stadium",
        "time": (now() + timedelta(days=1)).isoformat(),
        "is_used": False,
    }
    response = client.post("/tickets", json=data)
    assert response.status_code == 201
    json_data = response.json
    assert json_data["event_name"] == data["event_name"]
    assert json_data["location"] == data["location"]
    assert json_data["is_used"] == False


def test_create_ticket_missing_fields(client):
    data = {"location": "Stadium"}
    response = client.post("/tickets", json=data)
    assert response.status_code == 400
    assert "Missing required fields" in response.json.get("error", "")


def test_create_ticket_invalid_time(client):
    data = {
        "event_name": "Concert",
        "location": "Stadium",
        "time": "invalid-time-format",
    }
    response = client.post("/tickets", json=data)
    assert response.status_code == 400
    assert "Invalid time format" in response.json.get("error", "")


def test_get_ticket_by_id(client):
    # Create ticket first
    data = {
        "event_name": "Show",
        "location": "Theater",
        "time": (now() + timedelta(days=2)).isoformat(),
        "is_used": False,
    }
    post_resp = client.post("/tickets", json=data)
    ticket_id = post_resp.json["id"]

    get_resp = client.get(f"/tickets/{ticket_id}")
    assert get_resp.status_code == 200
    assert get_resp.json["id"] == ticket_id


def test_get_ticket_not_found(client):
    response = client.get("/tickets/999999")
    assert response.status_code == 404
    assert "Ticket not found" in response.json.get("error", "")


def test_patch_mark_ticket_as_used(client):
    # Create ticket first
    data = {
        "event_name": "Event",
        "location": "Venue",
        "time": (now() + timedelta(days=3)).isoformat(),
        "is_used": False,
    }
    post_resp = client.post("/tickets", json=data)
    ticket_id = post_resp.json["id"]

    patch_resp = client.patch(f"/tickets/{ticket_id}")
    assert patch_resp.status_code == 200
    assert patch_resp.json["is_used"] == True


def test_patch_ticket_not_found(client):
    response = client.patch("/tickets/999999")
    assert response.status_code == 404
    assert "Ticket not found" in response.json.get("error", "")


def test_delete_ticket(client):
    # Create ticket first
    data = {
        "event_name": "Delete Event",
        "location": "Delete Venue",
        "time": (now() + timedelta(days=4)).isoformat(),
        "is_used": False,
    }
    post_resp = client.post("/tickets", json=data)
    ticket_id = post_resp.json["id"]

    delete_resp = client.delete(f"/tickets/{ticket_id}")
    assert delete_resp.status_code == 200
    assert "Ticket deleted successfully" in delete_resp.json.get("message", "")


def test_delete_ticket_not_found(client):
    response = client.delete("/tickets/999999")
    assert response.status_code == 404
    assert "Ticket not found" in response.json.get("error", "")
