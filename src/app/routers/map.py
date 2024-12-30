from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
import googlemaps
from typing import List
from schemas.map import BloodDonationSite, RouteRequest
from utils.logger import setup_logger
from db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func, literal
from models.site import Site
from app.utils.response import Response

logger = setup_logger(__name__)

router = APIRouter()

GMAPS_API_KEY = "AIzaSyAmYG0ewlmb4zaJAkC6pBsFjqi0NBQu-Po"
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

@router.get("/nearest-site")
def get_nearest_site(user_lat: float, user_lng: float, db: Session = Depends(get_db)):
    try:
        distance_query = func.acos(
            func.sin(func.radians(user_lat)) * func.sin(func.radians(Site.latitude)) +
            func.cos(func.radians(user_lat)) * func.cos(func.radians(Site.latitude)) *
            func.cos(func.radians(Site.longtitude) - func.radians(user_lng))
        ) * 6371

        nearest_site = (
            db.query(Site, distance_query.label("distance"))
            .order_by(distance_query)
            .first()
        )

        if not nearest_site:
            raise HTTPException(status_code=404, detail="No sites found")

        site, distance = nearest_site
        return  Response(content={
            "id": site.id,
            "name": site.name,
            "latitude": site.latitude,
            "longtitude": site.longtitude,
            "city": site.city,
            "street": site.street,
            "distance_km": distance
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-route")
def get_route(route_request: RouteRequest):
    logger.info(f"Fetching route from ({route_request.user_lat}, {route_request.user_lng}) "
                f"to ({route_request.destination_lat}, {route_request.destination_lng})")

    directions = gmaps.directions(
        origin=(route_request.user_lat, route_request.user_lng),
        destination=(route_request.destination_lat, route_request.destination_lng),
        mode="driving"
    )   
    if not directions:
        logger.warning("No route found by the Google Directions API.")
        raise HTTPException(status_code=404, detail="No route found")

    overview_polyline = directions[0].get("overview_polyline", {}).get("points")
    legs = directions[0].get("legs", [])

    logger.info(f"Route successfully fetched. Polyline length: {len(overview_polyline) if overview_polyline else 0}")
    return {
        "overview_polyline": overview_polyline,
        "legs": legs
    }

