from skill_sdk import skill, Response, tell, ask
from skill_sdk.l10n import _
from typing import List
from external.database_api import UserDatabase
from external.activity_api.activity import Activity, ActivityType, ActivityManager
from external.monplany_manager import MonplanyManager
import re

monplany_manager = MonplanyManager(credentials_dir='./external/credentials/')
user_database = monplany_manager.user_database

available_events = ["einkaufen", "fitness", "gym", "wasser", "hobby", "kaufe", "sport"]
event_map_activity = {
    "einkaufen": {
        "type": ActivityType.EINKAUFEN,
        "response": _("MONPLANY_SHOP_EVENT")
    },
    "kaufe": {
       "type": ActivityType.EINKAUFEN,
       "response": "MONPLANY_SHOP_EVENT"
    },
    "fitness": {
        "type": ActivityType.GYM,
        "response": "MONPLANY_GYM_EVENT"
    },
    "gym": {
        "type": ActivityType.GYM,
        "response": "MONPLANY_GYM_EVENT"
    },
    "spoert": {
        "type": ActivityType.GYM,
        "response": "MONPLANY_GYM_EVENT"
    },
    "hobby": {
        "type":ActivityType.HOBBIES,
         "response": "MONPLANY_ASK_HOBBIES"
    },
    "wasser":{
        "type": ActivityType.GESUNDHEIT,
        "response": "MONPLANY_WATER_EVENT"
    }
}

def generate_code_response(user_id):
    code = user_database.insert_sync_info(user_id)
    code_text = str(code)
    user_code = ""
    for i in code_text:
        user_code += i + '.'
    response = tell(_('MONPLANY_ASK_LOGIN', code=user_code))
    return response

@skill.intent_handler('TEAM_21_CREATE_EVENT')
def ask_login(user_id:str, phone:str) -> Response:
    if not user_database.is_user_synced(user_id):
        response = generate_code_response(user_id)
    else:
        response = ask(_('MONPLANY_EVENT_TYPE', first_name=user_database.get_user_first_name(user_id)))
    return response

@skill.intent_handler('TEAM_21_CREATE_AUTOMATIC_EVENT')
def automatic_event(user_id:str) -> Response:

    if user_database.is_user_synced(user_id):
        for activity_type, activity in monplany_manager.available_activities.items():
            monplany_manager.add_activity_to_calendar(activity, user_id)
        msg = _('MONPLANY_AUTOMATIC_EVENT', first_name=user_database.get_user_first_name(user_id)) + _('MONPLANY_FINAl_MSG')
    else:
        msg = generate_code_response(user_id)
    return tell(msg)


@skill.intent_handler('TEAM_21_ASK_HOBBIES')
def ask_hobbies(user_id:str) -> Response:
    if user_database.is_user_synced(user_id):
        response = ask(_('MONPLANY_ASK_HOBBIES', first_name=user_database.get_user_first_name(user_id)))
    else:
        response = generate_code_response(user_id)
    return response

@skill.intent_handler('TEAM_21_TELL_HOBBIES')
def plan_hobbies(user_id:str, hobbies: str) -> Response:
    print(hobbies)
    if user_database.is_user_synced(user_id):
        hobbies = re.sub(r'[,.]|und', '', hobbies)
        hobbies = hobbies.split()
        print(hobbies)
        try:
            assert len(hobbies) > 0
            msg = _('MONPLANY_TELL_HOBBIES ', first_name=user_database.get_user_first_name(user_id), hobbies=len(hobbies))
            msg += ':'
            for id, str in enumerate(hobbies):
                if id == 0:
                    msg = msg + ' ' + str
                elif id == len(hobbies)-1:
                    msg = msg + ' und ' + str
                else:
                    msg = msg + ', ' + str
            msg+= '.'
            print(msg)
            response = tell(msg + _("MONPLANY_FINAl_MSG"))
            # send_event("Hobby",hobbies)
        except(AssertionError, ValueError, TypeError):
            response = tell(_('MONPLANY_EMPTY_HOBBIES'))
    else:
        response = generate_code_response(user_id)

    return response

@skill.intent_handler('TEAM_21_OTHER_EVENTS')
def plan_event(user_id:str, activity: str) -> Response:
    print(activity)
    if user_database.is_user_synced(user_id):
    # if True:
        lowercase = activity.lower()
        if lowercase in available_events:
            type = event_map_activity[lowercase]["type"]
            user_activity = monplany_manager.create_activity(type)
            monplany_manager.add_activity_to_calendar(user_activity, user_id)
            response = tell(_(event_map_activity[lowercase]["response"]))
            
        else:
            response = ask("MONPLANY_ACTIVITY_NOT_FOUND")
    else:
        response = generate_code_response(user_id)
    return response

@skill.intent_handler('TEAM_21_GYM')
def gym_event(user_id:str, hours:int, minutes:int) -> Response:

    print(hours, ' hours + ', minutes, " minutes.")
    try:
        if user_database.is_user_synced(user_id):
            assert hours > 0 or minutes > 0
            assert hours >= 0 and minutes > 0
            # if send_event("gym", gym_stunden, gym_minutes):
            response = tell(_("MONPLANY_GYM_OK", first_name=user_database.get_user_first_name(user_id)) + _("MONPLANY_FINAl_MSG"))
            # else:
            #   response = tell(_("MONPLANY_GYM_IMPOSSIBLE"))
        else:
            response = generate_code_response(user_id)
    except(AssertionError):
        response = tell("MONPLANY_WRONG_TIME")
    return response
