from datetime import datetime
import pytest


def create_plant(test_sesion):
    plant = m.Plant(name="test_plant",
                    acquire_time=datetime.now(),
                    species="test_species",
                    watering_frequency=7,
                    user_id=1)
    test_session.add(plant)
    test_session.commit()
    return plant
def test_token(test_client, test_user):
    response = test_client.post('/token',
                           data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token


def test_create_plant(test_client, test_user):
    token = test_token(test_client, test_user)
    response = test_client.post("/plant",
                                json={"name": "test_plant",
                                    "acquire_time": 
                                      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "species": "test_species",
                                    "watering_frequency": 7},
                                headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201


def test_read_plant(test_client, test_user):
    token = test_token(test_client, test_user)

