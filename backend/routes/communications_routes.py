# backend/space_vitals/routes/comms_routes.py

from flask import Blueprint, request, jsonify
from ..services.communications_service import CommunicationService

# Create a Blueprint — a Flask way to organize related routes
comms_bp = Blueprint('communications', __name__, url_prefix='/api/comms')

# Initialize the service (this could later be a shared instance)
comm_service = CommunicationService()


@comms_bp.route('/send', methods=['POST'])
def send_message():
    """
    Endpoint to send a new message.
    Expects JSON body with sender, recipient, channel, and content.
    """
    data = request.get_json()

    required_fields = ["sender", "recipient", "channel", "content"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        message = comm_service.send_message(
            sender=data["sender"],
            recipient=data["recipient"],
            channel=data["channel"],
            content=data["content"],
            msg_type=data.get("type", "text")
        )
        return jsonify({"message": "Message sent successfully", "data": message}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@comms_bp.route('/messages', methods=['GET'])
def get_messages():
    """
    Endpoint to retrieve all messages.
    Optional query parameter ?channel=crew|earth|station
    """
    channel = request.args.get("channel")
    messages = comm_service.get_messages(channel)
    return jsonify(messages), 200


@comms_bp.route('/latest', methods=['GET'])
def get_latest_message():
    """
    Endpoint to get the most recent message.
    Optional query parameter ?channel=crew|earth|station
    """
    channel = request.args.get("channel")
    latest = comm_service.get_latest_message(channel)
    if not latest:
        return jsonify({"message": "No messages found"}), 404
    return jsonify(latest), 200


@comms_bp.route('/clear', methods=['DELETE'])
def clear_messages():
    """
    Endpoint to clear all stored messages (useful for testing or resets)
    """
    comm_service.clear_messages()
    return jsonify({"message": "All messages cleared"}), 200
