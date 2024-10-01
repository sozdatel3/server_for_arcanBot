# from venv import logger
from app.core.config import custom_logger
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def create_broadcast(broadcast_name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"ALTER TABLE broadcasts ADD COLUMN {broadcast_name} BOOLEAN"
        )
        conn.commit()


@custom_logger.log_db_operation
def mark_broadcast_delivered(user_id: int, broadcast_name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO broadcasts (user_id, {broadcast_name})
            VALUES (?, TRUE)
            ON CONFLICT (user_id) DO UPDATE SET {broadcast_name} = TRUE
            """,
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def mark_broadcast_failed(user_id: int, broadcast_name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO broadcasts (user_id, {broadcast_name})
            VALUES (?, FALSE)
            ON CONFLICT (user_id) DO UPDATE SET {broadcast_name} = FALSE
            """,
            (user_id,),
        )
        conn.commit()


@custom_logger.log_db_operation
def get_all_broadcasts_statistics():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Получаем список всех колонок рассылок
        cursor.execute("PRAGMA table_info(broadcasts)")
        columns = [
            col[1]
            for col in cursor.fetchall()
            if col[1] not in ("id", "user_id", "created_at")
        ]

        # Формируем SQL-запрос динамически
        sql_query = f"""
        SELECT 
            DATE(created_at) as date,
            {', '.join([f"SUM(CASE WHEN {col} = TRUE THEN 1 ELSE 0 END) as {col}_delivered" for col in columns])},
            {', '.join([f"SUM(CASE WHEN {col} = FALSE THEN 1 ELSE 0 END) as {col}_failed" for col in columns])}
        FROM broadcasts
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
        """

        cursor.execute(sql_query)
        return cursor.fetchall(), columns


@custom_logger.log_db_operation
def get_broadcast_statistics(broadcast_name: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT 
                DATE(created_at) as date,
                SUM(CASE WHEN {broadcast_name} = TRUE THEN 1 ELSE 0 END) as delivered,
                SUM(CASE WHEN {broadcast_name} = FALSE THEN 1 ELSE 0 END) as failed
            FROM broadcasts
            WHERE {broadcast_name} IS NOT NULL
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
            """
        )
        return cursor.fetchall()
