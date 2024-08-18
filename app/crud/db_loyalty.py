import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from app.core.config import custom_logger
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def add_user_to_loyalty(
    user_id: int, referrer_id: Optional[int] = None
) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO loyalty (user_id, referrer_id) VALUES (?, ?)",
                (user_id, referrer_id),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


@custom_logger.log_db_operation
def get_user_balance(user_id: int) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT balance FROM loyalty WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result["balance"] if result else 0


@custom_logger.log_db_operation
def update_user_balance(
    user_id: int, points: int, no_transaction: bool = False
):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if no_transaction:
            cursor.execute(
                "UPDATE loyalty SET balance = balance + ? WHERE user_id = ?",
                (points, user_id),
            )
        else:
            cursor.execute(
                "UPDATE loyalty SET balance = balance + ?, last_transaction_date = ? WHERE user_id = ?",
                (points, datetime.now(), user_id),
            )
        conn.commit()


@custom_logger.log_db_operation
def user_exists(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM loyalty WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None


@custom_logger.log_db_operation
def record_transaction(
    user_id: int,
    amount: int,
    bonus: int,
    service: str,
    expiration_days: Optional[int] = None,
):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO transactions (user_id, amount, bonus, service, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, bonus, service, datetime.now()),
        )

        cursor.execute(
            """
            UPDATE loyalty 
            SET balance = balance + ?,
                total_spent = total_spent + ?, 
                count_of_transaction = count_of_transaction + 1,
                last_transaction_date = ?
            WHERE user_id = ?
            """,
            (bonus, amount, datetime.now(), user_id),
        )

        if not get_promo_code(user_id):
            generate_promo_code(user_id)

        if expiration_days is not None:
            add_expiration_bonus(user_id, bonus, expiration_days)

        conn.commit()


@custom_logger.log_db_operation
def add_expiration_bonus(user_id: int, bonus: int, expiration_days: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        add_date = datetime.now()
        expire_date = add_date + timedelta(days=expiration_days)

        cursor.execute(
            """
            INSERT INTO expiration_bonus_movement (user_id, bonus, add_date, expire_date)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, bonus, add_date, expire_date),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_count_of_transaction(user_id: int) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT count_of_transaction FROM loyalty WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        return result["count_of_transaction"] if result else 0


@custom_logger.log_db_operation
def get_user_transactions(
    user_id: int, limit: Optional[int] = 10
) -> List[dict]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if limit is None:
            cursor.execute(
                "SELECT amount, bonus, service, date FROM transactions WHERE user_id = ? ORDER BY date DESC",
                (user_id,),
            )
        else:
            cursor.execute(
                "SELECT amount, bonus, service, date FROM transactions WHERE user_id = ? ORDER BY date DESC LIMIT ?",
                (user_id, limit),
            )
        return [dict(row) for row in cursor.fetchall()]


@custom_logger.log_db_operation
def is_new_loyalty_user(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM loyalty WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is None


@custom_logger.log_db_operation
def get_total_spent(user_id: int) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT total_spent FROM loyalty WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result["total_spent"] if result else 0


@custom_logger.log_db_operation
def use_promo_code(
    promo_code: str, new_user_id: Optional[int] = None
) -> Optional[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM loyalty WHERE promo_code = ?", (promo_code,)
        )
        result = cursor.fetchone()
        if result:
            referrer_id = result["user_id"]
            record_transaction(referrer_id, 0, 500, "За друга")
            if new_user_id:
                add_user_to_loyalty(new_user_id, referrer_id)
            return referrer_id
    return None


@custom_logger.log_db_operation
def deduct_points(user_id: int, points: int) -> Tuple[bool, int]:
    current_balance = get_user_balance(user_id)
    if current_balance >= points:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE loyalty SET balance = balance - ? WHERE user_id = ?",
                (points, user_id),
            )
            conn.commit()
        return True, current_balance - points
    else:
        return False, current_balance


@custom_logger.log_db_operation
def check_balance(user_id: int, points: int) -> Tuple[bool, int]:
    current_balance = get_user_balance(user_id)
    return current_balance >= points, current_balance


@custom_logger.log_db_operation
def get_referrer_id(user_id: int) -> Optional[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT referrer_id FROM loyalty WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result["referrer_id"] if result else None


@custom_logger.log_db_operation
def get_promo_code(user_id: int) -> Optional[str]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT promo_code FROM loyalty WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result["promo_code"] if result else None


@custom_logger.log_db_operation
def generate_promo_code(user_id: int) -> str:
    promo_code = f"PROMO{user_id}"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE loyalty SET promo_code = ? WHERE user_id = ?",
            (promo_code, user_id),
        )
        conn.commit()
    return promo_code


@custom_logger.log_db_operation
def get_loyalty_stats() -> Tuple[int, int, int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*), SUM(balance), SUM(total_spent)
            FROM loyalty
            """
        )
        return cursor.fetchone()
