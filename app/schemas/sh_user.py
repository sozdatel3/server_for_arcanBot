from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: Optional[str] = None
    user_id: int
    chat_id: int
    referral_code: Optional[str] = None


class UserBasic(BaseModel):
    user_id: int
    chat_id: int
    username: Optional[str] = None


class UserUpdate(BaseModel):
    birth_date: Optional[str] = None
    first_sphere: Optional[int] = None
    points: Optional[int] = None
    discount_end: Optional[str] = None


class User(BaseModel):
    id: int
    username: Optional[str] = None
    user_id: int
    chat_id: int
    arcan: Optional[int] = None
    referral_code: Optional[str] = None
    first_name: Optional[str] = None
    discount_end: Optional[str] = None
    first_meet: Optional[str] = None
    first_sphere: Optional[int] = None
    file_sent: Optional[bool] = None
    feedback_choice: Optional[str] = None
    alredy_recive_one: Optional[str] = None
    march_send: Optional[bool] = None
    march_sphere_chosen: Optional[str] = None
    march_send_all: Optional[bool] = None
    no_friend: Optional[bool] = None
    comp_send: Optional[bool] = None
    time: Optional[str] = None
    april_sphere_chosen: Optional[str] = None
    april_send_to: Optional[bool] = None
    after_advert: Optional[str] = None
    may_send: Optional[bool] = None
    del_: Optional[bool] = None
    client_story: Optional[str] = None
    june_send: Optional[bool] = None
    jule_send: Optional[bool] = None
    do_u_know_inst: Optional[str] = None
    forecast_reminder: Optional[bool] = None
