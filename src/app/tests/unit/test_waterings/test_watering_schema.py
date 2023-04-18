import pytest

from src.app.routers.watering.schemas import WateringCreate


@pytest.mark.parametrize(
    "plant_id, user_id, timestamp, fertilizer",
    [
        (1, 1, "2023-04-12T18:11:29.275Z", 1),
        (2, 1, "2023-04-11T12:00:00.000Z", 0),
        (3, 2, "2023-04-10T10:30:30.500Z", 1),
        (4, 2, "2023-04-09T23:59:59.999Z", 0),
        (5, 1, "2023-04-08T06:15:45.123Z", 1),
        (6, 2, "2023-04-08T06:15:45.123Z", True),
        (7, 1, "2023-04-08T06:15:45.123Z", False),
    ]
)
def test_watering_create_correct(plant_id, user_id, timestamp, fertilizer):
    input_data = {
        "plant_id": plant_id,
        "user_id": user_id,
        "timestamp": timestamp,
        "fertilizer": fertilizer
    }
    obj = WateringCreate(**input_data)
    assert obj


@pytest.mark.parametrize(
    "plant_id, user_id, timestamp, fertilizer",
    [
        # Invalid plant_id values
        (0, 1, "2023-04-11T12:00:00.000Z", 0),
        (-1, 2, "2023-04-10T10:30:30.500Z", 1),
        (None, 2, "2023-04-09T23:59:59.999Z", 0),
        # Invalid user_id values
        (2, -1, "2023-04-08T06:15:45.123Z", 1),
        (3, None, "2023-04-08T06:15:45.123Z", 0),
        # Invalid timestamp values
        (4, 1, "invalid_timestamp", 1),
        (6, 1, "2023-04-06T25:00:00.000Z", 1),
        # Invalid fertilizer values
        (8, 1, "2023-04-04T11:11:11.111Z", None),
    ]
)
def test_watering_create_incorrect(plant_id, user_id, timestamp, fertilizer):
    input_data = {
        "plant_id": plant_id,
        "user_id": user_id,
        "timestamp": timestamp,
        "fertilizer": fertilizer
    }
    with pytest.raises(ValueError):
        obj = WateringCreate(**input_data)

