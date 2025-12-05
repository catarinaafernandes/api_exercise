# 1 rent -> 1 locker -> 1 block
#dropoff / retrieve - important methods for business logic

from bloqit_api.data.json_db import load_rents, load_lockers, write_json
from bloqit_api.schemas.rents import Rent
from bloqit_api.schemas.lockers import Locker
import datetime


RENTS_FILE = "rents.json"
LOCKERS_FILE = "lockers.json"


#auxs
#rents/lockers -> dict->
def _save_rents(rents : list[Rent]) -> None:
    data = [r.dict() for r in rents]
    write_json(RENTS_FILE, data)


def _save_lockers(lockers: list[Locker]) ->None:
    data = [l.dict() for l in lockers]
    write_json(LOCKERS_FILE, data)



#listing every rent
def all_rents() -> list[Rent]:
    return load_rents()


#find correct rent to 








#dropoff - create rent + ocupy one locker

#retrieve - ends rent + desocupy locker



