"""
Automated Test Suite for FraudGuard Flask Backend.
Tests:
  - GET /api/health
  - POST /api/predict (real PaySim legitimate & fraud samples)
  - POST /api/predict validation error handling
  - GET /api/transactions (pagination & filtering)
  - GET /api/dashboard (dynamic SQLite aggregation)
"""

import sys
import os
import json

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app import create_app
from backend.database.database import get_connection


def run_tests():
    print("=" * 70)
    print("  FRAUDGUARD STAGE 4 BACKEND VERIFICATION SUITE")
    print("=" * 70)

    app = create_app()
    client = app.test_client()

    # -------------------------------------------------------------------------
    # TEST 1: HEALTH CHECK
    # -------------------------------------------------------------------------
    print("\n[TEST 1] GET /api/health ...")
    resp = client.get("/api/health")
    assert resp.status_code == 200, f"Health check failed with {resp.status_code}"
    health_data = resp.get_json()
    print("  Response:", json.dumps(health_data, indent=2))
    assert health_data.get("status") == "ok", "Status is not 'ok'"
    assert health_data.get("model_loaded") is True, "Model is not loaded"
    assert health_data.get("database_connected") is True, "Database is not connected"
    print("  [PASS] Health check verified.")

    # -------------------------------------------------------------------------
    # TEST 2: PREDICT LEGITIMATE TRANSACTION (PaySim real data)
    # -------------------------------------------------------------------------
    print("\n[TEST 2] POST /api/predict (Legitimate PAYMENT) ...")
    legit_sample = {
        "step": 1,
        "type": "PAYMENT",
        "amount": 9839.64,
        "oldbalanceOrg": 170136.0,
        "newbalanceOrig": 160296.36,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
    }
    resp = client.post("/api/predict", json=legit_sample)
    assert resp.status_code == 200, f"Predict failed: {resp.data.decode()}"
    legit_res = resp.get_json()
    print("  Response:", json.dumps(legit_res, indent=2))
    assert legit_res["prediction"] == "LEGITIMATE", f"Expected LEGITIMATE, got {legit_res['prediction']}"
    assert legit_res["risk_level"] == "LOW", f"Expected LOW risk, got {legit_res['risk_level']}"
    assert legit_res["fraud_probability"] <= 30.0, f"Expected low prob, got {legit_res['fraud_probability']}"
    assert legit_res["transaction_id"].startswith("FG-"), f"Invalid tx ID format: {legit_res['transaction_id']}"
    print("  [PASS] Legitimate transaction prediction verified.")

    # -------------------------------------------------------------------------
    # TEST 3: PREDICT FRAUDULENT TRANSACTION (PaySim real data)
    # -------------------------------------------------------------------------
    print("\n[TEST 3] POST /api/predict (Fraudulent TRANSFER) ...")
    fraud_sample = {
        "step": 1,
        "type": "TRANSFER",
        "amount": 181.0,
        "oldbalanceOrg": 181.0,
        "newbalanceOrig": 0.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
    }
    resp = client.post("/api/predict", json=fraud_sample)
    assert resp.status_code == 200, f"Predict failed: {resp.data.decode()}"
    fraud_res = resp.get_json()
    print("  Response:", json.dumps(fraud_res, indent=2))
    assert fraud_res["prediction"] == "FRAUD", f"Expected FRAUD, got {fraud_res['prediction']}"
    assert fraud_res["risk_level"] == "HIGH", f"Expected HIGH risk, got {fraud_res['risk_level']}"
    assert fraud_res["fraud_probability"] >= 70.0, f"Expected high prob, got {fraud_res['fraud_probability']}"
    print("  [PASS] Fraudulent transaction prediction verified.")

    # -------------------------------------------------------------------------
    # TEST 4: PREDICTION VALIDATION (Missing fields, negative amount, bad type)
    # -------------------------------------------------------------------------
    print("\n[TEST 4] POST /api/predict (Validation handling) ...")
    # 4a: Invalid Type
    bad_type_sample = {
        "step": 1,
        "type": "BITCOIN_TRANSFER",
        "amount": 100.0,
        "oldbalanceOrg": 500.0,
        "newbalanceOrig": 400.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 100.0,
    }
    resp = client.post("/api/predict", json=bad_type_sample)
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    print("  Bad type rejected correctly:", resp.get_json().get("message"))

    # 4b: Negative amount
    negative_amt_sample = {
        "step": 1,
        "type": "TRANSFER",
        "amount": -50.0,
        "oldbalanceOrg": 500.0,
        "newbalanceOrig": 400.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 100.0,
    }
    resp = client.post("/api/predict", json=negative_amt_sample)
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    print("  Negative amount rejected correctly:", resp.get_json().get("message"))

    # 4c: Missing required fields
    missing_field_sample = {
        "type": "TRANSFER",
        "amount": 500.0,
    }
    resp = client.post("/api/predict", json=missing_field_sample)
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    print("  Missing fields rejected correctly:", resp.get_json().get("message"))
    print("  [PASS] Validation error handling verified.")

    # -------------------------------------------------------------------------
    # TEST 5: GET /api/transactions (Listing, Pagination, Filtering)
    # -------------------------------------------------------------------------
    print("\n[TEST 5] GET /api/transactions ...")
    resp = client.get("/api/transactions?page=1&limit=10")
    assert resp.status_code == 200, f"Transactions list failed: {resp.data.decode()}"
    tx_list_data = resp.get_json()
    print(f"  Total transactions in DB: {tx_list_data.get('total')}")
    print(f"  Retrieved count: {len(tx_list_data.get('transactions', []))}")
    assert tx_list_data["total"] >= 2, "Expected at least 2 transactions in DB"

    # Verify filtering by type
    resp_filter = client.get("/api/transactions?type=TRANSFER")
    assert resp_filter.status_code == 200
    transfer_data = resp_filter.get_json()
    for tx in transfer_data.get("transactions", []):
        assert tx["type"] == "TRANSFER", f"Filter mismatch: {tx['type']}"
    print("  [PASS] Transactions list and filtering verified.")

    # -------------------------------------------------------------------------
    # TEST 6: GET /api/dashboard (SQLite stats aggregation)
    # -------------------------------------------------------------------------
    print("\n[TEST 6] GET /api/dashboard ...")
    resp = client.get("/api/dashboard")
    assert resp.status_code == 200, f"Dashboard failed: {resp.data.decode()}"
    dash_data = resp.get_json()
    print("  Dashboard Stats:", json.dumps({k: v for k, v in dash_data.items() if k != "recent_transactions"}, indent=2))
    assert dash_data["total_transactions"] >= 2
    assert dash_data["fraud_detected"] >= 1
    assert dash_data["legitimate"] >= 1
    assert dash_data["fraud_rate"] > 0.0
    print("  [PASS] Dashboard metrics aggregation verified.")

    print("\n" + "=" * 70)
    print("  ALL STAGE 4 BACKEND TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
