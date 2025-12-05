from pydantic import BaseModel


#each bloq has lockers , lockers may contain rent
#convert JSON to .py 
class Bloq(BaseModel):
    id: str
    title: str
    address: str
