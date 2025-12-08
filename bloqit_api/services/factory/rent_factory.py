from uuid import uuid4
from bloqit_api.schemas.rents import Rent, RentSize, RentStatus
from datetime import datetime, timezone

#design pattern factory


class RentFactory:
    @staticmethod
    def create(weight: int, size: RentSize):
        return Rent(
            id = str(uuid4()),
            weight=weight,
            size = size,
            status = RentStatus.CREATED,
            lockerId = None,
            droppedOffAt = None,
            pickedUpAt = None
        )

