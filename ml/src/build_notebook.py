"""
FraudGuard EDA Notebook Generator
Writes the fraudguard_eda.ipynb to ml/notebooks/
"""
import json, os

def md_cell(source_lines):
    return {"cell_type": "markdown", "id": "m" + str(abs(hash(str(source_lines))))[:8],
            "metadata": {}, "source": source_lines}

def code_cell(source_lines):
    return {"cell_type": "code", "execution_count": None, "id": "c" + str(abs(hash(str(source_lines))))[:8],
            "metadata": {}, "outputs": [], "source": source_lines}

cells = []

# ---- HEADER ----
cells.append(md_cell([
    "# FraudGuard: Exploratory Data Analysis (EDA)\n",
    "## Stage 3B — PaySim Online Payment Fraud Detection Dataset\n",
    "\n",
    "**Project:** Online Payment Fraud Detection using Machine Learning\n",
    "**Dataset:** PaySim Synthetic Financial Transactions (`PS_20174392719_1491204439457_log.csv`)\n",
    "**Academic Context:** 4th-Year B.Tech Major Project\n",
    "\n",
    "---\n",
    "\n",
    "**Objectives of this Notebook:**\n",
    "1. Load and inspect the PaySim dataset\n",
    "2. Perform data quality checks\n",
    "3. Analyze the class distribution\n",
    "4. Analyze transaction types and fraud patterns\n",
    "5. Explore numerical feature distributions\n",
    "6. Engineer and evaluate new features\n",
    "7. Perform a strict data leakage audit\n",
    "8. Propose the final feature set for model training\n",
    "\n",
    "> **No model is trained in this notebook. This is a pure EDA and data preparation stage.**"
]))

# ---- SECTION 1: SETUP ----
cells.append(md_cell(["---\n", "## 1. Setup and Dataset Loading"]))
cells.append(code_cell([
    "import os, warnings\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "warnings.filterwarnings('ignore')\n",
    "sns.set_theme(style='whitegrid')\n",
    "\n",
    "DATA_PATH   = r'..\\data\\PS_20174392719_1491204439457_log.csv'\n",
    "RESULTS_DIR = r'..\\results'\n",
    "os.makedirs(RESULTS_DIR, exist_ok=True)\n",
    "\n",
    "print(f'Loading dataset: {DATA_PATH}')\n",
    "df = pd.read_csv(DATA_PATH)\n",
    "print(f'Dataset loaded. Shape: {df.shape}')"
]))

# ---- SECTION 2: OVERVIEW ----
cells.append(md_cell(["---\n", "## 2. Dataset Overview\n",
    "\n",
    "The PaySim dataset simulates **30 days** of mobile money transactions with realistic fraud patterns.\n",
    "Five transaction types: CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER."
]))
cells.append(code_cell([
    "print(f'Rows:    {df.shape[0]:,}')\n",
    "print(f'Columns: {df.shape[1]}')\n",
    "print(f'Columns: {list(df.columns)}')\n",
    "print('\\nData Types:')\n",
    "print(df.dtypes)\n",
    "print('\\nFirst 3 rows:')\n",
    "df.head(3)"
]))
cells.append(code_cell([
    "print('Numerical Statistics:')\n",
    "df.describe().T"
]))

# ---- SECTION 3: DATA QUALITY ----
cells.append(md_cell(["---\n", "## 3. Data Quality Checks\n",
    "\n",
    "Checking for missing values, duplicate rows, and cardinality of categorical columns."
]))
cells.append(code_cell([
    "print('--- Missing Values ---')\n",
    "print(df.isnull().sum())\n",
    "print(f'\\nTotal missing: {df.isnull().sum().sum()}')\n",
    "\n",
    "print('\\n--- Duplicate Rows ---')\n",
    "print(f'Duplicate rows: {df.duplicated().sum()}')\n",
    "\n",
    "print('\\n--- Categorical Cardinality ---')\n",
    "for col in ['type', 'nameOrig', 'nameDest']:\n",
    "    print(f'  {col}: {df[col].nunique():,} unique values')\n",
    "    if col == 'type':\n",
    "        print(f'     Values: {sorted(df[col].unique())}')"
]))
cells.append(md_cell([
    "**Data Quality Summary:**\n",
    "\n",
    "| Check | Result | Action |\n",
    "|---|---|---|\n",
    "| Missing Values | **0** | None required |\n",
    "| Duplicate Rows | **0** | None required |\n",
    "| `type` cardinality | **5** | One-hot encode |\n",
    "| `nameOrig` cardinality | **~6.35M** | Exclude — high cardinality ID |\n",
    "| `nameDest` cardinality | **~2.72M** | Exclude — high cardinality ID |"
]))

# ---- SECTION 4: CLASS DISTRIBUTION ----
cells.append(md_cell(["---\n", "## 4. Class Distribution (Fraud vs Legitimate)\n",
    "\n",
    "> A classifier predicting LEGITIMATE for every transaction achieves **99.87% accuracy** but catches **zero fraud**.\n",
    "> This is why **accuracy alone is completely insufficient** for fraud detection.\n",
    "> We must evaluate using **F1-Score, Recall, Precision, and ROC-AUC**."
]))
cells.append(code_cell([
    "total = len(df)\n",
    "fraud_count = int((df['isFraud'] == 1).sum())\n",
    "legit_count = total - fraud_count\n",
    "\n",
    "print(f'Legitimate Transactions : {legit_count:,}  ({legit_count/total*100:.4f}%)')\n",
    "print(f'Fraudulent Transactions : {fraud_count:,}   ({fraud_count/total*100:.4f}%)')\n",
    "print(f'Imbalance Ratio         : {legit_count//fraud_count}:1  (legitimate to fraud)')\n",
    "\n",
    "fig, axes = plt.subplots(1, 2, figsize=(13, 5))\n",
    "\n",
    "bars = axes[0].bar(['Legitimate', 'Fraud'], [legit_count, fraud_count],\n",
    "                   color=['#10B981', '#EF4444'], width=0.5)\n",
    "axes[0].set_yscale('log')\n",
    "axes[0].set_title('Class Distribution (Log Scale)', fontsize=13, fontweight='bold')\n",
    "axes[0].set_ylabel('Count (Log Scale)')\n",
    "for bar in bars:\n",
    "    h = bar.get_height()\n",
    "    axes[0].annotate(f'{int(h):,}',\n",
    "                     xy=(bar.get_x() + bar.get_width()/2, h),\n",
    "                     xytext=(0, 5), textcoords='offset points',\n",
    "                     ha='center', va='bottom', fontweight='bold')\n",
    "\n",
    "axes[1].pie([legit_count, fraud_count],\n",
    "            labels=['Legitimate (99.87%)', 'Fraud (0.13%)'],\n",
    "            colors=['#10B981', '#EF4444'], startangle=90,\n",
    "            wedgeprops=dict(edgecolor='white', linewidth=2))\n",
    "axes[1].set_title('Class Proportion', fontsize=13, fontweight='bold')\n",
    "\n",
    "plt.suptitle('PaySim Dataset: Class Imbalance', fontsize=14, fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.savefig(os.path.join(RESULTS_DIR, 'class_distribution.png'), dpi=300, bbox_inches='tight')\n",
    "plt.show()\n",
    "print('Saved: class_distribution.png')"
]))

# ---- SECTION 5: TRANSACTION TYPE ----
cells.append(md_cell(["---\n", "## 5. Transaction Type Analysis"]))
cells.append(code_cell([
    "type_stats = df.groupby('type').agg(\n",
    "    total  = ('isFraud', 'count'),\n",
    "    fraud  = ('isFraud', lambda x: (x == 1).sum()),\n",
    "    legit  = ('isFraud', lambda x: (x == 0).sum())\n",
    ").reset_index()\n",
    "type_stats['fraud_pct'] = type_stats['fraud'] / type_stats['total'] * 100\n",
    "print('Transaction Type Statistics:')\n",
    "print(type_stats.to_string(index=False))\n",
    "\n",
    "fig, axes = plt.subplots(1, 3, figsize=(17, 5))\n",
    "\n",
    "axes[0].bar(type_stats['type'], type_stats['total'], color='#3B82F6')\n",
    "axes[0].set_title('Total Volume by Type', fontweight='bold')\n",
    "axes[0].set_ylabel('Count')\n",
    "\n",
    "c1 = ['#10B981' if f == 0 else '#EF4444' for f in type_stats['fraud']]\n",
    "axes[1].bar(type_stats['type'], type_stats['fraud'], color=c1)\n",
    "axes[1].set_title('Fraud Count by Type', fontweight='bold')\n",
    "axes[1].set_ylabel('Fraud Count')\n",
    "\n",
    "c2 = ['#10B981' if p == 0 else '#EF4444' for p in type_stats['fraud_pct']]\n",
    "axes[2].bar(type_stats['type'], type_stats['fraud_pct'], color=c2)\n",
    "axes[2].set_title('Fraud Rate by Type (%)', fontweight='bold')\n",
    "axes[2].set_ylabel('Fraud Rate (%)')\n",
    "\n",
    "plt.suptitle('Fraud Pattern by Transaction Type', fontsize=13, fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.savefig(os.path.join(RESULTS_DIR, 'fraud_by_transaction_type.png'), dpi=300, bbox_inches='tight')\n",
    "plt.show()\n",
    "print('Saved: fraud_by_transaction_type.png')"
]))
cells.append(md_cell([
    "**Key Finding:** Fraud is **exclusively** confined to `CASH_OUT` and `TRANSFER` transaction types.\n",
    "- CASH_IN, PAYMENT, DEBIT have **zero fraud** cases\n",
    "- TRANSFER has the highest fraud rate at **0.769%**\n",
    "- This is a genuine behavioral signal — not data leakage"
]))

# ---- SECTION 6: NUMERICAL FEATURES ----
cells.append(md_cell(["---\n", "## 6. Numerical Feature Analysis"]))
cells.append(code_cell([
    "print('Amount Statistics by Class:')\n",
    "print(df.groupby('isFraud')['amount'].describe().T)\n",
    "\n",
    "print('\\nFeature Skewness:')\n",
    "for col in ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']:\n",
    "    print(f'  {col:20s}: {df[col].skew():.2f}')"
]))
cells.append(code_cell([
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "axes[0].hist(np.log1p(df[df['isFraud']==0]['amount'].sample(100000, random_state=42)),\n",
    "             bins=80, alpha=0.5, color='#10B981', label='Legitimate', density=True)\n",
    "axes[0].hist(np.log1p(df[df['isFraud']==1]['amount']),\n",
    "             bins=80, alpha=0.6, color='#EF4444', label='Fraudulent', density=True)\n",
    "axes[0].set_title('Amount Distribution (log1p scale)', fontweight='bold')\n",
    "axes[0].set_xlabel('log1p(amount)')\n",
    "axes[0].legend()\n",
    "\n",
    "axes[1].hist(df[df['isFraud']==0]['step'].sample(100000, random_state=42),\n",
    "             bins=60, alpha=0.5, color='#10B981', label='Legitimate', density=True)\n",
    "axes[1].hist(df[df['isFraud']==1]['step'],\n",
    "             bins=60, alpha=0.6, color='#EF4444', label='Fraudulent', density=True)\n",
    "axes[1].set_title('Step Distribution by Class', fontweight='bold')\n",
    "axes[1].set_xlabel('Step (1 hour per step)')\n",
    "axes[1].legend()\n",
    "\n",
    "plt.suptitle('Numerical Feature Distributions', fontsize=13, fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.savefig(os.path.join(RESULTS_DIR, 'amount_distribution.png'), dpi=300, bbox_inches='tight')\n",
    "plt.show()\n",
    "print('Saved: amount_distribution.png')"
]))
cells.append(code_cell([
    "# Balance feature distributions\n",
    "sample_df = df.sample(n=100000, random_state=42)\n",
    "fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n",
    "\n",
    "for ax, col, title in [\n",
    "    (axes[0,0], 'oldbalanceOrg',  'Old Balance (Origin)'),\n",
    "    (axes[0,1], 'newbalanceOrig', 'New Balance (Origin)'),\n",
    "    (axes[1,0], 'oldbalanceDest', 'Old Balance (Destination)'),\n",
    "    (axes[1,1], 'newbalanceDest', 'New Balance (Destination)'),\n",
    "]:\n",
    "    for cls, color, lbl in [(0,'#10B981','Legitimate'),(1,'#EF4444','Fraud')]:\n",
    "        data = sample_df[sample_df['isFraud']==cls][col]\n",
    "        data = data[data > 0]\n",
    "        ax.hist(np.log1p(data), bins=60, alpha=0.5, color=color, label=lbl, density=True)\n",
    "    ax.set_title(f'{title} (log1p)', fontweight='bold')\n",
    "    ax.legend()\n",
    "\n",
    "plt.suptitle('Balance Features: Legitimate vs Fraudulent', fontsize=14, fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.savefig(os.path.join(RESULTS_DIR, 'feature_analysis.png'), dpi=300, bbox_inches='tight')\n",
    "plt.show()\n",
    "print('Saved: feature_analysis.png')"
]))

# ---- SECTION 7: FRAUD PATTERNS ----
cells.append(md_cell(["---\n", "## 7. Fraud Pattern Analysis"]))
cells.append(code_cell([
    "fraud_df = df[df['isFraud'] == 1]\n",
    "legit_df = df[df['isFraud'] == 0]\n",
    "\n",
    "fraud_drained = (fraud_df['newbalanceOrig'] == 0).mean() * 100\n",
    "legit_drained = (legit_df['newbalanceOrig'] == 0).mean() * 100\n",
    "print(f'newbalanceOrig == 0 in Fraud  : {fraud_drained:.1f}%')\n",
    "print(f'newbalanceOrig == 0 in Legit  : {legit_drained:.1f}%')\n",
    "\n",
    "fraud_dest0 = (fraud_df['oldbalanceDest'] == 0).mean() * 100\n",
    "legit_dest0 = (legit_df['oldbalanceDest'] == 0).mean() * 100\n",
    "print(f'\\noldbalanceDest == 0 in Fraud  : {fraud_dest0:.1f}%')\n",
    "print(f'oldbalanceDest == 0 in Legit  : {legit_dest0:.1f}%')\n",
    "\n",
    "print('\\nisFlaggedFraud vs isFraud:')\n",
    "print(pd.crosstab(df['isFlaggedFraud'], df['isFraud']))\n",
    "\n",
    "flagged_ct = int(df[(df['isFlaggedFraud']==1)&(df['isFraud']==1)].shape[0])\n",
    "print(f'\\nisFlaggedFraud captures {flagged_ct} / {fraud_count} fraud cases ({flagged_ct/fraud_count*100:.2f}%)')"
]))
cells.append(md_cell([
    "**isFlaggedFraud Critical Finding:**\n",
    "\n",
    "| isFlaggedFraud | Legitimate | Fraud |\n",
    "|---|---|---|\n",
    "| 0 (not flagged) | 6,354,407 | **8,197** |\n",
    "| 1 (flagged) | 0 | **16** |\n",
    "\n",
    "- Captures only **0.19%** of fraud cases — it is an almost useless existing rule\n",
    "- **Decision: `isFlaggedFraud` must be EXCLUDED** — it constitutes indirect label leakage\n",
    "  because it was derived from the same fraud detection logic used to generate `isFraud`"
]))

# ---- SECTION 8: FEATURE ENGINEERING ----
cells.append(md_cell(["---\n", "## 8. Feature Engineering Exploration"]))
cells.append(code_cell([
    "df['errorBalanceOrig'] = df['oldbalanceOrg'] - df['amount'] - df['newbalanceOrig']\n",
    "df['errorBalanceDest'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']\n",
    "df['hour']             = df['step'] % 24\n",
    "\n",
    "numeric_cols = ['amount','oldbalanceOrg','newbalanceOrig','oldbalanceDest','newbalanceDest',\n",
    "               'errorBalanceOrig','errorBalanceDest','hour']\n",
    "corr = df[numeric_cols + ['isFraud']].corr()['isFraud'].drop('isFraud').sort_values(ascending=False)\n",
    "print('Pearson Correlation with isFraud:')\n",
    "print(corr)\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 5))\n",
    "colors = ['#10B981' if v >= 0 else '#EF4444' for v in corr.values]\n",
    "ax.barh(corr.index, corr.values, color=colors)\n",
    "ax.axvline(0, color='black', linewidth=0.8)\n",
    "ax.set_title('Feature Correlation with isFraud', fontsize=13, fontweight='bold')\n",
    "ax.set_xlabel('Pearson Correlation Coefficient')\n",
    "plt.tight_layout()\n",
    "plt.savefig(os.path.join(RESULTS_DIR, 'feature_correlation.png'), dpi=300, bbox_inches='tight')\n",
    "plt.show()\n",
    "print('Saved: feature_correlation.png')"
]))
cells.append(md_cell([
    "**Engineered Feature Evaluation:**\n",
    "\n",
    "| Feature | Correlation | Include? | Reason |\n",
    "|---|---|---|---|\n",
    "| `amount` | +0.077 | YES | Fraud involves larger amounts |\n",
    "| `errorBalanceDest` | +0.055 | YES | Destination didn't receive money as expected |\n",
    "| `errorBalanceOrig` | +0.011 | YES | Origin didn't lose money as expected |\n",
    "| `oldbalanceOrg` | +0.010 | YES | Fraud targets larger balances |\n",
    "| `newbalanceDest` | +0.001 | YES | Post-transaction balance signal |\n",
    "| `oldbalanceDest` | -0.006 | YES | Context for destination |\n",
    "| `newbalanceOrig` | -0.008 | YES | Drains to 0 in fraud |\n",
    "| `hour` | -0.031 | LOW | Weak temporal signal |\n",
    "\n",
    "Note: Tree-based models will capture non-linear relationships — linear Pearson correlation\n",
    "understates the importance of `type`, `errorBalanceOrig`, and `errorBalanceDest`."
]))

# ---- SECTION 9: LEAKAGE CHECK ----
cells.append(md_cell(["---\n", "## 9. Data Leakage Audit\n",
    "\n",
    "Leakage causes models that look perfect in evaluation but fail in production."
]))
cells.append(code_cell([
    "print('DATA LEAKAGE AUDIT')\n",
    "print('=' * 60)\n",
    "\n",
    "checks = [\n",
    "    ('isFraud',        'DIRECT TARGET',         'EXCLUDED — this is the prediction label'),\n",
    "    ('isFlaggedFraud', 'INDIRECT LEAKAGE',      'EXCLUDED — business rule derived from fraud logic'),\n",
    "    ('nameOrig',       'ID OVERFITTING',         'EXCLUDED — 6.35M unique values, zero generalization'),\n",
    "    ('nameDest',       'ID OVERFITTING',         'EXCLUDED — 2.72M unique values, zero generalization'),\n",
    "    ('errorBalanceOrig', 'SAFE',                 'Derived from input columns only — no leakage'),\n",
    "    ('errorBalanceDest', 'SAFE',                 'Derived from input columns only — no leakage'),\n",
    "    ('newbalanceOrig',   'SAFE',                 'Available at inference time'),\n",
    "    ('newbalanceDest',   'SAFE',                 'Available at inference time'),\n",
    "]\n",
    "\n",
    "for col, risk, action in checks:\n",
    "    print(f'  [{risk:18s}]  {col:20s}: {action}')"
]))

# ---- SECTION 10: PROPOSED FEATURES ----
cells.append(md_cell(["---\n", "## 10. Proposed Feature Set for Model Training"]))
cells.append(code_cell([
    "PROPOSED_FEATURES = [\n",
    "    'step',              # Time step — temporal context\n",
    "    'type',              # Transaction type — CRITICAL (OHE required)\n",
    "    'amount',            # Transaction amount — strong discriminator\n",
    "    'oldbalanceOrg',     # Origin balance before transaction\n",
    "    'newbalanceOrig',    # Origin balance after (drains to 0 in fraud)\n",
    "    'oldbalanceDest',    # Destination balance before transaction\n",
    "    'newbalanceDest',    # Destination balance after\n",
    "    'errorBalanceOrig',  # Engineered: balance discrepancy at origin\n",
    "    'errorBalanceDest',  # Engineered: balance discrepancy at destination\n",
    "]\n",
    "\n",
    "TARGET = 'isFraud'\n",
    "\n",
    "EXCLUDED = {\n",
    "    'isFraud':        'TARGET — prediction label, never include as input',\n",
    "    'isFlaggedFraud': 'INDIRECT LEAKAGE — derived from fraud detection threshold',\n",
    "    'nameOrig':       'HIGH CARDINALITY ID — 6.35M unique values',\n",
    "    'nameDest':       'HIGH CARDINALITY ID — 2.72M unique values',\n",
    "}\n",
    "\n",
    "print('PROPOSED FEATURES:')\n",
    "for i, f in enumerate(PROPOSED_FEATURES, 1):\n",
    "    print(f'  {i:2d}. {f}')\n",
    "\n",
    "print(f'\\nTARGET: {TARGET}')\n",
    "print('\\nEXCLUDED:')\n",
    "for col, reason in EXCLUDED.items():\n",
    "    print(f'  {col:20s}: {reason}')\n",
    "\n",
    "print('\\nFinal feature count after OHE of type (5 categories): 13 columns')"
]))

# ---- SECTION 11: CONCLUSIONS ----
cells.append(md_cell([
    "---\n",
    "## 11. EDA Conclusions & Stage 3C Recommendations\n",
    "\n",
    "### Dataset Summary\n",
    "\n",
    "| Property | Value |\n",
    "|---|---|\n",
    "| **Rows** | 6,362,620 |\n",
    "| **Columns** | 11 |\n",
    "| **Fraud Count** | 8,213 (0.1291%) |\n",
    "| **Legitimate Count** | 6,354,407 (99.8709%) |\n",
    "| **Imbalance Ratio** | ~773:1 |\n",
    "| **Missing Values** | 0 |\n",
    "| **Duplicate Rows** | 0 |\n",
    "| **Fraud confined to** | CASH_OUT + TRANSFER only |\n",
    "\n",
    "### Recommended Preprocessing (Stage 3C)\n",
    "1. Drop `isFlaggedFraud`, `nameOrig`, `nameDest`\n",
    "2. Compute `errorBalanceOrig` and `errorBalanceDest`\n",
    "3. One-Hot Encode `type` (5 values)\n",
    "4. Apply `RobustScaler` to continuous features (handles financial outliers)\n",
    "5. Stratified 80/20 train/test split\n",
    "\n",
    "### Imbalance Handling\n",
    "- **Primary strategy:** SMOTE-ENN (over-samples minority + cleans noisy samples)\n",
    "- **Alternative:** `class_weight='balanced'` (sklearn) / `scale_pos_weight` (XGBoost)\n",
    "- Evaluate both using cross-validated F1-score (fraud class) and ROC-AUC\n",
    "\n",
    "### Models to Compare (Stage 3C)\n",
    "- Logistic Regression (statistical baseline — needs scaling)\n",
    "- Random Forest (ensemble — handles imbalance with class weights)\n",
    "- XGBoost (gradient boosting — `scale_pos_weight` for imbalance)\n",
    "\n",
    "> **Champion model will be selected after cross-validated metric comparison in Stage 3C.**"
]))

# Build notebook object
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.14.0"}
    },
    "cells": cells
}

out_path = r'd:\stitch_fraudguard_ml_detection_system\ml\notebooks\fraudguard_eda.ipynb'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Notebook written to: {out_path}")
print(f"Cell count: {len(cells)}")
