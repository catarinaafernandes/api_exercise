from fastapi import APIRouter, status
from bloqit_api.services import rents_service
from bloqit_api.schemas.rents import RentSize, Rent
from bloqit_api.utils.errors import http_error

router = APIRouter()


#GET 
#read
@router.get("/", response_model=list[Rent], 
            status_code = status.HTTP_200_OK,
            summary="List all rents")
def list_rents() -> list[Rent]:
    try:
        return rents_service.get_all_rents()
    except ValueError as e:
        raise http_error(str(e))



#get by id
@router.get("/{rent_id}", response_model=Rent,
            status_code=status.HTTP_200_OK, 
            summary="Get a Rent by ID")
def get_rent(rent_id:str):
    try:
        return rents_service.get_rent_by_id(rent_id)

    except ValueError as e:
        raise http_error(str(e))
    


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
def dropoff(rent_id: str, locker_id:str):
    try:
        return rents_service.dropoff(rent_id, locker_id)
    except ValueError as e:
        raise http_error(str(e))
    


@router.post("/{rent_id}/confirm", response_model=Rent,
             summary="Confirm dropoff and set WAITING_PICKUP")
def confirm_dropoff(rent_id:str):
    try:
        return rents_service.confirm_dropoff(rent_id)
    except ValueError as e:
        raise http_error(str(e))
    


@router.post("/{rent_id}/retrieve", response_model=Rent,
             summary= "Retrieve -parcel delivered")
def retrieve(rent_id: str):
    try:
        return rents_service.retrieve(rent_id)
    except ValueError as e:
        raise http_error(str(e))
    


#TODO: add DTOs (REST)




