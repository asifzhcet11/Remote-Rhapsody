from flask import Flask, request
from flask_cors import CORS
from external.google_calendar_interface.calendar_service import CalendarService
from datetime import datetime, timedelta
import json
from external.skill_state_machine.skill_http_request import SkillHTTPRequest
from external.database_api import UserDatabase

server: Flask = Flask(__name__)
CORS(server, resources={r"/monplany/*": {"origins": "http://localhost:4200"}})
calendar_service = CalendarService(client_secret_file='./credentials/client_secret.json')
skill_http_request = SkillHTTPRequest()
user_database = UserDatabase()


@server.route('/monplany/calendar/creds/save', methods=['POST'])
def save_credentials():
    """
    HTTP request to save the credentials to be used for Google Calendar API
    :return: None
    """
    auth_code = request.json['authorizationCode']
    sync_code = request.json['synchronizaionCode']
    credentials = calendar_service.get_credentials(auth_code=auth_code)
    id_token = credentials.id_token
    user_database.insert_user_info(email=id_token['email'],
                                   first_name=id_token['given_name'],
                                   last_name=id_token['family_name'],
                                   events=[],
                                   google_auth_code=auth_code,
                                   sync_code=int(sync_code))
    user_database.print_collection(user_database.user_collection)
    return id_token


@server.route('/monplany/calendar/events', methods=['GET'])
def get_events():
    # retrieve auth code from mongodb
    service = calendar_service.init_calendar_service(calendar_service.get_crendentials())
    # Get today's time
    today = datetime.today()
    # Gey tomorrow time
    tomorrow = today + timedelta(1)
    # extract timeMin and timeMax
    timeMin = datetime(today.year, today.month, today.day)
    timeMin = timeMin.isoformat() + 'Z'
    timeMax = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    timeMax = timeMax.isoformat() + 'Z'
    # Getting the events from Calendar API
    results = service.events().list(calendarId='primary', timeMin=timeMin,
                                    timeMax=timeMax).execute()
    events = results.get('items', [])

    data = []
    for e in events:
        event = {
            'title': e['summary'],
            # 'htmlLink': e['htmlLink'],
            'start': e['start']['dateTime'],
            'end': e['end']['dateTime'],
            'editable': False,
            'backgroundColor': '#047bf8'
        }
        data.append(event)

    return json.dumps(data)

@server.route('/monplany/chatbot', methods=['GET'])
def chatbot():
    return skill_http_request.call_request(skill_http_request.create_request(intent='TEAM__21__HOBBIES'))

if __name__ == '__main__':
    server.run(debug=True)
