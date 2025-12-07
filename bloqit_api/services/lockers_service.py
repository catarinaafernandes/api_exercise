from bloqit_api.schemas.lockers import Locker
from bloqit_api.data.json_db import load_lockers, write_json
from bloqit_api.services.logger import log_change


LOCKERS_FILE = "lockers.json"

#for logs : save changes to json and log files  
def _save_lockers(lockers : list[Locker]) -> None:
    #load old lockers
    old_lockers = [l.model_dump(mode="json") for l in load_lockers()]  
    new_lockers = [l.model_dump(mode="json") for l in lockers]

    #logchange 
    for new in new_lockers:
        
        old = next((o for o in old_lockers if o["id"] == new["id"]), None)
        action = "CREATED" if old is None else "UPDATED"
        log_change("lockers", new["id"], old, new, action)

    write_json(LOCKERS_FILE, new_lockers) #save after logging


#getters
#list every locker
def get_all_lockers() -> list[Locker]:
    return load_lockers()


def get_locker_by_id(locker_id: str):
    lockers = load_lockers()
    locker = next((l for l in lockers if l.id == locker_id), None)

    if locker is None:
        raise ValueError("Locker not found")
    return locker