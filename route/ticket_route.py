from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.ticket_service import TicketService
from datetime import datetime

ticket_bp = Blueprint("ticket", __name__, url_prefix="/tickets")


class TicketAPI(MethodView):
    def get(self, ticket_id=None):
        if ticket_id is None:
            # Return list of tickets
            tickets = TicketService.get_all_tickets()
            tickets_list = [
                {
                    "id": t.id,
                    "event_name": t.event_name,
                    "location": t.location,
                    "time": t.time.isoformat() if t.time else None,
                    "is_used": t.is_used,
                }
                for t in tickets
            ]
            return jsonify(tickets_list), 200
        else:
            # Return single ticket
            ticket = TicketService.get_ticket_by_id(ticket_id)
            if not ticket:
                return jsonify({"error": "Ticket not found"}), 404
            ticket_data = {
                "id": ticket.id,
                "event_name": ticket.event_name,
                "location": ticket.location,
                "time": ticket.time.isoformat() if ticket.time else None,
                "is_used": ticket.is_used,
            }
            return jsonify(ticket_data), 200

    def post(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400
        # Validate required fields
        if "event_name" not in data or "time" not in data:
            return jsonify({"error": "Missing required fields: event_name, time"}), 400
        try:
            # Parse time string to datetime
            data["time"] = datetime.fromisoformat(data["time"])
        except Exception:
            return jsonify({"error": "Invalid time format, expected ISO format"}), 400
        try:
            ticket = TicketService.create_ticket(data)
            ticket_data = {
                "id": ticket.id,
                "event_name": ticket.event_name,
                "location": ticket.location,
                "time": ticket.time.isoformat() if ticket.time else None,
                "is_used": ticket.is_used,
            }
            return jsonify(ticket_data), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def patch(self, ticket_id):
        ticket = TicketService.mark_ticket_as_used(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404
        ticket_data = {
            "id": ticket.id,
            "event_name": ticket.event_name,
            "location": ticket.location,
            "time": ticket.time.isoformat() if ticket.time else None,
            "is_used": ticket.is_used,
        }
        return jsonify(ticket_data), 200

    def delete(self, ticket_id):
        success = TicketService.delete_ticket(ticket_id)
        if not success:
            return jsonify({"error": "Ticket not found"}), 404
        return jsonify({"message": "Ticket deleted successfully"}), 200


ticket_view = TicketAPI.as_view("ticket_api")
ticket_bp.add_url_rule(
    "", defaults={"ticket_id": None}, view_func=ticket_view, methods=["GET"]
)
ticket_bp.add_url_rule("", view_func=ticket_view, methods=["POST"])
ticket_bp.add_url_rule(
    "/<int:ticket_id>", view_func=ticket_view, methods=["GET", "PATCH", "DELETE"]
)
