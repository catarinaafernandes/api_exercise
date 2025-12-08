from fastapi.testclient import TestClient
from bloqit_api.main import app
import pytest
from bloqit_api.schemas.rents import RentSize, RentStatus
import shutil
from pathlib import Path


#test with endpoints without python(already tested with postman)
client = TestClient(app)


#garantee that jsons event in tmep path go back to the original state to isolate
@pytest.fixture
def tmp_env(monkeypatch, tmp_path):
    source = Path(__file__).parent.parent/"bloqit_api"/"data"
    test_data = tmp_path/"json"

    if test_data.exists():
        shutil.rmtree(test_data)
    test_data.mkdir()

    for file in source.glob("*.json"):
        shutil.copy(file, test_data/file.name)

    monkeypatch.setenv("JSON_PATH", str(test_data))
    return test_data


#test workflow complete
#1)test create rent
def test_create_rent(tmp_env):
    payload = {"weight":5, "size":"M"}
    response = client.post("/rents/",json=payload)
    assert response.status_code==201
    data = response.json()
    assert data["weight"] == 5
    assert data["size"] == RentSize.M.value
    assert data["status"] == RentStatus.CREATED.value
    assert "id" in data
    

    
#2)test dropoff
def test_dropoff(tmp_env):

#create rent inside this test
    payload = {"weight": 5, "size": "M"}
    response = client.post("/rents/", json=payload)
    rent_id = response.json()["id"]
    
    locker_id = "3c881050-54bb-48bb-9d2c-f221d10f876b"
    payload = {"locker_id": locker_id}
    response = client.post(f"/rents/{rent_id}/dropoff", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == RentStatus.WAITING_DROPOFF.value
    assert data["lockerId"] == locker_id
    
  
#3)test confirm dropoff
def test_confirm_dropoff(tmp_env):

    #create rent first
    rent = client.post("/rents", json={"weight":5, "size": "M"}).json()
    rent_id = rent["id"]

    #dropoff
    locker =  {"locker_id": "3c881050-54bb-48bb-9d2c-f221d10f876b"}
    client.post(f"/rents/{rent_id}/dropoff", json=locker)

    #confirm dropoff
    response =   client.post(f"/rents/{rent_id}/confirm_dropoff")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == RentStatus.WAITING_PICKUP.value



#4) test retrive
def test_retrieve(tmp_env):

    #create rent 
    rent = client.post("/rents", json={"weight":5, "size": "M"}).json()
    rent_id = rent["id"]

    #dropoff
    locker =  {"locker_id": "3c881050-54bb-48bb-9d2c-f221d10f876b"}
    client.post(f"/rents/{rent_id}/dropoff", json=locker)

    #confirm dropoff
    client.post(f"/rents/{rent_id}/confirm_dropoff")

    #RETRIEVE
    response =   client.post(f"/rents/{rent_id}/retrieve")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == RentStatus.DELIVERED.value 


    

## other tests
#tests if endpoint GET/rents responses correctly
def test_list_all_rents(tmp_env):
    response = client.get("/rents")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)



#more tests - other situations
def test_confirm_without_dropoff(tmp_env):
    rent = client.post(f"/rents/", json ={"weight" :1, "size": "S"}).json()
    client.post(f"/rents/{rent['id']}/dropoff", json={"locker_id":"3c881050-54bb-48bb-9d2c-f221d10f876b"})

    response = client.post(f'/rents/{rent["id"]}/retrieve')
    assert response.status_code >=400   #error code equal or higher than 400

                                    