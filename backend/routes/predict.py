"""
Prediction route handler for FraudGuard.
POST /api/predict
"""

import datetime
from flask import Blueprint, request, jsonify
from backend.services.feature_service import validate_and_prepare_features
from backend.services.model_service import model_service
from backend.services.risk_service import generate_transaction_id, classify_risk, get_recommendation
from backend.database.database import insert_transaction

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True, silent=True)
        if payload is None:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON body provided."
            }), 400

        # Validate inputs and compute engineered features
        sanitized_data, feature_matrix = validate_and_prepare_features(payload)

        # Run model prediction
        prediction, fraud_prob_pct = model_service.predict(feature_matrix)

        # Determine risk classification and recommendation
        risk_level = classify_risk(fraud_prob_pct)
        recommendation = get_recommendation(prediction, risk_level, fraud_prob_pct)

        # Generate unique transaction ID and timestamp
        transaction_id = generate_transaction_id()
        created_at = datetime.datetime.now().isoformat()

        # Record to SQLite database
        db_record = {
            "transaction_id": transaction_id,
            "created_at": created_at,
            "step": sanitized_data["step"],
            "type": sanitized_data["type"],
            "amount": sanitized_data["amount"],
            "oldbalance_org": sanitized_data["oldbalance_org"],
            "newbalance_orig": sanitized_data["newbalance_orig"],
            "oldbalance_dest": sanitized_data["oldbalance_dest"],
            "newbalance_dest": sanitized_data["newbalance_dest"],
            "error_balance_orig": sanitized_data["error_balance_orig"],
            "error_balance_dest": sanitized_data["error_balance_dest"],
            "fraud_probability": fraud_prob_pct,
            "prediction": prediction,
            "risk_level": risk_level,
        }
        insert_transaction(db_record)

        # Return standardized response
        response_data = {
            "transaction_id": transaction_id,
            "transactionId": transaction_id,
            "prediction": prediction,
            "fraud_probability": fraud_prob_pct,
            "fraudProbability": fraud_prob_pct,
            "risk_level": risk_level,
            "riskLevel": risk_level,
            "recommendation": recommendation,
            "created_at": created_at,
            "timestamp": created_at,
        }

        return jsonify(response_data), 200

    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 400
    except Exception as e:
        print(f"[Predict Error]: {e}", flush=True)
        return jsonify({
            "status": "error",
            "message": "An internal server error occurred while processing prediction."
        }), 500
