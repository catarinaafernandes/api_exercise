from pydantic import BaseModel
from enum import Enum

class LockerStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
#we can add more status if needed, now we have these two



class Locker(BaseModel):
    id: str
    bloqId: str
    status: LockerStatus
    isOccupied: bool

    





