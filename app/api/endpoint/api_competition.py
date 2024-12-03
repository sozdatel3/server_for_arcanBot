from fastapi import APIRouter, HTTPException

from app.crud import db_competition as competition_crud

router = APIRouter()


@router.get("/is-user-in-competition/{user_id}", response_model=dict)
async def is_user_in_competition(user_id: int):
    return {
        "is_user_in_competition": competition_crud.is_user_in_competition(
            user_id
        )
    }


@router.get("/is-user-subscribed/{user_id}", response_model=dict)
async def is_user_subscribed(user_id: int):
    return {"is_user_subscribed": competition_crud.is_user_subscribed(user_id)}


@router.get("/referal-code/{user_id}", response_model=dict)
async def get_referal_code(user_id: int):
    return {"referal_code": competition_crud.get_secret_link(user_id)}


@router.get("/count-of-friends/{user_id}", response_model=dict)
async def get_count_of_friends(user_id: int):
    return {"count_of_friends": competition_crud.get_count_of_friends(user_id)}


@router.post("/add-user/{user_id}", response_model=dict)
async def add_user_to_competition(user_id: int):
    if not competition_crud.is_user_in_competition(user_id):
        competition_crud.add_user_to_competition(user_id)
        return {
            "message": "User added to competition table successfully",
            "success": True,
        }
    else:
        raise HTTPException(
            status_code=400, detail="User already in competition table"
        )


@router.post(
    "/set-inst-username/{user_id}/{inst_username}", response_model=dict
)
async def set_inst_username(user_id: int, inst_username: str):
    competition_crud.set_inst_username(user_id, inst_username)
    return {"message": "Inst username set successfully"}


@router.post("/set-refer-id/{user_id}/{refer_id}", response_model=dict)
async def set_refer_id(user_id: int, refer_id: int):
    competition_crud.set_refer_id(user_id, refer_id)
    return {"message": "Refer id set successfully"}


@router.post("/set-status/{user_id}/{status}", response_model=dict)
async def set_status(user_id: int, status: str):
    competition_crud.set_status(user_id, status)
    return {"message": "Status set successfully"}


@router.get("/get-status/{user_id}", response_model=dict)
async def get_status(user_id: int):
    return {"status": competition_crud.get_status(user_id)}


@router.get("/get-user_id-by-secret-link/{secret_link}", response_model=dict)
async def get_user_id_by_secret_link(secret_link: str):
    return {"user_id": competition_crud.get_user_by_secret_link(secret_link)}


@router.post("/increment-count-of-friends/{user_id}", response_model=dict)
async def increment_count_of_friends(user_id: int):
    competition_crud.increment_count_of_friends(user_id)
    return {"message": "Count of friends incremented successfully"}


@router.get("/get-all-users/{status}", response_model=dict)
async def get_all_users_status(status: str):
    return {"users": competition_crud.get_all_users_status(status)}
