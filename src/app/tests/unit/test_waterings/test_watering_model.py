import pytest

from datetime import datetime
from app.routers.watering.models import Watering


valid_watering_data = {
    "id": 1,
    "plant_id": 2,
    "timestamp": datetime(2023, 4, 12, 18, 11, 29, 275000),
    "fertilizer": True,
    "user_id": 3,
}


def test_valid_watering_model():
    assert Watering(**valid_watering_data)


@pytest.mark.parametrize(
    "key, value",
    [
        ("id", "string"),
        ("plant_id", "string"),
        ("timestamp", "string"),
        ("fertilizer", "string"),
        ("user_id", "string"),
    ],
)
def test_model_wrong(key, value):
    data_set = valid_watering_data.copy()
    data_set[key] = value
    with pytest.raises((ValueError, TypeError)):
        Watering(**data_set)
