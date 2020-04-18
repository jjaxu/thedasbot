import requests

from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery

class JokeCommand(BotCommand):
    def execute(self):
        result = None
        try:
            response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"})
            if response.ok:
                result = response.content.decode()
        except Exception as err:
            print(f"Unable to fetch joke:\n\t{str(err)}")

        self.handle_normal_query(result or "Oops! Can't fetch joke right now.")
