from pydantic import BaseModel
from enum import Enum

class RentStatus(str,Enum):
  CREATED = "CREATED"
  WAITING_PICKUP = "WAITING_PICKUP"
  WAITING_DROPOFF = "WAITING_DROPOFF"
  DELIVERED = "DELIVERED"

class Rent(BaseModel):
  id: str
  locker_id: str|None   #saw in rents.json
  weight: int
  size:str
  status: RentStatus