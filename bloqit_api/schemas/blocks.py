from pydantic import BaseModel


#each bloq has lockers , lockers may contain rent
class Bloq(BaseModel):
    id: str
    title: str
    address: str
