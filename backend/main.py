# backend/main.py

from flask import Flask, jsonify
from flask_cors import CORS

# Import route blueprints
from routes.logbook_routes import logbook_bp
from routes.sleep_routes import sleep_bp
from routes.medical_routes import medical_bp
from routes.communications_routes import comms_bp
from routes.power_routes import power_bp
from routes.life_support_routes import life_support_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register all route blueprints
    app.register_blueprint(logbook_bp, url_prefix="/api/logbook")
    app.register_blueprint(sleep_bp, url_prefix="/api/sleep")
    app.register_blueprint(medical_bp, url_prefix="/api/medical")
    app.register_blueprint(comms_bp, url_prefix="/api/comms")
    app.register_blueprint(power_bp, url_prefix="/api/power")
    app.register_blueprint(life_support_bp, url_prefix="/api/life-support")

    # Simple health check route
    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)

