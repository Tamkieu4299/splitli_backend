from sqlalchemy import Column, Integer, ForeignKey

from sqlalchemy.orm import relationship
from ._base_model import BaseModel


class Join(BaseModel):
    __tablename__ = "joins"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False)

    group = relationship("Group", back_populates="joins")
    user = relationship("User", back_populates="joins")

    class Config:
        orm_mode = True