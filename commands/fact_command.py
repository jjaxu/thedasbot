import requests

from .botcommand import BotCommand

import sys
sys.path.append('..')

from boterror import BotError
from botquery import BotQuery

class FactCommand(BotCommand):
    def __init__(self, bot_query: BotQuery):
        super().__init__("fact")
        self.query = bot_query
        self.parse_mode = "HTML"

    def execute(self) -> str:
        try:
            response = requests.get("https://www.mentalfloss.com/api/facts", headers={"Accept": "text/plain"})
            if response.ok:
                return str(response.json()[0]['headline'])
        except Exception as err:
            print("Unable to fetch fact:\n\t{}".format(str(err)))
        return "Oops! Can't fetch fact right now."
