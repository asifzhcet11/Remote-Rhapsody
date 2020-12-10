import requests
from skill_sdk.test_helpers import create_context
import json

class SkillHTTPRequest:

    def __init__(self,
                 url='http://localhost:4242/v1/monplany',
                 headers=None):

        if headers is None:
            self.headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        else:
            self.headers = headers
        self.url = url

    def create_request(self, intent: str, locale:str = "de", attribute: dict = None) -> dict:
        context = create_context(intent).dict()

        # changes to make the old version works with newer version
        # context['locale'] = context['locale']['language']
        context['locale'] = locale
        context['intent'] = context['intent_name']

        del context['intent_name']
        del context['session']

        session = dict({'id': 123,
                        'new': "true",
                        'attributes': {
                            "attr-1": "1",
                            "attr-2": "2"
                        }})
        if attribute:
            context['attributesV2'].append(attribute)

        return {
            'context': context,
            'session': session
        }

    def call_request(self, data: dict) -> object:
        response = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
        return response.text
