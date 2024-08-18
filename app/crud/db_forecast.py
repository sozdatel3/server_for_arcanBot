from datetime import datetime, timedelta
from typing import Optional

from app.core.config import custom_logger, settings
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def add_user_to_forecast(user_id: int, arcan: Optional[int] = None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM monthly_forecasts WHERE user_id = ?", (user_id,)
        )
        existing_user = cursor.fetchone()

        if existing_user:
            if arcan is not None:
                cursor.execute(
                    "UPDATE monthly_forecasts SET arcan = ? WHERE user_id = ?",
                    (arcan, user_id),
                )
        else:
            cursor.execute(
                "INSERT INTO monthly_forecasts (user_id, arcan, subscription) VALUES (?, ?, TRUE)",
                (user_id, arcan),
            )

        cursor.execute("PRAGMA table_info(monthly_forecasts)")
        send_columns = [
            col[1] for col in cursor.fetchall() if col[1].endswith("_send")
        ]

        # set_clauses = [
        #     f"{col} = CASE WHEN {col} = TRUE THEN TRUE ELSE FALSE END"
        #     for col in send_columns
        # ]
        if send_columns:
            set_clauses = [
                f"{col} = CASE WHEN {col} = 1 THEN 1 ELSE 0 END"
                for col in send_columns
            ]
            sql_query = f"UPDATE monthly_forecasts SET {', '.join(set_clauses)} WHERE user_id = ?"
            cursor.execute(sql_query, (user_id,))
        sql_query = f"UPDATE monthly_forecasts SET {', '.join(set_clauses)}"
        cursor.execute(sql_query)

        conn.commit()


@custom_logger.log_db_operation
def add_month_column():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        month_name = datetime.now().strftime("%B").lower()
        column_send = f"{month_name}_send"
        column_like = f"{month_name}_like"
        try:
            cursor.execute(
                f"ALTER TABLE monthly_forecasts ADD COLUMN {column_send} BOOLEAN DEFAULT FALSE"
            )
            cursor.execute(
                f"ALTER TABLE monthly_forecasts ADD COLUMN {column_like} BOOLEAN DEFAULT NULL"
            )
            conn.commit()
        except:
            pass


@custom_logger.log_db_operation
def mark_forecast_sent(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        current_month = datetime.now().strftime("%B").lower()
        column_name = f"{current_month}_send"
        cursor.execute(
            f"UPDATE monthly_forecasts SET {column_name} = TRUE WHERE user_id = ?",
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_first_useful_and_date(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        time_to_send_new = datetime.now() + timedelta(days=7)
        if settings.DEBUG:
            time_to_send_new = datetime.now()
        cursor.execute(
            "UPDATE monthly_forecasts SET useful_sent = 1, time_to_send_useful = ? WHERE user_id = ?",
            (time_to_send_new, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def mark_forecast_like(user_id: int, like: bool):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        current_month = datetime.now().strftime("%B").lower()
        column_name = f"{current_month}_like"
        cursor.execute(
            f"UPDATE monthly_forecasts SET {column_name} = ? WHERE user_id = ?",
            (like, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def update_subscription_status(user_id: int, status: bool):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE monthly_forecasts SET subscription = ? WHERE user_id = ?",
            (status, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_subscription_status(user_id: int) -> Optional[bool]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT subscription FROM monthly_forecasts WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


@custom_logger.log_db_operation
def get_useful_sent(user_id: int) -> Optional[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT useful_sent FROM monthly_forecasts WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        return result[0] if result else None
