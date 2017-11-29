from datetime import datetime
from enum import Enum

import requests


class METHOD(Enum):
    GET_UPDATES = "getupdates"
    SEND_MESSAGE = "sendMessage"


class BotService:

    def __init__(self, token):
        self.token = token
        self.api = "https://api.telegram.org/bot{}/".format(token)
        self.chat_ids = set()
        self.offset = None
        self.timeout = 30

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.api + METHOD.SEND_MESSAGE.value, params)
        return response

    def get_updates(self):
        print("Getting updates at ", str(datetime.now()))
        params = {'timeout': self.timeout, 'offset': self.offset}
        response = requests.post(self.api + METHOD.GET_UPDATES.value, params)
        results = response.json()['result']

        for result in results:
            self.offset = get_update_id(result)
            print("     update_id: ", self.offset, ", chat_id: ", get_chat_id(result))
            self.chat_ids.add(get_chat_id(result))

        return response.json()

    def get_last_update(self):
        result = self.get_updates()

        if len(result) > 0:
            last_update = result[-1]
        else:
            last_update = result[len(result)]

        return last_update

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def get_update_id(update):
    chat_id = update['update_id']
    return chat_id


def parse_chat_id(updates):
    ids = set()
    results = updates['result']

    for result in results:
        ids.add(get_chat_id(result))
    return ids



