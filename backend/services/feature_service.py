"""
Feature validation and engineering service for FraudGuard.
Conforms strictly to Stage 3C feature configuration and Stage 3D validation.
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

SUPPORTED_TYPES = {"CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"}

REQUIRED_FIELDS = [
    "step",
    "type",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
]

EXPECTED_FEATURE_NAMES = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "errorBalanceOrig",
    "errorBalanceDest",
    "type_CASH_IN",
    "type_CASH_OUT",
    "type_DEBIT",
    "type_PAYMENT",
    "type_TRANSFER",
]


def normalize_payload_keys(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes common variations of payload field names to the canonical schema.
    (e.g., oldBalanceOrg -> oldbalanceOrg, oldbalance_org -> oldbalanceOrg).
    """
    mapping = {
        "oldbalanceorg": "oldbalanceOrg",
        "oldbalance_org": "oldbalanceOrg",
        "oldbalance": "oldbalanceOrg",
        "newbalanceorig": "newbalanceOrig",
        "newbalance_orig": "newbalanceOrig",
        "newbalanceorg": "newbalanceOrig",
        "newbalance_org": "newbalanceOrig",
        "oldbalancedest": "oldbalanceDest",
        "oldbalance_dest": "oldbalanceDest",
        "newbalancedest": "newbalanceDest",
        "newbalance_dest": "newbalanceDest",
    }
    normalized = {}
    for k, v in payload.items():
        lowered = k.lower()
        canonical_key = mapping.get(lowered, k)
        normalized[canonical_key] = v
    return normalized


def validate_and_prepare_features(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], np.ndarray]:
    """
    Validates input fields, performs feature engineering, and constructs the
    exact 13-feature array for XGBoost model inference.

    Returns:
        (sanitized_dict, feature_matrix)
    Raises:
        ValueError on validation failure.
    """
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    data = normalize_payload_keys(payload)

    # 1. Check for missing required fields
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None:
            # Check if default step can be applied if omitted
            if field == "step":
                data["step"] = 1
            else:
                raise ValueError(f"Missing required field: '{field}'")

    # 2. Validate transaction type
    raw_type = str(data["type"]).strip().upper()
    if raw_type not in SUPPORTED_TYPES:
        raise ValueError(
            f"Invalid transaction type '{data['type']}'. Supported types are: {sorted(list(SUPPORTED_TYPES))}"
        )

    # 3. Validate numeric values
    try:
        step = int(data["step"])
        if step < 0:
            raise ValueError("Field 'step' must be a non-negative integer.")
    except (ValueError, TypeError):
        raise ValueError("Field 'step' must be a valid integer.")

    numeric_fields = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]
    parsed_nums = {}
    for field in numeric_fields:
        try:
            val = float(data[field])
            if np.isnan(val) or np.isinf(val):
                raise ValueError(f"Field '{field}' cannot be NaN or Infinite.")
            if val < 0.0:
                raise ValueError(f"Field '{field}' cannot be negative (got {val}).")
            parsed_nums[field] = val
        except (ValueError, TypeError) as e:
            if "cannot be negative" in str(e) or "cannot be NaN" in str(e):
                raise
            raise ValueError(f"Field '{field}' must be a valid numeric value.")

    amount = parsed_nums["amount"]
    oldbalanceOrg = parsed_nums["oldbalanceOrg"]
    newbalanceOrig = parsed_nums["newbalanceOrig"]
    oldbalanceDest = parsed_nums["oldbalanceDest"]
    newbalanceDest = parsed_nums["newbalanceDest"]

    # 4. Feature Engineering: Error balance calculations
    errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig
    errorBalanceDest = oldbalanceDest + amount - newbalanceDest

    # 5. One-hot encoding for transaction type
    type_cols = {
        "type_CASH_IN": 1.0 if raw_type == "CASH_IN" else 0.0,
        "type_CASH_OUT": 1.0 if raw_type == "CASH_OUT" else 0.0,
        "type_DEBIT": 1.0 if raw_type == "DEBIT" else 0.0,
        "type_PAYMENT": 1.0 if raw_type == "PAYMENT" else 0.0,
        "type_TRANSFER": 1.0 if raw_type == "TRANSFER" else 0.0,
    }

    # 6. Assemble feature vector
    feature_dict = {
        "step": float(step),
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "errorBalanceOrig": errorBalanceOrig,
        "errorBalanceDest": errorBalanceDest,
        **type_cols,
    }

    feature_values = [feature_dict[col] for col in EXPECTED_FEATURE_NAMES]
    feature_matrix = np.array([feature_values], dtype=np.float32)

    sanitized = {
        "step": step,
        "type": raw_type,
        "amount": amount,
        "oldbalance_org": oldbalanceOrg,
        "newbalance_orig": newbalanceOrig,
        "oldbalance_dest": oldbalanceDest,
        "newbalance_dest": newbalanceDest,
        "error_balance_orig": errorBalanceOrig,
        "error_balance_dest": errorBalanceDest,
    }

    return sanitized, feature_matrix
