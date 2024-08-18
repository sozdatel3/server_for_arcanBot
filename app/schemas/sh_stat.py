from typing import List, Tuple

from pydantic import BaseModel


class ServiceStatistics(BaseModel):
    service: str
    amount: int
    count: int


class StatisticsResponse(BaseModel):
    new_users: int
    total_users: int
    external_purchases: int
    external_amount: float
    credited_points: int
    debited_points: int
    bot_purchases: int
    bot_amount: float
    checked_cities: int
    total_purchases: int
    total_amount: float
    services: List[Tuple[str, int, int]]


class FormattedStatisticsResponse(BaseModel):
    formatted_statistics: str
