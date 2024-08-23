from datetime import datetime

from fastapi import APIRouter

from app.crud import db_scheduler

router = APIRouter()


@router.get("/forecast_users/{current_month}")
async def get_forecast_users(current_month: str):
    return db_scheduler.get_forecast_users(current_month)


@router.put("/update_forecast_status/{user_id}/{column_name}")
async def update_forecast_status(user_id: int, column_name: str):
    db_scheduler.update_forecast_status(user_id, column_name)
    return {"status": "success"}


@router.put("/reset_forecast_reminder")
async def reset_forecast_reminder():
    db_scheduler.reset_forecast_reminder()
    return {"status": "success"}


@router.get("/gift_users")
async def get_gift_users():
    return db_scheduler.get_gift_users()


@router.put("/update_gift_status/{user_id}")
async def update_gift_status(user_id: int):
    db_scheduler.update_gift_status(user_id)
    return {"status": "success"}


@router.get("/expired_bonuses")
async def get_expired_bonuses():
    return db_scheduler.get_expired_bonuses()


@router.get("/spent_bonus/{user_id}")
async def get_spent_bonus(user_id: int, add_date: str, expire_date: str):
    add_date = datetime.strptime(add_date, "%Y-%m-%d %H:%M:%S")
    expire_date = datetime.strptime(expire_date, "%Y-%m-%d %H:%M:%S")
    return db_scheduler.get_spent_bonus(user_id, add_date, expire_date)


@router.put("/update_bonus_burned_status/{bonus_id}")
async def update_bonus_burned_status(bonus_id: int):
    db_scheduler.update_bonus_burned_status(bonus_id)
    return {"status": "success"}


@router.get("/users_for_useful_message")
async def get_users_for_useful_message():
    return db_scheduler.get_users_for_useful_message()


@router.put("/update_useful_sent_status/{user_id}")
async def update_useful_sent_status(user_id: int):
    db_scheduler.update_useful_sent_status(user_id)
    return {"status": "success"}


@router.get("/not-in-forecast")
async def get_users_not_in_forecast():
    return db_scheduler.get_users_not_in_forecasts()
