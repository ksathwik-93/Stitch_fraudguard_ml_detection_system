"""
FraudGuard Flask REST API Server.
Main entrypoint for ML inference, SQLite database, and dashboard services.
"""

import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add workspace directory to python path if not present
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from backend.database.database import init_db, check_db_health
from backend.services.model_service import model_service
from backend.routes.predict import predict_bp
from backend.routes.transactions import transactions_bp
from backend.routes.dashboard import dashboard_bp


def create_app() -> Flask:
    """Application factory for FraudGuard backend."""
    app = Flask(__name__)

    # Configure CORS for React Vite development environments (supporting any local port, e.g. 3000, 3001, 5173)
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    r"^https?://localhost(:\d+)?$",
                    r"^https?://127\.0\.0\.1(:\d+)?$",
                ],
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
            }
        },
        supports_credentials=True,
    )

    # Initialize SQLite database
    init_db()

    # Register Blueprints under /api prefix
    app.register_blueprint(predict_bp, url_prefix="/api")
    app.register_blueprint(transactions_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    # =========================================================================
    # HEALTH CHECK ENDPOINT
    # =========================================================================
    @app.route("/api/health", methods=["GET"])
    def health_check():
        model_loaded = model_service.check_health()
        db_connected = check_db_health()
        status = "ok" if (model_loaded and db_connected) else "degraded"

        return jsonify({
            "status": status,
            "model_loaded": model_loaded,
            "database_connected": db_connected,
            "model_type": type(model_service.model).__name__ if model_service.model else None,
            "model_name": model_service.feature_config.get("model_name", "XGBoost") if model_service.feature_config else None,
        }), 200

    # =========================================================================
    # CUSTOM ERROR HANDLERS (Standard JSON Responses)
    # =========================================================================
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": "error",
            "code": 400,
            "message": getattr(error, "description", "Bad Request")
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "The requested API endpoint was not found on this server."
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        print(f"[Internal Server Error]: {error}", flush=True)
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "An internal server error occurred. Please check backend logs."
        }), 500

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Starting FraudGuard Flask API on http://127.0.0.1:{port} ...", flush=True)
    app.run(host="127.0.0.1", port=port, debug=False)
