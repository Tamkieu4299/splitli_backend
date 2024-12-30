from pydantic import BaseModel
from typing import Optional, List

class SiteAdd(BaseModel):
    name: str
    city: str = None
    street: str = None
    longtitude: float = 0
    latitude: float = 0

    class Config:
        orm_mode = True

class SiteUpdate(BaseModel):
    name: Optional[str]
    city: Optional[str]
    street: Optional[str]
    longtitude: Optional[float]
    latitude: Optional[float]

class SiteFilter(BaseModel):
    name: Optional[str]
    city: Optional[str]
    street: Optional[str]
    longtitude: Optional[float] = 0
    latitude: Optional[float] = 0
    amount_of_donors: Optional[int]
    amount_of_approved_donors: Optional[int]
    amount_of_blood: Optional[int]

    class Config:
        orm_mode = True

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
    role: str
    has_approved: bool

    class Config:
        orm_mode = True

class SiteResponse(BaseModel):
    id: int
    name: str
    city: str = None
    street: str = None
    longtitude: float = 0
    latitude: float = 0
    amount_of_donors: int = 0
    amount_of_approved_donors: int = 0
    amount_of_blood: int = 0
    list_of_donors: List[UserResponseSchema] = []

    class Config:
        orm_mode = True
