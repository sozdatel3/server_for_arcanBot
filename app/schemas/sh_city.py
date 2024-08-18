from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CityCreate(BaseModel):
    user_id: int
    have_free_try: int = 2
    have_pay: bool = False


class CityUpdate(BaseModel):
    have_free_try: Optional[int]
    have_pay: Optional[bool]
    cities_checked: Optional[str]


class CityTransaction(BaseModel):
    amount: int
    date: datetime


class City(BaseModel):
    id: int
    user_id: int
    have_free_try: int
    have_pay: bool
    last_transaction_date: Optional[datetime]
    cities_checked: Optional[str]
