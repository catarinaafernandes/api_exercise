from fastapi.testclient import TestClient
from bloqit_api.main import app
import pytest
from bloqit_api.schemas.rents import RentSize, RentStatus
import shutil
from pathlib import Path


#test with endpoints without python(already tetsed with postaman)
client = TestClient(app)


#garantee that jsons event in tmep path go back to the origial state to isolate
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



def test_create_rent(tmp_env):
    payload = {"weight":5, "size":"M"}
    response = client.post("/rents/",json=payload)
    assert response.status_code==201
    data = response.json()
    assert data["weight"] == 5
    assert data["size"] == RentSize.M.value
    assert data["status"] == RentStatus.CREATED.value
    assert "id" in data
    

    

def test_dropoff(tmp_env):

#create rent inside thus test
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
    
  

"""to dropoff we need to use a rent that was already created so 
it has to be in the state created and not in state waiitng dropoff"""
#so use id rent from jsons in the previous state 