from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import relationship

from ._base_model import BaseModel


class Donation(BaseModel):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id", onupdate="RESTRICT", ondelete="RESTRICT"), nullable=False)
    
    volume_of_blood = Column(Float, default=0, nullable=True)
    has_approved = Column(Boolean, default=False)

    site = relationship("Site", back_populates="donations")
    user = relationship("User", back_populates="donations")
    
    class Config:
        orm_mode = True 