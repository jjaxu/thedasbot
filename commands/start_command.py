from .botcommand import BotCommand

import sys
sys.path.append('..')

from boterror import BotError
from botquery import BotQuery

class StartCommand(BotCommand):
    def __init__(self, bot_query: BotQuery):
        super().__init__("start")
        self.query = bot_query

    def execute(self) -> str:
        if self.skip_edited(): return None
        if self.query.is_private:
            return "Hello {}! Welcome to the DAS bot!".format(self.query.user_first_name)
        if self.query.is_group:
            return "Hello {}! I am the DAS Bot, {} has summoned me here!".format(
                self.query.chat_title,
                self.query.user_first_name
            )
        return "Greetings from the DAS bot!"
