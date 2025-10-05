from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import route blueprints from the modules
from spacevitals.routes.comms_routes import comms_bp
from spacevitals.routes.life_support_routes import life_support_bp
from spacevitals.routes.medical_routes import medical_bp
from spacevitals.routes.power_routes import power_bp

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Enable CORS (so frontend React app can communicate with backend)
    CORS(app)

    # Load configurations
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "spacevitals-secret-key")

    # Register blueprints for each module
    app.register_blueprint(comms_bp, url_prefix="/api/comms")
    app.register_blueprint(life_support_bp, url_prefix="/api/life-support")
    app.register_blueprint(medical_bp, url_prefix="/api/medical")
    app.register_blueprint(power_bp, url_prefix="/api/power")

    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "SpaceVitals backend is operational 🚀"}), 200

    return app


if __name__ == "__main__":
    app = create_app()

    # Run server (in development mode)
    app.run(host="0.0.0.0", port=5000, debug=True)
