from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select
from sqlalchemy.orm import relationship
from ._base_model import BaseModel


class Group(BaseModel):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)

    joins = relationship(
        "Join", back_populates="group", cascade="all, delete-orphan"
    )
    owes = relationship(
        "Owe", back_populates="group", cascade="all, delete-orphan"
    )

    class Config:
        orm_mode = True