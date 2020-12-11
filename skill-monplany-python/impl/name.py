from skill_sdk import skill, Response, tell, ask
from skill_sdk.l10n import _
from skill_sdk.entities import snake_to_camel

@skill.intent_handler('ASK__NAME')
def handler(name: str) -> Response:
    print(name)
    msg = _('HELLOAPP_ASK_NAME_RESPONSE', name=name)
    return tell(msg)


