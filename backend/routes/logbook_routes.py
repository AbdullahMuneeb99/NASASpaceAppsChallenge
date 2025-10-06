# backend/routes/logbook_routes.py

from flask import Blueprint, request, jsonify
from services.logbook_service import LogbookService

# Create Blueprint for Logbook module
logbook_bp = Blueprint("logbook", __name__, url_prefix="/logbook")

# Initialize the service
logbook_service = LogbookService()


@logbook_bp.route("/", methods=["POST"])
def add_log():
    """
    Create a new log entry.
    Expects JSON body with title, content, and author.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Invalid or missing JSON body"}), 400

    required_fields = ["title", "content", "author"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        new_log = logbook_service.create_log(
            title=data["title"],
            content=data["content"],
            author=data["author"]
        )
        return jsonify({
            "status": "success",
            "message": "Log entry created",
            "data": new_log
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@logbook_bp.route("/", methods=["GET"])
def list_logs():
    """
    Retrieve a list of logs with optional pagination (?skip=0&limit=50).
    """
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 50))

    try:
        logs = logbook_service.get_logs(skip=skip, limit=limit)
        return jsonify({"status": "success", "data": logs}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@logbook_bp.route("/<int:log_id>", methods=["GET"])
def get_log(log_id):
    """
    Retrieve a specific log entry by ID.
    """
    log = logbook_service.get_log(log_id)
    if not log:
        return jsonify({"status": "error", "message": "Log not found"}), 404
    return jsonify({"status": "success", "data": log}), 200


@logbook_bp.route("/<int:log_id>", methods=["PATCH"])
def update_log(log_id):
    """
    Update an existing log entry.
    Accepts partial JSON: title, content, author.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Invalid or missing JSON body"}), 400

    updated_log = logbook_service.update_log(log_id, **data)
    if not updated_log:
        return jsonify({"status": "error", "message": "Log not found"}), 404

    return jsonify({
        "status": "success",
        "message": "Log updated",
        "data": updated_log
    }), 200


@logbook_bp.route("/<int:log_id>", methods=["DELETE"])
def delete_log(log_id):
    """
    Delete a log entry by ID.
    """
    deleted = logbook_service.delete_log(log_id)
    if not deleted:
        return jsonify({"status": "error", "message": "Log not found"}), 404

    return jsonify({"status": "success", "message": "Log deleted"}), 200

