from datetime import datetime
from typing import List, Optional

from app.core.config import custom_logger
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def is_first_time_in_city(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT have_free_try FROM city WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result is None
        # return result is None or result[0]


@custom_logger.log_db_operation
def which_arcan(user_id: int) -> Optional[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT arcan FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result["arcan"] if result else None


@custom_logger.log_db_operation
def add_user_to_city_table(user_id: int):
    print("here")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO city (user_id, have_free_try) VALUES (?, 2)",
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_free_try_used(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE city SET have_free_try = have_free_try - 1 WHERE user_id = ? AND have_free_try > 0",
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def has_free_try(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT have_free_try FROM city WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return bool(result and result["have_free_try"] > 0)


@custom_logger.log_db_operation
def set_unlimited_city_compatibility(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE city SET have_pay = TRUE WHERE user_id = ?", (user_id,)
        )
        conn.commit()


@custom_logger.log_db_operation
def has_unlimited_city_compatibility(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT have_pay FROM city WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return bool(result and result["have_pay"])


@custom_logger.log_db_operation
def add_checked_city(user_id: int, city_name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT cities_checked FROM city WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        if result and result["cities_checked"]:
            cities = result["cities_checked"].split(",")
            if city_name not in cities:
                cities.append(city_name)
                new_cities = ",".join(cities)
                cursor.execute(
                    "UPDATE city SET cities_checked = ? WHERE user_id = ?",
                    (new_cities, user_id),
                )
        else:
            cursor.execute(
                "UPDATE city SET cities_checked = ? WHERE user_id = ?",
                (city_name, user_id),
            )
        conn.commit()


@custom_logger.log_db_operation
def get_checked_cities(user_id: int) -> List[str]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT cities_checked FROM city WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return (
            result["cities_checked"].split(",")
            if result and result["cities_checked"]
            else []
        )


@custom_logger.log_db_operation
def record_city_transaction(user_id: int, amount: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        current_time = datetime.now()
        cursor.execute(
            "INSERT INTO city_transactions (user_id, amount, date) VALUES (?, ?, ?)",
            (user_id, amount, current_time),
        )
        cursor.execute(
            "UPDATE city SET last_transaction_date = ? WHERE user_id = ?",
            (current_time, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_user_city_transactions(user_id: int, limit: int = 5) -> List[dict]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT amount, date FROM city_transactions WHERE user_id = ? ORDER BY date DESC LIMIT ?",
            (user_id, limit),
        )
        return [
            {"amount": row["amount"], "date": row["date"]}
            for row in cursor.fetchall()
        ]


@custom_logger.log_db_operation
def get_free_tries_left(user_id: int) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT have_free_try FROM city WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result["have_free_try"] if result else 0
