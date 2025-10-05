# backend/space_vitals/routes/life_support_routes.py

from flask import Blueprint, jsonify
from services.life_support_service import LifeSupportService

# Create Blueprint for Life Support module
life_support_bp = Blueprint("life_support", __name__, url_prefix="/life-support")

# Initialize the service
life_support_service = LifeSupportService()


@life_support_bp.route("/status", methods=["GET"])
def get_life_support_status():
    """
    Returns the current life support system status.
    """
    data = life_support_service.get_status()
    return jsonify({
        "status": "success",
        "data": data
    }), 200


@life_support_bp.route("/simulate", methods=["POST"])
def simulate_environment():
    """
    Simulates environmental fluctuations (oxygen, pressure, water).
    """
    updated = life_support_service.simulate_environment()
    return jsonify({
        "status": "success",
        "message": "Environmental data updated.",
        "data": updated
    }), 200


@life_support_bp.route("/refill-water", methods=["POST"])
def refill_water():
    """
    Refills portable water reserves.
    """
    result = life_support_service.refill_water()
    return jsonify({
        "status": "success",
        "data": result
    }), 200


@life_support_bp.route("/repair-leak", methods=["POST"])
def repair_leak():
    """
    Repairs detected leaks (if any).
    """
    result = life_support_service.repair_leak()
    return jsonify({
        "status": "success",
        "data": result
    }), 200

