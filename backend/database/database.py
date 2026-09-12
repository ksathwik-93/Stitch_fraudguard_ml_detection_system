"""
Database access and query utilities for FraudGuard SQLite database.
"""

import os
import sqlite3
from typing import Dict, Any, List, Optional, Tuple
from .schema import CREATE_TRANSACTIONS_TABLE, CREATE_INDICES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "fraudguard.db")


def get_db_path() -> str:
    """Return the absolute path to the SQLite database file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    return DB_PATH


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with Row row factory."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables and indices if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_TRANSACTIONS_TABLE)
        for idx_sql in CREATE_INDICES:
            cursor.execute(idx_sql)
        conn.commit()


def check_db_health() -> bool:
    """Verify database connectivity."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            return cursor.fetchone() is not None
    except Exception:
        return False


def insert_transaction(tx_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a processed transaction record into SQLite.
    Returns the inserted transaction dictionary with its auto-generated id.
    """
    insert_sql = """
    INSERT INTO transactions (
        transaction_id, created_at, step, type, amount,
        oldbalance_org, newbalance_orig, oldbalance_dest, newbalance_dest,
        error_balance_orig, error_balance_dest,
        fraud_probability, prediction, risk_level
    ) VALUES (
        :transaction_id, :created_at, :step, :type, :amount,
        :oldbalance_org, :newbalance_orig, :oldbalance_dest, :newbalance_dest,
        :error_balance_orig, :error_balance_dest,
        :fraud_probability, :prediction, :risk_level
    );
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(insert_sql, tx_data)
        row_id = cursor.lastrowid
        conn.commit()

        cursor.execute("SELECT * FROM transactions WHERE id = ?", (row_id,))
        row = cursor.fetchone()
        return dict(row) if row else tx_data


def get_transactions(
    page: int = 1,
    limit: int = 20,
    search: Optional[str] = None,
    tx_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    prediction: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    Retrieve paginated transactions, newest first, with optional filters.
    Returns (transactions_list, total_count, total_pages).
    """
    page = max(1, int(page))
    limit = max(1, min(100, int(limit)))
    offset = (page - 1) * limit

    conditions = []
    params: List[Any] = []

    if search:
        search_pattern = f"%{search.strip()}%"
        conditions.append("(transaction_id LIKE ? OR type LIKE ?)")
        params.extend([search_pattern, search_pattern])

    if tx_type:
        conditions.append("UPPER(type) = UPPER(?)")
        params.append(tx_type.strip())

    if risk_level:
        conditions.append("UPPER(risk_level) = UPPER(?)")
        params.append(risk_level.strip())

    if prediction:
        conditions.append("UPPER(prediction) = UPPER(?)")
        params.append(prediction.strip())

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    count_sql = f"SELECT COUNT(*) AS total FROM transactions {where_clause};"
    query_sql = f"""
    SELECT * FROM transactions
    {where_clause}
    ORDER BY id DESC
    LIMIT ? OFFSET ?;
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(count_sql, params)
        total_count = cursor.fetchone()["total"]

        total_pages = (total_count + limit - 1) // limit if total_count > 0 else 1

        cursor.execute(query_sql, params + [limit, offset])
        rows = cursor.fetchall()
        transactions = [dict(row) for row in rows]

    return transactions, total_count, total_pages


def get_dashboard_stats() -> Dict[str, Any]:
    """
    Calculate dashboard aggregate metrics and recent transactions directly from SQLite.
    Handles zero transactions safely.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        # Total counts and probabilities
        stats_sql = """
        SELECT
            COUNT(*) AS total_transactions,
            COALESCE(SUM(CASE WHEN UPPER(prediction) = 'FRAUD' OR UPPER(risk_level) = 'HIGH' THEN 1 ELSE 0 END), 0) AS fraud_detected,
            COALESCE(SUM(CASE WHEN UPPER(prediction) != 'FRAUD' AND UPPER(risk_level) != 'HIGH' THEN 1 ELSE 0 END), 0) AS legitimate,
            COALESCE(AVG(fraud_probability), 0.0) AS avg_fraud_prob
        FROM transactions;
        """
        cursor.execute(stats_sql)
        row = cursor.fetchone()

        total = row["total_transactions"]
        fraud_count = row["fraud_detected"]
        legit_count = row["legitimate"]
        avg_prob = float(row["avg_fraud_prob"])

        fraud_rate = round((fraud_count / total * 100.0), 2) if total > 0 else 0.0
        avg_fraud_prob = round(avg_prob, 2)

        # Recent transactions (up to 10 newest)
        cursor.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 10;")
        recent_rows = cursor.fetchall()
        recent_transactions = [dict(r) for r in recent_rows]

        # Risk distribution counts
        cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN UPPER(risk_level) = 'HIGH' THEN 1 ELSE 0 END), 0) AS high_risk,
            COALESCE(SUM(CASE WHEN UPPER(risk_level) = 'MEDIUM' THEN 1 ELSE 0 END), 0) AS medium_risk,
            COALESCE(SUM(CASE WHEN UPPER(risk_level) = 'LOW' THEN 1 ELSE 0 END), 0) AS low_risk
        FROM transactions;
        """)
        risk_row = cursor.fetchone()

    return {
        "total_transactions": total,
        "fraud_detected": fraud_count,
        "legitimate": legit_count,
        "fraud_rate": fraud_rate,
        "avg_fraud_prob": avg_fraud_prob,
        "risk_distribution": {
            "high": risk_row["high_risk"] if risk_row else 0,
            "medium": risk_row["medium_risk"] if risk_row else 0,
            "low": risk_row["low_risk"] if risk_row else 0,
        },
        "recent_transactions": recent_transactions,
    }
