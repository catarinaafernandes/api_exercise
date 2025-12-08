from bloqit_api.schemas.rents import RentSize, RentStatus
from bloqit_api.services.rents_service import create_rent,dropoff, confirm_dropoff, retrieve, get_all_rents, save_rents, save_lockers
from bloqit_api.services.lockers_service import get_all_lockers
import bloqit_api.data.json_db as db
from pathlib import Path
import os



os.environ["JSON_PATH"] = str(Path("tests/data")) 
#db.DATA_PATH = Path("tests/data") 

def test_flow():

    rents = get_all_rents()
    lockers = get_all_lockers()

    rent = create_rent(weight = 5, size = RentSize.M)
    #assert rent.status == "created"
    #assert rent.status == "CREATED"
    assert rent.status == RentStatus.CREATED
    

    rent = dropoff(rent.id, locker_id="3c881050-54bb-48bb-9d2c-f221d10f876b")
    assert rent.status == RentStatus.WAITING_DROPOFF
    #assert rent.status == "dropped"

    rent = confirm_dropoff(rent.id)
    assert rent.status == RentStatus.WAITING_PICKUP

    rent = retrieve(rent.id)
    assert rent.status == RentStatus.DELIVERED

    save_rents(rents)
    save_lockers(lockers) 
   
#tests passed but need reset jsons