"""
Risk classification, recommendation, and transaction ID generation service for FraudGuard.

Note:
The risk tiers (LOW: 0-30%, MEDIUM: 31-70%, HIGH: 71-100%) represent an application-level
heuristic risk categorization designed for demonstration and decision-support, and not a
legally or financially certified threshold.
"""

import datetime
import uuid
import threading

_counter_lock = threading.Lock()
_counter = 0


def generate_transaction_id() -> str:
    """
    Generate a unique, human-readable transaction identifier.
    Format: FG-YYYYMMDD-XXXXXX (e.g. FG-20260820-000001)
    """
    global _counter
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")

    with _counter_lock:
        _counter += 1
        cnt = _counter

    # Incorporate short random suffix to guarantee cross-process uniqueness
    rand_suffix = uuid.uuid4().hex[:4].upper()
    return f"FG-{date_str}-{cnt:04d}{rand_suffix}"


def classify_risk(fraud_probability_pct: float) -> str:
    """
    Classify fraud risk level based on model fraud probability percentage (0-100).
    - 0% to 30%: LOW
    - 31% to 70%: MEDIUM
    - 71% to 100%: HIGH
    """
    if fraud_probability_pct <= 30.0:
        return "LOW"
    elif fraud_probability_pct <= 70.0:
        return "MEDIUM"
    else:
        return "HIGH"


def get_recommendation(prediction: str, risk_level: str, fraud_probability_pct: float) -> str:
    """
    Provide risk-mitigation recommendation based on prediction and risk level.
    """
    if prediction == "FRAUD" or risk_level == "HIGH":
        return (
            f"High fraud risk detected ({fraud_probability_pct:.2f}%). Transaction parameters "
            "strongly match anomaly / account draining patterns. Recommended Action: Block transaction "
            "and alert fraud investigations team."
        )
    elif risk_level == "MEDIUM":
        return (
            f"Moderate fraud risk detected ({fraud_probability_pct:.2f}%). Transaction indicators "
            "deviate from standard baselines. Recommended Action: Route for manual review or step-up MFA."
        )
    else:
        return (
            f"Low fraud risk detected ({fraud_probability_pct:.2f}%). Transaction indicators appear "
            "within normal statistical bounds. Recommended Action: Approve transaction automatically."
        )
