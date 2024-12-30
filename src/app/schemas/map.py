from pydantic import BaseModel
from typing import List

class BloodDonationSite(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    donation_hours: str
    required_blood_types: List[str]


class RouteRequest(BaseModel):
    user_lat: float
    user_lng: float
    destination_lat: float
    destination_lng: float