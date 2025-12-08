import json,os
from pathlib import Path
from bloqit_api.schemas.bloqs import Bloq
from bloqit_api.schemas.lockers import Locker 
from bloqit_api.schemas.rents import Rent

#json files path
DATA_PATH = Path(os.environ.get("JSON_PATH", Path(__file__).parent))


#general function to read json - input
#json to py (desserializ)
def read_json(filename:str):
    file_path = DATA_PATH/filename
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

#general function to write json - output

def write_json(filename: str, data):
    file = DATA_PATH/filename
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)



#gave us json(raw)content
def get_bloqs():
    return read_json("bloqs.json")


def get_lockers():
    return read_json("lockers.json")


def get_rents():
    return read_json("rents.json")


#convert to pydantic
def load_bloqs():
    list =[]
    for b in get_bloqs():
        list.append(Bloq(**b))
    return list

def load_lockers():
    list = []
    for l in get_lockers():
        list.append(Locker(**l))
    return list
    
def load_rents():
    list = []
    for r in get_rents():
        list.append(Rent(**r))
    return list


#TODO change to a db and make seconds services and then re reoute accordingly