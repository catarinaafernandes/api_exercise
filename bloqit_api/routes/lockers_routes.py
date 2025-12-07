from bloqit_api.schemas.lockers import Locker
from bloqit_api.services.lockers_service import all_lockers, get_locker_by_id
from fastapi import APIRouter, HTTPException, status



router = APIRouter()

#GET
#get all
@router.get("/", response_model=list[Locker], 
            status_code = status.HTTP_200_OK, summary="List all lockers")
def list_lockers() -> list[Locker]:
    return all_lockers()


#get by id
@router.get("/{locker_id}", response_model=Locker,
            status_code=status.HTTP_200_OK, 
            summary="Get a locker by ID")
def get_locker(locker_id:str):
    try:
        return get_locker_by_id(locker_id)
    except HTTPException as e:
        raise e
    

"""don´t need POST because we don´t have info about possibility of creating new lockers 
and knowing that there are already some lockers.Same for bloqs"""