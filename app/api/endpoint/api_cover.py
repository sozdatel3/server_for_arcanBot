from typing import Dict, Optional

from fastapi import APIRouter, HTTPException

from app.crud import db_cover as covers_crud

router = APIRouter()


@router.post("/init_db")
def init_db():
    covers_crud.init_db()
    return {"message": "Database initialized successfully"}


@router.post("/arcan_descriptions")
def add_arcan_description(arcan: int, description: str):
    covers_crud.add_arcan_description(arcan, description)
    return {"message": "Arcan description added successfully"}


@router.get("/arcan_descriptions/{arcan}", response_model=Optional[str])
def get_arcan_description(arcan: int):
    description = covers_crud.get_arcan_description(arcan)
    if description is None:
        raise HTTPException(
            status_code=404, detail="Arcan description not found"
        )
    return description


@router.post("/cover_users")
def init_cover_user(user_id: int, arcan: int):
    covers_crud.init_cover_user(user_id, arcan)
    return {"message": "Cover user initialized successfully"}


@router.put("/cover_users/{user_id}/like")
def set_like_cover(user_id: int, like: bool):
    covers_crud.set_like_cover(user_id, like)
    return {"message": "Cover like status updated successfully"}


@router.put("/cover_users/{user_id}/payment")
def update_user_payment(user_id: int):
    covers_crud.update_user_payment(user_id)
    return {"message": "User payment updated successfully"}


@router.put("/cover_users/{user_id}/decrement_attempts")
def decrement_user_attempts(user_id: int):
    covers_crud.decrement_user_attempts(user_id)
    return {"message": "User attempts decremented successfully"}


@router.put("/cover_users/{user_id}/increment_attempts")
def increment_user_attempts(user_id: int):
    covers_crud.increment_user_attempts(user_id)
    return {"message": "User attempts incremented successfully"}


@router.get("/cover_users/{user_id}/attempts", response_model=int)
def get_user_attempts(user_id: int):
    return covers_crud.get_user_attempts(user_id)


@router.post("/transactions")
def record_transaction(user_id: int, amount: float):
    covers_crud.record_transaction(user_id, amount)
    return {"message": "Transaction recorded successfully"}


@router.get("/arcan_descriptions", response_model=Dict[int, Dict])
def get_all_arcan_descriptions(month: str):
    return covers_crud.get_all_arcan_descriptions(month)
