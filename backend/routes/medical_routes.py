# backend/space_vitals/routes/medical_routes.py

from flask import Blueprint, jsonify
from services.medical_service import MedicalService

# Create a Blueprint for the medical module
medical_bp = Blueprint("medical", __name__, url_prefix="/medical")

# Initialize service
medical_service = MedicalService()


@medical_bp.route("/vitals", methods=["GET"])
def get_vitals():
    """
    Returns the astronaut's latest vital sign readings.
    """
    vitals = medical_service.get_vitals()
    return jsonify({
        "status": "success",
        "data": vitals
    }), 200


@medical_bp.route("/health-status", methods=["GET"])
def get_health_status():
    """
    Returns a health summary, including vitals and assessment.
    Simulates small fluctuations in vitals before responding.
    """
    medical_service.simulate_vital_changes()
    health_data = medical_service.get_health_status()
    return jsonify({
        "status": "success",
        "data": health_data
    }), 200


@medical_bp.route("/first-aid", methods=["GET"])
def get_first_aid_protocol():
    """
    Returns the first-aid protocol text for astronauts.
    """
    protocol = medical_service.get_first_aid_protocol()
    return jsonify({
        "status": "success",
        "data": protocol
    }), 200


# (Optional) Debug route to refresh vitals manually
@medical_bp.route("/simulate", methods=["POST"])
def simulate_vitals():
    """
    Forces a vitals update (useful for testing or dashboards).
    """
    updated = medical_service.simulate_vital_changes()
    return jsonify({
        "status": "success",
        "message": "Vitals simulated successfully.",
        "data": updated
    }), 200
