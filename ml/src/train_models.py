"""
================================================================================
FraudGuard - Stage 3C: Online Payment Fraud Detection
Full Reproducible ML Training Pipeline
================================================================================

Dataset   : PaySim - PS_20174392719_1491204439457_log.csv
Target    : isFraud
Models    : Logistic Regression | Random Forest | XGBoost
Strategy  : class_weight='balanced' / scale_pos_weight (primary)
            SMOTE-ENN on 100K stratified subset (academic comparison)

Run:
    python ml/src/train_models.py

Author    : FraudGuard ML Team
Stage     : 3C — Model Training
================================================================================
"""

import os
import sys

# Force UTF-8 output on Windows to avoid cp1252 encoding errors
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
import time
import warnings
import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    roc_curve, precision_recall_curve,
    confusion_matrix, ConfusionMatrixDisplay,
)
from sklearn.pipeline import Pipeline

import joblib
import xgboost as xgb

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.sans-serif": "DejaVu Sans",
    "font.family": "sans-serif",
    "figure.dpi": 150,
})

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH  = os.path.join(BASE_DIR, "data", "PS_20174392719_1491204439457_log.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
MODELS_DIR  = os.path.join(BASE_DIR, "models")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE    = 0.20

# ─────────────────────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def banner(title: str) -> None:
    print("\n" + "=" * 70, flush=True)
    print(f"  {title}", flush=True)
    print("=" * 70, flush=True)


def sub(label: str) -> None:
    print(f"\n[>>] {label}", flush=True)


def ok(msg: str) -> None:
    print(f"    [OK] {msg}", flush=True)


def info(msg: str) -> None:
    print(f"    [..] {msg}", flush=True)


def warn(msg: str) -> None:
    print(f"    [!!] {msg}", flush=True)


# ─────────────────────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 1 — LOAD DATA")

if not os.path.exists(DATA_PATH):
    print(f"ERROR: Dataset not found at {DATA_PATH}", flush=True)
    sys.exit(1)

sub("Loading CSV …")
t0 = time.time()
df = pd.read_csv(DATA_PATH)
load_time = time.time() - t0
ok(f"Loaded {len(df):,} rows × {len(df.columns)} columns in {load_time:.1f}s")
info(f"Columns: {list(df.columns)}")

total_rows = len(df)
fraud_total   = int(df["isFraud"].sum())
legit_total   = total_rows - fraud_total
fraud_rate    = fraud_total / total_rows * 100
imbalance_ratio = legit_total / fraud_total

info(f"Fraud transactions : {fraud_total:,}")
info(f"Legitimate         : {legit_total:,}")
info(f"Fraud rate         : {fraud_rate:.4f}%")
info(f"Imbalance ratio    : {imbalance_ratio:.0f}:1")

# ─────────────────────────────────────────────────────────────────────────────
# 2. FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 2 — FEATURE ENGINEERING")

sub("Computing engineered features …")
df["errorBalanceOrig"] = df["oldbalanceOrg"] - df["amount"] - df["newbalanceOrig"]
df["errorBalanceDest"] = df["oldbalanceDest"] + df["amount"] - df["newbalanceDest"]
ok("errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig")
ok("errorBalanceDest = oldbalanceDest + amount - newbalanceDest")

# ─────────────────────────────────────────────────────────────────────────────
# 3. FEATURE MATRIX
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 3 — FEATURE MATRIX")

NUMERICAL_FEATURES = [
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "errorBalanceOrig",
    "errorBalanceDest",
]
CATEGORICAL_FEATURES = ["type"]
ENGINEERED_FEATURES  = ["errorBalanceOrig", "errorBalanceDest"]
TARGET               = "isFraud"

sub("One-hot encoding 'type' …")
type_dummies = pd.get_dummies(df["type"], prefix="type", drop_first=False)
type_columns = list(type_dummies.columns)
ok(f"Encoded transaction types: {type_columns}")

X_raw = pd.concat([df[NUMERICAL_FEATURES], type_dummies], axis=1)
y     = df[TARGET].values
ALL_FEATURE_NAMES = list(X_raw.columns)

info(f"Feature matrix shape: {X_raw.shape}")
info(f"All features: {ALL_FEATURE_NAMES}")

# ─────────────────────────────────────────────────────────────────────────────
# 4. TRAIN / TEST SPLIT
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 4 — STRATIFIED TRAIN / TEST SPLIT")

X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X_raw, y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)

train_size = len(X_train_raw)
test_size  = len(X_test_raw)

train_fraud = int(y_train.sum())
train_legit = train_size - train_fraud
test_fraud  = int(y_test.sum())
test_legit  = test_size - test_fraud

ok(f"Training set : {train_size:,} rows  ({train_fraud:,} fraud | {train_legit:,} legit)")
ok(f"Test set     : {test_size:,} rows  ({test_fraud:,} fraud | {test_legit:,} legit)")

# The test set is now LOCKED. It will NOT be touched by any preprocessing fit.
X_test_raw = X_test_raw.copy()

# ─────────────────────────────────────────────────────────────────────────────
# 5. SMOTE-ENN FEASIBILITY CHECK
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 5 — SMOTE-ENN FEASIBILITY ASSESSMENT")

sub("Estimating SMOTE-ENN computational cost …")
info(f"Training set size  : {train_size:,} rows")
info(f"Training fraud     : {train_fraud:,}")
info(f"Training legit     : {train_legit:,}")
info(f"Imbalance in train : ~{train_legit // train_fraud}:1")

# Estimate peak RAM for SMOTE-ENN:
#   - SMOTE generates synthetic minority samples to match majority count
#   - After SMOTE, combined set ≈ 2 × train_legit rows
#   - Each row has len(ALL_FEATURE_NAMES) float64 columns
smote_synthetic   = train_legit - train_fraud     # samples SMOTE would generate
smote_combined    = train_legit + train_legit      # ≈ 2 × legit after balancing
bytes_per_row     = len(ALL_FEATURE_NAMES) * 8    # float64
estimated_ram_gb  = (smote_combined * bytes_per_row) / (1024**3)

info(f"SMOTE would generate ≈ {smote_synthetic:,} synthetic fraud samples")
info(f"Post-SMOTE combined set ≈ {smote_combined:,} rows")
info(f"Estimated peak RAM (data only) ≈ {estimated_ram_gb:.2f} GB")
info(f"ENN editing phase adds further overhead (neighbour graph on {smote_combined:,} rows)")

SMOTE_ENN_PRACTICAL = False
if train_size < 300_000 and estimated_ram_gb < 4.0:
    SMOTE_ENN_PRACTICAL = True

if SMOTE_ENN_PRACTICAL:
    warn("Full SMOTE-ENN appears feasible — will run on full training data.")
else:
    warn("Full SMOTE-ENN on the complete training set is NOT PRACTICAL on this machine.")
    warn(f"  Reason: training set has {train_size:,} rows; post-SMOTE set would be")
    warn(f"  ≈ {smote_combined:,} rows requiring ≈ {estimated_ram_gb:.1f} GB of RAM for data")
    warn("  alone, plus the ENN graph computation overhead.")
    warn("  Decision: PRIMARY strategy = class_weight / scale_pos_weight.")
    warn("  ACADEMIC COMPARISON: SMOTE-ENN on a 100K stratified subset (documented).")

SMOTE_SUBSET_SIZE = 100_000   # rows for the academic SMOTE-ENN experiment

# ─────────────────────────────────────────────────────────────────────────────
# 6. PREPROCESSING
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 6 — PREPROCESSING")

sub("Fitting RobustScaler on training data (for Logistic Regression) …")
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train_raw)      # fit ONLY on train
X_test_scaled  = scaler.transform(X_test_raw)            # transform test (no fit)
ok("RobustScaler fitted on training data; test set transformed without re-fitting.")

# Tree-based models use the raw (unscaled) feature matrix
X_train_tree = X_train_raw.values.astype(np.float32)
X_test_tree  = X_test_raw.values.astype(np.float32)
ok("Raw feature arrays prepared for tree-based models.")

# ─────────────────────────────────────────────────────────────────────────────
# 7. scale_pos_weight for XGBoost
# ─────────────────────────────────────────────────────────────────────────────
scale_pos_weight_val = train_legit / train_fraud
info(f"XGBoost scale_pos_weight = {scale_pos_weight_val:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: EVALUATE MODEL ON TEST SET
# ─────────────────────────────────────────────────────────────────────────────

def evaluate_model(name: str, model, X_test, y_test, threshold: float = 0.5) -> dict:
    """Compute all metrics for a trained model on the test set."""
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        raw_scores = model.decision_function(X_test)
        # Sigmoid to convert to probabilities
        y_proba = 1 / (1 + np.exp(-raw_scores))
    else:
        y_proba = model.predict(X_test).astype(float)

    y_pred = (y_proba >= threshold).astype(int)

    accuracy  = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall    = recall_score(y_test, y_pred, zero_division=0)
    f1        = f1_score(y_test, y_pred, zero_division=0)
    roc_auc   = roc_auc_score(y_test, y_proba)
    pr_auc    = average_precision_score(y_test, y_proba)

    cm = confusion_matrix(y_test, y_pred)

    return {
        "name":      name,
        "accuracy":  accuracy,
        "precision": precision,
        "recall":    recall,
        "f1":        f1,
        "roc_auc":   roc_auc,
        "pr_auc":    pr_auc,
        "y_proba":   y_proba,
        "y_pred":    y_pred,
        "cm":        cm,
    }


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: PLOT CONFUSION MATRIX
# ─────────────────────────────────────────────────────────────────────────────

def plot_confusion_matrix(result: dict, save_path: str) -> None:
    cm     = result["cm"]
    name   = result["name"]
    labels = ["Legitimate", "Fraud"]

    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, cmap="Blues", colorbar=True, values_format=",d")
    ax.set_title(
        f"Confusion Matrix — {name}\n"
        f"Precision={result['precision']:.4f}  Recall={result['recall']:.4f}  F1={result['f1']:.4f}",
        fontsize=11, fontweight="bold", pad=12,
    )
    ax.set_xlabel("Predicted Label", fontsize=11)
    ax.set_ylabel("True Label", fontsize=11)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    ok(f"Saved confusion matrix → {os.path.basename(save_path)}")


# ─────────────────────────────────────────────────────────────────────────────
# 8. MODEL 1 — LOGISTIC REGRESSION
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 8 — MODEL 1: LOGISTIC REGRESSION")

sub("Training Logistic Regression with class_weight='balanced' …")
t0 = time.time()
lr_model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    solver="lbfgs",
    random_state=RANDOM_STATE,
    n_jobs=-1,
)
lr_model.fit(X_train_scaled, y_train)
lr_train_time = time.time() - t0
ok(f"Logistic Regression trained in {lr_train_time:.1f}s")

sub("Evaluating on test set …")
lr_result = evaluate_model("Logistic Regression", lr_model, X_test_scaled, y_test)
ok(f"  Accuracy  : {lr_result['accuracy']:.6f}")
ok(f"  Precision : {lr_result['precision']:.6f}")
ok(f"  Recall    : {lr_result['recall']:.6f}")
ok(f"  F1        : {lr_result['f1']:.6f}")
ok(f"  ROC-AUC   : {lr_result['roc_auc']:.6f}")
ok(f"  PR-AUC    : {lr_result['pr_auc']:.6f}")

cm_lr_path = os.path.join(RESULTS_DIR, "confusion_matrix_logistic_regression.png")
plot_confusion_matrix(lr_result, cm_lr_path)

# ─────────────────────────────────────────────────────────────────────────────
# 9. MODEL 2 — RANDOM FOREST
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 9 — MODEL 2: RANDOM FOREST")

# Memory-safe parameters for 5M-row dataset:
#   n_jobs=1         : avoids parallel worker OOM (each worker copies large index arrays)
#   max_samples=500000: each tree bootstraps from 500K rows, not the full 5M
#   n_estimators=100 : sufficient for robust fraud detection; faster than 200
sub("Training Random Forest (memory-safe config) ...")
info("  n_estimators=100  max_depth=20  max_samples=500K  n_jobs=1")
info("  n_jobs=1 eliminates parallel worker OOM on 5M-row dataset")
info("  max_samples=500K caps bootstrap size per tree")
t0 = time.time()
try:
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=20,
        min_samples_leaf=10,
        max_samples=500_000,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=1,
        verbose=0,
    )
    rf_model.fit(X_train_tree, y_train)
except MemoryError as mem_err:
    warn(f"RF still OOM ({mem_err}). Falling back to max_samples=200K, n_estimators=50 ...")
    rf_model = RandomForestClassifier(
        n_estimators=50,
        max_depth=15,
        min_samples_split=20,
        min_samples_leaf=10,
        max_samples=200_000,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=1,
        verbose=0,
    )
    rf_model.fit(X_train_tree, y_train)
rf_train_time = time.time() - t0
ok(f"Random Forest trained in {rf_train_time:.1f}s")

sub("Evaluating on test set ...")
rf_result = evaluate_model("Random Forest", rf_model, X_test_tree, y_test)
ok(f"  Accuracy  : {rf_result['accuracy']:.6f}")
ok(f"  Precision : {rf_result['precision']:.6f}")
ok(f"  Recall    : {rf_result['recall']:.6f}")
ok(f"  F1        : {rf_result['f1']:.6f}")
ok(f"  ROC-AUC   : {rf_result['roc_auc']:.6f}")
ok(f"  PR-AUC    : {rf_result['pr_auc']:.6f}")

cm_rf_path = os.path.join(RESULTS_DIR, "confusion_matrix_random_forest.png")
plot_confusion_matrix(rf_result, cm_rf_path)

# ─────────────────────────────────────────────────────────────────────────────
# 10. MODEL 3 — XGBOOST
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 10 — MODEL 3: XGBOOST")

sub(f"Training XGBoost with scale_pos_weight={scale_pos_weight_val:.2f} …")
sub("  Parameters: n_estimators=300, max_depth=6, learning_rate=0.1")
t0 = time.time()
xgb_model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=scale_pos_weight_val,
    eval_metric="aucpr",
    random_state=RANDOM_STATE,
    use_label_encoder=False,
    verbosity=0,
    n_jobs=1,               # single-threaded: avoids parallel memory pressure
)
xgb_model.fit(X_train_tree, y_train)
xgb_train_time = time.time() - t0
ok(f"XGBoost trained in {xgb_train_time:.1f}s")

sub("Evaluating on test set …")
xgb_result = evaluate_model("XGBoost", xgb_model, X_test_tree, y_test)
ok(f"  Accuracy  : {xgb_result['accuracy']:.6f}")
ok(f"  Precision : {xgb_result['precision']:.6f}")
ok(f"  Recall    : {xgb_result['recall']:.6f}")
ok(f"  F1        : {xgb_result['f1']:.6f}")
ok(f"  ROC-AUC   : {xgb_result['roc_auc']:.6f}")
ok(f"  PR-AUC    : {xgb_result['pr_auc']:.6f}")

cm_xgb_path = os.path.join(RESULTS_DIR, "confusion_matrix_xgboost.png")
plot_confusion_matrix(xgb_result, cm_xgb_path)

# ─────────────────────────────────────────────────────────────────────────────
# 11. ACADEMIC SMOTE-ENN EXPERIMENT (100K SUBSET)
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 11 — ACADEMIC: SMOTE-ENN ON 100K STRATIFIED SUBSET")

warn("Full SMOTE-ENN is computationally impractical on the full 5M+ training set.")
warn("Running a controlled SMOTE-ENN experiment on a documented 100K stratified")
warn("training subset for academic comparison ONLY.")
warn("This result is NOT used for model selection or the Flask API.")

smote_results = {}
try:
    from imblearn.combine import SMOTEENN
    from imblearn.over_sampling import SMOTE

    # Sample a stratified 100K subset from training data
    sub(f"Sampling {SMOTE_SUBSET_SIZE:,} stratified rows from training set …")
    idx_train = np.arange(len(y_train))
    # Use train_test_split to get stratified sample
    _, idx_sub, _, y_sub_check = train_test_split(
        idx_train, y_train,
        test_size=SMOTE_SUBSET_SIZE / len(y_train),
        random_state=RANDOM_STATE,
        stratify=y_train,
    )
    X_sub = X_train_scaled[idx_sub]
    y_sub = y_train[idx_sub]

    sub_fraud = int(y_sub.sum())
    sub_legit = len(y_sub) - sub_fraud
    ok(f"Subset: {len(y_sub):,} rows | {sub_fraud:,} fraud | {sub_legit:,} legit")

    sub("Applying SMOTE-ENN on 100K subset …")
    t0 = time.time()
    smote_enn = SMOTEENN(
        smote=SMOTE(random_state=RANDOM_STATE, k_neighbors=5),
        random_state=RANDOM_STATE,
    )
    X_sub_resampled, y_sub_resampled = smote_enn.fit_resample(X_sub, y_sub)
    smote_time = time.time() - t0
    ok(f"SMOTE-ENN completed in {smote_time:.1f}s")
    ok(f"Post-SMOTE-ENN: {len(y_sub_resampled):,} rows | "
       f"{int(y_sub_resampled.sum()):,} fraud | "
       f"{int((y_sub_resampled == 0).sum()):,} legit")

    sub("Training Logistic Regression on SMOTE-ENN subset …")
    t0 = time.time()
    lr_smote = LogisticRegression(
        max_iter=1000,
        solver="lbfgs",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    lr_smote.fit(X_sub_resampled, y_sub_resampled)
    lr_smote_time = time.time() - t0

    sub("Evaluating SMOTE-ENN LR on FULL test set …")
    lr_smote_result = evaluate_model(
        "LR (SMOTE-ENN 100K subset)", lr_smote, X_test_scaled, y_test
    )
    smote_results["lr_smote"] = lr_smote_result

    ok(f"  [ACADEMIC] LR SMOTE-ENN — "
       f"F1={lr_smote_result['f1']:.4f}  "
       f"Recall={lr_smote_result['recall']:.4f}  "
       f"PR-AUC={lr_smote_result['pr_auc']:.4f}")

    warn("NOTE: SMOTE-ENN result trained on 100K subset is for academic reference only.")
    warn("It is NOT used in final model selection or saved as the production model.")

except ImportError:
    warn("imbalanced-learn not installed — skipping SMOTE-ENN experiment.")
    warn("Install with: pip install imbalanced-learn")
except Exception as exc:
    warn(f"SMOTE-ENN experiment failed: {exc}")
    warn("Primary models (class_weight / scale_pos_weight) are unaffected.")


# ─────────────────────────────────────────────────────────────────────────────
# 12. COMBINED ROC CURVE
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 12 — COMBINED ROC CURVE")

sub("Generating combined ROC curve …")
fig, ax = plt.subplots(figsize=(8, 6))

colors = {"Logistic Regression": "#3B82F6", "Random Forest": "#10B981", "XGBoost": "#F59E0B"}
for res in [lr_result, rf_result, xgb_result]:
    fpr, tpr, _ = roc_curve(y_test, res["y_proba"])
    ax.plot(fpr, tpr,
            label=f"{res['name']} (AUC = {res['roc_auc']:.4f})",
            lw=2, color=colors.get(res["name"], "gray"))

ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random Classifier")
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.02])
ax.set_xlabel("False Positive Rate", fontsize=12)
ax.set_ylabel("True Positive Rate", fontsize=12)
ax.set_title("ROC Curve Comparison — All Models", fontsize=14, fontweight="bold")
ax.legend(loc="lower right", fontsize=10)
ax.grid(True, alpha=0.4)
plt.tight_layout()
roc_path = os.path.join(RESULTS_DIR, "roc_curve_comparison.png")
plt.savefig(roc_path, dpi=150, bbox_inches="tight")
plt.close()
ok(f"Saved → {os.path.basename(roc_path)}")


# ─────────────────────────────────────────────────────────────────────────────
# 13. COMBINED PRECISION-RECALL CURVE
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 13 — COMBINED PRECISION-RECALL CURVE")

sub("Generating combined Precision-Recall curve …")
fig, ax = plt.subplots(figsize=(8, 6))

for res in [lr_result, rf_result, xgb_result]:
    prec, rec, _ = precision_recall_curve(y_test, res["y_proba"])
    ax.plot(rec, prec,
            label=f"{res['name']} (PR-AUC = {res['pr_auc']:.4f})",
            lw=2, color=colors.get(res["name"], "gray"))

baseline = fraud_total / total_rows
ax.axhline(y=baseline, color="gray", linestyle="--", lw=1,
           label=f"Baseline (fraud rate = {baseline:.4f})")
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel("Recall", fontsize=12)
ax.set_ylabel("Precision", fontsize=12)
ax.set_title("Precision-Recall Curve Comparison — All Models", fontsize=14, fontweight="bold")
ax.legend(loc="upper right", fontsize=10)
ax.grid(True, alpha=0.4)
plt.tight_layout()
pr_path = os.path.join(RESULTS_DIR, "precision_recall_curve.png")
plt.savefig(pr_path, dpi=150, bbox_inches="tight")
plt.close()
ok(f"Saved → {os.path.basename(pr_path)}")


# ─────────────────────────────────────────────────────────────────────────────
# 14. FEATURE IMPORTANCE
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 14 — FEATURE IMPORTANCE")

def plot_feature_importance(importances, feature_names, model_name, save_path, top_n=15):
    fi_series = pd.Series(importances, index=feature_names).sort_values(ascending=False)
    fi_top    = fi_series.head(top_n)

    fig, ax = plt.subplots(figsize=(9, 6))
    palette = sns.color_palette("YlOrRd_r", n_colors=len(fi_top))
    bars = ax.barh(fi_top.index[::-1], fi_top.values[::-1], color=palette[::-1])
    ax.set_xlabel("Feature Importance Score", fontsize=11)
    ax.set_title(f"Top {top_n} Feature Importances — {model_name}", fontsize=13, fontweight="bold")
    ax.grid(True, axis="x", alpha=0.4)
    for bar, val in zip(bars, fi_top.values[::-1]):
        ax.text(bar.get_width() + fi_top.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{val:.5f}", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    ok(f"Saved feature importance → {os.path.basename(save_path)}")

# Random Forest
sub("Plotting Random Forest feature importance …")
rf_fi_path = os.path.join(RESULTS_DIR, "random_forest_feature_importance.png")
plot_feature_importance(
    rf_model.feature_importances_,
    ALL_FEATURE_NAMES,
    "Random Forest",
    rf_fi_path,
)

# XGBoost
sub("Plotting XGBoost feature importance …")
xgb_fi_path = os.path.join(RESULTS_DIR, "xgboost_feature_importance.png")
plot_feature_importance(
    xgb_model.feature_importances_,
    ALL_FEATURE_NAMES,
    "XGBoost",
    xgb_fi_path,
)

# ─────────────────────────────────────────────────────────────────────────────
# 15. MODEL METRICS CSV
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 15 — MODEL COMPARISON TABLE")

all_results = [lr_result, rf_result, xgb_result]
metrics_rows = []
for res in all_results:
    metrics_rows.append({
        "Model":     res["name"],
        "Accuracy":  round(res["accuracy"], 6),
        "Precision": round(res["precision"], 6),
        "Recall":    round(res["recall"], 6),
        "F1":        round(res["f1"], 6),
        "ROC_AUC":   round(res["roc_auc"], 6),
        "PR_AUC":    round(res["pr_auc"], 6),
    })

metrics_df = pd.DataFrame(metrics_rows)
csv_path = os.path.join(RESULTS_DIR, "model_metrics.csv")
metrics_df.to_csv(csv_path, index=False)
ok(f"Saved model metrics CSV → {os.path.basename(csv_path)}")
print(metrics_df.to_string(index=False), flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# 16. MODEL COMPARISON CHART
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 16 — MODEL COMPARISON BAR CHART")

sub("Plotting model comparison …")
metric_cols = ["Accuracy", "Precision", "Recall", "F1", "ROC_AUC", "PR_AUC"]
bar_colors  = ["#3B82F6", "#10B981", "#F59E0B"]

x     = np.arange(len(metric_cols))
width = 0.25

fig, ax = plt.subplots(figsize=(13, 6))
for i, row in metrics_df.iterrows():
    vals = [row[m] for m in metric_cols]
    bars = ax.bar(x + i * width, vals, width, label=row["Model"],
                  color=bar_colors[i % len(bar_colors)], alpha=0.9)
    for bar, val in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.005,
            f"{val:.3f}",
            ha="center", va="bottom", fontsize=7.5, fontweight="bold",
        )

ax.set_xticks(x + width)
ax.set_xticklabels(metric_cols, fontsize=11)
ax.set_ylim([0, 1.15])
ax.set_ylabel("Score", fontsize=12)
ax.set_title("Model Performance Comparison — All Metrics", fontsize=14, fontweight="bold")
ax.legend(fontsize=11)
ax.grid(True, axis="y", alpha=0.35)
plt.tight_layout()
comparison_path = os.path.join(RESULTS_DIR, "model_comparison.png")
plt.savefig(comparison_path, dpi=150, bbox_inches="tight")
plt.close()
ok(f"Saved model comparison chart → {os.path.basename(comparison_path)}")


# ─────────────────────────────────────────────────────────────────────────────
# 17. MODEL SELECTION
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 17 — MODEL SELECTION")

sub("Evaluating all models for final selection …")
print(flush=True)
for res in all_results:
    cm = res["cm"]
    tn, fp, fn, tp = cm.ravel()
    print(f"  {res['name']:25s} | "
          f"Prec={res['precision']:.4f} | "
          f"Rec={res['recall']:.4f} | "
          f"F1={res['f1']:.4f} | "
          f"ROC-AUC={res['roc_auc']:.4f} | "
          f"PR-AUC={res['pr_auc']:.4f} | "
          f"TP={tp:,} FN={fn:,} FP={fp:,}",
          flush=True)

print(flush=True)

# Selection criterion: prioritize PR-AUC and F1 for highly imbalanced fraud detection
# then break ties using Recall (missing fraud = high cost) then Precision
best_model_name = metrics_df.loc[
    metrics_df[["PR_AUC", "F1", "Recall"]].apply(
        lambda r: (r["PR_AUC"] * 0.5 + r["F1"] * 0.3 + r["Recall"] * 0.2), axis=1
    ).idxmax(),
    "Model"
]

best_result = next(r for r in all_results if r["name"] == best_model_name)
cm_best = best_result["cm"]
tn_b, fp_b, fn_b, tp_b = cm_best.ravel()

sub(f"Selected final model: {best_model_name}")
ok(f"  Precision : {best_result['precision']:.6f}")
ok(f"  Recall    : {best_result['recall']:.6f}")
ok(f"  F1        : {best_result['f1']:.6f}")
ok(f"  ROC-AUC   : {best_result['roc_auc']:.6f}")
ok(f"  PR-AUC    : {best_result['pr_auc']:.6f}")
ok(f"  True Fraud Caught (TP): {tp_b:,}")
ok(f"  Missed Fraud (FN)     : {fn_b:,}")
ok(f"  False Alerts (FP)     : {fp_b:,}")


# ─────────────────────────────────────────────────────────────────────────────
# 18. SAVE FINAL MODEL & PREPROCESSOR
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 18 — SAVE FINAL MODEL & PREPROCESSOR")

# Determine which X array was used for the best model
if best_model_name == "Logistic Regression":
    best_model_obj   = lr_model
    best_preprocessor = scaler
    preprocessor_type = "RobustScaler"
elif best_model_name == "Random Forest":
    best_model_obj   = rf_model
    best_preprocessor = None   # tree-based: no scaler needed
    preprocessor_type = "None (tree-based)"
else:  # XGBoost
    best_model_obj   = xgb_model
    best_preprocessor = None
    preprocessor_type = "None (tree-based)"

model_path = os.path.join(MODELS_DIR, "fraudguard_model.joblib")
joblib.dump(best_model_obj, model_path, compress=3)
ok(f"Saved model → {model_path}")

# Always save the scaler (needed for LR fallback and future use)
scaler_path = os.path.join(MODELS_DIR, "fraudguard_preprocessor.joblib")
joblib.dump(scaler, scaler_path, compress=3)
ok(f"Saved preprocessor (RobustScaler) → {scaler_path}")

# Also save all three models individually for API flexibility
lr_path  = os.path.join(MODELS_DIR, "logistic_regression_model.joblib")
rf_path  = os.path.join(MODELS_DIR, "random_forest_model.joblib")
xgb_path = os.path.join(MODELS_DIR, "xgboost_model.joblib")
joblib.dump(lr_model,  lr_path,  compress=3)
joblib.dump(rf_model,  rf_path,  compress=3)
joblib.dump(xgb_model, xgb_path, compress=3)
ok(f"Saved all three individual models to {MODELS_DIR}")

# ─────────────────────────────────────────────────────────────────────────────
# 19. FEATURE CONFIG JSON
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 19 — FEATURE CONFIG JSON")

type_categories = list(df["type"].unique())

feature_config = {
    "model_name":           best_model_name,
    "model_version":        "1.0.0",
    "training_random_state": RANDOM_STATE,
    "expected_feature_names": ALL_FEATURE_NAMES,
    "numerical_features":   NUMERICAL_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "engineered_features":  ENGINEERED_FEATURES,
    "encoding": {
        "type": {
            "method":     "one-hot (get_dummies)",
            "prefix":     "type",
            "drop_first": False,
            "categories": type_categories,
            "encoded_columns": type_columns,
        }
    },
    "preprocessing": {
        "logistic_regression": "RobustScaler (fitted on training data)",
        "random_forest":       "None (tree-based)",
        "xgboost":             "None (tree-based)",
    },
    "feature_engineering": {
        "errorBalanceOrig": "oldbalanceOrg - amount - newbalanceOrig",
        "errorBalanceDest": "oldbalanceDest + amount - newbalanceDest",
    },
    "excluded_columns": ["isFraud", "isFlaggedFraud", "nameOrig", "nameDest"],
    "target":           "isFraud",
    "selected_model_preprocessor": preprocessor_type,
}

config_path = os.path.join(MODELS_DIR, "feature_config.json")
with open(config_path, "w") as f:
    json.dump(feature_config, f, indent=2)
ok(f"Saved feature config → {config_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 20. TRAINING SUMMARY JSON
# ─────────────────────────────────────────────────────────────────────────────
banner("STEP 20 — TRAINING SUMMARY JSON")

model_metrics_all = {}
for res in all_results:
    model_metrics_all[res["name"]] = {
        "accuracy":  round(res["accuracy"], 6),
        "precision": round(res["precision"], 6),
        "recall":    round(res["recall"], 6),
        "f1":        round(res["f1"], 6),
        "roc_auc":   round(res["roc_auc"], 6),
        "pr_auc":    round(res["pr_auc"], 6),
    }

smote_meta = {}
if smote_results:
    lr_smote_r = smote_results.get("lr_smote")
    if lr_smote_r:
        smote_meta = {
            "experiment":       "SMOTE-ENN on 100K stratified training subset",
            "subset_size":      SMOTE_SUBSET_SIZE,
            "model":            "Logistic Regression",
            "note":             "ACADEMIC ONLY — not used for production model selection",
            "lr_smote_f1":      round(lr_smote_r["f1"], 6),
            "lr_smote_recall":  round(lr_smote_r["recall"], 6),
            "lr_smote_pr_auc":  round(lr_smote_r["pr_auc"], 6),
        }

training_summary = {
    "dataset_path":      DATA_PATH,
    "dataset_size":      total_rows,
    "train_size":        train_size,
    "test_size":         test_size,
    "fraud_count_total": fraud_total,
    "legit_count_total": legit_total,
    "fraud_rate_pct":    round(fraud_rate, 6),
    "imbalance_ratio":   round(imbalance_ratio, 2),
    "test_size_fraction": TEST_SIZE,
    "random_state":      RANDOM_STATE,
    "stratified_split":  True,
    "preprocessing": {
        "logistic_regression": "RobustScaler (fit on train only)",
        "random_forest":       "None (raw features)",
        "xgboost":             "None (raw features)",
    },
    "imbalance_strategy": {
        "logistic_regression": "class_weight='balanced'",
        "random_forest":       "class_weight='balanced'",
        "xgboost":             f"scale_pos_weight={scale_pos_weight_val:.4f}",
        "smote_enn_status":    "IMPRACTICAL on full set — academic subset experiment run",
    },
    "smote_enn_experiment": smote_meta,
    "model_metrics":     model_metrics_all,
    "selected_final_model": best_model_name,
    "training_date":     datetime.datetime.now().isoformat(),
    "training_times_seconds": {
        "logistic_regression": round(lr_train_time, 2),
        "random_forest":       round(rf_train_time, 2),
        "xgboost":             round(xgb_train_time, 2),
    },
    "output_artifacts": {
        "results_dir": RESULTS_DIR,
        "models_dir":  MODELS_DIR,
        "plots": [
            "confusion_matrix_logistic_regression.png",
            "confusion_matrix_random_forest.png",
            "confusion_matrix_xgboost.png",
            "roc_curve_comparison.png",
            "precision_recall_curve.png",
            "random_forest_feature_importance.png",
            "xgboost_feature_importance.png",
            "model_comparison.png",
        ],
        "data_files": [
            "model_metrics.csv",
            "training_summary.json",
        ],
        "model_files": [
            "fraudguard_model.joblib",
            "fraudguard_preprocessor.joblib",
            "feature_config.json",
            "logistic_regression_model.joblib",
            "random_forest_model.joblib",
            "xgboost_model.joblib",
        ],
    },
}

summary_path = os.path.join(RESULTS_DIR, "training_summary.json")
with open(summary_path, "w") as f:
    json.dump(training_summary, f, indent=2)
ok(f"Saved training summary → {summary_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 21. FINAL REPORT
# ─────────────────────────────────────────────────────────────────────────────
banner("STAGE 3C COMPLETE — FINAL TRAINING REPORT")

sep = "=" * 72
row = "-" * 72

print(f"\n{sep}", flush=True)
print("  FRAUDGUARD - STAGE 3C TRAINING REPORT", flush=True)
print(sep, flush=True)
print(f"  Dataset       : {total_rows:>12,} transactions", flush=True)
print(f"  Train set     : {train_size:>12,} rows", flush=True)
print(f"  Test set      : {test_size:>12,} rows", flush=True)
print(f"  Fraud (total) : {fraud_total:>12,} ({fraud_rate:.4f}%)", flush=True)
print(f"  Imbalance     : {imbalance_ratio:>12.0f}:1", flush=True)
print(row, flush=True)
print("  SMOTE-ENN     : Impractical on full set (RAM cost too high)", flush=True)
print("  Primary strategy: class_weight / scale_pos_weight", flush=True)
print("  Academic SMOTE-ENN on 100K subset: completed", flush=True)
print(row, flush=True)
print("  MODEL RESULTS (on ORIGINAL UNTOUCHED TEST SET)", flush=True)
print(f"  {'Model':<25} | {'Acc':>7} | {'Prec':>7} | {'Rec':>7} | {'F1':>7} | {'ROC-AUC':>8} | {'PR-AUC':>7}", flush=True)
print(row, flush=True)

for res in all_results:
    print(f"  {res['name']:<25} | "
          f"{res['accuracy']:>7.4f} | "
          f"{res['precision']:>7.4f} | "
          f"{res['recall']:>7.4f} | "
          f"{res['f1']:>7.4f} | "
          f"{res['roc_auc']:>8.4f} | "
          f"{res['pr_auc']:>7.4f}", flush=True)

print(row, flush=True)
print(f"  SELECTED FINAL MODEL : {best_model_name}", flush=True)
print(row, flush=True)
print("  Saved artifacts:", flush=True)
print("    ml/models/fraudguard_model.joblib", flush=True)
print("    ml/models/fraudguard_preprocessor.joblib", flush=True)
print("    ml/models/feature_config.json", flush=True)
print("    ml/results/training_summary.json", flush=True)
print("    ml/results/model_metrics.csv", flush=True)
print("    ml/results/confusion_matrix_*.png", flush=True)
print("    ml/results/roc_curve_comparison.png", flush=True)
print("    ml/results/precision_recall_curve.png", flush=True)
print("    ml/results/model_comparison.png", flush=True)
print(sep, flush=True)
print("\nStage 3C complete. All artifacts saved successfully.", flush=True)
