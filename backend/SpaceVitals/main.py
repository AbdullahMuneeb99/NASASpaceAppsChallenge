# backend/spacevitals/main.py
from flask import Flask, jsonify
from flask_cors import CORS

# Import blueprints from the new package paths
from spacevitals.routes.communications_routes import comms_bp
from spacevitals.routes.sleep_routes import sleep_bp
from spacevitals.routes.medical_routes import medical_bp
from spacevitals.routes.power_routes import power_bp
from spacevitals.routes.logbook_routes import logbook_bp  # you'll create this file below

def create_app():
    app = Flask(__name__)

    # Enable CORS for the API so the Vite/React frontend can call it
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints under /api/...
    app.register_blueprint(comms_bp,    url_prefix="/api/comms")
    app.register_blueprint(sleep_bp,    url_prefix="/api/sleep")
    app.register_blueprint(medical_bp,  url_prefix="/api/medical")
    app.register_blueprint(power_bp,    url_prefix="/api/power")
    app.register_blueprint(logbook_bp,  url_prefix="/api/logbook")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app

if __name__ == "__main__":
    app = create_app()
    # Runs on http://127.0.0.1:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
