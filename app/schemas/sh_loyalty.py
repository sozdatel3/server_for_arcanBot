from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LoyaltyCreate(BaseModel):
    user_id: int
    referrer_id: Optional[int] = None


class LoyaltyUpdate(BaseModel):
    balance: Optional[int] = None
    total_spent: Optional[int] = None
    count_of_transaction: Optional[int] = None


class Transaction(BaseModel):
    amount: int
    bonus: int
    service: str
    date: datetime


class LoyaltyStats(BaseModel):
    users_count: int
    total_balance: int
    total_spent: int
