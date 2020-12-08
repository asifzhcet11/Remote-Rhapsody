from skill_sdk import skill, Response, tell, ask
from skill_sdk.l10n import _
from typing import List
import re

@skill.intent_handler('TEAM__21__ASK__HOBBIES')
def handler() -> Response:
    msg = _('MONPLANY_ASK_HOBBIES')
    return tell(msg)

@skill.intent_handler('TEAM__21__TELL__HOBBIES')
def handler(hobbies: str) -> Response:
    print(hobbies)
    hobbies = re.sub(r'[,|.|und]', '', hobbies)
    hobbies = hobbies.split()
    try:
        assert len(hobbies) > 0
        msg = _('MONPLANY_TELL_HOBBIES', hobbies=len(hobbies))
        for id, str in enumerate(hobbies):
            if id == 0:
                msg = msg + ' ' + str
            elif id == len(hobbies)-1:
                msg = msg + ' und ' + str
            else:
                msg = msg + ', ' + str
        msg+= '.'
        response = ask(msg + _("MONPLANY_ASK_SHOPPING"))
    except(AssertionError, ValueError, TypeError):
        msg = _('MONPLANY_EMPTY_HOBBIES')
        response = tell(msg + _("MONPLANY_ASK_SHOPPING"))
    return response

@skill.intent_handler('TEAM__21__SHOPPING')
def handler(shopping: int) -> Response:
    print(shopping)
    if shopping < 0:
        msg = _("MONPLANY_NEGATIVE_SHOPPING_NUMBER")
    elif shopping == 0:
        msg = _("MONPLANY_NULL_SHOPPING_NUMBER")
    elif shopping > 7:
        msg = _("MONPLANY_BIG_SHOPPING_NUMBER")
    else:
        msg = _('MONPLANY_SHOPPING_NUMBER', number=shopping)

    response = tell(msg + _("MONPLANY_ASK_GYM"))
    return response

@skill.intent_handler('TEAM__21__GYM')
def handler(gym: bool) -> Response:
    print(gym)
    if gym :
        msg = _("MONPLANY_GO_GYM")
        response = tell(msg + _("MONPLANY_ASK_NUMBER_GYM"))
    else:
        msg = _("MONPLANY_NOGO_GYM")
        response = tell(msg + _("MONPLONY_FINALIZE"))
    return response

@skill.intent_handler('TEAM__21__NUMBER__GYM')
def handler(number_gym: int) -> Response:
    print(number_gym)
    if number_gym <= 0:
        msg = _("MONPLANY_NEGATIVE_GYM_NUMBER")
    elif number_gym > 7:
        msg = _("MONPLANY_BIG_GYM_NUMBER")
    else:
        msg = _('MONPLANY_GYM_NUMBER', number=number_gym)
    response = tell(msg + _("MONPLONY_FINALIZE"))
    return response
