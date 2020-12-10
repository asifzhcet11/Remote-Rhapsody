from enum import Enum

class ActivityType(Enum):
    HOBBIES = "HOBBIES"
    GYM = "GYM"
    EINKAUFEN = "EINKAUFEN"
    GESUNDHEIT = "GESUNDHEIT"

class Day(Enum):
    SONTAG = "SONTAG"
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    ALL = [SONTAG, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY]

class DayTime(Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"
    NIGHT = "NIGHT"
    ALL = [MORNING, AFTERNOON, EVENING, NIGHT]


class Activity:

    def __init__(self,
                 activity_type: ActivityType,
                 preferred_duration: float,
                 preferred_days: [Day],
                 preferred_day_times: [DayTime],
                 preferred_occurence: int):

        self.activity_type = activity_type
        self.preferred_duration = preferred_duration
        self.preferred_days = preferred_days
        self.preferred_day_times = preferred_day_times
        self.preferred_occurence = preferred_occurence

class ActivityManager:

    def __init__(self):
        self.available_activities = self._default_activities()

    def _default_activities(self):
        return {
                ActivityType.GYM: Activity(activity_type=ActivityType.GYM,
                                           preferred_duration=120,
                                           preferred_days=[Day.TUESDAY, Day.THURSDAY, Day.SATURDAY],
                                           preferred_day_times=[DayTime.EVENING],
                                           preferred_occurence=1),

                ActivityType.EINKAUFEN: Activity(activity_type=ActivityType.EINKAUFEN,
                                                 preferred_duration=45,
                                                 preferred_days=[Day.WEDNESDAY, Day.SATURDAY],
                                                 preferred_day_times=[DayTime.MORNING, DayTime.EVENING],
                                                 preferred_occurence=1),

                ActivityType.GESUNDHEIT: Activity(activity_type=ActivityType.GESUNDHEIT,
                                                  preferred_duration=5,
                                                  preferred_days=[Day.ALL],
                                                  preferred_day_times=[DayTime.ALL],
                                                  preferred_occurence=13)
                }

    def create_activity(self, activity_type: ActivityType,
                        duration: int = 0,
                        default: bool = True):

        activity: Activity = None
        if (default):
            activity = self.available_activities[activity_type]
        else:
            activity = self.available_activities[activity_type]
            if not duration==0:
                activity.preferred_duration = duration

        # TODO add to mongodb
        # TODO add to calendar




