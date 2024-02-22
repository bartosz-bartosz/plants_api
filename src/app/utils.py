from datetime import datetime, timedelta


def needs_watering(last_watering: datetime | None, watering_frequency: int):
    """Check if a plant needs watering based on last watering and watering frequency"""
    if not last_watering:
        return True
    return last_watering + timedelta(days=watering_frequency) < datetime.now()
