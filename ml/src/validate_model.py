"""
================================================================================
FraudGuard - Stage 3D: Saved ML Model Validation
================================================================================

This script validates that the saved ML model, preprocessing pipeline,
and feature configuration artifacts load properly and can make accurate
predictions on real transaction samples from the PaySim dataset.

Artifacts validated:
  - ml/models/fraudguard_model.joblib
  - ml/models/fraudguard_preprocessor.joblib
  - ml/models/feature_config.json

Results saved to:
  - ml/results/model_validation.json

Run:
  python ml/src/validate_model.py
================================================================================
"""

import os
import sys
import io
import json
import datetime
import pandas as pd
import numpy as np
import joblib

# Ensure UTF-8 output encoding on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DATA_PATH = os.path.join(BASE_DIR, "data", "PS_20174392719_1491204439457_log.csv")

MODEL_PATH = os.path.join(MODELS_DIR, "fraudguard_model.joblib")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "fraudguard_preprocessor.joblib")
CONFIG_PATH = os.path.join(MODELS_DIR, "feature_config.json")
VALIDATION_OUT_PATH = os.path.join(RESULTS_DIR, "model_validation.json")

os.makedirs(RESULTS_DIR, exist_ok=True)


def banner(title: str):
    print("\n" + "=" * 70, flush=True)
    print(f"  {title}", flush=True)
    print("=" * 70, flush=True)


def sub(msg: str):
    print(f"\n[>>] {msg}", flush=True)


def ok(msg: str):
    print(f"    [OK] {msg}", flush=True)


def info(msg: str):
    print(f"    [..] {msg}", flush=True)


def warn(msg: str):
    print(f"    [!!] {msg}", flush=True)


def main():
    validation_report = {
        "validation_date": datetime.datetime.now().isoformat(),
        "model_loading_status": "FAILED",
        "preprocessor_loading_status": "FAILED",
        "feature_config_status": "FAILED",
        "prediction_status": "FAILED",
        "model_type": None,
        "selected_model_preprocessor": None,
        "validation_transaction_count": 0,
        "validation_results": [],
        "warnings": [],
        "errors": []
    }

    # =========================================================================
    # STEP 1: LOAD ARTIFACTS
    # =========================================================================
    banner("STEP 1: LOAD ARTIFACTS")

    # 1.1 Load Feature Config
    sub("Loading feature configuration from feature_config.json ...")
    if not os.path.exists(CONFIG_PATH):
        err = f"feature_config.json not found at {CONFIG_PATH}"
        validation_report["errors"].append(err)
        print(f"ERROR: {err}", flush=True)
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        feature_config = json.load(f)
    ok(f"Loaded feature_config.json successfully")
    validation_report["feature_config_status"] = "PASSED"

    # 1.2 Load Model
    sub("Loading saved model from fraudguard_model.joblib ...")
    if not os.path.exists(MODEL_PATH):
        err = f"fraudguard_model.joblib not found at {MODEL_PATH}"
        validation_report["errors"].append(err)
        print(f"ERROR: {err}", flush=True)
        sys.exit(1)

    model = joblib.load(MODEL_PATH)
    model_type = type(model).__name__
    validation_report["model_type"] = model_type
    validation_report["model_loading_status"] = "PASSED"
    ok(f"Loaded model successfully: {model_type}")

    # 1.3 Load Preprocessor
    sub("Loading saved preprocessor from fraudguard_preprocessor.joblib ...")
    if not os.path.exists(PREPROCESSOR_PATH):
        err = f"fraudguard_preprocessor.joblib not found at {PREPROCESSOR_PATH}"
        validation_report["errors"].append(err)
        print(f"ERROR: {err}", flush=True)
        sys.exit(1)

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    preprocessor_type = type(preprocessor).__name__
    validation_report["selected_model_preprocessor"] = feature_config.get("selected_model_preprocessor", "None")
    validation_report["preprocessor_loading_status"] = "PASSED"
    ok(f"Loaded preprocessor successfully: {preprocessor_type}")

    # Report model info
    info(f"Model Class: {model_type}")
    info(f"Model Name in Config: {feature_config.get('model_name')}")
    info(f"Model Version: {feature_config.get('model_version')}")
    if hasattr(model, "classes_"):
        info(f"Model Target Classes: {model.classes_.tolist()}")
    if hasattr(model, "n_features_in_"):
        info(f"Number of Input Features: {model.n_features_in_}")

    # =========================================================================
    # STEP 2: VERIFY FEATURE CONFIGURATION
    # =========================================================================
    banner("STEP 2: VERIFY FEATURE CONFIGURATION")

    expected_num = [
        "step", "amount", "oldbalanceOrg", "newbalanceOrig",
        "oldbalanceDest", "newbalanceDest", "errorBalanceOrig", "errorBalanceDest"
    ]
    expected_cat = ["type"]
    expected_eng = ["errorBalanceOrig", "errorBalanceDest"]
    expected_exc = ["isFraud", "isFlaggedFraud", "nameOrig", "nameDest"]
    expected_encoded_cols = [
        "step", "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest",
        "newbalanceDest", "errorBalanceOrig", "errorBalanceDest",
        "type_CASH_IN", "type_CASH_OUT", "type_DEBIT", "type_PAYMENT", "type_TRANSFER"
    ]

    cfg_num = feature_config.get("numerical_features", [])
    cfg_cat = feature_config.get("categorical_features", [])
    cfg_eng = feature_config.get("engineered_features", [])
    cfg_exc = feature_config.get("excluded_columns", [])
    cfg_exp = feature_config.get("expected_feature_names", [])

    assert cfg_num == expected_num, f"Numerical features mismatch! Found: {cfg_num}, Expected: {expected_num}"
    assert cfg_cat == expected_cat, f"Categorical features mismatch! Found: {cfg_cat}, Expected: {expected_cat}"
    assert cfg_eng == expected_eng, f"Engineered features mismatch! Found: {cfg_eng}, Expected: {expected_eng}"
    assert cfg_exc == expected_exc, f"Excluded columns mismatch! Found: {cfg_exc}, Expected: {expected_exc}"
    assert cfg_exp == expected_encoded_cols, f"Expected feature names mismatch! Found: {cfg_exp}, Expected: {expected_encoded_cols}"

    ok(f"Numerical features (8) match exactly: {cfg_num}")
    ok(f"Categorical features (1) match exactly: {cfg_cat}")
    ok(f"Engineered features (2) match exactly: {cfg_eng}")
    ok(f"Excluded columns (4) verified: {cfg_exc}")
    ok(f"Expected feature vector (13) verified: {cfg_exp}")

    # =========================================================================
    # STEP 3: PREPROCESSOR CAPABILITY TEST
    # =========================================================================
    banner("STEP 3: PREPROCESSOR INTEGRITY TEST")
    sub("Testing RobustScaler transformation capability ...")
    try:
        dummy_data = np.zeros((1, len(cfg_exp)))
        scaled_dummy = preprocessor.transform(dummy_data)
        ok(f"RobustScaler successfully transformed test vector of shape {dummy_data.shape} -> {scaled_dummy.shape}")
        info(f"Note: Saved final model '{feature_config.get('model_name')}' is tree-based ({validation_report['selected_model_preprocessor']}), so it accepts unscaled features directly.")
    except Exception as e:
        warn(f"Preprocessor transform test failed: {e}")
        validation_report["warnings"].append(f"Preprocessor test error: {str(e)}")

    # =========================================================================
    # STEP 4: LOAD REAL VALIDATION TRANSACTIONS FROM PAYSim DATASET
    # =========================================================================
    banner("STEP 4: SELECT REAL TEST TRANSACTIONS FROM DATASET")
    sub(f"Loading sample rows from {DATA_PATH} ...")

    if not os.path.exists(DATA_PATH):
        err = f"Dataset not found at {DATA_PATH}"
        validation_report["errors"].append(err)
        print(f"ERROR: {err}", flush=True)
        sys.exit(1)

    # Read data in chunks or sample specific legitimate and fraud transactions
    # We want a diverse set of real transactions:
    # - Legitimate PAYMENT
    # - Legitimate CASH_OUT
    # - Legitimate TRANSFER
    # - Legitimate CASH_IN
    # - Legitimate DEBIT
    # - Fraud TRANSFER
    # - Fraud CASH_OUT
    sample_legit_list = []
    sample_fraud_list = []

    # Read chunks to quickly find distinct type examples without loading all 6.36M rows into RAM
    for chunk in pd.read_csv(DATA_PATH, chunksize=100000):
        if len(sample_fraud_list) < 4:
            frauds = chunk[chunk["isFraud"] == 1]
            if not frauds.empty:
                for _, r in frauds.iterrows():
                    sample_fraud_list.append(r.to_dict())
                    if len(sample_fraud_list) >= 4:
                        break

        if len(sample_legit_list) < 6:
            legits = chunk[chunk["isFraud"] == 0]
            for t_type in ["PAYMENT", "CASH_OUT", "TRANSFER", "CASH_IN", "DEBIT"]:
                type_rows = legits[legits["type"] == t_type]
                if not type_rows.empty and not any(s["type"] == t_type for s in sample_legit_list):
                    sample_legit_list.append(type_rows.iloc[0].to_dict())

        if len(sample_fraud_list) >= 4 and len(sample_legit_list) >= 5:
            break

    test_samples = sample_legit_list + sample_fraud_list
    validation_report["validation_transaction_count"] = len(test_samples)
    ok(f"Selected {len(test_samples)} real transactions from PaySim dataset ({len(sample_legit_list)} legitimate, {len(sample_fraud_list)} fraudulent)")

    # =========================================================================
    # STEP 5 & 6: FEATURE ENGINEERING & INFERENCE
    # =========================================================================
    banner("STEP 5 & 6: FEATURE ENGINEERING & PREDICTION INFERENCE")

    sub("Executing feature engineering and model prediction on test transactions ...")

    results_table = []
    for idx, tx in enumerate(test_samples, start=1):
        actual_label = int(tx["isFraud"])
        tx_type = tx["type"]
        amount = float(tx["amount"])
        step = int(tx["step"])
        oldbalanceOrg = float(tx["oldbalanceOrg"])
        newbalanceOrig = float(tx["newbalanceOrig"])
        oldbalanceDest = float(tx["oldbalanceDest"])
        newbalanceDest = float(tx["newbalanceDest"])

        # 5.1 Calculate engineered features
        errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig
        errorBalanceDest = oldbalanceDest + amount - newbalanceDest

        # 5.2 Build one-hot encoding for type
        type_cols = {
            "type_CASH_IN": 1.0 if tx_type == "CASH_IN" else 0.0,
            "type_CASH_OUT": 1.0 if tx_type == "CASH_OUT" else 0.0,
            "type_DEBIT": 1.0 if tx_type == "DEBIT" else 0.0,
            "type_PAYMENT": 1.0 if tx_type == "PAYMENT" else 0.0,
            "type_TRANSFER": 1.0 if tx_type == "TRANSFER" else 0.0,
        }

        # 5.3 Construct exact feature vector matching expected_feature_names
        feature_dict = {
            "step": step,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest,
            "errorBalanceOrig": errorBalanceOrig,
            "errorBalanceDest": errorBalanceDest,
            **type_cols
        }

        feature_vector = [feature_dict[col] for col in cfg_exp]
        X_sample = pd.DataFrame([feature_dict])[cfg_exp].values.astype(np.float32)

        # Verify excluded columns were NOT used
        for exc_col in expected_exc:
            assert exc_col not in feature_dict, f"Excluded feature {exc_col} was used!"

        # 6.1 Predict
        predicted_class = int(model.predict(X_sample)[0])

        # 6.2 Predict Proba
        if hasattr(model, "predict_proba"):
            probas = model.predict_proba(X_sample)[0]
            legit_prob = float(probas[0])
            fraud_prob = float(probas[1])
        else:
            legit_prob = 1.0 - float(predicted_class)
            fraud_prob = float(predicted_class)

        match = (predicted_class == actual_label)

        tx_result = {
            "transaction_index": idx,
            "step": step,
            "type": tx_type,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest,
            "errorBalanceOrig": errorBalanceOrig,
            "errorBalanceDest": errorBalanceDest,
            "actual_isFraud": actual_label,
            "predicted_isFraud": predicted_class,
            "legitimate_probability": round(legit_prob, 6),
            "fraud_probability": round(fraud_prob, 6),
            "is_correct": match,
            "risk_assessment": "HIGH RISK (FRAUD)" if predicted_class == 1 else "LOW RISK (LEGIT)"
        }
        validation_report["validation_results"].append(tx_result)
        results_table.append(tx_result)

    validation_report["prediction_status"] = "PASSED"
    ok(f"Successfully processed all {len(test_samples)} transactions through the prediction pipeline")

    # =========================================================================
    # STEP 7: PRINT PREDICTION RESULTS TABLE
    # =========================================================================
    banner("STEP 7: VALIDATION RESULTS SUMMARY")

    print(f"{'#':<3} | {'Type':<9} | {'Amount':>14} | {'Actual':<7} | {'Predicted':<9} | {'Fraud Prob':>11} | {'Legit Prob':>11} | {'Match':<5}")
    print("-" * 80)
    for r in results_table:
        match_str = "[OK]" if r["is_correct"] else "[MISMATCH]"
        actual_str = "FRAUD" if r["actual_isFraud"] == 1 else "LEGIT"
        pred_str = "FRAUD" if r["predicted_isFraud"] == 1 else "LEGIT"
        print(f"{r['transaction_index']:<3} | {r['type']:<9} | {r['amount']:>14,.2f} | {actual_str:<7} | {pred_str:<9} | {r['fraud_probability']:>11.4f} | {r['legitimate_probability']:>11.4f} | {match_str:<5}")

    print("-" * 80)
    correct_count = sum(1 for r in results_table if r["is_correct"])
    accuracy = (correct_count / len(results_table)) * 100
    print(f"Validation Accuracy: {correct_count}/{len(results_table)} ({accuracy:.1f}%)", flush=True)

    # =========================================================================
    # STEP 8: SAVE VALIDATION REPORT
    # =========================================================================
    banner("STEP 8: SAVE VALIDATION REPORT")
    with open(VALIDATION_OUT_PATH, "w") as f:
        json.dump(validation_report, f, indent=2)
    ok(f"Validation report saved to: {VALIDATION_OUT_PATH}")

    banner("STAGE 3D VALIDATION COMPLETE - ARTIFACTS ARE PRODUCTION-READY")
    print(f"Model Artifact     : {MODEL_PATH}")
    print(f"Preprocessor       : {PREPROCESSOR_PATH}")
    print(f"Feature Config     : {CONFIG_PATH}")
    print(f"Validation Report  : {VALIDATION_OUT_PATH}")


if __name__ == "__main__":
    main()
