import pytest
from pydantic import ValidationError

from app.routers.plant.schemas import PlantCreate


@pytest.mark.parametrize(
    "name, user_id, acquire_time, is_alive, species, watering_frequency, last_watering",
    [
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", 7, "2023-04-10T12:00:29.275Z"),
        ("another plant name", 2, "2023-04-11T10:23:29.275Z", 0, "cactus species", 14, "2023-04-08T08:30:29.275Z"),
        ("third plant name", 3, "2023-04-09T16:45:29.275Z", True, "fern species", 3, "2023-04-07T20:15:29.275Z"),
        ("third plant name", 3, "2023-04-09T16:45:29.275Z", False, "fern species", 3, "2023-04-07T20:15:29.275Z"),
    ],
)
def test_plant_create_schema_correct_data(name, user_id, acquire_time, is_alive, species, watering_frequency, last_watering):
    input_data = {
        "name": name,
        "user_id": user_id,
        "acquire_time": acquire_time,
        "is_alive": is_alive,
        "species": species,
        "watering_frequency": watering_frequency,
        "last_watering": last_watering,
    }
    obj = PlantCreate(**input_data)
    assert obj


@pytest.mark.parametrize(
    "name, user_id, acquire_time, is_alive, species, watering_frequency, last_watering",
    [
        # empty name
        ("", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", 7, "2023-04-10T12:00:29.275Z"),
        # invalid species
        ("", 1, "2023-04-12T18:11:29.275Z", 1, "", 7, "2023-04-10T12:00:29.275Z"),
        ("", 1, "2023-04-12T18:11:29.275Z", 1, "a", 7, "2023-04-10T12:00:29.275Z"),
        # empty user_id
        ("test plant name", "", "2023-04-12T18:11:29.275Z", 1, "plant species", 7, "2023-04-10T12:00:29.275Z"),
        # invalid is_alive
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", "invalid", "plant species", 7, "2023-04-10T12:00:29.275Z"),
        # is_alive wrong integer
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 6, "plant species", 7, "2023-04-10T12:00:29.275Z"),
        # invalid acquire_time
        ("test plant name", 1, "invalid", 1, "plant species", 7, "2023-04-10T12:00:29.275Z"),
        # invalid watering_frequency
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", "", "2023-04-10T12:00:29.275Z"),
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", 370, "2023-04-10T12:00:29.275Z"),
        # invalid last_watering
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", 7, "invalid"),
        # incorrect datetime format
        ("test plant name", 1, "2023/04/12T18:11:29.275Z", 1, "plant species", 7, "2023-04-10T12:00:29.275Z"),
        ("test plant name", 1, "string_instead_of_datetime", 1, "plant species", 7, "2023-04-10T12:00:29.275Z"),
    ],
)
def test_plant_create_schema_incorrect_data(name, user_id, acquire_time, is_alive, species, watering_frequency, last_watering):
    input_data = {
        "name": name,
        "user_id": user_id,
        "acquire_time": acquire_time,
        "is_alive": is_alive,
        "species": species,
        "watering_frequency": watering_frequency,
        "last_watering": last_watering,
    }

    with pytest.raises(ValidationError):
        obj = PlantCreate(**input_data)
