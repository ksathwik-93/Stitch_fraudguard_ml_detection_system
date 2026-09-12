"""
Live verification script querying running servers.
"""

import urllib.request
import json


def test_endpoint(url, data=None):
    req = urllib.request.Request(
        url,
        headers={"Content-Type": "application/json"} if data else {},
    )
    body = json.dumps(data).encode("utf-8") if data else None
    with urllib.request.urlopen(req, data=body) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def main():
    print("==================================================")
    print("  FRAUDGUARD LIVE INTEGRATION VERIFICATION")
    print("==================================================")

    # 1. Health Check
    print("\n[1] GET http://127.0.0.1:5000/api/health")
    status, res = test_endpoint("http://127.0.0.1:5000/api/health")
    print(f"Status: {status}")
    print("Payload:", json.dumps(res, indent=2))
    assert res["status"] == "ok"
    assert res["model_loaded"] is True
    assert res["database_connected"] is True

    # 2. Predict Fraud
    print("\n[2] POST http://127.0.0.1:5000/api/predict (PaySim Real Fraud)")
    fraud_sample = {
        "step": 1,
        "type": "TRANSFER",
        "amount": 181.0,
        "oldbalanceOrg": 181.0,
        "newbalanceOrig": 0.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
    }
    status, res = test_endpoint("http://127.0.0.1:5000/api/predict", fraud_sample)
    print(f"Status: {status}")
    print("Payload:", json.dumps(res, indent=2))
    assert res["prediction"] == "FRAUD"
    assert res["risk_level"] == "HIGH"
    assert res["fraud_probability"] == 100.0
    fraud_tx_id = res["transaction_id"]

    # 3. Predict Legit
    print("\n[3] POST http://127.0.0.1:5000/api/predict (PaySim Real Legit)")
    legit_sample = {
        "step": 1,
        "type": "PAYMENT",
        "amount": 9839.64,
        "oldbalanceOrg": 170136.0,
        "newbalanceOrig": 160296.36,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
    }
    status, res = test_endpoint("http://127.0.0.1:5000/api/predict", legit_sample)
    print(f"Status: {status}")
    print("Payload:", json.dumps(res, indent=2))
    assert res["prediction"] == "LEGITIMATE"
    assert res["risk_level"] == "LOW"
    assert res["fraud_probability"] == 0.0
    legit_tx_id = res["transaction_id"]

    # 4. Get Transactions
    print("\n[4] GET http://127.0.0.1:5000/api/transactions")
    status, res = test_endpoint("http://127.0.0.1:5000/api/transactions?limit=5")
    print(f"Status: {status}")
    print(f"Total Transactions in DB: {res.get('total')}")
    print(f"Page: {res.get('page')}, Limit: {res.get('limit')}, Pages: {res.get('pages')}")
    print(f"Returned Items: {len(res.get('transactions', []))}")
    ids = [t["id"] for t in res.get("transactions", [])]
    print(f"Latest Transaction IDs: {ids}")
    assert fraud_tx_id in ids or legit_tx_id in ids

    # 5. Get Dashboard Stats
    print("\n[5] GET http://127.0.0.1:5000/api/dashboard")
    status, res = test_endpoint("http://127.0.0.1:5000/api/dashboard")
    print(f"Status: {status}")
    print("Dashboard Stats:", json.dumps({k: v for k, v in res.items() if k != "recent_transactions" and k != "recentTransactions"}, indent=2))
    assert res["totalTransactions"] >= 2
    assert res["fraudDetected"] >= 1
    assert res["legitimate"] >= 1
    assert res["fraudRate"] > 0.0

    # 6. Test Vite Frontend HTTP Server
    print("\n[6] GET http://localhost:3000/ (Vite Dev Server)")
    with urllib.request.urlopen("http://localhost:3000/") as resp:
        html_code = resp.read().decode("utf-8")
        print(f"Status: {resp.status}, HTML Length: {len(html_code)} bytes")
        assert "FraudGuard" in html_code or "<div id=\"root\">" in html_code

    print("\n==================================================")
    print("  ALL LIVE INTEGRATION TESTS PASSED (100%)")
    print("==================================================")


if __name__ == "__main__":
    main()
