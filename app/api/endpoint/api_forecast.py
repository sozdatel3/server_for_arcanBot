from typing import Optional

from fastapi import APIRouter, Body, HTTPException

from app.crud import db_forecast as forecasts_crud
from app.schemas.sh_forecast import ForecastCreate

router = APIRouter()

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# class SubscriptionUpdate(BaseModel):
#     status: bool


class LikeUpdate(BaseModel):
    like: bool


@router.post("/users/", response_model=dict)
async def add_user_to_forecast(forecast: ForecastCreate):
    forecasts_crud.add_user_to_forecast(forecast.user_id, forecast.arcan)
    return {"message": "User added to forecast successfully"}


@router.post("/add_month_column", response_model=dict)
async def add_month_column():
    forecasts_crud.add_month_column()
    return {"message": "Month column added successfully"}


@router.put("/users/{user_id}/mark_sent", response_model=dict)
async def mark_forecast_sent(user_id: int):
    forecasts_crud.mark_forecast_sent(user_id)
    return {"message": "Forecast marked as sent successfully"}


@router.put("/users/{user_id}/set_first_useful", response_model=dict)
async def set_first_useful_and_date(user_id: int):
    forecasts_crud.set_first_useful_and_date(user_id)
    return {"message": "First useful set successfully"}


@router.put("/users/{user_id}/mark_like", response_model=dict)
async def mark_forecast_like(user_id: int, like_update: LikeUpdate):
    forecasts_crud.mark_forecast_like(user_id, like_update.like)
    return {"message": "Forecast like marked successfully"}


@router.put("/users/{user_id}/subscription", response_model=dict)
async def update_subscription_status(
    user_id: int,
    status: bool = Body(..., embed=True),
    # user_id: int, subscription_update: SubscriptionUpdate
):
    forecasts_crud.update_subscription_status(user_id, status)
    return {"message": "Subscription status updated successfully"}


# @router.get("/users/{user_id}/subscription", response_model=dict)
# async def get_subscription_status(user_id: int):
#     status = forecasts_crud.get_subscription_status(user_id)
#     if status is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"subscription_status": status}


class SubscriptionStatus(BaseModel):
    subscription_status: Optional[bool]


@router.get("/users/{user_id}/subscription", response_model=SubscriptionStatus)
async def get_subscription_status(user_id: int):
    status = forecasts_crud.get_subscription_status(user_id)
    if status is None:
        raise HTTPException(status_code=404, detail="User not found")
    return SubscriptionStatus(subscription_status=status)


@router.get("/users/{user_id}/useful_sent", response_model=dict)
async def get_useful_sent(user_id: int):
    useful_sent = forecasts_crud.get_useful_sent(user_id)
    if useful_sent is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"useful_sent": useful_sent}


"""
@router.post("/users/", response_model=dict)
def add_user_to_forecast(forecast: ForecastCreate):
    forecasts_crud.add_user_to_forecast(forecast.user_id, forecast.arcan)
    return {"message": "User added to forecast successfully"}


@router.post("/add_month_column", response_model=dict)
def add_month_column():
    forecasts_crud.add_month_column()
    return {"message": "Month column added successfully"}


@router.put("/users/{user_id}/mark_sent", response_model=dict)
def mark_forecast_sent(user_id: int):
    forecasts_crud.mark_forecast_sent(user_id)
    return {"message": "Forecast marked as sent successfully"}


@router.put("/users/{user_id}/set_first_useful", response_model=dict)
def set_first_useful_and_date(user_id: int):
    forecasts_crud.set_first_useful_and_date(user_id)
    return {"message": "First useful set successfully"}


@router.put("/users/{user_id}/mark_like", response_model=dict)
def mark_forecast_like(user_id: int, like: bool):
    forecasts_crud.mark_forecast_like(user_id, like)
    return {"message": "Forecast like marked successfully"}


@router.put("/users/{user_id}/subscription", response_model=dict)
def update_subscription_status(user_id: int, status: bool):
    forecasts_crud.update_subscription_status(user_id, status)
    return {"message": "Subscription status updated successfully"}


@router.get("/users/{user_id}/subscription", response_model=Optional[bool])
def get_subscription_status(user_id: int):
    status = forecasts_crud.get_subscription_status(user_id)
    if status is None:
        raise HTTPException(status_code=404, detail="User not found")
    return status


@router.get("/users/{user_id}/useful_sent", response_model=Optional[int])
def get_useful_sent(user_id: int):
    useful_sent = forecasts_crud.get_useful_sent(user_id)
    if useful_sent is None:
        raise HTTPException(status_code=404, detail="User not found")
    return useful_sent
"""
