from flask import Flask, request
from flask_cors import CORS
from external.google_calendar_interface.calendar_service import CalendarService
import json
from external.database.user_database import UserDatabase
from external.monplany_manager import MonplanyManager

server: Flask = Flask(__name__)
CORS(server, resources={r"/monplany/*": {"origins": "http://localhost:4200"}})
monplany_manager = MonplanyManager(credentials_dir='./credentials/')
calendar_service = monplany_manager.google_calendar_service
user_database = monplany_manager.user_database


@server.route('/monplany/calendar/creds/save', methods=['POST'])
def save_credentials():
    """
    HTTP request to save the credentials to be used for Google Calendar API
    :return: None
    """
    auth_code = request.json['authorizationCode']
    sync_code = request.json['synchronizaionCode']
    credentials = calendar_service.save_credentials(auth_code=auth_code)
    id_token = credentials.id_token
    user_database.insert_user_info(email=id_token['email'],
                                   first_name=id_token['given_name'],
                                   last_name=id_token['family_name'],
                                   events=[],
                                   sync_code=int(sync_code))

    return id_token


@server.route('/monplany/calendar/events', methods=['GET'])
def get_events():
    # retrieve the email from the request
    user_database.print_collection(user_database.user_collection)
    email = request.args.get('email')
    # get google calendar data
    google_calendar_events = calendar_service.get_google_calendar_events(email=email)
    for e in google_calendar_events:
        user_database.update_calendar_events_by_email(email, e)
    # get monplany calendar data
    all_calendar_events = user_database.get_calendar_events_by_email(email=email)
    return json.dumps(all_calendar_events)

@server.route('/monplany/calendar/events/reset', methods=['GET'])
def reset_events():
    email = request.args.get('email')
    user_database.reset_calendar_events(email=email)
    return "Done"


# @server.route('/monplany/chatbot', methods=['GET'])
# def chatbot():
#     return skill_http_request.call_request(skill_http_request.create_request(intent='TEAM__21__HOBBIES'))

if __name__ == '__main__':
    server.run(debug=True)
