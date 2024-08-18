from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArcanDescription(BaseModel):
    id: int
    arcan: int
    month: str
    description: str


class CoverUser(BaseModel):
    id: int
    user_id: int
    arcan: int
    like_last: Optional[bool]
    has_paid: bool
    attempts_left: int


class CoverTransaction(BaseModel):
    id: int
    user_id: int
    amount: float
    timestamp: datetime
