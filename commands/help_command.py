from .botcommand import BotCommand

import sys
sys.path.append('..')

from boterror import BotError
from botquery import BotQuery

class HelpCommand(BotCommand):
    def __init__(self, bot_query: BotQuery):
        super().__init__("help")
        self.query = bot_query

    def execute(self) -> str:
        if self.skip_edited(): return None
        return "You have invoked the help command!"

