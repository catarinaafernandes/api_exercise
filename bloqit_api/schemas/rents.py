from pydantic import BaseModel
from enum import Enum
from datetime import datetime, timezone
from typing import Optional
from pydantic import Field


class RentStatus(str,Enum):
  CREATED = "CREATED"
  WAITING_DROPOFF = "WAITING_DROPOFF"
  WAITING_PICKUP = "WAITING_PICKUP"
  DELIVERED = "DELIVERED"

class RentSize(str, Enum):
  XL = "XL"
  L = "L"
  M = "M"
  S = "S"
  XS = "XS"

class Rent(BaseModel):
  id: str
  lockerId: str|None   #saw in rents.json
  weight: int
  size: RentSize
  status: RentStatus
  createdAt: datetime = Field(default_factory = lambda:datetime.now(timezone.utc))
  droppedOffAt: Optional[datetime] = None
  pickedUpAt: Optional[datetime] =None


