from datetime import datetime
import pytest

from app.routers.plant.models import Plant


def create_plant(test_sesion):
    plant = Plant(name="test_plant",
                  acquire_time=datetime.now(),
                  species="test_species",
                  watering_frequency=7,
                  user_id=1)
    test_session.add(plant)
    test_session.commit()
    return plant

@pytest.fixture
def test_token(test_client, test_user):
    response = test_client.post('/token',
                           data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token


def test_create_plant(test_client, test_user, test_token):
    response = test_client.post("/plant",
                                json={"name": "test_plant",
                                    "acquire_time": 
                                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "species": "test_species",
                                    "watering_frequency": 7},
                                headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 201
    print(response.json())


def test_read_plant(test_client, test_user, test_token):
    test_create_plant(test_client, test_user, test_token)
    response = test_client.get("/plant/1",
                               headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "test_plant"
