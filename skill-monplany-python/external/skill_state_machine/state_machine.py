import requests
from skill_sdk.test_helpers import create_context
import pprint
import json


if __name__ == "__main__":
    url = 'http://localhost:4242/v1/monplany'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    context = create_context('TEAM__21__HOBBIES').dict()
    context['locale'] = context['locale']['language']
    context['intent'] = context['intent_name']
    del context['intent_name']
    del context['session']

    session = dict({'id': 123,
               'new': "true",
               'attributes': {
                   "attr-1": "1",
                   "attr-2": "2"
               }})

    data = {
        'context': context,
        'session': session}
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    print(res.text)
