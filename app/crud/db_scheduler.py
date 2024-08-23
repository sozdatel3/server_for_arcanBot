from datetime import datetime

from app.core.config import custom_logger
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def get_forecast_users(current_month):
    column_name = f"{current_month}_send"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT user_id, arcan
            FROM monthly_forecasts
            WHERE {column_name} = FALSE AND subscription = TRUE
            """
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def update_forecast_status(user_id, column_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE monthly_forecasts
            SET {column_name} = TRUE
            WHERE user_id = ?
            """,
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def reset_forecast_reminder():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET forecast_reminder = FALSE
            """
        )
        conn.commit()


@custom_logger.log_db_operation
def get_gift_users():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT user_id
            FROM gifts
            WHERE already_take = FALSE
            """
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def update_gift_status(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE gifts
            SET already_take = TRUE, gift_date = ?
            WHERE user_id = ?
            """,
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_expired_bonuses():
    current_date = datetime.now()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, user_id, bonus, add_date, expire_date
            FROM expiration_bonus_movement
            WHERE expire_date <= ? AND flag_is_burned = FALSE
            """,
            (current_date,),
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def get_spent_bonus(user_id, add_date, expire_date):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT SUM(bonus)
            FROM transactions
            WHERE user_id = ? AND date BETWEEN ? AND ? AND bonus < 0
            """,
            (user_id, add_date, expire_date),
        )
        return abs(cursor.fetchone()[0] or 0)


@custom_logger.log_db_operation
def update_bonus_burned_status(bonus_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE expiration_bonus_movement
            SET flag_is_burned = TRUE
            WHERE id = ?
            """,
            (bonus_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_users_for_useful_message():
    current_time = datetime.now()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT user_id
            FROM monthly_forecasts
            WHERE time_to_send_useful <= ? AND useful_sent = 1
            """,
            (current_time,),
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def update_useful_sent_status(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE monthly_forecasts
            SET useful_sent = 2
            WHERE user_id = ?
            """,
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_users_not_in_forecasts():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        return cursor.execute(
            """
        SELECT user_id
        FROM users
        WHERE user_id NOT IN (SELECT user_id FROM monthly_forecasts)
        AND forecast_reminder = FALSE
        """
        ).fetchall()
