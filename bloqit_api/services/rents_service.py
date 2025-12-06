# 1 rent -> 1 locker -> 1 block
#dropoff / retrieve - important methods for business logic
#workfow: create -dropoff- confirm dropoff - retireve

from bloqit_api.data.json_db import load_rents, load_lockers, write_json
from bloqit_api.schemas.lockers import Locker
from datetime import datetime
import uuid #To generate unique IDs
from bloqit_api.schemas.rents import RentSize, RentStatus, Rent


RENTS_FILE = "rents.json"
LOCKERS_FILE = "lockers.json"


#auxs to save data
#rents/lockers -> dict->
def _save_rents(rents : list[Rent]) -> None:
    data = [r.dict() for r in rents]
    #write_json(RENTS_FILE, data)
    write_json(RENTS_FILE, [r.model_dump(mode="json") for r in rents])



def _save_lockers(lockers: list[Locker]) -> None:
    data = [l.dict() for l in lockers]
    write_json(LOCKERS_FILE, data)


#Getters
#list every rent
def all_rents() -> list[Rent]:
    return load_rents()

#return rent that matches given ID or None if not found
def get_rent_by_id(rent_id: str) -> Rent | None:
    for r in load_rents():
        if r.id == rent_id:
            return r
    return None



#function to cretae rent (still without locker) 
def create_rent(weight:int, size:RentSize):
    rents = load_rents()
    rent = Rent(
        id = str(uuid.uuid4()),
        lockerId = None,
        weight = weight,
        size = size,
        status = RentStatus.CREATED,
        createdAt=datetime.utcnow()
    )

    rents.append(rent)
    _save_rents(rents)
    return rent


#DROPOFF - rent already created + ocupy one locker
#states: creates rent - waiting dropoff - waiting pickup - delivered
#rent need to be created to drop off
def dropoff(rent_id: str, locker_id: str): #assign rent to locker and chenge state to WAITINGDROPOFF

    lockers= load_lockers()
    rents = load_rents()   #list that will be saved back

    # find the rent inside the list rents
    rent = next((r for r in rents if r.id == rent_id), None)
    if rent is None:
        raise ValueError("Rent not found")

    if rent.status != RentStatus.CREATED:
        raise ValueError("Rent has to be created before drop-off")

    # find the locker
    locker = next((l for l in lockers if l.id == locker_id), None)
    if locker is None:
        raise ValueError("Locker not found")
    #attention:locker just can be used if open and not occupied! the locker can be open but occupied or closed and not occuoied
    if locker.status != "OPEN" or locker.isOccupied:
        raise ValueError("Locker is unavailable or occupied")

    #updates rent 
    rent.lockerId = locker_id
    rent.status = RentStatus.WAITING_DROPOFF
    rent.droppedOffAt = datetime.utcnow()

    # update locker to occupied
    locker.isOccupied = True

    # save changes
    _save_rents(rents)
    _save_lockers(lockers)

    return rent


#when customer drops off :locker is closed  - is waiting to pickup
#WAITING_DROPOFF -> chang state do WAITING_PICKUP
def confirm_dropoff(rent_id:str):
    rents = load_rents()

    #search rent with the given id
    rent = next ((r for r in rents if r.id == rent_id), None)
    if rent is None:
        raise ValueError("Rent not found")
    
    #verifies if state is Waiitng_dropoff
    if rent.status != RentStatus.WAITING_DROPOFF:
        raise ValueError(f"Can not confirm drop off because rent is {rent.status} , expected WAITING_DROPOFF state and must be")

    #updates rents list
    rent.status = RentStatus.WAITING_PICKUP
    _save_rents(rents)

    
    return rent

#RETRIEVE - ends rent + desocupy locker
#waiting_pickuo changes to DELIVERED state
def retrieve(rent_id: str):

    rents = load_rents()
    lockers = load_lockers()


    #search rent with the given id
    rent = next((r for r in rents if r.id == rent_id), None)
    if rent is None:
        raise ValueError("Rent not found")
    
    #check if rent is in correct state to retrieve
    if rent.status != RentStatus.WAITING_PICKUP:
        raise ValueError(f"Can not retrieve , rent state is {rent.status}, expected WAITING_PICKUP")
    
    #update 
    rent.status = RentStatus.DELIVERED
    rent.pickedUpAt = datetime.utcnow()

    #release locker
    locker = next((l for l in lockers if l.id == rent.lockerId), None)
    if locker:
        locker.isOccupied = False
        _save_lockers(lockers)


    _save_rents(rents)

    return rent

