from enum import Enum


class ActivityType(Enum):
    HOBBIES = "HOBBIES"
    GYM = "GYM"
    EINKAUFEN = "EINKAUFEN"
    GESUNDHEIT = "GESUNDHEIT"

class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SONTAG = 6

class DayTime(Enum):
    MORNING = 8
    AFTERNOON = 12
    EVENING = 16
    NIGHT = 20


class Activity:

    def __init__(self,
                 activity_type: ActivityType,
                 preferred_duration: float,
                 preferred_days: [Day],
                 preferred_day_times: [DayTime],
                 preferred_occurence: int,
                 background_color: str = "#4285F4"):

        self.activity_type = activity_type
        self.preferred_duration = preferred_duration
        self.preferred_days = preferred_days
        self.preferred_day_times = preferred_day_times
        self.preferred_occurence = preferred_occurence
        self.background_color = background_color







