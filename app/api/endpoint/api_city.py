from typing import Any, List

from fastapi import APIRouter, Body, HTTPException

from app.crud import db_city as cities_crud
from app.crud import db_loyalty as loyalty_crud
from app.crud import db_user as user_crud
from app.schemas.sh_city import CityTransaction

router = APIRouter()


@router.post("/users", response_model=dict)
async def add_user_to_city(user_id: int = Body(..., embed=True)):
    if cities_crud.is_first_time_in_city(user_id):
        cities_crud.add_user_to_city_table(user_id)
        return {"message": "User added to city table successfully"}
    else:
        raise HTTPException(
            status_code=400, detail="User already in city table"
        )


@router.put("/free_try/{user_id}", response_model=dict)
async def use_free_try(user_id: int):
    cities_crud.set_free_try_used(user_id)
    return {"message": "Free try used successfully"}


@router.get("/all-users-free-try", response_model=dict)
async def get_all_users_free_try(all: bool = False):
    users = user_crud.get_all_users()
    for user in users:
        if cities_crud.is_first_time_in_city(user["user_id"]):
            cities_crud.add_user_to_city_table(user["user_id"])

    users = cities_crud.get_all_city_users_and_free_tries(all)
    return {"users": [dict(user) for user in users]}
    # return {"message": "Free try used successfully"}


@router.put("/request-recived/{user_id}", response_model=dict)
async def set_request_recived(user_id: int):
    cities_crud.set_recive_request(user_id)
    return {"message": "Successfully"}


@router.put("/set-user-answer/{user_id}", response_model=dict)
async def set_user_answer(user_id: int, answer: dict[str, Any] = Body(...)):
    cities_crud.set_answer(user_id, answer["answer"])
    return {"message": "Successfully"}


@router.get("/all-answers", response_model=dict)
async def get_all_answers():
    return cities_crud.get_all_answers()
    # return {"message": "Free try used successfully"}


@router.get("/has_free_try/{user_id}", response_model=bool)
async def check_free_try(user_id: int):
    return cities_crud.has_free_try(user_id)


@router.put("/unlimited_compatibility/{user_id}", response_model=dict)
async def set_unlimited_compatibility(user_id: int):
    cities_crud.set_unlimited_city_compatibility(user_id)
    return {"message": "Unlimited city compatibility set successfully"}


@router.get("/has_unlimited_compatibility/{user_id}", response_model=bool)
async def check_unlimited_compatibility(user_id: int):
    return cities_crud.has_unlimited_city_compatibility(user_id)


@router.post("/checked_cities", response_model=dict)
async def add_checked_city(
    user_id: int = Body(...), city_name: str = Body(...)
):
    cities_crud.add_checked_city(user_id, city_name)
    return {"message": "Checked city added successfully"}


@router.get("/checked_cities/{user_id}", response_model=List[str])
async def get_checked_cities(user_id: int):
    return cities_crud.get_checked_cities(user_id)


@router.post("/transactions", response_model=int)
async def create_city_transaction(
    user_id: int = Body(...),
    amount: int = Body(...),
    type: str = Body(...),
    bonus: int = Body(embed=True, default=0),
    service: str = Body(embed=True, default=""),
):
    if type == "city":
        return cities_crud.record_city_transaction(user_id, amount)
    else:
        return loyalty_crud.record_pre_transaction(
            user_id, amount, bonus, service
        )


# @router.get("/transactions/last")
# async def get_last_transaction_id():
#     try:
#         last_id = get_last_transaction_id()
#         return last_id
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/transactions/last")
async def get_last_transaction_id():
    try:
        last_id = await cities_crud.get_last_transaction_id_from_db()
        return {"last_transaction_id": last_id}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}"
        )


@router.get("/transactions/{user_id}", response_model=List[CityTransaction])
async def get_user_transactions(user_id: int, limit: int = 5):
    return cities_crud.get_user_city_transactions(user_id, limit)


@router.get("/free_tries_left/{user_id}", response_model=int)
async def get_free_tries_left(user_id: int):
    return cities_crud.get_free_tries_left(user_id)


@router.get("/first_time/{user_id}", response_model=bool)
def is_first_time_in_city(user_id: int):
    return cities_crud.is_first_time_in_city(user_id)


@router.get("/arcan/{user_id}", response_model=int)
def get_user_arcan(user_id: int):
    arcan = cities_crud.which_arcan(user_id)
    # if arcan is None:
    #     raise HTTPException(
    #         status_code=404, detail="Arcan not found for this user"
    #     )
    return arcan


"""




# @router.post("/checked_cities", response_model=dict)
# def add_checked_city(user_id: int, city_name: str):
#     cities_crud.add_checked_city(user_id, city_name)
#     return {"message": "Checked city added successfully"}

# @router.post("/users", response_model=dict)
# def add_user_to_city(user_id: int):
#     if is_first_time_in_city(user_id):
#         cities_crud.add_user_to_city_table(user_id)
#         return {"message": "User added to city table successfully"}
#     else:
#         raise HTTPException(
#             status_code=404, detail="User already in city table"
#         )

from fastapi import Body


@router.post("/users", response_model=dict)
def add_user_to_city(user_id: int = Body(..., embed=True)):
    if cities_crud.is_first_time_in_city(user_id):
        cities_crud.add_user_to_city_table(user_id)
        return {"message": "User added to city table successfully"}
    else:
        raise HTTPException(
            status_code=400, detail="User already in city table"
        )


@router.put("/free_try/{user_id}", response_model=dict)
def use_free_try(user_id: int):
    cities_crud.set_free_try_used(user_id)
    return {"message": "Free try used successfully"}


@router.get("/has_free_try/{user_id}", response_model=bool)
def check_free_try(user_id: int):
    return cities_crud.has_free_try(user_id)


@router.put("/unlimited_compatibility/{user_id}", response_model=dict)
def set_unlimited_compatibility(user_id: int):
    cities_crud.set_unlimited_city_compatibility(user_id)
    return {"message": "Unlimited city compatibility set successfully"}


@router.get("/has_unlimited_compatibility/{user_id}", response_model=bool)
def check_unlimited_compatibility(user_id: int):
    return cities_crud.has_unlimited_city_compatibility(user_id)


@router.post("/checked_cities", response_model=dict)
def add_checked_city(user_id: int = Body(...), city_name: str = Body(...)):
    cities_crud.add_checked_city(user_id, city_name)
    return {"message": "Checked city added successfully"}


@router.get("/checked_cities/{user_id}", response_model=List[str])
def get_checked_cities(user_id: int):
    return cities_crud.get_checked_cities(user_id)


@router.post("/transactions", response_model=dict)
def create_city_transaction(user_id: int, amount: int):
    cities_crud.record_city_transaction(user_id, amount)
    return {"message": "City transaction recorded successfully"}


@router.get("/transactions/{user_id}", response_model=List[CityTransaction])
def get_user_transactions(user_id: int, limit: int = 5):
    return cities_crud.get_user_city_transactions(user_id, limit)


@router.get("/free_tries_left/{user_id}", response_model=int)
def get_free_tries_left(user_id: int):
    return cities_crud.get_free_tries_left(user_id)
"""
