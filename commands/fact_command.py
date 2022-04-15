import requests, traceback

from constants import PARSE_MODE_KEY
from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery

FACTS_URL = "https://facts-service.mmsport.voltaxservices.io/widget/properties/mentalfloss/random-facts"

class FactCommand(BotCommand):
    def execute(self):
        result = None
        try:
            response = requests.get(FACTS_URL)
            if response.ok:
                res = response.json()["data"][0]
                fact = res["body"]
                print(res)
                image_url = res["image"]["value"]["url"]
                result = f'<a href="{image_url}">&#x200b;</a>{str(fact)}'
        except Exception:
            print(f"Unable to fetch fact:\n\t{traceback.format_exc()}")

        self.handle_normal_query(result or "Oops! Can't fetch fact right now.")
    
    def format_response_json(self):
        self.response_json[PARSE_MODE_KEY] = "HTML"
