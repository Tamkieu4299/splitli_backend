from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select
from sqlalchemy.orm import relationship
from models.donation import Donation
from ._base_model import BaseModel


class Site(BaseModel):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    longtitude = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, default=0, nullable=False)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)

    donations = relationship(
        "Donation", back_populates="site", cascade="all, delete-orphan"
    )

    @hybrid_property
    def list_of_donors(self):
        if not self.donations:
            return []

        return [
            {**d.user.__dict__, "has_approved": d.has_approved}
            for d in self.donations
        ]

    @hybrid_property
    def amount_of_donors(self):
        return len(self.donations)

    @amount_of_donors.expression
    def amount_of_donors(cls):
        return (
            select(func.count(Donation.id))
            .where(Donation.site_id == cls.id)
            .label("amount_of_donors")
        )

    @hybrid_property
    def amount_of_blood(self):
        return sum(
            donation.volume_of_blood
            for donation in self.donations
            if donation.has_approved
        )

    @amount_of_blood.expression
    def amount_of_blood(cls):
        return (
            select(func.sum(Donation.volume_of_blood))
            .where(Donation.site_id == cls.id, Donation.has_approved == True)
            .label("amount_of_blood")
        )

    @hybrid_property
    def amount_of_approved_donors(self):
        return len(
            [donation for donation in self.donations if donation.has_approved]
        )

    @amount_of_approved_donors.expression
    def amount_of_approved_donors(cls):
        return (
            select(func.count(Donation.id))
            .where(Donation.site_id == cls.id, Donation.has_approved == True)
            .label("amount_of_approved_donors")
        )

    class Config:
        orm_mode = True
