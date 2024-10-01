from datetime import datetime
from typing import Any, Dict, List, Optional

from app.core.config import custom_logger
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def add_user(
    username: str,
    user_id: int,
    chat_id: int,
    referral_code: Optional[str] = None,
):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO users (username, user_id, chat_id, referral_code, first_meet) "
            "VALUES (?, ?, ?, ?, ?)",
            (username, user_id, chat_id, referral_code, current_date),
        )
        cursor.execute(
            "INSERT INTO gifts (user_id, already_take) VALUES (?, FALSE)",
            (chat_id,),
        )
        conn.commit()


# @custom_logger.log_db_operation
# def get_all_users() -> List[Dict[str, Any]]:
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             """
#             SELECT user_id, chat_id, username
#             FROM users
#             """
#         )
#         return cursor.fetchall()

# @custom_logger.log_db_operation
# def get_all_users() -> List[Dict[str, Any]]:
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             """
#             SELECT user_id, chat_id, username
#             FROM users
#             WHERE user_id <> 740905109 AND user_id <> 1358227914;
#             """
#         )
#         return [dict(row) for row in cursor.fetchall()]


@custom_logger.log_db_operation
def get_all_users() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT user_id, chat_id, username
            FROM users
            """
        )
        return [dict(row) for row in cursor.fetchall()]


# @custom_logger.log_db_operation
# def get_all_users_list() -> List[Dict[str, Any]]:
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             """
#             SELECT DISTINCT user_id, chat_id, username
#             FROM users
#             """
#         )
#         return [dict(row) for row in cursor.fetchall()]


@custom_logger.log_db_operation
def get_all_users_list() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT user_id, chat_id, COALESCE(username, '') as username
            FROM users
            """
        )
        return [dict(row) for row in cursor.fetchall()]


@custom_logger.log_db_operation
def get_user(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


@custom_logger.log_db_operation
def set_birth_date(chat_id: int, birth_date: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET first_name = ? WHERE chat_id = ?",
            (birth_date, chat_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def is_user_exists(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        )
        return result.fetchone() is not None


@custom_logger.log_db_operation
def is_already_know_birth(user_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT first_name FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return result is not None and result["first_name"] is not None


@custom_logger.log_db_operation
def get_arcan(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT arcan FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return result["arcan"] if result else None


@custom_logger.log_db_operation
def set_arcan(user_id: int, arcan: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "UPDATE users SET arcan = ? WHERE user_id = ?", (arcan, user_id)
        )
        conn.commit()


@custom_logger.log_db_operation
def db_no_friend(id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET no_friend = ? WHERE user_id = ?", ("TRUE", id)
        )
        conn.commit()


@custom_logger.log_db_operation
def set_advert(id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET after_advert = ? WHERE user_id = ?", ("Yes", id)
        )
        conn.commit()


@custom_logger.log_db_operation
def get_first_sphere(user_id: int) -> Optional[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "SELECT first_sphere FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return result["first_sphere"] if result else None


@custom_logger.log_db_operation
def set_first_sphere(user_id: int, sphere: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET first_sphere = ? WHERE user_id = ?",
            (sphere, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def add_points(user_id: int, points: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET points = points + ? WHERE id = ?",
            (points, user_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def what_choose_in_march(id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        return cursor.execute(
            "SELECT march_sphere_chosen FROM users WHERE chat_id = ?", (id,)
        ).fetchone()


@custom_logger.log_db_operation
def set_already_receive_one(chat_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET alredy_recive_one = ? WHERE chat_id = ?",
            (
                "True",
                chat_id,
            ),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_already_receive_all_march(chat_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET march_send_all = ? WHERE chat_id = ?",
            (
                "True",
                chat_id,
            ),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_discount_end(chat_id: int, discount_end: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET discount_end = ? WHERE chat_id = ?",
            (
                discount_end,
                chat_id,
            ),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_user_received_all_files(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET already_have_all_files = ? WHERE user_id = ?",
            (
                "True",
                user_id,
            ),
        )
        conn.commit()


@custom_logger.log_db_operation
def check_if_user_received_one_file(user_id: int) -> Optional[str]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT alredy_recive_one FROM users WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result["alredy_recive_one"] if result else None


@custom_logger.log_db_operation
def get_nik(id: int) -> Optional[str]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE user_id = ?", (id,))
        result = cursor.fetchone()
        return result["username"] if result else None


@custom_logger.log_db_operation
def check_if_user_received_all_files(user_id: int) -> Optional[str]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT already_have_all_files FROM users WHERE user_id = ?",
            (user_id,),
        )
        result = cursor.fetchone()
        return result["already_have_all_files"] if result else None


@custom_logger.log_db_operation
def get_gift_date() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT  
                CASE WHEN username IS NOT NULL THEN username ELSE gifts.user_id END AS username, 
                gifts.user_id, 
                gifts.gift_date
            FROM gifts, users
            WHERE users.user_id = gifts.user_id AND user_id <> 740905109 AND user_id <> 1358227914;
            """
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def get_active_users() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT  
                CASE WHEN username IS NOT NULL THEN username ELSE user_id END AS username, 
                user_id
            FROM users
            WHERE march_send <> 0 AND user_id <> 740905109 AND user_id <> 1358227914;
            """
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def get_not_active_users() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT  
                CASE WHEN username IS NOT NULL THEN username ELSE user_id END AS username, 
                user_id
            FROM users
            WHERE march_send = 0 AND user_id <> 740905109 AND user_id <> 1358227914;
            """
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def get_button_users() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT  
                CASE WHEN username IS NOT NULL THEN username ELSE user_id END AS username, 
                user_id
            FROM users
            WHERE no_friend <> 0 AND user_id <> 740905109 AND user_id <> 1358227914;
            """
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def get_reference_users() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT  
                CASE WHEN username IS NOT NULL THEN username ELSE user_id END AS username, 
                user_id
            FROM users
            WHERE march_send_all <> 0 AND user_id <> 740905109 AND user_id <> 1358227914;
            """
        )
        return cursor.fetchall()


@custom_logger.log_db_operation
def get_number_all_users_march() -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(user_id)
            FROM users
            WHERE march_send <> 0 AND user_id <> 740905109 AND user_id <> 1358227914;
            """
        )
        return cursor.fetchone()[0]


@custom_logger.log_db_operation
def get_number_all_users_past() -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(user_id)
            FROM users
            WHERE file_sent <> 0 AND user_id <> 740905109 AND user_id <> 1358227914;
            """
        )
        return cursor.fetchone()[0]


@custom_logger.log_db_operation
def get_comp_send_false_and_no_one_per() -> List[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT chat_id
            FROM users
            WHERE (feedback_choice != '1_per_month' OR feedback_choice IS NULL) AND comp_send = FALSE;
            """
        )
        return [row["chat_id"] for row in cursor.fetchall()]


@custom_logger.log_db_operation
def set_comp_send_true(chat_id: int, set_value: bool):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET comp_send = ? WHERE chat_id = ?",
            (set_value, chat_id),
        )
        conn.commit()


@custom_logger.log_db_operation
def set_time(time: str, chat_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET time = ? WHERE chat_id = ?", (time, chat_id)
        )
        conn.commit()


@custom_logger.log_db_operation
def add_info(chat_id: int, info: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET next_month = ? WHERE chat_id = ?",
            (info, chat_id),
        )
        conn.commit()
