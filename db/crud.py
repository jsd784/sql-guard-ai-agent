import os
import sqlite3
from sqlite3 import Row

from fastapi import HTTPException, status

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "chinook.db")


# DB_FILE = "chinook.db"


def run_sql(query: str, params: tuple = ()) -> list:
    """Run any SQL query (SELECT, INSERT, etc.) on the DB."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
        conn.commit()
        return []


def create_access_log(ip: str, sql: str, risk: str, banned: bool = False):
    """Create a new access log entry."""
    query = """
    INSERT INTO AccessLog (ip, sql, risk, banned)
    VALUES (?, ?, ?, ?);
    """
    run_sql(query, (ip, sql, risk, banned))


def is_ip_banned(ip: str) -> bool:
    """Check if the given IP is banned in the AccessLog."""
    query = "SELECT banned FROM AccessLog WHERE ip = ?;"
    results = run_sql(query, (ip,))
    return any(bool(row[0]) for row in results)


def update_access_log(log_id: int, **kwargs):
    """Update fields in an access log entry. Fields can include ip, sql, risk, banned."""
    fields = []
    values = []
    for key, val in kwargs.items():
        fields.append(f"{key} = ?")
        values.append(val)
    values.append(log_id)

    query = f"""
    UPDATE AccessLog
    SET {', '.join(fields)}
    WHERE id = ?;
    """
    run_sql(query, tuple(values))


def delete_access_log(log_id: int):
    """Delete an access log entry."""
    query = "DELETE FROM AccessLog WHERE id = ?;"
    run_sql(query, (log_id,))


def get_data_in_json(sql_query: str) -> list:
    """
    Execute a SELECT query and return the result as a JSON-compatible list of dictionaries.
    For non-SELECT queries, return "executed".
    """
    if sql_query.strip().lower().startswith("select"):
        try:
            with sqlite3.connect(db_path) as conn:
                conn.row_factory = Row  # Enable row factory for dict-like rows
                cursor = conn.cursor()
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]  # Convert rows to list of dicts
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error executing SELECT query: {e}",
            )
    else:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                conn.commit()
                return "executed"
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error executing non-SELECT query: {e}",
            )


# --- Example usage ---
if __name__ == "__main__":
    # Add a sample entry
    # create_access_log(ip="192.168.1.1", sql="SELECT * FROM Customers;", risk="low")

    # Run a query to test
    # print(run_sql("SELECT * FROM AccessLog LIMIT 1;"))

    # Update that entry by log_id
    # update_access_log(log_id=4, banned=True, risk="medium")

    # # Delete the entry  by log_id
    # delete_access_log(log_id=1)

    # check if IP is banned
    print(is_ip_banned("192.168.1.1"))

    # Run a query on Chinook database tables
    # print(run_sql("SELECT * FROM genres LIMIT 5;"))
