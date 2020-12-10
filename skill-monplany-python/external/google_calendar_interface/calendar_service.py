import json
import pickle
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build, Resource
from oauth2client import client
import httplib2
import os
from datetime import datetime, timedelta

class CalendarService:

    GOOGLE_CLIENT_ID: str = None
    GOOGLE_CLIENT_SECRET: str = None
    GOOGLE_CALENDAR_SCOPE: str = 'https://www.googleapis.com/auth/calendar'

    def __init__(self, client_secret_file):
        self._set_parameter(client_secret_file)

    def _set_parameter(self, client_secret_file):
        """
        Set the Google credentials API parameters
        :param client_secret_file: file from google developer console
        :return: None
        """
        data = json.load(open(client_secret_file))['web']
        CalendarService.GOOGLE_CLIENT_ID = data['client_id']
        CalendarService.GOOGLE_CLIENT_SECRET = data['client_secret']

    def get_credentials(self, auth_code: str) -> Credentials:
        """
        Save the credentials for the next run of the API calls
        :param auth_code: authorization code received from frontend after login
        :return: saved credentials: google.oauth2.credentials
        """
        credentials: Credentials = None
        # if os.path.exists('./credentials/token.pickle'):
        #     with open('./credentials/token.pickle', 'rb') as token:
        #         credentials = pickle.load(token)
        # else:
        credentials = client.credentials_from_code(
            client_id=CalendarService.GOOGLE_CLIENT_ID,
            client_secret=CalendarService.GOOGLE_CLIENT_SECRET,
            scope=CalendarService.GOOGLE_CALENDAR_SCOPE,
            code=auth_code
        )
        #TODO : replace with database here
        # with open('./credentials/token.pickle', 'wb') as token:
        #     pickle.dump(credentials, token)
        #     print("Saved Credentials")

        return credentials

    # def get_crendentials(self) -> Credentials:
    #     """
    #     Get the credentials of the user to access the calendar
    #     either from saved one or from google server
    #     :return: credentials: google.oauth2.credentials
    #     """
    #     credentials: Credentials = None
    #     # TODO : get data from database
    #     if os.path.exists('./credentials/token.pickle'):
    #         with open('./credentials/token.pickle', 'rb') as token:
    #             credentials = pickle.load(token)
    #     if not credentials:
    #         if credentials and credentials.expired and credentials.refresh_token:
    #             credentials.refresh(Request())
    #
    #         # else:
    #         #     if not auth_code:
    #         #         credentials = self.save_credentials(auth_code)
    #     return credentials

    def init_calendar_service(self, credentials: Credentials) -> Resource:
        """
        initializes the calendar service to run the calendar API
        :param credentials: credentials of the user
        :return: calendar service
        """
        http_auth = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http_auth)
        return service

    def get_available_slots(self, preferred_hours, appointments, duration=timedelta(hours=1)) -> []:
        """
        To get avaialable slots from the calendar
        :param preferred_hours: Hours for the user to select the event from
        :param appointments: already fixed appointments
        :param duration: how long the event is
        :return: array of free slots
        """
        free_slots = []
        slots = sorted([(preferred_hours[0], preferred_hours[0])] + appointments + [(preferred_hours[1], preferred_hours[1])])
        for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
            assert start <= end, "Cannot find free appointments"
            while start + duration <= end:
                free_slots.append({
                    'start': start,
                    'end': start+duration
                })
                start += duration
        return free_slots
