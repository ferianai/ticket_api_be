from instance.database import db
from models.ticket import Ticket
from sqlalchemy.exc import SQLAlchemyError


class TicketRepo:
    @staticmethod
    def get_all_tickets():
        return Ticket.query.all()

    @staticmethod
    def get_ticket_by_id(ticket_id):
        return db.session.get(Ticket, ticket_id)

    @staticmethod
    def create_ticket(data):
        try:
            # Check if existing ticket with the same event name and location and time
            existing_ticket = Ticket.query.filter_by(
                event_name=data.get("event_name"),
                location=data.get("location"),
                time=data.get("time"),
            ).first()
            if existing_ticket:
                raise ValueError(
                    "Ticket with the same event name, location, and time already exists."
                )

            ticket = Ticket(
                event_name=data.get("event_name"),
                location=data.get("location"),
                time=data.get("time"),
                is_used=data.get("is_used", False),
            )
            db.session.add(ticket)
            db.session.commit()
            return ticket
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def mark_ticket_as_used(ticket_id):
        ticket = db.session.get(Ticket, ticket_id)
        if ticket:
            try:
                ticket.is_used = True
                db.session.commit()
                return ticket
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e
        return None

    @staticmethod
    def delete_ticket(ticket_id):
        ticket = db.session.get(Ticket, ticket_id)
        if ticket:
            try:
                db.session.delete(ticket)
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e
        return False
