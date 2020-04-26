from constants import *
from config import *
import requests

# This class defines the base class that all commands for the bot must inherit from
class BotCommand:
    def __init__(self, query, command_arguments=None):
        self.query = query
        self.command_arguments = command_arguments
        self.ignore_edited = True
        self.response_json = None

    def skip_edited(self) -> bool:
        return self.query.is_edited and self.ignore_edited

    def execute(self):
        raise NotImplementedError("Method is not implemented, did you forget to override?")

    def handle_normal_query(self, response):
        if self.skip_edited():
            return

        self.response_json = dict()

        if response is None:
            print("Response is None: nothing sent back")
            return

        self.format_response_json()

        self.response_json[CHAT_ID_KEY] = self.query.chat_id
        self.response_json[TEXT_KEY] = response

        url = f"{BASE_URL}/{SEND_MESSAGE_ENDPOINT}"
        res = requests.post(url, json=self.response_json)
        if not res.ok:
            print(f"sendMessage did not complete successfully. Code: {res.status_code}\n\t{res.text}")

    def format_response_json(self):
        pass

    def handle_inline_query(self):
        pass

    def handle_callback_query(self):
        pass
