"""
ML Model Management and Inference Service.
Loads the trained XGBoost model and feature configuration once at startup.
"""

import os
import json
import joblib
import numpy as np
from typing import Dict, Any, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ML_MODELS_DIR = os.path.join(PROJECT_ROOT, "ml", "models")

MODEL_PATH = os.path.join(ML_MODELS_DIR, "fraudguard_model.joblib")
PREPROCESSOR_PATH = os.path.join(ML_MODELS_DIR, "fraudguard_preprocessor.joblib")
CONFIG_PATH = os.path.join(ML_MODELS_DIR, "feature_config.json")


class ModelService:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_config = None
        self.is_loaded = False
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """Load saved artifacts into memory."""
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}")
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Feature config not found at {CONFIG_PATH}")

        # Load feature config
        with open(CONFIG_PATH, "r") as f:
            self.feature_config = json.load(f)

        # Load XGBoost model
        self.model = joblib.load(MODEL_PATH)

        # Load preprocessor if present
        if os.path.exists(PREPROCESSOR_PATH):
            self.preprocessor = joblib.load(PREPROCESSOR_PATH)
        else:
            self.preprocessor = None

        self.is_loaded = True
        print(f"[ModelService] Successfully loaded XGBoost model ({type(self.model).__name__}) and configuration.")

    def check_health(self) -> bool:
        """Check if model and configuration are loaded and ready."""
        return self.is_loaded and self.model is not None

    def predict(self, feature_matrix: np.ndarray) -> Tuple[str, float]:
        """
        Run inference on the 13-feature matrix.

        Returns:
            Tuple of (prediction_label, fraud_probability_pct)
            prediction_label: "FRAUD" or "LEGITIMATE"
            fraud_probability_pct: float in [0.0, 100.0]
        """
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Model is not loaded.")

        # Run predict_proba for precise probabilities
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(feature_matrix)[0]
            # Binary classification: index 0 = Legit (0), index 1 = Fraud (1)
            fraud_prob = float(probabilities[1])
        else:
            pred = int(self.model.predict(feature_matrix)[0])
            fraud_prob = float(pred)

        # Run class prediction
        pred_class = int(self.model.predict(feature_matrix)[0])
        prediction_label = "FRAUD" if pred_class == 1 else "LEGITIMATE"

        fraud_probability_pct = round(fraud_prob * 100.0, 2)

        return prediction_label, fraud_probability_pct


# Global singleton instance loaded at module import time
model_service = ModelService()
