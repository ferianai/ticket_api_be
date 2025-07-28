from flask import Blueprint, jsonify

index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET"])
def index():
    """Index route that returns a welcome message."""
    return jsonify({"message": "Welcome to the TiketQ API!"}), 200
