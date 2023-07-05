import pytest
from pydantic import ValidationError

from app.routers.plant.schemas import PlantCreate


@pytest.mark.parametrize(
    "name, user_id, acquire_time, is_alive, species, watering_frequency",
    [
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", 7),
        ("another plant name", 2, "2023-04-11T10:23:29.275Z", 0, "cactus species", 14),
        ("third plant name", 3, "2023-04-09T16:45:29.275Z", True, "fern species", 3),
        ("third plant name", 3, "2023-04-09T16:45:29.275Z", False, "fern species", 3),
    ],
)
def test_plant_create_schema_correct_data(name, user_id, acquire_time, is_alive, species, watering_frequency):
    input_data = {
        "name": name,
        "user_id": user_id,
        "acquire_time": acquire_time,
        "is_alive": is_alive,
        "species": species,
        "watering_frequency": watering_frequency,
    }
    obj = PlantCreate(**input_data)
    assert obj


@pytest.mark.parametrize(
    "name, user_id, acquire_time, is_alive, species, watering_frequency",
    [
        # empty name
        ("", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", 7),
        # invalid species
        ("", 1, "2023-04-12T18:11:29.275Z", 1, "", 7),
        ("", 1, "2023-04-12T18:11:29.275Z", 1, "a", 7),
        # empty user_id
        ("test plant name", "", "2023-04-12T18:11:29.275Z", 1, "plant species", 7),
        # invalid is_alive
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", "invalid", "plant species", 7),
        # is_alive wrong integer
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 6, "plant species", 7),
        # invalid acquire_time
        ("test plant name", 1, "invalid", 1, "plant species", 7),
        # invalid watering_frequency
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", ""),
        ("test plant name", 1, "2023-04-12T18:11:29.275Z", 1, "plant species", 370),
        # incorrect datetime format
        ("test plant name", 1, "2023/04/12T18:11:29.275Z", 1, "plant species", 7),
        ("test plant name", 1, "string_instead_of_datetime", 1, "plant species", 7),
    ],
)
def test_plant_create_schema_incorrect_data(name, user_id, acquire_time, is_alive, species, watering_frequency):
    input_data = {
        "name": name,
        "user_id": user_id,
        "acquire_time": acquire_time,
        "is_alive": is_alive,
        "species": species,
        "watering_frequency": watering_frequency,
    }

    with pytest.raises(ValidationError):
        obj = PlantCreate(**input_data)
