# FraudGuard — Online Payment Fraud Detection System

> **B.Tech Final-Year Major Project** · Computer Science & Engineering

FraudGuard is an end-to-end academic system that demonstrates the application of supervised machine learning to detect fraudulent online payment transactions in real time. It combines a Python/Flask REST API backend, a React + TypeScript frontend dashboard, and an XGBoost classification model trained on the [PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1) synthetic financial dataset.

---

## Table of Contents

1. [Features](#features)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Machine Learning Models](#machine-learning-models)
5. [Model Comparison & Results](#model-comparison--results)
6. [Dataset Information](#dataset-information)
7. [Project Structure](#project-structure)
8. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Backend Setup](#backend-setup)
   - [Frontend Setup](#frontend-setup)
9. [Usage](#usage)
10. [Academic Disclaimer](#academic-disclaimer)
11. [Author](#author)

---

## Features

- **Real-Time Transaction Analysis** — Submit a payment transaction and receive an instant fraud prediction with probability score and risk classification (LOW / MEDIUM / HIGH).
- **XGBoost Champion Model** — Trained on 6.3 million PaySim records; achieves 99.999% accuracy and 0.9973 F1-score.
- **Feature Engineering** — Derives `errorBalanceOrig` and `errorBalanceDest` from raw balance fields, capturing account-draining anomaly patterns.
- **Transaction History** — All analysed transactions are persisted to a SQLite database and displayed in a searchable, filterable history table.
- **Live Dashboard** — Aggregated metrics (total transactions, fraud rate, average probability, risk distribution) updated in real time from the database.
- **Model Performance Page** — Comparative evaluation metrics, confusion matrix, ROC curve, and feature-importance chart for all three candidate models.
- **REST API** — Clean Flask REST API (`/api/health`, `/api/predict`, `/api/transactions`, `/api/dashboard`) with full CORS support.

---

## System Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                     React + TypeScript                         │
│              (Vite · Tailwind CSS · Chart.js)                  │
│   Dashboard | Analyze | History | Model Performance | About    │
└──────────────────────┬─────────────────────────────────────────┘
                       │ HTTP (via Vite dev-proxy / direct)
                       ▼
┌────────────────────────────────────────────────────────────────┐
│                   Flask REST API (Python)                      │
│  GET  /api/health        POST /api/predict                     │
│  GET  /api/transactions  GET  /api/dashboard                   │
└────────┬────────────────────────────┬───────────────────────────┘
         │                            │
         ▼                            ▼
┌─────────────────┐       ┌──────────────────────────────────────┐
│  SQLite (data/) │       │  XGBoost Model (ml/models/)          │
│  fraudguard.db  │       │  + feature_config.json               │
│  (auto-created) │       │  + fraudguard_preprocessor.joblib    │
└─────────────────┘       └──────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite 5, Tailwind CSS 3, Chart.js 4 |
| **Backend API** | Python 3.11+, Flask 3, Flask-CORS |
| **Machine Learning** | scikit-learn 1.2+, XGBoost 1.7+, pandas, numpy, joblib |
| **Database** | SQLite 3 (via Python standard library) |
| **Data Visualisation** | matplotlib, seaborn (training), Chart.js (dashboard) |

---

## Machine Learning Models

Three classification algorithms were trained and evaluated on the PaySim dataset:

| Model | Role |
| :--- | :--- |
| **Logistic Regression** | Baseline statistical classifier (RobustScaler preprocessing) |
| **Random Forest** | Ensemble baseline (class_weight='balanced') |
| **XGBoost** | Champion model (scale_pos_weight to handle class imbalance) |

### Feature Engineering

The following 13 features are supplied to the model at inference time:

| Feature | Description |
| :--- | :--- |
| `step` | Time step (1 unit = 1 hour) |
| `amount` | Transaction amount |
| `oldbalanceOrg` | Origin account balance before transaction |
| `newbalanceOrig` | Origin account balance after transaction |
| `oldbalanceDest` | Destination account balance before transaction |
| `newbalanceDest` | Destination account balance after transaction |
| `errorBalanceOrig` | Engineered: `oldbalanceOrg - amount - newbalanceOrig` |
| `errorBalanceDest` | Engineered: `oldbalanceDest + amount - newbalanceDest` |
| `type_CASH_IN` | One-hot encoded transaction type |
| `type_CASH_OUT` | One-hot encoded transaction type |
| `type_DEBIT` | One-hot encoded transaction type |
| `type_PAYMENT` | One-hot encoded transaction type |
| `type_TRANSFER` | One-hot encoded transaction type |

---

## Model Comparison & Results

Evaluated on a stratified held-out test set (20% of 6,362,620 records):

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Logistic Regression | 94.97% | 2.41% | 96.10% | 4.70% | 0.9909 |
| Random Forest | 99.99% | 94.25% | 99.82% | 96.96% | 0.9999 |
| **XGBoost ✓ Champion** | **99.999%** | **99.70%** | **99.76%** | **99.73%** | **0.9998** |

> The Logistic Regression baseline shows high recall but poor precision, meaning it flags many legitimate transactions as fraudulent. XGBoost achieves the best balance across all metrics and was selected as the production model.

---

## Dataset Information

| Property | Value |
| :--- | :--- |
| **Name** | PaySim — Synthetic Mobile Money Transactions |
| **Source** | [Kaggle — ealaxi/paysim1](https://www.kaggle.com/datasets/ealaxi/paysim1) |
| **Total Records** | 6,362,620 transactions |
| **Fraud Records** | 8,213 (~0.13%) |
| **File Size** | ~471 MB (CSV) |
| **License** | CC BY-SA 4.0 |

> ⚠️ **The PaySim dataset file is NOT included in this repository** due to its size (~471 MB). To retrain the models, download the CSV from Kaggle and place it at `ml/data/PS_20174392719_1491204439457_log.csv`.

The pre-trained model artifacts (`ml/models/`) are included so the application can be run immediately without retraining.

---

## Project Structure

```
stitch_fraudguard_ml_detection_system/
│
├── backend/                        # Flask REST API
│   ├── app.py                      # Application factory & entry point
│   ├── requirements.txt            # Python dependencies
│   ├── routes/
│   │   ├── predict.py              # POST /api/predict
│   │   ├── transactions.py         # GET  /api/transactions
│   │   └── dashboard.py            # GET  /api/dashboard
│   ├── services/
│   │   ├── model_service.py        # XGBoost model loader & inference
│   │   ├── feature_service.py      # Input validation & feature engineering
│   │   └── risk_service.py         # Risk classification & recommendations
│   ├── database/
│   │   ├── database.py             # SQLite access layer
│   │   └── schema.py               # Table DDL
│   └── test_backend.py             # Isolated backend test suite
│
├── frontend/                       # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/                  # Dashboard, Analyze, History, Performance, About
│   │   ├── components/             # Layout, analysis, dashboard, performance, common
│   │   ├── services/api.ts         # Frontend API client
│   │   ├── context/                # TransactionContext (shared state)
│   │   └── types/index.ts          # TypeScript type definitions
│   ├── package.json
│   └── vite.config.ts
│
├── ml/                             # Machine learning pipeline
│   ├── src/
│   │   ├── train_models.py         # Full training pipeline (LR, RF, XGBoost)
│   │   ├── validate_model.py       # Post-training validation
│   │   ├── run_eda.py              # Exploratory data analysis
│   │   └── build_notebook.py       # Notebook generation utility
│   ├── models/                     # Saved model artifacts (committed)
│   │   ├── fraudguard_model.joblib         # Champion XGBoost (252 KB)
│   │   ├── fraudguard_preprocessor.joblib  # RobustScaler for LR (< 1 KB)
│   │   ├── feature_config.json             # Feature names & config
│   │   ├── logistic_regression_model.joblib
│   │   ├── random_forest_model.joblib      # (691 KB)
│   │   └── xgboost_model.joblib
│   ├── results/                    # Training outputs (metrics, plots)
│   ├── notebooks/                  # Jupyter EDA notebook
│   ├── data/                       # ← NOT committed (see Dataset section)
│   └── requirements.txt
│
├── verify_full_integration.py      # End-to-end integration test script
├── fraudguard_project_info.md      # Project design notes
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python 3.11+** with `pip`
- **Node.js 18+** with `npm`
- Git

### Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/stitch_fraudguard_ml_detection_system.git
cd stitch_fraudguard_ml_detection_system

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r backend/requirements.txt

# 4. Start the Flask API server
python backend/app.py
# → Running on http://127.0.0.1:5000
```

The SQLite database (`backend/data/fraudguard.db`) is created automatically on first run.

**Verify the backend is healthy:**
```
GET http://127.0.0.1:5000/api/health
```

### Frontend Setup

```bash
# In a separate terminal, from the project root:
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
# → http://localhost:3000
```

The Vite dev server is pre-configured to proxy `/api/*` requests to `http://127.0.0.1:5000`.

---

## Usage

1. Start the Flask backend (`python backend/app.py`).
2. Start the Vite frontend (`npm run dev` inside `frontend/`).
3. Open [http://localhost:3000](http://localhost:3000) in a browser.
4. Navigate to **Analyze Transaction**, fill in the transaction fields, and click **Run Analysis**.
5. The prediction result (LEGITIMATE / FRAUD), fraud probability, risk level, and recommendation are displayed immediately.
6. View all analysed transactions in **Transaction History**.
7. Monitor aggregate metrics in the **Overview Dashboard**.

**To re-train the models** (requires the PaySim dataset):
```bash
pip install -r ml/requirements.txt
python ml/src/train_models.py
```

**To run the backend test suite:**
```bash
python backend/test_backend.py
# Runs against an isolated temporary database — does not affect live data
```

---

## Academic Disclaimer

This project is developed solely for academic purposes as a B.Tech final-year major project. It is a **simulation and demonstration system** and does **not**:

- Process real financial transactions or real money.
- Connect to any banking API, payment gateway, or live financial system.
- Provide legally or financially certified fraud scores.
- Guarantee the accuracy of any fraud prediction in a production context.

The PaySim dataset used for training is a **synthetic** dataset generated to mimic real mobile money transaction patterns; it does not contain actual personal or financial data.

---

## Author

**Sathwik** — B.Tech, Computer Science & Engineering  
Final Year Major Project · 2025–2026

---

*Built with Python · Flask · React · TypeScript · XGBoost · SQLite*
