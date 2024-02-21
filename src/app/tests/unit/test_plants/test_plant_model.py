import pytest

from datetime import datetime
from app.routers.plant.models import Plant


valid_plant_data = {
    "user_id": 1,
    "name": "plant name",
    "acquire_time": datetime.now,
    "is_alive": 1,
    "species": "plant species",
    "watering_frequency": 7,
}


def test_valid_plant():
    # Correct model
    assert Plant(
        user_id=1,
        name="plant name",
        acquire_time=datetime.now,
        is_alive=1,
        species="plant species",
        watering_frequency=7,
    )


@pytest.mark.parametrize(
    "key, value",
    [
        ("name", ""),
        ("name", True),
        ("name", "a"),
        ("name", "".join(["i" for _ in range(201)])),
    ],
)
def test_invalid_plant(key, value):
    # Wrong models
    data_set = valid_plant_data.copy()
    data_set[key] = value
    with pytest.raises((ValueError, TypeError)):
        Plant(**data_set)
