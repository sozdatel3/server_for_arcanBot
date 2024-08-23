from typing import List

from fastapi import APIRouter, Body, HTTPException

from app.crud import db_user as users_crud
from app.crud.db_loyalty import add_user_to_loyalty
from app.crud.db_scheduler import get_unique_users_count
from app.schemas.sh_user import User, UserCreate

router = APIRouter()


from fastapi import APIRouter

router = APIRouter()


@router.post("/", response_model=dict)
def create_user(user: UserCreate = Body(...)):
    if users_crud.is_user_exists(user.user_id):
        raise HTTPException(status_code=400, detail="User already exists")
    users_crud.add_user(
        user.username, user.user_id, user.chat_id, user.referral_code
    )
    add_user_to_loyalty(user.user_id)
    return {"message": "User created successfully"}


@router.get("/unique-users-count")
async def get_unique_users_count():
    count = await get_unique_users_count()
    return count


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)


@router.put("/{chat_id}/birth_date", response_model=dict)
async def update_birth_date(
    chat_id: int, birth_date: str = Body(..., embed=True)
):
    try:
        users_crud.set_birth_date(chat_id, birth_date)
        return {"message": "Birth date updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error updating birth date: {str(e)}"
        )


@router.get("/{user_id}/exists", response_model=dict)
def check_user_exists(user_id: int):
    exists = users_crud.is_user_exists(user_id)
    return {"exists": exists}


@router.get("/{user_id}/birth_date_known", response_model=dict)
def check_birth_date_known(user_id: int):
    known = users_crud.is_already_know_birth(user_id)
    return {"birth_date_known": known}


@router.put("/{user_id}/arcan", response_model=dict)
def set_user_arcan(user_id: int, arcan: int = Body(..., embed=True)):
    check_exist = users_crud.is_user_exists(user_id)
    if not check_exist:
        raise HTTPException(status_code=404, detail="User not found")
    users_crud.set_arcan(user_id, arcan)
    return {"arcan": arcan}


@router.get("/{user_id}/arcan", response_model=dict)
def get_user_arcan(user_id: int):
    arcan = users_crud.get_arcan(user_id)
    if arcan is None:
        raise HTTPException(
            status_code=404, detail="Arcan not found for this user"
        )
    return {"arcan": arcan}


@router.put("/{user_id}/no_friend", response_model=dict)
def set_no_friend(user_id: int):
    users_crud.db_no_friend(user_id)
    return {"message": "No friend status updated successfully"}


@router.put("/{user_id}/advert", response_model=dict)
def set_advert(user_id: int):
    users_crud.set_advert(user_id)
    return {"message": "Advert status updated successfully"}


@router.get("/{user_id}/first_sphere", response_model=dict)
def get_first_sphere(user_id: int):
    sphere = users_crud.get_first_sphere(user_id)
    return {"first_sphere": sphere}


# @router.get("/unique_users_count", response_model=dict)
# def get_unique_users_count():
#     count = users_crud.get_unique_users_count()
#     return {"unique_users_count": count}


@router.put("/{user_id}/first_sphere", response_model=dict)
def set_first_sphere(user_id: int, sphere: int = Body(..., embed=True)):
    users_crud.set_first_sphere(user_id, sphere)
    return {"message": "First sphere updated successfully"}


@router.put("/{user_id}/points", response_model=dict)
def add_points(user_id: int, points: int = Body(...)):
    users_crud.add_points(user_id, points)
    return {"message": f"Added {points} points to user {user_id}"}


@router.get("/{user_id}/march_choice", response_model=dict)
def get_march_choice(user_id: int):
    choice = users_crud.what_choose_in_march(user_id)
    return {"march_choice": choice["march_sphere_chosen"] if choice else None}


@router.put("/{chat_id}/receive_one", response_model=dict)
def set_receive_one(chat_id: int):
    users_crud.set_already_receive_one(chat_id)
    return {"message": "Receive one status updated successfully"}


@router.put("/{chat_id}/receive_all_march", response_model=dict)
def set_receive_all_march(chat_id: int):
    users_crud.set_already_receive_all_march(chat_id)
    return {"message": "Receive all March status updated successfully"}


@router.put("/{chat_id}/discount_end", response_model=dict)
def set_discount_end(chat_id: int, discount_end: str = Body(...)):
    users_crud.set_discount_end(chat_id, discount_end)
    return {"message": "Discount end date updated successfully"}


@router.put("/{user_id}/received_all_files", response_model=dict)
def set_received_all_files(user_id: int):
    users_crud.set_user_received_all_files(user_id)
    return {"message": "Received all files status updated successfully"}


@router.get("/{user_id}/received_one_file", response_model=dict)
def check_received_one_file(user_id: int):
    status = users_crud.check_if_user_received_one_file(user_id)
    return {"received_one_file": status}


@router.get("/{user_id}/nik", response_model=dict)
def get_user_nik(user_id: int):
    nik = users_crud.get_nik(user_id)
    if nik is None:
        raise HTTPException(
            status_code=404, detail="Nik not found for this user"
        )
    return {"nik": nik}


@router.get("/{user_id}/received_all_files", response_model=dict)
def check_received_all_files(user_id: int):
    status = users_crud.check_if_user_received_all_files(user_id)
    return {"received_all_files": status}


@router.get("/gift_dates", response_model=List[dict])
def get_gift_dates():
    return users_crud.get_gift_date()


@router.get("/active_users", response_model=List[dict])
def get_active_users():
    return users_crud.get_active_users()


@router.get("/inactive_users", response_model=List[dict])
def get_inactive_users():
    return users_crud.get_not_active_users()


@router.get("/button_users", response_model=List[dict])
def get_button_users():
    return users_crud.get_button_users()


@router.get("/reference_users", response_model=List[dict])
def get_reference_users():
    return users_crud.get_reference_users()


@router.get("/march_users_count", response_model=dict)
def get_march_users_count():
    count = users_crud.get_number_all_users_march()
    return {"march_users_count": count}


@router.get("/past_users_count", response_model=dict)
def get_past_users_count():
    count = users_crud.get_number_all_users_past()
    return {"past_users_count": count}


@router.get("/comp_send_false_users", response_model=List[int])
def get_comp_send_false_users():
    return users_crud.get_comp_send_false_and_no_one_per()


@router.put("/{chat_id}/comp_send", response_model=dict)
def set_comp_send(chat_id: int, set_value: bool = Body(...)):
    users_crud.set_comp_send_true(chat_id, set_value)
    return {"message": "Comp send status updated successfully"}


@router.put("/{chat_id}/time", response_model=dict)
def set_user_time(chat_id: int, time: str = Body(...)):
    users_crud.set_time(time, chat_id)
    return {"message": "User time updated successfully"}


@router.put("/{chat_id}/next_month_info", response_model=dict)
def add_next_month_info(chat_id: int, info: str = Body(...)):
    users_crud.add_info(chat_id, info)
    return {"message": "Next month info added successfully"}


"""
@router.post("/", response_model=dict)
def create_user(user: UserCreate):
    if users_crud.is_user_exists(user.user_id):
        raise HTTPException(status_code=400, detail="User already exists")
    users_crud.add_user(
        user.username, user.user_id, user.chat_id, user.referral_code
    )
    return {"message": "User created successfully"}


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)


@router.put("/{chat_id}/birth_date", response_model=dict)
def update_birth_date(chat_id: int, birth_date: str = Body(...)):
    users_crud.set_birth_date(chat_id, birth_date)
    return {"message": "Birth date updated successfully"}


@router.get("/{user_id}/exists", response_model=dict)
def check_user_exists(user_id: int):
    exists = users_crud.is_user_exists(user_id)
    return {"exists": exists}


@router.get("/{user_id}/birth_date_known", response_model=dict)
def check_birth_date_known(user_id: int):
    known = users_crud.is_already_know_birth(user_id)
    return {"birth_date_known": known}


@router.put("/{user_id}/{arcan}", response_model=dict)
def set_user_arcan(user_id: int, arcan: int):
    # arcan = users_crud.get_arcan(user_id)
    check_exist = users_crud.is_user_exists(user_id)
    if not check_exist:
        raise HTTPException(status_code=404, detail="User not found")
    users_crud.set_arcan(user_id, arcan)
    return {"arcan": arcan}


@router.get("/{user_id}/arcan", response_model=dict)
def get_user_arcan(user_id: int):
    arcan = users_crud.get_arcan(user_id)
    if arcan is None:
        raise HTTPException(
            status_code=404, detail="Arcan not found for this user"
        )
    return {"arcan": arcan}


@router.put("/{user_id}/no_friend", response_model=dict)
def set_no_friend(user_id: int):
    users_crud.db_no_friend(user_id)
    return {"message": "No friend status updated successfully"}


@router.put("/{user_id}/advert", response_model=dict)
def set_advert(user_id: int):
    users_crud.set_advert(user_id)
    return {"message": "Advert status updated successfully"}


@router.get("/{user_id}/first_sphere", response_model=dict)
def get_first_sphere(user_id: int):
    sphere = users_crud.get_first_sphere(user_id)
    return {"first_sphere": sphere}


@router.put("/{user_id}/first_sphere", response_model=dict)
def set_first_sphere(user_id: int, sphere: int):
    users_crud.set_first_sphere(user_id, sphere)
    return {"message": "First sphere updated successfully"}


@router.put("/{user_id}/points", response_model=dict)
def add_points(user_id: int, points: int):
    users_crud.add_points(user_id, points)
    return {"message": f"Added {points} points to user {user_id}"}


@router.get("/{user_id}/march_choice", response_model=dict)
def get_march_choice(user_id: int):
    choice = users_crud.what_choose_in_march(user_id)
    return {"march_choice": choice["march_sphere_chosen"] if choice else None}


@router.put("/{chat_id}/receive_one", response_model=dict)
def set_receive_one(chat_id: int):
    users_crud.set_already_receive_one(chat_id)
    return {"message": "Receive one status updated successfully"}


@router.put("/{chat_id}/receive_all_march", response_model=dict)
def set_receive_all_march(chat_id: int):
    users_crud.set_already_receive_all_march(chat_id)
    return {"message": "Receive all March status updated successfully"}


@router.put("/{chat_id}/discount_end", response_model=dict)
def set_discount_end(chat_id: int, discount_end: str):
    users_crud.set_discount_end(chat_id, discount_end)
    return {"message": "Discount end date updated successfully"}


@router.put("/{user_id}/received_all_files", response_model=dict)
def set_received_all_files(user_id: int):
    users_crud.set_user_received_all_files(user_id)
    return {"message": "Received all files status updated successfully"}


@router.get("/{user_id}/received_one_file", response_model=dict)
def check_received_one_file(user_id: int):
    status = users_crud.check_if_user_received_one_file(user_id)
    return {"received_one_file": status}


@router.get("/{user_id}/nik", response_model=dict)
def get_user_nik(user_id: int):
    nik = users_crud.get_nik(user_id)
    if nik is None:
        raise HTTPException(
            status_code=404, detail="Nik not found for this user"
        )
    return {"nik": nik}


@router.get("/{user_id}/received_all_files", response_model=dict)
def check_received_all_files(user_id: int):
    status = users_crud.check_if_user_received_all_files(user_id)
    return {"received_all_files": status}


@router.get("/gift_dates", response_model=List[dict])
def get_gift_dates():
    return users_crud.get_gift_date()


@router.get("/active_users", response_model=List[dict])
def get_active_users():
    return users_crud.get_active_users()


@router.get("/inactive_users", response_model=List[dict])
def get_inactive_users():
    return users_crud.get_not_active_users()


@router.get("/button_users", response_model=List[dict])
def get_button_users():
    return users_crud.get_button_users()


@router.get("/reference_users", response_model=List[dict])
def get_reference_users():
    return users_crud.get_reference_users()


@router.get("/march_users_count", response_model=dict)
def get_march_users_count():
    count = users_crud.get_number_all_users_march()
    return {"march_users_count": count}


@router.get("/past_users_count", response_model=dict)
def get_past_users_count():
    count = users_crud.get_number_all_users_past()
    return {"past_users_count": count}


@router.get("/comp_send_false_users", response_model=List[int])
def get_comp_send_false_users():
    return users_crud.get_comp_send_false_and_no_one_per()


@router.put("/{chat_id}/comp_send", response_model=dict)
def set_comp_send(chat_id: int, set_value: bool):
    users_crud.set_comp_send_true(chat_id, set_value)
    return {"message": "Comp send status updated successfully"}


@router.put("/{chat_id}/time", response_model=dict)
def set_user_time(chat_id: int, time: str):
    users_crud.set_time(time, chat_id)
    return {"message": "User time updated successfully"}


@router.put("/{chat_id}/next_month_info", response_model=dict)
def add_next_month_info(chat_id: int, info: str):
    users_crud.add_info(chat_id, info)
    return {"message": "Next month info added successfully"}
"""
