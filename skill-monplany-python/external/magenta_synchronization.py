from random import randint
import requests
import json
from urllib.parse import urlencode


class MagentaSyncronization:
    MSG_API_ENDPOINT = 'https://developer-api.telekom.com/vms/Messages.json'
    NUM_OF_DIGITS = 5
    FROM = 'MonPlany'
    LINK = 'http:localhost:4200/'
    MESSAGE = '{} is your MonPlany sync code.'
    HEADERS = {
        'Authorization': '5f63efb2394b9800019ed6e46235fb58825b4540837a8f1f7a76da41',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }

    # TODO User login test
    def is_user_available(self):
        pass

    def generate_sync_code(self, n=5):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def send_code(self, to: str, code: str):
        # TODO: check number validity
        # send request
        data = urlencode({'From': MagentaSyncronization.FROM,
                          'To': to,
                          'Body': MagentaSyncronization.MESSAGE.format(code)})
        response = requests.post(url=MagentaSyncronization.MSG_API_ENDPOINT,
                                 data=data,
                                 headers=MagentaSyncronization.HEADERS)
        print(response.text)

