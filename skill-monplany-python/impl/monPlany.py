from skill_sdk import skill, Response, tell, ask
from skill_sdk.l10n import _
from typing import List
from external.database_api import UserDatabase
from external.activity_api.activity import Activity, ActivityType, ActivityManager
import re

activity_manager = ActivityManager()
user_database = UserDatabase()
available_events = ["einkaufen", "fitness", "gym", "wasser", "hobby", "kaufe", "sport"]
event_map_activity = {
    "einkaufen": {
        "type": ActivityType.EINKAUFEN,
        "response": _("MONPLANY_SHOP_EVENT") + _("MONPLANY_FINAl_MSG")
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
        response = tell(_('MONPLANY_EVENT_TYPE'))
    return response

@skill.intent_handler('TEAM_21_CREATE_AUTOMATIC_EVENT')
def automatic_event(user_id:str) -> Response:

    if user_database.is_user_synced(user_id):
        # if user_database.
    #     if plan_today():
        msg = _('MONPLANY_AUTOMATIC_EVENT') + _('MONPLANY_FINAl_MSG')
    #     else:
    #       msg = _('MONPLANY_NO_PLAN_TODAY')
    else:
        msg = generate_code_response(user_id)
    return tell(msg)
    pass


@skill.intent_handler('TEAM_21_ASK_HOBBIES')
def ask_hobbies(user_id:str) -> Response:
    if user_database.is_user_synced(user_id):
        response = tell(_('MONPLANY_ASK_HOBBIES'))
    else:
        response = generate_code_response(user_id)
    return response

@skill.intent_handler('TEAM_21_TELL_HOBBIES')
def plan_hobbies(user_id:str, hobbies: str) -> Response:
    print(hobbies)
    if user_database.is_user_synced(user_id):
        hobbies = re.sub(r'[,|.|und]', '', hobbies)
        hobbies = hobbies.split()
        print(hobbies)
        try:
            assert len(hobbies) > 0
            msg = _('MONPLANY_TELL_HOBBIES', hobbies=len(hobbies))
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
            response = tell(_(event_map_activity[lowercase]["response"]))
            user_activity = activity_manager.create_activity(type)
            # if event.lower() == "einkaufen":
            #     response = tell()
            #     user_database.update_calendar_events_by_magenta_id(user_id, )
            #     # send_event("Einkaufen")
            # elif event.lower() == "wasser":
            #     response = tell("MONPLANY_WATER_REMINDER" + _("MONPLANY_FINAl_MSG"))
            #     # send_event("Gesundheit")
            # else:
            #     response = ask("MONPLANY_GYM_REMINDER")
        else:
            response = tell("MONPLANY_ACTIVITY_NOT_FOUND")
    else:
        response = generate_code_response(user_id)
    return response

@skill.intent_handler('TEAM_21_GYM')
def gym_event(user_id:str, hours:int=0, minutes:int=0) -> Response:

    print(hours, ' hours + ', minutes, " minutes.")
    try:
        if user_database.is_user_synced(user_id):
            assert hours > 0 or minutes > 0
            assert hours >= 0 and minutes > 0
            # if send_event("gym", gym_stunden, gym_minutes):
            response = tell(_("MONPLANY_GYM_OK") + _("MONPLANY_FINAl_MSG"))
            # else:
            #   response = tell(_("MONPLANY_GYM_IMPOSSIBLE"))
        else:
            response = generate_code_response(user_id)
    except(AssertionError):
        response = tell("MONPLANY_WRONG_TIME")
    return response
