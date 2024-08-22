from datetime import datetime
from typing import Dict, Optional

from app.core.config import custom_logger
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS arcan_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arcan INTEGER NOT NULL,
                month TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(arcan, month)
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cover_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                arcan INTEGER NOT NULL,
                like_last BOOLEAN DEFAULT NULL,
                has_paid BOOLEAN DEFAULT FALSE,
                attempts_left INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id)
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cover_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """
        )
        conn.commit()


@custom_logger.log_db_operation
def add_arcan_description(arcan: int, description: str, month: str = None):
    # month = datetime.now().strftime("%Y-%m")
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO arcan_descriptions (arcan, month, description) VALUES (?, ?, ?)",
            (arcan, month, description),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_arcan_description(arcan: int) -> Optional[str]:
    month = datetime.now().strftime("%Y-%m")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT description FROM arcan_descriptions WHERE arcan = ? AND month = ?",
            (arcan, month),
        )
        result = cursor.fetchone()
        return result[0] if result else None


@custom_logger.log_db_operation
def init_cover_user(user_id: int, arcan: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO cover_users (user_id, arcan) VALUES (?, ?)",
            (user_id, arcan),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_like_cover(user_id: int, like: bool):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cover_users SET like_last = ? WHERE user_id = ?",
            (like, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def update_user_payment(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cover_users SET has_paid = TRUE, attempts_left = attempts_left + 10 WHERE user_id = ?",
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def decrement_user_attempts(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cover_users SET attempts_left = attempts_left - 1 WHERE user_id = ? AND attempts_left > 0",
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def increment_user_attempts(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cover_users SET attempts_left = attempts_left + 1 WHERE user_id = ?",
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_user_attempts(user_id: int) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT attempts_left FROM cover_users WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        return result["attempts_left"] if result else 0


@custom_logger.log_db_operation
def record_transaction(user_id: int, amount: float):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cover_transactions (user_id, amount) VALUES (?, ?)",
            (user_id, amount),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_all_arcan_descriptions(month: str) -> Dict[int, Dict]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT arcan, description FROM arcan_descriptions WHERE month = ?",
            (month,),
        )
        results = cursor.fetchall()
        # return {row["arcan"]: dict(row) for row in results}
        return {row[0]: row for row in results}
