import hashlib
from datetime import datetime
from typing import List, Optional

# from venv import logger
from app.core.config import custom_logger, settings
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


# @custom_logger.log_db_operation
# def record_city_transaction(user_id: int, amount: int, status: bool):
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         current_time = datetime.now()
#         if not status:
#             cursor.execute(
#                 "INSERT INTO city_transactions (user_id, amount, create_date, status) VALUES (?, ?, ?, ?)",
#                 (user_id, amount, current_time, status),
#             )
#         else:
#             cursor.execute(
#                 "INSERT INTO city_transactions (user_id, amount, pay_date, status) VALUES (?, ?, ?, ?)",
#                 (user_id, amount, current_time, status),
#             )
#             cursor.execute(
#                 "UPDATE city SET last_transaction_date = ? WHERE user_id = ?",
#                 (current_time, user_id),
#             )

#         conn.commit()


# @custom_logger.log_db_operation
# def record_city_transaction(user_id: int, amount: int, status: bool = False):
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         current_time = datetime.now()

#         # Check if a transaction exists for the user
#         cursor.execute(
#             "SELECT id FROM city_transactions WHERE user_id = ? ORDER BY create_date DESC LIMIT 1",
#             (user_id,),
#         )
#         existing_transaction = cursor.fetchone()

#         if existing_transaction:
#             # Update existing transaction
#             if not status:
#                 cursor.execute(
#                     "UPDATE city_transactions SET amount = ?, create_date = ?, status = ? WHERE id = ?",
#                     (amount, current_time, status, existing_transaction[0]),
#                 )
#             else:
#                 cursor.execute(
#                     "UPDATE city_transactions SET amount = ?, pay_date = ?, status = ? WHERE id = ?",
#                     (amount, current_time, status, existing_transaction[0]),
#                 )
#         else:
#             # Insert new transaction
#             if not status:
#                 cursor.execute(
#                     "INSERT INTO city_transactions (user_id, amount, create_date, status) VALUES (?, ?, ?, ?)",
#                     (user_id, amount, current_time, status),
#                 )
#             else:
#                 cursor.execute(
#                     "INSERT INTO city_transactions (user_id, amount, pay_date, status) VALUES (?, ?, ?, ?)",
#                     (user_id, amount, current_time, status),
#                 )

#         # Update city table if status is True (this remains the same)
#         if status:
#             cursor.execute(
#                 "UPDATE city SET last_transaction_date = ? WHERE user_id = ?",
#                 (current_time, user_id),
#             )


#         conn.commit()
@custom_logger.log_db_operation
def record_city_transaction(user_id: int, amount: int, status: bool = False):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        current_time = datetime.now()

        # Check if a transaction exists for the user
        cursor.execute(
            "SELECT id FROM city_transactions WHERE user_id = ? ORDER BY create_date DESC LIMIT 1",
            (user_id,),
        )
        existing_transaction = cursor.fetchone()

        if existing_transaction:
            # Update existing transaction
            transaction_id = existing_transaction[0]
            if not status:
                cursor.execute(
                    "UPDATE city_transactions SET amount = ?, create_date = ?, status = ? WHERE id = ?",
                    (amount, current_time, status, transaction_id),
                )
            else:
                cursor.execute(
                    "UPDATE city_transactions SET amount = ?, pay_date = ?, status = ? WHERE id = ?",
                    (amount, current_time, status, transaction_id),
                )
        else:
            # Insert new transaction
            if not status:
                cursor.execute(
                    "INSERT INTO city_transactions (user_id, amount, create_date, status) VALUES (?, ?, ?, ?)",
                    (user_id, amount, current_time, status),
                )
            else:
                cursor.execute(
                    "INSERT INTO city_transactions (user_id, amount, pay_date, status) VALUES (?, ?, ?, ?)",
                    (user_id, amount, current_time, status),
                )
            transaction_id = cursor.lastrowid

        # Update city table if status is True (this remains the same)
        if status:
            cursor.execute(
                "UPDATE city SET last_transaction_date = ? WHERE user_id = ?",
                (current_time, user_id),
            )

        conn.commit()

    return transaction_id


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


@custom_logger.log_db_operation
def add_task_city_transaction(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO task_city_transactions (user_id) VALUES (?)",
            (user_id,),
        )
        # task_city_transactions
        conn.commit()


@custom_logger.log_db_operation
def del_task_city_transaction(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM task_city_transactions WHERE user_id = ?", (user_id,)
        )

        # task_city_transactions
        conn.commit()


@custom_logger.log_db_operation
def get_all_task_city_transaction():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM task_city_transactions")

        return cursor.fetchall()


# @custom_logger.log_db_operation
# def check_signature(transaction_id, signature_value) -> bool:
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT user_id, amount FROM city_transactions WHERE id = ?",
#             (transaction_id),
#         )
#         result = cursor.fetchone()
#         print(f"REEES = {result}")
#         if result:
#             user_id = result["user_id"]
#             amount = result["amount"]
#             print(
#                 f"HERE:{amount}:{transaction_id}:{settings.ACTIVE_ROBOKASSA_PASSWORD2}:Shp_id= {user_id}\n"
#             )
#             check_signature = hashlib.md5(
#                 f"{amount}:{transaction_id}:{settings.ACTIVE_ROBOKASSA_PASSWORD2}:Shp_id= {user_id} :".encode()
#             ).hexdigest()
#             if check_signature == signature_value:
#                 print("GOOOOD CHECK")
#                 return True
#         print("BAD CHECK")
#         return False


@custom_logger.log_db_operation
def check_signature(inv_id, signature_value, out_sum, shp_id) -> bool:
    # Примечание: out_sum и shp_id теперь передаются в функцию
    check_string = f"{out_sum}:{inv_id}:{settings.ACTIVE_ROBOKASSA_PASSWORD2}:Shp_id={shp_id}"
    check_signature = hashlib.md5(check_string.encode()).hexdigest().upper()
    print(f"Check string: {check_string}")
    print(f"Calculated signature: {check_signature}")
    print(f"Received signature: {signature_value}")
    return check_signature == signature_value.upper()
    # return result["have_free_try"] if result else 0


# @custom_logger.log_db_operation
# def get_last_transaction_id() -> int:
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT id FROM city_transactions ORDER BY id DESC LIMIT 1"
#         )
#         result = cursor.fetchone()
#         if result:
#             return result[0]
#         else:
#             return 0  # Возвращаем 0, если транзакций нет


async def get_last_transaction_id_from_db() -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM city_transactions ORDER BY id DESC LIMIT 1"
        )
        result = cursor.fetchone()
        return result[0] if result else 0
