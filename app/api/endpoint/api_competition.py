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
