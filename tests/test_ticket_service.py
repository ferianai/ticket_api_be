import pytest
from services.ticket_service import TicketService
from models.ticket import Ticket
from shared.crono import now
from datetime import timedelta
from instance.database import db


@pytest.fixture
def ticket_data():
    return {
        "event_name": "Concert",
        "location": "Stadium",
        "time": now() + timedelta(days=1),  # Ensure time is in the future
        "is_used": False,
    }


def test_create_ticket_success(app, ticket_data):
    with app.app_context():
        service = TicketService()
        ticket = service.create_ticket(ticket_data)
        assert ticket.id is not None
        assert ticket.event_name == ticket_data["event_name"]
        assert ticket.location == ticket_data["location"]
        assert ticket.is_used is False
        db.session.delete(ticket)  # Clean up after test
        db.session.commit()


def tset_get_all_tickets_empty(app):
    with app.app_context():
        service = TicketService()
        tickets = service.get_all_tickets()
        assert tickets == []


def test_get_ticket_all_tickets(app, ticket_data):
    with app.app_context():
        service = TicketService()
        # Create a ticket first
        ticket = service.create_ticket(ticket_data)
        tickets = service.get_all_tickets()
        assert len(tickets) >= 1
        assert tickets[0].id == ticket.id
        db.session.delete(ticket)  # Clean up after test
        db.session.commit()


def test_get_ticket_by_id(app, ticket_data):
    with app.app_context():
        service = TicketService()
        # Create a ticket first
        ticket = service.create_ticket(ticket_data)
        fetched_ticket = service.get_ticket_by_id(ticket.id)
        assert fetched_ticket is not None
        assert fetched_ticket.id == ticket.id
        db.session.delete(ticket)  # Clean up after test
        db.session.commit()


def test_mark_ticket_as_used(app, ticket_data):
    with app.app_context():
        service = TicketService()
        # Create a ticket first
        ticket = service.create_ticket(ticket_data)
        updated_ticket = service.mark_ticket_as_used(ticket.id)
        assert updated_ticket.is_used is True
        db.session.delete(updated_ticket)  # Clean up after test
        db.session.commit()


def test_mark_ticket_as_used_not_found(app, ticket_data):
    with app.app_context():
        service = TicketService()
        # Attempt to mark a non-existent ticket as used
        # did not raise value error but jsonify error jsonify({"error": "Ticket not found"})
        with pytest.raises(ValueError, match="Ticket not found"):
            service.mark_ticket_as_used(999999)


def test_delete_ticket(app, ticket_data):
    with app.app_context():
        service = TicketService()
        # Create a ticket first
        ticket = service.create_ticket(ticket_data)
        service.delete_ticket(ticket.id)
        # Verify the ticket is deleted
        with pytest.raises(ValueError, match="Ticket not found"):
            service.get_ticket_by_id(ticket.id)  # Should raise an error


def test_delete_ticket_not_found(app):
    with app.app_context():
        service = TicketService()
        # Attempt to delete a non-existent ticket
        with pytest.raises(ValueError, match="Ticket not found"):
            service.delete_ticket(999999)  # Non-existent ID


def test_get_ticket_by_id_not_found(app):
    with app.app_context():
        service = TicketService()
        # Attempt to get a non-existent ticket
        with pytest.raises(ValueError, match="Ticket not found"):
            service.get_ticket_by_id(999999)  # Non-existent ID
