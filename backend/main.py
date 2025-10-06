from flask import Flask, jsonify
from flask_cors import CORS

from routes.logbook_routes import logbook_bp
from routes.sleep_routes import sleep_bp
from routes.medical_routes import medical_bp
from routes.communications_routes import comms_bp
from routes.power_routes import power_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(logbook_bp, url_prefix="/api/logbook")
    app.register_blueprint(sleep_bp, url_prefix="/api/sleep")
    app.register_blueprint(medical_bp, url_prefix="/api/medical")
    app.register_blueprint(comms_bp, url_prefix="/api/comms")
    app.register_blueprint(power_bp, url_prefix="/api/power")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
