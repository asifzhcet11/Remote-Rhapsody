import json
import pickle
from google.oauth2.credentials import Credentials
from google_auth_httplib2 import Request
from googleapiclient.discovery import build, Resource
from oauth2client import client
import httplib2
import os
from datetime import datetime, timedelta


class CalendarService:
    GOOGLE_CLIENT_ID: str = None
    GOOGLE_CLIENT_SECRET: str = None
    GOOGLE_CALENDAR_SCOPE: str = 'https://www.googleapis.com/auth/calendar'


    def __init__(self, credentials_dir: str, client_secret_file='client_secret.json'):
        self.credentials_dir = credentials_dir
        self._set_parameter(credentials_dir + client_secret_file)

    def _set_parameter(self, client_secret_file):
        """
        Set the Google credentials API parameters
        :param client_secret_file: file from google developer console
        :return: None
        """
        data = json.load(open(client_secret_file))['web']
        CalendarService.GOOGLE_CLIENT_ID = data['client_id']
        CalendarService.GOOGLE_CLIENT_SECRET = data['client_secret']

    def save_credentials(self, auth_code: str) -> Credentials:
        """
        Save the credentials for the next run of the API calls
        :param auth_code: authorization code received from frontend after login
        :return: saved credentials: google.oauth2.credentials
        """
        credentials: Credentials = None

        credentials = client.credentials_from_code(
            client_id=CalendarService.GOOGLE_CLIENT_ID,
            client_secret=CalendarService.GOOGLE_CLIENT_SECRET,
            scope=CalendarService.GOOGLE_CALENDAR_SCOPE,
            code=auth_code
        )
        email = credentials.id_token['email']
        credentials_file = self.credentials_dir + email + '_credentials.pickle'
        if os.path.exists(credentials_file):
            with open(credentials_file, 'rb') as token:
                credentials = pickle.load(token)
        else:
            with open(credentials_file, 'wb') as token:
                pickle.dump(credentials, token)
                print("Saved Credentials for {}".format(email))

        return credentials

    def get_crendentials(self, email: str) -> Credentials:
        """
        Get the credentials of the user to access the calendar
        either from saved one or from google server
        :return: credentials: google.oauth2.credentials
        """
        credentials: Credentials = None
        credentials_file = self.credentials_dir + email + '_credentials.pickle'
        if os.path.exists(credentials_file):
            with open(credentials_file, 'rb') as token:
                credentials = pickle.load(token)
        if not credentials:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
        return credentials

    def init_calendar_service(self, credentials: Credentials) -> Resource:
        """
        initializes the calendar service to run the calendar API
        :param credentials: credentials of the user
        :return: calendar service
        """
        http_auth = credentials.authorize(httplib2.Http())
        service = build('calendar', 'v3', http_auth)
        return service

    def get_google_calendar_events(self, email: str) -> []:
        credentials = self.get_crendentials(email)
        service = self.init_calendar_service(credentials)
        # Get today's time
        today = datetime.today()
        # start week's day
        start = today - timedelta(days=today.weekday())
        # end week's day
        end = start + timedelta(days=7)
        # Gey tomorrow time
        # tomorrow = today + timedelta(1)
        # extract timeMin and timeMax
        timeMin = datetime(start.year, start.month, start.day)
        timeMin = timeMin.isoformat() + 'Z'
        timeMax = datetime(end.year, end.month, end.day)
        timeMax = timeMax.isoformat() + 'Z'
        # Getting the events from Calendar API
        results = service.events().list(calendarId='primary', timeMin=timeMin,
                                        timeMax=timeMax).execute()
        events = results.get('items', [])
        calendar_events = []
        for e in events:
            data = {
                'title': e['summary'],
                'start': e['start']['dateTime'],
                'end': e['end']['dateTime'],
                'editable': False,
                'backgroundColor': '#4285F4'
            }
            calendar_events.append(data)
        del service
        return calendar_events
        #return events

