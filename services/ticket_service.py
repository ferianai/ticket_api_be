from repo.ticket_repo import TicketRepo
from sqlalchemy.exc import SQLAlchemyError


class TicketService:
    @staticmethod
    def get_all_tickets():
        return TicketRepo.get_all_tickets()

    @staticmethod
    def get_ticket_by_id(ticket_id):
        return TicketRepo.get_ticket_by_id(ticket_id)

    @staticmethod
    def create_ticket(data):
        # Add any business logic or validation here if needed
        return TicketRepo.create_ticket(data)

    @staticmethod
    def mark_ticket_as_used(ticket_id):
        return TicketRepo.mark_ticket_as_used(ticket_id)

    @staticmethod
    def delete_ticket(ticket_id):
        return TicketRepo.delete_ticket(ticket_id)
