from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from app.core.config import custom_logger
from app.core.database import get_db_connection


@custom_logger.log_db_operation
def get_statistics(period: str) -> Dict:
    end_date = datetime.now()

    if period == "all_time":
        start_date = datetime.min
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    elif period == "week":
        start_date = end_date - timedelta(days=7)
    elif period == "today":
        start_date = end_date.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    else:
        raise ValueError("Invalid period")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Новые пользователи за выбранный период
        cursor.execute(
            """
            SELECT COUNT(*) FROM users
            WHERE first_meet >= ? AND first_meet <= ?
        """,
            (start_date, end_date),
        )
        new_users = cursor.fetchone()[0]

        # Всего уникальных пользователей
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # Количество и сумма покупок вне бота
        cursor.execute(
            """
            SELECT COUNT(*), SUM(amount)
            FROM transactions
            WHERE date >= ? AND date <= ?
        """,
            (start_date, end_date),
        )
        external_purchases, external_amount = cursor.fetchone()

        # Начисленные и списанные баллы
        cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN bonus > 0 THEN bonus ELSE 0 END) as credited,
                SUM(CASE WHEN bonus < 0 THEN ABS(bonus) ELSE 0 END) as debited
            FROM transactions
            WHERE date >= ? AND date <= ?
        """,
            (start_date, end_date),
        )
        credited_points, debited_points = cursor.fetchone()

        # Количество и сумма покупок в боте
        cursor.execute(
            """
            SELECT COUNT(*), SUM(amount)
            FROM city_transactions
            WHERE pay_date >= ? AND pay_date <= ?
        """,
            (start_date, end_date),
        )
        bot_purchases, bot_amount = cursor.fetchone()

        # Количество проверенных городов
        checked_cities = count_checked_cities(cursor)

        # Общее количество и сумма покупок
        total_purchases = (external_purchases or 0) + (bot_purchases or 0)
        total_amount = (external_amount or 0) + (bot_amount or 0)

        services = get_services_statistics(cursor, start_date, end_date)

    return {
        "new_users": new_users,
        "total_users": total_users,
        "external_purchases": external_purchases or 0,
        "external_amount": external_amount or 0,
        "credited_points": credited_points or 0,
        "debited_points": debited_points or 0,
        "bot_purchases": bot_purchases or 0,
        "bot_amount": bot_amount or 0,
        "checked_cities": checked_cities,
        "total_purchases": total_purchases,
        "total_amount": total_amount,
        "services": services,
    }


@custom_logger.log_db_operation
def get_services_statistics(
    cursor, start_date: datetime, end_date: datetime
) -> List[Tuple[str, int, int]]:
    # Получаем статистику по обычным услугам
    cursor.execute(
        """
        SELECT service, SUM(amount) as total_amount, COUNT(*) as count
        FROM transactions
        WHERE date >= ? AND date <= ?
        GROUP BY service
        ORDER BY total_amount DESC
    """,
        (start_date, end_date),
    )

    services = cursor.fetchall()

    # Получаем статистику по совместимости с городом и чаевым
    cursor.execute(
        """
        SELECT amount
        FROM city_transactions
        WHERE pay_date >= ? AND pay_date <= ?
    """,
        (start_date, end_date),
    )

    city_transactions = cursor.fetchall()

    compatibility_count = len(city_transactions)
    compatibility_amount = 270 * compatibility_count
    tips_amount = sum(
        max(0, transaction[0] - 270) for transaction in city_transactions
    )
    tips_count = sum(
        1 for transaction in city_transactions if transaction[0] > 270
    )

    # Добавляем статистику по совместимости и чаевым к общему списку услуг
    services.append(
        ("Совместимость с городом", compatibility_amount, compatibility_count)
    )
    if tips_amount > 0:
        services.append(("Чаевые", tips_amount, tips_count))

    # Сортируем список по убыванию суммы
    services.sort(key=lambda x: x[1], reverse=True)

    return services


@custom_logger.log_db_operation
def count_checked_cities(cursor) -> int:
    cursor.execute(
        """
        SELECT cities_checked
        FROM city
        WHERE cities_checked IS NOT NULL
    """
    )
    cities_lists = cursor.fetchall()

    total_cities = 0
    for cities_string in cities_lists:
        cities = cities_string[0].split(",")
        total_cities += len(cities)

    return total_cities


@custom_logger.log_db_operation
def format_statistics_response(stats: Dict) -> str:
    response = f"""
Статистика за выбранный период:

Новых пользователей: {stats['new_users']}
Всего уникальных пользователей: {stats['total_users']}

Покупки вне бота:
 - Количество: {stats['external_purchases']}
 - Сумма: {stats['external_amount']} руб.

Баллы:
 - Начислено: {stats['credited_points']}
 - Списано: {stats['debited_points']}

Покупки в боте:
 - Количество: {stats['bot_purchases']}
 - Сумма: {stats['bot_amount']} руб.

Проверено городов: {stats['checked_cities']}

Общая статистика:
 - Количество покупок: {stats['total_purchases']}
 - Сумма покупок: {stats['total_amount']} руб.

Статистика по услугам:
"""

    for i, (service, amount, count) in enumerate(stats["services"], 1):
        response += f"{i}. {service} - {amount} рублей, купили {count} раз\n"

    return response
