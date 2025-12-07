# 1 rent -> 1 locker -> 1 block
#dropoff / retrieve - important methods for business logic
#workflow: create -dropoff- confirm dropoff - retireve

from bloqit_api.data.json_db import load_rents, load_lockers, write_json
from bloqit_api.schemas.lockers import Locker
from datetime import datetime
import uuid #To generate unique IDs
from bloqit_api.schemas.rents import RentSize, RentStatus, Rent
from bloqit_api.services.logger import log_change
from fastapi import HTTPException


RENTS_FILE = "rents.json"
LOCKERS_FILE = "lockers.json"


#auxs to save data
#for logs
def _save_rents(rents : list[Rent]) -> None:
    #load old rents
    old_rents = [r.model_dump(mode="json") for r in load_rents()]  
    new_rents = [r.model_dump(mode="json") for r in rents]

    #logchange 
    for new in new_rents:
        
        old = next((o for o in old_rents if o["id"] == new["id"]), None)
        action = "CREATED" if old is None else "UPDATED"
        log_change("rents", new["id"], old, new, action)

    write_json(RENTS_FILE, new_rents) #save after logging



def _save_lockers(lockers: list[Locker]) -> None:
    #load old lockers
    old_lockers= [l.model_dump(mode="json") for l in load_lockers()]  
    new_lockers = [l.model_dump(mode="json") for l in lockers]

    for new in new_lockers:
        
        old = next((o for o in old_lockers if o["id"] == new["id"]), None)
        action = "CREATED" if old is None else "UPDATED"
        log_change("lockers", new["id"], old, new, action)

    write_json(LOCKERS_FILE, new_lockers)


#Getters
#list every rent
def all_rents() -> list[Rent]:
    return load_rents()


#util funct to avoid repeating text in the functions below
#find a rent inside a loaded list of rents, returns rent obj if found or none
def get_rent(rents: list[Rent], rent_id: str) -> Rent | None:
    return next((r for r in rents if r.id == rent_id), None)


def get_rent_by_id(rent_id:str):
    rents = bloqs = load_rents()
    rent = next((r for r in rents if r.id == rent_id), None)

    if rent is None:
        raise HTTPException(status_code=404, detail="Rent not found")
    return rent


#function to create rent (still without locker) 
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
    rent = get_rent(rents, rent_id)
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
#WAITING_DROPOFF -> change state do WAITING_PICKUP
def confirm_dropoff(rent_id:str):
    rents = load_rents()

    #search rent with the given id
    rent =get_rent(rents, rent_id)
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
    rent = get_rent(rents, rent_id)
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

