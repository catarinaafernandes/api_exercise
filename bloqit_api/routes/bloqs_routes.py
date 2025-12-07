from bloqit_api.schemas.bloqs import Bloq
from bloqit_api.services.bloqs_service import all_bloqs, get_bloq_by_id
from fastapi import APIRouter, HTTPException, status


router = APIRouter()

#GET
#get all
@router.get("/", response_model=list[Bloq], 
            status_code = status.HTTP_200_OK, summary="List all bloqs")
def list_bloqs() -> list[Bloq]:
    return all_bloqs()


#get by id
@router.get("/{bloq_id}", response_model=Bloq,
            status_code=status.HTTP_200_OK, 
            summary="Get Bloq by ID")
def get_bloq(bloq_id:str):
    try:
        return get_bloq_by_id(bloq_id)
    except HTTPException as e:
        raise e