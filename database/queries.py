from database.db import get_db
from datetime import datetime


def get_user_by_id(user_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if row is None:
        return None
    member_since = datetime.strptime(row["created_at"][:7], "%Y-%m").strftime("%B %Y")
    return {"name": row["name"], "email": row["email"], "member_since": member_since}


def get_summary_stats(user_id: int) -> dict:
    conn = get_db()
    row = conn.execute(
        """
        SELECT
            COALESCE(SUM(amount), 0.0) AS total_spent,
            COUNT(*)                   AS transaction_count,
            (
                SELECT category FROM expenses
                WHERE user_id = ?
                GROUP BY category
                ORDER BY SUM(amount) DESC
                LIMIT 1
            ) AS top_category
        FROM expenses
        WHERE user_id = ?
        """,
        (user_id, user_id),
    ).fetchone()
    conn.close()
    return {
        "total_spent":       row["total_spent"],
        "transaction_count": row["transaction_count"],
        "top_category":      row["top_category"] or "—",
    }


def get_recent_transactions(user_id: int, limit: int = 10) -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        """
        SELECT amount, category, date, description
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC, created_at DESC
        LIMIT ?
        """,
        (user_id, limit),
    ).fetchall()
    conn.close()
    return [
        {
            "date":        row["date"],
            "description": row["description"] or "—",
            "category":    row["category"],
            "amount":      row["amount"],
        }
        for row in rows
    ]


def get_category_breakdown(user_id: int) -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        """
        SELECT category, SUM(amount) AS amount
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY amount DESC
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    if not rows:
        return []
    total = sum(row["amount"] for row in rows)
    result = [
        {"name": row["category"], "amount": row["amount"], "pct": int(row["amount"] / total * 100)}
        for row in rows
    ]
    # Largest-remainder correction: int() always floors so remainder >= 0
    result[0]["pct"] += 100 - sum(r["pct"] for r in result)
    return result
