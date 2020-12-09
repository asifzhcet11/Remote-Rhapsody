from skill_sdk import skill, Response, tell, ask
from skill_sdk.l10n import _
from typing import List
import re

available_events = ["einkaufen", "fitness", "gym", "wasser"]
@skill.intent_handler('TEAM_21_LOGIN')
def ask_login() -> Response:
    # TODO: verify_login()
    # if !verify_login():
    #     response = tell(_('MONPLANY_ASK_LOGIN'))
    # else:
    #     response = ask(_('MONPLANY_OK_LOGIN'))
    # return response
    pass

@skill.intent_handler('TEAM_21_CREATE_EVENT')
def create_event() -> Response:
    # TODO:
    # Check if logged in
    # TODO: verify_login()
    # if !verify_login():
    #     return tell(_('MONPLANY_ASK_LOGIN'))
    # else:
    #     response = ask(_('MONPLANY_EVENT_TYPE'))
    # return reponse
    pass

@skill.intent_handler('TEAM_21_GET_PHONE')
def get_phone(phonenumber : int) -> Response:
    # TODO:
    # if send_phone_number_toserver(phonenumber):
    #    response = ask(_('MONPLANY_LOGIN_DONE'))
    # else:
    #    response = ask(_('MONPLANY_LOGIN_ERROR'))
    pass

@skill.intent_handler('TEAM_21_CREATE_AUTOMATIC_EVENT')
def automatic_event() -> Response:
    # TODO:
    # Check if logged in
    # if verify_login():
    # TODO: verify if automatic plan is possible

    #     if plan_today():
    #       msg = _('MONPLANY_AUTOMATIC_EVENT') + _('MONPLANY_FINAl_MSG')
    #     else:
    #       msg = _('MONPLANY_NO_PLAN_TODAY')
    # else:
    #     msg = _('MONPLANY_ASK_LOGIN')
    # return tell(msg)
    pass


@skill.intent_handler('TEAM_21_ASK_HOBBIES')
def ask_hobbies() -> Response:
    # if verify_login():
    response = ask(_('MONPLANY_ASK_HOBBIES'))
    # else:
    #     response = tell(_('MONPLANY_ASK_LOGIN'))
    return response

@skill.intent_handler('TEAM_21_TELL_HOBBIES')
def plan_hobbies(hobbies: str) -> Response:
    print(hobbies)
    # if verify_login():
    hobbies = re.sub(r'(,|.|und)', '', hobbies)
    hobbies = hobbies.split()
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
        response = ask(msg + _("MONPLANY_FINAl_MSG"))
        # send_event("Hobby",hobbies)
    except(AssertionError, ValueError, TypeError):
        response = ask(_('MONPLANY_EMPTY_HOBBIES'))
    #else:
    #   msg = _('MONPLANY_ASK_LOGIN')
    return response

@skill.intent_handler('TEAM_21_OTHER_EVENTS')
def plan_event(event: str) -> Response:
    # print(event)
    # TODO:
    # Check if logged in
    # if verify_login():
    #     if event.lower() in available_events:
    #         if event.lower() == "einkaufen":
    #             response = tell(_("MONPLANY_SHOP_EVENT") + _("MONPLANY_FINAl_MSG"))
    #             send_event("Einkaufen")
    #         elif event.lower() == "wasser":
    #             response = tell("MONPLANY_WATER_REMINDER" + _("MONPLANY_FINAl_MSG"))
    #             send_event("Gesundheit")
    #         else:
    #             response = ask("MONPLANY_GYM_REMINDER")
    #     else:
    #         response = tell("MONPLANY_ACTIVITY_NOT_FOUND")
    # else:
    #     msg = _('MONPLANY_ASK_LOGIN')
    #     response = tell(msg)
    # return reponse
    pass

@skill.intent_handler('TEAM_21_GYM')
def gym_event(gym_hours:int=0, gym_minutes:int=0) -> Response:

    # print(gym_hours, ' + ', gym_minutes)
    # Check if logged in
    # try:
    # if verify_login():
    #     assert gym_stunden > 0 or gym_minutes > 0
    #     assert gym_minutes>=0 and gym_minutes > 0
    #     if send_event("gym", gym_stunden, gym_minutes):
    #       response = tell(_("MONPLANY_GYM_OK") + _("MONPLANY_FINAl_MSG"))
    #     else:
    #       response = tell(_("MONPLANY_GYM_IMPOSSIBLE"))
    # else:
    #     msg = _('MONPLANY_ASK_LOGIN')
    #     response = tell(msg)
    # except(AssertionError):
    #     response = ask("MONPLANY_WRONG_TIME")
    # return reponse
    pass
