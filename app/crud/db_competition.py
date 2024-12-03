# CREATE TABLE IF NOT EXISTS new_year_competition (
#                 user_id INTEGER PRIMARY KEY,
#                 inst_username TEXT default NULL,
#                 subscribe BOOLEAN DEFAULT FALSE,
#                 count_of_friends INTEGER DEFAULT 0,
#                 should_send_message BOOLEAN DEFAULT FALSE,
#                 refer_id INTEGER DEFAULT NULL,
#                 FOREIGN KEY (user_id) REFERENCES users(user_id),
#                 FOREIGN KEY (refer_id) REFERENCES users(user_id)
#             )


# from venv import logger
import hashlib
from datetime import datetime
from typing import Optional

from app.core.config import custom_logger, settings
from app.core.database import get_db_connection


def add_user_to_competition(user_id: int):
    # secret_link = generate_referral_link(user_id)
    message = f"{settings.SECRET_WORD}{user_id}{datetime.now().timestamp()}"
    secret_link = hashlib.sha256(message.encode()).hexdigest()[:12]

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO new_year_competition (user_id, secret_link) VALUES (?, ?)",
            (user_id, secret_link),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_secret_link(user_id: int) -> str:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT secret_link FROM new_year_competition WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


@custom_logger.log_db_operation
def get_user_by_referral_code(secret_link: str) -> Optional[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM new_year_competition WHERE secret_link = ?",
            (secret_link,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


@custom_logger.log_db_operation
def is_user_in_competition(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM new_year_competition WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        return result is not None


@custom_logger.log_db_operation
def is_user_subscribed(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT subscribe FROM new_year_competition WHERE user_id = ?",
            (user_id,),
        )
        return cursor.fetchone()[0]


@custom_logger.log_db_operation
def set_inst_username(user_id: int, inst_username: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE new_year_competition SET inst_username = ? WHERE user_id = ?",
            (inst_username, user_id),
        )
        conn.commit()
        cursor.execute(
            "UPDATE users SET inst_username = ? WHERE user_id = ?",
            (inst_username, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_refer_id(user_id: int, refer_id: int):
    if not is_user_have_refer_id(user_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE new_year_competition SET refer_id = ? WHERE user_id = ?",
                (refer_id, user_id),
            )
            conn.commit()


@custom_logger.log_db_operation
def is_user_have_refer_id(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT refer_id FROM new_year_competition WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        return result is not None


@custom_logger.log_db_operation
def set_subscribe(user_id: int, subscribe: bool):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE new_year_competition SET subscribe = ? WHERE user_id = ?",
            (subscribe, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_status(user_id: int, status: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE new_year_competition SET status = ? WHERE user_id = ?",
            (status, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_status(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status FROM new_year_competition WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return False


@custom_logger.log_db_operation
def increment_count_of_friends(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE new_year_competition SET count_of_friends = count_of_friends + 1 WHERE user_id = ?",
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_count_of_friends(user_id: int) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT count_of_friends FROM new_year_competition WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0


@custom_logger.log_db_operation
def get_user_by_secret_link(secret_link: str) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM new_year_competition WHERE secret_link = ?",
            (secret_link,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0


@custom_logger.log_db_operation
def get_all_users_status(status: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT user_id, inst_username, count_of_friends, should_send_message FROM new_year_competition WHERE status = ?",
            (status,),
        ).fetchall()
        if result:
            return [
                {
                    "user_id": row[0],
                    "inst_username": row[1],
                    "count_of_friends": row[2],
                    "should_send_message": row[3],
                }
                for row in result
            ]
        return []
