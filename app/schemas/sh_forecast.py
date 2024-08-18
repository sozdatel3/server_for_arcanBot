from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ForecastCreate(BaseModel):
    user_id: int
    arcan: Optional[int] = None


class ForecastUpdate(BaseModel):
    arcan: Optional[int] = None
    subscription: Optional[bool] = None
    time_to_send_useful: Optional[datetime] = None
    useful_sent: Optional[int] = None


class Forecast(BaseModel):
    user_id: int
    arcan: Optional[int]
    subscription: bool
    time_to_send_useful: Optional[datetime]
    useful_sent: int
