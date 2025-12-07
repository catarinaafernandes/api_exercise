from fastapi import HTTPException
from bloqit_api.schemas.blocks import Bloq
from bloqit_api.data.json_db import write_json, load_bloqs
from bloqit_api.services.logger import log_change
import uuid


BLOQS_FILE = "bloqs.json"

#for logs : save changes to json and log files  
def _save_bloqs(bloqs : list[Bloq]) -> None:
    #load old bloqs
    old_bloqs = [l.model_dump(mode="json") for l in load_bloqs()]  
    new_bloqs = [l.model_dump(mode="json") for l in bloqs]

    #logchange 
    for new in new_bloqs:
        
        old = next((o for o in old_bloqs if o["id"] == new["id"]), None)
        action = "CREATED" if old is None else "UPDATED"
        log_change("bloqs", new["id"], old, new, action)

    write_json(BLOQS_FILE, new_bloqs) #save after logging


#getters
#list every bloq
def all_bloqs() -> list[Bloq]:
    return load_bloqs()


def get_bloq_by_id(bloq_id: str):
    bloqs = load_bloqs()
    bloq = next((b for b in bloqs if b.id == bloq_id), None)

    if bloq is None:
        raise HTTPException(status_code=404, detail="Bloq not found")
    return bloq



#function to create a bloq 
def create_bloq(title: str, address: str) :
    bloqs = load_bloqs()
    bloq = Bloq(
        id=str(uuid.uuid4()),
        title=title,
        address=address
    )
    bloqs.append(bloq)
    _save_bloqs(bloqs)
    return bloq
