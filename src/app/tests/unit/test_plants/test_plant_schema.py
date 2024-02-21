import pytest
from pydantic import ValidationError

from app.routers.plant.schemas import PlantCreate


valid_plant_create_data = {
    "name": "test plant name",
    "acquire_time": "2023-04-12T18:11:29.275Z",
    "is_alive": 1,
    "species": "plant species",
    "watering_frequency": 7,
}


def test_valid_plant_create_schema():
    assert PlantCreate(**valid_plant_create_data)


@pytest.mark.parametrize(
    "name, acquire_time, is_alive, species, watering_frequency",
    [
        # empty name
        ("", "2023-04-12T18:11:29.275Z", 1, "plant species", 7),
        # invalid species
        ("", "2023-04-12T18:11:29.275Z", 1, "", 7),
        ("", "2023-04-12T18:11:29.275Z", 1, "a", 7),
        # invalid is_alive
        (
            "test plant name",
            "2023-04-12T18:11:29.275Z",
            "invalid",
            "plant species",
            7,
        ),
        # is_alive wrong integer
        ("test plant name", "2023-04-12T18:11:29.275Z", 6, "plant species", 7),
        # invalid acquire_time
        ("test plant name", "invalid", 1, "plant species", 7),
        # invalid watering_frequency
        ("test plant name", "2023-04-12T18:11:29.275Z", 1, "plant species", ""),
        ("test plant name", "2023-04-12T18:11:29.275Z", 1, "plant species", 370),
        # incorrect datetime format
        ("test plant name", "2023/04/12T18:11:29.275Z", 1, "plant species", 7),
        ("test plant name", "string_instead_of_datetime", 1, "plant species", 7),
    ],
)
def test_plant_create_schema_incorrect_data(
    name, acquire_time, is_alive, species, watering_frequency
):
    input_data = {
        "name": name,
        "acquire_time": acquire_time,
        "is_alive": is_alive,
        "species": species,
        "watering_frequency": watering_frequency,
    }

    with pytest.raises(ValidationError):
        PlantCreate(**input_data)
