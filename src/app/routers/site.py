from typing import Optional

from constants.config import Settings
from crud.site import CRUDSite
from db.database import get_db
from fastapi import APIRouter, Depends, status, Query
from models.site import Site
from schemas.site import SiteAdd, SiteResponse, SiteUpdate, SiteFilter
from sqlalchemy.orm import Session
from utils.exception import CommonInvalid
from utils.logger import setup_logger

from app.utils.response import Response

logger = setup_logger(__name__)

settings = Settings()
router = APIRouter()

crud_site = CRUDSite(Site)


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
)
async def register_site(
    payload: SiteAdd,
    db: Session = Depends(get_db),
):
    new_site = await crud_site.create(payload.dict(), db)
    if new_site is None:
        raise CommonInvalid(detail=f"Fail to create site")
    return Response(content=SiteResponse.from_orm(new_site))


@router.put(
    "/update",
    status_code=status.HTTP_201_CREATED,
)
async def update_site(
    site_id: int,
    payload: SiteUpdate,
    db: Session = Depends(get_db),
):
    updated_site = crud_site.update(site_id, payload.dict(), db)
    if update_site is None:
        raise CommonInvalid(detail=f"Fail to update site")
    return Response(content=SiteResponse.from_orm(updated_site))


@router.get("/search/")
async def get_sites(
    db: Session = Depends(get_db),
):
    sites = crud_site.get_all(db, "created_at", "desc")
    sites_dict_list = [SiteResponse.from_orm(i) for i in sites]
    logger.info(f"Number of sites: {len(sites)}")
    return Response(content=sites_dict_list)


@router.get("/search/{id}")
async def get_site(
    id: int,
    db: Session = Depends(get_db),
):
    sites = crud_site.read(id, db)
    return Response(content=SiteResponse.from_orm(sites))

@router.post("/filter/")
async def filter_sites(
    payload: SiteFilter,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db),
):
    result = crud_site.filter_sites(
        db=db,
        name=payload.name,
        city=payload.city,
        street=payload.street,
        amount_of_donors=payload.amount_of_donors,
        amount_of_blood=payload.amount_of_blood,
        skip=skip,
        limit=limit,
    )
    sites_dict_list = [SiteResponse.from_orm(site) for site in result["results"]]
    return Response(content=sites_dict_list)
