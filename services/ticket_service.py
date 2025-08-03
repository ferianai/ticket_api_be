from repo.ticket_repo import TicketRepo
from shared.crono import now


class TicketService:
    @staticmethod
    def get_all_tickets():
        return TicketRepo.get_all_tickets()

    @staticmethod
    def get_ticket_by_id(ticket_id):
        ticket = TicketRepo.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        return ticket

    @staticmethod
    def create_ticket(data):
        if data["time"] < now():
            raise ValueError("Time must be in the future")
        return TicketRepo.create_ticket(data)

    @staticmethod
    def mark_ticket_as_used(ticket_id):
        ticket = TicketRepo.mark_ticket_as_used(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        return ticket

    @staticmethod
    def delete_ticket(ticket_id):
        success = TicketRepo.delete_ticket(ticket_id)
        if not success:
            raise ValueError("Ticket not found")
        return success
