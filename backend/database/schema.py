"""
Database schema definition for FraudGuard.
Table: transactions
"""

CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    step INTEGER NOT NULL,
    type TEXT NOT NULL,
    amount REAL NOT NULL,
    oldbalance_org REAL NOT NULL,
    newbalance_orig REAL NOT NULL,
    oldbalance_dest REAL NOT NULL,
    newbalance_dest REAL NOT NULL,
    error_balance_orig REAL NOT NULL,
    error_balance_dest REAL NOT NULL,
    fraud_probability REAL NOT NULL,
    prediction TEXT NOT NULL,
    risk_level TEXT NOT NULL
);
"""

CREATE_INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at DESC);",
    "CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);",
    "CREATE INDEX IF NOT EXISTS idx_transactions_risk_level ON transactions(risk_level);",
    "CREATE INDEX IF NOT EXISTS idx_transactions_prediction ON transactions(prediction);",
    "CREATE INDEX IF NOT EXISTS idx_transactions_tx_id ON transactions(transaction_id);"
]
