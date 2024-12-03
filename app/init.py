from app.core.database import get_db_connection
from app.crud.db_forecast import add_month_column


def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS city (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                have_free_try INTEGER DEFAULT 2,
                have_pay BOOL DEFAULT FALSE,
                last_transaction_date TIMESTAMP,
                cities_checked TEXT DEFAULT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS stat (
                id INTEGER PRIMARY KEY,
                counter INTEGER DEFAULT 0
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS every_day_stat (
                id INTEGER PRIMARY KEY,
                date TEXT,
                actions_count INTEGER DEFAULT 0,
                unique_users INTEGER DEFAULT 0
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS important_mes_id (
                id INTEGER PRIMARY KEY,
                message_id INTEGER DEFAULT 0,
                mes_name TEXT default NULL
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS new_year_competition (
                user_id INTEGER PRIMARY KEY,
                inst_username TEXT default NULL,
                subscribe BOOLEAN DEFAULT FALSE,
                count_of_friends INTEGER DEFAULT 0,
                should_send_message BOOLEAN DEFAULT FALSE,
                refer_id INTEGER DEFAULT NULL,
                secret_link TEXT DEFAULT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (refer_id) REFERENCES users(user_id)
            )
        """
        )

        # Создание таблицы задач
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS task_city_transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )
        # Создание таблицы задач
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS task_product_transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )
        # status BOOL DEFAULT FALSE,

        # Создание таблицы транзакций
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS city_transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount INTEGER,
                create_date TIMESTAMP,
                pay_date TIMESTAMP,
                status BOOL DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )
        # cursor.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS product_transactions (
        #         id INTEGER PRIMARY KEY,
        #         user_id INTEGER,
        #         amount INTEGER,
        #         create_date TIMESTAMP,
        #         pay_date TIMESTAMP,
        #         status BOOL DEFAULT FALSE,
        #         FOREIGN KEY (user_id) REFERENCES users(user_id)
        #     )
        # """
        # )

        # Создание таблицы пользователей с полем chat_id
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                user_id INTEGER,
                chat_id INTEGER,
                arcan INTEGER DEFAULT NULL,
                referral_code TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY,
                referrer_id INTEGER,
                referred_id INTEGER,
                FOREIGN KEY (referrer_id) REFERENCES users (id),
                FOREIGN KEY (referred_id) REFERENCES users (id)
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gifts (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                already_take BOLEAN DEFAULT FALSE,
                gift_date TEXT DEFAULT NULL
            )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS monthly_forecasts (
            user_id INTEGER PRIMARY KEY,
            arcan INTEGER,
            subscription BOOLEAN DEFAULT TRUE,
            time_to_send_useful TIMESTAMP DEFAULT NULL,
            useful_sent INTEGER DEFAULT 0
        )
        """
        )

        # Создание таблицы лояльности
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS loyalty (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                balance INTEGER DEFAULT 0,
                total_spent INTEGER DEFAULT 0,
                count_of_transaction INTEGER DEFAULT 0,
                last_transaction_date TIMESTAMP,
                promo_code TEXT UNIQUE,
                referrer_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (referrer_id) REFERENCES users(user_id)
            )
        """
        )
        # points INTEGER,

        # Создание таблицы транзакций
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount INTEGER,
                service TEXT,
                bonus INTEGER DEFAULT 0,
                comment TEXT,
                date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pre_transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount INTEGER,
                service TEXT,
                bonus INTEGER DEFAULT 0,
                comment TEXT,
                date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )
        # Создание таблицы временных бонусов
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expiration_bonus_movement (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            bonus INTEGER,
            add_date TIMESTAMP,
            expire_date TIMESTAMP,
            flag_is_burned BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """
        )

        # Создание таблицы для описаний арканов по месяцам
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS arcan_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arcan INTEGER NOT NULL,
                month TEXT NOT NULL,
                description TEXT NOT NULL,
                UNIQUE(arcan, month)
            )
            """
        )

        # Создание таблицы для отслеживания использования функции заставок
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cover_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                arcan INTEGER NOT NULL,
                like_last BOOLEAN DEFAULT NULL,
                has_paid BOOLEAN DEFAULT FALSE,
                attempts_left INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id)
            )
            """
        )

        # Создание таблицы для рассылок
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
            """
        )

        # Создание таблицы для транзакций
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cover_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
                """
        )

        # Создание таблицы для описаний арканов по месяцам
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS arcan_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            arcan INTEGER NOT NULL,
            month TEXT NOT NULL,
            description TEXT NOT NULL,
            UNIQUE(arcan, month)
        )
        """
        )

        # Создание таблицы для отслеживания использования функции заставок
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS cover_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            arcan INTEGER NOT NULL,
            like_last BOOLEAN DEFAULT NULL,
            has_paid BOOLEAN DEFAULT FALSE,
            attempts_left INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            UNIQUE(user_id)
        )
        """
        )

        # Создание таблицы для транзакций
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS cover_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
        )

        conn.commit()

        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN already_have_all_files TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN birth_date TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN like TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN first_name TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN discount_end TEXT DEFAULT NULL"
            )
        except:
            pass

        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN first_meet TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN first_sphere INTEGER DEFAULT 0"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN file_sent BOOLEAN DEFAULT FALSE;"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN feedback_choice TEXT DEFAULT NULL;"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN alredy_recive_one TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN inst_username TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN march_send BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN march_sphere_chosen TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN march_send_all BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN no_friend BOOLEAN DEFAULT FALSE"
            )
            conn.commit()
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN comp_send BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN time TEXT DEFAULT NULL"
            )
        except:
            pass
        # Создание таблицы для отслеживания переходов по реферальным ссылкам
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN april_sphere_chosen TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN april_send_to BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN after_advert TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN may_send BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN del BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN client_story TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN june_send BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN jule_send BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN do_u_know_inst TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN phone_number TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN forecast_reminder BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE city ADD COLUMN recive_request BOOLEAN DEFAULT FALSE"
            )
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE city ADD COLUMN choose_answer TEXT DEFAULT NULL"
            )
        except:
            pass
        try:
            cursor.execute(
                "UPDATE city SET have_pay = TRUE WHERE user_id = 798481953"
            )
            conn.commit()
        except:
            pass
        try:
            cursor.execute(
                "ALTER TABLE new_year_competition ADD COLUMN status TEXT DEFAULT NULL"
            )
            conn.commit()
        except:
            pass
        add_month_column()
        conn.commit()


# init()
