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
    avatar = Column(String, nullable=True)

    joins = relationship(
        "Join", back_populates="user", cascade="all, delete-orphan"
    )
    debts = relationship(
        "Owe", foreign_keys="[Owe.user_id]", back_populates="user", cascade="all, delete-orphan"
    )
    credits = relationship(
        "Owe", foreign_keys="[Owe.creditor_id]", back_populates="creditor", cascade="all, delete-orphan"
    )
    class Config:
        orm_mode = True
