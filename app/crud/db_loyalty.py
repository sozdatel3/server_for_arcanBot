import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from typing import List, Optional, Tuple

from app.core.config import custom_logger
from app.core.database import get_db_connection


def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "connection" not in kwargs or kwargs["connection"] is None:
            with get_db_connection() as conn:
                return func(*args, **kwargs, connection=conn)
        else:
            return func(*args, **kwargs)

    return wrapper


@custom_logger.log_db_operation
@with_db_connection
def add_user_to_loyalty(
    user_id: int, referrer_id: Optional[int] = None, connection=None
) -> bool:
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO loyalty (user_id, referrer_id) VALUES (?, ?)",
            (user_id, referrer_id),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False


@custom_logger.log_db_operation
@with_db_connection
def get_user_balance(user_id: int, connection=None) -> int:
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM loyalty WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0


@custom_logger.log_db_operation
@with_db_connection
def update_user_balance(
    user_id: int, points: int, no_transaction: bool = False, connection=None
):
    cursor = connection.cursor()
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
    connection.commit()


@custom_logger.log_db_operation
@with_db_connection
def user_exists(user_id: int, connection=None) -> bool:
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM loyalty WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None


# @custom_logger.log_db_operation
# @with_db_connection
# def record_transaction(
#     user_id: int,
#     amount: int,
#     bonus: int,
#     service: str,
#     expiration_days: Optional[int] = None,
#     connection=None,
# ):
#     cursor = connection.cursor()
#     cursor.execute(
#         "INSERT INTO transactions (user_id, amount, bonus, service, date) VALUES (?, ?, ?, ?, ?)",
#         (user_id, amount, bonus, service, datetime.now()),
#     )
#     cursor.execute(
#         """
#         UPDATE loyalty
#         SET balance = balance + ?,
#             total_spent = total_spent + ?,
#             count_of_transaction = count_of_transaction + 1,
#             last_transaction_date = ?
#         WHERE user_id = ?
#         """,
#         (bonus, amount, datetime.now(), user_id),
#     )
#     if not get_promo_code(user_id, connection):
#         generate_promo_code(user_id, connection)
#     if expiration_days is not None:
#         add_expiration_bonus(user_id, bonus, expiration_days, connection)
#     connection.commit()


@custom_logger.log_db_operation
@with_db_connection
def add_expiration_bonus(
    user_id: int, bonus: int, expiration_days: int, connection=None
):
    cursor = connection.cursor()
    add_date = datetime.now()
    expire_date = add_date + timedelta(days=expiration_days)
    cursor.execute(
        """
        INSERT INTO expiration_bonus_movement (user_id, bonus, add_date, expire_date)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, bonus, add_date, expire_date),
    )
    connection.commit()


@custom_logger.log_db_operation
@with_db_connection
def get_count_of_transaction(user_id: int, connection=None) -> int:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT count_of_transaction FROM loyalty WHERE user_id = ?",
        (user_id,),
    )
    result = cursor.fetchone()
    return result[0] if result else 0


@custom_logger.log_db_operation
@with_db_connection
def get_user_transactions(
    user_id: int, limit: Optional[int] = 10, connection=None
) -> List[dict]:
    cursor = connection.cursor()
    if limit is None:
        cursor.execute(
            "SELECT amount, bonus, service, comment, date FROM transactions WHERE user_id = ? ORDER BY date DESC",
            (user_id,),
        )
    else:
        cursor.execute(
            "SELECT amount, bonus, service, comment, date FROM transactions WHERE user_id = ? ORDER BY date DESC LIMIT ?",
            (user_id, limit),
        )
    # print("HERE 2\n", [dict(row) for row in cursor.fetchall()])
    return [dict(row) for row in cursor.fetchall()]


@custom_logger.log_db_operation
@with_db_connection
def is_new_loyalty_user(user_id: int, connection=None) -> bool:
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM loyalty WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is None


@custom_logger.log_db_operation
@with_db_connection
def get_total_spent(user_id: int, connection=None) -> int:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT total_spent FROM loyalty WHERE user_id = ?", (user_id,)
    )
    result = cursor.fetchone()
    return result[0] if result else 0


@custom_logger.log_db_operation
@with_db_connection
def use_promo_code(
    promo_code: str, new_user_id: Optional[int] = None, connection=None
) -> Optional[int]:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT user_id FROM loyalty WHERE promo_code = ?", (promo_code,)
    )
    result = cursor.fetchone()
    if result:
        referrer_id = result["user_id"]
        record_transaction(
            referrer_id, 0, 500, "За друга", connection=connection
        )
        if new_user_id:
            add_user_to_loyalty(
                new_user_id, referrer_id, connection=connection
            )
        return referrer_id
    return None


@custom_logger.log_db_operation
@with_db_connection
def deduct_points(
    user_id: int, points: int, connection=None
) -> Tuple[bool, int]:
    current_balance = get_user_balance(user_id, connection=connection)
    if current_balance >= points:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE loyalty SET balance = balance - ? WHERE user_id = ?",
            (points, user_id),
        )
        connection.commit()
        return True, current_balance - points
    else:
        return False, current_balance


@custom_logger.log_db_operation
@with_db_connection
def check_balance(
    user_id: int, points: int, connection=None
) -> Tuple[bool, int]:
    current_balance = get_user_balance(user_id, connection=connection)
    return current_balance >= points, current_balance


@custom_logger.log_db_operation
@with_db_connection
def get_referrer_id(user_id: int, connection=None) -> Optional[int]:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT referrer_id FROM loyalty WHERE user_id = ?", (user_id,)
    )
    result = cursor.fetchone()
    return result[0] if result else None


@custom_logger.log_db_operation
@with_db_connection
def record_transaction(
    user_id: int,
    amount: int,
    bonus: int,
    service: str,
    comment: str,
    expiration_days: Optional[int] = None,
    connection=None,
):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, amount, bonus, service, comment, date) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, amount, bonus, service, comment, datetime.now()),
    )
    print("HERE", user_id, amount, bonus, service, comment, datetime.now())
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
    if not get_promo_code(user_id, connection=connection):
        generate_promo_code(user_id, connection=connection)
    if expiration_days is not None:
        add_expiration_bonus(
            user_id, bonus, expiration_days, connection=connection
        )
    connection.commit()


@custom_logger.log_db_operation
@with_db_connection
def get_promo_code(user_id: int, connection=None) -> Optional[str]:
    cursor = connection.cursor()
    cursor.execute(
        "SELECT promo_code FROM loyalty WHERE user_id = ?", (user_id,)
    )
    result = cursor.fetchone()
    return result[0] if result else None


@custom_logger.log_db_operation
@with_db_connection
def generate_promo_code(user_id: int, connection=None) -> str:
    promo_code = f"PROMO{user_id}"
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE loyalty SET promo_code = ? WHERE user_id = ?",
        (promo_code, user_id),
    )
    connection.commit()
    return promo_code


@custom_logger.log_db_operation
@with_db_connection
def get_loyalty_stats(connection=None) -> Tuple[int, int, int]:
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT COUNT(*), SUM(balance), SUM(total_spent)
        FROM loyalty
        """
    )
    return cursor.fetchone()


'''
@custom_logger.log_db_operation
def add_user_to_loyalty(
    user_id: int, referrer_id: Optional[int] = None, connection=None
) -> bool:
    if connection is None:
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
    else:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO loyalty (user_id, referrer_id) VALUES (?, ?)",
                (user_id, referrer_id),
            )
            connection.commit()
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
    connector=None,
):
    if connector is None:
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

            if not get_promo_code(user_id, conn):
                generate_promo_code(user_id, conn)

            if expiration_days is not None:
                add_expiration_bonus(user_id, bonus, expiration_days, conn)

            conn.commit()
    else:
        cursor = connector.cursor()
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
        if not get_promo_code(user_id, connector):
            generate_promo_code(user_id, connector)
        if expiration_days is not None:
            add_expiration_bonus(user_id, bonus, expiration_days, connector)
        connector.commit()


@custom_logger.log_db_operation
def add_expiration_bonus(
    user_id: int, bonus: int, expiration_days: int, connector=None
):
    if connector is None:
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
    else:
        cursor = connector.cursor()
        add_date = datetime.now()
        expire_date = add_date + timedelta(days=expiration_days)
        cursor.execute(
            """
            INSERT INTO expiration_bonus_movement (user_id, bonus, add_date, expire_date)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, bonus, add_date, expire_date),
        )
        connector.commit()


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
            record_transaction(referrer_id, 0, 500, "За друга", conn)
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
def get_promo_code(user_id: int, connector=None) -> Optional[str]:
    if connector is None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT promo_code FROM loyalty WHERE user_id = ?", (user_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
    else:
        cursor = connector.cursor()
        cursor.execute(
            "SELECT promo_code FROM loyalty WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else None


@custom_logger.log_db_operation
def generate_promo_code(user_id: int, connector=None) -> str:
    promo_code = f"PROMO{user_id}"
    if connector is None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE loyalty SET promo_code = ? WHERE user_id = ?",
                (promo_code, user_id),
            )
            conn.commit()
    else:
        cursor = connector.cursor()
        cursor.execute(
            "UPDATE loyalty SET promo_code = ? WHERE user_id = ?",
            (promo_code, user_id),
        )
        connector.commit()
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
'''
