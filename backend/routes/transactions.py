"""
Transaction History route handler for FraudGuard.
GET /api/transactions
"""

from flask import Blueprint, request, jsonify
from backend.database.database import get_transactions

transactions_bp = Blueprint("transactions", __name__)


def format_transaction_item(row: dict) -> dict:
    """Format SQLite row for frontend consumption."""
    # Determine UI status
    pred = str(row.get("prediction", "")).upper()
    risk = str(row.get("risk_level", "")).upper()

    if pred == "FRAUD" or risk == "HIGH":
        status = "BLOCKED"
    elif risk == "MEDIUM":
        status = "REVIEW"
    else:
        status = "CLEARED"

    created_at = row.get("created_at", "")
    return {
        "id": row.get("transaction_id", f"TX-{row.get('id', 0)}"),
        "transaction_id": row.get("transaction_id", ""),
        "db_id": row.get("id"),
        "created_at": created_at,
        "dateTime": created_at,
        "step": row.get("step"),
        "type": row.get("type"),
        "amount": row.get("amount"),
        "oldbalance_org": row.get("oldbalance_org"),
        "oldBalanceOrg": row.get("oldbalance_org"),
        "newbalance_orig": row.get("newbalance_orig"),
        "newBalanceOrg": row.get("newbalance_orig"),
        "oldbalance_dest": row.get("oldbalance_dest"),
        "oldBalanceDest": row.get("oldbalance_dest"),
        "newbalance_dest": row.get("newbalance_dest"),
        "newBalanceDest": row.get("newbalance_dest"),
        "error_balance_orig": row.get("error_balance_orig"),
        "error_balance_dest": row.get("error_balance_dest"),
        "fraud_probability": row.get("fraud_probability"),
        "fraudProbability": row.get("fraud_probability"),
        "prediction": row.get("prediction"),
        "risk_level": row.get("risk_level"),
        "riskLevel": row.get("risk_level"),
        "status": status,
    }


@transactions_bp.route("/transactions", methods=["GET"])
def list_transactions():
    try:
        page = request.args.get("page", default=1, type=int)
        limit = request.args.get("limit", default=20, type=int)
        search = request.args.get("search", default=None, type=str)
        tx_type = request.args.get("type", default=None, type=str)
        risk_level = request.args.get("risk_level", default=None, type=str)
        prediction = request.args.get("prediction", default=None, type=str)

        rows, total_count, total_pages = get_transactions(
            page=page,
            limit=limit,
            search=search,
            tx_type=tx_type,
            risk_level=risk_level,
            prediction=prediction,
        )

        formatted_transactions = [format_transaction_item(r) for r in rows]

        return jsonify({
            "transactions": formatted_transactions,
            "page": page,
            "limit": limit,
            "total": total_count,
            "pages": total_pages,
        }), 200

    except Exception as e:
        print(f"[Transactions List Error]: {e}", flush=True)
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve transactions."
        }), 500
