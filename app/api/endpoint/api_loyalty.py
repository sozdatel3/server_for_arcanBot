from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Query

from app.crud import db_loyalty as loyalty_crud
from app.schemas.sh_loyalty import LoyaltyCreate, LoyaltyStats, Transaction

router = APIRouter()


@router.post("/users/", response_model=dict)
def add_user_to_loyalty(user: LoyaltyCreate):
    success = loyalty_crud.add_user_to_loyalty(user.user_id, user.referrer_id)
    if success:
        return {"message": "User added to loyalty system successfully"}
    else:
        raise HTTPException(
            status_code=401, detail="User already exists in loyalty system"
        )


@router.get("/users/{user_id}/balance", response_model=int)
def get_user_balance(user_id: int):
    return loyalty_crud.get_user_balance(user_id)


@router.put("/users/{user_id}/balance", response_model=dict)
def update_user_balance(
    user_id: int, points: int, no_transaction: bool = False
):
    loyalty_crud.update_user_balance(user_id, points, no_transaction)
    return {"message": "User balance updated successfully"}


@router.post("/transactions/", response_model=dict)
def record_transaction(
    user_id: int = Body(..., embed=True),
    amount: int = Body(..., embed=True),
    bonus: int = Body(..., embed=True),
    service: str = Body(embed=True, default=""),
    comment: str = Body(embed=True, default=""),
    expiration_days: Optional[int] = Body(embed=True, default=None),
):
    try:
        loyalty_crud.record_transaction(
            user_id, amount, bonus, service,comment, expiration_days
        )
        return {"message": "Transaction recorded successfully"}
    except Exception as e:
        print(f"Error recording transaction: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}/transactions", response_model=List[Transaction])
def get_user_transactions(user_id: int, limit: Optional[int] = Query(10)):
    return loyalty_crud.get_user_transactions(user_id, limit)


@router.get("/users/{user_id}/transaction_count", response_model=int)
def get_transaction_count(user_id: int):
    return loyalty_crud.get_count_of_transaction(user_id)


@router.get("/users/{user_id}/total_spent", response_model=int)
def get_total_spent(user_id: int):
    return loyalty_crud.get_total_spent(user_id)


@router.post("/{promo_code}/use", response_model=dict)
def use_promo_code(
    promo_code: str, new_user_id: Optional[int] = Body(None, embed=True)
):
    referrer_id = loyalty_crud.use_promo_code(promo_code, new_user_id)
    if referrer_id:
        return {
            "message": "Promo code used successfully",
            "referrer_id": referrer_id,
        }
    else:
        raise HTTPException(status_code=404, detail="Invalid promo code")


@router.put("/users/{user_id}/deduct_points", response_model=dict)
def deduct_points(user_id: int, points: int):
    success, new_balance = loyalty_crud.deduct_points(user_id, points)
    if success:
        return {
            "message": "Points deducted successfully",
            "new_balance": new_balance,
        }
    else:
        raise HTTPException(status_code=400, detail="Insufficient balance")


@router.get("/users/{user_id}/check_balance", response_model=dict)
def check_balance(user_id: int, points: int):
    sufficient, current_balance = loyalty_crud.check_balance(user_id, points)
    return {"sufficient": sufficient, "current_balance": current_balance}


@router.get("/users/{user_id}/referrer", response_model=Optional[int])
def get_referrer_id(user_id: int):
    return loyalty_crud.get_referrer_id(user_id)


@router.get("/users/{user_id}/promo_code", response_model=Optional[str])
def get_promo_code(user_id: int):
    return loyalty_crud.get_promo_code(user_id)


@router.post("/users/{user_id}/generate_promo_code", response_model=str)
def generate_promo_code(user_id: int):
    return loyalty_crud.generate_promo_code(user_id)


@router.get("/stats", response_model=LoyaltyStats)
def get_loyalty_stats():
    users_count, total_balance, total_spent = loyalty_crud.get_loyalty_stats()
    return LoyaltyStats(
        users_count=users_count,
        total_balance=total_balance,
        total_spent=total_spent,
    )


@router.get("/users/{user_id}/is_new", response_model=bool)
def is_new_loyalty_user(user_id: int):
    return loyalty_crud.user_exists(user_id)
