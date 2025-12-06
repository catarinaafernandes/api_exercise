from fastapi import APIRouter, HTTPException, status
from bloqit_api.services import rents_service
from bloqit_api.data.json_db import load_rents
from bloqit_api.schemas.rents import RentSize, Rent


router = APIRouter


#GET
@router.get("/", response_model=list[Rent], 
            status_code = status.HTTP_200_OK, summary="List all rents")
def list_rents() -> list[Rent]:
    return load_rents()


#POST
@router.post("/", response_model=list[Rent], 
            status_code = status.HTTP_201_CREATED, 
            summary="Create a new rent")
             
def create_rent(

)