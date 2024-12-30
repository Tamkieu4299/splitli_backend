from pydantic import BaseModel

# Define Pydantic schema
class VendorForJobResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    address_1: str
    address_2: str
    avatar: str = None
    business_license: str

    class Config:
        orm_mode = True  # To support SQLAlchemy models