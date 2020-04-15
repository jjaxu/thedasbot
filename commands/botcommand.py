from constants import *
from config import *
import requests

# This class defines the base class that all commands for the bot must inherit from
class BotCommand(object):
    def __init__(self, query):
        super().__init__()
        self.query = query
        self.ignore_edited = True
        self.parse_mode = None
        self.other_params = None

    def skip_edited(self) -> bool:
        return self.query.is_edited and self.ignore_edited

    def execute(self):
        raise NotImplementedError("Method is not implemented, did you forget to override?")

    def handle_normal_query(self, response):
        if self.query.is_edited and not ALLOW_EDITED_MESSAGES:
            return

        data = dict()

        if response is None:
            print("Response is None: nothing sent back")
            return
            
        if self.parse_mode:
            data[PARSE_MODE_KEY] = self.parse_mode

        if self.other_params:
            data.update(self.other_params)

        data[CHAT_ID_KEY] = self.query.chat_id
        data[TEXT_KEY] = response

        url = f"{BASE_URL}/{SEND_MESSAGE_ENDPOINT}"
        res = requests.post(url, json=data)
        if not res.ok:
            print(f"sendMessage did not complete successfully. Code: {res.status_code}\n\t{res.text}")

    def handle_inline_query(self):
        pass

    def handle_callback_query(self):
        pass
