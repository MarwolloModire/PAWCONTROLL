from pydantic import BaseModel, Field
from datetime import datetime, time


class WalkOrderCreate(BaseModel):
    # Сначала сделал так (потому-что не думал заниматься визуальной частью приложения).
    # Но в итоге сделал более менее интуитивно понятный интерфейс. Быстро оформив его буквально на коленке.
    apartment_number: str = Field(..., min_length=1, max_length=10, example="12B",
                                  description="Apartment number must be between 1 and 10 characters.")
    pet_name: str = Field(..., min_length=1, max_length=50, example="Buddy",
                          description="Pet name must be between 1 and 50 characters.")
    pet_breed: str = Field(..., min_length=1, max_length=50, example="Labrador",
                           description="Pet breed must be between 1 and 50 characters.")
    walk_date: datetime = Field(..., example="2024-08-28",
                                description="Date of the walk in YYYY-MM-DD format.")
    walk_time: time = Field(..., example="10:00",
                            description="Time of the walk (HH:MM format, must be on the hour or half-hour).")

    def __init__(self, **data):
        super().__init__(**data)
        self._validate_walk_time()
        self._validate_walk_date_and_time()

    def _validate_walk_time(self):
        allowed_times = [time(hour, minute)
                         for hour in range(7, 24) for minute in [0, 30]]
        if self.walk_time not in allowed_times:
            raise ValueError(
                "Walk time must be on the hour or half-hour between 7:00 and 23:00.")

    def _validate_walk_date_and_time(self):
        if not (time(7, 0) <= self.walk_time <= time(23, 0)):
            raise ValueError("Walk time must be between 7:00 AM and 11:00 PM.")
