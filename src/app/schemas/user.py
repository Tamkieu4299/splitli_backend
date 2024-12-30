from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    id: int
    user_name: str
    first_name: str
    last_name: str
    gender: int
    phone: str
    email: str
    sum_of_do_bloods: float = 0
    type_of_blood: str
    role = str

    class Config:
        orm_mode = True


class UserUpdateInfoSchema(BaseModel):
    user_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[date]
    gender: Optional[int]
    phone: Optional[str]
    email: Optional[str]
    token: Optional[str]
    token_type: Optional[str]
    country: Optional[str]
    city: Optional[str]
    address_1: Optional[str]
    address_2: Optional[str]
   