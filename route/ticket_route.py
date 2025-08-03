from flask import Blueprint, request, jsonify
from flask.views import MethodView
from services.ticket_service import TicketService
from datetime import datetime

ticket_bp = Blueprint("ticket", __name__, url_prefix="/tickets")


def serialize_ticket(ticket):
    return {
        "id": ticket.id,
        "event_name": ticket.event_name,
        "location": ticket.location,
        "time": ticket.time.isoformat() if ticket.time else None,
        "is_used": ticket.is_used,
    }


class TicketAPI(MethodView):
    def get(self, ticket_id=None):
        try:
            if ticket_id is None:
                tickets = TicketService.get_all_tickets()
                return jsonify([serialize_ticket(t) for t in tickets]), 200
            ticket = TicketService.get_ticket_by_id(ticket_id)
            return jsonify(serialize_ticket(ticket)), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    def post(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        if "event_name" not in data or "time" not in data:
            return (
                jsonify({"error": "Missing required fields: event_name or time"}),
                400,
            )

        try:
            data["time"] = datetime.fromisoformat(data["time"])
        except Exception:
            return jsonify({"error": "Invalid time format, expected ISO format"}), 400

        try:
            ticket = TicketService.create_ticket(data)
            return (
                jsonify(
                    {
                        "message": "Ticket created successfully",
                        "ticket": serialize_ticket(ticket),
                    }
                ),
                201,
            )
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    def patch(self, ticket_id):
        try:
            ticket = TicketService.mark_ticket_as_used(ticket_id)
            return jsonify(serialize_ticket(ticket)), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    def delete(self, ticket_id):
        try:
            TicketService.delete_ticket(ticket_id)
            return jsonify({"message": "Ticket deleted successfully"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404


# Register endpoints
ticket_view = TicketAPI.as_view("ticket_api")
ticket_bp.add_url_rule(
    "", defaults={"ticket_id": None}, view_func=ticket_view, methods=["GET"]
)
ticket_bp.add_url_rule("", view_func=ticket_view, methods=["POST"])
ticket_bp.add_url_rule(
    "/<int:ticket_id>", view_func=ticket_view, methods=["GET", "PATCH", "DELETE"]
)
