from datetime import datetime
from app.routers.watering.models import Watering


def test_model_correct():
    # correct model
    assert Watering(
        id=1,
        plant_id=2,
        timestamp=datetime(2023, 4, 12, 18, 11, 29, 275000),
        fertilizer=True,
        user_id=3
    )


def test_model_wrong():
    assert Watering(
        id='string',
        plant_id=2,
        timestamp=datetime(2023, 4, 12, 18, 11, 29, 275000),
        fertilizer=True,
        user_id=3
    )
