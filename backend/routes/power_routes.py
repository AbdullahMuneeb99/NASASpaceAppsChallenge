# backend/space_vitals/routes/power_routes.py

from flask import Blueprint, jsonify
from services.power_service import PowerService

# Create Blueprint for Power module
power_bp = Blueprint("power", __name__, url_prefix="/power")

# Initialize PowerService
power_service = PowerService()


@power_bp.route("/status", methods=["GET"])
def get_power_status():
    """
    Returns current power status and maintenance alerts.
    """
    status = power_service.get_power_status()
    return jsonify({
        "status": "success",
        "data": status
    }), 200


@power_bp.route("/simulate", methods=["POST"])
def simulate_power_usage():
    """
    Simulates power usage and returns updated status.
    """
    updated = power_service.simulate_power_usage()
    return jsonify({
        "status": "success",
        "message": "Power usage simulated.",
        "data": updated
    }), 200


@power_bp.route("/maintain", methods=["POST"])
def perform_maintenance():
    """
    Performs maintenance on power systems and resets values.
    """
    result = power_service.perform_maintenance()
    return jsonify({
        "status": "success",
        "data": result
    }), 200
