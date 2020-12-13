from random import randint
import requests
from urllib.parse import urlencode


class MagentaSyncronizer:
    MSG_API_ENDPOINT = 'https://developer-api.telekom.com/vms/Messages.json'
    NUM_OF_DIGITS = 5
    FROM = 'Monplany'
    LINK = 'http:localhost:4200/'
    MESSAGE = '{} is your Monplany sync code.'
    HEADERS = {
        'Authorization': '5f63efb2394b9800019ed6e46235fb58825b4540837a8f1f7a76da41',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }

    # TODO User login test
    def is_user_available(self):
        pass

    def generate_sync_code(self, n=4):
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1
        return randint(range_start, range_end)

    def send_code(self, to: str, code: str):
        # TODO: check number validity
        # send request
        data = urlencode({'From': MagentaSyncronizer.FROM,
                          'To': to,
                          'Body': MagentaSyncronizer.MESSAGE.format(code)})
        response = requests.post(url=MagentaSyncronizer.MSG_API_ENDPOINT,
                                 data=data,
                                 headers=MagentaSyncronizer.HEADERS)
        print(response.text)

    def send_msg(self, to: str, msg: str):
        # TODO: check number validity
        # send request
        data = urlencode({'From': MagentaSyncronizer.FROM,
                          'To': to,
                          'Body': msg})
        response = requests.post(url=MagentaSyncronizer.MSG_API_ENDPOINT,
                                 data=data,
                                 headers=MagentaSyncronizer.HEADERS)
        print(response.text)

