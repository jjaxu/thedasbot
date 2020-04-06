import requests

from .botcommand import BotCommand

import sys
sys.path.append('..')

from boterror import BotError
from botquery import BotQuery

class JokeCommand(BotCommand):
    def __init__(self, bot_query: BotQuery):
        super().__init__("joke")
        self.query = bot_query

    def execute(self) -> str:
        try:
            response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"})
            if response.ok:
                return response.content.decode()
        except Exception as err:
            print("Unable to fetch joke:\n\t{}".format(str(err)))
        return "Oops! Can't fetch joke right now."
