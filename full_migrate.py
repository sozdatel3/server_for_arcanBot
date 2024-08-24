import os
import sqlite3


def get_table_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [column[1] for column in cursor.fetchall()]


def migrate_table(old_cursor, new_cursor, table_name):
    old_columns = get_table_columns(old_cursor, table_name)
    new_columns = get_table_columns(new_cursor, table_name)
    common_columns = list(set(old_columns) & set(new_columns))

    old_cursor.execute(f"SELECT {', '.join(common_columns)} FROM {table_name}")
    rows = old_cursor.fetchall()

    if rows:
        placeholders = ", ".join(["?" for _ in common_columns])
        insert_query = f"""
            INSERT OR IGNORE INTO {table_name} ({', '.join(common_columns)})
            VALUES ({placeholders})
        """
        new_cursor.executemany(insert_query, rows)
        print(f"Migrated {len(rows)} rows from {table_name}")
    else:
        print(f"No data to migrate from {table_name}")


def migrate_data(old_db_path, new_db_path):
    # Проверка существования баз данных
    if not os.path.exists(old_db_path):
        raise FileNotFoundError(f"Old database not found: {old_db_path}")
    if not os.path.exists(new_db_path):
        raise FileNotFoundError(f"New database not found: {new_db_path}")

    # Подключение к старой и новой базам данных
    old_conn = sqlite3.connect(old_db_path)
    new_conn = sqlite3.connect(new_db_path)
    old_cursor = old_conn.cursor()
    new_cursor = new_conn.cursor()

    try:
        # Миграция таблиц
        tables_to_migrate = ["users", "referrals", "gifts"]
        for table in tables_to_migrate:
            migrate_table(old_cursor, new_cursor, table)

        # Миграция таблицы monthly_forecasts
        new_cursor.execute(
            """
            INSERT OR IGNORE INTO monthly_forecasts (user_id, arcan)
            SELECT user_id, arcan FROM users WHERE arcan IS NOT NULL
        """
        )
        print("Migrated data to monthly_forecasts")

        new_conn.commit()
        print("Data migration completed successfully.")

    except Exception as e:
        print(f"An error occurred during migration: {e}")
        new_conn.rollback()

    finally:
        old_conn.close()
        new_conn.close()


def migrate_loyalty_data(old_cursor, new_cursor):
    # Получаем все уникальные user_id из таблицы users
    old_cursor.execute(
        "SELECT DISTINCT user_id FROM users WHERE user_id IS NOT NULL"
    )
    user_ids = old_cursor.fetchall()

    # Вставляем данные в таблицу loyalty
    new_cursor.executemany(
        "INSERT OR IGNORE INTO loyalty (user_id) VALUES (?)", user_ids
    )

    print(f"Migrated {len(user_ids)} unique users to loyalty table")


def add_month_column(conn):

    cursor = conn.cursor()
    # month_name = datetime.now().strftime("%B").lower()
    column_send = "september_send"
    column_like = "september_like"
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


# def migrate_city_transaction(old_cursor, new_cursor):
#     # Получаем все данные из таблицы city_transaction
#     old_cursor.execute("SELECT * FROM city_transactions")
#     transactions = old_cursor.fetchall()

#     # Получаем имена столбцов
#     old_cursor.execute("PRAGMA table_info(city_transaction)")
#     columns = [column[1] for column in old_cursor.fetchall()]

#     # Подготавливаем SQL запрос для вставки
#     placeholders = ", ".join(["?" for _ in columns])
#     insert_query = f"""
#         INSERT OR IGNORE INTO city_transaction ({', '.join(columns)})
#         VALUES ({placeholders})
#     """

#     # Вставляем данные в новую таблицу city_transaction
#     new_cursor.executemany(insert_query, transactions)

#     print(f"Migrated {len(transactions)} rows to city_transactions table")


def migrate_city_transaction(old_cursor, new_cursor):
    # Получаем все данные из таблицы city_transactions
    old_cursor.execute("SELECT * FROM city_transactions")
    transactions = old_cursor.fetchall()

    if not transactions:
        print("No data found in city_transactions table")
        return

    # Получаем имена столбцов
    old_cursor.execute("PRAGMA table_info(city_transactions)")
    columns = [column[1] for column in old_cursor.fetchall()]

    if not columns:
        print("No columns found in city_transactions table")
        return

    # Подготавливаем SQL запрос для вставки
    placeholders = ", ".join(["?" for _ in columns])
    insert_query = f"""
        INSERT OR IGNORE INTO city_transactions ({', '.join(columns)})
        VALUES ({placeholders})
    """

    try:
        # Вставляем данные в новую таблицу city_transactions
        new_cursor.executemany(insert_query, transactions)
        print(f"Migrated {len(transactions)} rows to city_transactions table")
    except sqlite3.Error as e:
        print(f"Error inserting into city_transactions: {e}")
        print(f"Insert query: {insert_query}")
        print(
            f"First row of data: {transactions[0] if transactions else 'No data'}"
        )


def migrate_nastuxa(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET arcan = 14 WHERE user_id = 817011039")
    cursor.execute(
        "UPDATE monthly_forecasts SET arcan = 14 WHERE user_id = 817011039"
    )
    conn.commit()


if __name__ == "__main__":
    # old_db_path = "mydatabase.db"
    old_db_path = "new_database-11.db"
    new_db_path = "new_database.db"

    # try:
    #     migrate_data(old_db_path, new_db_path)
    # except Exception as e:
    #     print(f"Migration failed: {e}")
    old_conn = sqlite3.connect(old_db_path)
    new_conn = sqlite3.connect(new_db_path)
    migrate_nastuxa(new_conn)
    # migrate_loyalty_data(old_conn.cursor(), new_conn.cursor())
    # migrate_city_transaction(old_conn.cursor(), new_conn.cursor())
    # new_conn.commit()
    # add_month_column(new_conn)
