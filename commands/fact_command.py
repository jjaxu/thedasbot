import requests

from constants import *
from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery

class FactCommand(BotCommand):
    def execute(self):
        result = None
        try:
            response = requests.get("https://www.mentalfloss.com/api/facts", headers={"Accept": "text/plain"})
            if response.ok:
                fact = response.json()[0]
                result = f'<a href="{fact["primaryImage"]}">&#x200b;</a>{str(fact["headline"])}'
        except Exception as err:
            print(f"Unable to fetch fact:\n\t{str(err)}")

        self.handle_normal_query(result or "Oops! Can't fetch fact right now.")
    
    def format_response_json(self):
        self.response_json[PARSE_MODE_KEY] = "HTML"
