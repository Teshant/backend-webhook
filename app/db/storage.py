from datetime import datetime
from typing import Dict, Any
from app.db.models import get_db_connection


def insert_message(data: Dict[str, Any]) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO messages (
                message_id, from_msisdn, to_msisdn, ts, text, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["message_id"],
                data["from"],
                data["to"],
                data["ts"],
                data.get("text"),
                datetime.utcnow().isoformat() + "Z",
            ),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def fetch_messages(limit, offset, from_msisdn=None, since=None, q=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    filters = []
    params = []

    if from_msisdn:
        filters.append("from_msisdn = ?")
        params.append(from_msisdn)

    if since:
        filters.append("ts >= ?")
        params.append(since)

    if q:
        filters.append("LOWER(text) LIKE ?")
        params.append(f"%{q.lower()}%")

    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    total = cursor.execute(
        f"SELECT COUNT(*) FROM messages {where_clause}", params
    ).fetchone()[0]

    rows = cursor.execute(
        f"""
        SELECT * FROM messages
        {where_clause}
        ORDER BY ts ASC, message_id ASC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    ).fetchall()

    conn.close()

    return {
        "data": [dict(row) for row in rows],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def fetch_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    total = cursor.execute(
        "SELECT COUNT(*) FROM messages"
    ).fetchone()[0]

    senders = cursor.execute(
        """
        SELECT from_msisdn AS sender, COUNT(*) AS count
        FROM messages
        GROUP BY from_msisdn
        ORDER BY count DESC
        LIMIT 10
        """
    ).fetchall()

    first_ts = cursor.execute(
        "SELECT MIN(ts) FROM messages"
    ).fetchone()[0]

    last_ts = cursor.execute(
        "SELECT MAX(ts) FROM messages"
    ).fetchone()[0]

    conn.close()

    return {
        "total_messages": total,
        "senders_count": len(senders),
        "messages_per_sender": [
            {"from": row["sender"], "count": row["count"]}
            for row in senders
        ],
        "first_message_ts": first_ts,
        "last_message_ts": last_ts,
    }
