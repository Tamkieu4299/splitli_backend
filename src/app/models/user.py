from sqlalchemy import Column, Integer, String,Float
from sqlalchemy.orm import relationship

from ._base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(Integer, nullable=True)
    email = Column(String, nullable=True)

    
    class Config:
        orm_mode = True
