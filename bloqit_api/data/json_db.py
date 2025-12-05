import json
from pathlib import Path
from bloqit_api.schemas.blocks import Bloq
from bloqit_api.schemas.lockers import Locker 
from bloqit_api.schemas.rents import Rent


DATA_PATH = Path("bloqit_api/data")



def read_json(filename:str):
    file_path = DATA_PATH/filename
    with open(DATA_PATH/file_path, "r", encoding="utf-8") as f:
        return json.load(f)



def get_bloqs():
    return read_json("bloqs.json")


def get_lockers():
    return read_json("lockers.json")


def get_rents():
    return read_json("rents.json")




def load_bloqs():
    return 