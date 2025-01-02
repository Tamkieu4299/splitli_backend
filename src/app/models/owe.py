from sqlalchemy import Column, Integer, Float, ForeignKey

from sqlalchemy.orm import relationship
from ._base_model import BaseModel


class Owe(BaseModel):
    __tablename__ = "owes"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # The user who owes money
    creditor_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # The user to whom money is owed
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="debts")
    creditor = relationship("User", foreign_keys=[creditor_id], back_populates="credits")
    group = relationship("Group", back_populates="owes")