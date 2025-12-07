from fastapi import APIRouter, HTTPException, status
from bloqit_api.services import rents_service
from bloqit_api.data.json_db import load_rents
from bloqit_api.schemas.rents import RentSize, Rent
from pydantic import BaseModel


router = APIRouter()


#error handling (for exceptions)
def http_error(message: str):
    msg = message.lower()

    if "not found" in msg:
        return HTTPException(status_code=404, detail=message)
    #404 for rent_id or locker_id not found

    if "occupied" in msg or "unavailable" in msg:
        return HTTPException(status_code=409, detail=message)
    #409 for conflict of states - ex:

    if "state" in msg:
        return HTTPException(status_code=400, detail=message)
    #400 - ex:

    return HTTPException(status_code=400, detail=message)
    #400 bad request, default error - error form client



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
    try:
        return rents_service.create_rent(weight, size)
    except ValueError as e:
        raise http_error(str(e))
    
        

#posts to id
#post action in a resource that was already created
@router.post("/{rent_id}/dropoff", response_model=Rent,
             summary= "Assign rent to locker and change state to WAITING DROPOFF")
def dropoff(rent_id: str, lockerId:str):
    try:
        return rents_service.dropoff(rent_id, lockerId)
    except ValueError as e:
        raise http_error(str(e))
    


@router.post("/{rent_id}/confirm", response_model=Rent,
             summary="Confirm dropoff and set WAITING_PICKUP")
def confirm_dropoff(rent_id:str):
    try:
        return rents_service.confirm_dropoff(rent_id)
    except ValueError as e:
        raise http_error(str(e))
    


@router.post("/{rent_id}/retrieve", response_model=Rent)
def retrieve(rent_id: str):
    try:
        return rents_service.retrieve(rent_id)
    except ValueError as e:
        raise http_error(str(e))
    


#TODO: add DTOs (REST)




