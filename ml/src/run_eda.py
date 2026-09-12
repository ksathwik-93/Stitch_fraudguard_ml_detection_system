import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.family': 'sans-serif'})

data_path = r"d:\stitch_fraudguard_ml_detection_system\ml\data\PS_20174392719_1491204439457_log.csv"
results_dir = r"d:\stitch_fraudguard_ml_detection_system\ml\results"
os.makedirs(results_dir, exist_ok=True)

print(f"Loading dataset from: {data_path}", flush=True)
df = pd.read_csv(data_path)
print("Dataset loaded successfully!", flush=True)

print("="*60, flush=True)
print("DATASET OVERVIEW", flush=True)
print("="*60, flush=True)
num_rows, num_cols = df.shape
print(f"Number of rows: {num_rows:,}", flush=True)
print(f"Number of columns: {num_cols}", flush=True)
print(f"Column names: {list(df.columns)}", flush=True)
print("\nData Types:", flush=True)
print(df.dtypes, flush=True)

print("\nMissing Values:", flush=True)
missing = df.isnull().sum()
print(missing, flush=True)

print("\nDuplicate Rows Count:", flush=True)
duplicates = df.duplicated().sum()
print(f"Duplicates: {duplicates}", flush=True)

print("\nCategorical Features Unique Values:", flush=True)
for col in ['type', 'nameOrig', 'nameDest']:
    if col in df.columns:
        print(f"  {col}: {df[col].nunique():,} unique values", flush=True)

print("\nNumerical Statistics:", flush=True)
print(df.describe().T[['count', 'mean', 'std', 'min', '50%', 'max']], flush=True)

print("="*60, flush=True)
print("FRAUD CLASS DISTRIBUTION", flush=True)
print("="*60, flush=True)
fraud_counts = df['isFraud'].value_counts()
legit_count = int(fraud_counts.get(0, 0))
fraud_count = int(fraud_counts.get(1, 0))
legit_pct = (legit_count / num_rows) * 100
fraud_pct = (fraud_count / num_rows) * 100

print(f"Legitimate Transactions (0): {legit_count:,} ({legit_pct:.4f}%)", flush=True)
print(f"Fraudulent Transactions (1): {fraud_count:,} ({fraud_pct:.4f}%)", flush=True)

# Plot Class Distribution
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#10B981', '#EF4444']
bars = ax.bar(['Legitimate (0)', 'Fraud (1)'], [legit_count, fraud_count], color=colors, width=0.5)
ax.set_yscale('log')
ax.set_title('Transaction Class Distribution (Log Scale)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Number of Transactions (Log Scale)', fontsize=12)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:,}\n({height/num_rows*100:.3f}%)',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
class_dist_path = os.path.join(results_dir, 'class_distribution.png')
plt.savefig(class_dist_path, dpi=300)
plt.close()
print(f"Saved: {class_dist_path}", flush=True)

print("="*60, flush=True)
print("TRANSACTION TYPE ANALYSIS", flush=True)
print("="*60, flush=True)
type_stats = df.groupby('type').agg(
    total_count=('isFraud', 'count'),
    fraud_count=('isFraud', lambda x: (x == 1).sum()),
    legit_count=('isFraud', lambda x: (x == 0).sum())
).reset_index()
type_stats['fraud_percentage'] = (type_stats['fraud_count'] / type_stats['total_count']) * 100
print(type_stats.to_string(index=False), flush=True)

# Plot Fraud by Transaction Type
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Total Volume by Type
sns.barplot(data=type_stats, x='type', y='total_count', ax=ax1, palette='Blues_r')
ax1.set_title('Total Transaction Volume by Type', fontsize=13, fontweight='bold')
ax1.set_ylabel('Count', fontsize=11)
ax1.set_xlabel('Transaction Type', fontsize=11)
for p in ax1.patches:
    ax1.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

# Fraud Count by Type
sns.barplot(data=type_stats, x='type', y='fraud_count', ax=ax2, palette='Reds_r')
ax2.set_title('Fraud Transactions Count by Type', fontsize=13, fontweight='bold')
ax2.set_ylabel('Fraud Count', fontsize=11)
ax2.set_xlabel('Transaction Type', fontsize=11)
for p in ax2.patches:
    ax2.annotate(f'{int(p.get_height()):,}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=9, xytext=(0, 3), textcoords='offset points')

plt.tight_layout()
fraud_type_path = os.path.join(results_dir, 'fraud_by_transaction_type.png')
plt.savefig(fraud_type_path, dpi=300)
plt.close()
print(f"Saved: {fraud_type_path}", flush=True)

print("="*60, flush=True)
print("NUMERICAL FEATURE ANALYSIS", flush=True)
print("="*60, flush=True)
print("\nAmount Statistics by Class:", flush=True)
print(df.groupby('isFraud')['amount'].describe().T, flush=True)

# Amount distribution plot
fig, ax = plt.subplots(figsize=(10, 5))
sns.kdeplot(data=df[df['isFraud'] == 0]['amount'], ax=ax, label='Legitimate', color='#10B981', log_scale=True, fill=True, alpha=0.3)
sns.kdeplot(data=df[df['isFraud'] == 1]['amount'], ax=ax, label='Fraudulent', color='#EF4444', log_scale=True, fill=True, alpha=0.3)
ax.set_title('Transaction Amount Distribution (Log Scale)', fontsize=14, fontweight='bold')
ax.set_xlabel('Amount (Log Scale)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend()
plt.tight_layout()
amount_dist_path = os.path.join(results_dir, 'amount_distribution.png')
plt.savefig(amount_dist_path, dpi=300)
plt.close()
print(f"Saved: {amount_dist_path}", flush=True)

# Feature Analysis Grid (Origin & Destination balances)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. oldbalanceOrg vs isFraud (Subsample for fast boxplot)
sample_df = df.sample(n=100000, random_state=42)
sns.boxplot(data=sample_df, x='isFraud', y='oldbalanceOrg', ax=axes[0,0], palette=['#10B981', '#EF4444'])
axes[0,0].set_yscale('log')
axes[0,0].set_title('oldbalanceOrg by Class (Log Scale Sample)', fontweight='bold')
axes[0,0].set_xticklabels(['Legitimate (0)', 'Fraud (1)'])

# 2. newbalanceOrig vs isFraud
sns.boxplot(data=sample_df, x='isFraud', y='newbalanceOrig', ax=axes[0,1], palette=['#10B981', '#EF4444'])
axes[0,1].set_yscale('log')
axes[0,1].set_title('newbalanceOrig by Class (Log Scale Sample)', fontweight='bold')
axes[0,1].set_xticklabels(['Legitimate (0)', 'Fraud (1)'])

# 3. oldbalanceDest vs isFraud
sns.boxplot(data=sample_df, x='isFraud', y='oldbalanceDest', ax=axes[1,0], palette=['#10B981', '#EF4444'])
axes[1,0].set_yscale('log')
axes[1,0].set_title('oldbalanceDest by Class (Log Scale Sample)', fontweight='bold')
axes[1,0].set_xticklabels(['Legitimate (0)', 'Fraud (1)'])

# 4. Step distribution by Class
sns.histplot(data=sample_df, x='step', hue='isFraud', bins=50, ax=axes[1,1], palette=['#10B981', '#EF4444'], stat='density', common_norm=False)
axes[1,1].set_title('Step (Time) Distribution by Class (Sample)', fontweight='bold')

plt.tight_layout()
feature_analysis_path = os.path.join(results_dir, 'feature_analysis.png')
plt.savefig(feature_analysis_path, dpi=300)
plt.close()
print(f"Saved: {feature_analysis_path}", flush=True)

print("="*60, flush=True)
print("isFlaggedFraud ANALYSIS", flush=True)
print("="*60, flush=True)
flagged_counts = df['isFlaggedFraud'].value_counts()
print(f"isFlaggedFraud Counts:\n{flagged_counts}", flush=True)
flagged_fraud_match = pd.crosstab(df['isFlaggedFraud'], df['isFraud'])
print("\nisFlaggedFraud vs isFraud Cross-tabulation:", flush=True)
print(flagged_fraud_match, flush=True)

print("="*60, flush=True)
print("FEATURE ENGINEERING ANALYSIS", flush=True)
print("="*60, flush=True)
df['errorBalanceOrig'] = df['oldbalanceOrg'] - df['amount'] - df['newbalanceOrig']
df['errorBalanceDest'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']
df['hour'] = df['step'] % 24

print("\nEngineered Feature Correlation with isFraud:", flush=True)
num_cols_to_corr = ['isFraud', 'errorBalanceOrig', 'errorBalanceDest', 'hour', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']
corr = df[num_cols_to_corr].corr()['isFraud']
print(corr.sort_values(ascending=False), flush=True)

print("\nExecution complete!", flush=True)
