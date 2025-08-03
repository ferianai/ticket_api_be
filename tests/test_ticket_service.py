import pytest
from services.ticket_service import TicketService
from shared.crono import now
from datetime import timedelta
from instance.database import db


@pytest.fixture
def ticket_data():
    return {
        "event_name": "Concert",
        "location": "Stadium",
        "time": now() + timedelta(days=1),
        "is_used": False,
    }


def test_create_ticket_success(app, ticket_data):
    with app.app_context():
        ticket = TicketService.create_ticket(ticket_data)
        assert ticket.id is not None
        assert ticket.event_name == ticket_data["event_name"]
        assert ticket.location == ticket_data["location"]
        assert ticket.is_used is False
        db.session.delete(ticket)
        db.session.commit()


def test_get_all_tickets_empty(app):
    with app.app_context():
        tickets = TicketService.get_all_tickets()
        assert tickets == []


def test_get_all_tickets_contains_ticket(app, ticket_data):
    with app.app_context():
        ticket = TicketService.create_ticket(ticket_data)
        tickets = TicketService.get_all_tickets()
        assert any(t.id == ticket.id for t in tickets)
        db.session.delete(ticket)
        db.session.commit()


def test_get_ticket_by_id(app, ticket_data):
    with app.app_context():
        ticket = TicketService.create_ticket(ticket_data)
        fetched = TicketService.get_ticket_by_id(ticket.id)
        assert fetched.id == ticket.id
        db.session.delete(ticket)
        db.session.commit()


def test_get_ticket_by_id_not_found(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Ticket not found"):
            TicketService.get_ticket_by_id(999999)


def test_mark_ticket_as_used(app, ticket_data):
    with app.app_context():
        ticket = TicketService.create_ticket(ticket_data)
        updated = TicketService.mark_ticket_as_used(ticket.id)
        assert updated.is_used is True
        db.session.delete(updated)
        db.session.commit()


def test_mark_ticket_as_used_not_found(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Ticket not found"):
            TicketService.mark_ticket_as_used(999999)


def test_delete_ticket(app, ticket_data):
    with app.app_context():
        ticket = TicketService.create_ticket(ticket_data)
        TicketService.delete_ticket(ticket.id)
        with pytest.raises(ValueError, match="Ticket not found"):
            TicketService.get_ticket_by_id(ticket.id)


def test_delete_ticket_not_found(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Ticket not found"):
            TicketService.delete_ticket(999999)


def test_create_duplicate_ticket_should_fail(app, ticket_data):
    with app.app_context():
        TicketService.create_ticket(ticket_data)
        with pytest.raises(ValueError, match="already exists"):
            TicketService.create_ticket(ticket_data)


def test_create_ticket_with_past_time_should_fail(app, ticket_data):
    ticket_data["time"] = now() - timedelta(days=1)
    with app.app_context():
        with pytest.raises(ValueError, match="in the future"):
            TicketService.create_ticket(ticket_data)
