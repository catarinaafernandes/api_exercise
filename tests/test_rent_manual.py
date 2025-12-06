from bloqit_api.services.rents_service import dropoff, retrieve, confirm_dropoff, create_rent
from bloqit_api.schemas.rents import RentSize

rent = create_rent(weight = 5, size = RentSize.M)
print("Rent created:", rent)


#rent = dropoff(rent.id, "6b33b2d1-af38-4b60-a3c5-53a69f70a351")
rent = dropoff(rent.id, "3c881050-54bb-48bb-9d2c-f221d10f876b")
print("dropped:", rent)


rent = confirm_dropoff(rent.id)
print("waiting pickup", rent)


rent = retrieve(rent.id)
print("delivered:", rent)



#TODO: test passed, reset jsons - need to track modifications to logfiles      