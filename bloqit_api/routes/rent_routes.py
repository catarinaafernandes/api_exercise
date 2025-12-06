from fastapi import APIRouter, HTTPException, status
from bloqit_api.services import rents_service
from bloqit_api.data.json_db import load_rents
from bloqit_api.schemas.rents import RentSize, Rent


router = APIRouter()


#GET 
#read
@router.get("/", response_model=list[Rent], 
            status_code = status.HTTP_200_OK, summary="List all rents")
def list_rents() -> list[Rent]:
    return load_rents()


#POST
#post withou id creates new resource
@router.post("/", response_model=Rent, 
            status_code = status.HTTP_201_CREATED, 
            summary="Create a new rent")
             
def create_rent(weight: int, size: RentSize):
    return rents_service.create_rent(weight, size)


#posts to id
#post action in a resource that was already created
@router.post("/{rent_id}/dropoff", response_model=Rent,
             summary= "Assign rent to locker and change state to WAITING DROPOFF")
def dropoff(rent_id: str, lockerId:str):
    return rents_service.dropoff(rent_id, lockerId)


@router.post("/{rent_id}/confirm", response_model=Rent,
             summary="Confirm dropoff and set WAITING_PICKUP")
def confirm_dropoff(rent_id:str):
    return rents_service.confirm_dropoff(rent_id)


@router.post("/{rent_id}/retrieve", response_model=Rent)
def retrieve(rent_id: str):
    return rents_service.retrieve(rent_id)


#TODO: add status codes and handling excepctions




