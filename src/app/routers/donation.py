from typing import List

from constants.config import Settings
from crud.donation import CRUDDonation
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.donation import Donation
from secret import get_current_active_user
from schemas.donation import DonationSchema, DonationResponse
from sqlalchemy.orm import Session
from utils.exception import CommonInvalid
from app.utils.response import Response

settings = Settings()

router = APIRouter()

donation_crud = CRUDDonation(Donation)


@router.post("/register", response_model=DonationResponse)
async def donation(    
    payload: DonationSchema,
    db: Session = Depends(get_db),
):  
    if donation_crud.read_by_user_id_and_donation_id(payload.user_id, payload.site_id,db):
        raise CommonInvalid(detail=f"You have registered for this site")
    donation = await donation_crud.create(payload.dict(), db)
    if donation is None:
        raise CommonInvalid(detail=f"Fail to create donation")
    return Response(content=DonationResponse.from_orm(donation))


@router.get("/donations", response_model=List[DonationResponse])
async def get_donations(    
    db: Session = Depends(get_db),
):
    donation = donation_crud.get_all(db)
    return Response(content=[DonationResponse.from_orm(i) for i in donation])

@router.get("/search_by_site/{site_id}")
async def get_site(
    site_id: int,
    db: Session = Depends(get_db),
):
    donations = donation_crud.get_by_site_id(site_id, db)
    return Response(content=[DonationResponse.from_orm(i) for i in donations])

@router.put("/approve/{donation_id}", response_model=DonationResponse)
async def approve_donation(
    donation_id: int,
    volume_of_blood: float,
    db: Session = Depends(get_db),
):
    updated_donation = donation_crud.update(donation_id, {"volume_of_blood": volume_of_blood, "has_approved": True}, db)
    if updated_donation is None:
        raise CommonInvalid(detail=f"Fail to update donation")
    return Response(content=DonationResponse.from_orm(updated_donation))


@router.put("/approve/{site_id}/{user_id}", response_model=DonationResponse)
async def approve_donation(
    site_id: int,
    user_id: int,
    volume_of_blood: float,
    db: Session = Depends(get_db),
):
    donation = donation_crud.read_by_user_id_and_donation_id(user_id, site_id,db)
    if donation is None:
        raise CommonInvalid(detail=f"You have not register for this site")
    if donation.get("has_approved"):
        raise CommonInvalid(detail=f"Your donation has been approved")
    updated_donation = donation_crud.update(donation.get("id"), {"volume_of_blood": volume_of_blood, "has_approved": True}, db)
    if updated_donation is None:
        raise CommonInvalid(detail=f"Fail to update donation")
    return Response(content=DonationResponse.from_orm(updated_donation))
