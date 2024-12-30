
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


class UserRegisterBaseSchema(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    password: str
    gender: int
    phone: str
    email: str
    sum_of_do_bloods: float = 0
    type_of_blood: str
    role: Literal["donor", "admin", "vendor"]  = "donor"

    class Config:
        orm_mode = True

class LoginMobileSchema(BaseModel):
    phone: str
    password: str

    class Config:
        orm_mode = True
        
class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True 

class ResetPasswordBaseSchema(BaseModel):
    id: str
    password: str
    new_password: str

    class Config:
        orm_mode = True

class SimpleResetPasswordSchema(BaseModel):
    phone: str
    new_password: str


class RegisterResponse(BaseModel):
    id: int
    user_name: str
    first_name: str
    last_name: str
    gender: int
    phone: str
    email: str
    token: str
    token_type: str
    sum_of_do_bloods: float = 0
    type_of_blood: str
    role = str

    class Config:
        orm_mode = True
        json_encoders = {
            date: lambda v: v.isoformat(),  # Convert date to ISO format string
            datetime: lambda v: v.isoformat()  # Convert datetime to ISO format string
        }

class LoginResponse(BaseModel):
    id: int
    user_name: str
    first_name: str
    last_name: str
    phone: str
    email: str
    token: str
    token_type: str
    sum_of_do_bloods: float = 0
    type_of_blood: str
    role = str

    class Config:
        orm_mode = True