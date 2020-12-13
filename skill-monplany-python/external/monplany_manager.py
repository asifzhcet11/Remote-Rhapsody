from external.activity_interface.activity import Activity, ActivityType, Day, DayTime
from external.database.user_database import UserDatabase
from external.google_calendar_interface.calendar_service import CalendarService
from datetime import datetime, timedelta
from external.notification.notification_service import NotificationService, NotificationMsg
from dateutil.parser import parse, isoparse


class MonplanyManager:

    def __init__(self, credentials_dir: str):
        self.available_activities = self._default_activities()
        self.user_database = UserDatabase()
        self.google_calendar_service = CalendarService(credentials_dir)
        self.notification_services = dict()

    def _default_activities(self):
        return {
            ActivityType.GYM: Activity(activity_type=ActivityType.GYM,
                                       preferred_duration=120,
                                       preferred_days=[Day.TUESDAY, Day.THURSDAY, Day.SATURDAY],
                                       preferred_day_times=[DayTime.EVENING, DayTime.EVENING, DayTime.EVENING],
                                       preferred_occurence=1,
                                       background_color='#829356'
                                       ),

            ActivityType.EINKAUFEN: Activity(activity_type=ActivityType.EINKAUFEN,
                                             preferred_duration=90,
                                             preferred_days=[Day.WEDNESDAY, Day.SATURDAY],
                                             preferred_day_times=[DayTime.EVENING, DayTime.EVENING],
                                             preferred_occurence=1,
                                             background_color='#BCA136'),

            ActivityType.GESUNDHEIT: Activity(activity_type=ActivityType.GESUNDHEIT,
                                              preferred_duration=30,
                                              preferred_days=[Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY,
                                                              Day.FRIDAY, Day.SATURDAY, Day.SONTAG],
                                              preferred_day_times=[DayTime.MORNING, DayTime.MORNING, DayTime.MORNING,
                                                                   DayTime.AFTERNOON, DayTime.AFTERNOON,
                                                                   DayTime.EVENING, DayTime.EVENING],
                                              preferred_occurence=2,
                                              background_color='#9A2617')
        }

    def create_activity(self, activity_type: ActivityType,
                        duration: int = 0,
                        default: bool = True) -> Activity:

        if (default):
            activity = self.available_activities[activity_type]
        else:
            activity = self.available_activities[activity_type]
            if not duration == 0:
                activity.preferred_duration = duration
        return activity

    def get_available_slots(self, preferred_hours, appointments, duration=timedelta(hours=1)) -> []:
        """
        To get avaialable slots from the calendar
        :param preferred_hours: Hours for the user to select the event from
        :param appointments: already fixed appointments
        :param duration: how long the event is
        :return: array of free slots
        """
        free_slots = []
        slots = sorted(
            [(preferred_hours[0], preferred_hours[0])] + appointments + [(preferred_hours[1], preferred_hours[1])])
        for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
            if not start <= end:
                break
            while start + duration <= end:
                free_slots.append({
                    'start': start,
                    'end': start + duration
                })
                start += duration
        return free_slots

    def add_activity_to_calendar(self, activity: Activity, magenta_id: str):
        print(magenta_id)
        email = self.user_database.get_email_from_id(magenta_id=magenta_id)
        appointments = list()

        # get all the appointments for the week of google calendar
        google_calendar_events = self.google_calendar_service.get_google_calendar_events(email=email)
        for google_appointment in google_calendar_events:
            google_appointment_pair = self.generate_appointment_from_string(start=google_appointment['start'],
                                                                            end=google_appointment['end'])
            appointments.append(google_appointment_pair)

        # get all the appointments of monplany
        monplany_events = self.user_database.get_calendar_events_by_magenta_id(magenta_id=magenta_id)
        for monplany_appointment in monplany_events:
            monplany_appointment_pair = self.generate_appointment_from_string(start=monplany_appointment['start'],
                                                                              end=monplany_appointment['end'])
            appointments.append(monplany_appointment_pair)

        # Get today's day
        today = datetime.today()
        # Go to start week's day
        start = today - timedelta(days=today.weekday())
        for i in range(len(activity.preferred_days)):
            preferred_day = activity.preferred_days[i].value
            preferred_day_time = activity.preferred_day_times[i].value
            activity_date = start + timedelta(days=preferred_day)
            start_date_time = datetime(activity_date.year, activity_date.month, activity_date.day,
                                       hour=preferred_day_time)
            end_date_time = datetime(activity_date.year, activity_date.month, activity_date.day,
                                     hour=(preferred_day_time + 4))

            # first check if appointment already available
            if not self.if_activity_already_planned(activity, monplany_events=monplany_events,
                                                    datetime=start_date_time):
                filtered_appointments = self.filter_appointments_by_date(appointments, start_date_time)
                available_slots = self.get_available_slots((start_date_time, end_date_time), filtered_appointments,
                                                           timedelta(minutes=activity.preferred_duration))
                print(available_slots)
                if (len(available_slots) >= activity.preferred_occurence):
                    for occurence in range(activity.preferred_occurence):
                        available_slot = available_slots[occurence]
                        self.user_database.update_calendar_events_by_magenta_id(magenta_id, {
                            'title': activity.activity_type.value,
                            'start': available_slot['start'].astimezone().isoformat(),
                            'end': available_slot['end'].astimezone().isoformat(),
                            'editable': False,
                            'backgroundColor': activity.background_color
                        })
                else:
                    print("No free slots available for Activity with type {} on {} at preferred time".format(
                        activity.activity_type.value,
                        start_date_time.date()))

            else:
                print("Activity with type {} is already planned on {}".format(activity.activity_type.value,
                                                                              start_date_time.date()))

    def filter_appointments_by_date(self, appointments: [(datetime, datetime)], datetime: datetime) -> [
        (datetime, datetime)]:
        filtered_appointments = []
        for appointment in appointments:
            if appointment[0].date() == datetime.date():
                filtered_appointments.append(appointment)
        return filtered_appointments

    def if_activity_already_planned(self, activity: Activity, monplany_events: [{}], datetime: datetime) -> bool:
        threshold = activity.preferred_occurence
        occurence = 0
        for event in monplany_events:
            start = datetime.fromisoformat(event['start'])
            if start.date() == datetime.date() and event['title'] == activity.activity_type.value:
                occurence += 1
                if occurence == threshold:
                    return True
        return False

    def generate_appointment_from_string(self, start: str, end: str) -> ():
        start_datetime_obj = datetime.fromisoformat(start)
        end_datetime_obj = datetime.fromisoformat(end)
        appointment_pair = (datetime(start_datetime_obj.year,
                                     start_datetime_obj.month,
                                     start_datetime_obj.day,
                                     hour=start_datetime_obj.hour,
                                     minute=start_datetime_obj.minute),
                            datetime(end_datetime_obj.year,
                                     end_datetime_obj.month,
                                     end_datetime_obj.day,
                                     hour=end_datetime_obj.hour,
                                     minute=end_datetime_obj.minute))
        return appointment_pair

    def create_notification_service(self, magenta_id: str):
        notification_service = NotificationService(id=magenta_id)
        self.notification_services[magenta_id] = notification_service

    def update_next_notification(self, magenta_id: str):
        events = self.user_database.get_calendar_events_by_magenta_id(magenta_id=magenta_id)
        dict_events = {}
        now = datetime.now()
        datetime_now = datetime(now.year, now.month, now.day, now.hour, now.minute)
        for i in range(len(events)):
            e = events[i]
            event_date = datetime.fromisoformat(e['start'])
            event_datetime = datetime(event_date.year,
                                      event_date.month,
                                      event_date.day,
                                      event_date.hour,
                                      event_date.minute)

            diff = (event_datetime - datetime_now).total_seconds()
            if diff > 0:
                print(i, diff)
                dict_events[i] = diff

        sort_dict=dict(sorted(dict_events.items(), key=lambda item: item[1]))
        key_first = list(sort_dict.keys())[0]
        # self.notification_services[magenta_id].setup_notification(time=sort_dict[key_first],
        #                                                           msg=events[0]['title'])
        notification_service: NotificationService = self.notification_services[magenta_id]
        notification_msg = NotificationMsg(phone_no="+4915175834426", body=events[0]['title'])
        notification_service.setup_notification(time=10,
                                                msg=notification_msg)