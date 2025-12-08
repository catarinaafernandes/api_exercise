from pydantic import BaseModel
from bloqit_api.schemas.rents import RentSize

class RentCreateRequest(BaseModel):
    weight: int
    size: RentSize

class RentDropoffRequest(BaseModel):    
    locker_id: str
    rent_id: str

class RentConfirmDropoffRequest(BaseModel):
    rent_id: str

class RentRetriveRequest(BaseModel):
    rent_id: str    