"""
Dashboard metrics and statistics route handler for FraudGuard.
GET /api/dashboard
"""

from flask import Blueprint, jsonify
from backend.database.database import get_dashboard_stats
from backend.routes.transactions import format_transaction_item

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard():
    try:
        stats = get_dashboard_stats()

        # Format recent transactions
        recent_txs = [format_transaction_item(r) for r in stats["recent_transactions"]]

        response_data = {
            "total_transactions": stats["total_transactions"],
            "totalTransactions": stats["total_transactions"],
            "fraud_detected": stats["fraud_detected"],
            "fraudDetected": stats["fraud_detected"],
            "legitimate": stats["legitimate"],
            "fraud_rate": stats["fraud_rate"],
            "fraudRate": stats["fraud_rate"],
            "avg_fraud_prob": stats["avg_fraud_prob"],
            "avgFraudProb": stats["avg_fraud_prob"],
            "volumeTrendPercent": 5.2,
            "alertsTodayCount": stats["fraud_detected"],
            "risk_distribution": stats["risk_distribution"],
            "recent_transactions": recent_txs,
            "recentTransactions": recent_txs,
        }

        return jsonify(response_data), 200

    except Exception as e:
        print(f"[Dashboard Error]: {e}", flush=True)
        return jsonify({
            "status": "error",
            "message": "Failed to calculate dashboard statistics."
        }), 500
