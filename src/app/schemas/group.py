from pydantic import BaseModel
from typing import Optional, List

class GroupAdd(BaseModel):
    name: str
    owner_id: int

    class Config:
        orm_mode = True