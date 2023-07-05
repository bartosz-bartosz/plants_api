import pytest

from datetime import datetime
from app.routers.plant.models import Plant


def test_name():
    # Correct model
    assert Plant(user_id=1,
                 name='plant name',
                 acquire_time=datetime.now,
                 is_alive=1,
                 species='plant species',
                 watering_frequency=7)

    # Wrong models
    with pytest.raises(ValueError):
        # name empty
        name_fail = Plant(user_id=1,
                          name='',
                          acquire_time=datetime.now,
                          is_alive=1,
                          species='plant species',
                          watering_frequency=7)

    with pytest.raises(ValueError):
        # name too short
        name_fail = Plant(user_id=1,
                          name='a',
                          acquire_time=datetime.now,
                          is_alive=1,
                          species='plant species',
                          watering_frequency=7)

    with pytest.raises(ValueError):
        # name too long
        name_fail = Plant(user_id=1,
                          name=''.join(["i" for _ in range(201)]),
                          acquire_time=datetime.now,
                          is_alive=1,
                          species='plant species',
                          watering_frequency=7)
