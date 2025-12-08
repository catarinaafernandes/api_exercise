from pathlib import Path
import os

def test_flow():
    from bloqit_api.schemas.rents import RentSize, RentStatus
    from bloqit_api.services.rents_service import create_rent,dropoff, confirm_dropoff, retrieve
    from bloqit_api.data.json_db import get_data_path

    tmp_path = get_data_path()
    rent = create_rent(weight = 5, size = RentSize.M, path=tmp_path)

    assert rent.status == RentStatus.CREATED
    

    rent = dropoff(rent.id, locker_id="3c881050-54bb-48bb-9d2c-f221d10f876b", path=tmp_path)
    assert rent.status == RentStatus.WAITING_DROPOFF

    rent = confirm_dropoff(rent.id, path=tmp_path)
    assert rent.status == RentStatus.WAITING_PICKUP

    rent = retrieve(rent.id, path=tmp_path)
    assert rent.status == RentStatus.DELIVERED

   
#tests passed but need reset jsons
#tests passed with tmp path without changing original jsons
#attention: we have to chose lockerd open and see state
#these tests call services diretcly, now we eill do tests for endpoints diretcly